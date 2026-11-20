from chi_adm_authorized_validation import authorized_current
"""Actual memorials and audits AST interpreter and static preservation checks; not the game engine."""
from pathlib import Path
import copy
import hashlib
import json
import re
import validate_chi_adm as core
import validate_chi_adm_court_register as ui
ROOT=Path(__file__).resolve().parents[1]
E=core.definitions('common/scripted_effects/chi_adm_memorials.txt')
T=core.definitions('common/scripted_triggers/chi_adm_memorials.txt')
B=core.definitions('common/scripted_buttons/chi_adm_memorials.txt')
G=core.definitions('common/scripted_guis/chi_adm_memorials.txt')

def static():
    assert T['chi_adm_memorials_valid']==[('chi_adm_target_valid','=','yes')]
    baseline=json.loads((ROOT/'tools/chi_adm_memorials_baseline.json').read_text())
    for path,digest in baseline['files'].items():
        assert (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest) or authorized_current(path),path
    current=core.load('common/journal_entries/chi_adm_court_register_governance.txt')
    def strip(items):
        out=[]
        for k,op,v in items:
            if k=='scripted_button' and str(v).startswith('chi_adm_memorials_'):continue
            if k=='widget' and 'chi_adm_memorials_desk_status' in str(v):continue
            out.append((k,op,strip(v) if isinstance(v,list) else v))
        return out
    assert json.loads(json.dumps(strip(current)))==baseline['desk_original'],'court register changed beyond desk extension'
    entries=core.definitions('common/journal_entries/chi_adm_memorials.txt')
    assert len(entries)==4
    for entry in entries.values():
        assert core.get(entry,'transferable')=='no' and core.get(entry,'can_revolution_inherit')=='no'
        assert core.get(core.get(entry,'outcome'),'flags')==[('hidden','list',''),('invalid_outcome','list','')]
    gui=(ROOT/'gui/journal_entry_widgets/chi_adm_memorials.gui').read_text()
    ui.check_model_structure(gui)
    assert gui.count('datamodel = "[AccessPlayer.GetSubjects]"')==3
    assert 'JournalEntry.GetCountry.GetSubjects' not in gui
    for expression in re.findall(r'"(\[[^"\n]*\])"',gui):
        assert expression.count("'")%2==0 and expression.count('(')==expression.count(')'),expression
    assert 'Var(\'chi_adm_memorials_audit_progress\')' in gui
    for key in re.findall(r"GetScriptedGui\('([^']+)'\)",gui):assert key in G,key
    loc=(ROOT/'localization/english/chi_adm_l_english.yml').read_text('utf-8-sig')
    keys=re.findall(r'^ (chi_adm_memorials_\w+):',loc,re.M)
    assert len(keys)==len(set(keys))
    refs=set(re.findall(r'(?:text|tooltip) = "(chi_adm_memorials_\w+)"',gui))
    for folder in ['scripted_effects','scripted_triggers','scripted_buttons','scripted_guis','journal_entries','customizable_localization']:
        body=core.definitions('common/'+folder+'/chi_adm_memorials.txt')
        source=(ROOT/'common'/folder/'chi_adm_memorials.txt').read_text()
        refs.update(re.findall(r'(?:name|desc|text|localization_key|conclusion_desc) = (chi_adm_memorials_\w+)',source))
    refs={x for x in refs if x in keys or not any(x==key for key in set(re.findall(r'name = (chi_adm_memorials_\w+)',(ROOT/'common/scripted_effects/chi_adm_memorials.txt').read_text())))}
    assert refs<=set(keys),refs-set(keys)
    for name,body in entries.items(): assert name in keys and name+'_reason' in keys and name+'_status' in keys
    for path in (ROOT/'localization/english').rglob('*.yml'):
        if path.name!='chi_adm_l_english.yml':assert not re.search(r'^ chi_adm_memorials_',path.read_text('utf-8-sig'),re.M)
    events=core.definitions('events/chi_adm_memorials.txt')
    province=events['chi_adm_memorials.2']
    assert core.get(province,'duration')=='30'
    options=[v for k,op,v in province if k=='option']
    assert len(options)==13
    for option in options[:-1]:
        assert core.get(option,'trigger') and core.get(option,'show_as_unavailable')
        assert len(core.get(option,'hidden_effect'))==1
        assert core.get(option,'hidden_effect')[0][0] in E
    assert {k for k,op,v in options[-1]}=={'name','default_option','ai_chance'}
    for key,event in events.items():
        if not isinstance(event,list):continue
        assert key=='chi_adm_memorials.2' or set(k for k,op,v in core.get(event,'option'))=={'name','default_option'}
    game=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game')
    native=(game/'common/modifier_type_definitions/00_modifier_types.txt').read_text('utf-8-sig')
    mods=core.definitions('common/static_modifiers/chi_adm_memorials.txt')
    for name,body in mods.items():
        for key,op,value in body:
            if key=='icon':assert (game/value).exists() or (ROOT/value).exists()
            else:assert key in native,key
    assert 'birth_rate' not in str(mods) and 'income_transfer' not in str(E)
    assert not any(x in str(E) for x in ['activate_law','annex','kill_character','start_enactment'])
    print('PASS memorials and audits static: provincial accounts-imperial law reform hashes, court register desk-only extension, four nested JEs, native GUI/loc/modifiers, no law/integration changes')

