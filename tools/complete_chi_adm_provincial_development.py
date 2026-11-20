"""provincial development extensions. Never regenerate or replace the completed provincial accounts–negotiated integration systems."""
from pathlib import Path
import re

R = Path(__file__).resolve().parents[1]
L = {}; E = {}; T = {}; B = {}; V = {}; M = {}; J = {}; EV = []
def loc(k,v): L['chi_adm_provincial_development_'+k]=v; return 'chi_adm_provincial_development_'+k
def out(folder,body): (R/folder).write_text(body+'\n',encoding='utf-8-sig')
def definitions(folder,objects): out(folder,'\n\n'.join(k+' = {\n'+v+'\n}' for k,v in objects.items()))
def fx(k,v): E['chi_adm_provincial_development_'+k]=v
def tr(k,v): T['chi_adm_provincial_development_'+k]=v
def adj(stat,n): return f'chi_adm_adjust_{stat} = {{ AMOUNT = {n} }}'
def action(k,title,desc,cond,body,ai=10):
    loc(k,title);loc(k+'_desc',desc)
    fx(k,'if = { limit = { '+cond+' } '+body+' }')
    B['chi_adm_provincial_development_'+k]=f'''name = chi_adm_provincial_development_{k}
desc = chi_adm_provincial_development_{k}_desc
visible = {{ {cond} }}
possible = {{ {cond} }}
effect = {{ chi_adm_provincial_development_{k} = yes }}
ai_chance = {{ base = {ai} }}'''
def send(n): return f'''save_scope_as = chi_adm_provincial_development_province
c:CHI = {{ save_scope_as = chi_adm_provincial_development_court trigger_event = {{ id = chi_adm_provincial_development_ext.{n} popup = yes }} }}'''
def event(n,title,desc,options,court=False):
    loc(f'ext_{n}_t',title);loc(f'ext_{n}_d',desc)
    items=[]
    for key,weight in options:
        cond=B['chi_adm_provincial_development_'+key].split('visible = { ',1)[1].split(' }\npossible',1)[0]
        gate='scope:chi_adm_provincial_development_province = { '+cond+' }' if court else cond
        effect='scope:chi_adm_provincial_development_province = { chi_adm_provincial_development_'+key+' = yes }' if court else 'chi_adm_provincial_development_'+key+' = yes'
        items.append(f'option = {{ name = chi_adm_provincial_development_{key} trigger = {{ {gate} }} {effect} ai_chance = {{ base = {weight} }} }}')
    items.append('option = { name = chi_adm_provincial_development_later default_option = yes ai_chance = { base = 0 } }')
    EV.append(f'''chi_adm_provincial_development_ext.{n} = {{
type = country_event
title = chi_adm_provincial_development_ext_{n}_t
desc = chi_adm_provincial_development_ext_{n}_d
event_image = {{ video = "ep1_persian_court" }}
icon = "gfx/interface/icons/event_icons/event_scales.dds"
duration = 30
{chr(10).join(items)}
}}''')

