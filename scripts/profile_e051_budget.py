import os
for key in ('OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'OPENBLAS_NUM_THREADS'):
    os.environ[key] = '2'
import json
import sys
import time
from pathlib import Path
root = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(root / 'scripts'))
from check_daily_retrieval import get_case
import numpy as np
from sklearn.ensemble import HistGradientBoostingClassifier
from threadpoolctl import threadpool_limits
from src.models.hier_backoff import _layout
config, schema, frame, cells, truth, frame_hash = get_case('unhcr', 'clean')
records, items, options = _layout(frame, schema)
given = [name for name in items if records[name]['class'] == 'GIVEN']
predicted = [name for name in items if records[name]['class'] == 'PREDICT']
visible = ~frame[predicted].isna().any(axis=1).to_numpy()
x = np.column_stack([frame[name].map({v:i for i,v in enumerate(options[name])}).to_numpy(dtype=float) for name in given])
categorical = [len(options[name]) <=255 for name in given]
heads = sorted(predicted, key=lambda name: -len(options[name]))[:8]
rows = []
with threadpool_limits(limits=2):
    for name in heads:
        y = frame.loc[visible,name].map({v:i for i,v in enumerate(options[name])}).to_numpy(dtype=int)
        start = time.perf_counter()
        if len(np.unique(y)) > 1:
            model = HistGradientBoostingClassifier(max_iter=40,max_leaf_nodes=15,
                learning_rate=.1,l2_regularization=1,early_stopping=False,
                random_state=0,max_bins=255,categorical_features=categorical)
            model.fit(x[visible],y)
            model.predict_proba(x[~visible])
        row = {'head':name,'classes':len(options[name]),'observed_classes':len(np.unique(y)),
               'seconds':time.perf_counter()-start}
        rows.append(row)
        print(json.dumps(row),flush=True)
result = {'purpose':'Eight largest-schema-class heads; runtime feasibility only, no gain reading',
          'frame_sha256':frame_hash,'fit_rows':int(visible.sum()),'query_rows':int((~visible).sum()),
          'rows':rows,'rough_all_head_seconds_using_sample_max':max(r['seconds'] for r in rows)*len(predicted),
          'warning':'Extrapolation, not a measured all-head or shared-run budget.'}
(root/'tmp/e051-cost.json').write_text(json.dumps(result,indent=2)+'\n')
