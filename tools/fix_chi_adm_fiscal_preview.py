from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
for relative in ('localization/english/chi_adm_l_english.yml', 'tools/refine_chi_adm_negotiated_integration_offer_tooltips.py'):
    path = root / relative
    encoding = 'utf-8-sig' if path.suffix == '.yml' else 'utf-8'
    text = path.read_text(encoding=encoding).replace('provincial [concept_income]', 'provincial [concept_treasury] income')
    path.write_text(text, encoding=encoding)
path = root / 'common/scripted_guis/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
for tier, multiplier, years in [(1, 1, 5), (2, 2, 10)]:
    marker = f'custom_tooltip_no_bullet = chi_adm_negotiated_integration_protection_effects_{tier}'
    preview = f'''every_scope_state = {{
                    add_modifier = {{
                        name = chi_adm_negotiated_integration_local_privileges
                        multiplier = {multiplier}
                        years = {years}
                    }}
                }}'''
    text = text.replace(marker, preview)
path.write_text(text, encoding='utf-8')
