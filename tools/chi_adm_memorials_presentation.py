"""memorials and audits presentation-only projection of native effects; never runs gameplay."""
import re
import validate_chi_adm as core
ICONS={'loyalty':'gfx/interface/icons/generic_icons/population_loyalist.dds',
       'autonomy':'gfx/interface/icons/diplomatic_action_icons/da_increase_autonomy.dds',
       'corruption':'gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds'}

def emit(items):
    return '\n'.join(k if op=='list' else k+' '+op+' '+('{ '+emit(v)+' }' if isinstance(v,list) else v) for k,op,v in items)

def enrich(value):
    # Custom provincial accounts are not the native interest-group loyalty concept.
    value=re.sub(r'£([\d,]+)',r'@money!#v \1#!',value)
    for word,concept in [('Authority','authority'),('Bureaucracy','bureaucracy'),('Prestige','prestige'),('Gold Reserves','gold_reserves')]:
        value=re.sub(r'\b'+word+r'\b','[concept_'+concept+']',value)
    for word in ('Loyalty','Autonomy','Corruption'):
        value=re.sub(r'\b'+word+r'\b','[concept_chi_adm_'+word.lower()+']',value)
    for kind in ICONS:
        value=re.sub(r'(?:@chi_adm_'+kind+r'!\[Nbsp\])?\[concept_chi_adm_'+kind+r'\]',
                     '@chi_adm_'+kind+'![Nbsp][concept_chi_adm_'+kind+']',value)
    return value

