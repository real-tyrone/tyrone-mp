from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
regions = {1: [('outer', 'OUTER_MANCHURIA')], 2: [('altai', 'ALTAI'), ('jetisy', 'JETISY'), ('kirghizia', 'KIRGHIZIA')], 3: [('amur', 'AMUR')]}
path = root / 'events/chi_qing_treaty_approval.txt'
text = path.read_text(encoding='utf-8')
for number, states in regions.items():
    marker = f'trigger = {{ exists = c:RUS var:chi_qing_treaty_pending = {number} }}'
    immediate = '\n    immediate = {\n        c:RUS = { save_scope_as = treaty_russia }\n'
    for key, state in states:
        immediate += f'        s:STATE_{state} = {{ save_scope_as = treaty_{key} }}\n'
    immediate += '    }'
    if marker + immediate not in text:
        text = text.replace(marker, marker + immediate)
path.write_text(text, encoding='utf-8')
country = "the [SCOPE.sCountry('treaty_russia').GetName]"
adj = "[SCOPE.sCountry('treaty_russia').GetAdjectiveNoFlag]"
state = lambda key: "[SCOPE.sStateRegion('treaty_" + key + "').GetName]"
terms = f"An outstanding [concept_obligation] owed to {country} requires acceptance. Otherwise, refusal worsens [concept_relations] by #r 10#! and blocks further treaty requests for #v 12 months#!."
descriptions = {
1: f"Envoys from {country} have presented a demand for {state('outer')}. The {adj} delegation seeks control of the maritime frontier beyond the Ussuri, extending its sovereign’s authority toward the Pacific coast.\n\nThe Grand Council warns that surrendering these lands would diminish the dynasty’s northeastern defenses. Ratification will transfer the affected territories held by the imperial government and its subjects to {country}.\n\n{terms}",
2: f"Representatives of {country} have proposed a settlement of the western frontier. Their demands encompass {state('altai')}, {state('jetisy')} and {state('kirghizia')}, redrawing the boundary between the {adj} possessions and the imperial dominions.\n\nThe frontier commissioners protest that these valleys and mountain passes sustain the empire’s authority in the northwest. Ratification will transfer the affected territories held by the imperial government and its subjects to {country}.\n\n{terms}",
3: f"{adj} envoys have presented a treaty concerning the Heilongjiang, known abroad as the Amur River. The delegation demands recognition of {adj} sovereignty over {state('amur')}.\n\nFor generations, the rivers and forests of the northeast have formed part of the Manchu homeland. The imperial ministers warn that ratification would surrender the affected territories held by the Throne and its subjects to {country}, bringing its frontier closer to the dynasty’s ancestral heartland.\n\n{terms}",
}
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
for number, description in descriptions.items():
    line = f' chi_qing_treaty_{number}_desc: "' + description.replace('\n', r'\n') + '"'
    text, count = re.subn(r'^ chi_qing_treaty_' + str(number) + r'_desc:.*$', lambda _: line, text, flags=re.M)
    assert count == 1
path.write_text(text, encoding='utf-8-sig')
