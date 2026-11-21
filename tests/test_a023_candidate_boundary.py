"""Information/freeze tests only; never train or score a model."""
from dataclasses import replace
import json
import sys

import pytest

from scripts.check_a023_candidate_boundary import (
    Boundary, RecordingStub, Response, fixture_roles, schema_family, seal,
)


def setup_boundary():
    roles = fixture_roles()
    stub = RecordingStub()
    boundary = Boundary(roles, stub)
    return boundary, stub


def responses(boundary, *roles):
    return tuple(Response(row, role, 'invented') for row, (role, _) in
                 boundary.roles.items() if role in roles)


def library(boundary):
    return boundary.build(
        (('legacy', ()), ('upstream', ('3',)), ('endpoints', ('3', '7a'))),
        responses(boundary, 'reference', 'fit'),
        responses(boundary, 'calibration_legacy', 'calibration_replay'))


@pytest.mark.parametrize('role', ['calibration_legacy', 'calibration_replay', 'selection', 'evaluation'])
def test_builder_rejects_nonfit_responses_before_backend(role):
    boundary, stub = setup_boundary()
    with pytest.raises(ValueError, match='role'):
        boundary.build((('legacy', ()),), responses(boundary, 'reference', 'fit', role),
                       responses(boundary, 'calibration_legacy', 'calibration_replay'))
    assert stub.events == []


@pytest.mark.parametrize('role', ['fit', 'selection', 'evaluation'])
def test_calibrator_rejects_forbidden_labels_before_any_call(role):
    boundary, stub = setup_boundary()
    with pytest.raises(ValueError, match='role'):
        boundary.build((('legacy', ()),), responses(boundary, 'reference', 'fit'),
                       responses(boundary, 'calibration_legacy', 'calibration_replay', role))
    assert not stub.events


def test_forged_roles_and_group_overlap_fail():
    boundary, stub = setup_boundary()
    forged = tuple(replace(x, role='fit') for x in responses(boundary, 'selection'))
    with pytest.raises(ValueError, match='role'):
        boundary.build((('legacy', ()),), responses(boundary, 'reference', 'fit') + forged,
                       responses(boundary, 'calibration_legacy', 'calibration_replay'))
    roles = fixture_roles()
    roles['s0'] = ('selection', 'group-reference')
    with pytest.raises(ValueError, match='group'):
        Boundary(roles, stub)
    assert not stub.events


def test_one_shared_build_lambda_eligibility_and_no_feedback():
    boundary, stub = setup_boundary()
    frozen = library(boundary)
    data = json.loads(frozen.payload)
    assert data['budget']['base_pipelines'] == 2
    assert data['budget']['normal_neural_calls'] == 6
    assert data['rules']['minimum_bucket'] == 30
    assert data['rules']['fallback'] == 'legacy'
    fits = [e for e in stub.events if e['stage'] in ('base_pd', 'metric')]
    assert len(fits) == 2
    lam = [e for e in stub.events if e['stage'] == 'lambda']
    assert all(e['context']['inactive_roles'] == ['calibration_legacy', 'calibration_replay'] for e in lam)
    assert all(e['context']['active_roles'] == ['calibration_replay'] for e in lam)
    before = list(stub.events)
    with pytest.raises(ValueError, match='frozen'):
        library(boundary)
    assert stub.events == before
    choices = boundary.choose(frozen, responses(boundary, 'selection'))
    select_events = [e for e in stub.events if e['stage'].startswith('select_')]
    assert len(select_events) == 2
    assert select_events[0]['context'] == select_events[1]['context']
    assert json.loads(choices.payload)['library_digest'] == frozen.digest


def test_selection_and_evaluation_boundaries_and_seals():
    boundary, stub = setup_boundary()
    frozen = library(boundary)
    with pytest.raises(ValueError, match='role'):
        boundary.choose(frozen, responses(boundary, 'selection', 'evaluation'))
    changed = json.loads(frozen.payload)
    changed['candidates'][1]['lambda_artifact'] = 'changed'
    with pytest.raises(ValueError, match='identity'):
        boundary.choose(seal(changed), responses(boundary, 'selection'))
    with pytest.raises(ValueError, match='digest'):
        boundary.choose(replace(frozen, payload=frozen.payload + ' '), responses(boundary, 'selection'))
    with pytest.raises(ValueError, match='choices'):
        boundary.evaluate(frozen, seal({}), responses(boundary, 'evaluation'))
    choices = boundary.choose(frozen, responses(boundary, 'selection'))
    with pytest.raises(ValueError, match='frozen'):
        boundary.choose(frozen, responses(boundary, 'selection'))
    with pytest.raises(ValueError, match='role'):
        boundary.evaluate(frozen, choices, responses(boundary, 'evaluation', 'selection'))
    with pytest.raises(ValueError, match='choices'):
        boundary.evaluate(frozen, seal({'library_digest': frozen.digest}), responses(boundary, 'evaluation'))
    boundary.evaluate(frozen, choices, responses(boundary, 'evaluation'))
    assert stub.events[-1]['stage'] == 'evaluate'
    assert not any(name.startswith('src.models') for name in sys.modules)


def test_r_has_separate_dev_capability_but_cannot_see_e():
    boundary, stub = setup_boundary()
    frozen = library(boundary)
    choices = boundary.choose(frozen, responses(boundary, 'selection'))
    dev = responses(boundary, 'reference', 'fit', 'calibration_legacy', 'calibration_replay', 'selection')
    with pytest.raises(ValueError, match='role'):
        boundary.build_r(dev + responses(boundary, 'evaluation'))
    boundary.build_r(dev)
    with pytest.raises(ValueError, match='budget'):
        boundary.build_r(dev)
    boundary.evaluate(frozen, choices, responses(boundary, 'evaluation'))
    assert len([e for e in stub.events if e['stage'].startswith('base_')]) == 2


def test_schema_only_masks_preserve_sections_and_collapse_without_channel():
    schema = {'items': {
        's3_parent': {'class': 'PREDICT'},
        's7a_child': {'class': 'PREDICT', 'gate': {'parent': 's3_parent'}},
        's7b_child': {'class': 'PREDICT', 'gate': {'parent': 's3_parent'}},
        's7a_other': {'class': 'PREDICT'},
    }}
    report = schema_family(schema)
    assert report['candidates'] == (('legacy', ()), ('upstream', ('3',)),
                                     ('endpoints', ('3', '7a', '7b')))
    assert report['sections']['7a'] == ['s7a_child', 's7a_other']
    single = {'items': {'parent': {'class': 'PREDICT'}, 'child':
                       {'class': 'PREDICT', 'gate': {'parent': 'parent'}}}}
    assert schema_family(single)['candidates'] == (('legacy', ()),)
    assert schema_family(single)['mechanism_identifiable'] is False


def test_injected_selector_receives_no_builder_and_cannot_return_unknown_candidate():
    class BadSelector(RecordingStub):
        def __call__(self, stage, labels, context):
            result = super().__call__(stage, labels, context)
            if stage.startswith('select_'):
                assert set(context) == {'library_digest', 'candidate_order', 'rules', 'budget'}
                return 'not-in-frozen-family'
            return result
    stub = BadSelector()
    boundary = Boundary(fixture_roles(), stub)
    frozen = library(boundary)
    with pytest.raises(ValueError, match='candidate'):
        boundary.choose(frozen, responses(boundary, 'selection'))
