"""Build the bounded memorials and audits protocol. No generated provincial accounts-imperial law reform replacements."""
from pathlib import Path
import re
import chi_adm_memorials_presentation as presentation
ROOT=Path(__file__).resolve().parents[1]
LOC={}
def loc(key,text):
    LOC['chi_adm_memorials_'+key]=text
    return 'chi_adm_memorials_'+key
def write(path,text):
    (ROOT/path).write_text(text.strip()+'\n',encoding='utf-8')
T={}; E={}; B={}; G={}; C={}
def trig(name,body): T['chi_adm_memorials_'+name]=body
def effect(name,body): E['chi_adm_memorials_'+name]=body
def guard(name,gate,body): effect(name,f'if = {{ limit = {{ {gate} }} {body} }}')
def stat(name,amount): return f'chi_adm_adjust_{name} = {{ AMOUNT = {amount} }}'
def relation(amount): return f'change_relations = {{ country = c:CHI value = {amount} }}'
def result(number): return f'set_variable = {{ name = chi_adm_memorials_result value = {number} }}'
def notify(court=False):
    if court: return 'save_scope_as = chi_adm_memorials_province c:CHI ?= { trigger_event = { id = chi_adm_memorials.1 popup = yes } }'
    return 'chi_adm_memorials_ensure_responses = yes trigger_event = { id = chi_adm_memorials.2 popup = yes }'
def decision(name,title,description,gate,action):
    loc(name,title);loc(name+'_tt',description)
    G['chi_adm_memorials_'+name]=f'scope = country is_valid = {{ {gate} }} effect = {{ {action} }}'
def button(name,title,description,visible,gate,action,weight=10):
    loc(name,title);loc(name+'_desc',description)
    ai=''
    if name=='file_relief': ai='modifier = { trigger = { gold_reserves < 10000 } factor = 4 } modifier = { trigger = { gold_reserves >= 10000 } factor = 0.25 }'
    if name=='file_discretion': ai='modifier = { trigger = { relative_bureaucracy < 0 } factor = 4 }'
    if name in ('accept_edict','audit_cooperate'): ai='modifier = { trigger = { var:chi_adm_loyalty >= 60 } factor = 3 } modifier = { trigger = { var:chi_adm_corruption >= 60 } factor = 0.5 }'
    if name in ('appeal_edict','audit_obstruct'): ai='modifier = { trigger = { var:chi_adm_autonomy >= 60 } factor = 3 }'
    if name in ('defy_edict','resist_settlement'): ai='modifier = { trigger = { var:chi_adm_loyalty < 40 } factor = 4 }'
    if name=='audit_conceal': ai='modifier = { trigger = { var:chi_adm_corruption >= 60 } factor = 3 } modifier = { trigger = { var:chi_adm_loyalty >= 60 } factor = 0.5 }'
    B['chi_adm_memorials_'+name]=f'''name = chi_adm_memorials_{name} desc = chi_adm_memorials_{name}_desc
visible = {{ {visible} }}
possible = {{ custom_tooltip = {{ text = chi_adm_memorials_{name}_desc {gate} }} }}
effect = {{ custom_tooltip = chi_adm_memorials_{name}_desc hidden_effect = {{ {action} }} }}
ai_chance = {{ base = {weight} {ai} }}'''

trig('valid','chi_adm_target_valid = yes')
trig('court','c:CHI ?= this chi_adm_court_valid = yes')
trig('court_free','c:CHI = { authority >= 25 NOT = { has_modifier = chi_adm_memorials_court_staff } }')
trig('memorial_free','chi_adm_memorials_valid = yes authority >= 25 NOT = { has_variable = chi_adm_memorials_memorial } NOT = { has_variable = chi_adm_memorials_memorial_cooldown }')
trig('edict_room','c:CHI = { NOT = { any_subject_or_below = { count >= 2 chi_adm_memorials_valid = yes OR = { has_variable = chi_adm_memorials_edict has_variable = chi_adm_memorials_audit } } } }')
trig('edict_free','chi_adm_memorials_valid = yes chi_adm_memorials_court_free = yes chi_adm_memorials_edict_room = yes NOT = { has_variable = chi_adm_memorials_edict } NOT = { has_variable = chi_adm_memorials_edict_cooldown } NOT = { has_variable = chi_adm_memorials_audit }')
trig('audit_free','chi_adm_memorials_valid = yes chi_adm_memorials_edict_room = yes NOT = { has_variable = chi_adm_memorials_edict } chi_adm_memorials_court_free = yes NOT = { has_variable = chi_adm_memorials_audit } NOT = { has_variable = chi_adm_memorials_audit_cooldown }')
trig('memorial_pending','chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_memorial var:chi_adm_memorials_memorial_stage = 1')
trig('edict_reply','chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_edict OR = { var:chi_adm_memorials_edict_stage = 1 var:chi_adm_memorials_edict_stage = 3 var:chi_adm_memorials_edict_stage = 4 }')
trig('audit_choice','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 1')
trig('centralised','c:CHI = { has_journal_entry = je_mandate_of_heaven je:je_mandate_of_heaven = { "scripted_bar_progress(chi_centralisation_progress_bar)" >= 6 } }')
effect('court_cost','c:CHI = { add_modifier = { name = chi_adm_memorials_court_staff months = 6 } }')
for protocol in ('memorial','edict','audit'):
    variables={'memorial':['memorial','memorial_stage','memorial_left'], 'edict':['edict','edict_stage','edict_left','edict_delay_used','edict_appeal_used'], 'audit':['audit','audit_mode','audit_progress','audit_left','audit_settlement']}[protocol]
    effect('clear_'+protocol,' '.join('remove_variable = chi_adm_memorials_'+v for v in variables)+(' remove_modifier = chi_adm_memorials_audit_burden' if protocol=='audit' else ''))
effect('cleanup','chi_adm_memorials_clear_memorial = yes chi_adm_memorials_clear_edict = yes chi_adm_memorials_clear_audit = yes remove_modifier = chi_adm_memorials_exposed remove_modifier = chi_adm_memorials_supervision remove_modifier = chi_adm_memorials_light_supervision remove_modifier = chi_adm_memorials_suspicion remove_modifier = chi_adm_memorials_discretion remove_modifier = chi_adm_memorials_honors remove_modifier = chi_adm_memorials_emergency')

memorials=[('relief','Request Fiscal Relief','Request £20,000 from Qing reserves. Counteroffer: £10,000. Filing commits 25 Authority for six months; one memorial every two years.','always = yes'),('discretion','Petition for Administrative Latitude','Seek twelve months of lighter supervision: +2% Bureaucracy, +5 Autonomy, +2 Corruption and +2 Loyalty. Counteroffer grants only +3 Autonomy and +1 Loyalty. Filing commits 25 Authority for six months; two-year cooldown.','always = yes'),('military','Memorial for Emergency Assistance','While at war, request £10,000 and temporary military discretion (+3 Autonomy, +3 Loyalty, +5% military wages for twelve months). Counteroffer: £5,000, +2 Autonomy, +2 Loyalty, same wage burden. Filing commits 25 Authority for six months; two-year cooldown.','is_at_war = yes')]
for i,(name,title,description,extra) in enumerate(memorials,1):
    gate=f'chi_adm_memorials_memorial_free = yes {extra}'
    guard('file_'+name,gate,f'''set_variable = chi_adm_memorials_memorial_record set_variable = {{ name = chi_adm_memorials_memorial value = {i} }} set_variable = {{ name = chi_adm_memorials_memorial_stage value = 1 }} set_variable = {{ name = chi_adm_memorials_memorial_left value = 6 }} set_variable = {{ name = chi_adm_memorials_memorial_cooldown days = 730 }} add_modifier = {{ name = chi_adm_memorials_clerks months = 6 }} {result(1)} {notify(True)}''')
    button('file_'+name,title,description+' The memorial expires after six monthly reviews; a compromise must be accepted within three.','chi_adm_memorials_valid = yes',gate,f'chi_adm_memorials_file_{name} = yes',5)

