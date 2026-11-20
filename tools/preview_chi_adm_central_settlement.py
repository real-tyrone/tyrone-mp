from pathlib import Path

root = Path(__file__).resolve().parents[1]
preview = '''show_as_tooltip = {
    scope:chi_adm_negotiated_integration_target = {
        if = {
            limit = { var:chi_adm_negotiated_integration_honors > 0 exists = ruler }
            ruler = { add_modifier = { name = chi_adm_negotiated_integration_honored years = 10 } }
            c:CHI = { add_modifier = { name = chi_adm_negotiated_integration_honors_patronage years = 5 } }
        }
    }
}'''
path = root / 'events/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
marker = 'custom_tooltip = chi_adm_negotiated_integration_central_settlement_desc'
if marker + '\n' not in text:
    text = text.replace(marker, marker + '\n' + preview + '\n')
path.write_text(text, encoding='utf-8')
