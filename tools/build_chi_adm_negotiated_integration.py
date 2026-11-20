"""negotiated integration negotiated integration. Generate owned files; patch only old integration entry points."""
from pathlib import Path
import json,re,hashlib
import validate_chi_adm as core
ROOT=Path(__file__).resolve().parents[1]
GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
P='chi_adm_negotiated_integration_'
E={};T={};G={};LOC={}
def write(path,text): (ROOT/path).write_text(text.rstrip()+'\n',encoding='utf-8')
def loc(key,text):LOC[P+key]=text;return P+key
def sv(key,value):return f'set_variable = {{ name = {P+key} value = {value} }}'
def rm(key):return 'remove_variable = '+P+key
def adj(key,value):return f'chi_adm_adjust_{key} = {{ AMOUNT = {value} }}'
def bump():return 'if = { limit = { NOT = { has_variable = chi_adm_negotiated_integration_revision } } set_variable = { name = chi_adm_negotiated_integration_revision value = 0 } } change_variable = { name = chi_adm_negotiated_integration_revision add = 1 }'
def send(n,court=False):
    s='save_scope_as = chi_adm_negotiated_integration_target save_scope_value_as = { name = chi_adm_negotiated_integration_revision value = var:chi_adm_negotiated_integration_revision } '
    return s+('c:CHI = { ' if court else '')+f'trigger_event = {{ id = chi_adm_negotiated_integration.{n} popup = yes }}'+(' }' if court else '')
def effect(key,text):E[P+key]=text

patched=['common/scripted_buttons/tyrone_qing_administrations.txt','gui/journal_entry_widgets/chi_adm_court_register_ledger.gui']
baseline=ROOT/'tools/chi_adm_negotiated_integration_baseline.json'
if not baseline.exists():
    files={}
    for directory in ('common/scripted_effects','common/scripted_triggers','common/journal_entries','common/static_modifiers','common/on_actions','common/diplomatic_actions','events'):
        for path in (ROOT/directory).glob('*chi_adm*'):
            files[path.relative_to(ROOT).as_posix()]=hashlib.sha256(path.read_bytes()).hexdigest()
    for path in ('common/history/global/zzzz_qing_administrations.txt','common/scripted_effects/tyrone_qing_administrations.txt','common/diplomatic_actions/tyrone_qing_administrations.txt','common/diplomatic_plays/tyrone_chinese_warlords.txt','common/scripted_effects/tyrone_chinese_warlords.txt'):
        files[path]=hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
    baseline.write_text(json.dumps({'files':files,'buttons':core.load(patched[0]),'ledger':(ROOT/patched[1]).read_text('utf-8')},indent=2),encoding='utf-8')

T.update({
P+'valid':'chi_adm_target_valid = yes NOT = { has_war_with = c:CHI } NOT = { is_diplomatic_play_enemy_of = c:CHI }',
P+'court':'c:CHI ?= this chi_adm_court_valid = yes',
P+'resources':'c:CHI = { authority >= 0 relative_bureaucracy >= 0 }',
P+'active':'has_variable = chi_adm_negotiated_integration_work NOT = { has_variable = chi_adm_negotiated_integration_paused }',
P+'can_propose':'''chi_adm_negotiated_integration_valid = yes NOT = { has_variable = chi_adm_negotiated_integration_stage } NOT = { has_variable = chi_adm_negotiated_integration_retry }
NOT = { has_variable = chi_adm_negotiated_integration_repayment_left } var:chi_adm_autonomy <= 25 is_at_war = no is_diplomatic_play_committed_participant = no
c:CHI = { has_technology_researched = central_archives has_variable = chi_qing_centralisation_unlocked authority >= 0 relative_bureaucracy >= 0 is_at_war = no is_diplomatic_play_committed_participant = no }''',
P+'can_begin':'chi_adm_negotiated_integration_valid = yes chi_adm_negotiated_integration_resources = yes OR = { var:chi_adm_negotiated_integration_stage = 1 var:chi_adm_negotiated_integration_stage = 2 }',
P+'reply':'chi_adm_negotiated_integration_valid = yes var:chi_adm_negotiated_integration_stage = 1',
P+'court_reply':'chi_adm_negotiated_integration_valid = yes var:chi_adm_negotiated_integration_stage = 2',
P+'event_current':'exists = scope:chi_adm_negotiated_integration_target scope:chi_adm_negotiated_integration_target = { chi_adm_negotiated_integration_valid = yes var:chi_adm_negotiated_integration_revision = scope:chi_adm_negotiated_integration_revision }',
P+'can_finish':'''chi_adm_negotiated_integration_valid = yes chi_adm_negotiated_integration_active = yes NOT = { has_variable = chi_adm_negotiated_integration_breach }
var:chi_adm_negotiated_integration_elapsed >= chi_adm_negotiated_integration_required
OR = { AND = { is_ai = yes NOT = { has_variable = chi_adm_negotiated_integration_player_agreed } } has_variable = chi_adm_negotiated_integration_final_consent }''',
P+'coercible':'''chi_adm_negotiated_integration_valid = yes is_at_war = no is_diplomatic_play_committed_participant = no
OR = { AND = { var:chi_adm_negotiated_integration_stage = 2 OR = { var:chi_adm_negotiated_integration_response = 2 var:chi_adm_negotiated_integration_response = 4 } }
AND = { var:chi_adm_negotiated_integration_stage = 1 var:chi_adm_negotiated_integration_wait >= 6 } var:chi_adm_negotiated_integration_stage = 6 AND = { var:chi_adm_negotiated_integration_stage = 9 OR = { var:chi_adm_negotiated_integration_fault = 2 has_variable = chi_adm_negotiated_integration_repayment_refused } } }
c:CHI = { is_at_war = no is_diplomatic_play_committed_participant = no }'''
})
effect('recount','''set_variable = { name = chi_adm_negotiated_integration_count value = 0 }
every_subject_or_below = { limit = { chi_adm_negotiated_integration_valid = yes chi_adm_negotiated_integration_active = yes }
c:CHI = { change_variable = { name = chi_adm_negotiated_integration_count add = 1 } } }''')
effect('stop_payments',' '.join(f'c:CHI ?= {{ remove_diplomatic_pact = {{ country = root type = chi_adm_negotiated_integration_{k} }} }}' for k in ('subsidy','subsidy_strong','repayment','repayment_half')))
effect('apply_subsidy','''chi_adm_negotiated_integration_stop_payments = yes
if = { limit = { NOT = { has_variable = chi_adm_negotiated_integration_paused } }
if = { limit = { var:chi_adm_negotiated_integration_subsidy = 1 } c:CHI = { create_diplomatic_pact = { country = root type = chi_adm_negotiated_integration_subsidy } } }
else_if = { limit = { var:chi_adm_negotiated_integration_subsidy = 2 } c:CHI = { create_diplomatic_pact = { country = root type = chi_adm_negotiated_integration_subsidy_strong } } }
}''')
FIELDS='stage work paused elapsed response wait subsidy protection honors pressure final_offer final_consent final_sent suspend_request suspend_age suspend_refused breach fault paid_terms repayment_offer repayment_requested repayment_refused cancel_request requested_subsidy requested_protection requested_honors player_agreed'.split()
effect('clear','chi_adm_negotiated_integration_stop_payments = yes '+' '.join(rm(k) for k in FIELDS)+' '+bump()+' c:CHI ?= { chi_adm_negotiated_integration_recount = yes }')
effect('close','chi_adm_negotiated_integration_clear = yes '+sv('retry','yes months = 6'))
effect('ensure','''if = { limit = { NOT = { has_journal_entry = chi_adm_negotiated_integration_province } } add_journal_entry = { type = chi_adm_negotiated_integration_province } }
c:CHI = { if = { limit = { NOT = { has_journal_entry = chi_adm_negotiated_integration_court } } add_journal_entry = { type = chi_adm_negotiated_integration_court } } }''')
effect('propose','chi_adm_negotiated_integration_clear = yes '+' '.join(sv(k,v) for k,v in [('stage',1),('elapsed',0),('wait',0),('subsidy',0),('protection',0),('honors',0)])+' chi_adm_negotiated_integration_ensure = yes '+send(1))
effect('begin',sv('stage',3)+' '+sv('work','yes')+' '+sv('elapsed',0)+' '+rm('wait')+' '+rm('response')+' '+bump()+'''
if = { limit = { is_ai = no } set_variable = chi_adm_negotiated_integration_player_agreed }
chi_adm_negotiated_integration_apply_subsidy = yes
if = { limit = { var:chi_adm_negotiated_integration_subsidy > 0 } set_variable = chi_adm_negotiated_integration_paid_terms }
if = { limit = { var:chi_adm_negotiated_integration_honors > 0 exists = ruler }
ruler = { remove_modifier = chi_adm_negotiated_integration_honored add_modifier = { name = chi_adm_negotiated_integration_honored years = 10 } }
 c:CHI = {
  remove_modifier = chi_adm_negotiated_integration_honors_patronage
  add_modifier = { name = chi_adm_negotiated_integration_honors_patronage years = 5 }
 }
'''+adj('loyalty',3)+''' change_relations = { country = c:CHI value = 5 } }
c:CHI = { chi_adm_negotiated_integration_recount = yes }''')
for key,response in [('centralize',2),('request_subsidy',3),('request_protection',3),('request_honors',3),('refuse',4),('delay',5)]:
    request=key.removeprefix('request_') if key.startswith('request_') else None
    effect(key,sv('stage',2)+' '+sv('response',response)+' '+(sv('requested_'+request,'yes') if request else '')+' '+bump()+' '+send(2,True))