def apply(effects,buttons,guis,loc,triggers):
    trees={k:core.parse(v) for k,v in effects.items()}
    trigger_trees={k:core.parse(v) for k,v in triggers.items()}
    def requirement_parts(items,outer=True):
        result=[];private=[]
        for k,op,v in items:
            if k=='text' or (k=='always' and v=='yes'):continue
            if k in trigger_trees and v=='yes':
                result+=requirement_parts(trigger_trees[k],False)
            elif k=='chi_adm_target_valid':
                result.append(('hidden_trigger','=',[(k,op,v)]))
            elif k in ('authority','gold_reserves','relative_bureaucracy','is_at_war','has_modifier') or (k=='NOT' and all(x[0]=='has_modifier' for x in v)):
                result.append((k,op,v))
            elif k.startswith('var:chi_adm_') and k[4:] in ('chi_adm_loyalty','chi_adm_autonomy','chi_adm_corruption'):
                kind=k.removeprefix('var:chi_adm_')
                compare={'>=':'greater than or equal to','>':'greater than','<':'less than','<=':'less than or equal to','=':'equal to'}[op]
                key='chi_adm_memorials_requirement_'+kind+'_'+str(len(loc))
                loc[key]=f"[ROOT.GetCountry.GetName] @chi_adm_{kind}![Nbsp][concept_chi_adm_{kind}] is {compare} #variable {v}#!"
                result.append(('custom_tooltip','=',[('text','=',key),(k,op,v)]))
            else:private.append((k,op,v))
        if private:
            key='chi_adm_memorials_case_requirements'
            loc[key]='The administration is eligible and the case, cooldown and response-window rules permit this choice.'
            result.insert(0,('custom_tooltip','=',[('text','=',key)]+private))
        if outer:
            combined=[];visible=[]
            for entry in result:
                if entry[0]=='custom_tooltip' and core.get(entry[2],'text')=='chi_adm_memorials_case_requirements':
                    combined.extend(x for x in entry[2] if x[0]!='text')
                else:visible.append(entry)
            result=([('custom_tooltip','=',[('text','=','chi_adm_memorials_case_requirements')]+combined)] if combined else [])+visible
        return result
    conditions={}
    def readable_limit(limit):
        if 'var:chi_adm_memorials_' not in str(limit):return limit
        source=repr(limit)
        if source not in conditions:
            key='chi_adm_memorials_preview_condition_'+str(len(conditions)+1)
            label='When these terms apply to the current provincial case.'
            for field,values in [('memorial',{1:'For a fiscal relief memorial.',2:'For a memorial seeking administrative latitude.',3:'For emergency military assistance.'}),('edict',{1:'For an administrative supervision edict.',2:'For an imperial commendation.',3:'For emergency military assistance.'})]:
                for number,text in values.items():
                    if (f'var:chi_adm_memorials_{field}', '=', str(number)) in limit:label=text
            if ('var:chi_adm_memorials_edict_stage','=','4') in limit:label='Under the negotiated terms.'
            conditions[source]=key;loc[key]=label
        return [('custom_tooltip','=',[('text','=',conditions[source])]+limit)]
    def project(items,seen=()):
        out=[]
        for k,op,v in items:
            if k in trees:
                assert k not in seen
                out+=project(trees[k],seen+(k,))
            elif k.startswith('chi_adm_adjust_'):
                kind=k.removeprefix('chi_adm_adjust_');amount=int(core.get(v,'AMOUNT'))
                key='chi_adm_memorials_preview_'+kind+('_gain_' if amount>=0 else '_loss_')+str(abs(amount))
                color='g' if (amount>0)==(kind!='corruption') else 'r'
                loc[key]=f'[concept_chi_adm_{kind}]: #{color} {amount:+d}#! (bounded to #v 0–100#!)'
                out.append(('custom_tooltip','=',key))
            elif k in ('add_modifier','add_treasury','change_relations'):
                out.append((k,op,v))
            elif k=='remove_modifier':
                out.append(('if','=',[('limit','=',[('has_modifier','=',v)]),(k,op,v)]))
            elif k in ('c:CHI','hidden_effect'):
                children=project(v,seen)
                if children:out+=children if k=='hidden_effect' else [(k,op,children)]
            elif k in ('if','else_if','else'):
                # Keep the whole conditional chain, including empty alternatives,
                # so a preview cannot turn an else into an unconditional reward.
                children=project([x for x in v if x[0]!='limit'],seen)
                limit=[(a,b,readable_limit(z)) for a,b,z in v if a=='limit']
                out.append((k,op,limit+children))
        return out
    def action_preview(live):
        # Eligibility is already shown by the button. Keep consequences visible
        # even while its outer availability gate is currently false.
        if len(live)==1 and live[0][0] in trees:
            body=trees[live[0][0]]
            if len(body)==1 and body[0][0]=='if':
                return project([x for x in body[0][2] if x[0]!='limit'])
        return project(live)
    for name,source in buttons.items():
        body=core.parse(source)
        live=core.get(core.get(body,'effect'),'hidden_effect')
        preview=action_preview(live)
        new=[]
        for k,op,v in body:
            if k=='effect':v=[('show_as_tooltip','=',preview),('hidden_effect','=',live)]
            if k=='possible':
                tip=core.get(v,'custom_tooltip')
                v=requirement_parts(tip)
            new.append((k,op,v))
        buttons[name]=emit(new)
    def court_requirements(items,actor='Province'):
        output=[]
        for k,op,v in items:
            if k=='chi_adm_target_valid':continue
            if k in trigger_trees and v=='yes' and 'can_pay' not in k:
                output+=court_requirements(trigger_trees[k],actor);continue
            if k=='c:CHI' and isinstance(v,list):
                for child in v:
                    for entry in court_requirements([child],'Qing'):
                        if entry[0]=='if':
                            condition=entry[2][0][2]
                            entry[2][0]=('limit','=',[('c:CHI','=',condition)])
                        output.append(entry)
                continue
            label='The current case permits this action'
            if k=='OR' and 'court_staff' in str(v) and 'authority' in str(v):label='Qing can share its active Court Correspondence or commit #v 25#! [concept_authority]'
            if 'can_pay' in k:label='Qing can fund the requested settlement'
            elif k=='authority':label=f'{actor}: at least #v {v}#! [concept_authority] available'
            elif k=='gold_reserves':label=f'{actor}: at least @money!#v {float(v):,.0f}#! in [concept_gold_reserves]'
            elif k=='is_at_war':label='The province is at [concept_war]'
            elif k.startswith('var:chi_adm_'):
                field=k[4:]
                if field in ('chi_adm_corruption','chi_adm_loyalty','chi_adm_autonomy'):
                    kind=field.removeprefix('chi_adm_');compare={'>=':'at least','<':'below','=':'equal to','>':'above','<=':'at most'}[op]
                    label=f"[concept_chi_adm_{kind}]: {compare} #v {v}#! (currently #v [ROOT.GetCountry.MakeScope.Var('{field}').GetValue|0]#!)"
                elif field.endswith('memorial_stage'):label='A memorial is awaiting the court\x27s reply'
                elif field.endswith('edict_stage'):label='A provincial appeal is awaiting the court\x27s reply'
                elif field.endswith('audit'):label='The audit has exposed misconduct and awaits a court decision'
            elif k=='has_variable':label='An edict is awaiting resolution'
            elif k=='NOT':
                content=str(v)
                if 'any_subject_or_below' in content:label='Fewer than #v two#! edicts or audits are outstanding'
                elif 'court_staff' in content:label='Imperial clerks are free of another correspondence commitment'
                elif 'cooldown' in content:label='The target\x27s '+('three-year audit' if 'audit' in content else 'two-year edict')+' cooldown has ended'
                elif 'audit' in content:label='No audit is already pending in this province'
                elif 'edict' in content:label='No edict is already pending in this province'
            key='chi_adm_memorials_court_requirement_'+str(len(loc))
            loc[key+'_yes']=enrich('@green_checkmark! '+label)
            loc[key+'_no']=enrich('@red_cross! '+label)
            output.append(('if','=',[('limit','=',[(k,op,v)]),('custom_tooltip_no_bullet','=',key+'_yes')]))
            output.append(('else','=',[('custom_tooltip_no_bullet','=',key+'_no')]))
        return output
    loc['chi_adm_memorials_requirements_heading']='#bold Requirements#!'
    loc['chi_adm_memorials_effects_heading']='#bold Immediate effects#!'
    for name,source in guis.items():
        body=core.parse(source)
        if not any(k=='effect' for k,op,v in body):continue
        live=core.get(body,'effect')
        body=[(k,op,[('custom_tooltip','=',name+'_tt'),('show_as_tooltip','=',[('custom_tooltip_no_bullet','=','chi_adm_memorials_requirements_heading')]+court_requirements(core.get(body,'is_valid'))+[('custom_tooltip_no_bullet','=','chi_adm_memorials_effects_heading')]+action_preview(live)),('hidden_effect','=',live)] if k=='effect' else v) for k,op,v in body]
        guis[name]=emit(body)
    # Native cards carry immediate numerical consequences; descriptions explain
    # the purpose and consent/deadline policy instead of repeating them three times.
    descriptions={
        'file_relief':'Petition for @money!#v 20,000#! from Qing [concept_gold_reserves] and #g +5#! [concept_chi_adm_loyalty]. A compromise offers half the money and #g +3#! [concept_chi_adm_loyalty]. No payment occurs until approval. Filing cooldown: #v two years#!; answer window: #v six monthly reviews#!.',
        'file_discretion':"Request #v twelve months#! of [GetStaticModifier('chi_adm_memorials_discretion').GetName]:\n[GetStaticModifier('chi_adm_memorials_discretion').GetDesc]\nIf approved: [concept_chi_adm_autonomy] #g +5#!, [concept_chi_adm_corruption] #r +2#!, [concept_chi_adm_loyalty] #g +2#!. A compromise gives only #v +3#! [concept_chi_adm_autonomy] and #g +1#! [concept_chi_adm_loyalty]. Filing cooldown: #v two years#!; answer window: #v six monthly reviews#!.",
        'file_military':"Request @money!#v 10,000#!, [concept_chi_adm_autonomy] #v +3#! and [concept_chi_adm_loyalty] #g +3#! while at [concept_war], with #v twelve months#! of [GetStaticModifier('chi_adm_memorials_emergency').GetName]:\n[GetStaticModifier('chi_adm_memorials_emergency').GetDesc]\nA compromise offers @money!#v 5,000#!, #v +2#! [concept_chi_adm_autonomy] and #g +2#! [concept_chi_adm_loyalty] with the same modifier. No payment occurs until approval. Filing cooldown: #v two years#!.",
        'accept_counter':'Accept the revised court settlement. The effects below reflect the current memorial; the court must still hold the required [concept_gold_reserves].',
        'decline_counter':'Withdraw the memorial. Its original filing cooldown remains.',
        'accept_edict':'Consent to the current edict or revised terms. The effects below reflect the decree currently before this administration.',
        'appeal_edict':'Ask once for revised terms. The court has #v three monthly reviews#! to answer; no compliance is imposed.',
        'delay_edict':'Postpone the decree once for #v three monthly reviews#!.',
        'defy_edict':'Decline the decree and keep local arrangements. No law, office or government is forcibly changed.',
        'audit_cooperate':'Open the registers to the Censorate. Investigation advances #v 25/100#! per review; disclosure becomes more likely. A clean finding improves the accounts.',
        'audit_obstruct':'Hinder access to the registers. Investigation advances #v 10/100#! per review; it cannot be stalled indefinitely.',
        'audit_conceal':'Pay to conceal the accounts. Investigation advances #v 20/100#! per review; detection is less likely. Success adds Corruption and Autonomy, with #v four years#! of suspicion.',
        'pay_restitution':'Authorize restitution from provincial [concept_gold_reserves] to the Qing [concept_treasury].',
        'accept_reform':'Accept the supervised reorganization. This is also available instead of paying restitution.',
        'resist_settlement':'Refuse the proposed settlement. Existing exposure penalties remain until expiry.'}
    for name,text in descriptions.items():loc['chi_adm_memorials_'+name+'_desc']=text
    loc['chi_adm_memorials_audit_cooperate_desc']+=' The staff modifier has a #v twelve-month maximum#! and ends when investigation closes.'
    loc['chi_adm_memorials_approve_memorial_tt']='Grant the current memorial. No imperial staff commitment is charged.'
    loc['chi_adm_memorials_tolerate_tt']='Recognize local patronage without restitution. Existing exposure penalties remain; suspicion raises future audit risk.'
    loc['chi_adm_memorials_propose_reform_tt']="Offer supervised reform, subject to the governor's consent: [concept_chi_adm_corruption] #g -10#!, [concept_chi_adm_loyalty] #r -2#!, [concept_chi_adm_autonomy] #r -3#! (#r -1#! in frontier offices). If accepted, apply #v twelve months#! of [GetStaticModifier('chi_adm_memorials_supervision').GetName]:\n[GetStaticModifier('chi_adm_memorials_supervision').GetDesc]"
    for key in list(loc):
        if key.endswith('_tt'):
            loc[key]=re.sub(r'Commits? 25 Qing Authority for six months[;.,]?', 'Requires uncommitted imperial clerks.',loc[key])
    loc['chi_adm_memorials_desk_display']='File one memorial at a time; the filing cooldown is #v two years#!. A court compromise requires your consent. Replies are entered in Provincial Correspondence.'
    for key in list(loc):loc[key]=enrich(loc[key])

