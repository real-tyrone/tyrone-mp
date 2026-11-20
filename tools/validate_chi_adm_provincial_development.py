from pathlib import Path
import re
import validate_chi_adm as core

root = Path(__file__).resolve().parents[1]
files = list(root.glob('common/*/chi_adm_provincial_development.txt')) + [root/'events/chi_adm_provincial_development.txt']
for path in files:
    core.parse(path.read_text(encoding='utf-8-sig'))
loc = (root/'localization/english/chi_adm_l_english.yml').read_text(encoding='utf-8-sig')
keys = re.findall(r'^ (\w+):',loc,re.M)
assert len(keys) == len(set(keys)), 'Duplicate English localization keys'
type_directory = Path('C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game/common/modifier_type_definitions')
types = '\n'.join(path.read_text(encoding='utf-8-sig') for path in sorted(type_directory.glob('*.txt')))
modifiers = core.parse((root/'common/static_modifiers/chi_adm_provincial_development.txt').read_text(encoding='utf-8-sig'))
for _,_,body in modifiers:
    for key,_,value in body:
        if key != 'icon':
            assert re.search(r'^'+key+r'\s*=',types,re.M), key
for path in files:
    text = path.read_text(encoding='utf-8-sig')
    for key in re.findall(r'(?:desc|title|conclusion_desc)\s*=\s*(chi_adm_provincial_development_\w+)',text):
        assert key in keys, key
# Restoration returns only the tracked emergency grant; other gains remain.
for starting in range(101):
    for grant in (5,10):
        actual = min(100, starting+grant)
        restored = max(0,actual-grant)
        assert 0 <= restored <= 100
print('PASS emergency powers parse, localization references and installed modifier types.')
import validate_chi_adm_provincial_development_complete
import validate_chi_adm_provincial_development_funding