def grant_memorial(reduced=False):
    relief=10000 if reduced else 20000;military=5000 if reduced else 10000
    return f'''if = {{ limit = {{ var:chi_adm_memorials_memorial = 1 c:CHI = {{ gold_reserves >= {relief} }} }} c:CHI = {{ add_treasury = -{relief} }} add_treasury = {relief} {stat('loyalty',3 if reduced else 5)} }}
if = {{ limit = {{ var:chi_adm_memorials_memorial = 2 }} {stat('autonomy',3 if reduced else 5)} {stat('loyalty',1 if reduced else 2)} {'' if reduced else stat('corruption',2)+' add_modifier = { name = chi_adm_memorials_discretion months = 12 }'} }}
if = {{ limit = {{ var:chi_adm_memorials_memorial = 3 c:CHI = {{ gold_reserves >= {military} }} }} c:CHI = {{ add_treasury = -{military} }} add_treasury = {military} {stat('autonomy',2 if reduced else 3)} {stat('loyalty',2 if reduced else 3)} add_modifier = {{ name = chi_adm_memorials_emergency months = 12 }} }}'''
for name,reduced in [('full',False),('reduced',True)]:
    money1=10000 if reduced else 20000;money3=5000 if reduced else 10000
    trig('can_pay_'+name,f'OR = {{ AND = {{ var:chi_adm_memorials_memorial = 1 c:CHI = {{ gold_reserves >= {money1} }} }} var:chi_adm_memorials_memorial = 2 AND = {{ var:chi_adm_memorials_memorial = 3 is_at_war = yes c:CHI = {{ gold_reserves >= {money3} }} }} }}')
guard('approve_memorial','chi_adm_memorials_memorial_pending = yes chi_adm_memorials_can_pay_full = yes',f'{grant_memorial()} chi_adm_memorials_clear_memorial = yes {result(2)} {notify()}')
guard('counter_memorial','chi_adm_memorials_memorial_pending = yes chi_adm_memorials_can_pay_reduced = yes',f'set_variable = {{ name = chi_adm_memorials_memorial_stage value = 2 }} set_variable = {{ name = chi_adm_memorials_memorial_left value = 3 }} {result(3)} {notify()}')
guard('reject_memorial','chi_adm_memorials_memorial_pending = yes',f'{stat("loyalty",-3)} {relation(-3)} chi_adm_memorials_clear_memorial = yes {result(4)} {notify()}')
guard('accept_counter','chi_adm_memorials_valid = yes var:chi_adm_memorials_memorial_stage = 2 chi_adm_memorials_can_pay_reduced = yes',f'{grant_memorial(True)} chi_adm_memorials_clear_memorial = yes {result(2)} {notify(True)}')
guard('decline_counter','chi_adm_memorials_valid = yes var:chi_adm_memorials_memorial_stage = 2',f'chi_adm_memorials_clear_memorial = yes {result(5)} {notify(True)}')

edicts=[('supervision','Order Administrative Supervision','Offer a twelve-month review: Corruption -5, Autonomy -3 (-1 for frontier offices), Bureaucracy -2%. Negotiated version: Corruption -3, no Autonomy loss, Bureaucracy -1%. Requires Corruption at least 40.','var:chi_adm_corruption >= 40'),('honors','Confer an Imperial Commendation','Offer recognition: Loyalty +5, Autonomy -2, Prestige +5% for twelve months. Negotiated recognition: Loyalty +3, no Autonomy loss. Requires Loyalty at least 60 and Corruption below 60.','var:chi_adm_loyalty >= 60 var:chi_adm_corruption < 60'),('emergency','Offer Emergency Military Assistance','While the province is at war, offer £10,000 from Qing reserves, +3 Autonomy and +5% military wages for twelve months. Negotiated aid: £5,000 and +2 Autonomy. No troops, laws or military reform bonuses are created.','is_at_war = yes c:CHI = { gold_reserves >= 10000 }')]
for i,(name,title,description,extra) in enumerate(edicts,1):
    gate=f'chi_adm_memorials_edict_free = yes {extra}'
    guard('send_'+name,gate,f'chi_adm_memorials_court_cost = yes set_variable = {{ name = chi_adm_memorials_edict value = {i} }} set_variable = {{ name = chi_adm_memorials_edict_stage value = 1 }} set_variable = {{ name = chi_adm_memorials_edict_left value = 6 }} set_variable = {{ name = chi_adm_memorials_edict_cooldown days = 730 }} {result(6)} {notify()}')
    decision('send_'+name,title,description+' Commits 25 Qing Authority for six months; two-year target cooldown. At most two outstanding edicts or audits; one intervention per province. Six reviews to reply; appeal or postponement gives three. An expired edict costs 3 Loyalty.',gate,f'chi_adm_memorials_send_{name} = yes')
trig('edict_payable','OR = { NOT = { var:chi_adm_memorials_edict = 3 } AND = { var:chi_adm_memorials_edict_stage = 4 is_at_war = yes c:CHI = { gold_reserves >= 5000 } } AND = { NOT = { var:chi_adm_memorials_edict_stage = 4 } is_at_war = yes c:CHI = { gold_reserves >= 10000 } } }')
guard('accept_edict','chi_adm_memorials_edict_reply = yes chi_adm_memorials_edict_payable = yes',f'''if = {{ limit = {{ var:chi_adm_memorials_edict = 1 }} if = {{ limit = {{ var:chi_adm_memorials_edict_stage = 4 }} {stat('corruption',-3)} add_modifier = {{ name = chi_adm_memorials_light_supervision months = 12 }} }} else = {{ {stat('corruption',-5)} if = {{ limit = {{ chi_adm_frontier = yes }} {stat('autonomy',-1)} }} else = {{ {stat('autonomy',-3)} }} add_modifier = {{ name = chi_adm_memorials_supervision months = 12 }} }} }}
if = {{ limit = {{ var:chi_adm_memorials_edict = 2 }} if = {{ limit = {{ var:chi_adm_memorials_edict_stage = 4 }} {stat('loyalty',3)} }} else = {{ {stat('loyalty',5)} {stat('autonomy',-2)} }} add_modifier = {{ name = chi_adm_memorials_honors months = 12 }} }}
if = {{ limit = {{ var:chi_adm_memorials_edict = 3 }} if = {{ limit = {{ var:chi_adm_memorials_edict_stage = 4 }} c:CHI = {{ add_treasury = -5000 }} add_treasury = 5000 {stat('autonomy',2)} }} else = {{ c:CHI = {{ add_treasury = -10000 }} add_treasury = 10000 {stat('autonomy',3)} }} add_modifier = {{ name = chi_adm_memorials_emergency months = 12 }} }}
chi_adm_memorials_clear_edict = yes {result(7)} {notify(True)}''')
guard('appeal_edict','chi_adm_memorials_edict_reply = yes NOT = { has_variable = chi_adm_memorials_edict_appeal_used }',f'set_variable = chi_adm_memorials_edict_appeal_used set_variable = {{ name = chi_adm_memorials_edict_stage value = 2 }} set_variable = {{ name = chi_adm_memorials_edict_left value = 3 }} {result(8)} {notify(True)}')
guard('delay_edict','chi_adm_memorials_edict_reply = yes NOT = { has_variable = chi_adm_memorials_edict_delay_used }',f'set_variable = chi_adm_memorials_edict_delay_used set_variable = {{ name = chi_adm_memorials_edict_stage value = 3 }} set_variable = {{ name = chi_adm_memorials_edict_left value = 3 }} {stat("loyalty",-2)} {result(9)}')
guard('defy_edict','chi_adm_memorials_edict_reply = yes',f'{stat("loyalty",-6)} {relation(-5)} chi_adm_memorials_clear_edict = yes {result(10)} {notify(True)}')
guard('negotiate_edict','chi_adm_memorials_valid = yes var:chi_adm_memorials_edict_stage = 2',f'set_variable = {{ name = chi_adm_memorials_edict_stage value = 4 }} set_variable = {{ name = chi_adm_memorials_edict_left value = 3 }} {result(3)} {notify()}')
guard('withdraw_edict','chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_edict',f'chi_adm_memorials_clear_edict = yes {result(5)} {notify()}')

