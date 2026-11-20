"""Focused regression checks for continuous corruption taxation capacity."""
import json
from math import isclose
import validate_chi_adm as core


def check():
    original = json.loads((core.ROOT / 'tools/chi_adm_tax_capacity_original.json').read_text('utf-8'))
    current = {p: json.loads(json.dumps(core.load(p))) for p in original}
    p = 'common/diplomatic_actions/tyrone_qing_administrations.txt'
    removed = []
    def strip_tax(tree):
        result = []
        for key, op, value in tree:
            if key == 'state_tax_capacity_mult':
                assert value == '0.25'
                removed.append(value)
                continue
            result.append([key, op, strip_tax(value) if isinstance(value, list) else value])
        return result
    # User revised the pact bases independently: preserve current 20% civil / 15% frontier.
    for name, _, body in original[p]:
        for entry in next(v for k, _, v in body if k == 'pact'):
            if entry[0] == 'income_transfer': entry[2] = '0.20' if name in ('qing_viceroyalty_administration','qing_civil_administration') else '0.15'
    # Military-administration pact was explicitly removed after negotiated integration.
    original[p] = [entry for entry in original[p] if entry[0] != 'qing_military_administration']
    assert strip_tax(original[p]) == current[p]
    assert len(removed) == 2
    p = 'common/static_modifiers/chi_adm_core.txt'
    expected = original[p]
    for entry in expected:
        if entry[0].startswith('chi_adm_corruption_tier_'):
            entry[2] = []
    expected.append(['chi_adm_corruption_tax_capacity', '=', [['state_tax_capacity_mult', '=', '0.25']]])
    actual = [e for e in current[p] if e[0] not in ('chi_adm_loyalty_remittance','chi_adm_autonomy_remittance')]
    for entry in actual:
        if entry[0] == 'chi_adm_corruption_tax_capacity': entry[2] = [e for e in entry[2] if e[0] != 'icon']
    assert expected == actual
    p = 'common/scripted_effects/chi_adm_core.txt'
    expected = original[p]
    for entry in expected:
        if entry[0] == 'chi_adm_refresh_status':
            entry[2] = [['chi_adm_remove_status', '=', 'yes']]
    # MCH initialization is separately exercised by the provincial accounts model at 85/15/25.
    assert [e for e in expected if e[0] != 'chi_adm_initialize'] == [e for e in current[p] if e[0] != 'chi_adm_initialize']
    p = 'common/journal_entries/chi_adm_governance.txt'
    actual = current[p]
    scaling = [e for e in actual[0][2] if e[0] == 'scaling_modifiers_while_active']
    scaling = [e for e in scaling if e[2][0][2] == 'chi_adm_corruption_tax_capacity']
    assert scaling == [['scaling_modifiers_while_active', '=', [['modifier', '=', 'chi_adm_corruption_tax_capacity'], ['value', '=', 'chi_adm_corruption_tax_capacity_scale']]]]
    actual[0][2] = [e for e in actual[0][2] if e[0] != 'scaling_modifiers_while_active']
    assert actual == original[p]
    p = 'common/script_values/chi_adm_core.txt'
    assert current[p][:-4] == original[p]
    values = core.VALUE_DEFS
    assert values['chi_adm_corruption_tax_capacity_scale'] == core.parse('value = 1 subtract = { value = var:chi_adm_corruption multiply = 0.02 } min = -1 max = 1')
    assert values['chi_adm_corruption_tax_capacity_percent'] == core.parse('value = chi_adm_corruption_tax_capacity_scale multiply = 25')
    def evaluate(block, corruption):
        total = 0
        for key, _, val in block:
            if isinstance(val, list):
                n = evaluate(val, corruption)
            elif val == 'var:chi_adm_corruption':
                n = corruption
            elif val in values:
                n = evaluate(values[val], corruption)
            else:
                n = float(val)
            if key == 'value': total = n
            elif key == 'subtract': total -= n
            elif key == 'multiply': total *= n
            elif key == 'min': total = max(total, n)
            elif key == 'max': total = min(total, n)
            else: raise AssertionError(key)
        return total
    for corruption in range(101):
        factor = evaluate(values['chi_adm_corruption_tax_capacity_scale'], corruption)
        assert isclose(.25 * factor, .25 - .005 * corruption, abs_tol=1e-12)
        assert isclose(evaluate(values['chi_adm_corruption_tax_capacity_percent'], corruption), 25 - .5 * corruption, abs_tol=1e-12)
    print('PASS corruption tax capacity: all 101 values, native JE binding, legacy cleanup, fixed bonuses removed; other pact/effect/JE/modifier mechanics preserved')

if __name__ == '__main__':
    check()