effect('central_settlement',adj('autonomy',-5)+''' if = { limit = { has_variable = chi_adm_negotiated_integration_pressure } '''+adj('loyalty',-3)+''' }
else_if = { limit = { var:chi_adm_negotiated_integration_honors > 0 } '''+adj('loyalty',3)+''' }
if = { limit = { var:chi_adm_negotiated_integration_honors > 0 exists = ruler } ruler = { remove_modifier = chi_adm_negotiated_integration_honored add_modifier = { name = chi_adm_negotiated_integration_honored years = 10 } }
 c:CHI = {
  remove_modifier = chi_adm_negotiated_integration_honors_patronage
  add_modifier = { name = chi_adm_negotiated_integration_honors_patronage years = 5 }
 } }
change_relations = { country = c:CHI value = 3 } chi_adm_negotiated_integration_clear = yes '''+sv('retry','yes months = 12'))
effect('renew','''if = { limit = { has_variable = chi_adm_negotiated_integration_pressure } set_variable = chi_adm_negotiated_integration_final_offer }
'''+sv('stage',1)+' '+sv('wait',0)+' '+bump()+' '+send(1))
for kind in ('subsidy','protection','honors'):
    effect('offer_'+kind,f'change_variable = {{ name = {P+kind} add = 1 }} '+rm('requested_'+kind)+' chi_adm_negotiated_integration_renew = yes')
effect('pressure',adj('loyalty',-5)+' change_relations = { country = c:CHI value = -10 } '+sv('pressure','yes')+' '+sv('stage',1)+' '+sv('wait',0)+' '+bump()+' '+send(1))
effect('grant_time',sv('stage',10)+' '+sv('wait',3)+' '+bump())
effect('reopen',send(1))
effect('ask_suspend','set_variable = chi_adm_negotiated_integration_suspend_request '+sv('suspend_age',0)+' '+bump()+' '+send(4))
effect('suspend','set_variable = chi_adm_negotiated_integration_paused remove_variable = chi_adm_negotiated_integration_suspend_request chi_adm_negotiated_integration_stop_payments = yes '+bump()+' c:CHI = { chi_adm_negotiated_integration_recount = yes }')
effect('refuse_suspend','remove_variable = chi_adm_negotiated_integration_suspend_request set_variable = chi_adm_negotiated_integration_suspend_refused '+bump()+' '+send(2,True))
effect('force_suspend','''set_variable = chi_adm_negotiated_integration_paused set_variable = chi_adm_negotiated_integration_breach remove_variable = chi_adm_negotiated_integration_suspend_request remove_variable = chi_adm_negotiated_integration_suspend_refused
chi_adm_negotiated_integration_stop_payments = yes c:CHI = { chi_adm_negotiated_integration_recount = yes } '''+bump()+' '+send(5))
effect('resume','remove_variable = chi_adm_negotiated_integration_paused chi_adm_negotiated_integration_apply_subsidy = yes c:CHI = { chi_adm_negotiated_integration_recount = yes } '+bump())
effect('forgive_breach','remove_variable = chi_adm_negotiated_integration_breach '+bump())
effect('withdraw_breach',adj('loyalty',-5)+' change_relations = { country = c:CHI value = -10 } chi_adm_negotiated_integration_close = yes')
effect('revoke_terms',sv('subsidy',0)+' '+sv('protection',0)+' '+sv('honors',0)+' set_variable = chi_adm_negotiated_integration_breach chi_adm_negotiated_integration_stop_payments = yes '+bump()+' '+send(5))
effect('ask_cancel','set_variable = chi_adm_negotiated_integration_cancel_request '+bump()+' '+send(7))
effect('decline_cancel','remove_variable = chi_adm_negotiated_integration_cancel_request '+bump())
for key,fault in [('cancel_mutual',1),('cancel_provincial',2)]:
    penalty=adj('loyalty',-5)+' change_relations = { country = c:CHI value = -10 }' if fault==2 else ''
    effect(key,penalty+''' if = { limit = { has_variable = chi_adm_negotiated_integration_paid_terms }
chi_adm_negotiated_integration_stop_payments = yes remove_variable = chi_adm_negotiated_integration_work remove_variable = chi_adm_negotiated_integration_paused
'''+sv('stage',9)+' '+sv('fault',fault)+' '+bump()+' c:CHI = { chi_adm_negotiated_integration_recount = yes } '+send(2,True)+''' }
else = { chi_adm_negotiated_integration_close = yes }''')
effect('propose_repayment','set_variable = chi_adm_negotiated_integration_repayment_requested '+bump()+' '+send(6))
effect('repay_accept','''if = { limit = { var:chi_adm_negotiated_integration_fault = 2 } '''+sv('repayment_left',12)+''' c:CHI = { create_diplomatic_pact = { country = root type = chi_adm_negotiated_integration_repayment } } }
else = { '''+sv('repayment_left',6)+''' c:CHI = { create_diplomatic_pact = { country = root type = chi_adm_negotiated_integration_repayment_half } } }
remove_variable = chi_adm_negotiated_integration_stage remove_variable = chi_adm_negotiated_integration_repayment_requested '''+sv('retry','yes months = 6')+' '+bump())
effect('repay_compromise','remove_variable = chi_adm_negotiated_integration_repayment_requested set_variable = chi_adm_negotiated_integration_repayment_offer '+bump()+' '+send(2,True))
effect('accept_repay_compromise',sv('repayment_left',6)+''' c:CHI = { create_diplomatic_pact = { country = root type = chi_adm_negotiated_integration_repayment_half } }
remove_variable = chi_adm_negotiated_integration_stage remove_variable = chi_adm_negotiated_integration_repayment_offer '''+sv('retry','yes months = 6')+' '+bump())
effect('repay_refuse','remove_variable = chi_adm_negotiated_integration_repayment_requested set_variable = chi_adm_negotiated_integration_repayment_refused '+bump()+' '+send(2,True))
effect('final_yes','set_variable = chi_adm_negotiated_integration_final_consent chi_adm_negotiated_integration_finish = yes')
effect('final_no',sv('stage',6)+' '+bump()+' '+send(2,True))
effect('hold',sv('stage',5)+' remove_variable = chi_adm_negotiated_integration_final_sent '+bump())
effect('apply_protection','''if = { limit = { var:chi_adm_negotiated_integration_protection > 0 }
every_scope_state = {
if = { limit = { root = { var:chi_adm_negotiated_integration_protection = 2 } }
set_variable = { name = chi_adm_negotiated_integration_tax_left value = 60 } set_variable = { name = chi_adm_negotiated_integration_tax_total value = 60 } set_variable = { name = chi_adm_negotiated_integration_tax_strength value = 2 }
} else = {
set_variable = { name = chi_adm_negotiated_integration_tax_left value = 60 } set_variable = { name = chi_adm_negotiated_integration_tax_total value = 60 } set_variable = { name = chi_adm_negotiated_integration_tax_strength value = 1 }
} chi_adm_negotiated_integration_update_tax = yes } }''')
effect('update_tax','''remove_modifier = chi_adm_negotiated_integration_local_privileges
if = { limit = { var:chi_adm_negotiated_integration_tax_left > 0 } add_modifier = { name = chi_adm_negotiated_integration_local_privileges multiplier = chi_adm_negotiated_integration_tax_scale } }
else = { remove_variable = chi_adm_negotiated_integration_tax_left remove_variable = chi_adm_negotiated_integration_tax_total remove_variable = chi_adm_negotiated_integration_tax_strength }''')
effect('finish','''if = { limit = { chi_adm_negotiated_integration_can_finish = yes }
chi_adm_negotiated_integration_apply_protection = yes
if = { limit = { exists = ruler } ruler = { save_scope_as = chi_adm_negotiated_integration_governor remove_character_role = ruler transfer_character = c:CHI } }
save_scope_as = chi_adm_negotiated_integration_annex_target chi_adm_negotiated_integration_clear = yes chi_adm_memorials_cleanup = yes
c:CHI = { annex = scope:chi_adm_negotiated_integration_annex_target chi_adm_negotiated_integration_recount = yes }
}''')
effect('coerce','''save_scope_as = chi_adm_negotiated_integration_target chi_adm_negotiated_integration_clear = yes '''+sv('retry','yes months = 6')+'''
c:CHI = { every_subject_or_below = { limit = { chi_adm_eligible = yes NOT = { this = scope:chi_adm_negotiated_integration_target } }
if = { limit = { OR = { var:chi_adm_autonomy >= 60 var:chi_adm_loyalty < 40 } } '''+adj('loyalty',-8)+''' change_relations = { country = c:CHI value = -15 } }
else_if = { limit = { var:chi_adm_loyalty >= 80 var:chi_adm_autonomy < 30 } change_relations = { country = c:CHI value = -2 } }
else = { '''+adj('loyalty',-3)+''' change_relations = { country = c:CHI value = -5 } }
} create_diplomatic_play = { type = dp_chi_adm_negotiated_integration_integration target_country = scope:chi_adm_negotiated_integration_target } }''')
effect('province_tick','''if = { limit = { has_variable = chi_adm_negotiated_integration_stage }
if = { limit = { NOT = { chi_adm_negotiated_integration_valid = yes } } chi_adm_negotiated_integration_clear = yes }
else = { chi_adm_negotiated_integration_ensure = yes
if = { limit = { var:chi_adm_negotiated_integration_stage = 1 } change_variable = { name = chi_adm_negotiated_integration_wait add = 1 } }
if = { limit = { var:chi_adm_negotiated_integration_stage = 10 } change_variable = { name = chi_adm_negotiated_integration_wait subtract = 1 }
if = { limit = { var:chi_adm_negotiated_integration_wait <= 0 } '''+sv('stage',1)+' '+sv('wait',0)+' '+bump()+' '+send(1)+''' } }
if = { limit = { has_variable = chi_adm_negotiated_integration_suspend_request } change_variable = { name = chi_adm_negotiated_integration_suspend_age add = 1 } }
if = { limit = { chi_adm_negotiated_integration_active = yes NOT = { has_variable = chi_adm_negotiated_integration_breach } }
change_variable = { name = chi_adm_negotiated_integration_elapsed add = 1 }
if = { limit = { var:chi_adm_negotiated_integration_stage = 3 var:chi_adm_negotiated_integration_elapsed >= chi_adm_negotiated_integration_census_end } '''+sv('stage',4)+''' }
if = { limit = { var:chi_adm_negotiated_integration_elapsed >= chi_adm_negotiated_integration_required }
if = { limit = { is_ai = yes NOT = { has_variable = chi_adm_negotiated_integration_player_agreed } } chi_adm_negotiated_integration_finish = yes }
else_if = { limit = { NOT = { var:chi_adm_negotiated_integration_stage = 6 } NOT = { has_variable = chi_adm_negotiated_integration_final_sent } }
'''+sv('stage',5)+' set_variable = chi_adm_negotiated_integration_final_sent '+bump()+' '+send(3)+''' }
} } } }
if = { limit = { has_variable = chi_adm_negotiated_integration_repayment_left }
if = { limit = { NOT = { chi_adm_negotiated_integration_valid = yes } } chi_adm_negotiated_integration_stop_payments = yes remove_variable = chi_adm_negotiated_integration_repayment_left }
else = { change_variable = { name = chi_adm_negotiated_integration_repayment_left subtract = 1 }
if = { limit = { var:chi_adm_negotiated_integration_repayment_left <= 0 } chi_adm_negotiated_integration_stop_payments = yes remove_variable = chi_adm_negotiated_integration_repayment_left } }
}''')
effect('court_tick','''chi_adm_negotiated_integration_recount = yes
if = { limit = { chi_adm_negotiated_integration_court = yes NOT = { has_journal_entry = chi_adm_negotiated_integration_court } } add_journal_entry = { type = chi_adm_negotiated_integration_court } }
'''+ '\n'.join('c:'+tag+' ?= { chi_adm_negotiated_integration_province_tick = yes }' for tag in core.TAGS)+'\nchi_adm_negotiated_integration_recount = yes')