guard('open_audit','chi_adm_memorials_audit_free = yes',f'''chi_adm_memorials_court_cost = yes set_variable = {{ name = chi_adm_memorials_audit value = 1 }} set_variable = {{ name = chi_adm_memorials_audit_progress value = 0 }} set_variable = {{ name = chi_adm_memorials_audit_left value = 3 }} set_variable = {{ name = chi_adm_memorials_audit_cooldown days = 1095 }} {result(11)} {notify()}''')
for mode,name in [(1,'cooperate'),(2,'obstruct'),(3,'conceal')]:
    extra='gold_reserves >= 5000 var:chi_adm_corruption >= 40' if mode==3 else 'always = yes'
    guard('audit_'+name,'chi_adm_memorials_audit_choice = yes '+extra,f'set_variable = {{ name = chi_adm_memorials_audit value = 2 }} set_variable = {{ name = chi_adm_memorials_audit_mode value = {mode} }} remove_variable = chi_adm_memorials_audit_left '+('add_treasury = -5000 ' if mode==3 else '')+('add_modifier = { name = chi_adm_memorials_audit_burden months = 12 } ' if mode==1 else stat('loyalty',-3) if mode==2 else '')+result(12))
effect('audit_finding',f'''random_list = {{
50 = {{ modifier = {{ if = {{ limit = {{ var:chi_adm_corruption >= 60 }} add = 60 }} if = {{ limit = {{ var:chi_adm_corruption < 20 }} subtract = 40 }} if = {{ limit = {{ var:chi_adm_loyalty >= 60 }} subtract = 20 }} if = {{ limit = {{ var:chi_adm_memorials_audit_mode = 1 }} add = 20 }} if = {{ limit = {{ var:chi_adm_memorials_audit_mode = 3 }} subtract = 30 }} if = {{ limit = {{ has_modifier = chi_adm_memorials_suspicion }} add = 40 }} if = {{ limit = {{ is_at_war = yes }} subtract = 10 }} if = {{ limit = {{ relative_bureaucracy < 0 }} add = 10 }} min = 10 max = 150 }}
set_variable = {{ name = chi_adm_memorials_audit value = 3 }} set_variable = {{ name = chi_adm_memorials_audit_left value = 6 }} add_modifier = {{ name = chi_adm_memorials_exposed months = 12 }} {result(13)} {notify(True)} }}
50 = {{ if = {{ limit = {{ var:chi_adm_memorials_audit_mode = 3 }} {stat('corruption',3)} {stat('autonomy',2)} add_modifier = {{ name = chi_adm_memorials_suspicion months = 48 }} {result(14)} }} else = {{ if = {{ limit = {{ var:chi_adm_memorials_audit_mode = 1 }} {stat('loyalty',2)} {stat('corruption',-3)} }} {result(15)} }} chi_adm_memorials_clear_audit = yes {notify(True)} {notify()} }}
}} remove_modifier = chi_adm_memorials_audit_burden''')
for num,name in [(1,'restitution'),(2,'reform')]:
    guard('propose_'+name,'chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 3',f'set_variable = {{ name = chi_adm_memorials_audit value = 4 }} set_variable = {{ name = chi_adm_memorials_audit_settlement value = {num} }} set_variable = {{ name = chi_adm_memorials_audit_left value = 3 }} {result(16)} {notify()}')
guard('tolerate','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 3 chi_adm_memorials_court_free = yes',f'chi_adm_memorials_court_cost = yes {stat("corruption",3)} {stat("loyalty",2)} add_modifier = {{ name = chi_adm_memorials_suspicion months = 48 }} chi_adm_memorials_clear_audit = yes {result(17)} {notify()}')
guard('pay_restitution','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 4 var:chi_adm_memorials_audit_settlement = 1 gold_reserves >= 10000',f'add_treasury = -10000 c:CHI = {{ add_treasury = 10000 }} {stat("corruption",-12)} {stat("loyalty",-4)} {stat("autonomy",-3)} remove_modifier = chi_adm_memorials_exposed chi_adm_memorials_clear_audit = yes {result(18)} {notify(True)}')
guard('accept_reform','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 4',f'{stat("corruption",-10)} {stat("loyalty",-2)} if = {{ limit = {{ chi_adm_frontier = yes }} {stat("autonomy",-1)} }} else = {{ {stat("autonomy",-3)} }} add_modifier = {{ name = chi_adm_memorials_supervision months = 12 }} remove_modifier = chi_adm_memorials_exposed chi_adm_memorials_clear_audit = yes {result(19)} {notify(True)}')
guard('resist_settlement','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 4',f'{stat("loyalty",-8)} {stat("autonomy",3)} {relation(-5)} chi_adm_memorials_clear_audit = yes {result(20)} {notify(True)}')

