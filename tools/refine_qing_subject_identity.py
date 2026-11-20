from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
tags = {'XIB': ('Shaan-Gan Viceroyalty', 'Shaan-Gan'), 'FRS': ('Min-Zhe Viceroyalty', 'Min-Zhe'), 'HNA': ('Huguang Viceroyalty', 'Huguang'), 'AHU': ('Liangjiang Viceroyalty', 'Liangjiang'), 'MCH': ('Three Eastern Provinces', 'Manchurian')}
for relative in ('localization/english/chi_adm_l_english.yml', 'localization/english/tyrone_qing_administrations_l_english.yml'):
    path = root / relative
    text = path.read_text(encoding='utf-8-sig')
    for tag in tags:
        text = re.sub(r'^ ' + tag + r'(?:_ADJ)?:.*\n?', '', text, flags=re.M)
    path.write_text(text, encoding='utf-8-sig')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
for tag, (name, adjective) in tags.items():
    for key, value in [(f'chi_adm_subject_{tag}_name', name), (f'chi_adm_subject_{tag}_adj', adjective)]:
        if not re.search(r'^ ' + key + ':', text, re.M):
            text += f'\n {key}: "{value}"\n'
path.write_text(text, encoding='utf-8-sig')
path = root / 'common/dynamic_country_names/zz_chi_adm_restored_names.txt'
text = path.read_text(encoding='utf-8')
for tag in tags:
    text = re.sub(r'\bname = ' + tag + r'\b', 'name = chi_adm_subject_' + tag + '_name', text)
    text = text.replace('adjective = ' + tag + '_ADJ', 'adjective = chi_adm_subject_' + tag + '_adj')
# All four replaced offices are viceroyalties; MCH is a frontier administration.
parts = text.split('INJECT:')
for i, part in enumerate(parts):
    if not part:
        continue
    tag = part.split(' ', 1)[0]
    subject = 'frontier' if tag == 'MCH' else 'viceroyalty'
    parts[i] = part.replace('chi_qing_administrative_subject = yes', 'is_subject_type = subject_type_qing_' + subject + '_administration')
path.write_text('INJECT:'.join(parts), encoding='utf-8')
path = root / 'common/coat_of_arms/coat_of_arms/tyrone_qing_administrations.txt'
path.write_text('# Custom administration flag overrides removed; inherit country flag patterns.\n', encoding='utf-8')
path = root / 'common/history/global/zzzz_qing_administrations.txt'
text = path.read_text(encoding='utf-8-sig').replace('state_region = s:STATE_SHENGJING state_region = s:STATE_SOUTHERN_MANCHURIA', 'state_region = s:STATE_AMUR state_region = s:STATE_SHENGJING state_region = s:STATE_SOUTHERN_MANCHURIA')
path.write_text(text, encoding='utf-8-sig')
print('Applied conditional names, removed flag overrides and assigned Amur to MCH.')
