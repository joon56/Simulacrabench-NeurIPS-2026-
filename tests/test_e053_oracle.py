"""Mathematical and isolation checks for the E053 diagnostic."""
import json
import numpy as np
import pandas as pd
import pytest

from scripts import screen_e053 as screen


def test_concave_optimum_and_tangent_bound():
    base = np.array([.2, .8, .4, .6])
    evidence = np.array([.9, .2, .7, .3])
    result = screen.optimize_bucket(base, evidence, 2)
    grid = np.linspace(0, .98, 20001)
    scores = np.log(.001 + .998 * (base[:, None] + grid * (evidence-base)[:, None])).mean(0)
    assert result['log_upper'] >= scores.max()-1e-12
    assert result['log_score'] >= scores.max()-1e-8
    assert result['log_upper']-result['log_score'] <= 1e-9


@pytest.mark.parametrize('base,evidence,expected', [([.2],[.8],.98),([.8],[.2],0),([.5],[.5],0)])
def test_boundaries_and_flat_objective(base, evidence, expected):
    assert screen.optimize_bucket(np.array(base), np.array(evidence), 2)['lambda'] == expected


def test_missing_evidence_retains_identity_and_scores_all_cells():
    base = {'a': np.array([[.8,.2],[.2,.8]]), 'b':np.array([[.6,.4],[.6,.4]])}
    lib = {'base':base,'identity':base,'evidence':{'a':np.array([[.1,.9],[.9,.1]]),'b':np.zeros((2,2))},
           'available':{'a':np.ones(2,dtype=bool),'b':np.zeros(2,dtype=bool)},
           'concentration':np.array([False,True]),'legacy_returned':False}
    result = screen.score_family(lib, {'a':np.array([1,0]),'b':np.array([0,0])}, np.arange(2), False)
    assert result['delta_skill'] > 0
    assert result['cells']==4
    assert result['changed_vectors']==2
    returned = screen.score_family(lib, {'a':np.array([1,0]),'b':np.array([0,0])}, np.arange(2), True)
    assert returned['delta_skill']==0


def test_existing_output_refuses_before_loading(tmp_path, monkeypatch):
    (tmp_path/'adult-seed54-manifest.json').write_text('{}')
    monkeypatch.setattr(screen,'prepare',lambda seed: pytest.fail('loaded before refusal'))
    with pytest.raises(FileExistsError):
        screen.run(54,tmp_path)


def test_partition_hides_every_outer_answer():
    frame=pd.DataFrame({'g':['x']*5000,'y':['a']*5000})
    schema={'items':{'g':{'class':'GIVEN','values':['x']},'y':{'class':'PREDICT','values':['a','b']}}}
    masked, parts=screen.split_frame(frame,schema)
    assert masked.y.iloc[:2600].notna().all()
    assert masked.y.iloc[2600:].isna().all()
    assert masked.g.notna().all()
    assert sum(map(len,parts.values()))==5000
    assert len(set(np.concatenate(list(parts.values()))))==5000


def test_capture_dormant_recipe_without_refit(monkeypatch):
    from src.models import supervised_retrieval as module
    from src.models.hier_backoff import _layout
    frame=pd.DataFrame({'g':[str(i%3) for i in range(610)],'y':['a' if i%2 else 'b' for i in range(610)]})
    frame.loc[600:,'y']=np.nan
    schema={'items':{'g':{'class':'GIVEN','values':['0','1','2']},'y':{'class':'PREDICT','values':['a','b']}},'gated_value':'NA_GATED'}
    calls=[]
    def fit(*args,**kwargs):
        calls.append(1)
        return [np.asarray(args[5]).copy()],[],[]
    monkeypatch.setattr(module,'fit_sections',fit)
    monkeypatch.setattr(module,'_best_lambda',lambda *args:0.)
    capture=screen.capture_layer(frame,schema,{'y':np.full((610,2),.5)})
    assert len(calls)==1
    assert capture['legacy_evidence']=={} and capture['lambdas']=={}
    assert set(capture['evidence'])==set(range(600,610))
    assert capture['materialized_dormant']
    assert capture['query_donor_checks'] > 0
    for ev,_ in capture['evidence'].values():
        assert np.isclose(ev['y'].sum(),1)