effect('repair_delivery_once','if = { limit = { chi_adm_memorials_valid = yes NOT = { has_variable = chi_adm_memorials_delivery_repaired } } set_variable = chi_adm_memorials_delivery_repaired if = { limit = { var:chi_adm_memorials_result = 22 NOT = { has_variable = chi_adm_memorials_edict } } remove_variable = chi_adm_memorials_edict_cooldown set_variable = { name = chi_adm_memorials_result value = 24 } } if = { limit = { var:chi_adm_memorials_result = 23 NOT = { has_variable = chi_adm_memorials_audit } } remove_variable = chi_adm_memorials_audit_cooldown set_variable = { name = chi_adm_memorials_result value = 25 } } }')
effect('ensure_responses','if = { limit = { chi_adm_memorials_valid = yes OR = { has_variable = chi_adm_memorials_memorial has_variable = chi_adm_memorials_edict has_variable = chi_adm_memorials_audit } NOT = { has_journal_entry = chi_adm_memorials_responses } } add_journal_entry = { type = chi_adm_memorials_responses } if = { limit = { chi_adm_memorials_edict_reply = yes var:chi_adm_memorials_edict_left < 3 } set_variable = { name = chi_adm_memorials_edict_left value = 3 } } if = { limit = { OR = { var:chi_adm_memorials_audit = 1 var:chi_adm_memorials_audit = 4 } var:chi_adm_memorials_audit_left < 3 } set_variable = { name = chi_adm_memorials_audit_left value = 3 } } if = { limit = { var:chi_adm_memorials_memorial_stage = 2 var:chi_adm_memorials_memorial_left < 3 } set_variable = { name = chi_adm_memorials_memorial_left value = 3 } } }')
effect('ai_reply','''if = { limit = { chi_adm_memorials_valid = yes is_ai = yes }
 if = { limit = { var:chi_adm_memorials_memorial_stage = 2 } if = { limit = { chi_adm_memorials_can_pay_reduced = yes } chi_adm_memorials_accept_counter = yes } else = { chi_adm_memorials_decline_counter = yes } }
 if = { limit = { chi_adm_memorials_edict_reply = yes }
  if = { limit = { var:chi_adm_loyalty < 40 } chi_adm_memorials_defy_edict = yes }
  else_if = { limit = { var:chi_adm_autonomy >= 60 NOT = { has_variable = chi_adm_memorials_edict_appeal_used } } chi_adm_memorials_appeal_edict = yes }
  else_if = { limit = { chi_adm_memorials_edict_payable = yes } chi_adm_memorials_accept_edict = yes }
  else = { chi_adm_memorials_defy_edict = yes }
 }
 if = { limit = { chi_adm_memorials_audit_choice = yes }
  if = { limit = { var:chi_adm_corruption >= 60 var:chi_adm_loyalty < 60 gold_reserves >= 5000 } chi_adm_memorials_audit_conceal = yes }
  else_if = { limit = { var:chi_adm_loyalty < 40 } chi_adm_memorials_audit_obstruct = yes }
  else = { chi_adm_memorials_audit_cooperate = yes }
 }
 if = { limit = { var:chi_adm_memorials_audit = 4 }
  if = { limit = { var:chi_adm_loyalty < 40 } chi_adm_memorials_resist_settlement = yes }
  else_if = { limit = { var:chi_adm_memorials_audit_settlement = 1 gold_reserves >= 10000 } chi_adm_memorials_pay_restitution = yes }
  else = { chi_adm_memorials_accept_reform = yes }
 }
}''')
# Only active protocols tick; no global country iteration or synchronized UI state.
effect('monthly','''if = { limit = { chi_adm_memorials_valid = no } chi_adm_memorials_cleanup = yes }
else = {
 chi_adm_memorials_ensure_responses = yes
 chi_adm_memorials_ai_reply = yes
 if = { limit = { has_variable = chi_adm_memorials_memorial_left } change_variable = { name = chi_adm_memorials_memorial_left subtract = 1 } if = { limit = { var:chi_adm_memorials_memorial_left <= 0 } chi_adm_memorials_clear_memorial = yes '''+result(21)+''' } }
 if = { limit = { has_variable = chi_adm_memorials_edict_left } change_variable = { name = chi_adm_memorials_edict_left subtract = 1 } if = { limit = { var:chi_adm_memorials_edict_left <= 0 } '''+stat('loyalty',-3)+''' chi_adm_memorials_clear_edict = yes '''+result(22)+''' } }
 if = { limit = { var:chi_adm_memorials_audit = 2 }
  if = { limit = { var:chi_adm_memorials_audit_mode = 1 } change_variable = { name = chi_adm_memorials_audit_progress add = 25 } }
  else_if = { limit = { var:chi_adm_memorials_audit_mode = 3 } change_variable = { name = chi_adm_memorials_audit_progress add = 20 } }
  else = { change_variable = { name = chi_adm_memorials_audit_progress add = 10 } }
  if = { limit = { var:chi_adm_memorials_audit_progress >= 100 } set_variable = { name = chi_adm_memorials_audit_progress value = 100 } chi_adm_memorials_audit_finding = yes }
 }
 else_if = { limit = { has_variable = chi_adm_memorials_audit_left } change_variable = { name = chi_adm_memorials_audit_left subtract = 1 }
  if = { limit = { var:chi_adm_memorials_audit_left <= 0 }
   if = { limit = { var:chi_adm_memorials_audit = 1 } chi_adm_memorials_audit_obstruct = yes }
   else = { '''+stat('loyalty',-3)+''' chi_adm_memorials_clear_audit = yes '''+result(23)+''' }
  }
 }
 if = { limit = { c:CHI = { is_ai = yes } }
  if = { limit = { chi_adm_memorials_memorial_pending = yes }
   if = { limit = { chi_adm_memorials_can_pay_full = yes var:chi_adm_loyalty >= 40 } chi_adm_memorials_approve_memorial = yes }
   else_if = { limit = { chi_adm_memorials_can_pay_reduced = yes } chi_adm_memorials_counter_memorial = yes }
   else = { chi_adm_memorials_reject_memorial = yes }
  }
  if = { limit = { var:chi_adm_memorials_edict_stage = 2 } chi_adm_memorials_negotiate_edict = yes }
  if = { limit = { var:chi_adm_memorials_audit = 3 }
   if = { limit = { gold_reserves >= 10000 var:chi_adm_corruption >= 60 } chi_adm_memorials_propose_restitution = yes }
   else = { chi_adm_memorials_propose_reform = yes }
  }
 }
}''')
effect('ai_dispatch','''if = { limit = { chi_adm_memorials_valid = yes c:CHI = { is_ai = yes } chi_adm_memorials_court_free = yes }
 if = { limit = { chi_adm_memorials_audit_free = yes var:chi_adm_corruption >= 60 } chi_adm_memorials_open_audit = yes }
 else_if = { limit = { chi_adm_memorials_edict_free = yes is_at_war = yes c:CHI = { gold_reserves >= 10000 } } chi_adm_memorials_send_emergency = yes }
 else_if = { limit = { chi_adm_memorials_edict_free = yes chi_adm_memorials_centralised = yes var:chi_adm_corruption >= 40 } chi_adm_memorials_send_supervision = yes }
 else_if = { limit = { chi_adm_memorials_edict_free = yes var:chi_adm_loyalty >= 80 var:chi_adm_corruption < 60 } chi_adm_memorials_send_honors = yes }
}''')

# Functional court actions operate on the row's country; script checks revalidate.
for name,title,description,gate,action in [
('approve_memorial','Approve Memorial','Grant the requested relief. Requires 25 Qing Authority free for six months and sufficient reserves: £20,000 fiscal relief or £10,000 emergency assistance. Discretion: +2% Bureaucracy, +5 Autonomy, +2 Corruption, +2 Loyalty for twelve months.','chi_adm_memorials_memorial_pending = yes chi_adm_memorials_can_pay_full = yes','chi_adm_memorials_approve_memorial = yes'),
('counter_memorial','Offer a Compromise','Commit 25 Qing Authority for six months; offer half the money or +3 Autonomy/+1 Loyalty without the Bureaucracy concession. The governor must accept; funds are checked again at acceptance.','chi_adm_memorials_memorial_pending = yes chi_adm_memorials_can_pay_reduced = yes','chi_adm_memorials_counter_memorial = yes'),
('reject_memorial','Reject Memorial','Close the memorial: provincial Loyalty -3, relations -3. No treasury payment.','chi_adm_memorials_memorial_pending = yes','chi_adm_memorials_reject_memorial = yes'),
('negotiate_edict','Offer Revised Terms','Answer the appeal with the negotiated form of the current edict. The governor must still accept within three reviews.','chi_adm_memorials_valid = yes var:chi_adm_memorials_edict_stage = 2','chi_adm_memorials_negotiate_edict = yes'),
('withdraw_edict','Withdraw Edict','Close the outstanding decree without forcing compliance. Its two-year target cooldown remains.','chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_edict','chi_adm_memorials_withdraw_edict = yes'),
('open_audit','Dispatch the Censorate','Commit 25 Qing Authority for six months; one audit per province every three years. At most two outstanding edicts or audits; one intervention per province. Governor chooses cooperation (4 reviews), obstruction (10) or paid concealment (5). No initial reply after three reviews counts as obstruction. Findings wait six reviews for Qing; settlements allow three for the governor. An expired finding or settlement costs 3 Loyalty. Findings are uncertain.','chi_adm_memorials_audit_free = yes','chi_adm_memorials_open_audit = yes'),
('propose_restitution','Request Restitution','After exposed misconduct, request £10,000 paid from provincial reserves to Qing. Requires governor consent: Corruption -12, Loyalty -4, Autonomy -3. The governor may instead accept administrative reform.','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 3','chi_adm_memorials_propose_restitution = yes'),
('propose_reform','Require an Answer on Reform','Offer supervised administrative reform: Corruption -10, Loyalty -2, Autonomy -3 (-1 frontier), Bureaucracy -2% for twelve months. Governor may refuse.','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 3','chi_adm_memorials_propose_reform = yes'),
('tolerate','Tolerate Local Patronage','Close the finding without restitution: Corruption +3, Loyalty +2; suspicion costs 1% provincial Bureaucracy and increases future detection for four years. Commits 25 Qing Authority for six months; exposed-account penalties remain.','chi_adm_memorials_valid = yes var:chi_adm_memorials_audit = 3 chi_adm_memorials_court_free = yes','chi_adm_memorials_tolerate = yes')]: decision(name,title,description,gate,action)

