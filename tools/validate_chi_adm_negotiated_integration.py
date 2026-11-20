from chi_adm_authorized_validation import authorized_current
"""Focused actual-AST negotiated integration checks. Does not execute Victoria 3 or render its GUI."""
from pathlib import Path
import copy,hashlib,json,re
import validate_chi_adm as c
ROOT=c.ROOT;GAME=Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game')
E=c.definitions('common/scripted_effects/chi_adm_negotiated_integration.txt')
T=c.definitions('common/scripted_triggers/chi_adm_negotiated_integration.txt')
V=c.definitions('common/script_values/chi_adm_negotiated_integration.txt')
P='chi_adm_negotiated_integration_'

def static():
    baseline=json.loads((ROOT/'tools/chi_adm_negotiated_integration_baseline.json').read_text('utf-8'))
    for path,digest in baseline['files'].items():
        assert (hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest) or authorized_current(path),path
    old={k:v for k,_,v in baseline['buttons'] if not k.startswith('chi_qing_integrate_')}
    buttons=c.definitions('common/scripted_buttons/tyrone_qing_administrations.txt')
    current={k:json.loads(json.dumps(v)) for k,v in buttons.items() if not k.startswith('chi_qing_integrate_')}
    assert old==current,'Unrelated/warlord buttons changed'
    for tag in c.TAGS:
        fx=c.get(buttons['chi_qing_integrate_'+tag],'effect')
        assert fx==c.parse('c:'+tag+' = { chi_adm_negotiated_integration_propose = yes }')
    ledger=(ROOT/'gui/journal_entry_widgets/chi_adm_court_register_ledger.gui').read_text('utf-8')
    line='\n    textbox = { size = { 488 0 } max_width = 488 autoresize = yes multiline = yes text = "chi_adm_negotiated_integration_ledger_display" }'
    assert ledger.count(line)==1 and ledger.replace(line,'')==baseline['ledger']
    owned=[]
    for base in ('common','events','gui'):
        for path in (ROOT/base).rglob('chi_adm_negotiated_integration.*'):
            if path.suffix in ('.txt','.gui'):
                source=path.read_text('utf-8-sig')
                if path.suffix=='.gui':
                    depth=0
                    for token in re.findall(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',source):
                        if token=='{':depth+=1
                        elif token=='}':depth-=1
                        assert depth>=0,path
                    assert depth==0,path
                else:c.parse(source)
                owned.append(path)
    alltext='\n'.join(path.read_text('utf-8-sig') for path in owned)
    assert 'add_treasury' not in alltext and 'activate_law' not in alltext and 'on_daily_pulse' not in alltext
    assert 'play_as' not in alltext and 'birth_rate' not in alltext
    entries=c.definitions('common/journal_entries/chi_adm_negotiated_integration.txt');assert len(entries)==2
    events=c.definitions('events/chi_adm_negotiated_integration.txt');assert len(events)==9 # namespace, seven decisions, one calendar clock
    for key,body in events.items():
        if key=='namespace':continue
        if key=='chi_adm_negotiated_integration.8':
            assert c.get(body,'hidden')=='yes'
            assert 'chi_adm_negotiated_integration_clock_revision' in str(c.get(body,'trigger'))
            continue
        assert c.get(body,'cancellation_trigger') and c.get(body,'trigger')
        options=[v for k,_,v in body if k=='option']
        assert sum(any(k=='default_option' and v=='yes' for k,_,v in opt) for opt in options)==1
        assert c.get(options[-1],'name')==P+'read_later'
        for opt in options[:-1]:assert 'chi_adm_negotiated_integration_event_current' in str(c.get(opt,'trigger'))
    mods=c.definitions('common/static_modifiers/chi_adm_negotiated_integration.txt')
    for body in mods.values():assert (GAME/c.get(body,'icon')).is_file()
    assert c.get(mods[P+'commitment'],'country_authority_mult')=='-0.10'
    assert c.get(mods[P+'commitment'],'country_bureaucracy_mult')=='-0.10'
    pacts=c.definitions('common/diplomatic_actions/chi_adm_negotiated_integration.txt')
    for key,rate,direction in [('subsidy','0.10','yes'),('subsidy_strong','0.20','yes'),('repayment','0.10','no'),('repayment_half','0.05','no')]:
        pact=c.get(pacts[P+key],'pact')
        assert c.get(pact,'income_transfer')==rate
        assert c.get(pact,'second_country_gets_income_transfer')==direction
        assert c.get(pact,'income_transfer_based_on_second_country')=='yes'
        assert not any(k in ('subject_type','has_junior_participant') for k,_,v in pact)
    native=c.parse((GAME/'common/war_goal_types/00_annex_country.txt').read_text('utf-8-sig'))[0][2]
    war=c.definitions('common/war_goal_types/chi_adm_negotiated_integration.txt')[P+'annexation']
    expected=copy.deepcopy(native);c.get(expected,'infamy').append(('multiply','=','0.25'))
    assert expected==war,'Coercive war goal must preserve native infamy and annexation behavior'
    gui=(ROOT/'gui/journal_entry_widgets/chi_adm_negotiated_integration.gui').read_text('utf-8')
    assert 'GetScriptedButtons' not in gui
    assert 'max_width = 440 autoresize = yes multiline = yes' in gui
    guis=c.definitions('common/scripted_guis/chi_adm_negotiated_integration.txt')
    for name in re.findall(r"GetScriptedGui\('([^']+)'\)",gui):assert name in guis,name
    for panel in gui.split('name = "chi_adm_negotiated_integration_')[1:]:
        clicks=re.findall(r"onclick = .*GetScriptedGui\('([^']+)'\)",panel)
        assert len(clicks)==len(set(clicks)),'Duplicate action rendering'
    loc=(ROOT/'localization/english/chi_adm_l_english.yml').read_text('utf-8-sig')
    keys=re.findall(r'^ ([\w.]+):',loc,re.M);assert len(keys)==len(set(keys))
    for key in re.findall(r'(?:text|title|desc|flavor|name|conclusion_desc|custom_tooltip_no_bullet|localization_key)\s*=\s*"?(chi_adm_negotiated_integration_\w+)',alltext):
        if key not in E and key not in guis and key not in V and not re.search(r'(?:set_variable|change_variable|save_scope_value_as)\s*=\s*\{\s*name\s*=\s*'+key+r'\b',alltext):assert key in keys,key
    assert (ROOT/'localization/english/chi_adm_l_english.yml').read_bytes().startswith(b'\xef\xbb\xbf')
    print('PASS negotiated integration static: all 13 proposal entry points, unchanged provincial accounts-memorials and audits and warlord content, two nested JEs, seven guarded events, four native payment pacts, quarter-native Infamy, GUI/loc/icons')

class Entity:
    def __init__(self,tag,kind='country'):
        self.tag=tag;self.kind=kind;self.v={};self.mods={};self.journals=set();self.alive=True;self.subject=tag!='CHI';self.ai=True
        self.authority=100;self.bureau=.5;self.war=False;self.enemy=False;self.play=False;self.liberty=0;self.relations=80;self.court=True
        self.tech=True;self.central=True;self.states=[];self.governor=None;self.transferred=False
        if kind=='country' and tag!='CHI':
            self.v.update(chi_adm_loyalty=70,chi_adm_autonomy=25,chi_adm_corruption=25)
            self.governor=Entity(tag+'_governor','character');self.states=[Entity(tag+'_state','state')]

class World:
    def __init__(self):
        self.countries={tag:Entity(tag) for tag in ['CHI']+c.TAGS};self.court=self.countries['CHI'];self.scopes={};self.events=[];self.scheduled=[];self.pacts=set();self.plays=[];self.expiry={};self.month=0
    def target(self,key,current):
        if key.startswith('c:'):return self.countries.get(key[2:])
        if key.startswith('scope:'):return self.scopes.get(key[6:])
        if key=='ruler':return current.governor
        raise AssertionError(key)
    def n(self,value,current):
        if isinstance(value,list):return self.value(value,current)
        if value in ('prestige','army_power_projection','gdp'):return current.v.get(value,100)
        if value.startswith('c:CHI.') and value[6:] in ('prestige','army_power_projection','gdp'):return self.countries['CHI'].v.get(value[6:],100)
        if value.startswith('var:'):return current.v.get(value[4:],0)
        if value.startswith('scope:'):return self.scopes[value[6:]]
        if value in V:return self.value(V[value],current)
        if value=='yes':return 1
        if value=='no':return 0
        return float(value)
    def value(self,block,current,start=0):
        total=start;taken=False
        for key,_,val in block:
            if key=='c:CHI':total=self.value(val,self.court,total)
            elif key=='if':
                if self.cond(c.get(val,'limit'),current):total=self.value([x for x in val if x[0]!='limit'],current,total)
            else:
                n=self.n(val,current)
                if key=='value':total=n
                elif key=='add':total+=n
                elif key=='subtract':total-=n
                elif key=='multiply':total*=n
                elif key=='divide':total/=n
                elif key=='min':total=max(total,n)
                elif key=='max':total=min(total,n)
                else:raise AssertionError('value '+key)
        return total
    def cond(self,block,current):
        for key,op,val in block:
            if key in ('OR','AND','NOT'):
                parts=[self.cond([x],current) for x in val];ok=any(parts) if key=='OR' else not all(parts) if key=='NOT' else all(parts)
            elif key in T:ok=self.cond(T[key],current)==(val=='yes')
            elif key in ('chi_adm_target_valid','chi_adm_eligible'):
                ok=(current.tag in c.TAGS and current.alive and current.subject and self.court.alive and self.court.court)==(val=='yes')
            elif key=='chi_adm_court_valid':ok=(self.court.alive and self.court.court)==(val=='yes')
            elif key=='chi_adm_frontier':ok=(current.tag in c.FRONTIER)==(val=='yes')
            elif key.startswith(('c:','scope:')):
                target=self.target(key,current)
                ok=bool(target) and (self.cond(val,target) if isinstance(val,list) else target is current)
            elif key=='exists':
                target=self.target(val,current);ok=target is not None and (not isinstance(target,Entity) or target.alive)
            elif key=='this':ok=current is self.target(val,current)
            elif key=='has_variable':ok=val in current.v
            elif key=='has_modifier':ok=val in current.mods
            elif key=='has_journal_entry':ok=val in current.journals
            elif key=='is_ai':ok=current.ai==(val=='yes')
            elif key=='is_at_war':ok=current.war==(val=='yes')
            elif key=='is_diplomatic_play_committed_participant':ok=current.play==(val=='yes')
            elif key in ('has_war_with','is_diplomatic_play_enemy_of'):ok=current.enemy
            elif key=='has_technology_researched':ok=current.tech
            elif key=='always':ok=val=='yes'
            else:
                left={'authority':current.authority,'relative_bureaucracy':current.bureau,'liberty_desire':current.liberty,'relations:c:CHI':current.relations}.get(key)
                if left is None:left=self.n(key,current)
                right=self.n(val,current);ok={'=':left==right,'>=':left>=right,'<=':left<=right,'>':left>right,'<':left<right}[op]
            if not ok:return False
        return True
    def run(self,block,current):
        taken=False
        for key,op,val in block:
            if key in ('if','else_if','else'):
                if key=='if':taken=False
                if not taken and (key=='else' or self.cond(c.get(val,'limit'),current)):
                    self.run([x for x in val if x[0]!='limit'],current);taken=True
            elif key in E:self.run(E[key],current)
            elif key.startswith('chi_adm_adjust_'):
                field='chi_adm_'+key.removeprefix('chi_adm_adjust_');current.v[field]=max(0,min(100,current.v[field]+self.n(c.get(val,'AMOUNT'),current)))
            elif key in ('chi_adm_memorials_cleanup','chi_adm_imperial_law_clear'):pass # protected earlier helpers, independently validated
            elif key.startswith(('c:','scope:')) or key=='ruler':
                target=self.target(key,current)
                if target is not None and target.alive:self.run(val,target)
            elif key in ('every_subject_or_below','every_scope_state'):
                items=[x for x in self.countries.values() if x.subject and x.alive] if key=='every_subject_or_below' else current.states
                for target in items:
                    limit=next((v for k,_,v in val if k=='limit'),[])
                    if self.cond(limit,target):self.run([x for x in val if x[0]!='limit'],target)
            elif key=='set_variable':
                if isinstance(val,str):current.v[val]=1
                else:
                    name=c.get(val,'name');current.v[name]=self.n(c.get(val,'value'),current)
                    if any(k=='months' for k,_,v in val):self.expiry[(current.tag,name)]=self.month+self.n(c.get(val,'months'),current)
            elif key=='remove_variable':current.v.pop(val,None)
            elif key=='change_variable':
                name=c.get(val,'name')
                for k,_,v in val:
                    if k=='add':current.v[name]=current.v.get(name,0)+self.n(v,current)
                    elif k=='subtract':current.v[name]=current.v.get(name,0)-self.n(v,current)
            elif key=='save_scope_as':self.scopes[val]=current
            elif key=='save_scope_value_as':self.scopes[c.get(val,'name')]=self.n(c.get(val,'value'),current)
            elif key=='trigger_event':
                record=(c.get(val,'id'),current.tag,dict(self.scopes));self.events.append(record)
                if any(k=='months' for k,_,v in val):self.scheduled.append((self.month+self.n(c.get(val,'months'),current),record))
            elif key=='add_journal_entry':current.journals.add(c.get(val,'type'))
            elif key=='change_relations':current.relations+=self.n(c.get(val,'value'),current)
            elif key in ('create_diplomatic_pact','remove_diplomatic_pact'):
                other=self.target(c.get(val,'country'),current);pact=(current.tag,other.tag,c.get(val,'type'))
                if key=='create_diplomatic_pact':self.pacts.add(pact)
                else:self.pacts.discard(pact)
            elif key=='remove_modifier':current.mods.pop(val,None)
            elif key=='add_modifier':current.mods[c.get(val,'name')]=self.n(next((v for k,_,v in val if k=='multiplier'),'1'),current)
            elif key=='transfer_character':current.transferred=True
            elif key=='remove_character_role':pass
            elif key=='annex':
                target=self.target(val,current);assert target.alive
                target.alive=False;target.subject=False;current.states.extend(target.states);target.states=[]
            elif key=='create_diplomatic_play':self.plays.append((current.tag,self.target(c.get(val,'target_country'),current).tag))
            else:raise AssertionError('effect '+key)
    def do(self,key,country):self.run(E[P+key],country)
    def tick(self,n=1):
        for _ in range(n):
            self.month+=1
            for (tag,key),until in list(self.expiry.items()):
                if until<=self.month:self.countries[tag].v.pop(key,None);del self.expiry[(tag,key)]
            self.do('court_tick',self.court)
            due=[x for x in self.scheduled if x[0]<=self.month]
            self.scheduled=[x for x in self.scheduled if x[0]>self.month]
            event=c.definitions('events/chi_adm_negotiated_integration.txt')['chi_adm_negotiated_integration.8']
            for _,(key,tag,scopes) in due:
                if key!='chi_adm_negotiated_integration.8':continue
                self.scopes=scopes;country=self.countries[tag]
                if country.alive and self.cond(c.get(event,'trigger'),country):self.run(c.get(event,'immediate'),country)
    def start(self,tag='ZHI',human=False):
        p=self.countries[tag];p.ai=not human;self.court.v['chi_qing_centralisation_unlocked']=1
        self.do('propose',p);self.do('begin',p);return p

def model():
    # No unrelated country can enter; calendar work does not advance on a maintenance pulse.
    w=World()
    for tag in ('TIB','KOR','LAN'):
        p=Entity(tag);w.do('propose',p);assert P+'stage' not in p.v
    p=w.start();w.do('court_tick',w.court);w.do('court_tick',w.court)
    assert p.v[P+'elapsed']==0
    # Every administration uses the same genuine negotiation and six-review implementation.
    for tag in c.TAGS:
        w=World();p=w.start(tag);assert p.v[P+'stage']==3
        w.tick(2);assert p.v[P+'stage']==3 and p.alive
        w.tick();assert p.v[P+'stage']==4
        state=p.states[0];governor=p.governor
        w.tick(3);assert not p.alive and governor.transferred
        assert state in w.court.states and w.court.v[P+'count']==0
        assert P+'stage' not in p.v
    # Dynamic totals change, not elapsed time: 3/6 becomes 3/9, then 3/12.
    w=World();p=w.start();w.tick(3);q=w.start('AHU');assert p.v[P+'elapsed']==3
    assert w.n(P+'required',p)==9
    r=w.start('HNA');assert w.n(P+'required',p)==12
    w.do('ask_suspend',r);w.do('suspend',r)
    assert w.n(P+'required',p)==9 and r.v[P+'elapsed']==0
    w.do('resume',r);assert w.n(P+'required',p)==12
    # Each due calendar review sees the live count after earlier completions.
    w.tick(9);assert not p.alive and not q.alive and not r.alive
    # Human agreement never authorizes early or inferred final annexation; no AI-control gate.
    w=World();p=w.start(human=True);w.do('final_yes',p);assert p.alive
    w.tick(6);assert p.alive and p.v[P+'stage']==5
    w.tick(3);assert p.alive
    w.do('final_yes',p);assert not p.alive and not p.ai
    # Final refusal gives the court both a hold route and a provincial-breach route.
    w=World();p=w.start(human=True);w.tick(6);w.do('final_no',p)
    assert p.alive and p.v[P+'stage']==6
    w.do('hold',p);assert p.v[P+'stage']==5
    w.do('final_no',p);w.do('cancel_provincial',p);assert P+'stage' not in p.v
    # Negotiation, closer centralization, one pressure attempt, one improved final offer.
    w=World();p=w.countries['SHN'];w.court.v['chi_qing_centralisation_unlocked']=1
    w.do('propose',p);w.do('centralize',p);w.do('central_settlement',p)
    assert p.alive and p.v['chi_adm_autonomy']==20 and P+'retry' in p.v
    w.do('propose',p);assert P+'stage' not in p.v
    w.tick(12);w.do('propose',p);assert p.v[P+'stage']==1
    stale=copy.copy(w.events[-1][2]);w.do('refuse',p);w.do('pressure',p)
    loyalty=p.v['chi_adm_loyalty'];w.do('refuse',p);w.do('pressure',p)
    assert p.v['chi_adm_loyalty']==loyalty and p.v[P+'stage']==2
    w.do('offer_subsidy',p);assert p.v[P+'final_offer']==1 and not w.pacts
    w.do('refuse',p);w.do('offer_protection',p);assert p.v[P+'protection']==1
    w.scopes=stale;assert not w.cond(T[P+'event_current'],p)
    # Weekly payment agreement starts only at acceptance and is idempotent.
    w=World();p=w.countries['ZHI'];w.court.v['chi_qing_centralisation_unlocked']=1
    w.do('propose',p);w.do('request_subsidy',p);w.do('offer_subsidy',p)
    assert not w.pacts
    w.do('begin',p);w.do('begin',p)
    assert w.pacts=={('CHI','ZHI',P+'subsidy')} and p.v[P+'elapsed']==0
    w.do('ask_suspend',p);w.do('suspend',p);assert not w.pacts and w.court.v[P+'count']==0
    w.tick(2);assert p.v[P+'elapsed']==0
    w.do('resume',p);assert len(w.pacts)==1 and w.court.v[P+'count']==1
    # Deficits block new starts, never ongoing work; peace gates only initial proposal.
    w.court.authority=-1;w.court.bureau=-.2
    q=w.countries['AHU'];w.do('propose',q);assert P+'stage' not in q.v
    p.war=True;w.tick();assert p.v[P+'elapsed']==1
    # Qing breach permits withdrawal without a repayment claim.
    w.do('ask_suspend',p);w.do('refuse_suspend',p);w.do('force_suspend',p)
    assert P+'breach' in p.v and not w.pacts
    w.do('withdraw_breach',p);assert P+'stage' not in p.v and P+'repayment_left' not in p.v
    # Cancellation and repayment remain consent-based and timed, including counteroffers.
    w=World();p=w.countries['ZHI'];w.court.v['chi_qing_centralisation_unlocked']=1
    w.do('propose',p);w.do('offer_subsidy',p);w.do('begin',p)
    w.do('ask_cancel',p);w.do('cancel_mutual',p)
    assert p.v[P+'stage']==9 and not w.pacts
    w.do('propose_repayment',p);assert not w.pacts
    w.do('repay_compromise',p);assert not w.pacts
    w.do('accept_repay_compromise',p);assert w.pacts=={('CHI','ZHI',P+'repayment_half')}
    w.tick(6);assert not w.pacts and P+'repayment_left' not in p.v
    # Protected territory actually decays from -10%/-20% to zero, including state transfer.
    for strength,total in [(1,60),(2,60)]:
        w=World();p=w.start();p.v[P+'protection']=strength;state=p.states[0]
        w.tick(6);assert state.mods[P+'local_privileges']==strength
        for _ in range(total):
            state.v[P+'tax_left']-=1;w.do('update_tax',state)
        assert P+'local_privileges' not in state.mods and not state.v
    # Independence, collapse and hostile war invalidate safely; unrelated wars do not.
    for broken in ('subject','court','enemy'):
        w=World();p=w.start()
        if broken=='subject':p.subject=False
        elif broken=='court':w.court.court=False
        else:p.enemy=True
        w.tick();assert p.alive and P+'stage' not in p.v and w.court.v[P+'count']==0
    # Coercion starts a real play, with varied other-subject reactions and no governor transfer.
    w=World();p=w.countries['ZHI'];w.court.v['chi_qing_centralisation_unlocked']=1
    q=w.countries['AHU'];q.v['chi_adm_loyalty']=30
    r=w.countries['HNA'];r.v.update(chi_adm_loyalty=90,chi_adm_autonomy=10)
    w.do('propose',p);w.do('refuse',p);w.do('coerce',p)
    assert w.plays==[('CHI','ZHI')] and p.alive and not p.governor.transferred
    assert q.v['chi_adm_loyalty']==22 and r.v['chi_adm_loyalty']==90
    # AI acceptance is genuinely responsive to all four factors in the actual event AST.
    options=[v for k,_,v in c.definitions('events/chi_adm_negotiated_integration.txt')['chi_adm_negotiated_integration.1'] if k=='option']
    chance=c.get(next(o for o in options if c.get(o,'name')==P+'begin'),'ai_chance')
    def weight(country):
        result=float(c.get(chance,'base'))
        for key,_,body in chance:
            if key=='modifier' and w.cond(c.get(body,'trigger'),country):result*=float(c.get(body,'factor'))
        return result
    w=World();p=w.countries['ZHI'];high=weight(p)
    p.v['chi_adm_loyalty']=20;assert weight(p)<high
    p.v['chi_adm_loyalty']=70;p.v['chi_adm_autonomy']=80;assert weight(p)<high
    p.v['chi_adm_autonomy']=25;p.v['chi_adm_corruption']=80;assert weight(p)<high
    p.v['chi_adm_corruption']=25;p.relations=-20;assert weight(p)<high
    # Saving scalar state preserves elapsed time and terms; loading must not advance timers.
    w=World();p=w.start();w.tick(3)
    restored=json.loads(json.dumps(p.v));p.v=restored;w.do('recount',w.court)
    assert p.v[P+'elapsed']==3 and w.n(P+'required',p)==6
    print('PASS negotiated integration actual-effect model: 13 offices; six-review stages and dynamic concurrency; human final consent while player-controlled; negotiation/pressure/refusal; payments/suspension/repayment; decay, war/collapse cleanup and persisted scalars')

if __name__=='__main__':
    static();model()
    print('PENDING: Victoria 3 runtime, payment formula/weekly debit-credit, annexation player handling, governor roster survival, native peace settlement, GUI at 1080p and save/load.')