@pytest.mark.parametrize('active',[[],[0]])
def test_nonempty_capture_matches_original(monkeypatch, active):
    from src.models import supervised_retrieval as module
    frame=pd.DataFrame({'g':[str(i%3) for i in range(610)],'y':['a' if i%2 else 'b' for i in range(610)]})
    frame.loc[600:,'y']=np.nan
    schema={'items':{'g':{'class':'GIVEN','values':['0','1','2']},'y':{'class':'PREDICT','values':['a','b']}},'gated_value':'NA_GATED'}
    monkeypatch.setattr(module,'fit_sections',lambda *args,**kw:([np.asarray(args[5]).copy()],active,[]))
    monkeypatch.setattr(module,'_best_lambda',lambda *args:.5)
    model={'y':np.full((610,2),.5)}
    expected, weights=module.supervised_layer(frame,schema,model)
    captured=screen.capture_layer(frame,schema,model)
    assert captured['lambdas']==weights
    assert not captured['materialized_dormant']
    for row in expected:
        assert captured['evidence'][row][1]==expected[row][1]
        assert np.array_equal(captured['evidence'][row][0]['y'],expected[row][0]['y'])


def test_probability_validation_rejects_invalid_endpoint():
    with pytest.raises(ValueError):
        screen.normalized(np.array([[.5,-.5]]))
    with pytest.raises(ValueError):
        screen.normalized(np.array([[.5,.4]]))


def test_freezes_artifacts_before_oracle_scoring(tmp_path, monkeypatch):
    frame=pd.DataFrame({'g':['x']*5000,'y':['a']*5000})
    schema={'items':{'g':{'class':'GIVEN','values':['x']},'y':{'class':'PREDICT','values':['a','b']}}}
    masked,parts=screen.split_frame(frame,schema)
    monkeypatch.setattr(screen,'prepare',lambda seed:(frame,schema,masked,parts,{}))
    lib={'base':{'y':np.full((2400,2),.5)},'identity':{'y':np.full((2400,2),.5)},
         'evidence':{'y':np.zeros((2400,2))},'available':{'y':np.zeros(2400,dtype=bool)},
         'concentration':np.zeros(2400,dtype=bool),'query':np.arange(2600,5000),
         'predicted':['y'],'options':{'y':['a','b']},'legacy_returned':False,
         'capture':{'lambdas':{},'materialized_dormant':False}}
    monkeypatch.setattr(screen,'build_library',lambda *args:lib)
    original=screen.score_family
    def checked(*args):
        m=json.loads((tmp_path/'adult-seed54-manifest.json').read_text())
        assert screen.digest((tmp_path/'adult-seed54-capture.pkl.gz').read_bytes())==m['capture_sha256']
        assert screen.digest((tmp_path/'adult-seed54-arrays.npz').read_bytes())==m['arrays_sha256']
        return original(*args)
    monkeypatch.setattr(screen,'score_family',checked)
    result=screen.run(54,tmp_path)
    assert result['gate']=='STOP'
    assert result['selection_or_audit_evaluated'] is False
    assert result['uncensored_bucket']['cells']==800


def test_gated_schema_rejected_before_fitting():
    frame=pd.DataFrame({'g':['a'],'y':[np.nan]})
    schema={'items':{'g':{'class':'GIVEN','values':['a']},
                    'y':{'class':'PREDICT','values':['x'],'gate':{'parent':'g','observed_if':['a']}}},
            'gated_value':'NA_GATED'}
    with pytest.raises(ValueError,match='ungated'):
        screen.build_library(frame,schema)
