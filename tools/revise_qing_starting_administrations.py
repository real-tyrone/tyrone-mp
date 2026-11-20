from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
def edit(relative, function):
    path = root / relative
    raw = path.read_bytes()
    text = function(raw.decode('utf-8-sig'))
    path.write_bytes((b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b'') + text.encode('utf-8'))
def remove_definition(text, key):
    match = re.search(r'(?m)^' + re.escape(key) + r'\s*=\s*\{', text)
    if not match:
        return text
    end = text.index('{', match.start()) + 1
    depth = 1
    while depth:
        depth += (text[end] == '{') - (text[end] == '}')
        end += 1
    return text[:match.start()] + text[end:]

path = root / 'common/history/global/zzzz_qing_administrations.txt'
text = path.read_text(encoding='utf-8-sig')
# Each setup segment starts with the seed selection and ends after its pact/capital.
segments = list(re.finditer(r'   random_scope_state = \{ limit = \{ state_region = s:(\w+) \} save_scope_as = chi_qing_seed \}', text))
for tag, target in [('QXN', 'XIB'), ('QIM', 'MGL'), ('QHN', 'AHU')]:
    matches = list(re.finditer(r'   random_scope_state = \{ limit = \{ state_region = s:(\w+) \} save_scope_as = chi_qing_seed \}', text))
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else text.index('   # Finalize laws', match.start())
        segment = text[match.start():end]
        if f'tag = {tag}\n' not in segment:
            continue
        transfer = next(line for line in segment.splitlines() if 'set_state_owner' in line).replace('c:' + tag, 'c:' + target)
        text = text[:match.start()] + transfer + '\n' + text[end:]
        break
marker = '   # Finalize laws'
if 'tag = MCH' not in text:
    text = text.replace(marker, '''   random_scope_state = { limit = { state_region = s:STATE_SOUTHERN_MANCHURIA } save_scope_as = chi_qing_seed }
   create_country = {
    tag = MCH
    origin = this
    state = scope:chi_qing_seed
    on_created = {
     copy_laws = c:CHI
     set_state_religion = rel:confucian
     if = { limit = { NOT = { country_has_primary_culture = cu:manchu } } add_primary_culture = cu:manchu }
     effect_starting_technology_tier_4_tech = yes
     set_variable = chi_qing_appointed_administration
    }
   }
   every_scope_state = {
    limit = { OR = { state_region = s:STATE_SHENGJING state_region = s:STATE_SOUTHERN_MANCHURIA state_region = s:STATE_NORTHERN_MANCHURIA state_region = s:STATE_OUTER_MANCHURIA } }
    set_state_owner = c:MCH
   }
   create_diplomatic_pact = { country = c:MCH type = qing_frontier_administration }
   c:MCH = {
    set_capital = STATE_SOUTHERN_MANCHURIA
    add_liberty_desire = -100
    change_relations = { country = c:CHI value = 80 }
   }
   c:XIB = { if = { limit = { NOT = { country_has_primary_culture = cu:mongol } } add_primary_culture = cu:mongol } }
''' + marker, 1)
text = text.replace('NOT = { c:CHI ?= this } country_has_primary_culture = cu:manchu', 'NOT = { c:CHI ?= this } NOT = { c:MCH ?= this } country_has_primary_culture = cu:manchu')
path.write_text(text, encoding='utf-8-sig')
edit('common/country_definitions/tyrone_qing_administrations.txt', lambda s: re.sub(r'(XIB = \{.*?cultures = )\{ han \}', r'\1{ han mongol }', s, flags=re.S))
edit('common/coat_of_arms/coat_of_arms/tyrone_qing_administrations.txt', lambda s: remove_definition(s, 'XIB'))
edit('common/subject_types/tyrone_qing_administrations.txt', lambda s: remove_definition(s, 'subject_type_qing_military_administration'))
edit('common/diplomatic_actions/tyrone_qing_administrations.txt', lambda s: remove_definition(s, 'qing_military_administration'))
edit('common/scripted_triggers/tyrone_qing_administrations.txt', lambda s: s.replace('  is_subject_type = subject_type_qing_military_administration\n', '').replace('  c:QIM ?= this', '  c:MCH ?= this').replace('  c:QXN ?= this\n', '').replace('  c:QHN ?= this\n', ''))
edit('common/scripted_effects/chi_adm_core.txt', lambda s: s.replace('set_variable = chi_adm_initialized', '''if = {
 limit = { c:MCH ?= this }
 set_variable = { name = chi_adm_loyalty value = 85 }
 set_variable = { name = chi_adm_autonomy value = 15 }
 set_variable = { name = chi_adm_corruption value = 25 }
}
set_variable = chi_adm_initialized''', 1))
edit('common/scripted_effects/chi_adm_negotiated_integration.txt', lambda s: s.replace('c:QIM ?= { chi_adm_negotiated_integration_province_tick = yes }', 'c:MCH ?= { chi_adm_negotiated_integration_province_tick = yes }'))
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
for tag, name in [('XIB', 'Shaan-Gan Viceroyalty'), ('FRS', 'Min-Zhe Viceroyalty'), ('HNA', 'Huguang Viceroyalty'), ('AHU', 'Liangjiang Viceroyalty'), ('MCH', 'Manchurian Military Governorate')]:
    if not re.search(r'^ ' + tag + ':', text, re.M):
        text += f'\n {tag}: "{name}"\n'
path.write_text(text, encoding='utf-8-sig')
print('Updated starting territory, MCH frontier accounts, names and XIB flag override.')
