"""One bounded all3 official-entry regression plus unchanged role/branch spies."""
import ast
import copy
import json
import os
from pathlib import Path
import sys
import threading
import time
import traceback

START=time.perf_counter()
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
sys.path.insert(0,str(HERE))
for variable in ('OMP_NUM_THREADS','MKL_NUM_THREADS','OPENBLAS_NUM_THREADS','NUMEXPR_NUM_THREADS'):
    os.environ[variable]='2'


def main():
    import psutil
    process=psutil.Process();process.cpu_affinity(process.cpu_affinity()[:2])
    from schema_entry import runtime_entry,official_loader,CONFIG,KIT
    from orchestration import layout
    import tests_model_free
    loader=official_loader();config=loader.load_config(str(CONFIG))
    fixture=ROOT/'tmp/a040-full-path-local-retry1/schema-entry-fixtures'
    reports=[];negatives=[]
    expected={'unicef':(7,12,14885,1488),'world_bank':(9,76,5195,520),'unhcr':(17,213,8279,621)}
    for name,(ng,nh,nf,nq) in expected.items():
        path=KIT/'data'/(name+'.json')
        raw=json.loads(path.read_text(encoding='utf-8'))
        schema,metadata=runtime_entry(path)
        direct=loader.load_schema(str(path),config)
        assert json.dumps(schema,ensure_ascii=False)==json.dumps(direct,ensure_ascii=False)
        assert list(schema['items'])==list(raw['items'])
        given,heads,options=layout(schema)
        assert given==[n for n,r in raw['items'].items() if r['class']=='GIVEN']
        assert heads==[n for n,r in raw['items'].items() if r['class']=='PREDICT']
        assert (len(given),len(heads),schema['split']['n_train'],schema['split']['n_dev'])==(ng,nh,nf,nq)
        assert sum(schema['split'][key] for key in ('n_train','n_dev','n_test'))==schema['dataset']['n_rows']
        assert ('gated_value' in raw)==(name=='unhcr')
        assert schema['gated_value']==config['gated_value']
        for item,values in options.items():
            assert values==loader.options_for(direct,item)==metadata['options'][item]
            spec=raw['items'][item];gated=bool(spec.get('gate'))
            assert values[:len(spec['values'])]==spec['values']
            assert len(values)==len(spec['values'])+int(gated)
            assert values.count(config['gated_value'])==int(gated)
            if gated:assert values[-1]==config['gated_value']
        alternate=copy.deepcopy(raw);alternate['gated_value']='CONTRADICTORY_RAW_METADATA'
        altered=fixture/(name+'-raw-override.json')
        with altered.open('x',encoding='utf-8') as stream:json.dump(alternate,stream)
        changed,changed_metadata=runtime_entry(altered)
        assert changed==schema and changed_metadata['runtime_sha256']==metadata['runtime_sha256']
        reports.append(dict(instrument=name,given=len(given),heads=len(heads),visible=nf,query=nq,
                            vectors=nh*nq,probability_width=sum(len(options[h]) for h in heads),metadata=metadata))
    assert sum(r['vectors'] for r in reports)==189649
    assert reports[-1]['probability_width']==834
    template=json.loads((KIT/'data/unicef.json').read_text(encoding='utf-8'))
    cases=[]
    def invalid(label,mutate):
        data=copy.deepcopy(template);mutate(data);cases.append((label,data))
    first=next(iter(template['items']))
    invalid('missing_values',lambda s:s['items'][first].update(values=[]))
    invalid('null_option',lambda s:s['items'][first].update(values=[None]))
    invalid('numeric_option',lambda s:s['items'][first].update(values=[123]))
    invalid('sentinel_in_values',lambda s:s['items'][first].update(values=[config['gated_value']]))
    invalid('missing_parent',lambda s:s['items'][first].update(gate={'parent':'MISSING'}))
    invalid('dataset_field',lambda s:s['dataset'].pop('version'))
    invalid('dataset_rows',lambda s:s['dataset'].update(n_rows=0))
    invalid('split_missing',lambda s:s['split'].pop('n_train'))
    invalid('split_type',lambda s:s['split'].update(n_train=True))
    invalid('split_total',lambda s:s['split'].update(n_train=s['split']['n_train']+1))
    for label,data in cases:
        path=fixture/(label+'.json')
        with path.open('x',encoding='utf-8') as stream:json.dump(data,stream)
        messages=[]
        for call in (lambda:loader.load_schema(str(path),config),lambda:runtime_entry(path)):
            try:call()
            except ValueError as exc:messages.append(str(exc))
            else:raise AssertionError('Invalid schema silently accepted: '+label)
        assert messages[0]==messages[1]
        negatives.append(dict(case=label,expected_exception='ValueError',message=messages[0]))
    import yaml
    bad_config=copy.deepcopy(config);bad_config['phases'][1]['noised']='not_boolean'
    config_path=fixture/'invalid-config.yml'
    with config_path.open('x',encoding='utf-8') as stream:yaml.safe_dump(bad_config,stream)
    try:runtime_entry(KIT/'data/unicef.json',config_path)
    except ValueError as exc:negatives.append(dict(case='invalid_config',expected_exception='ValueError',message=str(exc)))
    else:raise AssertionError('Invalid config silently accepted')
    connections=[]
    for name in ('generate_fixture.py','runner.py'):
        tree=ast.parse((HERE/name).read_text(encoding='utf-8-sig'))
        imported=[n for n in ast.walk(tree) if isinstance(n,ast.ImportFrom) and n.module=='schema_entry'
                  and any(a.name=='runtime_entry' for a in n.names)]
        assignments=[n for n in ast.walk(tree) if isinstance(n,ast.Assign) and isinstance(n.value,ast.Call)
                     and isinstance(n.value.func,ast.Name) and n.value.func.id=='runtime_entry']
        assert len(imported)==len(assignments)==1
        assert isinstance(assignments[0].targets[0],ast.Tuple)
        assert [n.id for n in assignments[0].targets[0].elts]==['schema','runtime_metadata']
        connections.append(name)
    spy=tests_model_free.main()
    assert not any(n in sys.modules for n in ('torch','tabicl','adapter','runner','e041'))
    return dict(outcome='PASS_MODEL_FREE_ONLY',entry_outcome='ALL3_RUNTIME_ENTRY_PASS',schemas=reports,
                expected_negative_cases=negatives,actual_connections=connections,spies=spy,
                model_imports=0,scientific_fits=0)


if __name__=='__main__':
    timer=threading.Timer(60,lambda:os._exit(2));timer.daemon=True;timer.start()
    result={};code=1
    try:
        result=main();code=0
    except BaseException as exc:
        result=dict(outcome='LOCAL_FULL_PATH_FAIL',error=repr(exc),traceback=traceback.format_exc())
    result['elapsed_seconds']=time.perf_counter()-START
    if result['elapsed_seconds']>=60:result['outcome']='LOCAL_RESOURCE_LIMIT';code=1
    with (HERE/'model-free-result.json').open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
    timer.cancel()
    print(json.dumps({k:v for k,v in result.items() if k not in ('schemas','spies','expected_negative_cases')}))
    sys.exit(code)
