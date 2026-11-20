from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
def ending(s,opening):
    i=opening+1;depth=1
    while depth:depth+=(s[i]=='{')-(s[i]=='}');i+=1
    return i
# A compact is usable only while its territory remains within that administration.
checks={1:['ULIASTAI','URGA','TUVA','ALTAI'],2:['ALXA','HINGGAN'],3:['DZUNGARIA','TIANSHAN','JETISY','KIRGHIZIA'],4:['QINGHAI'],5:['SHENGJING','SOUTHERN_MANCHURIA','NORTHERN_MANCHURIA','OUTER_MANCHURIA','AMUR']}
p='common/scripted_triggers/chi_adm_provincial_development_extension.txt';s=r(p)
for n,states in checks.items():
    conditions=' '.join('state_region = s:STATE_'+state for state in states)
    s+=f'\nchi_adm_provincial_development_region_{n}_held = {{ any_scope_state = {{ OR = {{ {conditions} }} }} }}\n'
s+='\nchi_adm_provincial_development_compact_region_valid = { OR = {\n'+'\n'.join(f'AND = {{ var:chi_adm_provincial_development_compact_case = {n} chi_adm_provincial_development_region_{n}_held = yes }}' for n in checks)+'\n} }\n';w(p,s)
for p in ['common/scripted_effects/chi_adm_provincial_development_extension.txt','common/scripted_buttons/chi_adm_provincial_development_extension.txt','common/scripted_guis/chi_adm_provincial_development_extension.txt']:
    s=r(p)
    for n in checks:
        key=f'chi_adm_provincial_development_compact_{n} = {{';start=s.index(key);opening=s.index('{',start);end=ending(s,opening)
        block=s[start:end].replace('chi_adm_target_valid = yes',f'chi_adm_target_valid = yes chi_adm_provincial_development_region_{n}_held = yes')
        s=s[:start]+block+s[end:]
    s=s.replace('chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_compact_offer','chi_adm_target_valid = yes chi_adm_provincial_development_compact_region_valid = yes has_variable = chi_adm_provincial_development_compact_offer')
    if 'scripted_effects' in p:
        s=s.replace('chi_adm_provincial_development_extension_monthly = {','''chi_adm_provincial_development_extension_monthly = {
if = { limit = { has_variable = chi_adm_provincial_development_compact_case NOT = { chi_adm_provincial_development_compact_region_valid = yes } }
 remove_variable = chi_adm_provincial_development_compact_case remove_variable = chi_adm_provincial_development_compact_offer
}
if = { limit = { has_variable = chi_adm_provincial_development_enforcement_target NOT = { chi_adm_target_valid = yes } }
 remove_variable = chi_adm_provincial_development_enforcement_target
}
''',1)
    w(p,s)
# Keep MCH's territorial name through modernization, with the correct relationship.
p='common/dynamic_country_names/tyrone_qing_administrations.txt';s=r(p)
if 'chi_adm_provincial_development_mch_viceroyalty_name' not in s:
    marker='INJECT:MCH = {' if 'INJECT:MCH = {' in s else 'MCH = {'
    assert marker in s
    s=s.replace(marker,marker+'''
 dynamic_country_name = {
  name = chi_adm_provincial_development_mch_viceroyalty_name
  adjective = chi_adm_subject_MCH_adj
  priority = 4500
  trigger = { scope:actor ?= { is_direct_subject_of = c:CHI is_subject_type = subject_type_qing_viceroyalty_administration } }
 }
''',1)
w(p,s)
p='localization/english/chi_adm_l_english.yml';s=r(p)
s+='\n chi_adm_provincial_development_mch_viceroyalty_name: "Three Eastern Provinces"\n'
s=s.replace('Explicitly assume remaining project expenses. Completed reviews are retained.','Explicitly assume remaining project expenses and existing inspection obligations. Completed reviews are retained. Imperial contributions continue only while eligible under the current court relationship.')
w(p,s)
# Make the post-crisis window a real three-calendar-month timer, not 3-4 pulses.
p='common/scripted_effects/chi_adm_provincial_development.txt';s=r(p)
start=s.index('if = { limit = { has_variable = chi_adm_provincial_development_package NOT = { has_variable = chi_adm_provincial_development_dispute } }')
opening=s.index('{',start);end=ending(s,opening)
replacement='''if = { limit = { has_variable = chi_adm_provincial_development_package NOT = { has_variable = chi_adm_provincial_development_dispute } }
 if = { limit = { chi_adm_provincial_development_crisis = yes }
  if = { limit = { has_variable = chi_adm_provincial_development_grace }
   remove_variable = chi_adm_provincial_development_grace
   change_variable = { name = chi_adm_provincial_development_grace_revision add = 1 }
  }
 }
 else_if = { limit = { NOT = { has_variable = chi_adm_provincial_development_grace } NOT = { has_variable = chi_adm_provincial_development_case } }
  set_variable = chi_adm_provincial_development_grace
  if = { limit = { NOT = { has_variable = chi_adm_provincial_development_grace_revision } } set_variable = { name = chi_adm_provincial_development_grace_revision value = 0 } }
  change_variable = { name = chi_adm_provincial_development_grace_revision add = 1 }
  save_scope_value_as = { name = chi_adm_provincial_development_grace_revision value = var:chi_adm_provincial_development_grace_revision }
  trigger_event = { id = chi_adm_provincial_development.3 months = 3 popup = no }
 }
}'''
s=s[:start]+replacement+s[end:];w(p,s)
p='events/chi_adm_provincial_development.txt';s=r(p)+'''
chi_adm_provincial_development.3 = {
 type = country_event
 hidden = yes
 trigger = {
  chi_adm_target_valid = yes
  has_variable = chi_adm_provincial_development_package
  has_variable = chi_adm_provincial_development_grace
  var:chi_adm_provincial_development_grace_revision = scope:chi_adm_provincial_development_grace_revision
  NOT = { chi_adm_provincial_development_crisis = yes }
  NOT = { has_variable = chi_adm_provincial_development_case }
 }
 immediate = {
  chi_adm_provincial_development_remove_bonuses = yes
  set_variable = { name = chi_adm_provincial_development_case value = 4 }
  set_variable = { name = chi_adm_provincial_development_deadline value = 6 }
  c:CHI = { save_scope_as = chi_adm_provincial_development_court }
  trigger_event = { id = chi_adm_provincial_development.2 popup = yes }
 }
}
''';w(p,s)
