from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'common/scripted_buttons/04_russia_buttons.txt'
text = path.read_text(encoding='utf-8')
pattern = r'effect = \{\s*custom_tooltip = chi_qing_treaty_request_tt\s*hidden_effect = \{\s*c:CHI = \{\s*set_variable = \{ name = chi_qing_treaty_pending value = ([123]) \}\s*trigger_event = \{ id = chi_qing_treaty\.\1 popup = yes \}\s*\}\s*\}\s*\}'
def replacement(match):
    number = match.group(1)
    return f'''effect = {{
        c:CHI = {{
            hidden_effect = {{
                set_variable = {{ name = chi_qing_treaty_pending value = {number} }}
            }}
            trigger_event = {{ id = chi_qing_treaty.{number} popup = yes }}
        }}
    }}'''
text, count = re.subn(pattern, replacement, text)
assert count == 3, count
path.write_text(text, encoding='utf-8')
