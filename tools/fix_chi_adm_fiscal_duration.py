from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'common/scripted_effects/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
start = text.index('chi_adm_negotiated_integration_apply_protection = {')
end = text.index('\nchi_adm_negotiated_integration_update_tax =', start)
text = text[:start] + '''chi_adm_negotiated_integration_apply_protection = {
    save_scope_as = chi_adm_negotiated_integration_province
    if = {
        limit = { var:chi_adm_negotiated_integration_protection > 0 }
        every_scope_state = {
            remove_modifier = chi_adm_negotiated_integration_local_privileges
            remove_variable = chi_adm_negotiated_integration_tax_left
            remove_variable = chi_adm_negotiated_integration_tax_total
            remove_variable = chi_adm_negotiated_integration_tax_strength
            remove_variable = chi_adm_negotiated_integration_tax_new
            if = {
                limit = { scope:chi_adm_negotiated_integration_province = { var:chi_adm_negotiated_integration_protection = 2 } }
                add_modifier = { name = chi_adm_negotiated_integration_local_privileges multiplier = 2 years = 5 }
            }
            else = {
                add_modifier = { name = chi_adm_negotiated_integration_local_privileges multiplier = 1 years = 5 }
            }
        }
    }
}
''' + text[end:]
path.write_text(text, encoding='utf-8')
for relative in ('common/scripted_guis/chi_adm_negotiated_integration.txt', 'events/chi_adm_negotiated_integration.txt'):
    path = root / relative
    text = path.read_text(encoding='utf-8')
    text = re.sub(r'(name = chi_adm_negotiated_integration_local_privileges\s+multiplier = 2\s+years = )10', r'\g<1>5', text)
    path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
lines = text.splitlines()
for i, line in enumerate(lines):
    if 'chi_adm_negotiated_integration_' in line and any(word in line.lower() for word in ('tax collection', 'penalty decays', 'fiscal privileges survive')):
        line = line.replace('fading over #v 10 years#!', 'lasting #v 5 years#! at full strength').replace('fading over #v 5 years#!', 'lasting #v 5 years#! at full strength')
        line = line.replace('The penalty decays monthly over #v 10 years#!.', 'The full penalty lasts #v 5 years#!, then expires.').replace('The penalty decays monthly over #v 5 years#!.', 'The full penalty lasts #v 5 years#!, then expires.')
        line = line.replace('fading over five years, or -20% over ten', 'for five years, or -20% for five years').replace('or to -20% for ten years', 'or to -20% for five years').replace('and decay monthly', 'and expire after five years')
        line = line.replace('decaying over ten years', 'lasting five years').replace('decaying over five years', 'lasting five years')
        line = line.replace('diminish each month until the agreed term expires', 'remain at full strength for five years, then expire')
        lines[i] = line
path.write_text('\n'.join(lines) + '\n', encoding='utf-8-sig')