replies=[
('accept_counter','Accept the Court Compromise','Fiscal compromise: @money!#v 10,000#! and +3 Loyalty. Emergency: @money!#v 5,000#!, +2 Autonomy, +2 Loyalty, +5% military wages for twelve months. Administrative: +3 Autonomy and +1 Loyalty. Court funds are checked again; no second filing cost.','var:chi_adm_memorials_memorial_stage = 2','chi_adm_memorials_can_pay_reduced = yes',30),
('decline_counter','Withdraw the Memorial','Decline the compromise without further penalty; the filing cooldown remains.','var:chi_adm_memorials_memorial_stage = 2','always = yes',5),
('accept_edict','Accept the Imperial Edict','Implement the displayed edict or revised terms. Supervision trades Bureaucracy and discretion for lower Corruption; honors trade discretion for Loyalty/Prestige; aid is paid by Qing. Emergency aid requires an ongoing war and court funds.','chi_adm_memorials_edict_reply = yes','chi_adm_memorials_edict_payable = yes',40),
('appeal_edict','Appeal the Edict','Ask once for revised terms; no compliance is imposed. The court has three monthly reviews to answer.','chi_adm_memorials_edict_reply = yes','NOT = { has_variable = chi_adm_memorials_edict_appeal_used }',15),
('delay_edict','Request Time for the Edict','One deliberate postponement: Loyalty -2 and a three-review window.','chi_adm_memorials_edict_reply = yes','NOT = { has_variable = chi_adm_memorials_edict_delay_used }',5),
('defy_edict','Decline the Edict','Keep local arrangements. Loyalty -6 and relations -5; no forced laws, appointment or annexation.','chi_adm_memorials_edict_reply = yes','always = yes',5),
('audit_cooperate','Open the Provincial Registers','Cooperate: investigation advances 25/100 each monthly review. Bureaucracy -2% during investigation. Disclosure is more likely; a clean finding gives Loyalty +2 and Corruption -3.','chi_adm_memorials_audit_choice = yes','always = yes',40),
('audit_obstruct','Obstruct the Inspectors','Investigation advances only 10/100 each review. Loyalty -3; delay cannot stop the inquiry indefinitely.','chi_adm_memorials_audit_choice = yes','always = yes',10),
('audit_conceal','Conceal the Accounts','Spend £5,000 from your reserves (not a transfer). Requires Corruption at least 40. Progress 20/100 each review; discovery is less likely. Successful concealment adds 3 Corruption, 2 Autonomy and four years of suspicion (-1% Bureaucracy and higher future detection).','chi_adm_memorials_audit_choice = yes','gold_reserves >= 5000 var:chi_adm_corruption >= 40',10),
('pay_restitution','Authorize Restitution','Pay £10,000 from provincial reserves to Qing; Corruption -12, Loyalty -4, Autonomy -3. Removes exposed-account burden.','var:chi_adm_memorials_audit = 4 var:chi_adm_memorials_audit_settlement = 1','gold_reserves >= 10000',30),
('accept_reform','Accept Administrative Reform','Corruption -10, Loyalty -2, Autonomy -3 (-1 frontier); Bureaucracy -2% for twelve months. Removes exposed-account burden. Available instead of restitution if money is scarce.','var:chi_adm_memorials_audit = 4','always = yes',30),
('resist_settlement','Refuse the Settlement','Keep your treasury and local organization. Loyalty -8, Autonomy +3, relations -5; exposed-account burden remains until its expiry.','var:chi_adm_memorials_audit = 4','always = yes',5)]
for name,title,description,visible,gate,weight in replies:
    button(name,title,description,'chi_adm_memorials_valid = yes '+visible,'chi_adm_memorials_valid = yes '+visible+' '+gate,'chi_adm_memorials_'+name+' = yes',weight)

for name,body in [('memorial_row','chi_adm_memorials_valid = yes OR = { has_variable = chi_adm_memorials_memorial has_variable = chi_adm_memorials_memorial_record }'),('edict_row','chi_adm_memorials_valid = yes'),('audit_row','chi_adm_memorials_valid = yes')]: G['chi_adm_memorials_'+name]=f'scope = country is_valid = {{ {body} }}'
G['chi_adm_memorials_audit_bar']='scope = country is_valid = { chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_audit }'
for kind in ('memorial','edict','audit'): G['chi_adm_memorials_'+kind+'_detail']=f'scope = country is_valid = {{ chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_{kind} }}'
G['chi_adm_memorials_register_record']='scope = country is_valid = { chi_adm_memorials_valid = yes has_variable = chi_adm_memorials_result }'

mods={
'court_staff':('country_authority_add = -25','Court Correspondence','Provincial correspondence occupies imperial clerks for six months.'),
'clerks':('country_authority_add = -25','Memorial Clerks','Preparing the memorial occupies provincial clerks for six months.'),
'discretion':('country_bureaucracy_mult = 0.02','Administrative Latitude','Temporary discretion relieves provincial administrative burdens.'),
'supervision':('country_bureaucracy_mult = -0.02','Supervised Provincial Offices','Reorganizing the offices occupies provincial staff for twelve months.'),
'light_supervision':('country_bureaucracy_mult = -0.01','Negotiated Supervision','A narrower review occupies fewer provincial clerks.'),
'honors':('country_prestige_mult = 0.05','Imperial Commendation','The Dragon Throne has recognized this administration.'),
'emergency':('country_military_wages_mult = 0.05','Emergency Military Discretion','Temporary authorization carries higher military payroll obligations; no army reform bonus is added.'),
'audit_burden':('country_bureaucracy_mult = -0.02','Censorate Investigation','Opening the registers occupies provincial staff during investigation.'),
'exposed':('country_bureaucracy_mult = -0.02','Exposed Accounts','Unresolved misconduct disrupts the provincial offices for up to twelve months.'),
'suspicion':('country_bureaucracy_mult = -0.01','Suspected Patronage','Suspect accounts impair administration and increase future audit detection for four years.')}
write('common/static_modifiers/chi_adm_memorials.txt','\n'.join(f'chi_adm_memorials_{name} = {{ icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds {body} }}' for name,(body,title,desc) in mods.items()))
for name,(_,title,desc) in mods.items():loc(name,title);loc(name+'_desc',desc)
# Explicitly replace same-name timed modifiers instead of allowing accumulation.
for name,body in E.items():
    E[name]=re.sub(r'add_modifier\s*=\s*{\s*name\s*=\s*(chi_adm_memorials_\w+)',lambda m:'remove_modifier = '+m[1]+' '+m[0],body)