# Projects are state-owned. A persistent country object records the paying owner;
# conquest/annexation pauses progress until the new owner explicitly assumes it.
tr('project_free','chi_adm_target_valid = yes NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_project } }')
tr('conversion_ready','''chi_adm_target_valid = yes
is_subject_type = subject_type_qing_frontier_administration
NOT = { has_variable = chi_adm_provincial_development_conversion }
NOT = { has_modifier = chi_adm_provincial_development_guarantee }
NOT = { has_variable = chi_adm_provincial_development_compact_case }
is_at_war = no
relative_bureaucracy >= 0.10
var:chi_adm_loyalty >= 60
var:chi_adm_autonomy <= 60
c:CHI = { has_technology_researched = central_archives relative_bureaucracy >= 0.10 }
NOT = { any_scope_state = { turmoil >= 0.25 } }''')
tr('project_affordable','fixed_income > 0 gold_reserves >= 0')
V['chi_adm_provincial_development_project_bill']='value = fixed_income multiply = var:chi_adm_provincial_development_bill_weight multiply = 0.05 min = 0'
V['chi_adm_provincial_development_sponsored_bill']='value = fixed_income multiply = var:chi_adm_provincial_development_sponsor_weight multiply = 0.025 min = 0'
V['chi_adm_provincial_development_project_progress']='value = var:chi_adm_provincial_development_display_done divide = { value = var:chi_adm_provincial_development_display_total min = 1 } multiply = 100 min = 0 max = 100'
V['chi_adm_provincial_development_conversion_progress']='value = 18 subtract = var:chi_adm_provincial_development_conversion divide = 18 multiply = 100 min = 0 max = 100'
M['chi_adm_provincial_development_project_expense']='icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_negative.dds country_expenses_add = 1'
loc('project_expense','Provincial Development Expenditure')
M['chi_adm_provincial_development_supervision']='icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds country_authority_mult = -0.05'
loc('supervision','Imperial Restoration Commission')
M['chi_adm_provincial_development_guarantee']='icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds country_prestige_mult = 0.02'
loc('guarantee','Guaranteed Provincial Settlement')
M['chi_adm_provincial_development_sanctions']='icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_negative.dds country_authority_mult = -0.05'
loc('sanctions','Court Censure')
branches=[('military','Military','building_group_bg_military_throughput_add',.02),('economic','Economic','building_group_bg_manufacturing_throughput_add',.02),('administrative','Administrative','state_tax_capacity_mult',.03)]
for number,(branch,title,modifier,amount) in enumerate(branches,1):
    for tier in (1,2,3):
        M[f'chi_adm_provincial_development_{branch}_{tier}']=f'icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds {modifier} = {amount*tier:.2f}'
        loc(f'{branch}_{tier}',f'{title} Self-Strengthening — Tier {tier}')
        gate='chi_adm_provincial_development_project_free = yes '
        if tier>1: gate+='has_technology_researched = central_archives '
        gate+='every_scope_state = { '+('NOT = { has_variable = chi_adm_provincial_development_'+branch+' }' if tier==1 else f'var:chi_adm_provincial_development_{branch} = {tier-1}')+' }'
        months={1:12,2:18,3:24}[tier]
        body=f'''every_scope_state = {{
set_variable = {{ name = chi_adm_provincial_development_project value = {number} }}
set_variable = {{ name = chi_adm_provincial_development_project_tier value = {tier} }}
set_variable = {{ name = chi_adm_provincial_development_project_left value = {months} }}
set_variable = {{ name = chi_adm_provincial_development_project_total value = {months} }}
set_variable = {{ name = chi_adm_provincial_development_project_owner value = root }}
}}
{adj('autonomy',{1:2,2:3,3:4}[tier])}'''
        action(f'start_{branch}_{tier}',f'Begin {title} Development — Tier {tier}',f'Fund a {months}-month provincial program. Weekly expense is #v {tier*5}%#! of provincial income. Improves current states; later acquisitions receive no free upgrades.',gate,body)
    upgrades=[]
    for tier in (1,2,3):
        remove=' '.join(f'remove_modifier = chi_adm_provincial_development_{branch}_{x}' for x in (1,2,3))
        upgrades.append(f'''if = {{ limit = {{ var:chi_adm_provincial_development_project_tier = {tier} }}
{remove}
add_modifier = {{ name = chi_adm_provincial_development_{branch}_{tier} }}
set_variable = {{ name = chi_adm_provincial_development_{branch} value = {tier} }} }}''')
    fx('complete_'+branch,'\n'.join(upgrades))

