"""One-time mechanical migration to the requested canonical country tags."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
mapping = {'QSG': 'XIB', 'QMZ': 'FRS', 'QHG': 'HNA', 'QLJ': 'AHU'}
changed = []
for directory in ('common', 'events', 'gui', 'localization', 'tools', 'docs'):
    for path in (root / directory).rglob('*'):
        if not path.is_file() or path.suffix not in ('.txt', '.gui', '.yml', '.py', '.json', '.md') or path.name == Path(__file__).name:
            continue
        raw = path.read_bytes()
        try:
            text = raw.decode('utf-8-sig')
        except UnicodeDecodeError:
            continue
        original = text
        for before, after in mapping.items():
            text = text.replace(before, after)
        if path.as_posix().endswith('country_definitions/tyrone_qing_administrations.txt'):
            text = re.sub(r'(FRS = \{.*?cultures = )\{ han \}', r'\1{ han min }', text, flags=re.S)
            text = re.sub(r'(XIB = \{.*?capital = )STATE_XIAN', r'\1STATE_NINGXIA', text, flags=re.S)
        if path.as_posix().endswith('history/global/zzzz_qing_administrations.txt'):
            text = re.sub(r'(c:XIB = \{\s*)set_capital = STATE_XIAN', r'\1set_capital = STATE_NINGXIA', text)
        if text != original:
            path.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.encode('utf-8'))
            changed.append(str(path.relative_to(root)))
print('\n'.join(changed))
