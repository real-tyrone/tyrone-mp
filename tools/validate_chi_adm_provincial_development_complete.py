"""Focused source/actual-effect regression checks; not an engine simulation."""
from pathlib import Path
import re,copy
import validate_chi_adm as c
import validate_chi_adm_negotiated_integration as model
R=c.ROOT
files=list((R/'common').glob('*/chi_adm_provincial_development*.txt'))+list((R/'events').glob('chi_adm_provincial_development*.txt'))+list((R/'gui/journal_entry_widgets').glob('chi_adm_provincial_development*.gui'))
def parse_file(path):
    source = path.read_text(encoding='utf-8-sig')
    if path.suffix == '.gui':
        source = re.sub(r'blockoverride "(\w+)"\s*\{', r'\1 = {', source)
    return c.parse(source)

trees={p.relative_to(R).as_posix():parse_file(p) for p in files}
def defs(kind):
    result={}
    for path,tree in trees.items():
        if path.startswith(kind+'/'):
            for key,_,body in tree:
                assert key not in result,(kind,key)
                result[key]=body
    return result
E=defs('common/scripted_effects');T=defs('common/scripted_triggers');V=defs('common/script_values');B=defs('common/scripted_buttons');G=defs('common/scripted_guis');M=defs('common/static_modifiers')
L=(R/'localization/english/chi_adm_l_english.yml').read_text(encoding='utf-8-sig')
keys=re.findall(r'^ (\w+):',L,re.M)
assert len(keys)==len(set(keys))
for path,tree in trees.items():
    source=(R/path).read_text(encoding='utf-8-sig')
    for key in re.findall(r'(?:desc|title|conclusion_desc|localization_key)\s*=\s*(chi_adm_provincial_development_\w+)',source):assert key in keys,(path,key)
    shared = c.definitions('common/scripted_guis/chi_adm_negotiated_integration.txt')
    for name in re.findall(r"GetScriptedGui\('([^']+)'\)",source):assert name in G or name == 'chi_adm_negotiated_integration_row' and name in shared,(path,name)
for name in M:assert name in keys,name
type_directory = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions')
native = '\n'.join(path.read_text(encoding='utf-8-sig') for path in sorted(type_directory.glob('*.txt')))
for name,body in M.items():
    for key,_,value in body:
        if key=='icon':continue
        assert re.search(r'^'+re.escape(key)+r'\s*=',native,re.M),(name,key)
        assert 'birth_rate' not in key
army=c.definitions('common/static_modifiers/chi_early_army.txt')
modernization={key for body in army.values() for key,_,_ in body if key!='icon'}
emergency={key for name,body in M.items() if name.startswith('chi_adm_provincial_development_package_') for key,_,_ in body if key!='icon'}
# The only common field is the existing artillery program's +50% supply COST.
# provincial development's -5% provisioning offsets part of that cost; it duplicates no reform bonus.
assert modernization & emergency <= {'country_military_goods_cost_mult'}
for body in army.values():
    for key,_,value in body:
        if key == 'country_military_goods_cost_mult':assert float(value) >= 0
# Run the real emergency helper trees through the existing strict effect model.
model.E.update(E);model.T.update(T);model.V.update(V)
class EmergencyWorld(model.World):
    def cond(self,block,current):
        if len(block)==1 and block[0][0]=='OR':
            return any(self.cond([entry],current) for entry in block[0][2])
        return super().cond(block,current)
for starting in range(101):
    for grant,action in [(5,'approve'),(10,'defy')]:
        w=EmergencyWorld();p=w.countries['ZHI'];p.v['chi_adm_autonomy']=starting;p.war=True
        p.v.update(chi_adm_provincial_development_case=1 if grant==5 else 3,chi_adm_provincial_development_offer=1)
        w.run(E['chi_adm_provincial_development_'+action],p)
        assert p.v['chi_adm_autonomy']==min(100,starting+grant)
        assert p.v['chi_adm_provincial_development_autonomy_grant']==min(grant,100-starting)
        # Unrelated later Autonomy must not be removed by restoration.
        p.v['chi_adm_autonomy']=min(100,p.v['chi_adm_autonomy']+2)
        expected=max(0,p.v['chi_adm_autonomy']-p.v['chi_adm_provincial_development_autonomy_grant'])
        p.v['chi_adm_provincial_development_case']=4
        w.run(E['chi_adm_provincial_development_restore'],p)
        assert p.v['chi_adm_autonomy']==expected
        assert 'chi_adm_provincial_development_package' not in p.v
# Assert state persistence and explicit new-owner consent from actual effect bodies.
source=(R/'common/scripted_effects/chi_adm_provincial_development_extension.txt').read_text(encoding='utf-8-sig')
source=' '.join(source.split())
assert 'var:chi_adm_provincial_development_project_owner ?= owner' in source
assert 'set_variable = { name = chi_adm_provincial_development_project_owner value = root }' in source
assert 'chi_adm_provincial_development_takeover' in E
for branch in ('military','economic','administrative'):
    for tier,months in [(1,12),(2,18),(3,24)]:
        assert f'chi_adm_provincial_development_start_{branch}_{tier}' in E
        body=str(E[f'chi_adm_provincial_development_start_{branch}_{tier}'])
        assert 'chi_adm_provincial_development_project_left' in body and str(months) in body
        assert f'chi_adm_provincial_development_{branch}_{tier}' in M
assert 'chi_adm_adjust_autonomy = { AMOUNT = -20 }' in source
assert 'change_subject_type = subject_type_qing_viceroyalty_administration' in source
assert 'change_subject_type = subject_type_qing_civil_administration' in source
assert 'months = 36' in source and 'has_variable = chi_adm_provincial_development_demand_cooldown' in source
assert 'add_war_goal' in (R/'common/on_actions/chi_adm_provincial_development_enforcement.txt').read_text(encoding='utf-8-sig')
for p in ('common/scripted_effects/chi_adm_negotiated_integration.txt','common/scripted_triggers/chi_adm_negotiated_integration.txt','common/scripted_guis/chi_adm_negotiated_integration.txt','events/chi_adm_negotiated_integration.txt'):
    assert 'has_modifier = chi_adm_provincial_development_guarantee' in (R/p).read_text(encoding='utf-8-sig')
print('PASS provincial development: source parsing/IDs/localization/native modifier types and GUI bindings; 202 actual-effect cap/defiance/restoration cases; project tiers, territorial ownership consent, conversion, bounded crisis demand and enforcement/negotiated integration guarantee wiring.')
print('PENDING runtime: weekly expense/pact scaling, custom enforcement settlement, state-country object persistence, human takeover, event/UI layouts and two-player choices.')
