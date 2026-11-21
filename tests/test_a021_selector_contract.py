"""Handwritten fixtures only; never import a production model or data cache."""
import importlib.util
import json
import math
from dataclasses import replace

import pytest


def test_module_exists():
    assert importlib.util.find_spec('scripts.check_a021_selector_contract') is not None


@pytest.fixture
def contract():
    from scripts import check_a021_selector_contract
    return check_a021_selector_contract


def test_selection_changes_choice_but_not_candidates_or_lambda(contract):
    spec = contract.fixture_spec()
    library = contract.build_library(spec)
    digest = library.digest
    before = library.payload
    labels = contract.fixture_labels('selection')
    p, d = contract.compare_selectors(library, labels)
    altered = {row: (0, 2) for row in labels}
    p2, _ = contract.compare_selectors(library, altered)
    assert p.candidate != p2.candidate
    assert library.digest == digest and library.payload == before
    spec['calibration_labels']['c1'] = (0, 2)
    assert library.payload == before
    assert p.library_digest == d.library_digest == digest


def test_evaluation_labels_cannot_change_library_or_choices(contract):
    library = contract.build_library(contract.fixture_spec())
    decisions = contract.compare_selectors(library, contract.fixture_labels('selection'))
    first = contract.evaluate_fixture(library, decisions[0], contract.fixture_labels('evaluation'))
    altered = {n: (0, 0) for n in contract.fixture_labels('evaluation')}
    second = contract.evaluate_fixture(library, decisions[0], altered)
    assert first != second
    assert decisions == contract.compare_selectors(library, contract.fixture_labels('selection'))
    with pytest.raises(ValueError, match='role'):
        contract.compare_selectors(library, altered)


def test_forbidden_labels_donors_and_cross_role_groups_fail(contract):
    spec = contract.fixture_spec()
    spec['calibration_labels']['s0'] = (1, 2)
    with pytest.raises(ValueError, match='calibration'):
        contract.build_library(spec)
    spec = contract.fixture_spec()
    spec['donors'] = ['r0', 's0']
    with pytest.raises(ValueError, match='donor'):
        contract.build_library(spec)
    spec = contract.fixture_spec()
    spec['rows']['s0']['group'] = spec['rows']['r0']['group']
    with pytest.raises(ValueError, match='group'):
        contract.build_library(spec)


def test_frozen_checksum_prevents_post_selection_candidate_edits(contract):
    library = contract.build_library(contract.fixture_spec())
    corrupt = replace(library, payload=library.payload.replace('C0', 'BAD', 1))
    with pytest.raises(ValueError, match='hash'):
        contract.compare_selectors(corrupt, contract.fixture_labels('selection'))


def test_lambda_zero_unchanged_and_leaf_identity(contract):
    spec = contract.fixture_spec()
    row = spec['tables']['s0']
    zero = contract.render(row, row['legacy'], {'s1_parent': 0., 's2_child': 0.})
    changed = contract.render(row, row['learned'], {'s1_parent': 0., 's2_child': 0.})
    assert zero == changed
    new = contract.render(row, row['learned'], {'s1_parent': 0., 's2_child': .3})
    old_child = zero['s2_child']
    direct = tuple(.7*g+.3*e for g, e in zip(old_child, row['learned']['s2_child']))
    assert new['s1_parent'] == zero['s1_parent']
    assert new['s2_child'] == pytest.approx(direct, abs=1e-12)
    old_e = (.2, .3, .5)
    r = tuple(.7*g+.3*e for g, e in zip(old_child, old_e))
    replacement = tuple(x+.3*(b-a) for x, a, b in zip(r, old_e, row['learned']['s2_child']))
    assert replacement == pytest.approx(direct, abs=1e-12)


