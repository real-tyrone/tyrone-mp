"""Restore only the three eastern-border buttons from installed vanilla."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
path = root / 'common/scripted_buttons/04_russia_buttons.txt'
vanilla = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/scripted_buttons/04_russia_buttons.txt').read_text(encoding='utf-8-sig')
raw = path.read_bytes()
text = raw.decode('utf-8-sig')
def span(source, key):
    match = re.search(r'(?m)^' + re.escape(key) + r'\s*=\s*\{', source)
    assert match, key
    end = source.index('{', match.start()) + 1
    depth = 1
    while depth:
        depth += (source[end] == '{') - (source[end] == '}')
        end += 1
    return match.start(), end
keys = ('je_the_eastern_border_treaty_of_beijing', 'je_the_eastern_border_russia_chuguchak_protocol', 'je_the_eastern_border_treaty_of_aigun')
for key in keys:
    start, end = span(text, key)
    original_start, original_end = span(vanilla, key)
    text = text[:start] + vanilla[original_start:original_end] + text[end:]
for key in keys:
    start, end = span(text, key)
    original_start, original_end = span(vanilla, key)
    assert text[start:end] == vanilla[original_start:original_end]
path.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.encode('utf-8'))
print('All three treaty button definitions match installed vanilla exactly.')
