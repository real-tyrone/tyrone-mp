"""Regression checks for separate native remittance scaling and starting offices."""
import json
from math import isclose
import validate_chi_adm as c

def check():
    old=json.loads((c.ROOT/'tools/chi_adm_remittance_original.json').read_text('utf-8'))
    mods=c.definitions('common/static_modifiers/chi_adm_core.txt')
    native=c.ROOT
    game=__import__('pathlib').Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
    for name in ('chi_adm_corruption_tax_capacity','chi_adm_loyalty_remittance','chi_adm_autonomy_remittance'):
        assert (game/c.get(mods[name],'icon')).is_file(),name
    for kind in ('loyalty','autonomy'):
        assert c.get(mods['chi_adm_'+kind+'_remittance'],'country_overlord_income_transfer_mult')=='0.5'
    p='common/static_modifiers/chi_adm_core.txt'
    actual=json.loads(json.dumps(c.load(p)))
    actual=[e for e in actual if e[0] not in ('chi_adm_loyalty_remittance','chi_adm_autonomy_remittance')]
    for e in actual:
        if e[0]=='chi_adm_corruption_tax_capacity':e[2]=[v for v in e[2] if v[0]!='icon']
    assert actual==old[p]
    p='common/journal_entries/chi_adm_governance.txt'
    actual=json.loads(json.dumps(c.load(p)))
    for kind in ('loyalty','autonomy'):
        block=['scaling_modifiers_while_active','=',[['modifier','=','chi_adm_'+kind+'_remittance'],['value','=','chi_adm_'+kind+'_remittance_scale']]]
        assert actual[0][2].count(block)==1
        actual[0][2].remove(block)
    assert actual==old[p]
    values=c.VALUE_DEFS
    assert values['chi_adm_loyalty_remittance_scale']==c.parse('value = var:chi_adm_loyalty multiply = 0.02 subtract = 1 min = -1 max = 1')
    assert values['chi_adm_autonomy_remittance_scale']==c.parse('value = 1 subtract = { value = var:chi_adm_autonomy multiply = 0.02 } min = -1 max = 1')
    for loyalty in range(101):
        for autonomy in range(101):
            l=.5*max(-1,min(1,loyalty*.02-1))
            a=.5*max(-1,min(1,1-autonomy*.02))
            assert isclose(l,(loyalty-50)/100,abs_tol=1e-12)
            assert isclose(a,(50-autonomy)/100,abs_tol=1e-12)
            assert 0-1e-12<=1+l+a<=2+1e-12
    assert isclose(.20*(1+.5+.5),.40)
    p='common/script_values/chi_adm_core.txt'
    assert json.loads(json.dumps(c.load(p)))[:-2]==old[p]
    p='common/history/buildings/11_tyrone_east_asia.txt'
    actual=json.loads(json.dumps(c.load(p)))
    original=old[p][0][2]
    assert actual[0][2][:len(original)]==original
    extras=actual[0][2][len(original):]
    expected={'SHANXI':10,'XIAN':15,'WESTERN_HUBEI':10,'EASTERN_HUBEI':10,'HUNAN':5,'HENAN':15,'SHANDONG':15}
    assert len(extras)==len(expected)
    for state,_,body in extras:
        b=c.get(c.get(body,'region_state:CHI'),'create_building')
        assert c.get(b,'building')=='"building_government_administration"'
        owner=c.get(c.get(b,'add_ownership'),'country')
        assert c.get(owner,'country')=='"c:CHI"'
        assert int(c.get(owner,'levels'))==expected[state.removeprefix('s:STATE_')]
    print('PASS remittances: 10,201 Loyalty/Autonomy combinations, additive native subject-side modifiers, 20% to 40% example; three valid native icons; seven starting building additions only')

if __name__=='__main__':check()
