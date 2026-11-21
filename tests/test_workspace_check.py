"""Workspace checks use generated documentation only, never research fixtures."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/check_workspace.py'
spec = importlib.util.spec_from_file_location('workspace_check', SCRIPT)
check = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check)


class WorkspaceCheckTests(unittest.TestCase):
    def test_missing_entry_is_a_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            result = check.check_documents(Path(directory))
            self.assertTrue(result['errors'])
            self.assertIn('AGENTS.md', ' '.join(result['errors']))

    def test_links_resolve_relative_to_document(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / 'docs').mkdir()
            (root / 'target.md').write_text('ok', encoding='utf-8')
            missing = check.missing_links(
                root, 'docs/index.md', '[ok](../target.md#part) [bad](missing.md) '
                '[web](https://example.org/) [anchor](#part)')
            self.assertEqual(missing, ['docs/index.md: missing.md'])

    def test_paths_outside_workspace_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            missing = check.missing_links(Path(directory), 'README.md',
                                          '[outside](../../outside.md)')
            self.assertEqual(missing, ['README.md: ../../outside.md'])

    def test_bom_is_accepted_and_broken_local_link_is_reported(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in check.DOCUMENTS:
                target = root / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text('ordinary documentation', encoding='utf-8-sig')
            (root / 'README.md').write_text('[missing](gone.md)', encoding='utf-8-sig')
            result = check.check_documents(root)
            self.assertIn('README.md: gone.md', result['errors'])
            self.assertIn('README.md', result['sha256'])

    def test_no_research_content_is_read(self):
        # A directory at a data-like filename would fail any attempted file read.
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ('external/secret.parquet', 'output/model.pkl',
                         'submissions/archive.zip', 'src/models/trap.py'):
                (root / name).mkdir(parents=True)
            result = check.check_documents(root)
            self.assertFalse(any(name.startswith(('external/', 'output/', 'src/',
                                                  'submissions/'))
                                 for name in result['sha256']))


if __name__ == '__main__':
    unittest.main()