VALUES='''chi_adm_negotiated_integration_required = { value = 6 c:CHI = { add = { value = var:chi_adm_negotiated_integration_count subtract = 1 min = 0 multiply = 3 } } }
chi_adm_negotiated_integration_census_end = { value = chi_adm_negotiated_integration_required divide = 2 }
chi_adm_negotiated_integration_progress = { value = var:chi_adm_negotiated_integration_elapsed divide = chi_adm_negotiated_integration_required multiply = 100 min = 0 max = 100 }
chi_adm_negotiated_integration_cost_scale = { value = var:chi_adm_negotiated_integration_count min = 0 }
chi_adm_negotiated_integration_tax_scale = { value = var:chi_adm_negotiated_integration_tax_left divide = var:chi_adm_negotiated_integration_tax_total multiply = var:chi_adm_negotiated_integration_tax_strength min = 0 max = 2 }
'''
weights={
'begin':'''base = 20 modifier = { trigger = { var:chi_adm_loyalty >= 70 } factor = 3 } modifier = { trigger = { var:chi_adm_loyalty < 40 } factor = 0.2 }
modifier = { trigger = { var:chi_adm_autonomy >= 60 } factor = 0.25 } modifier = { trigger = { var:chi_adm_autonomy <= 25 } factor = 2 }
modifier = { trigger = { var:chi_adm_corruption >= 60 } factor = 0.3 } modifier = { trigger = { var:chi_adm_corruption < 20 } factor = 1.5 }
modifier = { trigger = { relations:c:CHI >= 50 } factor = 2 } modifier = { trigger = { relations:c:CHI < 0 } factor = 0.25 }
modifier = { trigger = { c:CHI = { has_modifier = chi_mandate_consolidated_authority } } factor = 2 }
modifier = { trigger = { var:chi_adm_negotiated_integration_subsidy > 0 } factor = 2 } modifier = { trigger = { var:chi_adm_negotiated_integration_protection > 0 } factor = 2 }
modifier = { trigger = { var:chi_adm_negotiated_integration_honors > 0 } factor = 1.5 } modifier = { trigger = { chi_adm_frontier = yes var:chi_adm_negotiated_integration_protection = 0 } factor = 0.25 }''',
'centralize':'''base = 20 modifier = { trigger = { var:chi_adm_autonomy >= 50 } factor = 2 } modifier = { trigger = { chi_adm_frontier = yes } factor = 2 }''',
'refuse':'''base = 8 modifier = { trigger = { var:chi_adm_loyalty < 40 } factor = 4 } modifier = { trigger = { var:chi_adm_autonomy >= 60 } factor = 3 } modifier = { trigger = { var:chi_adm_corruption >= 60 } factor = 2 } modifier = { trigger = { relations:c:CHI < 0 } factor = 3 }'''
}
# key -> (player-facing name, effect summary, actual eligibility)
A={}
def action(key,name,desc,condition):A[key]=(name,desc,condition)
action('propose','Propose Direct Administration','Open event negotiations. No annexation, resource commitment or subsidy begins until the province agrees.',T[P+'can_propose'])
action('begin','Accept Full Integration','Begin census and registration. Qing commits @aut![Nbsp]#v 10%#! [concept_authority] and @bur![Nbsp]#v 10%#! [concept_bureaucracy] per active commission. Agreed subsidies begin automatically.',T[P+'can_begin'])
action('centralize','Offer Closer Centralization','Offer cooperation without annexation: -5 [concept_chi_adm_autonomy] if Qing agrees. Another peaceful proposal must wait one year.',T[P+'reply'])
action('request_subsidy','Request Financial Support','Ask for automatic weekly support: 10% of provincial income, or 20% under stronger terms, during active implementation.',T[P+'reply'])
action('request_protection','Request Fiscal Privileges','Ask to preserve local tax privileges after annexation: -10% Tax Collection fading over five years, or -20% over ten. Frontier laws remain unchanged during negotiations.',T[P+'reply'])
action('request_honors','Request Imperial Recognition','Ask for the governor to receive +10 Popularity and +10 Prominence for ten years, +3 provincial Loyalty and +5 relations on agreement.',T[P+'reply'])
action('refuse','Decline Annexation','Decline this offer. Qing may negotiate, use its single pressure attempt, withdraw or escalate.',T[P+'reply'])
action('delay','Request More Time','Ask for three further monthly reviews before responding.',T[P+'reply'])
action('central_settlement','Accept Closer Centralization','Agree to -5 provincial Autonomy without annexation. Loyalty changes by -3 after pressure, or +3 if imperial honors were offered; the governor receives those honors. Relations improve by 3. No annexation subsidy or post-annexation privilege begins. Another proposal must wait one year.',T[P+'court_reply']+' var:chi_adm_negotiated_integration_response = 2')
for kind,name,desc in [
('subsidy','Offer Greater Financial Support','Raise the proposed automatic weekly subsidy from none to 10%, or from 10% to 20%, of provincial income. It starts only after agreement and stops on suspension, annexation or cancellation.'),
('protection','Offer Greater Fiscal Protection','Raise promised fiscal privileges from none to -10% Tax Collection for five years, or to -20% for ten years. They begin after annexation and decay monthly.'),
('honors','Offer Imperial Honors','Offer +10 governor Popularity and Prominence for ten years, +3 Loyalty and +5 relations on agreement.')]:
    action('offer_'+kind,name,desc,T[P+'court_reply']+' var:chi_adm_negotiated_integration_'+kind+' < '+str(1 if kind=='honors' else 2))