action('takeover','Assume Unfinished Provincial Works','Explicitly assume remaining project expenses. Completed reviews are retained.','any_scope_state = { has_variable = chi_adm_provincial_development_project NOT = { var:chi_adm_provincial_development_project_owner = root } }','every_scope_state = { limit = { has_variable = chi_adm_provincial_development_project } set_variable = { name = chi_adm_provincial_development_project_owner value = root } }')
action('ask_sponsor','Seek Imperial Sponsorship','Seek shared funding and faster completion in exchange for court inspections and less provincial discretion.','chi_adm_target_valid = yes any_scope_state = { has_variable = chi_adm_provincial_development_project NOT = { has_variable = chi_adm_provincial_development_project_sponsored } } NOT = { has_variable = chi_adm_provincial_development_sponsor_case }','set_variable = chi_adm_provincial_development_sponsor_case '+send(1))
action('offer_sponsor','Offer Imperial Sponsorship','Offer half the project expense and accelerated work. The governor must accept.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_sponsor_case c:CHI = { gold_reserves >= 0 fixed_income > 0 }','set_variable = { name = chi_adm_provincial_development_sponsor_case value = 2 } c:CHI = { save_scope_as = chi_adm_provincial_development_court } trigger_event = { id = chi_adm_provincial_development_ext.2 popup = yes }')
action('accept_sponsor','Accept Sponsorship and Inspection','Accept inspections and shared funding. Shortens total work to 9/12/18 months without resetting completed work.','chi_adm_target_valid = yes var:chi_adm_provincial_development_sponsor_case = 2','''every_scope_state = {
limit = { has_variable = chi_adm_provincial_development_project NOT = { has_variable = chi_adm_provincial_development_project_sponsored } }
set_variable = chi_adm_provincial_development_project_sponsored
if = { limit = { var:chi_adm_provincial_development_project_tier = 1 } change_variable = { name = chi_adm_provincial_development_project_left subtract = 3 } set_variable = { name = chi_adm_provincial_development_project_total value = 9 } }
else = { change_variable = { name = chi_adm_provincial_development_project_left subtract = 6 } if = { limit = { var:chi_adm_provincial_development_project_tier = 2 } set_variable = { name = chi_adm_provincial_development_project_total value = 12 } } else = { set_variable = { name = chi_adm_provincial_development_project_total value = 18 } } }
}
chi_adm_adjust_autonomy = { AMOUNT = -1 }
remove_variable = chi_adm_provincial_development_sponsor_case
c:CHI = { save_scope_as = chi_adm_provincial_development_court }''')
action('decline_sponsor','Continue Without Sponsorship','Continue locally funded work without accepting court safeguards.','has_variable = chi_adm_provincial_development_sponsor_case','remove_variable = chi_adm_provincial_development_sponsor_case',5)
event(1,'A Provincial Development Petition',"[SCOPE.sCountry('chi_adm_provincial_development_province').GetName] seeks funding and technical assistance. The governor retains the right to reject imperial safeguards.",[('offer_sponsor',60),('decline_sponsor',10)],True)
event(2,'Inspectors and Provincial Works','The imperial court offers shared funding and accelerated work in exchange for inspections. Accepting reduces the political discretion gained by the program.',[('accept_sponsor',60),('decline_sponsor',15)])

# Compact numbers: Mongol leagues, Inner Mongolian banners, Ili, Xining, Manchuria.
for n,tag,title in [(1,'MGL','Mongol Noble Leagues'),(2,'MGL','Inner Mongolian Banners'),(3,'XIN','Ili Garrison Compact'),(4,'XIB','Xining Religious and Frontier Compact'),(5,'MCH','Three Eastern Generalships')]:
    gate=f'chi_adm_target_valid = yes c:{tag} ?= this NOT = {{ has_variable = chi_adm_provincial_development_compact_case }} NOT = {{ has_modifier = chi_adm_provincial_development_guarantee }}'
    action(f'compact_{n}',f'Review {title}','Open a distinct regional negotiation over customary protections, recruitment duties, fiscal obligations and elite recognition.',gate,f'set_variable = {{ name = chi_adm_provincial_development_compact_case value = {n} }} '+send(3))
    loc('compact_name_'+str(n),title)
for kind,title,desc,body in [
('customs','Affirm Customary Protections','Protect existing laws and customary institutions; gain Loyalty at the cost of local discretion.',adj('loyalty',3)+' '+adj('autonomy',2)+' set_variable = chi_adm_provincial_development_customs_protected'),
('recruit','Negotiate Recruitment Duties','Request closer military cooperation in return for recognition. The governor decides.',adj('autonomy',-3)+' '+adj('loyalty',-2)),
('fiscal','Negotiate Administrative Obligations','Request stronger fiscal and administrative oversight without imposing a new remittance tax.',adj('autonomy',-3)+' '+adj('corruption',-3)),
('honor','Recognize Regional Elites','Recognize local elites and sustain their customary authority.',adj('loyalty',5)+' '+adj('autonomy',2)),
]:
    action('offer_'+kind,title,desc,'chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_compact_case NOT = { has_variable = chi_adm_provincial_development_compact_offer }',f'set_variable = {{ name = chi_adm_provincial_development_compact_offer value = {list(["customs","recruit","fiscal","honor"]).index(kind)+1} }} c:CHI = {{ save_scope_as = chi_adm_provincial_development_court }} trigger_event = {{ id = chi_adm_provincial_development_ext.4 popup = yes }}')
    fx('apply_compact_'+kind,body)
