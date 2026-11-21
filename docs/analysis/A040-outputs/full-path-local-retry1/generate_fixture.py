"""New-only fake input generation. No model imports or query truth generation."""
import hashlib
import json
from pathlib import Path
import sys
import time

import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
TEMP=ROOT/'tmp/a040-full-path-local-retry1'
sys.path.insert(0,str(HERE))
from orchestration import layout
from schema_entry import runtime_entry


def main():
    start=time.perf_counter()
    rng=np.random.Generator(np.random.PCG64(4000))
    shuffled=np.random.Generator(np.random.PCG64(4001)).permutation(8279)
    roles={'fit':sorted(shuffled[2000:].tolist()),'selection':sorted(shuffled[:1000].tolist()),
           'evaluation':sorted(shuffled[1000:2000].tolist()),'external':list(range(8279,8900)),
           'permutation':shuffled.tolist(),'permutation_seed':4001}
    with (HERE/'roles.json').open('x',encoding='utf-8') as stream:json.dump(roles,stream)
    records=[]
    for name,nvisible,nquery in [('unicef',14885,1488),('world_bank',5195,520),('unhcr',8279,621)]:
        schema_path=ROOT/'external/starter-kit/data'/(name+'.json')
        schema,runtime_metadata=runtime_entry(schema_path)
        given,heads,options=layout(schema);n=nvisible+nquery
        columns={}
        blocks=[roles[k] for k in ('fit','selection','evaluation')] if name=='unhcr' else [list(range(nvisible))]
        coverage={}
        for item,spec in schema['items'].items():
            if spec['class'] not in ('GIVEN','PREDICT'):continue
            opts=options[item];K=len(opts)
            if item in given:
                values=np.asarray(opts,dtype=object)[rng.permutation(np.arange(n)%K)]
            else:
                values=np.full(n,np.nan,dtype=object)
                for block in blocks:
                    codes=rng.permutation(np.arange(len(block))%K)
                    assert len(np.unique(codes))==K
                    values[block]=np.asarray(opts,dtype=object)[codes]
                coverage[item]=K
            columns[item]=values
        frame=pd.DataFrame(columns,index=range(n))
        assert frame.loc[nvisible:,heads].isna().all().all()
        assert frame.loc[:nvisible-1,given+heads].notna().all().all()
        output=TEMP/(name+'.json')
        text=frame.to_json(orient='split',force_ascii=False)
        with output.open('x',encoding='utf-8') as stream:stream.write(text)
        records.append({'instrument':name,'path':output.relative_to(ROOT).as_posix(),
                        'sha256':hashlib.sha256(text.encode()).hexdigest(),'bytes':output.stat().st_size,
                        'schema_path':schema_path.relative_to(ROOT).as_posix(),
                        'schema_sha256':hashlib.sha256(schema_path.read_bytes()).hexdigest(),
                        'runtime_schema':runtime_metadata,
                        'visible':nvisible,'query':nquery,'given':len(given),'heads':len(heads),
                        'vectors':nquery*len(heads),'coverage':coverage})
    result={'seed':4000,'query_truth_generated':False,'old_fixture_read':False,
            'elapsed_seconds':time.perf_counter()-start,'inputs':records,
            'role_sha256':hashlib.sha256((HERE/'roles.json').read_bytes()).hexdigest()}
    with (HERE/'fixture-manifest.json').open('x',encoding='utf-8') as stream:json.dump(result,stream,indent=2)
    print(json.dumps({'created':len(records),'seconds':result['elapsed_seconds'],'scientific_calls':0}))


if __name__=='__main__':main()
