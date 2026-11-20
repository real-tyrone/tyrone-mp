"""Keep each country's conditional name list in its existing injection."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'common/dynamic_country_names/tyrone_qing_administrations.txt'
text = path.read_text(encoding='utf-8')
extra = root / 'common/dynamic_country_names/zz_chi_adm_restored_names.txt'
source = extra.read_text(encoding='utf-8')
for match in re.finditer(r'INJECT:(\w+) = \{', source):
    tag = match.group(1)
    start = source.index('{', match.start()) + 1
    end = start
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    body = source[start:end - 1]
    if f'name = chi_adm_subject_{tag}_name' in text:
        continue
    marker = f'INJECT:{tag} = {{'
    if marker in text:
        text = text.replace(marker, marker + body, 1)
    else:
        text += '\n' + marker + body + '}\n'
path.write_text(text, encoding='utf-8')
extra.write_text('# Conditional administration names consolidated into tyrone_qing_administrations.txt.\n', encoding='utf-8')
