"""Use the court country's adjective in target-country negotiated integration tooltips."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
adjective = '[ROOT.GetCountry.GetOverlord.GetAdjectiveNoFlag]'
phrases = ('Qing administration', 'Qing subject', 'Qing administrative service', 'Qing Authority', 'Qing resources', 'Qing breach', 'Qing court')
lines = text.splitlines()
changed = 0
for index, line in enumerate(lines):
    if re.match(r' chi_adm_negotiated_integration_\w+:', line) and '_event_' not in line:
        original = line
        for phrase in phrases:
            line = line.replace(phrase, adjective + phrase[4:])
        if line != original:
            changed += 1
            lines[index] = line
path.write_text('\n'.join(lines) + '\n', encoding='utf-8-sig')
# Keep the source generator's target-country action descriptions consistent.
path = root / 'tools/build_chi_adm_negotiated_integration.py'
text = path.read_text(encoding='utf-8')
for phrase in phrases:
    text = text.replace(phrase, adjective + phrase[4:])
path.write_text(text, encoding='utf-8')
print(f'Updated {changed} negotiated integration tooltip lines.')
