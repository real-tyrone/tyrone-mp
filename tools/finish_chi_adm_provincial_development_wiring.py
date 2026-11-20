from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8-sig')
p='gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui';s=read(p).replace('[GetPlayer.GetSubjectCountries]','[AccessPlayer.GetSubjects]');write(p,s)
# Ensure projects charge a province-wide fraction, not that fraction per state.
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=read(p)
s=s.replace('add = prev.var:chi_adm_provincial_development_project_tier','add = { value = prev.var:chi_adm_provincial_development_project_tier multiply = prev.total_population divide = { value = root.total_population min = 1 } }')
# Store the selected project tier on the country for sponsorship terms.
s=re.sub(r'(chi_adm_provincial_development_start_\w+_([123]) = \{\nif = \{ limit = \{ .*? \} )every_scope_state',lambda m:m[1]+f'set_variable = {{ name = chi_adm_provincial_development_current_tier value = {m[2]} }} every_scope_state',s)
s=s.replace('chi_adm_adjust_autonomy = { AMOUNT = -1 }\nremove_variable = chi_adm_provincial_development_sponsor_case','''if = { limit = { var:chi_adm_provincial_development_current_tier = 3 } chi_adm_adjust_autonomy = { AMOUNT = -2 } }
else = { chi_adm_adjust_autonomy = { AMOUNT = -1 } }
save_scope_as = chi_adm_provincial_development_payee
c:CHI = {
    if = { limit = { scope:chi_adm_provincial_development_payee = { var:chi_adm_provincial_development_current_tier = 1 } } create_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_1 } }
    else_if = { limit = { scope:chi_adm_provincial_development_payee = { var:chi_adm_provincial_development_current_tier = 2 } } create_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_2 } }
    else = { create_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_3 } }
}
remove_variable = chi_adm_provincial_development_sponsor_case''')
# Do not keep collecting old sponsorship when no work or no Qing relationship remains.
s += '''
chi_adm_provincial_development_refresh_payments = {
    if = { limit = { OR = { NOT = { chi_adm_target_valid = yes } NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_project } } NOT = { chi_adm_provincial_development_project_affordable = yes } } }
        save_scope_as = chi_adm_provincial_development_payee
        c:CHI ?= {
            remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_1 }
            remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_2 }
            remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_3 }
        }
    }
}
'''
s=s.replace('chi_adm_provincial_development_extension_monthly = {','chi_adm_provincial_development_extension_monthly = {\nchi_adm_provincial_development_refresh_payments = yes',1)
# Do not assume any new owner's consent to project expenditure.
s=s.replace('var:chi_adm_provincial_development_project_owner = root owner = { chi_adm_provincial_development_project_affordable = yes }','var:chi_adm_provincial_development_project_owner = root owner = { chi_adm_provincial_development_project_affordable = yes }')
# Refusal of restoration notifies Qing immediately.
write(p,s)
p='common/diplomatic_actions/chi_adm_provincial_development.txt'
write(p,'\n'.join(f'''chi_adm_provincial_development_sponsorship_{tier} = {{
groups = {{ general }}
requires_approval = no
selectable = {{ always = no }}
pact = {{ is_two_sided_pact = no income_transfer = {tier*.025} max_paying_country_income_to_transfer = 1 second_country_gets_income_transfer = yes income_transfer_based_on_second_country = yes }}
}}''' for tier in (1,2,3)))
# Real custom defense demand; target victory enforces a guarantee rather than independence.
p='common/on_actions/chi_adm_provincial_development_enforcement.txt'
write(p,'''on_diplomatic_play_started = { on_actions = { chi_adm_provincial_development_enforcement_started } }
chi_adm_provincial_development_enforcement_started = {
trigger = { is_diplomatic_play_type = dp_chi_adm_provincial_development_enforcement }
effect = {
    add_war_goal = { holder = scope:target target_country = scope:initiator type = chi_adm_provincial_development_guarantee }
}
}
''')
# negotiated integration must respect a guarantee through every direct execution path, not just UI.
for p in ['common/scripted_triggers/chi_adm_negotiated_integration.txt','common/scripted_effects/chi_adm_negotiated_integration.txt','common/scripted_guis/chi_adm_negotiated_integration.txt']:
    s=read(p)
    if p.endswith('scripted_triggers/chi_adm_negotiated_integration.txt'):
        s=s.replace('chi_adm_negotiated_integration_coercible = {','chi_adm_negotiated_integration_coercible = {\nNOT = { has_modifier = chi_adm_provincial_development_guarantee }',1)
    elif p.endswith('scripted_effects/chi_adm_negotiated_integration.txt'):
        start=s.index('chi_adm_negotiated_integration_coerce = {');pos=s.index('limit = {',start)+len('limit = {');s=s[:pos]+' NOT = { has_modifier = chi_adm_provincial_development_guarantee } '+s[pos:]
    else:
        start=s.index('chi_adm_negotiated_integration_coerce = {');pos=s.index('is_valid = {',start)+len('is_valid = {');s=s[:pos]+' NOT = { has_modifier = chi_adm_provincial_development_guarantee } '+s[pos:]
    write(p,s)
