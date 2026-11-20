from pathlib import Path

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
            set_variable = { name = chi_adm_negotiated_integration_tax_left value = 60 }
            set_variable = { name = chi_adm_negotiated_integration_tax_total value = 60 }
            if = {
                limit = { scope:chi_adm_negotiated_integration_province = { var:chi_adm_negotiated_integration_protection = 2 } }
                set_variable = { name = chi_adm_negotiated_integration_tax_strength value = 2 }
            }
            else = {
                set_variable = { name = chi_adm_negotiated_integration_tax_strength value = 1 }
            }
            chi_adm_negotiated_integration_update_tax = yes
            set_variable = { name = chi_adm_negotiated_integration_tax_new value = yes days = 1 }
        }
    }
}
''' + text[end:]
path.write_text(text, encoding='utf-8')
path = root / 'tools/build_chi_adm_negotiated_integration.py'
text = path.read_text(encoding='utf-8').replace('chi_adm_negotiated_integration_tax_left value = 120', 'chi_adm_negotiated_integration_tax_left value = 60').replace('chi_adm_negotiated_integration_tax_total value = 120', 'chi_adm_negotiated_integration_tax_total value = 60')
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
text = text.replace('lasting #v 5 years#! at full strength', 'fading over #v 5 years#!')
text = text.replace('The full penalty lasts #v 5 years#!, then expires.', 'The penalty fades monthly over #v 5 years#!, then expires.')
text = text.replace('remain at full strength for five years, then expire', 'fade monthly over five years, then expire')
text = text.replace('or -20% for five years', 'or -20% fading over five years').replace('and expire after five years', 'and fade monthly over five years')
path.write_text(text, encoding='utf-8-sig')
