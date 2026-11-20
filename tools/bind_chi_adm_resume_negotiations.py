from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'gui/journal_entry_widgets/chi_adm_negotiated_integration.gui'
text = path.read_text(encoding='utf-8')
marker = 'button = { visible = "[GetScriptedGui(\'chi_adm_negotiated_integration_offer_honors\')'
button = '''button = {
    visible = "[GetScriptedGui('chi_adm_negotiated_integration_resume_court_negotiations').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
    size = { 440 54 }
    using = default_button_action
    enabled = "[GetScriptedGui('chi_adm_negotiated_integration_resume_court_negotiations').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
    onclick = "[GetScriptedGui('chi_adm_negotiated_integration_resume_court_negotiations').Execute(GuiScope.SetRoot(Country.MakeScope).End)]"
    tooltip = "[GetScriptedGui('chi_adm_negotiated_integration_resume_court_negotiations').ExecuteTooltip(GuiScope.SetRoot(Country.MakeScope).End)]"
    textbox = {
        size = { 416 0 }
        max_width = 416
        autoresize = yes
        multiline = yes
        parentanchor = center
        align = center|nobaseline
        text = "chi_adm_negotiated_integration_resume_court_negotiations"
        alwaystransparent = yes
    }
}
'''
if 'text = "chi_adm_negotiated_integration_resume_court_negotiations"' not in text:
    assert marker in text
    text = text.replace(marker, button + marker, 1)
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
if ' chi_adm_negotiated_integration_resume_court_negotiations:' not in text:
    text += '\n chi_adm_negotiated_integration_resume_court_negotiations: "Review the Provincial Reply"\n chi_adm_negotiated_integration_resume_court_negotiations_desc: "Reopen the governor’s memorial and review the available court responses. Previously used pressure and final-offer limits still apply; leaving the papers open does not renew them."\n'
path.write_text(text, encoding='utf-8-sig')