action('accept_compact','Accept the Revised Compact','Apply only the negotiated obligations. Existing laws remain unchanged.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_compact_offer','\n'.join(f'if = {{ limit = {{ var:chi_adm_provincial_development_compact_offer = {i} }} chi_adm_provincial_development_apply_compact_{kind} = yes }}' for i,kind in enumerate(['customs','recruit','fiscal','honor'],1))+'''set_variable = { name = chi_adm_provincial_development_compact_cooldown value = yes months = 24 }
remove_variable = chi_adm_provincial_development_compact_offer remove_variable = chi_adm_provincial_development_compact_case''')
action('refuse_compact','Retain the Existing Compact','Decline the revision. Existing institutions and laws continue.','has_variable = chi_adm_provincial_development_compact_case','remove_variable = chi_adm_provincial_development_compact_offer remove_variable = chi_adm_provincial_development_compact_case set_variable = { name = chi_adm_provincial_development_compact_cooldown value = yes months = 24 }',15)
event(3,'The Frontier Compact',"[SCOPE.sCountry('chi_adm_provincial_development_province').GetName] invites a review of its regional obligations. Propose one targeted revision; the governor must consent.",[(f'offer_{k}',20) for k in ['customs','recruit','fiscal','honor']]+[('refuse_compact',5)],True)
event(4,'Custom and Imperial Service','The court proposes a regional settlement. Accepting changes only the specified administrative obligations; it does not overwrite local law.',[('accept_compact',50),('refuse_compact',20)])

action('propose_conversion','Propose Civil Reorganization','Offer an eighteen-month negotiated conversion. Existing laws and regional compacts remain. Completion reduces Autonomy by 20.','chi_adm_provincial_development_conversion_ready = yes','set_variable = { name = chi_adm_provincial_development_conversion value = -1 } c:CHI = { save_scope_as = chi_adm_provincial_development_court } trigger_event = { id = chi_adm_provincial_development_ext.5 popup = yes }')
action('accept_conversion','Agree to Civil Reorganization','Begin eighteen months of preparation. MCH becomes a viceroyalty; other frontier administrations become provincial administrations.','chi_adm_target_valid = yes var:chi_adm_provincial_development_conversion = -1','set_variable = { name = chi_adm_provincial_development_conversion value = 18 } set_variable = chi_adm_provincial_development_conversion_agreed')
action('decline_conversion','Preserve the Frontier Government','Decline the initial conversion without authorizing enforcement.','var:chi_adm_provincial_development_conversion = -1','remove_variable = chi_adm_provincial_development_conversion',15)
action('repudiate_conversion','Repudiate the Agreed Conversion','Pause the agreement. The court may negotiate or seek enforcement.','has_variable = chi_adm_provincial_development_conversion_agreed var:chi_adm_provincial_development_conversion > 0 NOT = { has_variable = chi_adm_provincial_development_conversion_repudiated }','set_variable = chi_adm_provincial_development_conversion_repudiated set_variable = chi_adm_provincial_development_dispute',5)
fx('finish_conversion','''if = { limit = { c:MCH ?= this } change_subject_type = subject_type_qing_viceroyalty_administration }
else = { change_subject_type = subject_type_qing_civil_administration }
chi_adm_adjust_autonomy = { AMOUNT = -20 }
remove_variable = chi_adm_provincial_development_conversion
remove_variable = chi_adm_provincial_development_conversion_agreed
remove_variable = chi_adm_provincial_development_conversion_repudiated''')
event(5,'A Civil Government for the Frontier','The imperial court offers an eighteen-month transition to civil administration. Existing laws and regional compacts survive. The governor must agree before preparation begins.',[('accept_conversion',45),('decline_conversion',25)])