# Effective MCH native government predicates and converted frontier eligibility.
p='common/government_types/00_00_chi_adm_government_types.txt';s=read(p)
s=s.replace('c:YUN ?= this c:SIH ?= this }','c:YUN ?= this c:SIH ?= this c:MCH ?= this }',1)
s=s.replace('c:SHN ?= this c:SHA ?= this c:QHN ?= this }','c:SHN ?= this c:SHA ?= this c:MGL ?= this c:XIN ?= this }',1)
s+='''
chi_adm_government_titles_gov_manchurian_generalships = {
 transfer_of_power = hereditary
 male_ruler = chi_adm_government_titles_title_manchuria
 female_ruler = chi_adm_government_titles_title_manchuria
 male_heir = ""
 female_heir = ""
 possible = {
  c:MCH ?= this
  is_direct_subject_of = c:CHI
  is_subject_type = subject_type_qing_frontier_administration
  has_law_or_variant = law_type:law_monarchy
  has_gov_regency = no
 }
}
'''
write(p,s)
p='common/scripted_triggers/chi_adm_government_titles_eligibility.txt';s=read(p);s=s.replace(' OR = {',' OR = {\n  AND = { c:MCH ?= this is_direct_subject_of = c:CHI has_law_or_variant = law_type:law_monarchy has_gov_regency = no OR = { is_subject_type = subject_type_qing_frontier_administration is_subject_type = subject_type_qing_viceroyalty_administration } }\n  AND = { OR = { c:MGL ?= this c:XIN ?= this } is_direct_subject_of = c:CHI is_subject_type = subject_type_qing_civil_administration has_law_or_variant = law_type:law_monarchy has_gov_regency = no }',1);write(p,s)
# Respect negotiated compact cooldowns and store each regional agreement separately.
for p in ['common/scripted_effects/chi_adm_provincial_development_extension.txt','common/scripted_buttons/chi_adm_provincial_development_extension.txt']:
    s=read(p).replace('NOT = { has_variable = chi_adm_provincial_development_compact_case } NOT = { has_modifier = chi_adm_provincial_development_guarantee }','NOT = { has_variable = chi_adm_provincial_development_compact_case } NOT = { has_variable = chi_adm_provincial_development_compact_cooldown } NOT = { has_modifier = chi_adm_provincial_development_guarantee }')
    if 'scripted_effects' in p:
        marker='remove_variable = chi_adm_provincial_development_compact_offer remove_variable = chi_adm_provincial_development_compact_case'
        record='\n'.join(f'if = {{ limit = {{ var:chi_adm_provincial_development_compact_case = {i} }} set_variable = {{ name = chi_adm_provincial_development_regional_compact_{i} value = var:chi_adm_provincial_development_compact_offer }} }}' for i in range(1,6))
        s=s.replace(marker,record+'\n'+marker,1)
    write(p,s)
# Crisis includes a weak court in a major imperial war; daily/global polling is unnecessary.
p='common/scripted_triggers/chi_adm_provincial_development.txt';s=read(p)
s=s.replace('chi_adm_provincial_development_broad_danger = {','''chi_adm_provincial_development_broad_danger = {
 OR = {
  c:CHI = {
   is_at_war = yes
   has_journal_entry = je_mandate_of_heaven
   je:je_mandate_of_heaven = { "scripted_bar_progress(chi_centralisation_progress_bar)" <= 3 }
  }''',1)
pos=s.index('\nchi_adm_provincial_development_crisis =');s=s[:pos].rstrip()+'\n}\n'+s[pos:];write(p,s)
# Event cases must not execute stale choices against a different case/owner.
p='events/chi_adm_provincial_development_extension.txt';s=read(p)
for n in range(1,8):
    marker=f'desc = chi_adm_provincial_development_ext_{n}_d'
    guard='scope:chi_adm_provincial_development_province = { chi_adm_target_valid = yes }' if n in (1,3,6,7) else 'chi_adm_target_valid = yes'
    s=s.replace(marker,marker+'\ntrigger = { '+guard+' }\ncancellation_trigger = { NOT = { '+guard+' } }',1)
write(p,s)
# Extra button controls let court revisit requests that were intentionally left open.
p='common/scripted_guis/chi_adm_provincial_development_extension.txt';s=read(p)
s+='''
chi_adm_provincial_development_review_militia = {
scope = country
is_valid = { chi_adm_target_valid = yes var:chi_adm_provincial_development_case = 1 }
effect = {
 save_scope_as = chi_adm_provincial_development_province
 c:CHI = { save_scope_as = chi_adm_provincial_development_court trigger_event = { id = chi_adm_provincial_development.1 popup = yes } }
}
}
''';write(p,s)
p='gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui';s=read(p);marker='textbox = { size = { 440 0 } max_width = 440 autoresize = yes multiline = yes text = "[Country.GetName]" }';s=s.replace(marker,marker+'''
button = {
 size = { 440 48 } using = default_button_action
 visible = "[GetScriptedGui('chi_adm_provincial_development_review_militia').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
 onclick = "[GetScriptedGui('chi_adm_provincial_development_review_militia').Execute(GuiScope.SetRoot(Country.MakeScope).End)]"
 textbox = { size = { 416 0 } max_width = 416 autoresize = yes multiline = yes text = "chi_adm_provincial_development_review_militia" }
}
''');write(p,s)
p='localization/english/chi_adm_l_english.yml';s=read(p)
extras={'chi_adm_provincial_development_review_militia':'Review the Emergency Warrant','chi_adm_provincial_development_grant_discretion':'Grant Provincial Discretion'}
for i in (1,2,3):
    extras[f'chi_adm_provincial_development_sponsorship_{i}']='Imperial Development Sponsorship'
    extras[f'chi_adm_provincial_development_sponsorship_{i}_desc']=f'Automatic weekly support equal to {i*2.5:g}% of provincial income during sponsored development.'
for k,v in extras.items():
    if not re.search(r'^ '+k+':',s,re.M):s+='\n '+k+': "'+v+'"\n'
write(p,s)
print('Wired provincial development project costs, native sponsorship, enforcement defense, government selection and GUI.')
