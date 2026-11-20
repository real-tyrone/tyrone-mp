"""Apply current relative national strength to provincial negotiation choices."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
def modifiers(resist=False):
    lines = []
    for stat in ('prestige', 'army_power_projection', 'gdp'):
        # Positive denominators avoid treating two collapsed economies/armies as weakness.
        for comparison, ratio, factor in (('<', .10, .8 if resist else 1.25), ('>=', .50, 1.25 if resist else .8), ('>=', 1, 1.25 if resist else .8)):
            lines.append(f'''modifier = {{
    trigger = {{
        c:CHI = {{ {stat} > 0 }}
        {stat} {comparison} {{ value = c:CHI.{stat} multiply = {ratio} }}
    }}
    factor = {factor}
}}''')
    return '\n'.join(lines)

path = root / 'events/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
start = text.index('chi_adm_negotiated_integration.1 =')
end = text.index('chi_adm_negotiated_integration.2 =')
section = text[start:end]
if 'value = c:CHI.army_power_projection multiply = ' not in section:
    for action in ('begin', 'centralize', 'request_subsidy', 'request_protection', 'request_honors', 'delay', 'refuse'):
        start_action = section.index('option = { name = chi_adm_negotiated_integration_' + action + ' ')
        ai = section.index('ai_chance = {', start_action) + len('ai_chance = {')
        section = section[:ai] + '\n' + modifiers(action != 'begin') + '\n' + section[ai:]
    text = text[:start] + section + text[end:]
path.write_text(text, encoding='utf-8')

# Preserve changes when the event generator is deliberately rerun.
path = root / 'tools/build_chi_adm_negotiated_integration.py'
text = path.read_text(encoding='utf-8')
marker = "event(1,'A Province Before the Throne'"
if '# Relative national strength in provincial negotiations.' not in text:
    additions = '# Relative national strength in provincial negotiations.\n'
    for action in ('begin', 'centralize', 'request_subsidy', 'request_protection', 'request_honors', 'delay', 'refuse'):
        additions += f"weights[{action!r}] = weights.get({action!r}, 'base = 8') + {chr(10) + modifiers(action != 'begin')!r}\n"
    text = text.replace(marker, additions + marker, 1)
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
needle = 'and offered concessions influence negotiations.'
text = text.replace(needle, 'and offered concessions influence negotiations. Provincial [concept_prestige], [concept_army_power_projection] and [concept_gdp] relative to the central government also affect AI willingness: weaker provinces are more receptive; stronger provinces seek concessions or resist.')
path.write_text(text, encoding='utf-8-sig')