# Political response to sustained crisis; one bounded demand chain per province.
action('grant_discretion','Grant Provincial Discretion','Grant limited crisis discretion: +5 Autonomy and +3 Loyalty.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_crisis_demand',adj('autonomy',5)+' '+adj('loyalty',3)+' remove_variable = chi_adm_provincial_development_crisis_demand set_variable = { name = chi_adm_provincial_development_demand_cooldown value = yes months = 36 }')
action('resist_demand','Maintain Court Authority','Refuse the demand: −3 Loyalty; no automatic grant of powers.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_crisis_demand',adj('loyalty',-3)+' remove_variable = chi_adm_provincial_development_crisis_demand set_variable = { name = chi_adm_provincial_development_demand_cooldown value = yes months = 36 }',15)
action('fund_alternative','Fund the Existing Administration','Transfer 10,000 from the court treasury to the province instead of granting discretion.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_crisis_demand c:CHI = { gold_reserves >= 10000 }','c:CHI = { add_treasury = -10000 } add_treasury = 10000 '+adj('loyalty',3)+' remove_variable = chi_adm_provincial_development_crisis_demand set_variable = { name = chi_adm_provincial_development_demand_cooldown value = yes months = 36 }')
event(6,'The Burden of Imperial Crisis',"[SCOPE.sCountry('chi_adm_provincial_development_province').GetName] requests greater discretion during the imperial emergency. Grant powers, fund an alternative or resist. Ignoring the demand allows a bounded increase in autonomy.",[('grant_discretion',35),('fund_alternative',30),('resist_demand',20)],True)

action('censure','Censure Provincial Defiance','Impose a two-year court censure and lose 3 provincial Loyalty.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_dispute NOT = { has_modifier = chi_adm_provincial_development_guarantee }','add_modifier = { name = chi_adm_provincial_development_sanctions years = 2 } '+adj('loyalty',-3),15)
action('tolerate','Tolerate Provincial Discretion','End the dispute without reclaiming its Autonomy gain.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_dispute','remove_variable = chi_adm_provincial_development_dispute remove_modifier = chi_adm_provincial_development_unrestored remove_variable = chi_adm_provincial_development_package remove_variable = chi_adm_provincial_development_autonomy_grant',15)
action('enforce','Enforce the Imperial Settlement','Launch a contested enforcement play. Victory restores disputed powers, costs 5 Loyalty and imposes two years of supervision. Provincial victory grants +5 Autonomy and a three-year guarantee.','chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_dispute NOT = { has_modifier = chi_adm_provincial_development_guarantee } is_at_war = no c:CHI = { is_at_war = no NOT = { has_variable = chi_adm_provincial_development_enforcement } }','set_variable = chi_adm_provincial_development_enforcement_target c:CHI = { set_variable = chi_adm_provincial_development_enforcement create_diplomatic_play = { type = dp_chi_adm_provincial_development_enforcement target_country = prev } }',5)
fx('court_victory','''if = { limit = { has_variable = chi_adm_provincial_development_conversion_repudiated } chi_adm_provincial_development_finish_conversion = yes }
if = { limit = { has_variable = chi_adm_provincial_development_autonomy_grant } chi_adm_adjust_autonomy = { AMOUNT = chi_adm_provincial_development_restoration_change } }
chi_adm_adjust_loyalty = { AMOUNT = -5 }
chi_adm_provincial_development_cleanup = yes
add_modifier = { name = chi_adm_provincial_development_supervision years = 2 }
remove_variable = chi_adm_provincial_development_enforcement_target
c:CHI = { remove_variable = chi_adm_provincial_development_enforcement }''')
fx('province_victory','''chi_adm_adjust_autonomy = { AMOUNT = 5 }
add_modifier = { name = chi_adm_provincial_development_guarantee years = 3 }
remove_variable = chi_adm_provincial_development_dispute
remove_variable = chi_adm_provincial_development_enforcement_target
c:CHI = { remove_variable = chi_adm_provincial_development_enforcement }''')
event(7,'A Governor and the Imperial Court',"[SCOPE.sCountry('chi_adm_provincial_development_province').GetName] retains disputed powers. Censure, tolerate the arrangement or seek a contested settlement.",[('censure',25),('tolerate',30),('enforce',10)],True)