class Country:
    def __init__(self,tag):
        self.tag=tag;self.v={'chi_adm_loyalty':70,'chi_adm_autonomy':25,'chi_adm_corruption':25}
        self.mods={};self.treasury=100000;self.authority=100;self.war=False;self.bureau=.1
        self.journals=set();self.valid=True;self.ai=False;self.relations=80;self.centralised=True

class World:
    def __init__(self):
        self.court=Country('CHI');self.subjects=[Country(tag) for tag in core.TAGS]
        self.branch=0;self.events=[];self.expiries={}
    def n(self,s,c):
        if s.startswith('var:'):return c.v.get(s[4:],0)
        return float(s)
    def cond(self,items,c):
        for k,op,v in items:
            if k in ('OR','AND','NOT'):
                parts=(self.cond([x],c) for x in v)
                ok=any(parts) if k=='OR' else not all(parts) if k=='NOT' else all(parts)
            elif k=='chi_adm_memorials_valid':ok=(c.valid and self.court.valid)==(v=='yes')
            elif k=='chi_adm_memorials_centralised':ok=self.court.centralised==(v=='yes')
            elif k in T:ok=self.cond(T[k],c)==(v=='yes')
            elif k=='c:CHI':ok=self.cond(v,self.court) if isinstance(v,list) else c is self.court
            elif k=='any_subject_or_below':
                sub=[x for x in v if x[0]!='count'];num=sum(self.cond(sub,p) for p in self.subjects)
                cmp=next((x for x in v if x[0]=='count'),('count','>=','1'))
                ok=num>=float(cmp[2])
            elif k=='has_journal_entry':ok=v in c.journals
            elif k=='has_variable':ok=v in c.v
            elif k=='has_modifier':ok=v in c.mods
            elif k=='is_at_war':ok=c.war==(v=='yes')
            elif k=='is_ai':ok=c.ai==(v=='yes')
            elif k=='chi_adm_frontier':ok=(c.tag in core.FRONTIER)==(v=='yes')
            elif k=='hidden_trigger':ok=self.cond(v,c)
            elif k=='always':ok=v=='yes'
            else:
                a={'gold_reserves':c.treasury,'relative_bureaucracy':c.bureau,'authority':c.authority-25*('chi_adm_memorials_court_staff' in c.mods)}.get(k)
                if a is None:a=self.n(k,c)
                b=self.n(v,c)
                ok={'=':a==b,'>=':a>=b,'<=':a<=b,'>':a>b,'<':a<b}[op]
            if not ok:return False
        return True
    def run(self,items,c):
        taken=False
        for k,op,v in items:
            if k in ('if','else_if','else'):
                if k=='if':taken=False
                if not taken and (k=='else' or self.cond(core.get(v,'limit'),c)):
                    self.run([x for x in v if x[0]!='limit'],c);taken=True
            elif k in E:self.run(E[k],c)
            elif k.startswith('chi_adm_adjust_'):
                field='chi_adm_'+k.removeprefix('chi_adm_adjust_')
                c.v[field]=max(0,min(100,c.v[field]+self.n(core.get(v,'AMOUNT'),c)))
            elif k=='c:CHI':self.run(v,self.court)
            elif k=='set_variable':
                if isinstance(v,str):c.v[v]=1
                else:
                    name=core.get(v,'name');c.v[name]=self.n(next((x for a,b,x in v if a=='value'),'1'),c)
                    if any(a=='days' for a,b,x in v):self.expiries[(c.tag,name)]=float(core.get(v,'days'))
            elif k=='remove_variable':c.v.pop(v,None)
            elif k=='change_variable':
                name=core.get(v,'name')
                for a,b,x in v:
                    if a=='add':c.v[name]=c.v.get(name,0)+self.n(x,c)
                    elif a=='subtract':c.v[name]=c.v.get(name,0)-self.n(x,c)
            elif k=='add_modifier':c.mods[core.get(v,'name')]=float(next((x for a,b,x in v if a=='months'),'0'))
            elif k=='remove_modifier':c.mods.pop(v,None)
            elif k=='add_journal_entry':c.journals.add(core.get(v,'type'))
            elif k=='add_treasury':c.treasury+=self.n(v,c)
            elif k=='change_relations':c.relations+=float(core.get(v,'value'))
            elif k=='random_list':self.run([x for x in v[self.branch][2] if x[0]!='modifier'],c)
            elif k=='trigger_event':self.events.append((c.tag,core.get(v,'id')))
            elif k in ('save_scope_as','custom_tooltip','show_as_tooltip'):pass
            elif k=='hidden_effect':self.run(v,c)
            else:raise AssertionError('Unmodelled effect: '+k)
    def do(self,name,c):self.run(E['chi_adm_memorials_'+name],c)
    def tick(self,c,n=1):
        for _ in range(n):self.do('monthly',c)