def bars():
    output='''widget = { size = { 472 248 } parentanchor = hcenter
background = { using = dark_area } background = { using = frame_small }
'''
    for i,(kind,texture) in enumerate([('loyalty','gold'),('autonomy','default'),('corruption','bad')]):
        y=16+i*76
        output+=f'''widget = {{ position = {{ 16 {y} }} size = {{ 440 68 }} tooltip = "chi_adm_{kind}_tooltip"
textbox = {{ size = {{ 225 26 }} text = "chi_adm_{kind}_display" }}
textbox = {{ position = {{ 225 0 }} size = {{ 215 26 }} align = right|nobaseline text = "chi_adm_{kind}_tier_display" }}
progressbar = {{ position = {{ 0 32 }} size = {{ 440 20 }} min = 0 max = 100
value = "[FixedPointToFloat(Country.MakeScope.Var('chi_adm_{kind}').GetValue)]"
progresstexture = "gfx/interface/progressbar/progressbar_{texture}.dds" noprogresstexture = "gfx/interface/progressbar/progressbar_empty.dds" direction = horizontal skip_initial_animation = yes }}
widget = {{ position = {{ 0 32 }} size = {{ 440 20 }} background = {{ texture = "gfx/interface/progressbar/progressbar_frame.dds" spriteType = Corneredstretched spriteborder = {{ 6 6 }} texture_density = 2 }} }}
}}
'''
    return output+'}\n'