presentation.apply(E,B,G,LOC,T)
for folder,data in [('scripted_triggers',T),('scripted_effects',E),('scripted_buttons',B),('scripted_guis',G)]:write(f'common/{folder}/chi_adm_memorials.txt','\n\n'.join(f'{name} = {{\n{body}\n}}' for name,body in data.items()))
write('common/on_actions/chi_adm_memorials.txt','''on_monthly_pulse_country = { on_actions = { chi_adm_memorials_tick } }
chi_adm_memorials_tick = { trigger = { OR = { AND = { chi_adm_memorials_valid = yes NOT = { has_variable = chi_adm_memorials_delivery_repaired } } has_variable = chi_adm_memorials_memorial has_variable = chi_adm_memorials_edict has_variable = chi_adm_memorials_audit has_modifier = chi_adm_memorials_exposed has_modifier = chi_adm_memorials_supervision has_modifier = chi_adm_memorials_light_supervision has_modifier = chi_adm_memorials_discretion has_modifier = chi_adm_memorials_honors has_modifier = chi_adm_memorials_emergency has_modifier = chi_adm_memorials_suspicion AND = { chi_adm_memorials_valid = yes c:CHI = { is_ai = yes } } } } effect = { chi_adm_memorials_repair_delivery_once = yes chi_adm_memorials_monthly = yes chi_adm_memorials_ai_dispatch = yes } }''')

for key,title in [('memorials','Imperial Memorials'),('edicts','Imperial Edicts'),('audits','Imperial Audits'),('responses','Provincial Correspondence')]:
    loc(key,title);loc(key+'_reason',{'memorials':'Governors and viceroys send memorials to the Dragon Throne. Approve a request, negotiate narrower terms or refuse it. Every concession is entered in the provincial registers.', 'edicts':'Address individual administrations through supervision, commendation or emergency assistance. Governors may accept, appeal, postpone or decline the court\'s instructions.', 'audits':'The Censorate examines the accounts. Cooperation opens the registers; obstruction slows the inquiry; concealment risks later suspicion. Exposed misconduct requires a negotiated settlement.', 'responses':'Reply to the court and the Censorate. Treasury payments and changes in local administration require your decision.'}[key]);loc(key+'_status','Review the current correspondence and available actions.')
loc('closed','This correspondence is closed because the administration is no longer in imperial service.')
loc('req','An eligible Qing administration or a valid Qing court')
entries=[]
for key in ('memorials','edicts','audits','responses'):
    province=key=='responses';valid='chi_adm_memorials_valid = yes OR = { has_variable = chi_adm_memorials_memorial has_variable = chi_adm_memorials_edict has_variable = chi_adm_memorials_audit }' if province else 'chi_adm_memorials_court = yes'
    buttons='\n'.join('scripted_button = chi_adm_memorials_'+x[0] for x in replies) if province else ''
    entries.append(f'''chi_adm_memorials_{key} = {{
icon = "gfx/interface/icons/event_icons/event_scales.dds"
group = {'je_group_chi_adm_court_register_province' if province else 'je_group_chi_adm_court_register_court'}
context = country transferable = no can_revolution_inherit = no
is_shown_when_inactive = {{ {valid} }} possible = {{ {valid} }}
activation_description = {{ custom_tooltip = {{ text = chi_adm_memorials_req {valid} }} }}
widget = {{ gui = "gui/journal_entry_widgets/chi_adm_memorials.gui" name = "chi_adm_memorials_{key}" container = "custom_widget_container_1" }}
{buttons}
outcome = {{ flags = {{ hidden invalid_outcome }} conclusion_desc = chi_adm_memorials_closed trigger = {{ NOT = {{ {valid} }} }} {'effect = { if = { limit = { chi_adm_memorials_valid = no } chi_adm_memorials_cleanup = yes } }' if province else ''} }}
}}''')
write('common/journal_entries/chi_adm_memorials.txt','\n'.join(entries))

# Small informational events only; decisions stay accessible in the JEs.
loc('court_notice','A Memorial Reaches the Dragon Throne')
loc('court_notice_desc',"[SCOPE.sCountry('chi_adm_memorials_province').GetName] has entered a new reply in the registers. Open Governance of the Empire to review Imperial Memorials, Edicts and Audits. The live record contains the current case and costs.")
loc('province_notice','Instructions from the Dragon Throne')
loc('province_notice_desc','New correspondence has reached the provincial offices. [ROOT.GetCountry.GetCustom(\'chi_adm_memorials_result\')]\nReview Provincial Correspondence beneath The Governor\'s Accounts. Acknowledging this notice never authorizes a payment or compliance.')
loc('ack','Enter it in the registers.')
write('events/chi_adm_memorials.txt','namespace = chi_adm_memorials\n'+'\n'.join(f'''chi_adm_memorials.{i} = {{ type = country_event placement = ROOT title = chi_adm_memorials_{title} desc = chi_adm_memorials_{desc} event_image = {{ video = "ep1_persian_court" }} icon = "gfx/interface/icons/event_icons/event_scales.dds" duration = 3 {gate} option = {{ name = chi_adm_memorials_ack default_option = yes }} }}''' for i,title,desc,gate in [(1,'court_notice','court_notice_desc','cancellation_trigger = { NOT = { exists = scope:chi_adm_memorials_province } }'),(2,'province_notice','province_notice_desc','trigger = { chi_adm_memorials_valid = yes }')]))

# Same native button gates and helpers, now also available in the event.
import validate_chi_adm as _core
_options=[]
for _name,*_ in replies:
    _button=_core.parse(B['chi_adm_memorials_'+_name])
    _visible=_core.get(_button,'visible')
    _possible=_core.get(_button,'possible')
    _live=_core.get(_core.get(_button,'effect'),'hidden_effect')
    _options.append('option = { name = chi_adm_memorials_'+_name+' trigger = { '+presentation.emit(_visible+_possible)+' } show_as_unavailable = { '+presentation.emit(_visible)+' } custom_tooltip = chi_adm_memorials_'+_name+'_desc hidden_effect = { '+presentation.emit(_live)+' } ai_chance = { '+presentation.emit(_core.get(_button,'ai_chance'))+' } }')
_event=(ROOT/'events/chi_adm_memorials.txt').read_text(encoding='utf-8')
_event=_event[:_event.index('chi_adm_memorials.2 =')]+'''chi_adm_memorials.2 = { type = country_event placement = ROOT title = chi_adm_memorials_province_notice desc = chi_adm_memorials_province_notice_desc event_image = { video = "ep1_persian_court" } icon = "gfx/interface/icons/event_icons/event_scales.dds" duration = 30 trigger = { chi_adm_memorials_valid = yes } '''+ '\n'.join(_options)+''' option = { name = chi_adm_memorials_ack default_option = yes ai_chance = { base = 0 } } }'''
write('events/chi_adm_memorials.txt',_event)

def custom(name,var,mapping):
    C['chi_adm_memorials_'+name]='type = country\n'+'\n'.join(f'text = {{ trigger = {{ var:chi_adm_memorials_{var} = {i} }} localization_key = {loc(name+"_"+str(i),text)} }}' for i,text in mapping.items())+f'\ntext = {{ trigger = {{ always = yes }} localization_key = {loc("none","No active case")} }}'