action('pressure','Press the Imperial Claim','One attempt only: Loyalty -5 and relations -10. The governor still decides. After another refusal one improved offer remains; further refusal permits only withdrawal or coercion.',T[P+'court_reply']+' NOT = { has_variable = chi_adm_negotiated_integration_pressure }')
action('grant_time','Grant Three Months','Give the provincial council three monthly reviews. Negotiation occupies no integration slot.',T[P+'court_reply']+' var:chi_adm_negotiated_integration_response = 5')
action('close','Withdraw the Proposal','End negotiations without annexation. Another proposal must wait six months. During implementation use cancellation by agreement instead.',T[P+'valid']+' OR = { var:chi_adm_negotiated_integration_stage = 1 var:chi_adm_negotiated_integration_stage = 2 var:chi_adm_negotiated_integration_stage = 9 var:chi_adm_negotiated_integration_stage = 10 }')
action('ask_suspend','Request Agreed Suspension','Ask to pause work. Agreed suspension preserves elapsed time, releases [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] resources, stops subsidies and no longer slows other integrations.',T[P+'valid']+' '+T[P+'active']+' var:chi_adm_negotiated_integration_stage < 5 NOT = { has_variable = chi_adm_negotiated_integration_suspend_request }')
action('suspend','Agree to Suspension','Pause work and subsidies, release [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] resources and preserve elapsed time.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_suspend_request')
action('refuse_suspend','Decline Suspension','Insist on the agreement. Qing may continue or suspend unilaterally in breach.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_suspend_request')
action('force_suspend','Suspend Despite Objections','Pause work and payments despite the governor. This breaches Qing\'s agreement; consent may be withdrawn without repayment.',T[P+'valid']+' '+T[P+'active']+' OR = { has_variable = chi_adm_negotiated_integration_suspend_refused AND = { has_variable = chi_adm_negotiated_integration_suspend_request var:chi_adm_negotiated_integration_suspend_age >= 6 } }')
action('resume','Resume Implementation','Restore agreed subsidies and the @aut! #r −10%#! [concept_authority] and @bur! #r −10%#! [concept_bureaucracy] commitment. Preserve elapsed time; this project again increases the shared duration.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_paused NOT = { has_variable = chi_adm_negotiated_integration_breach } '+T[P+'resources'])
action('revoke_terms','Revoke the Agreed Concessions','Deliberately revoke the promised concessions. The governor may withdraw consent; Qing has no repayment claim.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_work NOT = { has_variable = chi_adm_negotiated_integration_breach }')
action('forgive_breach','Maintain Consent Despite the Breach','Waive the breach and preserve agreement. Suspended work stays paused until Qing resumes it.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_breach')
action('withdraw_breach','Withdraw Consent','Withdraw because Qing broke its terms. End integration; Loyalty -5 and relations -10. Qing has no repayment claim.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_breach')
action('ask_cancel','Propose Mutual Cancellation','Ask to end the agreement. Past assistance may then be discussed in a partial repayment settlement.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_work NOT = { has_variable = chi_adm_negotiated_integration_cancel_request }')
action('cancel_mutual','Agree to Cancellation','End integration and future subsidies. Qing may seek a negotiated partial repayment if financial support was agreed.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_cancel_request')
action('decline_cancel','Maintain the Agreement','Decline mutual cancellation. The existing terms continue.',T[P+'valid']+' has_variable = chi_adm_negotiated_integration_cancel_request')
action('final_yes','Confirm Peaceful Annexation','Explicitly authorize immediate annexation now that implementation is complete. Your country ceases to exist. The governor joins Qing without a guaranteed office.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 5 '+T[P+'active']+' NOT = { has_variable = chi_adm_negotiated_integration_breach } var:chi_adm_negotiated_integration_elapsed >= chi_adm_negotiated_integration_required')
action('final_no','Withhold Final Confirmation','Keep your country intact. Qing may hold the process open or declare provincial breach and seek repayment or coercion.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 5')
action('hold','Keep the Completed Process Open','Allow another final confirmation. Silence never authorizes peaceful annexation.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 6')
action('cancel_provincial','Declare Provincial Breach','Cancel after final confirmation was refused. Loyalty -5 and relations -10. Agreed financial assistance permits a repayment request, decided through events.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 6')
action('propose_repayment','Negotiate Repayment','Seek temporary automatic payments to Qing: 10% of provincial income for twelve months after provincial breach, or 5% for six months after mutual cancellation. The province must agree.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 9 NOT = { has_variable = chi_adm_negotiated_integration_repayment_requested } NOT = { has_variable = chi_adm_negotiated_integration_repayment_offer }')
action('repay_accept','Accept the Repayment Terms','Begin the proposed temporary automatic payment to Qing. No one-time treasury transfer or permanent tax is created.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 9 has_variable = chi_adm_negotiated_integration_repayment_requested')
action('repay_compromise','Offer Partial Repayment','Offer 5% of provincial income for six months. Qing must approve this compromise.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 9 has_variable = chi_adm_negotiated_integration_repayment_requested')
action('repay_refuse','Refuse Repayment','Reject repayment. Qing may forgive the claim or escalate through a diplomatic play.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 9 has_variable = chi_adm_negotiated_integration_repayment_requested')
action('accept_repay_compromise','Accept Partial Repayment','Accept automatic payments of 5% of provincial income for six months as settlement.',T[P+'valid']+' var:chi_adm_negotiated_integration_stage = 9 has_variable = chi_adm_negotiated_integration_repayment_offer')
action('coerce','Enforce the Claim by Diplomatic Play','Launch a contested annexation play at 25% of normal annexation Infamy. Victory annexes immediately. Resistant administrations lose 8 Loyalty/15 relations, ordinary offices 3 Loyalty/5 relations; loyal centralized offices lose only 2 relations.',T[P+'coercible'])
action('reopen','Review the Provincial Proposal','Reopen the decision event without changing terms or inferring consent.',T[P+'reply'])
PROVINCE={'begin','centralize','request_subsidy','request_protection','request_honors','refuse','delay','suspend','refuse_suspend','forgive_breach','withdraw_breach','final_yes','final_no','repay_accept','repay_compromise','repay_refuse','cancel_mutual','decline_cancel','reopen'}
COURT=set(A)-PROVINCE
for key,(name,desc,cond) in A.items():
    E[P+key]='if = { limit = { '+cond+' } '+E[P+key]+' }'
    loc(key,name);loc(key+'_desc',desc)
    yes=loc(key+'_ready','@green_checkmark![Nbsp]Requirements met.')
    reason={'propose':'Requires a direct [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] administration, no open case or cooldown, Liberty Desire at most 25, Central Archives, Mandate centralization, peace and no committed diplomatic plays. Qing needs nonnegative Authority and Bureaucracy.',
    'begin':'Requires an open offer and nonnegative current [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] Authority and Bureaucracy. The new commitment may create a deficit.',
    'resume':'Requires agreed suspension, no unresolved [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] breach and nonnegative current [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] Authority and Bureaucracy.',
    'coerce':'Requires refused annexation, six unanswered reviews, withheld final confirmation or a repayment dispute. Both countries must be at peace and clear of committed plays.'}.get(key,'Requires the matching open stage, an unused response or concession, and continued [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] administrative service. Current stage and terms appear above.')
    no=loc(key+'_blocked','@red_cross![Nbsp]'+reason)
    if key == 'propose':
        loc('propose_requirements_heading','Requirements:')
        requirements=[
            ('chi_adm_negotiated_integration_req_admin','chi_adm_eligible = yes'),
            ('chi_adm_negotiated_integration_req_central','c:CHI = { has_variable = chi_qing_centralisation_unlocked }'),
            ('chi_adm_negotiated_integration_req_case','NOT = { has_variable = chi_adm_negotiated_integration_stage } NOT = { has_variable = chi_adm_negotiated_integration_retry } NOT = { has_variable = chi_adm_negotiated_integration_repayment_left }')]
        lines=[]
        for req,trigger in requirements:
            loc(req.removeprefix('chi_adm_negotiated_integration_'), {
                'chi_adm_negotiated_integration_req_admin':'@green_checkmark! The administration is a direct [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] subject.',
                'chi_adm_negotiated_integration_req_central':'@green_checkmark! [ROOT.GetCountry.GetOverlord.GetName] has at least #v 6#! Mandate centralization, or Consolidated Imperial Authority.',
                'chi_adm_negotiated_integration_req_case':'@green_checkmark! No proposal, retry period or repayment case is active.'}[req])
            lines.append(f'''if = {{ limit = {{ {trigger} }} custom_tooltip_no_bullet = {req} }} else = {{ custom_tooltip_no_bullet = {req}_no }}''')
            loc(req.removeprefix('chi_adm_negotiated_integration_')+'_no', {
                'chi_adm_negotiated_integration_req_admin':'@red_cross! The administration is not a direct [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] subject.',
                'chi_adm_negotiated_integration_req_central':'@red_cross! [ROOT.GetCountry.GetOverlord.GetName] needs at least #v 6#! Mandate centralization, or Consolidated Imperial Authority.',
                'chi_adm_negotiated_integration_req_case':'@red_cross! A proposal, retry period or repayment case is already active.'}[req])
        requirement_tooltip='show_as_tooltip = { custom_tooltip_no_bullet = chi_adm_negotiated_integration_propose_requirements_heading '+ ' '.join(lines) +' }'
        G[P+key]=f'''scope = country is_valid = {{ {cond} }} effect = {{ custom_tooltip = {P+key}_desc
{requirement_tooltip}
hidden_effect = {{ {P+key} = yes }} }}'''
    else:
        G[P+key]=f'''scope = country is_valid = {{ {cond} }} effect = {{ custom_tooltip = {P+key}_desc
show_as_tooltip = {{ if = {{ limit = {{ {cond} }} custom_tooltip_no_bullet = {yes} }} else = {{ custom_tooltip_no_bullet = {no} }} }}
hidden_effect = {{ {P+key} = yes }} }}'''