def older_desk_loc(text):
    # Native button effects display modifiers; custom account checks use the
    # country/icon/concept/comparison layout of vanilla's Authority trigger.
    entries={
        'chi_adm_loyal_memorial_result':"#g +5 Loyalty#!.",
        'chi_adm_negotiate_discretion_result':"#g -5 Autonomy#! and #r -5 Loyalty#!.",
        'chi_adm_supervise_offices_result':"#g -5 Corruption#!."}
    for key,value in entries.items():
        text=re.sub(r'^ '+key+r':.*$',lambda m:' '+key+': "'+enrich(value).replace('\n','\\n')+'"',text,flags=re.M)
    # Give the established bar labels/hover prose the same distinct concepts.
    def entry(match):
        return match[1]+enrich(match[2])+match[3]
    text=re.sub(r'^( chi_adm_(?:loyalty|autonomy|corruption)_(?:display|tooltip): ")(.*)(")$',entry,text,flags=re.M)
    text=re.sub(r'^( chi_adm_(?:req_authority|req_bureaucracy|m2_commitments_tooltip): ")(.*)(")$',entry,text,flags=re.M)
    flavor={'chi_adm_memorial_effort_desc':"Provincial clerks remain assigned to correspondence with the Dragon Throne.",
            'chi_adm_negotiation_effort_desc':"Provincial staff are implementing a negotiated extension of court supervision.",
            'chi_adm_inspection_effort_desc':"Inspectors examine the provincial registers and reorganize the local offices."}
    for key,value in flavor.items():
        text=re.sub(r'^ '+key+r':.*$',lambda m:' '+key+': "'+value+'"',text,flags=re.M)
    tax="[concept_tax_capacity] from [concept_chi_adm_corruption]: #v [Country.MakeScope.ScriptValue('chi_adm_corruption_tax_capacity_percent')|+=1]%#!"
    for i in range(1,6):
        text=re.sub(r'^ chi_adm_court_register_corruption_effect_'+str(i)+r':.*$',lambda m:' chi_adm_court_register_corruption_effect_'+str(i)+': "'+tax+'"',text,flags=re.M)
        text=re.sub(r'^ chi_adm_corruption_tier_'+str(i)+r'_desc:.*$',lambda m:' chi_adm_corruption_tier_'+str(i)+'_desc: "Descriptive corruption tier. Tax Capacity is calculated continuously from the accounts."',text,flags=re.M)
    for key,value in {'chi_adm_loyalty_remittance':'Loyalty: Imperial Remittances','chi_adm_loyalty_remittance_desc':'Provincial loyalty adjusts payments to the overlord from -50% at 0 Loyalty to +50% at 100 Loyalty. This multiplies the existing pact rate.','chi_adm_autonomy_remittance':'Autonomy: Imperial Remittances','chi_adm_autonomy_remittance_desc':'Provincial autonomy adjusts payments to the overlord from +50% at 0 Autonomy to -50% at 100 Autonomy. This adds to the Loyalty adjustment and multiplies the existing pact rate.','chi_adm_corruption_tax_capacity':'Provincial Revenue Administration','chi_adm_corruption_tax_capacity_desc':'The integrity of the provincial accounts determines effective Tax Capacity.'}.items():
        line=' '+key+': "'+value+'"'
        if re.search(r'^ '+key+r':.*$',text,re.M):text=re.sub(r'^ '+key+r':.*$',lambda m:line,text,flags=re.M)
        else:text+=line+'\n'
    desk={
        'chi_adm_court_register_service_end_header':'$je_standard_completion_header$',
        'chi_adm_court_register_service_end_effect_header':'$je_standard_on_completion_header$',
        'chi_adm_court_register_service_closed':'This administration is no longer in imperial service.',
        'chi_adm_court_register_court_relationship':"[concept_overlord]: [Country.GetOverlord.GetName]\n[concept_relations]: #bold [Country.GetRelationsWithDesc(Country.GetOverlord)]#! ([Country.GetRelationsWith(Country.GetOverlord)|+=])",
        'chi_adm_court_register_desk_instructions':'Select a provincial action or submit a memorial to the court.',
        'chi_adm_court_register_memorial_available':'Memorials: @green_checkmark![Nbsp]Ready',
        'chi_adm_court_register_memorial_occupied':'Memorials: @red_cross![Nbsp]Committed',
        'chi_adm_court_register_negotiation_available':'Supervision: @green_checkmark![Nbsp]Ready',
        'chi_adm_court_register_negotiation_occupied':'Supervision: @red_cross![Nbsp]Committed',
        'chi_adm_court_register_inspection_available':'Inspections: @green_checkmark![Nbsp]Ready',
        'chi_adm_court_register_inspection_occupied':'Inspections: @red_cross![Nbsp]Committed',
        'chi_adm_court_register_commitments_tooltip':"Each staff commitment lasts #v 24 months#!.\n\n#v [GetStaticModifier('chi_adm_memorial_effort').GetName]#!\n[GetStaticModifier('chi_adm_memorial_effort').GetDesc]\n\n#v [GetStaticModifier('chi_adm_negotiation_effort').GetName]#!\n[GetStaticModifier('chi_adm_negotiation_effort').GetDesc]\n\n#v [GetStaticModifier('chi_adm_inspection_effort').GetName]#!\n[GetStaticModifier('chi_adm_inspection_effort').GetDesc]"}
    for key,value in desk.items():
        text=re.sub(r'^ '+key+r':.*$',lambda m:' '+key+': "'+value.replace('\n','\\n')+'"',text,flags=re.M)
    for key,kind,comparison,threshold in [
        ('chi_adm_req_loyalty_room','loyalty','less than','chi_adm_value_max'),
        ('chi_adm_req_loyalty','loyalty','greater than or equal to','chi_adm_action_step'),
        ('chi_adm_req_autonomy','autonomy','greater than or equal to','chi_adm_action_step'),
        ('chi_adm_req_corruption','corruption','greater than or equal to','chi_adm_action_step')]:
        value=f"[ROOT.GetCountry.GetName] @chi_adm_{kind}![Nbsp][concept_chi_adm_{kind}] is {comparison} #variable [ROOT.GetCountry.MakeScope.ScriptValue('{threshold}')|0]#!"
        text=re.sub(r'^ '+key+r':.*$',lambda m:' '+key+': "'+value+'"',text,flags=re.M)
    return text


