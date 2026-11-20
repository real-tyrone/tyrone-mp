"""Generate comprehensive imperial law reform mapping from installed laws overlaid by this mod.

Run after changing laws; IDs are append-only. --check detects stale generated files.
Native enactability remains authoritative; this is not an enactment simulator.
"""
from pathlib import Path
import json
import re
import sys
sys.dont_write_bytecode = True
import validate_chi_adm as core

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r'C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game')
CHECK = '--check' in sys.argv

def emit(items, indent=0):
    rows = []
    for k, op, v in items:
        if op == 'list':
            rows.append(' '*indent+k)
        elif isinstance(v, list):
            rows.append(' '*indent+k+' '+op+' {\n'+emit(v, indent+1)+'\n'+' '*indent+'}')
        else:
            rows.append(' '*indent+k+' '+op+' '+v)
    return '\n'.join(rows)

def write(path, text):
    p = ROOT/path
    old = p.read_text('utf-8-sig') if p.exists() else ''
    if CHECK:
        if str(path).endswith('.yml'):
            # later features append English sections; ordering is not semantic.
            entries = lambda source: dict(re.findall(r'^\s*(\w+):\s*(.*)$', source, re.M))
            assert entries(old) == entries(text), f'Stale generated localization: {path}; run generator'
        else:
            assert old == text, f'Stale generated file: {path}; run generator'
    elif old != text:
        p.write_text(text, encoding='utf-8-sig' if path.endswith('.yml') else 'utf-8')

def replace(path, name, body):
    p = ROOT/path
    text = p.read_text('utf-8-sig')
    parsed = core.parse(text)
    defs = {k:v for k, _, v in parsed}
    defs[name] = core.parse(body)
    # These imperial law reform mapping files contain ordinary definition blocks only.
    write(path, emit([(k,'=',v) for k,v in defs.items()])+'\n')

def discover():
    files = {p.name:p for p in (GAME/'common/laws').glob('*.txt')}
    files.update({p.name:p for p in (ROOT/'common/laws').glob('*.txt')})
    effective = {}
    replacements = {}
    for name,p in sorted(files.items()):
        for key,op,body in core.parse(p.read_text('utf-8-sig')):
            if not isinstance(body,list):
                continue
            law = key.removeprefix('REPLACE:')
            if not law.startswith('law_'):
                continue
            record = (p,body)
            (replacements if key.startswith('REPLACE:') else effective)[law] = record
    effective.update(replacements)
    return effective

