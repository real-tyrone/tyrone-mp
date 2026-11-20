from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def get(p):return (R/p).read_text(encoding='utf-8-sig')
def put(p,s):(R/p).write_text(s,encoding='utf-8-sig')
# An effect iterator is not a valid all-states trigger. Preserve the same predicate
# as the negation of any state failing it.
for p in ['common/scripted_buttons/chi_adm_provincial_development_extension.txt','common/scripted_effects/chi_adm_provincial_development_extension.txt']:
    s=get(p)
    s=re.sub(r'every_scope_state = \{ NOT = \{ has_variable = (chi_adm_provincial_development_\w+) \} \}',r'NOT = { any_scope_state = { has_variable = \1 } }',s)
    s=re.sub(r'every_scope_state = \{ (var:chi_adm_provincial_development_\w+ = [12]) \}',r'NOT = { any_scope_state = { NOT = { \1 } } }',s)
    put(p,s)
# Distinct progress visibility: conversion bars must not show a false completed state.
p='gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui';s=get(p)
s=s.replace('progressbar = { size = { 440 16 }','progressbar = { progresstexture = "gfx/interface/progressbar/progressbar_gold.dds" noprogresstexture = "gfx/interface/progressbar/progressbar_empty.dds" direction = horizontal size = { 440 16 }')
put(p,s)
# Reopen a declined restoration as an actual court dispute.
p='common/scripted_effects/chi_adm_provincial_development.txt';s=get(p)
s=s.replace('set_variable = { name = chi_adm_provincial_development_dispute value = yes }','''set_variable = { name = chi_adm_provincial_development_dispute value = yes }
save_scope_as = chi_adm_provincial_development_province
c:CHI = { trigger_event = { id = chi_adm_provincial_development_ext.7 popup = yes } }''')
# Crisis grants record actual rather than nominal room at the autonomy cap.
for grant in (5,10):s=s.replace(f'name = chi_adm_provincial_development_autonomy_grant value = {grant}',f'name = chi_adm_provincial_development_autonomy_grant value = chi_adm_provincial_development_grant_{grant}')
put(p,s)
# Native project payment events and explicit AI choices through the same helpers.
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=get(p)
s+='''
chi_adm_provincial_development_ai_monthly = {
 if = { limit = { is_ai = yes }
  if = { limit = { any_scope_state = { has_variable = chi_adm_provincial_development_project NOT = { var:chi_adm_provincial_development_project_owner = root } } } chi_adm_provincial_development_takeover = yes }
  if = { limit = { chi_adm_target_valid = yes chi_adm_provincial_development_project_affordable = yes }
   if = { limit = { chi_adm_provincial_development_project_free = yes }
    if = { limit = { NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_economic } } } chi_adm_provincial_development_start_economic_1 = yes }
    else_if = { limit = { NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_administrative } } } chi_adm_provincial_development_start_administrative_1 = yes }
    else_if = { limit = { NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_military } } } chi_adm_provincial_development_start_military_1 = yes }
    else_if = { limit = { has_technology_researched = central_archives } chi_adm_provincial_development_start_economic_2 = yes chi_adm_provincial_development_start_administrative_2 = yes chi_adm_provincial_development_start_military_2 = yes chi_adm_provincial_development_start_economic_3 = yes chi_adm_provincial_development_start_administrative_3 = yes chi_adm_provincial_development_start_military_3 = yes }
   }
   if = { limit = { NOT = { has_variable = chi_adm_provincial_development_sponsor_case } any_scope_state = { has_variable = chi_adm_provincial_development_project NOT = { has_variable = chi_adm_provincial_development_project_sponsored } } } chi_adm_provincial_development_ask_sponsor = yes }
  }
 }
 if = { limit = { c:CHI ?= this is_ai = yes }
  every_subject_or_below = {
   limit = { chi_adm_target_valid = yes }
   if = { limit = { var:chi_adm_provincial_development_case = 1 } chi_adm_provincial_development_approve = yes }
   if = { limit = { has_variable = chi_adm_provincial_development_sponsor_case NOT = { var:chi_adm_provincial_development_sponsor_case = 2 } } chi_adm_provincial_development_offer_sponsor = yes }
   if = { limit = { has_variable = chi_adm_provincial_development_crisis_demand } chi_adm_provincial_development_fund_alternative = yes if = { limit = { has_variable = chi_adm_provincial_development_crisis_demand } chi_adm_provincial_development_grant_discretion = yes } }
   if = { limit = { chi_adm_provincial_development_conversion_ready = yes var:chi_adm_loyalty >= 75 } chi_adm_provincial_development_propose_conversion = yes }
  }
 }
}
'''
put(p,s)
p='common/on_actions/chi_adm_provincial_development_extension.txt';s=get(p)
s=s.replace('chi_qing_administration_tag = yes','c:CHI ?= this chi_qing_administration_tag = yes',1)
s=s.replace('effect = { chi_adm_provincial_development_extension_monthly = yes }','effect = { chi_adm_provincial_development_extension_monthly = yes chi_adm_provincial_development_ai_monthly = yes }')
put(p,s)
# Funding expenses stop while insolvent, instead of charging progress that cannot run.
p='common/script_values/chi_adm_provincial_development_extension.txt';s=get(p)
s=s.replace('multiply = 0.05 min = 0','multiply = 0.05 min = 0 if = { limit = { NOT = { chi_adm_provincial_development_project_affordable = yes } } multiply = 0 }')
put(p,s)
# Protect fully sponsored prior projects from repeat offers and stale counterevents.
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=get(p)
s=s.replace('has_variable = chi_adm_provincial_development_sponsor_case c:CHI', 'has_variable = chi_adm_provincial_development_sponsor_case NOT = { var:chi_adm_provincial_development_sponsor_case = 2 } c:CHI')
put(p,s)
print('Audited provincial development iterator predicates, project/AI paths and native progress textures.')
