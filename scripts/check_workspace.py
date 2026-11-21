"""Read-only workspace wiring check. No scientific imports, data reads or writes."""
import argparse
import hashlib
from importlib import metadata
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (
    'AGENTS.md', 'CLAUDE.md', 'README.md', 'docs/status.md', 'docs/workflow.md',
    'docs/session-prompts.ko.md', 'docs/index.md', 'docs/codex-setup.ko.md',
    '.agents/skills/paper-session/SKILL.md', '.claude/skills/paper-session/SKILL.md',
    'requirements.txt', 'requirements-models.txt',
)
PACKAGES = ('numpy', 'pandas', 'pytest', 'pyarrow', 'PyYAML',
            'scipy', 'scikit-learn', 'torch', 'threadpoolctl')


def missing_links(root, name, text):
    """Check file targets only, not heading anchors or remote URLs."""
    missing = []
    for target in re.findall(r'(?<!!)\[[^\]\n]+\]\(([^)\n]+)\)', text):
        target = target.strip().strip('<>')
        parts = urlsplit(target)
        if parts.scheme or parts.netloc or not parts.path:
            continue
        destination = (root / name).parent / unquote(parts.path)
        if not destination.resolve().is_relative_to(root.resolve()) or not destination.exists():
            missing.append(f'{name}: {target}')
    return missing


def check_documents(root):
    root = root.resolve()
    texts, hashes, errors = {}, {}, []
    for name in DOCUMENTS:
        path = root / name
        if not path.resolve().is_relative_to(root):
            errors.append(f'{name}: resolves outside workspace')
            continue
        try:
            content = path.read_bytes()
            texts[name] = content.decode('utf-8-sig')
            hashes[name] = hashlib.sha256(content).hexdigest()
        except (OSError, UnicodeError) as exc:
            errors.append(f'{name}: {type(exc).__name__}')
    for name, content in texts.items():
        errors.extend(missing_links(root, name, content))
    for target in ('CLAUDE.md', 'docs/status.md', 'docs/log.md', 'docs/workflow.md'):
        if target not in texts.get('AGENTS.md', '') or not (root / target).is_file():
            errors.append(f'AGENTS.md: missing entry reference or file {target}')
    workflow = texts.get('docs/workflow.md', '')
    revision = re.search(r'Role/entry revision:\s*\*\*([^*]+)\*\*', workflow)
    if not revision:
        errors.append('docs/workflow.md: missing revision')
    elif revision[1] not in texts.get('docs/session-prompts.ko.md', ''):
        errors.append('docs/session-prompts.ko.md: workflow revision mismatch')
    skill = texts.get('.agents/skills/paper-session/SKILL.md', '')
    if '.claude/skills/paper-session/SKILL.md' not in skill:
        errors.append('Codex paper-session: missing shared protocol reference')
    for name in ('.agents/skills/paper-session/SKILL.md',
                 '.claude/skills/paper-session/SKILL.md'):
        if not re.match(r'\A---\r?\nname: paper-session\r?\ndescription:', texts.get(name, '')):
            errors.append(f'{name}: missing skill metadata')
    return {'errors': errors, 'sha256': hashes,
            'workflow_revision': revision[1] if revision else None}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    result = check_documents(args.root)
    versions = {}
    for package in PACKAGES:
        try:
            versions[package] = metadata.version(package)
        except metadata.PackageNotFoundError:
            versions[package] = None
    missing = [name for name, version in versions.items() if version is None]
    result.update(
        status='FAIL' if result['errors'] else 'PASS_DOCUMENT_WIRING',
        python=sys.version.split()[0], executable=sys.executable, packages=versions,
        warnings=([f'Packages absent in this interpreter: {", ".join(missing)}'] if missing else []),
        limits=['Static wiring only; not proof of agent loading or compliance.',
                'Package metadata only; not import, ABI, model or release validation.',
                'No log contents, response files, caches, models or archives read.',
                'No git commands, network requests or file writes.'],
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if result['errors'] else 0


if __name__ == '__main__':
    raise SystemExit(main())