fx('state_project_tick','''if = { limit = { var:chi_adm_provincial_development_project_owner = root owner = { chi_adm_provincial_development_project_affordable = yes } }
    change_variable = { name = chi_adm_provincial_development_project_left subtract = 1 }
    if = { limit = { var:chi_adm_provincial_development_project_left <= 0 }
        if = { limit = { var:chi_adm_provincial_development_project = 1 } chi_adm_provincial_development_complete_military = yes }
        else_if = { limit = { var:chi_adm_provincial_development_project = 2 } chi_adm_provincial_development_complete_economic = yes }
        else = { chi_adm_provincial_development_complete_administrative = yes }
        remove_variable = chi_adm_provincial_development_project remove_variable = chi_adm_provincial_development_project_tier
        remove_variable = chi_adm_provincial_development_project_left remove_variable = chi_adm_provincial_development_project_total
        remove_variable = chi_adm_provincial_development_project_owner remove_variable = chi_adm_provincial_development_project_sponsored
    }
}''')
fx('extension_monthly','''set_variable = { name = chi_adm_provincial_development_bill_weight value = 0 }
set_variable = { name = chi_adm_provincial_development_sponsor_weight value = 0 }
set_variable = { name = chi_adm_provincial_development_display_done value = 0 }
set_variable = { name = chi_adm_provincial_development_display_total value = 0 }
every_scope_state = {
    limit = { has_variable = chi_adm_provincial_development_project }
    if = { limit = { var:chi_adm_provincial_development_project_owner = root }
        root = { change_variable = { name = chi_adm_provincial_development_bill_weight add = prev.var:chi_adm_provincial_development_project_tier } }
        if = { limit = { has_variable = chi_adm_provincial_development_project_sponsored }
            root = { change_variable = { name = chi_adm_provincial_development_sponsor_weight add = prev.var:chi_adm_provincial_development_project_tier } }
        }
        root = {
            change_variable = { name = chi_adm_provincial_development_display_total add = prev.var:chi_adm_provincial_development_project_total }
            change_variable = { name = chi_adm_provincial_development_display_done add = { value = prev.var:chi_adm_provincial_development_project_total subtract = prev.var:chi_adm_provincial_development_project_left } }
        }
        chi_adm_provincial_development_state_project_tick = yes
    }
}
if = { limit = { chi_adm_target_valid = yes }
    if = { limit = { has_variable = chi_adm_provincial_development_conversion var:chi_adm_provincial_development_conversion > 0 NOT = { has_variable = chi_adm_provincial_development_conversion_repudiated } is_at_war = no relative_bureaucracy >= 0 }
        change_variable = { name = chi_adm_provincial_development_conversion subtract = 1 }
        if = { limit = { var:chi_adm_provincial_development_conversion <= 0 } chi_adm_provincial_development_finish_conversion = yes }
    }
    if = { limit = { chi_adm_provincial_development_crisis = yes NOT = { has_variable = chi_adm_provincial_development_demand_cooldown } NOT = { has_variable = chi_adm_provincial_development_crisis_demand } }
        set_variable = { name = chi_adm_provincial_development_crisis_demand value = 6 }
        '''+send(6)+'''
    }
    else_if = { limit = { has_variable = chi_adm_provincial_development_crisis_demand }
        change_variable = { name = chi_adm_provincial_development_crisis_demand subtract = 1 }
        if = { limit = { var:chi_adm_provincial_development_crisis_demand <= 0 }
            chi_adm_adjust_autonomy = { AMOUNT = 10 }
            remove_variable = chi_adm_provincial_development_crisis_demand
            set_variable = { name = chi_adm_provincial_development_demand_cooldown value = yes months = 36 }
        }
    }
}
if = { limit = { has_variable = chi_adm_provincial_development_enforcement_target NOT = { is_at_war = yes } NOT = { is_diplomatic_play_committed_participant = yes } }
    remove_variable = chi_adm_provincial_development_enforcement_target
    c:CHI = { remove_variable = chi_adm_provincial_development_enforcement }
}''')