def court_text(loc):
    loc['chi_adm_memorials_province_notice_desc']="The provincial offices have received a court instruction.\n\n#bold Edict#!: [ROOT.GetCountry.GetCustom('chi_adm_memorials_edict_name')]\n[ROOT.GetCountry.GetCustom('chi_adm_memorials_edict_terms')]\n\n#bold Censorate#!: [ROOT.GetCountry.GetCustom('chi_adm_memorials_audit_stage')]\n\nChoose a reply below, or review Provincial Correspondence under The Governor's Accounts. Recording the notice alone does not authorize compliance or payment."

    texts={
    'approve_memorial_tt':"Approve the governor's memorial. No imperial staff commitment is charged.",
    'reject_memorial_tt':"Reject the governor's memorial.",
    'counter_memorial_tt':'Offer reduced terms.\n\n#bold Proposed settlement#!\n- Fiscal relief: half the requested payment.\n- Military aid: half the payment and reduced discretion.\n- Administrative latitude: +3 Autonomy and +1 Loyalty, without the Bureaucracy concession.\n\nThe governor has #v three monthly reviews#! to accept. Payment occurs only after acceptance.',
    'open_audit_tt':'Commission an examination of the provincial accounts.\n\n#bold Investigation routes#!\n- Cooperation: #v 4#! reviews.\n- Obstruction: #v 10#! reviews.\n- Paid concealment: #v 5#! reviews.\nNo reply within #v 3#! reviews counts as obstruction. Findings are uncertain.\n\n#bold Limits#!\n- One audit per province every #v three years#!.\n- At most #v two#! outstanding edicts or audits.\n- One intervention per province.',
    'negotiate_edict_tt':"Offer revised terms in response to the governor's appeal.\n\nThe governor has #v three monthly reviews#! to accept or refuse.",
    'withdraw_edict_tt':'Withdraw the outstanding edict.\n\nIts original cooldown remains.',
    'propose_restitution_tt':'Request restitution from the provincial treasury.\n\n#bold If the governor accepts#!\n- Transfer @money!#v 10,000#! to Qing.\n- Corruption: #g -12#!\n- Loyalty: #r -4#!\n- Autonomy: #r -3#!\n- Remove the exposed-account penalty.\n\nThe governor may choose administrative reform instead. Reply window: #v three monthly reviews#!.',
    'audits_status':'Select an administration to open or review an audit.',
    'memorials_status':'Review provincial memorials and issue a court reply.',
    'edicts_status':'Select an administration to issue or review an edict.',
    'audit_chances':'#bold Discovery risk#!\nHigh Corruption, cooperation and prior suspicion increase discovery. High Loyalty, concealment and wartime disruption reduce it; a Bureaucracy deficit increases it.\n\nDetection weight: #v 50#! versus #v 50#! for no finding.\n- Corruption 60+: #v +60#!; below 20: #v -40#!.\n- Loyalty 60+: #v -20#!.\n- Cooperation: #v +20#!; concealment: #v -30#!.\n- Prior suspicion: #v +40#!.\n- War: #v -10#!; Bureaucracy deficit: #v +10#!.\nDetection weight stays between #v 10#! and #v 150#!.',
    }
    for key,value in texts.items():loc['chi_adm_memorials_'+key]=enrich(value)
    for key in ('send_supervision_tt','send_honors_tt','send_emergency_tt'):
        key="chi_adm_memorials_"+key
        value=loc[key]
        value=value.replace(' Negotiated version:', '\n\n#bold Revised terms#!\n').replace(' Negotiated recognition:', '\n\n#bold Revised terms#!\n').replace(' Negotiated aid:', '\n\n#bold Revised terms#!\n')
        value=value.replace(' Requires uncommitted imperial clerks.', '\n\nRequires uncommitted imperial clerks.').replace(' At most two outstanding', '\nAt most two outstanding').replace(' Six reviews to reply;', '\nReply window: six monthly reviews;')
        loc[key]=value