def model():
    # Several memorials may share an already-active court staff commitment.
    w=World();total=w.court.treasury+sum(p.treasury for p in w.subjects)
    for p in w.subjects[:3]:w.do('file_relief',p)
    w.do('approve_memorial',w.subjects[0])
    assert 'chi_adm_memorials_court_staff' not in w.court.mods
    w.do('counter_memorial',w.subjects[1])
    w.do('approve_memorial',w.subjects[2])
    assert w.subjects[1].v['chi_adm_memorials_memorial_stage']==2
    assert w.subjects[0].treasury==120000 and w.subjects[2].treasury==120000
    assert w.court.treasury+sum(p.treasury for p in w.subjects)==total
    assert 'chi_adm_memorials_court_staff' not in w.court.mods
    w=World();p=w.subjects[0];w.do('file_relief',p);w.court.authority=24
    w.do('approve_memorial',p);assert p.treasury==120000
    w.court.mods['chi_adm_memorials_court_staff']=3
    w.do('approve_memorial',p);assert p.treasury==120000
    other=w.subjects[1];w.do('file_discretion',other)
    w.do('counter_memorial',other)
    assert other.v['chi_adm_memorials_memorial_stage']==2
    assert w.court.mods['chi_adm_memorials_court_staff']==3, 'Memorial refreshed unrelated court staff'
    # All 15 distinct offices participate; aid is a balanced, once-only transfer.
    for tag in core.TAGS:
        w=World();p=next(x for x in w.subjects if x.tag==tag)
        total=p.treasury+w.court.treasury
        w.do('file_relief',p);w.do('file_discretion',p)
        assert p.v['chi_adm_memorials_memorial']==1
        w.do('approve_memorial',p);w.do('approve_memorial',p)
        assert p.treasury==120000 and w.court.treasury==80000
        assert p.treasury+w.court.treasury==total
        w.do('file_relief',p);assert 'chi_adm_memorials_memorial' not in p.v
    w=World();p=w.subjects[0];w.do('file_relief',p);w.court.treasury=9999
    w.do('approve_memorial',p);w.do('counter_memorial',p)
    assert p.v['chi_adm_memorials_memorial_stage']==1 and p.treasury==100000
    w.court.treasury=15000;w.do('counter_memorial',p);assert p.v['chi_adm_memorials_memorial_stage']==2
    snap=json.loads(json.dumps(p.v));p.v=snap;w.do('accept_counter',p);w.do('accept_counter',p)
    assert p.treasury==110000 and w.court.treasury==5000
    w=World();p=w.subjects[0];w.do('file_discretion',p);w.tick(p,6)
    assert 'chi_adm_memorials_memorial' not in p.v and p.v['chi_adm_memorials_result']==21
    # Two-slot limit is derived from current live subject state, not a counter.
    w=World()
    for p in w.subjects[:3]:
        p.v['chi_adm_corruption']=50;w.court.mods.clear();w.do('send_supervision',p)
    assert sum('chi_adm_memorials_edict' in p.v for p in w.subjects)==2
    w.subjects[0].valid=False;w.do('send_supervision',w.subjects[2]);assert 'chi_adm_memorials_edict' in w.subjects[2].v
    p=w.subjects[1];before=copy.deepcopy(p.v);w.do('appeal_edict',p);w.do('appeal_edict',p)
    assert p.v['chi_adm_memorials_edict_stage']==2
    w.do('negotiate_edict',p);w.do('accept_edict',p);w.do('accept_edict',p)
    assert p.v['chi_adm_corruption']==before['chi_adm_corruption']-3
    w=World();p=w.subjects[0];w.do('send_honors',p);w.do('defy_edict',p);w.do('defy_edict',p)
    assert p.v['chi_adm_loyalty']==64 and 'chi_adm_memorials_honors' not in p.mods
    for tag in ('ZHI','MGL'):
        w=World();p=next(x for x in w.subjects if x.tag==tag);p.v['chi_adm_corruption']=70
        w.do('send_supervision',p);w.do('accept_edict',p)
        assert p.v['chi_adm_autonomy']==(24 if tag=='MGL' else 22)
    # Modes genuinely advance the actual effect AST at their advertised rates.
    for mode,length in [('cooperate',4),('obstruct',10),('conceal',5)]:
        for finding in (0,1):
            w=World();w.branch=finding;p=w.subjects[0];p.v['chi_adm_corruption']=80
            w.do('open_audit',p);w.do('open_audit',p)
            w.do('audit_'+mode,p);w.do('audit_'+mode,p)
            if mode=='conceal':assert p.treasury==95000
            w.tick(p,length-1);assert p.v['chi_adm_memorials_audit_progress']<100
            w.tick(p)
            if finding==0:
                assert p.v['chi_adm_memorials_audit']==3 and p.v['chi_adm_memorials_audit_progress']==100
                if mode=='conceal':
                    w.do('propose_restitution',p);total=p.treasury+w.court.treasury
                    w.do('pay_restitution',p);w.do('pay_restitution',p)
                    assert p.treasury+w.court.treasury==total and p.treasury==85000
                else:
                    w.do('propose_reform',p);w.do('accept_reform',p)
                    assert p.v['chi_adm_corruption']==70
            else:
                assert 'chi_adm_memorials_audit' not in p.v
                if mode=='conceal':assert p.mods['chi_adm_memorials_suspicion']==48
            assert 'chi_adm_memorials_audit_burden' not in p.mods
    w=World();p=w.subjects[0];w.do('open_audit',p);w.tick(p,3)
    assert p.v['chi_adm_memorials_audit_mode']==2
    # Invalidation clears obligations and outcome modifiers, retains cooldowns.
    for invalid in ('subject','court'):
        w=World();p=w.subjects[0];w.do('file_relief',p);w.do('open_audit',p)
        if invalid=='subject':p.valid=False
        else:w.court.valid=False
        w.tick(p);w.tick(p)
        assert 'chi_adm_memorials_memorial' not in p.v and 'chi_adm_memorials_audit' not in p.v
        assert 'chi_adm_memorials_audit_cooldown' in p.v
    # AI uses the same effects, costs and target/state checks.
    w=World();w.court.ai=True;p=w.subjects[0];w.do('file_relief',p);w.tick(p)
    assert p.treasury==120000 and 'chi_adm_memorials_court_staff' not in w.court.mods
    w=World();w.court.ai=True;p=w.subjects[0];p.v['chi_adm_corruption']=90
    w.do('ai_dispatch',p);assert p.v['chi_adm_memorials_audit']==1
    # Dynamic probability AST is bounded and both findings stay possible.
    weights=core.get(E['chi_adm_memorials_audit_finding'],'random_list')
    modifier=core.get(weights[0][2],'modifier')
    assert ('min','=','10') in modifier and ('max','=','150') in modifier
    def weight(c):
        value=50
        for k,op,v in modifier:
            terms=[x for x in v if x[0]!='limit'] if k=='if' and w.cond(core.get(v,'limit'),c) else []
            for operation,_,amount in terms:
                value+=float(amount)*(1 if operation=='add' else -1)
            if k=='min':value=max(value,float(v))
            if k=='max':value=min(value,float(v))
        return value
    p.war=False;p.bureau=.1;p.mods.clear();p.v.update(chi_adm_loyalty=70,chi_adm_corruption=10,chi_adm_memorials_audit_mode=1)
    assert weight(p)==10
    p.v['chi_adm_corruption']=80;assert weight(p)==110
    p.v['chi_adm_memorials_audit_mode']=3;assert weight(p)==60
    p.mods['chi_adm_memorials_suspicion']=48;assert weight(p)==100
    w=World();w.do('open_audit',w.subjects[0]);w.court.mods.clear()
    w.do('send_honors',w.subjects[1]);w.court.mods.clear();w.do('open_audit',w.subjects[2])
    assert 'chi_adm_memorials_audit' not in w.subjects[2].v
    # Lost/concluded response JE is explicitly restored before expiry.
    for result,kind in [(22,'edict'),(23,'audit')]:
        w=World();p=w.subjects[0]
        p.v.update({'chi_adm_memorials_result':result,'chi_adm_memorials_'+kind+'_cooldown':1})
        w.do('repair_delivery_once',p)
        assert 'chi_adm_memorials_'+kind+'_cooldown' not in p.v
        p.v.update({'chi_adm_memorials_result':result,'chi_adm_memorials_'+kind+'_cooldown':1})
        w.do('repair_delivery_once',p)
        assert 'chi_adm_memorials_'+kind+'_cooldown' in p.v
    w=World();p=w.subjects[0];w.do('send_honors',p)
    assert 'chi_adm_memorials_responses' in p.journals
    p.journals.clear();w.tick(p);assert 'chi_adm_memorials_responses' in p.journals
    p.journals.clear();p.v['chi_adm_memorials_edict_left']=1;w.tick(p)
    assert p.v['chi_adm_memorials_edict_left']==2 and 'chi_adm_memorials_edict' in p.v
    # AI fallback answers at the last review instead of expiring unanswered.
    p.ai=True;p.v['chi_adm_memorials_edict_left']=1;w.tick(p)
    assert p.v['chi_adm_memorials_result']==7 and 'chi_adm_memorials_edict' not in p.v
    w=World();p=w.subjects[0];p.ai=True;w.do('open_audit',p);p.v['chi_adm_memorials_audit_left']=1;w.tick(p)
    assert p.v['chi_adm_memorials_audit']==2 and p.v['chi_adm_memorials_audit_mode']==1
    # Human cases still require explicit acceptance.
    w=World();p=w.subjects[0];w.do('send_honors',p);w.tick(p)
    assert p.v['chi_adm_memorials_edict_stage']==1 and 'chi_adm_memorials_honors' not in p.mods
    print('PASS memorials and audits actual-effect model: 13 offices, balanced payments, consent/counters, cooldowns, two edicts, all audit modes/findings, frontier terms, timeouts, AI, scalar restore and cleanup')

