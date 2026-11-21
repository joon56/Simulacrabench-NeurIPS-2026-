"""New orchestration spies only; no scientific model imports or fits."""
import ast
import inspect
import io
import json
import os
from pathlib import Path
import sys
import time
import threading

START = time.perf_counter()
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))


def main():
    for name in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
        os.environ[name]='2'
    import numpy as np
    import pandas as pd
    import orchestration as o
    from telemetry import EventLog
    sink = io.StringIO()
    log = EventLog(sink)
    log.emit('probe', head_name='head', classes=15)
    assert json.loads(sink.getvalue())['head_name'] == 'head'
    sites = 0
    for path in HERE.glob('*.py'):
        if path.name == Path(__file__).name:
            continue
        tree=ast.parse(path.read_text(encoding='utf-8-sig'))
        expansions={}
        for assignment in ast.walk(tree):
            if not isinstance(assignment,ast.Assign):continue
            for target in assignment.targets:
                if isinstance(target,ast.Name):
                    value=assignment.value
                    if isinstance(value,ast.Dict):
                        expansions.setdefault(target.id,set()).update(k.value for k in value.keys if isinstance(k,ast.Constant))
                    elif isinstance(value,ast.Call) and isinstance(value.func,ast.Name) and value.func.id=='dict':
                        expansions.setdefault(target.id,set()).update(k.arg for k in value.keywords if k.arg is not None)
                elif isinstance(target,ast.Subscript) and isinstance(target.value,ast.Name) and isinstance(target.slice,ast.Constant):
                    expansions.setdefault(target.value.id,set()).add(target.slice.value)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == 'emit':
                keywords={k.arg:None for k in node.keywords if k.arg is not None}
                for k in node.keywords:
                    if k.arg is None:
                        assert isinstance(k.value,ast.Name) and k.value.id in expansions
                        for key in expansions[k.value.id]:
                            assert key not in keywords
                            keywords[key]=None
                assert not {'event','elapsed'} & set(keywords)
                inspect.signature(log.emit).bind(*[None for _ in node.args], **keywords)
                sites += 1
    schema = {'gated_value': 'NA_GATED', 'items': {
        'g': {'class': 'GIVEN', 'values': ['a', 'b']},
        's3_11_intent_return_12m_lbl': {'class': 'PREDICT', 'values': ['n', 'y']},
        'h': {'class': 'PREDICT', 'values': ['n', 'y']}}}
    heads = list(schema['items'])[1:]
    frame = pd.DataFrame({'g': ['a', 'b']*5,
                          heads[0]: ['n', 'y']*4+[np.nan]*2,
                          heads[1]: ['y', 'n']*4+[np.nan]*2})
    plan = o.RolePlan((0,1,2,3), (4,5), (6,7), (8,9))
    traces = []
    for accepted in (False, True):
        calls = []
        class Math:
            @staticmethod
            def select_alpha(p, q, truth):
                calls.append('S')
                assert list(truth[heads[0]]) == [0, 1]
                return .5
            @staticmethod
            def independent_check(p, q, truth, alpha):
                calls.append('E')
                assert alpha == .5 and list(truth[heads[1]]) == [1, 0]
                return accepted, 0.1 if accepted else -0.1
            @staticmethod
            def mix(p, q, alpha):
                return p if alpha == 0 else (1-alpha)*p + alpha*q
        raw_by_stage = {}
        def base(f, s, stage, fit_rows):
            calls.append(stage)
            assert set(f.index[f[heads].notna().all(axis=1)]) == set(fit_rows)
            outside = sorted(set(f.index)-set(fit_rows))
            assert f.loc[outside, heads].isna().all().all()
            values = [[.2+row*.01, .8-row*.01] for row in outside for _ in heads]
            raw_by_stage[stage] = values
            return values
        def expert(view, stage):
            calls.append(stage)
            assert view.query_rows == ([4,5,6,7] if stage == 'expert_shadow' else [8,9])
            for head in heads:
                X, y = view.fit_input(head)
                assert list(X.index) == list(view.fit_rows) and list(X.columns) == ['g']
                assert len(y) == (4 if stage == 'expert_shadow' else 8)
            return {h: np.tile([.4,.6], (len(view.query_rows),1)) for h in heads}
        predictor = o.FullPathPredictor(base, expert, Math, log)
        saved = frame.copy(deep=True)
        natural = predictor.predict(frame, schema, plan)
        assert frame.equals(saved)
        assert calls[:4] == ['unhcr_shadow','expert_shadow','S','E']
        assert calls[4] == 'unhcr_final'
        assert calls.count('expert_final') == int(accepted)
        if not accepted:
            assert natural is raw_by_stage['unhcr_final']
        engineering = predictor.engineering_active()
        assert calls.count('expert_final') == 1 and len(engineering) == 4
        assert predictor.render_final(0) is raw_by_stage['unhcr_final']
        assert predictor.render_final(.25, empty=True) is raw_by_stage['unhcr_final']
        predictor.engineering_active()
        assert calls.count('expert_final') == 1
        assert predictor.last['alpha'] == .5 and predictor.last['accepted'] == accepted
        traces.append({'accepted':accepted,'calls':calls})
    sealed = o.SealedRoles(frame,schema,plan)
    try:
        sealed.evaluation()
    except PermissionError:
        pass
    else:
        raise AssertionError('Early E access allowed')
    bad = sealed.shadow.copy();bad.loc[4,heads[0]]='n'
    try:
        o.FitView(bad,schema,plan.fit,plan.selection+plan.evaluation)
    except PermissionError:
        pass
    else:
        raise AssertionError('Unmasked held target allowed')
    controls = {'gated_value':'NA_GATED','items':{'g':schema['items']['g'],'h':schema['items']['h']}}
    marker = [[.4,.6],[.6,.4]]
    control = o.FullPathPredictor(lambda *args:marker, lambda *args: (_ for _ in ()).throw(AssertionError('Control expert')), Math, log)
    assert control.predict(frame[['g','h']],controls) is marker
    assert o.restore([[.1,.9],[.2,.8],[.3,.7],[.4,.6]],heads,[4,6],{h:['n','y'] for h in heads})[heads[1]].tolist()==[[.2,.8],[.4,.6]]
    assert not any(n in sys.modules for n in ('torch','tabicl','adapter','runner','e041'))
    return {'outcome':'PASS_MODEL_FREE_ONLY','traces':traces,'logger_sites':sites,'scientific_fits':0,'model_imports':0}


if __name__ == '__main__':
    timer=threading.Timer(60,lambda:os._exit(2));timer.daemon=True;timer.start()
    result = main()
    result['elapsed_seconds'] = time.perf_counter()-START
    assert result['elapsed_seconds'] < 60
    with (HERE/'model-free-result.json').open('x',encoding='utf-8') as stream:
        json.dump(result,stream,indent=2)
    timer.cancel()
    print(json.dumps(result))
