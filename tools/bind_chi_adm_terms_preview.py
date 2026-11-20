from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'gui/journal_entry_widgets/chi_adm_negotiated_integration.gui'
text = path.read_text(encoding='utf-8')
needle = 'text = "chi_adm_negotiated_integration_terms_display" }'
replacement = '''text = "chi_adm_negotiated_integration_terms_display"
    tooltip = "[GetScriptedGui('chi_adm_negotiated_integration_terms_preview').ExecuteTooltip(GuiScope.SetRoot(Country.MakeScope).End)]"
}'''
text = text.replace(needle, replacement)
path.write_text(text, encoding='utf-8')