# Native custom war goal: no annexation/independence side effects.
out('common/war_goal_types/chi_adm_provincial_development.txt','''chi_adm_provincial_development_restore = {
icon = "gfx/interface/icons/war_goals/reduce_autonomy.dds"
kind = custom
target_type = country
contestion_type = control_half_target_country_states
possible = { scope:target_country = { has_variable = chi_adm_provincial_development_enforcement_target } }
valid = { scope:target_country = { has_variable = chi_adm_provincial_development_enforcement_target } }
maneuvers = 20
infamy = 5
on_enforced = { scope:target_country = { chi_adm_provincial_development_court_victory = yes } }
}
chi_adm_provincial_development_guarantee = {
icon = "gfx/interface/icons/war_goals/reduce_autonomy.dds"
kind = custom
target_type = country
contestion_type = control_half_target_country_states
possible = { always = yes }
valid = { always = yes }
maneuvers = 0
infamy = 0
on_enforced = { root = { chi_adm_provincial_development_province_victory = yes } }
}''')
out('common/diplomatic_plays/chi_adm_provincial_development.txt','''dp_chi_adm_provincial_development_enforcement = {
war_goal = chi_adm_provincial_development_restore
texture = "gfx/interface/icons/war_goals/reduce_autonomy.dds"
requires_interest_marker = no
possible = { c:CHI ?= this scope:target_country = { chi_adm_target_valid = yes has_variable = chi_adm_provincial_development_dispute NOT = { has_modifier = chi_adm_provincial_development_guarantee } } }
ai_acceptance_max = 50
on_weekly_pulse = {}
on_war_begins = {}
on_war_end = {}
}''')
for key,value in [('dp_chi_adm_provincial_development_enforcement','Enforce Imperial Administration'),('war_goal_chi_adm_provincial_development_restore','Restore Imperial Authority'),('war_goal_chi_adm_provincial_development_restore_type_name','Restore Imperial Authority'),('war_goal_chi_adm_provincial_development_guarantee','Guarantee Provincial Discretion'),('war_goal_chi_adm_provincial_development_guarantee_type_name','Guarantee Provincial Discretion')]: L[key]=value

# Native JE funding owns costs; fixed-income scaling is recalculated by the engine.
loc('development','Provincial Self-Strengthening')
loc('development_reason','Develop the province through military, economic and administrative initiatives. Completed improvements stay with their states. Occupation or a change of owner does not silently authorize new expenditure.')
loc('frontier','Customary Administration and the Imperial Court')
loc('frontier_reason','Review regional compacts, negotiate civil government and resolve disputes over exceptional provincial powers.')
loc('court_extension','Frontier and Provincial Affairs')
loc('court_extension_reason','Review the administrations’ development, regional agreements and outstanding disputes. Governors retain explicit choices through court correspondence.')
province_keys=[k for k in B if not any(k.endswith('_'+x) for x in ['offer_sponsor','offer_customs','offer_recruit','offer_fiscal','offer_honor','grant_discretion','resist_demand','fund_alternative','censure','tolerate','enforce','propose_conversion'])]
for name,keys in [('development',[k for k in province_keys if any(x in k for x in ['start_','sponsor','takeover'])]),('frontier',[k for k in province_keys if k not in [x for x in province_keys if any(y in x for y in ['start_','sponsor','takeover'])]])]:
    J['chi_adm_provincial_development_'+name]=f'''icon = "gfx/interface/icons/event_icons/event_scales.dds"
group = je_group_chi_adm_court_register_province
context = country
transferable = no
is_shown_when_inactive = {{ OR = {{ chi_adm_target_valid = yes any_scope_state = {{ has_variable = chi_adm_provincial_development_project }} }} }}
possible = {{ OR = {{ chi_adm_target_valid = yes any_scope_state = {{ has_variable = chi_adm_provincial_development_project }} }} }}
widget = {{ gui = "gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui" name = "chi_adm_provincial_development_status" container = "custom_widget_container_1" }}
'''+'\n'.join('scripted_button = '+k for k in keys)+('''
scaling_modifiers_while_active = { modifier = chi_adm_provincial_development_project_expense value = chi_adm_provincial_development_project_bill }
''' if name=='development' else '')
court_keys=[k for k in B if k not in province_keys]
J['chi_adm_provincial_development_court_extension']='''icon = "gfx/interface/icons/event_icons/event_scales.dds"
group = je_group_chi_adm_court_register_court
context = country
transferable = no
is_shown_when_inactive = { c:CHI ?= this chi_adm_court_valid = yes }
possible = { c:CHI ?= this chi_adm_court_valid = yes }
widget = { gui = "gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui" name = "chi_adm_provincial_development_court_status" container = "custom_widget_container_1" }'''
G={}
for k in court_keys:
    cond=B[k].split('visible = { ',1)[1].split(' }\npossible',1)[0]
    G[k]=f'scope = country is_valid = {{ {cond} }} effect = {{ {k} = yes }}'
