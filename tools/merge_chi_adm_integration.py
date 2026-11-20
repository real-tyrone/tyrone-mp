"""Merge the Qing integration register into the existing administrations JE."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
old = 'je_qing_imperial_administrations'
path = ROOT / 'common/journal_entries/tyrone_qing_administrations.txt'
text = path.read_text(encoding='utf-8-sig')
text = re.sub(r'^\s*scripted_button = chi_qing_integrate_\w+\n', '\n', text, flags=re.M)
if 'name = "chi_adm_negotiated_integration_court"' not in text:
    text = text.replace(' context = country', ' widget = { gui = "gui/journal_entry_widgets/chi_adm_negotiated_integration.gui" name = "chi_adm_negotiated_integration_court" container = "custom_widget_container_1" }\n scaling_modifiers_while_active = { modifier = chi_adm_negotiated_integration_commitment value = chi_adm_negotiated_integration_cost_scale }\n context = country', 1)
path.write_text(text, encoding='utf-8')
for relative in ('common/scripted_effects/chi_adm_negotiated_integration.txt', 'common/on_actions/chi_adm_negotiated_integration.txt'):
    path = ROOT / relative
    text = path.read_text(encoding='utf-8')
    text = text.replace('has_journal_entry = chi_adm_negotiated_integration_court', 'has_journal_entry = ' + old)
    text = text.replace('type = chi_adm_negotiated_integration_court', 'type = ' + old)
    path.write_text(text, encoding='utf-8')
path = ROOT / 'common/journal_entries/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
start = text.index('chi_adm_negotiated_integration_province =')
text = '''# Compatibility entry: existing saves retire the former separate register.
chi_adm_negotiated_integration_court = {
    context = country
    possible = { always = no }
    outcome = {
        flags = { hidden invalid_outcome }
        trigger = { always = yes }
    }
}
''' + text[start:]
path.write_text(text, encoding='utf-8')
print('Merged integration register into Qing Imperial Administrations.')