# Private terminal cleanup must not inherit the narrower public Withdraw button gate.
effect('end','chi_adm_negotiated_integration_clear = yes '+sv('retry','yes months = 6'))
effect('orphan_cleanup','chi_adm_negotiated_integration_clear = yes remove_variable = chi_adm_negotiated_integration_repayment_left')
for key in E:E[key]=E[key].replace('chi_adm_negotiated_integration_close = yes','chi_adm_negotiated_integration_end = yes')
# Proactive offers are permitted before a reply as well as in response to one.
for kind in ('subsidy','protection','honors'):
    key='offer_'+kind
    old=T[P+'court_reply']
    new=T[P+'valid']+' OR = { var:chi_adm_negotiated_integration_stage = 1 var:chi_adm_negotiated_integration_stage = 2 }'
    name,desc,cond=A[key];A[key]=(name,desc,cond.replace(old,new))
    E[P+key]=E[P+key].replace(old,new)
    G[P+key]=G[P+key].replace(old,new)
# A new concurrent project may move a ready province back below the completion threshold.
E[P+'province_tick']=E[P+'province_tick'].replace('change_variable = { name = chi_adm_negotiated_integration_elapsed add = 1 }','''change_variable = { name = chi_adm_negotiated_integration_elapsed add = 1 }
if = { limit = { var:chi_adm_negotiated_integration_stage = 5 var:chi_adm_negotiated_integration_elapsed < chi_adm_negotiated_integration_required }
set_variable = { name = chi_adm_negotiated_integration_stage value = 4 } remove_variable = chi_adm_negotiated_integration_final_sent '''+bump()+' }')
# Work advances on calendar-month events from acceptance/resumption, not the
# next first-of-month pulse. Separate clock generations reject old paused timers.
source=E[P+'province_tick']
start=source.index('if = { limit = { chi_adm_negotiated_integration_active = yes')
i=source.index('{',start)+1;depth=1
while depth:
    if source[i]=='{':depth+=1
    elif source[i]=='}':depth-=1
    i+=1
effect('work_tick',source[start:i])
E[P+'province_tick']=source[:start]+source[i:]
effect('schedule_work','''if = { limit = { NOT = { has_variable = chi_adm_negotiated_integration_clock } } set_variable = { name = chi_adm_negotiated_integration_clock value = 0 } }
change_variable = { name = chi_adm_negotiated_integration_clock add = 1 }
save_scope_value_as = { name = chi_adm_negotiated_integration_clock_revision value = var:chi_adm_negotiated_integration_clock }
trigger_event = { id = chi_adm_negotiated_integration.8 months = 1 popup = no }''')
for key in ('begin','resume'):
    # Insert inside the public eligibility guard, after all state is established.
    body=E[P+key];pos=body.rfind('}')
    E[P+key]=body[:pos]+' chi_adm_negotiated_integration_schedule_work = yes '+body[pos:]
E[P+'finish']=E[P+'finish'].replace('chi_adm_memorials_cleanup = yes','chi_adm_memorials_cleanup = yes chi_adm_imperial_law_clear = yes')
E[P+'apply_protection']=E[P+'apply_protection'].replace('chi_adm_negotiated_integration_update_tax = yes','chi_adm_negotiated_integration_update_tax = yes set_variable = { name = chi_adm_negotiated_integration_tax_new value = yes days = 1 }')
E[P+'update_tax']=E[P+'update_tax'].replace('remove_variable = chi_adm_negotiated_integration_tax_strength','remove_variable = chi_adm_negotiated_integration_tax_strength remove_variable = chi_adm_negotiated_integration_tax_new')
E[P+'revoke_terms']=E[P+'revoke_terms'].replace('set_variable = { name = chi_adm_negotiated_integration_honors value = 0 }','set_variable = { name = chi_adm_negotiated_integration_honors value = 0 } if = { limit = { exists = ruler } ruler = { remove_modifier = chi_adm_negotiated_integration_honored } }')
# Native effect previews show the actual modifier contents without applying them.
preview='show_as_tooltip = { c:CHI = { add_modifier = { name = chi_adm_negotiated_integration_commitment } } } '
G[P+'begin']=G[P+'begin'].replace('hidden_effect = {',preview+'hidden_effect = {',1)
G[P+'offer_honors']=G[P+'offer_honors'].replace('hidden_effect = {','show_as_tooltip = { ruler ?= { add_modifier = { name = chi_adm_negotiated_integration_honored years = 10 } } } hidden_effect = {',1)


EVENTS=['namespace = chi_adm_negotiated_integration']
def option(key,court=False,ai='base = 10'):
    cond=A[key][2]
    guard='chi_adm_negotiated_integration_event_current = yes '+('scope:chi_adm_negotiated_integration_target = { '+cond+' }' if court else cond)
    fx=('scope:chi_adm_negotiated_integration_target = { '+P+key+' = yes }') if court else P+key+' = yes'
    return f'option = {{ name = {P+key} trigger = {{ {guard} }} custom_tooltip = {P+key}_desc hidden_effect = {{ {fx} }} ai_chance = {{ {ai} }} }}'