loc('status',"#gold Provincial Development and Compacts#!\n@chi_adm_loyalty! [concept_chi_adm_loyalty]: #v [Country.MakeScope.Var('chi_adm_loyalty').GetValue|0]#!  @chi_adm_autonomy! [concept_chi_adm_autonomy]: #v [Country.MakeScope.Var('chi_adm_autonomy').GetValue|0]#!\nProject reviews: #v [Country.MakeScope.Var('chi_adm_provincial_development_display_done').GetValue|0]#! / #v [Country.MakeScope.Var('chi_adm_provincial_development_display_total').GetValue|0]#!\nCivil preparation: #v [Country.MakeScope.Var('chi_adm_provincial_development_conversion').GetValue|0]#! reviews remaining. Higher-tier projects require Central Archives. Hover available actions for their costs and terms.")
widgets='''flowcontainer = {
name = "chi_adm_provincial_development_status"
direction = vertical
spacing = 8
datacontext = "[JournalEntry.GetCountry]"
textbox = { size = { 440 0 } max_width = 440 autoresize = yes multiline = yes text = "chi_adm_provincial_development_status" }
progressbar = { size = { 440 16 } min = 0 max = 100 value = "[FixedPointToFloat(Country.MakeScope.ScriptValue('chi_adm_provincial_development_project_progress'))]" }
progressbar = { size = { 440 16 } min = 0 max = 100 value = "[FixedPointToFloat(Country.MakeScope.ScriptValue('chi_adm_provincial_development_conversion_progress'))]" }
}
flowcontainer = {
name = "chi_adm_provincial_development_court_status"
direction = vertical
spacing = 8
datamodel = "[GetPlayer.GetDiplomaticPacts]"
item = { }
}
'''
# Use the already working country list, rather than an unverified diplomatic model.
widgets=widgets[:widgets.index('flowcontainer = {\nname = "chi_adm_provincial_development_court_status"')]
widgets+='''flowcontainer = {
name = "chi_adm_provincial_development_court_status"
direction = vertical
spacing = 8
datamodel = "[GetPlayer.GetSubjectCountries]"
item = { flowcontainer = { direction = vertical spacing = 6
textbox = { size = { 440 0 } max_width = 440 autoresize = yes multiline = yes text = "[Country.GetName]" }
'''
for key in court_keys:
    widgets+=f'''button = {{
size = {{ 440 48 }} using = default_button_action
visible = "[GetScriptedGui('{key}').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
onclick = "[GetScriptedGui('{key}').Execute(GuiScope.SetRoot(Country.MakeScope).End)]"
tooltip = "[GetScriptedGui('{key}').ExecuteTooltip(GuiScope.SetRoot(Country.MakeScope).End)]"
textbox = {{ size = {{ 416 0 }} max_width = 416 autoresize = yes multiline = yes text = "{key}" }}
}}
'''
widgets+='} }\n}'
out('gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui',widgets)
definitions('common/scripted_effects/chi_adm_provincial_development_extension.txt',E)
definitions('common/scripted_triggers/chi_adm_provincial_development_extension.txt',T)
definitions('common/script_values/chi_adm_provincial_development_extension.txt',V)
definitions('common/static_modifiers/chi_adm_provincial_development_extension.txt',M)
definitions('common/scripted_buttons/chi_adm_provincial_development_extension.txt',B)
definitions('common/scripted_guis/chi_adm_provincial_development_extension.txt',G)
definitions('common/journal_entries/chi_adm_provincial_development_extension.txt',J)
out('events/chi_adm_provincial_development_extension.txt','namespace = chi_adm_provincial_development_ext\n\n'+'\n\n'.join(EV))
out('common/on_actions/chi_adm_provincial_development_extension.txt','''on_monthly_pulse_country = { on_actions = { chi_adm_provincial_development_extension_monthly } }
chi_adm_provincial_development_extension_monthly = {
trigger = { OR = { chi_qing_administration_tag = yes any_scope_state = { has_variable = chi_adm_provincial_development_project } } }
effect = { chi_adm_provincial_development_extension_monthly = yes }
}''')
p=R/'localization/english/chi_adm_l_english.yml';s=p.read_text(encoding='utf-8-sig')
for k,v in L.items():
    if not re.search(r'^ '+k+':',s,re.M): s+='\n '+k+': "'+v.replace('\n',r'\n')+'"\n'
p.write_text(s,encoding='utf-8-sig')
print('Built provincial development extensions; run focused validation before runtime testing.')
