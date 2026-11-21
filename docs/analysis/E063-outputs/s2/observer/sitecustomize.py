import hashlib, json, os, sys, time
class Audit:
    """Standalone observational profiler, also copied outside the ZIP for CLI."""
    def __init__(self, main_path, log_path, previous, limits, ntrain, instrument):
        self.main_path = os.path.normcase(os.path.abspath(main_path))
        self.stream = open(log_path, 'x', encoding='utf-8')
        self.totals = dict(previous)
        self.limits = limits
        self.ntrain = ntrain
        self.instrument = instrument
        self.started = {}
        self.environment_recorded = False
        self.roles = json.loads(os.environ.get('E063_ROLES', '{}'))
        self.metric_roles = json.loads(os.environ.get('E063_METRIC_ROLES', '{}'))

    def emit(self, row):
        row.update(instrument=self.instrument, pid=os.getpid())
        self.stream.write(json.dumps(row, allow_nan=False) + '\n')
        self.stream.flush()

    def profile(self, frame, event, arg):
        if event not in ('call', 'return'):
            return
        name = frame.f_code.co_name
        filename = os.path.normcase(os.path.abspath(frame.f_code.co_filename))
        is_model = filename == self.main_path
        if is_model and name == '<module>' and event == 'return':
            torch = sys.modules['torch']
            torch.set_num_threads(2)
            torch.set_num_interop_threads(2)
            if torch.cuda.is_available():
                raise RuntimeError('GPU not allowed')
            self.environment_recorded = True
            self.emit(dict(event='environment', torch_threads=torch.get_num_threads(),
                           torch_interop_threads=torch.get_num_interop_threads(), cuda=False))
        if is_model and name == '_targets' and event == 'call':
            rows, predicted = frame.f_locals['rows'], frame.f_locals['predict_items']
            if len(rows) and (min(rows.index) < 0 or max(rows.index) >= self.ntrain
                             or rows[predicted].isna().any().any()):
                raise RuntimeError('DEV PREDICT reached training targets')
            self.emit(dict(event='target_boundary', rows=len(rows)))
            digest = hashlib.sha256(__import__('numpy').asarray(rows.index, dtype='<i8').tobytes()).hexdigest()
            roles = [key for key, value in self.roles.items() if value['index_sha256'] == digest]
            if not roles:
                raise RuntimeError('Frozen neural target role mismatch')
            self.emit(dict(event='target_role', rows=len(rows), roles=roles, index_sha256=digest))
        if is_model and name in ('fit_sections', '_e063_fit_sections') and event == 'call':
            for role in ('fit', 'select', 'bank'):
                digest = hashlib.sha256(__import__('numpy').asarray(frame.f_locals[role], dtype='<i8').tobytes()).hexdigest()
                if digest != self.metric_roles[role]['index_sha256']:
                    raise RuntimeError('Metric role identity mismatch: ' + role)
            self.emit(dict(event='metric_roles', function=name, status='PASS'))
        if is_model and name == '_e063_fit_sections' and event == 'return' and arg is not None:
            learned, active, sections = arg
            self.emit(dict(event='round_fit', weights=[w.tolist() for w in learned],
                           active=list(active), sections=sections))
        if is_model and name == '_e063_round_layer' and event == 'return':
            self.emit(dict(event='round_lambda', values={k: list(v) for k,v in frame.f_locals.get('lam', {}).items()}))
        if is_model and name == '_e063_predict' and event == 'return':
            self.emit(dict(event='round_support', values=frame.f_globals['_e063_LAST_DIAGNOSTICS']))
        kind = ('full_stack' if is_model and name == '_e063_predict' else
                'neural' if is_model and name == '_train_on' else
                'metric' if name == 'minimize' and filename.replace('\\', '/').endswith('/scipy/optimize/_minimize.py') else None)
        if kind is None:
            return
        if event == 'call':
            if kind == 'neural' and str(frame.f_locals['dev']) != 'cpu':
                raise RuntimeError('Non-CPU neural training')
            if kind == 'metric':
                args = frame.f_locals['args']
                nf = self.metric_roles['fit']['rows']
                if any(args[i].shape[0] != nf for i in (0, 1, 2)):
                    raise RuntimeError('Non-F rows reached metric optimizer')
                self.emit(dict(event='optimizer_slice', fit_rows=nf,
                               coordinates=len(frame.f_locals['x0'])))
            self.totals[kind] += 1
            self.emit(dict(event='enter', kind=kind, function=name, totals=dict(self.totals)))
            if self.totals[kind] > self.limits[kind]:
                raise RuntimeError('Call cap: ' + kind)
            self.started[id(frame)] = time.perf_counter()
        else:
            row = dict(event='return', kind=kind, function=name,
                       seconds=time.perf_counter() - self.started.pop(id(frame), time.perf_counter()),
                       returned=arg is not None)
            if kind == 'neural':
                row.update(epochs=int(frame.f_locals.get('epoch', 0)),
                           best_epoch=int(frame.f_locals.get('best_epoch', 0)),
                           device=str(frame.f_locals.get('dev')))
            if kind == 'metric' and arg is not None:
                row.update(iterations=int(arg.nit), success=bool(arg.success))
            self.emit(row)

if os.environ.get('E063_AUDIT_MAIN'):
    _audit = Audit(os.environ['E063_AUDIT_MAIN'], os.environ['E063_AUDIT_LOG'] + '-' + str(os.getpid()) + '.jsonl', json.loads(os.environ['E063_PRIOR']), json.loads(os.environ['E063_CAPS']), int(os.environ['E063_NTRAIN']), os.environ['E063_INSTRUMENT'])
    sys.setprofile(_audit.profile)