def event(n,title,desc,flavor,options):
    for suffix,text in [('t',title),('d',desc),('f',flavor)]:loc(f'event_{n}_{suffix}',text)
    EVENTS.append(f'''chi_adm_negotiated_integration.{n} = {{ type = country_event placement = ROOT title = chi_adm_negotiated_integration_event_{n}_t desc = chi_adm_negotiated_integration_event_{n}_d flavor = chi_adm_negotiated_integration_event_{n}_f
event_image = {{ video = "ep1_persian_court" }} icon = "gfx/interface/icons/event_icons/event_scales.dds" duration = 30
trigger = {{ chi_adm_negotiated_integration_event_current = yes }} cancellation_trigger = {{ NOT = {{ chi_adm_negotiated_integration_event_current = yes }} }}
{options}
option = {{ name = chi_adm_negotiated_integration_read_later default_option = yes ai_chance = {{ base = 0 }} }} }}''')
loc('read_later','Leave the papers open')
# Relative national strength in provincial negotiations.
weights['begin'] = weights.get('begin', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 0.8\n}'
weights['centralize'] = weights.get('centralize', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 1.25\n}'
weights['request_subsidy'] = weights.get('request_subsidy', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 1.25\n}'
weights['request_protection'] = weights.get('request_protection', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 1.25\n}'
weights['request_honors'] = weights.get('request_honors', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 1.25\n}'
weights['delay'] = weights.get('delay', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 1.25\n}'
weights['refuse'] = weights.get('refuse', 'base = 8') + '\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige < { value = c:CHI.prestige multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { prestige > 0 }\n        prestige >= { value = c:CHI.prestige multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection < { value = c:CHI.army_power_projection multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { army_power_projection > 0 }\n        army_power_projection >= { value = c:CHI.army_power_projection multiply = 1 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp < { value = c:CHI.gdp multiply = 0.1 }\n    }\n    factor = 0.8\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 0.5 }\n    }\n    factor = 1.25\n}\nmodifier = {\n    trigger = {\n        c:CHI = { gdp > 0 }\n        gdp >= { value = c:CHI.gdp multiply = 1 }\n    }\n    factor = 1.25\n}'
event(1,'A Province Before the Throne','The court proposes direct administration of [ROOT.GetCountry.GetName]. Acceptance begins census and registration. The governor may request concessions, offer closer centralization or refuse. Existing provincial laws and frontier customs remain intact until annexation.','The imperial seal rests beside the provincial registers. Neither seal alone settles the terms.', '\n'.join(option(k,ai=weights.get(k,'base = 8')) for k in ('begin','centralize','request_subsidy','request_protection','request_honors','delay','refuse')))
event(2,'Memorial on Direct Administration',"[SCOPE.sCountry('chi_adm_negotiated_integration_target').GetName] has answered the court. Review its response and existing terms in Administrative Integration. Concessions are offered individually; silence grants no consent.",'The Grand Council reads the governor\'s memorial before advising the throne.', '\n'.join(option(k,True,ai='base = '+str({'central_settlement':40,'offer_subsidy':20,'offer_protection':25,'offer_honors':20,'pressure':8,'coerce':2,'close':5,'hold':10}.get(k,10))) for k in ('central_settlement','offer_subsidy','offer_protection','offer_honors','pressure','grant_time','close','force_suspend','hold','cancel_provincial','propose_repayment','accept_repay_compromise','coerce')))
event(3,'The Final Provincial Seal','Census and transition are complete. Confirming now explicitly authorizes peaceful annexation of your country by Qing. Withholding confirmation preserves your country; Qing may keep talks open or declare breach.','The last register awaits the governor\'s seal.',option('final_yes',ai='base = 100')+'\n'+option('final_no',ai='base = 0'))
event(4,'A Pause in the Registers','Qing requests suspension. Agreement preserves elapsed time, stops subsidies and releases administrative resources. Refusal leaves Qing free to continue or suspend in breach.','The commissioners ask whether their desks may be closed for a season.',option('suspend',ai='base = 40')+'\n'+option('refuse_suspend',ai='base = 10'))
event(5,'The Court Has Broken Its Terms','Qing revoked agreed concessions or suspended work without agreement. Maintain consent or withdraw without a repayment claim against you.','A promise beneath the imperial seal remains a promise.',option('forgive_breach',ai=weights['begin'])+'\n'+option('withdraw_breach',ai=weights['refuse']))
event(6,'Accounts After Cancellation','Qing seeks temporary automatic repayment. Provincial breach permits 10% of provincial income for twelve months; mutual cancellation permits 5% for six months. Accept, counter with partial repayment or refuse. No payment starts without agreement.','The accounts record assistance; the two seals decide its settlement.', '\n'.join(option(k,ai='base = '+str(w)) for k,w in [('repay_accept',30),('repay_compromise',30),('repay_refuse',15)]))
event(7,'Shall the Commission Be Recalled?','Qing proposes ending integration by agreement. Acceptance ends work and future subsidies. Past assistance may be discussed in a partial repayment settlement. Declining keeps the agreement in force.','The commissioners await instructions before packing their registers.',option('cancel_mutual',ai='base = 30')+'\n'+option('decline_cancel',ai='base = 20'))
EVENTS.append('''chi_adm_negotiated_integration.8 = { type = country_event hidden = yes
trigger = { chi_adm_negotiated_integration_valid = yes chi_adm_negotiated_integration_active = yes var:chi_adm_negotiated_integration_clock = scope:chi_adm_negotiated_integration_clock_revision }
immediate = { c:CHI = { chi_adm_negotiated_integration_recount = yes } chi_adm_negotiated_integration_work_tick = yes
if = { limit = { chi_adm_negotiated_integration_valid = yes chi_adm_negotiated_integration_active = yes }
trigger_event = { id = chi_adm_negotiated_integration.8 months = 1 popup = no } }
} }''')

PACT=[]
for key,rate,receives in [('subsidy',.10,'yes'),('subsidy_strong',.20,'yes'),('repayment',.10,'no'),('repayment_half',.05,'no')]:
    loc(key,{'subsidy':'Provincial Integration Subsidy','subsidy_strong':'Enhanced Integration Subsidy','repayment':'Integration Repayment','repayment_half':'Negotiated Partial Repayment'}[key])
    description=(f'Automatic weekly assistance from Qing, equal to {rate:.0%} of provincial income, during active agreed integration.' if receives=='yes' else f'An agreed temporary automatic payment to Qing, equal to {rate:.0%} of provincial income.')
    loc(key+'_desc',description);loc(key+'_pact_desc',description)
    loc(key+'_action_name',LOC[P+key]);loc(key+'_action_break_name','End '+LOC[P+key])
    PACT.append(f'''chi_adm_negotiated_integration_{key} = {{ groups = {{ general }} requires_approval = no should_notify_third_parties = no show_in_lens = no can_select_to_break = no selectable = {{ always = no }}
pact = {{ is_two_sided_pact = no income_transfer = {rate:.2f} {'max_paying_country_income_to_transfer = 1.0' if receives == 'yes' else ''} second_country_gets_income_transfer = {receives} income_transfer_based_on_second_country = yes }} }}''')
MODS='''chi_adm_negotiated_integration_commitment = { icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds country_authority_mult = -0.10 country_bureaucracy_mult = -0.10 }
chi_adm_negotiated_integration_honored = { icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds character_popularity_add = 10 character_prominence_add = 10 }
chi_adm_negotiated_integration_local_privileges = { icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_negative.dds state_tax_collection_mult = -0.10 }
'''
for key,name,desc in [('commitment','Administrative Integration Commissions','Each active commission commits court Authority and Bureaucracy. Suspended commissions release their commitments.'),('honored','Recognition by the Dragon Throne','The court recognizes the governor\'s service and standing.'),('local_privileges','Negotiated Provincial Tax Privileges','Local fiscal privileges survive negotiated annexation and diminish each month until the agreed term expires.')]:
    loc(key,name);loc(key+'_desc',desc)
WG=(GAME/'common/war_goal_types/00_annex_country.txt').read_text('utf-8-sig').replace('annex_country = {','chi_adm_negotiated_integration_annexation = {',1)
start=WG.index('infamy = {');i=WG.index('{',start)+1;depth=1
while depth:
    if WG[i]=='{':depth+=1
    elif WG[i]=='}':depth-=1
    i+=1
WG=WG[:i-1]+'\n\t\tmultiply = 0.25\n\t'+WG[i-1:]
for key,value in [('annexation','Enforce Direct Administration'),('annexation_desc','Annex the administration through a contested settlement at one quarter of normal annexation Infamy.'),('annexation_action_name','Enforce Direct Administration'),('annexation_action_name_desc','Demand the administration\'s annexation into Qing.')]:loc(key,value)
PLAY='''dp_chi_adm_negotiated_integration_integration = { war_goal = chi_adm_negotiated_integration_annexation texture = "gfx/interface/icons/war_goals/annex_country.dds" blocked_by_diplomatic_status = no add_infamy_for_starting_initiator_wargoals = yes selectable_in_lens = { always = no }
possible = { c:CHI ?= this chi_adm_court_valid = yes scope:target_country = { chi_adm_eligible = yes } }
ai_acceptance_max = 75 on_weekly_pulse = {} on_war_begins = {} on_war_end = {} }
'''
ENTRIES=[]
for side,cond in [('court','chi_adm_negotiated_integration_court = yes'),('province','chi_adm_negotiated_integration_valid = yes has_variable = chi_adm_negotiated_integration_stage')]:
    loc(side,'Administrative Integration' if side=='court' else 'The Provincial Integration Commission')
    loc(side+'_reason','Negotiate the terms of direct administration, review provincial seals and follow census and transition. No proposal alone changes laws or authorizes annexation.')
    loc(side+'_closed','This administrative register has closed.')
    ENTRIES.append(f'''chi_adm_negotiated_integration_{side} = {{ icon = "gfx/interface/icons/event_icons/event_scales.dds" group = je_group_chi_adm_court_register_{'court' if side=='court' else 'province'} context = country transferable = no can_revolution_inherit = no
is_shown_when_inactive = {{ {cond} }} possible = {{ {cond} }}
widget = {{ gui = "gui/journal_entry_widgets/chi_adm_negotiated_integration.gui" name = "chi_adm_negotiated_integration_{side}" container = "custom_widget_container_1" }}
'''+('scaling_modifiers_while_active = { modifier = chi_adm_negotiated_integration_commitment value = chi_adm_negotiated_integration_cost_scale }' if side=='court' else '')+f'''
outcome = {{ flags = {{ hidden invalid_outcome }} conclusion_desc = chi_adm_negotiated_integration_{side}_closed trigger = {{ NOT = {{ {cond} }} }} }} }}''')
loc('proposal_gate','Requires an eligible direct [ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag] administration, Liberty Desire at most 25, Central Archives, unlocked Mandate centralization and no pending case or cooldown. Qing needs nonnegative Authority and Bureaucracy. Both countries must be at peace and outside committed diplomatic plays.')