def presentation():
    baseline=json.loads((ROOT/'tools/chi_adm_memorials_presentation_baseline.json').read_text())
    for path,digest in baseline['files'].items():
        assert (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest) or authorized_current(path),path
    norm=lambda x:json.loads(json.dumps(x))
    def canonical(items):
        out=[]
        for k,op,v in items:
            if k=='text' or (k=='always' and v=='yes'):continue
            if k in ('custom_tooltip','hidden_trigger','AND'):out.extend(canonical(v))
            elif k in T and v=='yes':out.extend(canonical(T[k]))
            elif k=='OR':out.append((k,op,tuple(canonical([child]) for child in v)))
            else:out.append((k,op,canonical(v) if isinstance(v,list) else v))
        return tuple(sorted(set(out),key=repr))
    def live_button(items):
        out=[]
        for k,op,v in items:
            if k=='effect':v=[x for x in v if x[0] not in ('custom_tooltip','show_as_tooltip')]
            if k=='possible':
                v=canonical(v)
            out.append((k,op,v))
        return norm(out)
    for name,old in baseline['buttons'].items():
        assert live_button(B[name])==live_button(old),name
        possible=core.get(B[name],'possible')
        assert sum(1 for k,_,v in possible if k=='custom_tooltip' and core.get(v,'text')=='chi_adm_memorials_case_requirements')<=1
        preview=core.get(core.get(B[name],'effect'),'show_as_tooltip')
        assert preview or name.endswith(('decline_counter','appeal_edict'))
    original=json.loads((ROOT/'tools/chi_adm_native_tooltip_baseline.json').read_text())['buttons']
    current=core.definitions('common/scripted_buttons/chi_adm_core.txt')
    for name,old in original.items():
        assert canonical(core.get(current[name],'possible'))==canonical(core.get(old,'possible'))
        assert 'chi_adm_req_service' not in str(core.get(current[name],'possible'))
        assert any(k=='hidden_trigger' for k,_,v in core.get(current[name],'possible'))
        assert norm([x for x in current[name] if x[0] not in ('possible','effect')])==[x for x in old if x[0] not in ('possible','effect')]
        assert norm(core.executable_effects(core.get(current[name],'effect')))==norm(core.executable_effects(core.get(old,'effect')))
        assert len([x for x in core.get(current[name],'effect') if x[0]=='add_modifier'])==1
        assert not any(k=='add_modifier' for k,_,v in core.get(core.get(current[name],'effect'),'hidden_effect'))
    for name in ('chi_adm_memorials_file_relief','chi_adm_memorials_file_discretion','chi_adm_memorials_file_military'):
        assert ('authority','>=','25') in core.get(B[name],'possible')
    for name,old in baseline['guis'].items():
        current=G[name]
        assert norm([x for x in current if x[0]!='effect'])==[x for x in old if x[0]!='effect'],name
        if any(k=='effect' for k,_,v in old):
            assert norm(core.get(core.get(current,'effect'),'hidden_effect'))==core.get(old,'effect'),name
            assert set(k for k,_,v in core.get(current,'effect'))=={'custom_tooltip','show_as_tooltip','hidden_effect'}
    # Presentation wrappers execute each live payment once, not once for the
    # preview and again for its helper. The native show_as_tooltip contract is
    # modeled as non-executing, matching installed effects documentation.
    w=World();p=w.subjects[0]
    preview=core.get(core.get(G['chi_adm_memorials_send_supervision'],'effect'),'show_as_tooltip')
    requirement_checks=[]
    for k,op,v in preview:
        if k=='custom_tooltip_no_bullet' and v=='chi_adm_memorials_effects_heading':break
        if k=='if':requirement_checks.append(core.get(v,'limit'))
    assert [('var:chi_adm_corruption','>=','40')] in requirement_checks
    assert not all(w.cond(check,p) for check in requirement_checks)
    p.v['chi_adm_corruption']=50
    assert all(w.cond(check,p) for check in requirement_checks)
    w.court.mods['chi_adm_memorials_court_staff']=6
    assert not all(w.cond(check,p) for check in requirement_checks)
    w=World();p=w.subjects[0]
    w.run(core.get(B['chi_adm_memorials_file_relief'],'effect'),p)
    assert p.treasury==100000 and w.court.treasury==100000
    w.run(core.get(G['chi_adm_memorials_approve_memorial'],'effect'),p)
    w.run(core.get(G['chi_adm_memorials_approve_memorial'],'effect'),p)
    assert p.treasury==120000 and w.court.treasury==80000
    gui=(ROOT/'gui/journal_entry_widgets/chi_adm_memorials.gui').read_text()
    for kind in ('loyalty','autonomy','corruption'):
        assert gui.count(f"value = \"[FixedPointToFloat(Country.MakeScope.Var('chi_adm_{kind}').GetValue)]\"")==4
        assert gui.count(f'text = "chi_adm_{kind}_tier_display"')==2
    for name in ('send_supervision','send_honors','send_emergency','approve_memorial','open_audit'):
        assert f"GetScriptedGui('chi_adm_memorials_{name}').ExecuteTooltip" in gui
    concepts=core.definitions('common/game_concepts/chi_adm.txt')
    assert set(concepts)=={'concept_chi_adm_'+x for x in ('loyalty','autonomy','corruption')}
    loc=(ROOT/'localization/english/chi_adm_l_english.yml').read_text('utf-8-sig')
    for key in concepts:
        assert len(re.findall(r'^ '+key+r':',loc,re.M))==1
        assert len(re.findall(r'^ '+key+r'_desc:',loc,re.M))==1
    game=Path(r'C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game')
    known=set(concepts)
    texticons=(ROOT/'gui/chi_adm_texticons.gui').read_text()
    for key,body in concepts.items():
        texture=core.get(body,'texture').strip('"')
        assert (game/texture).exists()
        assert texticons.count('icon = '+key.removeprefix('concept_'))==1
    for name in ('chi_adm_loyal_memorial','chi_adm_negotiate_discretion'):
        assert ('authority','>=','25') in core.get(core.definitions('common/scripted_buttons/chi_adm_core.txt')[name],'possible')
    for path in (game/'common/game_concepts').glob('*.txt'):
        known.update(re.findall(r'^(concept_\w+)\s*=',path.read_text('utf-8-sig'),re.M))
    relevant='\n'.join(x for x in loc.splitlines() if x.startswith((' chi_adm_memorials_',' concept_chi_adm_')))
    assert not re.search(r'\\n\?\s|\w\?s\b|\?\d',relevant), 'Corrupted bullet, apostrophe or currency marker'
    assert set(re.findall(r'\[(concept_\w+)\]',relevant))<=known
    assert '£' not in relevant and '@money!#v 20,000#!' in relevant
    for key in ('loyal_memorial','negotiate_discretion','supervise_offices'):
        result=re.search(r'^ chi_adm_'+key+r'_result:.*$',loc,re.M)[0]
        assert 'GetStaticModifier' not in result
    print('PASS memorials and audits presentation: live account bars, distinct concepts, native tooltip-only previews, money formatting and unchanged gameplay/eligibility/AI')

if __name__=='__main__':
    static();model();presentation()
    print('PENDING: Victoria 3 GUI, native random weights, actual monthly/expiry timing, save/load and two-human sessions.')