custom('memorial_name','memorial',{1:'Fiscal relief',2:'Administrative latitude',3:'Emergency military assistance'})
custom('memorial_stage','memorial_stage',{1:'Before the Dragon Throne',2:'Court compromise awaiting provincial consent'})
custom('edict_name','edict',{1:'Administrative supervision',2:'Imperial commendation',3:'Emergency military assistance'})
custom('edict_stage','edict_stage',{1:'Awaiting the governor\'s reply',2:'Appeal before the court',3:'Deliberate postponement',4:'Revised terms awaiting consent'})
C['chi_adm_memorials_edict_terms']='type = country\n'
for i,(name,title,description,extra) in enumerate(edicts,1):
    C['chi_adm_memorials_edict_terms']+=f'text = {{ trigger = {{ var:chi_adm_memorials_edict = {i} }} localization_key = {loc("edict_terms_"+str(i),description)} }}\n'
C['chi_adm_memorials_edict_terms']+='text = { trigger = { always = yes } localization_key = chi_adm_memorials_none }'
custom('audit_stage','audit',{1:'Awaiting access to the registers',2:'Investigation in progress',3:'Misconduct exposed: court decision required',4:'Settlement awaiting provincial consent'})
custom('audit_mode','audit_mode',{1:'Open cooperation: +25 progress per review',2:'Obstruction: +10 progress per review',3:'Concealment: +20 progress per review'})
C['chi_adm_memorials_audit_deadline']='type = country text = { trigger = { has_variable = chi_adm_memorials_audit_left } localization_key = chi_adm_memorials_audit_reply_left } text = { trigger = { always = yes } localization_key = chi_adm_memorials_audit_no_deadline }'
loc('audit_reply_left',"Response reviews remaining: [Country.MakeScope.Var('chi_adm_memorials_audit_left').GetValue|0]")
loc('audit_no_deadline','The investigation advances at the rate shown above.')
custom('result','result',{1:'Memorial filed',2:'Memorial granted',3:'Revised terms offered',4:'Memorial rejected',5:'Correspondence withdrawn',6:'Edict dispatched',7:'Edict accepted',8:'Appeal filed',9:'Edict postponed',10:'Edict declined',11:'Audit opened',12:'Registers under examination',13:'Misconduct exposed',14:'Concealment succeeded; suspicion remains',15:'Inquiry closed without a finding',16:'Settlement proposed',17:'Local patronage tolerated',18:'Restitution paid',19:'Administrative reform accepted',20:'Settlement refused',21:'Memorial expired unanswered',22:'Edict expired: Loyalty -3',23:'Audit settlement expired: Loyalty -3',24:'Expired edict delivery repaired; the court may resend',25:'Expired audit delivery repaired; the court may resend'})
write('common/customizable_localization/chi_adm_memorials.txt','\n\n'.join(f'{name} = {{ {body} }}' for name,body in C.items()))
loc('memorial_display',"Memorial: [Country.GetCustom('chi_adm_memorials_memorial_name')]\n[Country.GetCustom('chi_adm_memorials_memorial_stage')]\nMonthly reviews remaining: [Country.MakeScope.Var('chi_adm_memorials_memorial_left').GetValue|0]")
loc('edict_display',"Edict: [Country.GetCustom('chi_adm_memorials_edict_name')]\n[Country.GetCustom('chi_adm_memorials_edict_stage')]\nMonthly reviews remaining: [Country.MakeScope.Var('chi_adm_memorials_edict_left').GetValue|0]")
loc('edict_terms_display',"[Country.GetCustom('chi_adm_memorials_edict_terms')]")
loc('audit_display',"Censorate: [Country.GetCustom('chi_adm_memorials_audit_stage')]\n[Country.GetCustom('chi_adm_memorials_audit_mode')]\nInvestigation: [Country.MakeScope.Var('chi_adm_memorials_audit_progress').GetValue|0]/100\n[Country.GetCustom('chi_adm_memorials_audit_deadline')]")
loc('result_display',"Last entry: [Country.GetCustom('chi_adm_memorials_result')]")
loc('desk_display','Memorials require 25 provincial Authority for six months and a two-year filing cooldown. One petition may be pending at a time. Replies arrive in Provincial Correspondence. Frontier memorials preserve customary arrangements.')
loc('audit_chances','Detection weights: base 50 against 50 for no finding; +60 at Corruption 60+, -40 below Corruption 20, -20 at Loyalty 60+, +20 cooperation, -30 concealment, +40 prior suspicion, -10 war, +10 Bureaucracy deficit. Detection weight is bounded 10-150. Discovery disrupts Bureaucracy by 2% for twelve months; court settlements require your answer.')

def txt(key,width=440): return f'textbox = {{ size = {{ {width} 0 }} max_width = {width} autoresize = yes multiline = yes text = "chi_adm_memorials_{key}" }}'
def compact_accounts():
    output='widget = { size = { 440 66 } background = { using = dark_area } background = { using = frame_small }\n'
    for i,(kind,texture) in enumerate([('loyalty','gold'),('autonomy','default'),('corruption','bad')]):
        loc('compact_'+kind,f"@chi_adm_{kind}![Nbsp]{kind[0].upper()} #v [Country.MakeScope.Var('chi_adm_{kind}').GetValue|0]#!")
        loc('compact_'+kind+'_tooltip',f"[concept_chi_adm_{kind}]: #v [Country.MakeScope.Var('chi_adm_{kind}').GetValue|0]#!/100\n[Country.GetCustom('chi_adm_{kind}_tier')]")
        output+=f'''widget = {{ position = {{ {8+i*144} 10 }} size = {{ 136 46 }} tooltip = "chi_adm_memorials_compact_{kind}_tooltip"
textbox = {{ size = {{ 136 26 }} align = center|nobaseline text = "chi_adm_memorials_compact_{kind}" }}
progressbar = {{ position = {{ 0 32 }} size = {{ 136 10 }} min = 0 max = 100 value = "[FixedPointToFloat(Country.MakeScope.Var('chi_adm_{kind}').GetValue)]" progresstexture = "gfx/interface/progressbar/progressbar_{texture}.dds" noprogresstexture = "gfx/interface/progressbar/progressbar_empty.dds" direction = horizontal skip_initial_animation = yes }}
}}'''
    return output+'}'