def text(key):return f'textbox = {{ size = {{ 440 0 }} max_width = 440 autoresize = yes multiline = yes text = "{P+key}" }}'
def button(key,visible=None):
    visibility=visible or "GetScriptedGui('"+P+key+"').IsValid(GuiScope.SetRoot(Country.MakeScope).End)"
    return f'''button = {{ visible = "[{visibility}]" size = {{ 440 54 }} using = default_button_action
enabled = "[GetScriptedGui('{P+key}').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
onclick = "[GetScriptedGui('{P+key}').Execute(GuiScope.SetRoot(Country.MakeScope).End)]"
tooltip = "[GetScriptedGui('{P+key}').ExecuteTooltip(GuiScope.SetRoot(Country.MakeScope).End)]"
textbox = {{ size = {{ 416 0 }} max_width = 416 autoresize = yes multiline = yes parentanchor = center align = center|nobaseline text = "{P+key}" alwaystransparent = yes }} }}'''
G[P+'row']='scope = country is_valid = { chi_adm_eligible = yes }'
G[P+'progress_visible']='scope = country is_valid = { has_variable = chi_adm_negotiated_integration_work }'
G[P+'show_begin']='scope = country is_valid = { chi_adm_negotiated_integration_reply = yes }'
G[P+'show_resume']='scope = country is_valid = { chi_adm_negotiated_integration_valid = yes has_variable = chi_adm_negotiated_integration_paused NOT = { has_variable = chi_adm_negotiated_integration_breach } }'
loc('overview','Each active commission costs @aut![Nbsp]#v 10%#! [concept_authority] and @bur![Nbsp]#v 10%#! [concept_bureaucracy]. Six months plus three per additional active commission. Negotiations and agreed suspensions do not count; elapsed time is preserved.')
loc('accounts',"@chi_adm_loyalty![Nbsp][concept_chi_adm_loyalty]: #v [Country.MakeScope.Var('chi_adm_loyalty').GetValue|0]#!    @chi_adm_autonomy![Nbsp][concept_chi_adm_autonomy]: #v [Country.MakeScope.Var('chi_adm_autonomy').GetValue|0]#!    @chi_adm_corruption![Nbsp][concept_chi_adm_corruption]: #v [Country.MakeScope.Var('chi_adm_corruption').GetValue|0]#!")
loc('stage_display',"#bold [Country.GetCustom('chi_adm_negotiated_integration_stage')]#!\n[Country.GetCustom('chi_adm_negotiated_integration_response')]\n[Country.GetCustom('chi_adm_negotiated_integration_activity')]")
loc('progress_display',"Elapsed implementation: #v [Country.MakeScope.Var('chi_adm_negotiated_integration_elapsed').GetValue|0]#! / #v [Country.MakeScope.ScriptValue('chi_adm_negotiated_integration_required')|0]#! required monthly reviews.\nCensus ends at half the required duration; transition follows. New or completed commissions change the total without erasing elapsed time.")
loc('terms_display',"#bold Agreed or offered terms#!\n[Country.GetCustom('chi_adm_negotiated_integration_subsidy')]\n[Country.GetCustom('chi_adm_negotiated_integration_protection')]\n[Country.GetCustom('chi_adm_negotiated_integration_honors')]")
loc('waiting_display',"[Country.GetCustom('chi_adm_negotiated_integration_waiting')]\n[Country.GetCustom('chi_adm_negotiated_integration_requests')]")
loc('negotiation_help','@chi_adm_loyalty! [concept_chi_adm_loyalty], @chi_adm_autonomy! [concept_chi_adm_autonomy], @chi_adm_corruption! [concept_chi_adm_corruption], [concept_relations] and offered concessions influence negotiations. One pressure attempt is permitted, then one improved offer. Further refusal leaves withdrawal or coercion. Unanswered human proposals grant no consent; Qing may escalate after six monthly reviews.')
loc('ledger_display',"#bold Integration#! [Country.GetCustom('chi_adm_negotiated_integration_stage')]")
BAR='''progressbar = { size = { 440 18 } min = 0 max = 100 value = "[FixedPointToFloat(Country.MakeScope.ScriptValue('chi_adm_negotiated_integration_progress'))]" progresstexture = "gfx/interface/progressbar/progressbar_gold.dds" noprogresstexture = "gfx/interface/progressbar/progressbar_empty.dds" direction = horizontal skip_initial_animation = yes tooltip = "chi_adm_negotiated_integration_overview" }'''
progress='flowcontainer = { direction = vertical spacing = 6 visible = "[GetScriptedGui(\'chi_adm_negotiated_integration_progress_visible\').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]" '+text('progress_display')+BAR+' }'
# Reuse memorials and audits's proven compact live L/A/C strip instead of squeezing three concepts into a line.
source=(ROOT/'gui/journal_entry_widgets/chi_adm_memorials.gui').read_text('utf-8')
match=re.search(r'widget = \{ size = \{ 440 66 \}',source);assert match
i=source.index('{',match.start())+1;depth=1
while depth:
    if source[i]=='{':depth+=1
    elif source[i]=='}':depth-=1
    i+=1
accounts=source[match.start():i]
card=accounts+text('stage_display')+text('terms_display')+text('waiting_display')+progress
court='''flowcontainer = { name = "chi_adm_negotiated_integration_court" direction = vertical spacing = 10 parentanchor = hcenter ignoreinvisible = yes
'''+text('overview')+text('negotiation_help')+'''flowcontainer = { direction = vertical spacing = 8 ignoreinvisible = yes datamodel = "[AccessPlayer.GetSubjects]" item = {
flowcontainer = { direction = vertical spacing = 8 ignoreinvisible = yes visible = "[GetScriptedGui('chi_adm_negotiated_integration_row').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
section_header_button = { blockoverride "layout" { size = { 472 38 } } blockoverride "left_text" { text = "[Country.GetNameNoFormatting]" }
blockoverride "onclick" { onclick = "[GetVariableSystem.Toggle(Concatenate('chi_adm_negotiated_integration_', Country.GetNameNoFormatting))]" }
blockoverride "onclick_showmore" { visible = "[Not(GetVariableSystem.Exists(Concatenate('chi_adm_negotiated_integration_', Country.GetNameNoFormatting)))]" }
blockoverride "onclick_showless" { visible = "[GetVariableSystem.Exists(Concatenate('chi_adm_negotiated_integration_', Country.GetNameNoFormatting))]" } }
flowcontainer = { direction = vertical spacing = 8 margin = { 16 12 } ignoreinvisible = yes visible = "[GetVariableSystem.Exists(Concatenate('chi_adm_negotiated_integration_', Country.GetNameNoFormatting))]"
'''+card+'\n'.join(button(k,"GetScriptedGui('chi_adm_negotiated_integration_"+('row' if k=='propose' else 'show_resume')+"').IsValid(GuiScope.SetRoot(Country.MakeScope).End)" if k in ('propose','resume') else None) for k in sorted(COURT))+' } } } } }'
province='''flowcontainer = { name = "chi_adm_negotiated_integration_province" direction = vertical spacing = 10 parentanchor = hcenter ignoreinvisible = yes datacontext = "[JournalEntry.GetCountry]"
'''+card+text('negotiation_help')+'\n'.join(button(k,"GetScriptedGui('chi_adm_negotiated_integration_show_begin').IsValid(GuiScope.SetRoot(Country.MakeScope).End)" if k=='begin' else None) for k in sorted(PROVINCE))+' }'
CUSTOM=[]
def custom(key,options,fallback):
    parts=[]
    for i,(condition,label) in enumerate(options):
        name=loc(key+'_'+str(i),label);parts.append(f'text = {{ trigger = {{ {condition} }} localization_key = {name} }}')
    name=loc(key+'_default',fallback);parts.append(f'text = {{ trigger = {{ always = yes }} localization_key = {name} }}')
    CUSTOM.append(P+key+' = { type = country '+' '.join(parts)+' }')
