"""Explicit official runtime-schema entry; no response generation or scoring."""
from functools import lru_cache
import hashlib
import importlib.util
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
KIT = ROOT / 'external/starter-kit'
CONFIG = KIT / 'config.yml'


@lru_cache(maxsize=1)
def official_loader():
    spec = importlib.util.spec_from_file_location('a040_official_schema', KIT / 'make_sandbox.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def runtime_entry(schema_path, config_path=CONFIG):
    schema_path, config_path = Path(schema_path), Path(config_path)
    loader = official_loader()
    config = loader.load_config(str(config_path))
    schema = loader.load_schema(str(schema_path), config)
    canonical = json.dumps(schema, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    metadata = dict(raw_sha256=sha256(schema_path), config_sha256=sha256(config_path),
                    loader_sha256=sha256(KIT / 'make_sandbox.py'),
                    runtime_sha256=hashlib.sha256(canonical).hexdigest(),
                    runtime_hash_encoding='UTF-8 JSON ensure_ascii=False,separators=comma/colon,original key order',
                    item_order=list(schema['items']),
                    options={n:loader.options_for(schema,n) for n,r in schema['items'].items()
                             if r['class'] in ('GIVEN','PREDICT')})
    return schema, metadata
