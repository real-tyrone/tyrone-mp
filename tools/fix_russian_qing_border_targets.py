"""Allow Russian treaty buttons to target Qing-held and Qing-subject territory."""
from pathlib import Path
import re

path = Path(__file__).resolve().parents[1] / 'common/scripted_buttons/04_russia_buttons.txt'
text = path.read_text(encoding='utf-8-sig')
# Restrict edits to the three eastern treaty definitions.
for key in ('je_the_eastern_border_treaty_of_beijing', 'je_the_eastern_border_russia_chuguchak_protocol', 'je_the_eastern_border_treaty_of_aigun'):
    match = re.search(r'(?m)^' + key + r' = \{', text)
    start = match.start()
    end = text.index('{', start) + 1
    depth = 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    block = text[start:end]
    # Culture is not a reliable proxy for membership in the imperial realm.
    pattern = r'OR\s*=\s*\{\s*country_has_primary_culture = cu:manchu\s*country_has_primary_culture = cu:han\s*(?:country_has_primary_culture = cu:uighur\s*)?\}'
    block = re.sub(pattern, 'OR = { c:CHI ?= this is_subject_of = c:CHI }', block)
    block = re.sub(r'(is_subject = no\s+is_subject_of = ROOT)', r'\1\n\t\t\t\tis_subject_of = c:CHI', block)
    text = text[:start] + block + text[end:]
path.write_text(text, encoding='utf-8')
print('Updated visibility, eligibility and donor selection for all three border treaties.')