custom('stage',[(f'var:chi_adm_negotiated_integration_stage = {i}',s) for i,s in [(1,'Imperial proposal: awaiting the governor'),(2,'Provincial reply: court decision required'),(3,'Census and registration'),(4,'Bureaucratic transition'),(5,'Implementation complete: final provincial confirmation'),(6,'Final confirmation withheld: court decision required'),(9,'Repayment settlement under discussion'),(10,'Provincial council considering the proposal')]],'No active integration proposal')
custom('response',[(f'var:chi_adm_negotiated_integration_response = {i}',s) for i,s in [(2,'Closer centralization offered without annexation.'),(3,'The governor requests concessions.'),(4,'The governor declines annexation.'),(5,'The governor requests more time.')]],'No provincial counterproposal recorded.')
custom('activity',[('has_variable = chi_adm_negotiated_integration_breach','Qing broke the agreement; provincial consent may be withdrawn.'),('has_variable = chi_adm_negotiated_integration_paused','Suspended: elapsed time preserved; costs and subsidies stopped.'),('has_variable = chi_adm_negotiated_integration_work','Implementation active: commitments and agreed payments continue.')],'Negotiation only: no implementation commitment or subsidy.')
custom('subsidy',[('var:chi_adm_negotiated_integration_subsidy = 2','Automatic subsidy: 20% of provincial income during active implementation.'),('var:chi_adm_negotiated_integration_subsidy = 1','Automatic subsidy: 10% of provincial income during active implementation.')],'No subsidy offered.')
custom('protection',[('var:chi_adm_negotiated_integration_protection = 2','After annexation: -20% Tax Collection, decaying over ten years.'),('var:chi_adm_negotiated_integration_protection = 1','After annexation: -10% Tax Collection, decaying over five years.')],'No post-annexation fiscal privileges offered.')
custom('honors',[('var:chi_adm_negotiated_integration_honors = 1','Honors: +10 governor Popularity/Prominence for ten years; +3 Loyalty/+5 relations on agreement.')],'No imperial honors offered.')
custom('waiting',[('has_variable = chi_adm_negotiated_integration_repayment_left',"Repayment reviews remaining: [Country.MakeScope.Var('chi_adm_negotiated_integration_repayment_left').GetValue|0]"),('var:chi_adm_negotiated_integration_stage = 1',"Unanswered monthly reviews: [Country.MakeScope.Var('chi_adm_negotiated_integration_wait').GetValue|0] / 6 before escalation."),('has_variable = chi_adm_negotiated_integration_suspend_request','An agreed suspension has been requested.'),('has_variable = chi_adm_negotiated_integration_cancel_request','Qing requested mutual cancellation.')],'No response deadline authorizes annexation.')
custom('requests',[('has_variable = chi_adm_negotiated_integration_requested_subsidy','Financial support requested.'),('has_variable = chi_adm_negotiated_integration_requested_protection','Local fiscal protections requested.'),('has_variable = chi_adm_negotiated_integration_requested_honors','Imperial honors requested.')],'No unanswered request for a specific concession.')

# Effect ROOT is inherited from its caller. Payment and state work must use an explicit province target.
for key in E:
    E[key]=E[key].replace('country = root','country = scope:chi_adm_negotiated_integration_province').replace('root = { var:chi_adm_negotiated_integration_protection','scope:chi_adm_negotiated_integration_province = { var:chi_adm_negotiated_integration_protection')
for key in ('stop_payments','apply_protection'):
    E[P+key]='save_scope_as = chi_adm_negotiated_integration_province '+E[P+key]
# Every public action establishes its own target even when called from an old Qing button.
for key in A:E[P+key]='save_scope_as = chi_adm_negotiated_integration_province '+E[P+key]
for category,data in [('scripted_effects',E),('scripted_triggers',T),('scripted_guis',G)]:write('common/'+category+'/chi_adm_negotiated_integration.txt','\n\n'.join(k+' = {\n'+v+'\n}' for k,v in data.items()))
write('common/script_values/chi_adm_negotiated_integration.txt',VALUES)
write('common/static_modifiers/chi_adm_negotiated_integration.txt',MODS)
write('common/diplomatic_actions/chi_adm_negotiated_integration.txt','\n'.join(PACT))
write('common/war_goal_types/chi_adm_negotiated_integration.txt',WG)
write('common/diplomatic_plays/chi_adm_negotiated_integration.txt',PLAY)
write('common/journal_entries/chi_adm_negotiated_integration.txt','\n'.join(ENTRIES))
write('events/chi_adm_negotiated_integration.txt','\n\n'.join(EVENTS))
write('common/customizable_localization/chi_adm_negotiated_integration.txt','\n'.join(CUSTOM))
write('gui/journal_entry_widgets/chi_adm_negotiated_integration.gui',court+'\n'+province)
write('common/on_actions/chi_adm_negotiated_integration.txt','''on_game_started_after_lobby = { on_actions = { chi_adm_negotiated_integration_start } }
chi_adm_negotiated_integration_start = { effect = { c:CHI ?= { chi_adm_negotiated_integration_recount = yes if = { limit = { chi_adm_negotiated_integration_court = yes NOT = { has_journal_entry = chi_adm_negotiated_integration_court } } add_journal_entry = { type = chi_adm_negotiated_integration_court } } } } }
on_monthly_pulse_country = { on_actions = { chi_adm_negotiated_integration_monthly chi_adm_negotiated_integration_orphan chi_adm_negotiated_integration_tax_monthly } }
chi_adm_negotiated_integration_monthly = { trigger = { c:CHI ?= this } effect = { chi_adm_negotiated_integration_court_tick = yes } }
chi_adm_negotiated_integration_orphan = { trigger = { chi_qing_administration_tag = yes OR = { has_variable = chi_adm_negotiated_integration_stage has_variable = chi_adm_negotiated_integration_repayment_left } NOT = { chi_adm_negotiated_integration_valid = yes } } effect = { chi_adm_negotiated_integration_orphan_cleanup = yes } }
chi_adm_negotiated_integration_tax_monthly = { trigger = { any_scope_state = { has_variable = chi_adm_negotiated_integration_tax_left } } effect = {
every_scope_state = { limit = { has_variable = chi_adm_negotiated_integration_tax_left NOT = { has_variable = chi_adm_negotiated_integration_tax_new } } change_variable = { name = chi_adm_negotiated_integration_tax_left subtract = 1 } chi_adm_negotiated_integration_update_tax = yes }
} }
''')
p=ROOT/patched[0];s=p.read_text('utf-8')
for tag in core.TAGS:
    m=re.search(r'(?m)^chi_qing_integrate_'+tag+r' = \{',s);assert m,tag
    i=s.index('{',m.start())+1;depth=1
    while depth:
        if s[i]=='{':depth+=1
        elif s[i]=='}':depth-=1
        i+=1
    replacement=f'''chi_qing_integrate_{tag} = {{
 name = chi_qing_integrate_{tag}
 desc = chi_adm_negotiated_integration_propose_desc
 visible = {{ c:CHI ?= this exists = c:{tag} c:{tag} = {{ chi_adm_eligible = yes }} }}
 possible = {{ c:{tag} = {{ chi_adm_negotiated_integration_can_propose = yes }} }}
 effect = {{ c:{tag} = {{ chi_adm_negotiated_integration_propose = yes }} }}
 ai_chance = {{ base = 3 }}
}}'''
    s=s[:m.start()]+replacement+s[i:]
p.write_text(s,encoding='utf-8')
p=ROOT/patched[1];s=p.read_text('utf-8')
marker='    textbox = { size = { 488 44 } multiline = yes text = "chi_adm_court_register_commitments_display" tooltip = "chi_adm_court_register_commitments_tooltip" }'
addition='\n    textbox = { size = { 488 0 } max_width = 488 autoresize = yes multiline = yes text = "chi_adm_negotiated_integration_ledger_display" }'
if 'chi_adm_negotiated_integration_ledger_display' not in s:
    assert marker in s;s=s.replace(marker,marker+addition,1);p.write_text(s,encoding='utf-8')
p=ROOT/'localization/english/chi_adm_l_english.yml';s=p.read_text('utf-8-sig')
s=re.sub(r'^ chi_adm_negotiated_integration_\w+:.*\n','',s,flags=re.M).replace(' # Negotiated Integration\n','')
s=re.sub(r'^ dp_chi_adm_negotiated_integration_integration:.*\n','',s,flags=re.M)
block=' # Negotiated Integration\n'+''.join(' '+k+': '+json.dumps(v,ensure_ascii=False)+'\n' for k,v in LOC.items())+' dp_chi_adm_negotiated_integration_integration: "Enforce Qing Direct Administration"\n'
at=re.search(r'^ chi_adm_imperial_law_(?:requested_name|group_name|current_name|requested_icon|current_icon)_\d+:',s,re.M);pos=at.start() if at else len(s)
s=s[:pos].rstrip()+'\n\n'+block+s[pos:];p.write_text(s,encoding='utf-8-sig')
print(f'Built negotiated integration: {len(E)} effects, {len(G)} GUI bindings, seven decision events + calendar clock, two nested JEs, {len(LOC)} English keys')