def main():
    effective = discover()
    previous = json.loads((ROOT/'tools/chi_adm_imperial_law_catalog.json').read_text())
    allocation = ROOT/'tools/chi_adm_imperial_law_ids.json'
    ids = json.loads(allocation.read_text()) if allocation.exists() else {x['law']:x['id'] for x in previous}
    next_id = max(ids.values(), default=0)+1
    for law in sorted(effective):
        if law not in ids:
            ids[law] = next_id
            next_id += 1
    write('tools/chi_adm_imperial_law_ids.json', json.dumps(ids,indent=2,sort_keys=True)+'\n')
    rows = []
    for law,(path,body) in effective.items():
        group = core.get(body,'group')
        rows.append(dict(id=ids[law], law=law, group=group))
    rows.sort(key=lambda x:x['id'])
    write('tools/chi_adm_imperial_law_catalog.json', json.dumps(rows,indent=2)+'\n')
    groups = {g:i+1 for i,g in enumerate(sorted({x['group'] for x in rows}))}
    tp = 'common/scripted_triggers/chi_adm_imperial_law.txt'
    replace(tp,'chi_adm_imperial_law_civil','''exists = c:CHI
chi_qing_administration_tag = yes
chi_qing_administrative_subject = yes
is_direct_subject_of = c:CHI
c:CHI = { has_variable = chi_qing_1836_setup NOT = { has_variable = tyr_chi_fragmented } }''')
    replace(tp,'chi_adm_imperial_law_supported_law','OR = { '+' '.join('type = law_type:'+x['law'] for x in rows)+' }')
    replace(tp,'chi_adm_imperial_law_supported_type','OR = { '+' '.join('this = law_type:'+x['law'] for x in rows)+' }')
    replace(tp,'chi_adm_imperial_law_court_still_requests','exists = c:CHI\nOR = {\n'+'\n'.join(f"AND = {{ var:chi_adm_imperial_law_law_id = {x['id']} c:CHI = {{ has_law = law_type:{x['law']} }} }}" for x in rows)+'\n}')
    replace(tp,'chi_adm_imperial_law_matches_request','OR = {\n'+'\n'.join(f"AND = {{ owner = {{ var:chi_adm_imperial_law_law_id = {x['id']} }} type = law_type:{x['law']} }}" for x in rows)+'\n}')
    replace(tp,'chi_adm_imperial_law_adopted','OR = {\n'+'\n'.join(f"AND = {{ var:chi_adm_imperial_law_law_id = {x['id']} has_law = law_type:{x['law']} }}" for x in rows)+'\n}')
    replace(tp,'chi_adm_imperial_law_government_support','OR = {\n'+'\n'.join(f"AND = {{ var:chi_adm_imperial_law_law_id = {x['id']} any_interest_group = {{ is_in_government = yes law_stance = {{ law = law_type:{x['law']} value > neutral }} }} }}" for x in rows)+'\n}')
    ep = 'common/scripted_effects/chi_adm_imperial_law.txt'
    replace(ep,'chi_adm_imperial_law_dispatch','\n'.join(f'''if = {{ limit = {{ type = law_type:{x['law']} }} owner = {{ every_subject_or_below = {{ limit = {{ chi_adm_imperial_law_civil = yes NOT = {{ has_law = law_type:{x['law']} }} NOT = {{ exists = imposed_law }} NOT = {{ has_journal_entry = je_law_imposition }} }} chi_adm_imperial_law_receive = {{ ID = {x['id']} }} }} }} }}''' for x in rows))
    replace(ep,'chi_adm_imperial_law_advance_backlog','''if = { limit = { has_variable = chi_adm_imperial_law_backlog_id chi_adm_imperial_law_civil = yes }
set_variable = { name = chi_adm_imperial_law_next_id value = var:chi_adm_imperial_law_backlog_id }
remove_variable = chi_adm_imperial_law_backlog_id
'''+ '\n'.join(f"if = {{ limit = {{ var:chi_adm_imperial_law_next_id = {x['id']} }} chi_adm_imperial_law_receive = {{ ID = {x['id']} }} }}" for x in rows)+ '\nremove_variable = chi_adm_imperial_law_next_id\n}')
    replace(ep,'chi_adm_imperial_law_schedule_implementation','\n'.join(f"if = {{ limit = {{ var:chi_adm_imperial_law_law_id = {x['id']} }} trigger_event = {{ id = chi_adm_imperial_law_law.{1000+x['id']} months = 12 popup = no }} }}" for x in rows))
    write('events/chi_adm_imperial_law_implementation.txt','namespace = chi_adm_imperial_law_law\n'+'\n'.join(f"chi_adm_imperial_law_law.{1000+x['id']} = {{ type = country_event hidden = yes trigger = {{ chi_adm_imperial_law_valid = yes var:chi_adm_imperial_law_status = 3 var:chi_adm_imperial_law_law_id = {x['id']} NOT = {{ has_variable = chi_adm_imperial_law_implementation_wait }} }} immediate = {{ chi_adm_imperial_law_finish_implementation = yes }} }}" for x in rows)+'\n')
    replace(ep,'chi_adm_imperial_law_set_incoming_group','\n'.join(f"if = {{ limit = {{ $ID$ = {x['id']} }} set_variable = {{ name = chi_adm_imperial_law_incoming_group value = {groups[x['group']]} }} }}" for x in rows))
    replace(ep,'chi_adm_imperial_law_set_current_group','\n'.join(f"if = {{ limit = {{ var:chi_adm_imperial_law_law_id = {x['id']} }} set_variable = {{ name = chi_adm_imperial_law_law_group value = {groups[x['group']]} }} }}" for x in rows))
    ap = 'common/on_actions/chi_adm_imperial_law.txt'
    replace(ap,'chi_adm_imperial_law_native_route','trigger = { chi_adm_imperial_law_native_request = yes }\neffect = { set_variable = { name = chi_adm_imperial_law_native_redirected days = 3 } imposed_law = { save_scope_as = chi_adm_imperial_law_native_law cancel_imposition = yes }\n'+'\n'.join(f"if = {{ limit = {{ scope:chi_adm_imperial_law_native_law = {{ type = law_type:{x['law']} }} }} chi_adm_imperial_law_receive = {{ ID = {x['id']} }} }}" for x in rows)+'\n}')
    cp = 'common/customizable_localization/chi_adm_imperial_law.txt'
    for name,var,key in [('requested_name','law_id','requested_name'),('group_name','law_id','group_name'),('current_name','law_id','current_name'),('backlog_name','backlog_id','requested_name'),('selected_name','selected_id','requested_name'),('requested_icon','law_id','requested_icon')]:
        replace(cp,'chi_adm_imperial_law_'+name,'type = country\n'+'\n'.join(f"text = {{ trigger = {{ var:chi_adm_imperial_law_{var} = {x['id']} }} localization_key = chi_adm_imperial_law_{key}_{x['id']} }}" for x in rows)+'\ntext = { trigger = { always = yes } localization_key = chi_adm_imperial_law_no_record }')
    # GUI-only lookup: resolve real native texture paths, never nested localized
    # getter expressions. Current icon follows live law state in the request group.
    icon_triggers = []
    for group,gid in groups.items():
        icon_triggers.append(('chi_adm_imperial_law_icon_group_'+str(gid),'=',core.parse('OR = { '+' '.join(f"var:chi_adm_imperial_law_law_id = {x['id']}" for x in rows if x['group']==group)+' }')))
    write('common/scripted_triggers/chi_adm_imperial_law_icons.txt',emit(icon_triggers)+'\n')
    # Bind textures directly to native objects. Localized strings are text, not
    # a verified image-resource transport in the JE context (runtime failure).
    icon_guis = []
    requested_icons = []
    current_icons = []
    for x in rows:
        name = f"chi_adm_imperial_law_requested_icon_{x['id']}_gui"
        icon_guis.append((name,'=',core.parse(f"scope = country is_valid = {{ var:chi_adm_imperial_law_law_id = {x['id']} }}")))
        requested_icons.append(f'''icon = {{ size = {{ 48 48 }} parentanchor = center
visible = "[GetScriptedGui('{name}').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
texture = "[GetLawType('{x['law']}').GetTexture]" }}''')
    for group,gid in groups.items():
        name = f'chi_adm_imperial_law_current_icon_{gid}_gui'
        icon_guis.append((name,'=',core.parse(f'scope = country is_valid = {{ chi_adm_imperial_law_icon_group_{gid} = yes }}')))
        current_icons.append(f'''icon = {{ size = {{ 48 48 }} parentanchor = center
visible = "[GetScriptedGui('{name}').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
texture = "[Country.GetActiveLawFromGroup('{group}').GetTexture]" }}''')
    write('common/scripted_guis/chi_adm_imperial_law_icons.txt',emit(icon_guis)+'\n')
    gui_path = 'gui/journal_entry_widgets/chi_adm_imperial_law.gui'
    gui = (ROOT/gui_path).read_text('utf-8-sig')
    for which,content in [('requested',requested_icons),('current',current_icons)]:
        start = '# BEGIN GENERATED '+which.upper()+' ICONS'
        end = '# END GENERATED '+which.upper()+' ICONS'
        block = start+'\nwidget = { size = { 48 48 }\n'+'\n'.join(content)+'\n}\n'+end
        if start in gui:
            gui = re.sub(re.escape(start)+r'.*?'+re.escape(end),lambda m:block,gui,flags=re.S)
        else:
            old = 'icon = { size = { 48 48 } texture = "[Country.GetCustom(\'chi_adm_imperial_law_'+which+'_icon\')]" }'
            assert old in gui, 'Cannot find icon slot: '+which
            gui = gui.replace(old,block)
    write(gui_path,gui)
    replace(cp,'chi_adm_imperial_law_current_icon','type = country\n'+'\n'.join(f"text = {{ trigger = {{ chi_adm_imperial_law_icon_group_{groups[x['group']]} = yes has_law = law_type:{x['law']} }} localization_key = chi_adm_imperial_law_requested_icon_{x['id']} }}" for x in rows))
    # Manual selection cycles only laws currently held by Qing. Recipient stays
    # the scripted GUI root throughout; no saved temporary country/law targets.
    replace(ep,'chi_adm_imperial_law_select_next','''set_variable = { name = chi_adm_imperial_law_selection_after value = 0 }
if = { limit = { has_variable = chi_adm_imperial_law_selected_id } set_variable = { name = chi_adm_imperial_law_selection_after value = var:chi_adm_imperial_law_selected_id } }
remove_variable = chi_adm_imperial_law_selection_found
'''+ '\n'.join(f"if = {{ limit = {{ NOT = {{ has_variable = chi_adm_imperial_law_selection_found }} var:chi_adm_imperial_law_selection_after < {x['id']} c:CHI = {{ has_law = law_type:{x['law']} }} }} set_variable = {{ name = chi_adm_imperial_law_selected_id value = {x['id']} }} set_variable = chi_adm_imperial_law_selection_found }}" for x in rows)+ '\n'+ '\n'.join(f"if = {{ limit = {{ NOT = {{ has_variable = chi_adm_imperial_law_selection_found }} c:CHI = {{ has_law = law_type:{x['law']} }} }} set_variable = {{ name = chi_adm_imperial_law_selected_id value = {x['id']} }} set_variable = chi_adm_imperial_law_selection_found }}" for x in rows)+'\nremove_variable = chi_adm_imperial_law_selection_found\nremove_variable = chi_adm_imperial_law_selection_after')
    replace(ep,'chi_adm_imperial_law_send_selected','\n'.join(f"if = {{ limit = {{ var:chi_adm_imperial_law_selected_id = {x['id']} c:CHI = {{ has_law = law_type:{x['law']} }} }} chi_adm_imperial_law_receive = {{ ID = {x['id']} }} }}" for x in rows))
    replace(tp,'chi_adm_imperial_law_selected_sendable','chi_adm_imperial_law_civil = yes\nNOT = { exists = imposed_law }\nNOT = { has_journal_entry = je_law_imposition }\nOR = {\n'+'\n'.join(f"AND = {{ var:chi_adm_imperial_law_selected_id = {x['id']} c:CHI = {{ has_law = law_type:{x['law']} }} NOT = {{ has_law = law_type:{x['law']} }} NOT = {{ has_variable = chi_adm_imperial_law_repeat_{x['id']} }} NOT = {{ AND = {{ has_variable = chi_adm_imperial_law_active var:chi_adm_imperial_law_law_id = {x['id']} }} }} }}" for x in rows)+'\n}')
    lp = 'localization/english/chi_adm_l_english.yml'
    loc = (ROOT/lp).read_text('utf-8-sig')
    loc = re.sub(r'^ chi_adm_imperial_law_(?:requested_name|group_name|current_name|requested_icon|current_icon)_\d+:.*\n','',loc,flags=re.M)
    for x in rows:
        for k,value in [('requested_icon',core.get(effective[x['law']][1], 'icon').strip(chr(34))),('requested_name',f"[GetLawType('{x['law']}').GetName]"),('group_name',f"[GetLawGroup('{x['group']}').GetName]"),('current_name',f"[Country.GetActiveLawFromGroup('{x['group']}').GetName]")]:
            loc += f' chi_adm_imperial_law_{k}_{x["id"]}: "{value}"\n'
    write(lp,loc)
    # Full source-level coverage, not invented per-country legal verdicts.
    report = ['# imperial law reform complete law registry coverage','',f'{len(rows)} effective laws; {len(groups)} law groups. Every row is requestable when Qing holds it. Automatic dispatch: all 15 administrations. Native manual interactions remain available; the court docket is retired. No law/group whitelist.','',
    'Legality is country- and time-dependent. Requestable does not mean enactable. Imperial adoption uses native law_is_available to retain technology, conflicting-law and custom restrictions while waiving political support. Gradual implementation blocks new enactments for 12 calendar months, then activates the law; instant adoption activates it immediately. This report records exact source restrictions, not a fabricated verdict for an unspecified save. An incompatible request stays blocked and permits petition/refusal. No unsupported laws are intentionally omitted.','',
    'Native manual exposure requires a can_impose definition; the court selector covers every law whether or not that native button exists. Runtime event ordering, native legality and actual save/load remain unverified. Only game/common/laws and this mod are included; other enabled mods require regeneration against their effective load order.','']
    referenced = set()
    def collect(items):
        for key,op,value in items:
            referenced.add(key)
            if isinstance(value,list):
                collect(value)
    for x in sorted(rows,key=lambda x:(x['group'],x['law'])):
        path,body = effective[x['law']]
        source = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else 'game/'+str(path.relative_to(GAME))
        report += [f"## {x['law']} (ID {x['id']})",'',f"Group: `{x['group']}`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **{'present' if any(k=='can_impose' for k,_,v in body) else 'absent; use court selector'}**. Source: `{source}`.",'','Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):','', '```paradox']
        restrictions = [(k,op,v) for k,op,v in body if k in ('can_enact','is_visible','unlocking_technologies','disallowing_laws','possible','is_available','on_impose')]
        collect(restrictions)
        report += [emit(restrictions) if restrictions else '# No additional conditions declared on this law.', '```','']
        if any(k=='can_enact' and isinstance(v,list) and ('always','=','no') in v for k,op,v in body):
            report += ['**Ordinary enactment is unconditionally prohibited by this law\'s `can_enact = { always = no }` clause.** The request remains possible; acceptance cannot bypass this restriction.','']
    # Include the exact scripted predicates referenced by law conditions, so a
    # custom condition is inspectable rather than merely labelled incompatible.
    trigger_files = {p.name:p for p in (GAME/'common/scripted_triggers').glob('*.txt')}
    trigger_files.update({p.name:p for p in (ROOT/'common/scripted_triggers').glob('*.txt')})
    predicates, overrides = {}, {}
    for name,p in sorted(trigger_files.items()):
        # Index top-level blocks independently. Some unrelated installed trigger
        # files contain stray top-level delimiters; don't repair those files or
        # make law coverage depend on parsing unrelated commander predicates.
        text = p.read_text('utf-8-sig')
        for match in re.finditer(r'^([\w:]+)\s*=\s*{',text,re.M):
            depth = 1
            end = None
            for token in re.finditer(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}]',text[match.end():]):
                if token.group() == '{':
                    depth += 1
                elif token.group() == '}':
                    depth -= 1
                if depth == 0:
                    end = match.end()+token.end()
                    break
            if end is None:
                continue
            key = match.group(1)
            (overrides if key.startswith('REPLACE:') else predicates)[key.removeprefix('REPLACE:')] = (p,text[match.start():end])
    predicates.update(overrides)
    done = set()
    report += ['# Referenced scripted eligibility predicates','', 'These definitions are source evidence, not results evaluated for a particular country. Engine built-ins retain their native meaning.','']
    while True:
        pending = sorted((referenced & predicates.keys()) - done)
        if not pending:
            break
        for key in pending:
            done.add(key)
            path,snippet = predicates[key]
            body = core.parse(snippet)[0][2]
            source = str(path.relative_to(ROOT)) if path.is_relative_to(ROOT) else 'game/'+str(path.relative_to(GAME))
            report += [f'## {key}', '', f'Source: `{source}`.', '', '```paradox', emit([(key,'=',body)]), '```','']
            collect(body)
    write('docs/chi_adm_imperial_law_coverage.md','\n'.join(report)+'\n')
    print(f'{"CHECKED" if CHECK else "GENERATED"}: {len(rows)} laws / {len(groups)} groups')

if __name__ == '__main__':
    main()
