from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'common/scripted_buttons/04_russia_buttons.txt'
text = path.read_text(encoding='utf-8')
def end_block(s, opening):
    depth = 1
    end = opening + 1
    while depth:
        depth += (s[end] == '{') - (s[end] == '}')
        end += 1
    return end
requests = [
 ('je_the_eastern_border_treaty_of_beijing', 1, ['STATE_OUTER_MANCHURIA'], 'rus_bought_outer_manchuria', 'Primorye'),
 ('je_the_eastern_border_russia_chuguchak_protocol', 2, ['STATE_ALTAI', 'STATE_JETISY', 'STATE_KIRGHIZIA'], 'rus_chuguchak_protocol', 'the Ili frontier'),
 ('je_the_eastern_border_treaty_of_aigun', 3, ['STATE_AMUR'], 'rus_bought_amur', 'Amur'),
]
events = ['namespace = chi_qing_treaty']
loc = {'chi_qing_treaty_request_tt': 'Submit a territorial treaty to [GetPlayer.GetName]. The imperial court must approve before territory changes hands.',
       'chi_qing_treaty_accept': 'Approve the territorial settlement.',
       'chi_qing_treaty_decline': 'Reject the Russian demand.'}
for key, number, states, flag, label in requests:
    start = text.index(key + ' = {')
    opening = text.index('{', start)
    end = end_block(text, opening)
    block = text[start:end].replace('is_player = no', '')
    pos = block.index('effect = {')
    fx_open = block.index('{', pos)
    fx_end = end_block(block, fx_open)
    effect = f'''effect = {{
        custom_tooltip = chi_qing_treaty_request_tt
        hidden_effect = {{
            c:CHI = {{
                set_variable = {{ name = chi_qing_treaty_pending value = {number} }}
                trigger_event = {{ id = chi_qing_treaty.{number} popup = yes }}
            }}
        }}
    }}'''
    block = block[:pos] + effect + block[fx_end:]
    pos = block.index('possible = {') + len('possible = {')
    block = block[:pos] + '\n exists = c:CHI\n hidden_trigger = { c:CHI = { NOT = { has_variable = chi_qing_treaty_pending } NOT = { has_variable = chi_qing_treaty_retry } } }\n' + block[pos:]
    text = text[:start] + block + text[end:]
    transfers = '\n'.join(f'''s:{state} = {{ every_scope_state = {{
        limit = {{ owner = {{ OR = {{ c:CHI ?= this is_subject_of = c:CHI }} }} }}
        set_state_owner = c:RUS
    }} }}''' for state in states)
    events.append(f'''chi_qing_treaty.{number} = {{
    type = country_event
    title = chi_qing_treaty_{number}_title
    desc = chi_qing_treaty_{number}_desc
    event_image = {{ video = "asia_poor_people_moving" }}
    icon = "gfx/interface/icons/event_icons/event_scales.dds"
    duration = 30
    trigger = {{ exists = c:RUS var:chi_qing_treaty_pending = {number} }}
    option = {{
        name = chi_qing_treaty_accept
        {transfers}
        c:RUS = {{ set_variable = {flag} }}
        if = {{ limit = {{ owes_obligation_to = c:RUS }} set_owes_obligation_to = {{ country = c:RUS setting = no }} }}
        remove_variable = chi_qing_treaty_pending
        ai_chance = {{
            base = 50
            modifier = {{ trigger = {{ relations:c:RUS >= -19 }} factor = 100 }}
            modifier = {{ trigger = {{ owes_obligation_to = c:RUS }} factor = 100 }}
            modifier = {{ trigger = {{ is_at_war = yes }} factor = 3 }}
            modifier = {{ trigger = {{ c:RUS.army_power_projection >= chi_qing_treaty_realm_power }} factor = 4 }}
            modifier = {{ trigger = {{ c:RUS.army_power_projection < {{ value = chi_qing_treaty_realm_power multiply = 0.5 }} }} factor = 0.25 }}
            modifier = {{ trigger = {{ relations:c:RUS < -50 }} factor = 0.5 }}
        }}
    }}
    option = {{
        name = chi_qing_treaty_decline
        trigger = {{ NOT = {{ owes_obligation_to = c:RUS }} }}
        default_option = yes
        change_relations = {{ country = c:RUS value = -10 }}
        remove_variable = chi_qing_treaty_pending
        set_variable = {{ name = chi_qing_treaty_retry value = yes months = 12 }}
        ai_chance = {{
            base = 50
            modifier = {{ trigger = {{ relations:c:RUS >= -19 }} factor = 0 }}
        }}
    }}
}}''')
    loc[f'chi_qing_treaty_{number}_title'] = 'A Russian Territorial Demand'
    loc[f'chi_qing_treaty_{number}_desc'] = f"[GetPlayer.GetName] has received a Russian demand for {label}. Approval transfers the affected imperial and subject territories to [GetGlobalVariable('unused').GetName]" if False else f"[ROOT.GetCountry.GetName] must decide whether to cede {label} to Russia. Approval transfers the affected imperial and subject territories. A Russian-held [concept_obligation] prevents refusal. Rejection worsens [concept_relations] by #r 10#! and blocks new requests for #v 12 months#!."
path.write_text(text, encoding='utf-8')
(root / 'events/chi_qing_treaty_approval.txt').write_text('\n\n'.join(events) + '\n', encoding='utf-8')
path = root / 'common/script_values/chi_qing_treaty_approval.txt'
path.write_text('''chi_qing_treaty_realm_power = {
    value = army_power_projection
    every_subject_or_below = { add = army_power_projection }
}
''', encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
loc['chi_qing_treaty_request_tt'] = 'Submit a territorial treaty to the Chinese imperial court. No territory is transferred before approval.'
for key, value in loc.items():
    if not re.search(r'^ ' + key + ':', text, re.M):
        text += f'\n {key}: "{value}"\n'
path.write_text(text, encoding='utf-8-sig')
# Human landowners must pass the shared native predicate as well.
path = root / 'common/scripted_triggers/zz_chi_qing_treaty_partner.txt'
native = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_triggers/00_ip5_victoria_scripted_triggers.txt').read_text(encoding='utf-8-sig')
start = native.index('country_is_valid_qing_treaty_partner = {')
opening = native.index('{', start)
text = native[start:end_block(native, opening)]
text = text.replace('is_player = no', 'always = yes').replace('var:china_warlord_explosion <= 3', 'var:china_warlord_explosion <= 4')
text = text.replace('country_has_primary_culture = cu:han', 'country_has_primary_culture = cu:han\n\t\tcountry_has_primary_culture = cu:uighur')
text = text.replace('is_subject_of = ROOT', 'is_subject_of = ROOT\n\t\tis_subject_of = c:CHI')
path.write_text(text, encoding='utf-8')
