"""Separate negotiated offer descriptions from their conditional effect previews."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
loc = {
    'offer_honors_desc': 'Offer imperial recognition for the governor\'s service.',
    'offer_protection_desc': 'Offer to preserve provincial fiscal privileges after peaceful annexation.',
    'offer_subsidy_desc': 'Offer financial support during active implementation.',
    'offer_effects': '#bold Effects upon agreement:#!',
    'honors_effects': '@chi_adm_loyalty! [concept_chi_adm_loyalty]: #g +3#!\n[concept_relations] with [ROOT.GetCountry.GetOverlord.GetName]: #g +5#!',
    'protection_effects_1': 'After annexation, owned [concept_state]s receive [GetStaticModifier(\'chi_adm_negotiated_integration_local_privileges\').GetName|v]:\n@tax! [concept_tax_capacity]: local Tax Collection #r −10%#!\nThe penalty decays monthly over #v 5 years#!.',
    'protection_effects_2': 'After annexation, owned [concept_state]s receive [GetStaticModifier(\'chi_adm_negotiated_integration_local_privileges\').GetName|v]:\nLocal Tax Collection #r −20%#!\nThe penalty decays monthly over #v 10 years#!.',
    'subsidy_effects_1': 'Receive an automatic weekly payment from [ROOT.GetCountry.GetOverlord.GetName] equal to #v 10%#! of provincial [concept_treasury] income.',
    'subsidy_effects_2': 'Receive an automatic weekly payment from [ROOT.GetCountry.GetOverlord.GetName] equal to #v 20%#! of provincial [concept_treasury] income.',
    'subsidy_effects_end': 'Payments start upon agreement and stop during suspension, upon annexation or upon cancellation.',
}
# Tax collection is distinct from tax capacity; use the actual modifier name.
loc['protection_effects_1'] = loc['protection_effects_1'].replace('@tax! [concept_tax_capacity]: local Tax Collection', 'Local Tax Collection')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
for key, value in loc.items():
    line = ' chi_adm_negotiated_integration_' + key + ': "' + value.replace('\n', r'\n') + '"'
    pattern = r'^ chi_adm_negotiated_integration_' + key + r':.*$'
    if re.search(pattern, text, re.M):
        text = re.sub(pattern, lambda _: line, text, flags=re.M)
    else:
        text += '\n' + line + '\n'
path.write_text(text, encoding='utf-8-sig')
path = root / 'common/scripted_guis/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
for action, variable in [('offer_subsidy', 'subsidy'), ('offer_protection', 'protection'), ('offer_honors', 'honors')]:
    start = text.index('chi_adm_negotiated_integration_' + action + ' = {')
    end = text.find('\nchi_adm_negotiated_integration_', start + 1)
    if end < 0:
        end = len(text)
    block = text[start:end]
    if 'custom_tooltip_no_bullet = chi_adm_negotiated_integration_offer_effects' in block:
        continue
    preview = '\n\t\tshow_as_tooltip = {\n\t\t\tcustom_tooltip_no_bullet = chi_adm_negotiated_integration_offer_effects\n'
    if variable == 'honors':
        preview += '\t\t\tcustom_tooltip_no_bullet = chi_adm_negotiated_integration_honors_effects\n'
    else:
        preview += f'\t\t\tif = {{\n\t\t\t\tlimit = {{ var:chi_adm_negotiated_integration_{variable} = 0 }}\n\t\t\t\tcustom_tooltip_no_bullet = chi_adm_negotiated_integration_{variable}_effects_1\n\t\t\t}}\n\t\t\telse = {{ custom_tooltip_no_bullet = chi_adm_negotiated_integration_{variable}_effects_2 }}\n'
        if variable == 'subsidy':
            preview += '\t\t\tcustom_tooltip_no_bullet = chi_adm_negotiated_integration_subsidy_effects_end\n'
    preview += '\t\t}\n'
    block = block.replace('hidden_effect = {', preview + '\t\thidden_effect = {', 1)
    text = text[:start] + block + text[end:]
path.write_text(text, encoding='utf-8')