def test_cross_section_parent_recomputes_child_and_gains_are_not_additive(contract):
    row = contract.fixture_spec(child_change=True)['tables']['s0']
    zero = {'s1_parent': 0., 's2_child': 0.}
    p = {'s1_parent': .5, 's2_child': 0.}
    c = {'s1_parent': 0., 's2_child': .5}
    both = {'s1_parent': .5, 's2_child': .5}
    outputs = [contract.render(row, row['learned'], lam) for lam in (zero, p, c, both)]
    assert contract.section('s1_parent') != contract.section('s2_child')
    assert outputs[1]['s2_child'] != outputs[0]['s2_child']
    assert outputs[1]['s2_child'][-1] == pytest.approx(1-outputs[1]['s1_parent'][1])
    scores = [contract.row_log(p, (1, 2)) for p in outputs]
    assert abs((scores[3]-scores[0])-((scores[1]-scores[0])+(scores[2]-scores[0]))) > 1e-6


def test_official_normalization_floor_and_pooled_score(contract):
    p = contract.floor((0., 2., 6.))
    assert p == pytest.approx((.001, .001+.997*.25, .001+.997*.75))
    vectors = {'s1_parent': (2., 0.), 's2_child': (0., 1., 3.)}
    expected = (math.log(.001+.998)+math.log(.001+.997*.75))/2
    assert contract.row_log(vectors, (0, 2)) == pytest.approx(expected)
    for bad in ((-1e-20, 1.), (0., 0.), (float('nan'), 1.)):
        with pytest.raises(ValueError):
            contract.floor(bad)


def test_same_objective_rules_candidates_give_same_decision(contract):
    library = contract.build_library(contract.fixture_spec())
    for objective in ('proxy', 'deployed'):
        a, b = contract.compare_selectors(library, contract.fixture_labels('selection'), objectives=(objective, objective))
        assert a == b


def test_disagreement_is_handwritten_mechanical_example_only(contract):
    library = contract.build_library(contract.fixture_spec())
    p, d = contract.compare_selectors(library, contract.fixture_labels('selection'))
    assert p.candidate == 'C1' and d.candidate == 'C0'
    data = json.loads(library.payload)
    assert data['scope'] == 'HANDWRITTEN_FIXTURE_ONLY'
    assert data['candidate_order'] == ['C0', 'C1', 'C2', 'C3']


def test_cluster_se_and_strict_common_threshold_ties(contract):
    mean, se = contract.cluster_mean_se([1., 3., 2., -2., 1.], ['a', 'a', 'b', 'c', 'c'])
    assert mean == 1 and se == pytest.approx(math.sqrt(1.5*14/25))
    assert not contract.qualifies(.003, 0., contract.Rules())
    assert not contract.qualifies(.02, .01, contract.Rules())
    assert contract.qualifies(.021, .01, contract.Rules())


def test_activity_changes_calibration_subset_before_selection(contract):
    spec = contract.fixture_spec()
    library = json.loads(contract.build_library(spec).payload)
    assert library['candidates'][0]['calibration_rows']['s1_parent'] == ['c0', 'c1']
    assert library['candidates'][1]['calibration_rows']['s1_parent'] == ['c1']
    assert library['candidates'][1]['calibration_rows']['s2_child'] == ['c0', 'c1']
    assert all('s0' not in ids for candidate in library['candidates'] for ids in candidate['calibration_rows'].values())


def test_schema_counter_uses_predict_parents_and_regex(contract):
    schema = {'items': {'s1_root': {'class': 'PREDICT'}, 's2_child': {'class': 'PREDICT', 'gate': {'parent': 's1_root'}},
                        's2_given': {'class': 'GIVEN'}, 's2_leaf': {'class': 'PREDICT', 'gate': {'parent': 's2_given'}},
                        'skip': {'class': 'EXCLUDE', 'gate': {'parent': 's1_root'}}}}
    result = contract.schema_links(schema)
    assert result['predict_parent_edges'] == 1 and result['cross_section_edges'] == 1
    assert result['given_parent_edges'] == 1