def bar(): return '''progressbar = { size = { 440 18 } visible = "[GetScriptedGui('chi_adm_memorials_audit_bar').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]" min = 0 max = 100 value = "[FixedPointToFloat(Country.MakeScope.Var('chi_adm_memorials_audit_progress').GetValue)]" progresstexture = "gfx/interface/progressbar/progressbar_gold.dds" noprogresstexture = "gfx/interface/progressbar/progressbar_empty.dds" direction = horizontal skip_initial_animation = yes tooltip = "chi_adm_memorials_audit_chances" }'''
gui=[]
for key,actions in [('memorials',['approve_memorial','counter_memorial','reject_memorial']),('edicts',['send_supervision','send_honors','send_emergency','negotiate_edict','withdraw_edict']),('audits',['open_audit','propose_restitution','propose_reform','tolerate'])]:
    rowtype={'memorials':'memorial','edicts':'edict','audits':'audit'}[key]
    gui.append(f'''flowcontainer = {{ name = "chi_adm_memorials_{key}" direction = vertical parentanchor = hcenter spacing = 10
 flowcontainer = {{ direction = vertical spacing = 8 ignoreinvisible = yes datamodel = "[AccessPlayer.GetSubjects]" item = {{
 flowcontainer = {{ direction = vertical spacing = 8 visible = "[GetScriptedGui('chi_adm_memorials_{rowtype}_row').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
 section_header_button = {{ blockoverride "layout" {{ size = {{ 472 38 }} }} blockoverride "left_text" {{ text = "[Country.GetNameNoFormatting]" }}
 blockoverride "onclick" {{ onclick = "[GetVariableSystem.Toggle(Concatenate('chi_adm_memorials_{key}_', Country.GetNameNoFormatting))]" }}
 blockoverride "onclick_showmore" {{ visible = "[Not(GetVariableSystem.Exists(Concatenate('chi_adm_memorials_{key}_', Country.GetNameNoFormatting)))]" }}
 blockoverride "onclick_showless" {{ visible = "[GetVariableSystem.Exists(Concatenate('chi_adm_memorials_{key}_', Country.GetNameNoFormatting))]" }} }}
 flowcontainer = {{ direction = vertical spacing = 8 ignoreinvisible = yes margin = {{ 16 12 }} visible = "[GetVariableSystem.Exists(Concatenate('chi_adm_memorials_{key}_', Country.GetNameNoFormatting))]"
 {compact_accounts() if key in ('audits','edicts') else ''}
 {txt(rowtype+'_display')} {bar() if key=='audits' else ''} {txt('result_display')}
''')
    for action in actions:
        visibility = "visible = \"[GetScriptedGui('chi_adm_memorials_edict_detail').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]\"" if action in ('negotiate_edict','withdraw_edict') else ''
        gui.append(f'''button = {{ {visibility} size = {{ 440 58 }} using = default_button_action enabled = "[GetScriptedGui('chi_adm_memorials_{action}').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]" onclick = "[GetScriptedGui('chi_adm_memorials_{action}').Execute(GuiScope.SetRoot(Country.MakeScope).End)]" tooltip = "chi_adm_memorials_{action}_tt" textbox = {{ size = {{ 416 0 }} max_width = 416 autoresize = yes multiline = yes parentanchor = center align = center|nobaseline text = "chi_adm_memorials_{action}" alwaystransparent = yes }} }}''')
    gui.append('} } } } }')
details=''
for kind in ('memorial','edict','audit'):
    details+=f'''flowcontainer = {{ direction = vertical spacing = 8 visible = "[GetScriptedGui('chi_adm_memorials_{kind}_detail').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]" {txt(kind+'_display')} {txt('edict_terms_display') if kind=='edict' else ''} {bar() if kind=='audit' else ''} }}'''
gui.append('flowcontainer = { name = "chi_adm_memorials_responses" direction = vertical parentanchor = hcenter spacing = 10 ignoreinvisible = yes datacontext = "[JournalEntry.GetCountry]" '+presentation.bars()+details+txt('result_display')+' }')
gui.append('flowcontainer = { name = "chi_adm_memorials_desk_status" direction = vertical parentanchor = hcenter spacing = 8 ignoreinvisible = yes datacontext = "[JournalEntry.GetCountry]" '+presentation.bars()+txt('desk_display')+'''flowcontainer = { direction = vertical visible = "[GetScriptedGui('chi_adm_memorials_memorial_detail').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]" '''+txt('memorial_display')+'''} flowcontainer = { direction = vertical visible = "[GetScriptedGui('chi_adm_memorials_register_record').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]" '''+txt('result_display')+' } }')
# ExecuteTooltip is the native presentation side of the same scripted GUI used
# by the court button. Its live helper is hidden; only the read-only preview shows.
source='\n'.join(gui)
source=re.sub(r'tooltip = "chi_adm_memorials_(\w+)_tt"',lambda m:'tooltip = "[GetScriptedGui(\'chi_adm_memorials_'+m[1]+'\').ExecuteTooltip(GuiScope.SetRoot(Country.MakeScope).End)]"',source)
gui=[source]
write('gui/journal_entry_widgets/chi_adm_memorials.gui','\n'.join(gui))

concepts={
 'loyalty':('Loyalty','Provincial Loyalty measures an administration\'s willingness to serve the Qing throne on a scale of #v 0–100#!. It influences cooperation, negotiation and political tension. It adjusts payments to the [concept_overlord] by -50% at 0 Loyalty, 0% at 50 and +50% at 100, multiplying the pact rate. It is distinct from [concept_liberty_desire] and interest-group loyalty; a loyal governor may still petition or refuse an imperial request.'),
 'autonomy':('Autonomy','Administrative Autonomy measures an office\'s freedom to conduct provincial affairs on a scale of #v 0–100#!. It adjusts payments to the [concept_overlord] by +50% at 0 Autonomy, 0% at 50 and -50% at 100. This adds to the Loyalty adjustment before multiplying the pact rate. Greater discretion encourages negotiation and makes closer supervision politically costly. It does not by itself mean disloyalty. Memorials, court settlements and audits may change it.'),
 'corruption':('Corruption','Provincial Corruption measures patronage and concealed accounts on a scale of #v 0–100#!. It changes [concept_tax_capacity] continuously: #g +25%#! at 0, #v 0%#! at 50 and #r -25%#! at 100. Each point reduces the modifier by 0.5 percentage points. Corruption at #v 60#! or above increases detection weight in imperial audits. Investigation, restitution and supervised reform can improve the accounts.')}
write('common/game_concepts/chi_adm.txt','\n'.join('concept_chi_adm_'+kind+' = { texture = "'+presentation.ICONS[kind]+'" }' for kind in concepts))
write('gui/chi_adm_texticons.gui','\n'.join('texticon = { icon = chi_adm_'+kind+' iconsize = { offset = { 0 22 } fontsize = 82 texture = "'+texture+'" } }' for kind,texture in presentation.ICONS.items()))
for kind,(title,desc) in concepts.items():
    LOC['concept_chi_adm_'+kind]=title
    LOC['concept_chi_adm_'+kind+'_desc']=desc

presentation.court_text(LOC)

def integrate():
    path=ROOT/'common/journal_entries/chi_adm_court_register_governance.txt'
    text=path.read_text('utf-8-sig')
    marker=' scripted_button = chi_adm_supervise_offices'
    if 'scripted_button = chi_adm_memorials_file_relief' not in text:
        text=text.replace(marker,marker+'\n'+ '\n'.join(' scripted_button = chi_adm_memorials_file_'+x[0] for x in memorials)+'\n widget = { gui = "gui/journal_entry_widgets/chi_adm_memorials.gui" name = "chi_adm_memorials_desk_status" container = "custom_widget_container_2" }')
        path.write_text(text,encoding='utf-8')
    path=ROOT/'localization/english/chi_adm_l_english.yml'
    text=path.read_text('utf-8-sig')
    text=re.sub(r'^ chi_adm_memorials_\w+:.*\n','',text,flags=re.M)
    text=re.sub(r'^ concept_chi_adm_\w+:.*\n','',text,flags=re.M)
    text=presentation.older_desk_loc(text)
    text=text.replace(' # Memorials, Edicts and Audits\n','')
    block=' # Memorials, Edicts and Audits\n'
    for key,value in LOC.items():
        assert '"' not in value
        if not key.startswith('concept_'):value=presentation.enrich(value)
        block+=f' {key}: "{value.replace(chr(10),chr(92)+"n")}"\n'
    # imperial law reform owns its generated mappings at EOF. Insert memorials and audits ahead of that block so
    # both generators remain idempotent without removing any imperial law reform localization.
    at=re.search(r'^ chi_adm_imperial_law_(?:requested_name|group_name|current_name|requested_icon|current_icon)_\d+:',text,re.M)
    pos=at.start() if at else len(text)
    text=text[:pos].rstrip()+'\n\n'+block+text[pos:]
    path.write_text(text,encoding='utf-8-sig')
integrate()
print(f'Built memorials and audits: {len(E)} effects, {len(B)} provincial buttons, {len(G)} court/display GUIs, {len(LOC)} localized strings')
