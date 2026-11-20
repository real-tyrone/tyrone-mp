"""emergency powers: emergency provincial powers and court restoration workflow."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
LOC = {}
def loc(key, value):
    LOC['chi_adm_provincial_development_' + key] = value
    return 'chi_adm_provincial_development_' + key
def write(relative, text):
    (ROOT / relative).write_text(text.strip() + '\n', encoding='utf-8-sig')
def adjust(stat, amount):
    return f'chi_adm_adjust_{stat} = {{ AMOUNT = {amount} }}'

triggers = '''
chi_adm_provincial_development_direct_danger = {
    OR = { is_at_war = yes any_scope_state = { turmoil >= 0.40 } }
}
chi_adm_provincial_development_broad_danger = {
    any_country = {
        NOT = { chi_qing_realm = yes }
        is_adjacent_to_country = root
        relations:root < -50
        army_power_projection >= { value = chi_adm_provincial_development_imperial_power multiply = 2 }
    }
}
chi_adm_provincial_development_crisis = {
    OR = { chi_adm_provincial_development_direct_danger = yes var:chi_adm_provincial_development_warning >= 3 }
}
chi_adm_provincial_development_can_request = {
    chi_adm_target_valid = yes
    chi_adm_provincial_development_crisis = yes
    NOT = { has_variable = chi_adm_provincial_development_case }
    NOT = { has_variable = chi_adm_provincial_development_package }
    NOT = { has_variable = chi_adm_provincial_development_retry }
}
chi_adm_provincial_development_case_valid = {
    chi_adm_target_valid = yes
    has_variable = chi_adm_provincial_development_case
}
'''
write('common/scripted_triggers/chi_adm_provincial_development.txt', triggers)
write('common/script_values/chi_adm_provincial_development.txt', '''
chi_adm_provincial_development_imperial_power = {
    value = 0
    c:CHI = {
        add = army_power_projection
        every_subject_or_below = { add = army_power_projection }
    }
}
''')
mods = []
for number, name, body in [
    (1, 'Provincial Recruitment Warrant', 'military_formation_mobilization_speed_mult = 0.15'),
    (2, 'Provincial Defensive Readiness', 'unit_morale_recovery_mult = 0.10 military_formation_organization_gain_mult = 0.10'),
    (3, 'Provincial Military Provisioning', 'country_military_goods_cost_mult = -0.05'),
]:
    mods.append(f'chi_adm_provincial_development_package_{number} = {{ icon = gfx/interface/icons/timed_modifier_icons/modifier_rifle_positive.dds {body} state_tax_collection_mult = -0.05 }}')
    loc('package_' + str(number), name)
mods += ['chi_adm_provincial_development_unrestored = { icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds state_tax_collection_mult = -0.05 }']
loc('unrestored', 'Unsettled Emergency Accounts')
write('common/static_modifiers/chi_adm_provincial_development.txt', '\n'.join(mods))

effects = []
def effect(key, body):
    effects.append('chi_adm_provincial_development_' + key + ' = {\n' + body + '\n}')
def dispatch(number):
    return f'''save_scope_as = chi_adm_provincial_development_province
    c:CHI = {{ save_scope_as = chi_adm_provincial_development_court trigger_event = {{ id = chi_adm_provincial_development.{number} popup = yes }} }}'''
def notify():
    return 'c:CHI = { save_scope_as = chi_adm_provincial_development_court } trigger_event = { id = chi_adm_provincial_development.2 popup = yes }'
effect('remove_bonuses', '\n'.join(f'remove_modifier = chi_adm_provincial_development_package_{i}' for i in (1,2,3)))
effect('clear_case', 'remove_variable = chi_adm_provincial_development_case remove_variable = chi_adm_provincial_development_deadline')
effect('grant', '''chi_adm_provincial_development_remove_bonuses = yes
set_variable = { name = chi_adm_provincial_development_package value = var:chi_adm_provincial_development_offer }
if = { limit = { var:chi_adm_provincial_development_package = 1 } add_modifier = { name = chi_adm_provincial_development_package_1 } }
else_if = { limit = { var:chi_adm_provincial_development_package = 2 } add_modifier = { name = chi_adm_provincial_development_package_2 } }
else = { add_modifier = { name = chi_adm_provincial_development_package_3 } }
chi_adm_provincial_development_clear_case = yes
remove_variable = chi_adm_provincial_development_grace
remove_variable = chi_adm_provincial_development_offer
''')
for number in (1,2,3):
    effect('request_' + str(number), f'''if = {{ limit = {{ chi_adm_provincial_development_can_request = yes }}
        set_variable = {{ name = chi_adm_provincial_development_offer value = {number} }}
        set_variable = {{ name = chi_adm_provincial_development_case value = 1 }}
        set_variable = {{ name = chi_adm_provincial_development_deadline value = 6 }}
        {dispatch(1)}
    }}''')
effect('approve', f'''if = {{ limit = {{ chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 1 }}
    set_variable = {{ name = chi_adm_provincial_development_autonomy_grant value = 5 }}
    {adjust('autonomy',5)} chi_adm_provincial_development_grant = yes
}}''')
for number in (1,2,3):
    effect('counter_' + str(number), f'''if = {{ limit = {{ chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 1 }}
        set_variable = {{ name = chi_adm_provincial_development_offer value = {number} }}
        set_variable = {{ name = chi_adm_provincial_development_case value = 2 }}
        set_variable = {{ name = chi_adm_provincial_development_deadline value = 6 }}
        {notify()}
    }}''')
effect('refuse', f'''if = {{ limit = {{ chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 1 }}
    set_variable = {{ name = chi_adm_provincial_development_case value = 3 }}
    set_variable = {{ name = chi_adm_provincial_development_deadline value = 6 }} {notify()}
}}''')
effect('accept_counter', f'''if = {{ limit = {{ chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 2 }}
    set_variable = {{ name = chi_adm_provincial_development_autonomy_grant value = 5 }}
    {adjust('autonomy',5)} chi_adm_provincial_development_grant = yes
}}''')
effect('defy', f'''if = {{ limit = {{ chi_adm_provincial_development_case_valid = yes chi_adm_provincial_development_crisis = yes OR = {{ var:chi_adm_provincial_development_case = 2 var:chi_adm_provincial_development_case = 3 }} }}
    set_variable = {{ name = chi_adm_provincial_development_autonomy_grant value = 10 }}
    {adjust('autonomy',10)} {adjust('loyalty',-5)}
    change_relations = {{ country = c:CHI value = -10 }}
    chi_adm_provincial_development_grant = yes
}}''')
effect('abandon', '''chi_adm_provincial_development_clear_case = yes remove_variable = chi_adm_provincial_development_offer
set_variable = { name = chi_adm_provincial_development_retry value = yes months = 12 }''')
effect('restore', '''if = { limit = { chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 4 }
    chi_adm_adjust_autonomy = { AMOUNT = chi_adm_provincial_development_restoration_change }
    chi_adm_provincial_development_remove_bonuses = yes
    remove_modifier = chi_adm_provincial_development_unrestored
    remove_variable = chi_adm_provincial_development_package
    remove_variable = chi_adm_provincial_development_autonomy_grant
    chi_adm_provincial_development_abandon = yes
}''')
effect('resist_restoration', f'''if = {{ limit = {{ chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 4 }}
    {adjust('loyalty',-3)} change_relations = {{ country = c:CHI value = -5 }}
    add_modifier = {{ name = chi_adm_provincial_development_unrestored }}
    chi_adm_provincial_development_clear_case = yes
    set_variable = {{ name = chi_adm_provincial_development_dispute value = yes }}
}}''')
effect('cleanup', '''chi_adm_provincial_development_remove_bonuses = yes remove_modifier = chi_adm_provincial_development_unrestored
chi_adm_provincial_development_clear_case = yes
remove_variable = chi_adm_provincial_development_package remove_variable = chi_adm_provincial_development_offer
remove_variable = chi_adm_provincial_development_grace remove_variable = chi_adm_provincial_development_dispute
remove_variable = chi_adm_provincial_development_warning remove_variable = chi_adm_provincial_development_autonomy_grant''')
effect('monthly', f'''if = {{ limit = {{ chi_adm_target_valid = yes }}
    if = {{ limit = {{ chi_adm_provincial_development_broad_danger = yes }}
        if = {{ limit = {{ NOT = {{ has_variable = chi_adm_provincial_development_warning }} }} set_variable = {{ name = chi_adm_provincial_development_warning value = 0 }} }}
        change_variable = {{ name = chi_adm_provincial_development_warning add = 1 }}
    }} else = {{ remove_variable = chi_adm_provincial_development_warning }}
    if = {{ limit = {{ has_variable = chi_adm_provincial_development_package NOT = {{ has_variable = chi_adm_provincial_development_dispute }} }}
        if = {{ limit = {{ chi_adm_provincial_development_crisis = yes }} remove_variable = chi_adm_provincial_development_grace }}
        else = {{
            if = {{ limit = {{ NOT = {{ has_variable = chi_adm_provincial_development_grace }} }} set_variable = {{ name = chi_adm_provincial_development_grace value = 3 }} }}
            else = {{ change_variable = {{ name = chi_adm_provincial_development_grace subtract = 1 }} }}
            if = {{ limit = {{ var:chi_adm_provincial_development_grace <= 0 NOT = {{ has_variable = chi_adm_provincial_development_case }} }}
                chi_adm_provincial_development_remove_bonuses = yes
                set_variable = {{ name = chi_adm_provincial_development_case value = 4 }}
                set_variable = {{ name = chi_adm_provincial_development_deadline value = 6 }}
                {notify()}
            }}
        }}
    }}
    if = {{ limit = {{ has_variable = chi_adm_provincial_development_deadline }}
        change_variable = {{ name = chi_adm_provincial_development_deadline subtract = 1 }}
        if = {{ limit = {{ var:chi_adm_provincial_development_deadline <= 0 }}
            if = {{ limit = {{ var:chi_adm_provincial_development_case = 1 }} chi_adm_provincial_development_refuse = yes }}
            else_if = {{ limit = {{ var:chi_adm_provincial_development_case = 4 }} chi_adm_provincial_development_resist_restoration = yes }}
            else = {{ chi_adm_provincial_development_abandon = yes }}
        }}
    }}
    if = {{ limit = {{ is_ai = yes chi_adm_provincial_development_can_request = yes }} chi_adm_provincial_development_request_1 = yes }}
}} else = {{ chi_adm_provincial_development_cleanup = yes }}''')
write('common/scripted_effects/chi_adm_provincial_development.txt', '\n\n'.join(effects))
path = ROOT / 'common/script_values/chi_adm_provincial_development.txt'
with path.open('a', encoding='utf-8') as handle:
    handle.write('\nchi_adm_provincial_development_restoration_change = { value = var:chi_adm_provincial_development_autonomy_grant multiply = -1 }\n')

actions = [
('request_1','Request a Recruitment Warrant','Seek permission for faster mobilization. Approval grants +5 [concept_chi_adm_autonomy] and a temporary fiscal burden.','chi_adm_provincial_development_can_request = yes'),
('request_2','Request Defensive Readiness','Seek permission for improved recovery and organization. Approval grants +5 [concept_chi_adm_autonomy] and a temporary fiscal burden.','chi_adm_provincial_development_can_request = yes'),
('request_3','Request Local Provisioning','Seek permission for reduced military supply costs. Approval grants +5 [concept_chi_adm_autonomy] and a temporary fiscal burden.','chi_adm_provincial_development_can_request = yes'),
('accept_counter','Accept the Court’s Warrant','Accept the proposed emergency powers. Gain #v 5#! [concept_chi_adm_autonomy].','chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 2'),
('defy','Mobilize on Provincial Authority','Gain #v 10#! [concept_chi_adm_autonomy]; lose #r 5#! [concept_chi_adm_loyalty] and #r 10#! [concept_relations].','chi_adm_provincial_development_case_valid = yes chi_adm_provincial_development_crisis = yes OR = { var:chi_adm_provincial_development_case = 2 var:chi_adm_provincial_development_case = 3 }'),
('abandon','Set Aside the Petition','Close this petition. A new request must wait #v 12 months#!.','chi_adm_provincial_development_case_valid = yes OR = { var:chi_adm_provincial_development_case = 2 var:chi_adm_provincial_development_case = 3 }'),
('restore','Return Exceptional Powers','Return the tracked emergency [concept_chi_adm_autonomy] gain and remove the unsettled-accounts penalty.','chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 4'),
('resist_restoration','Retain Provincial Discretion','Retain the emergency [concept_chi_adm_autonomy], with reduced tax revenue, #r −3#! [concept_chi_adm_loyalty] and #r −5#! [concept_relations].','chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 4'),
]
buttons = []
for key, title, desc, condition in actions:
    loc(key, title);loc(key+'_desc',desc)
    buttons.append(f'''chi_adm_provincial_development_{key} = {{
    name = chi_adm_provincial_development_{key}
    desc = chi_adm_provincial_development_{key}_desc
    visible = {{ {condition} }}
    possible = {{ {condition} }}
    effect = {{ chi_adm_provincial_development_{key} = yes }}
    ai_chance = {{ base = 0 }}
}}''')
write('common/scripted_buttons/chi_adm_provincial_development.txt','\n\n'.join(buttons))
events = ['namespace = chi_adm_provincial_development']
court_options = []
for key, title in [('approve','Authorize the Requested Powers'),('counter_1','Offer a Recruitment Warrant'),('counter_2','Offer Defensive Readiness'),('counter_3','Offer Local Provisioning'),('refuse','Withhold the Imperial Seal')]:
    loc(key,title)
    court_options.append(f'''option = {{
        name = chi_adm_provincial_development_{key}
        trigger = {{ scope:chi_adm_provincial_development_province = {{ chi_adm_provincial_development_case_valid = yes var:chi_adm_provincial_development_case = 1 }} }}
        scope:chi_adm_provincial_development_province = {{ chi_adm_provincial_development_{key} = yes }}
        ai_chance = {{ base = {60 if key == 'approve' else 10} }}
    }}''')
loc('court_title','A Provincial Emergency Warrant')
loc('court_desc',"[SCOPE.sCountry('chi_adm_provincial_development_province').GetName] requests exceptional military powers. Authorize the request, offer another warrant, or refuse. Provincial mobilization may proceed in defiance while the crisis lasts.")
loc('province_title','The Imperial Seal and Provincial Arms')
loc('province_desc','Review the court’s response or settle the emergency accounts. Refusal and silence never authorize peaceful annexation. Military benefits lapse after a three-month post-crisis grace period; the return of exceptional discretion remains a political settlement.')
loc('later','Keep the Memorial Open')
for number, side, options in [(1,'court','\n'.join(court_options)),(2,'province','\n'.join(f'''option = {{ name = chi_adm_provincial_development_{key} trigger = {{ {condition} }} chi_adm_provincial_development_{key} = yes ai_chance = {{ base = {50 if key in ('accept_counter','restore') else 10} }} }}''' for key,_,_,condition in actions if not key.startswith('request_')))]:
    events.append(f'''chi_adm_provincial_development.{number} = {{
    type = country_event
    title = chi_adm_provincial_development_{side}_title
    desc = chi_adm_provincial_development_{side}_desc
    event_image = {{ video = "ep1_persian_court" }}
    icon = "gfx/interface/icons/event_icons/event_scales.dds"
    duration = 30
    {options}
    option = {{ name = chi_adm_provincial_development_later default_option = yes ai_chance = {{ base = 0 }} }}
}}''')
write('events/chi_adm_provincial_development.txt','\n\n'.join(events))
loc('province','Provincial Emergency Powers')
loc('province_reason','The court’s warrants strengthen provincial defenses while placing exceptional power in local hands. Submit a military petition during a genuine crisis, answer the imperial counterproposal, and settle the return of discretion when danger passes.')
loc('closed','This administration has left imperial service.')
write('common/journal_entries/chi_adm_provincial_development.txt', '''chi_adm_provincial_development_province = {
    icon = "gfx/interface/icons/event_icons/event_scales.dds"
    group = je_group_chi_adm_court_register_province
    context = country
    transferable = no
    can_revolution_inherit = no
    is_shown_when_inactive = { chi_adm_target_valid = yes }
    possible = { chi_adm_target_valid = yes }
''' + '\n'.join('    scripted_button = chi_adm_provincial_development_'+key for key,_,_,_ in actions) + '''
    outcome = {
        flags = { hidden invalid_outcome }
        conclusion_desc = chi_adm_provincial_development_closed
        trigger = { NOT = { chi_adm_target_valid = yes } }
    }
}''')
write('common/on_actions/chi_adm_provincial_development.txt', '''on_monthly_pulse_country = { on_actions = { chi_adm_provincial_development_monthly } }
chi_adm_provincial_development_monthly = {
    trigger = { OR = { chi_qing_administration_tag = yes has_variable = chi_adm_provincial_development_package has_variable = chi_adm_provincial_development_case } }
    effect = { chi_adm_provincial_development_monthly = yes }
}''')
path = ROOT / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
for key,value in LOC.items():
    if not re.search(r'^ '+key+':',text,re.M):
        text += '\n '+key+': "'+value.replace('\n',r'\n')+'"\n'
path.write_text(text,encoding='utf-8-sig')
print('Built emergency powers emergency powers workflow. Remaining provincial development systems are not implemented.')
