"""Stdlib-only AST regression; never imports either scientific runner."""
import ast
import hashlib
import inspect
import io
import json
import os
from pathlib import Path
import sys
import threading
import time
from types import SimpleNamespace

START = time.perf_counter()
HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'local-technical'
RESULT = HERE / 'logging-regression.json'


def timeout():
    RESULT.write_text(json.dumps({'outcome': 'INCOMPLETE', 'reason': '60s model-free cap'}))
    os._exit(2)


def actual_logger(directory):
    tree = ast.parse((directory / 'runner.py').read_text(encoding='utf-8-sig'))
    node = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'event')
    sink = io.StringIO()
    namespace = dict(EVENTS=sink, json=json, time=time, START=START)
    module = ast.Module(body=[node], type_ignores=[])
    exec(compile(module, str(directory / 'runner.py'), 'exec'), namespace)
    return namespace['event'], sink, ast.dump(node, include_attributes=False)


def event_calls(directory):
    result = []
    for filename in ('runner.py', 'tests_local.py', 'prototype.py', 'watchdog.py'):
        tree = ast.parse((directory / filename).read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'event':
                result.append((filename, node))
    return result


def main():
    before, old_sink, old_ast = actual_logger(OLD)
    after, sink, new_ast = actual_logger(HERE)
    assert old_ast == new_ast, 'Logger implementation unexpectedly changed'
    original = next(n for _, n in event_calls(OLD)
                    if isinstance(n.args[0], ast.Constant) and n.args[0].value == 'many_class_head')
    corrected = next(n for _, n in event_calls(HERE)
                     if isinstance(n.args[0], ast.Constant) and n.args[0].value == 'many_class_head')
    environment = dict(name='fixture_head', estimator=SimpleNamespace(n_classes_=15))
    try:
        eval(compile(ast.Expression(original), '<original-call>', 'eval'), dict(event=before, **environment))
    except TypeError as exc:
        original_error = str(exc)
        assert "multiple values for argument 'name'" in original_error
    else:
        raise AssertionError('Original collision was not reproduced')
    assert old_sink.getvalue() == ''
    eval(compile(ast.Expression(corrected), '<corrected-call>', 'eval'), dict(event=after, **environment))
    payload = json.loads(sink.getvalue())
    assert payload['event'] == 'many_class_head'
    assert payload['head_name'] == 'fixture_head' and payload['classes'] == 15
    assert 'name' not in payload and set(payload) == {'event', 'elapsed', 'head_name', 'classes'}
    sites = []
    for filename, node in event_calls(HERE):
        assert not any(isinstance(x, ast.Starred) for x in node.args)
        assert all(x.arg is not None for x in node.keywords)
        keywords = {x.arg: 0 for x in node.keywords}
        inspect.signature(after).bind(*[0 for _ in node.args], **keywords)
        assert 'event' not in keywords and 'elapsed' not in keywords
        sites.append(dict(file=filename, line=node.lineno, keywords=list(keywords)))
    # Only literal consumer references in the actual implementation are allowed.
    consumers = []
    for filename in ('runner.py', 'tests_local.py', 'prototype.py', 'watchdog.py'):
        tree = ast.parse((HERE / filename).read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) and node.slice.value in ('head_name', 'name'):
                consumers.append(dict(file=filename, line=node.lineno, key=node.slice.value))
    assert consumers == [], consumers
    forbidden = [n for n in sys.modules if n == 'torch' or n.startswith('torch.') or
                 n == 'tabicl' or n.startswith('tabicl.') or n in ('prototype', 'runner', 'tests_local')]
    assert not forbidden
    return dict(outcome='PASS_MODEL_FREE_ONLY', original_error=original_error,
                actual_logger_ast_sha256=hashlib.sha256(old_ast.encode()).hexdigest(),
                payload=payload, call_sites=sites, call_sites_checked=len(sites),
                affected_consumers=consumers, forbidden_imports=forbidden,
                scientific_processes=0, logger_imported=False)


if __name__ == '__main__':
    timer = threading.Timer(60, timeout)
    timer.daemon = True
    timer.start()
    code = 1
    try:
        result = main()
        code = 0
    except BaseException as exc:
        result = dict(outcome='LOCAL_CONTRACT_FAIL', error=repr(exc), scientific_processes=0)
    result['elapsed_seconds'] = time.perf_counter() - START
    assert result['elapsed_seconds'] < 60
    with RESULT.open('x', encoding='utf-8') as stream:
        json.dump(result, stream, indent=2)
    timer.cancel()
    print(json.dumps(result))
    sys.exit(code)
