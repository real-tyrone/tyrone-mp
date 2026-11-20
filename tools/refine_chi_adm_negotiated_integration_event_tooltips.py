"""Share court action previews with their event choices without executing them."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'events/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
gui = (root / 'common/scripted_guis/chi_adm_negotiated_integration.txt').read_text(encoding='utf-8')
def block_end(source, opening):
    depth = 1
    cursor = opening + 1
    while depth:
        depth += (source[cursor] == '{') - (source[cursor] == '}')
        cursor += 1
    return cursor

for action in ('offer_honors', 'offer_subsidy', 'offer_protection'):
    start = gui.index('chi_adm_negotiated_integration_' + action + ' = {')
    opening = gui.index('{', start)
    body = gui[opening:block_end(gui, opening)]
    previews = []
    for match in re.finditer(r'show_as_tooltip\s*=\s*\{', body):
        opening = body.index('{', match.start())
        preview = body[opening + 1:block_end(body, opening) - 1]
        if '_ready' in preview:
            continue
        # Existing GUI descriptions refer to their root province; events root in China.
        previews.append('show_as_tooltip = { scope:chi_adm_negotiated_integration_target = { ' + preview + ' } }')
    marker = 'custom_tooltip = chi_adm_negotiated_integration_' + action + '_desc'
    # Event choice is a proposal: preview the settlement, do not grant it here.
    if previews and marker + '\n' not in text:
        text = text.replace(marker, marker + '\n' + '\n'.join(previews) + '\n')
marker = 'custom_tooltip = chi_adm_negotiated_integration_pressure_desc'
if marker + '\n' not in text:
    text = text.replace(marker, marker + '''
    show_as_tooltip = {
        scope:chi_adm_negotiated_integration_target = {
            chi_adm_adjust_loyalty = { AMOUNT = -5 }
            change_relations = { country = c:CHI value = -10 }
        }
    }
''')
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
text = re.sub(r'^ chi_adm_negotiated_integration_pressure_desc:.*$', ' chi_adm_negotiated_integration_pressure_desc: "Press the provincial government to reconsider. This attempt may be used only once. The governor retains the final decision; another refusal permits one revised offer, withdrawal or a [concept_diplomatic_play]."', text, flags=re.M)
text = text.replace('Review its response and existing terms in Administrative Integration.', 'Review its response and existing terms in Qing Imperial Administrations.')
path.write_text(text, encoding='utf-8-sig')
