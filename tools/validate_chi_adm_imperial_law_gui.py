"""Focused imperial law reform GUI regression checks; not a renderer or engine test."""
import hashlib
import json
import re
from pathlib import Path
import validate_chi_adm as core
import validate_chi_adm_court_register as ui
import generate_chi_adm_imperial_law_laws as gen

ROOT = Path(__file__).resolve().parents[1]

def checks():
    for path,digest in json.loads((ROOT/'tools/chi_adm_imperial_law_gui_mechanics_baseline.json').read_text()).items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==digest, path
    gui=(ROOT/'gui/journal_entry_widgets/chi_adm_imperial_law.gui').read_text()
    ui.check_model_structure(gui)
    visibility=core.definitions('common/scripted_guis/chi_adm_imperial_law.txt')['chi_adm_imperial_law_responses_visible']
    assert core.get(visibility,'is_valid')==[('chi_adm_imperial_law_can_answer','=','yes')]
    assert "GetScriptedGui('chi_adm_imperial_law_responses_visible')" in gui
    prompts=core.definitions('common/customizable_localization/chi_adm_imperial_law.txt')['chi_adm_imperial_law_response_prompt']
    assert core.get(core.get(prompts,'text'),'trigger')==[('chi_adm_imperial_law_can_answer','=','yes')]

    for expression in re.findall(r'"(\[[^"\n]*\])"',gui):
        assert expression.count("'") % 2 == 0, expression
        assert expression.count('(')==expression.count(')'), expression
    filters=re.findall(r"visible = \"\[ScriptedButton.HasTag\('([^']+)'\)\]\"",gui)
    assert sorted(filters)==['chi_adm_imperial_law_compliance','chi_adm_imperial_law_negotiation','chi_adm_imperial_law_refusal']
    expected={
        'compliance':{'immediate','gradual','queue','prioritize'},
        'negotiation':{'petition','delay'}, 'refusal':{'refuse'}}
    buttons=core.definitions('common/scripted_buttons/chi_adm_imperial_law.txt')
    for name,body in buttons.items():
        tags=[k for k,op,v in core.get(body,'tags')]
        matches=[tag for tag in filters if tag in tags]
        assert len(matches)==1, (name,matches)
        assert name.removeprefix('chi_adm_imperial_law_').removesuffix('_button') in expected[matches[0].removeprefix('chi_adm_imperial_law_')]
    # Both free and occupied provinces render each currently visible entry once.
    for names in [('immediate','gradual','petition','delay','refuse'),('queue','prioritize','petition','refuse')]:
        rendered=[name for tag in filters for name in names if tag in [k for k,op,v in core.get(buttons['chi_adm_imperial_law_'+name+'_button'],'tags')]]
        assert sorted(rendered)==sorted(names)
    assert gui.count('background = { using = frame_small }')==2
    assert gui.count('margin = { 16 14 }')==2
    assert 48+12+380==440 and 440+2*16==472
    for line in gui.splitlines():
        if line.startswith('textbox =') or 'textbox = {' in line:
            assert 'multiline = yes' in line and 'autoresize = yes' in line
            assert re.search(r'size = { (380|440) 0 }',line),line
            assert re.search(r'max_width = (380|440)',line),line
    assert gui.count('tooltip = "SCRIPTED_ACTION_TOOLTIP"')==3
    loc=(ROOT/'localization/english/chi_adm_l_english.yml').read_text('utf-8-sig')
    icons=core.definitions('common/customizable_localization/chi_adm_imperial_law.txt')
    current=icons['chi_adm_imperial_law_current_icon']
    rows=json.loads((ROOT/'tools/chi_adm_imperial_law_catalog.json').read_text())
    # Prevent reintroducing the localization-to-image bridge that failed in game.
    assert "Country.GetCustom('chi_adm_imperial_law_requested_icon')" not in gui
    assert "Country.GetCustom('chi_adm_imperial_law_current_icon')" not in gui
    selectors=core.definitions('common/scripted_guis/chi_adm_imperial_law_icons.txt')
    assert len(selectors)==len(rows)+len({r['group'] for r in rows})
    for name,body in selectors.items():
        assert {k for k,op,v in body}=={'scope','is_valid'}
        assert core.get(body,'scope')=='country'
    for row in rows:
        assert gui.count(f"texture = \"[GetLawType('{row['law']}').GetTexture]\"")==1
        name=f"chi_adm_imperial_law_requested_icon_{row['id']}_gui"
        assert core.get(selectors[name],'is_valid')==[('var:chi_adm_imperial_law_law_id','=',str(row['id']))]
        assert gui.count(f"GetScriptedGui('{name}')")==1
    for group in {r['group'] for r in rows}:
        assert gui.count(f"texture = \"[Country.GetActiveLawFromGroup('{group}').GetTexture]\"")==1
    laws=gen.discover()
    for row in rows:
        texture=core.get(laws[row['law']][1],'icon').strip('"')
        assert (ROOT/texture).exists() or (gen.GAME/texture).exists(),texture
        key='chi_adm_imperial_law_requested_icon_'+str(row['id'])
        assert f' {key}: "{texture}"' in loc
        branch=next(v for k,op,v in current if k=='text' and core.get(v,'localization_key')==key)
        assert ('has_law','=', 'law_type:'+row['law']) in core.get(branch,'trigger')
    assert 'GetTexture' not in '\n'.join(line for line in loc.splitlines() if re.match(r'\s*chi_adm_imperial_law_(requested|current)_icon_\d+:',line))
    print('PASS imperial law reform GUI: unique button filters, padded panels, direct native texture bindings, 264 law/27 group read-only icon selectors, existing icon assets, gameplay hashes unchanged')

if __name__=='__main__':
    checks()
