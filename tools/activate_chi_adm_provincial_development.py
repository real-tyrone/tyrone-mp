from pathlib import Path
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
for p in ['common/scripted_buttons/chi_adm_provincial_development_extension.txt','common/scripted_effects/chi_adm_provincial_development_extension.txt']:
    s=r(p).replace('literacy >=','literacy_rate >=')
    if 'scripted_effects' in p:
        s=s.replace('set_variable = chi_adm_provincial_development_conversion_repudiated set_variable = chi_adm_provincial_development_dispute','''set_variable = chi_adm_provincial_development_conversion_repudiated set_variable = chi_adm_provincial_development_dispute
save_scope_as = chi_adm_provincial_development_province
c:CHI = { trigger_event = { id = chi_adm_provincial_development_ext.7 popup = yes } }''')
        s += '''
chi_adm_provincial_development_ensure_entries = {
 if = { limit = { chi_adm_target_valid = yes }
  if = { limit = { NOT = { has_journal_entry = chi_adm_provincial_development_province } } add_journal_entry = { type = chi_adm_provincial_development_province } }
  if = { limit = { NOT = { has_journal_entry = chi_adm_provincial_development_frontier } } add_journal_entry = { type = chi_adm_provincial_development_frontier } }
 }
 if = { limit = { OR = { chi_adm_target_valid = yes any_scope_state = { has_variable = chi_adm_provincial_development_project } } }
  if = { limit = { NOT = { has_journal_entry = chi_adm_provincial_development_development } } add_journal_entry = { type = chi_adm_provincial_development_development } }
 }
 if = { limit = { c:CHI ?= this chi_adm_court_valid = yes NOT = { has_journal_entry = chi_adm_provincial_development_court_extension } } add_journal_entry = { type = chi_adm_provincial_development_court_extension } }
}
'''
        s=s.replace('chi_adm_provincial_development_ai_monthly = {','''chi_adm_provincial_development_ai_monthly = {
 if = { limit = { is_ai = yes chi_adm_target_valid = yes NOT = { has_variable = chi_adm_provincial_development_compact_case } NOT = { has_variable = chi_adm_provincial_development_compact_cooldown } }
  if = { limit = { c:MGL ?= this } if = { limit = { has_variable = chi_adm_provincial_development_regional_compact_1 } chi_adm_provincial_development_compact_2 = yes } else = { chi_adm_provincial_development_compact_1 = yes } }
  else_if = { limit = { c:XIN ?= this } chi_adm_provincial_development_compact_3 = yes }
  else_if = { limit = { c:XIB ?= this } chi_adm_provincial_development_compact_4 = yes }
  else_if = { limit = { c:MCH ?= this } chi_adm_provincial_development_compact_5 = yes }
 }
''',1)
    w(p,s)
p='common/on_actions/chi_adm_provincial_development_extension.txt';s=r(p).replace('effect = { chi_adm_provincial_development_extension_monthly = yes','effect = { chi_adm_provincial_development_ensure_entries = yes chi_adm_provincial_development_extension_monthly = yes')
s+='''
on_game_started_after_lobby = { on_actions = { chi_adm_provincial_development_start_entries } }
chi_adm_provincial_development_start_entries = {
effect = {
 c:CHI ?= {
  chi_adm_provincial_development_ensure_entries = yes
  every_subject_or_below = { limit = { chi_adm_target_valid = yes } chi_adm_provincial_development_ensure_entries = yes }
 }
}
}
''';w(p,s)
