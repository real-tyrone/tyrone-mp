from pathlib import Path

root = Path(__file__).resolve().parents[1]
grant = 'add_modifier = { name = chi_adm_negotiated_integration_honored years = 10 }'
cost = '\n c:CHI = {\n  remove_modifier = chi_adm_negotiated_integration_honors_patronage\n  add_modifier = { name = chi_adm_negotiated_integration_honors_patronage years = 5 }\n }'
for relative in ('common/scripted_effects/chi_adm_negotiated_integration.txt', 'tools/build_chi_adm_negotiated_integration.py'):
    path = root / relative
    text = path.read_text(encoding='utf-8')
    # Attach only to actual ruler grants, never to the GUI preview.
    needle = 'ruler = { remove_modifier = chi_adm_negotiated_integration_honored ' + grant + ' }'
    if needle + cost not in text:
        text = text.replace(needle, needle + cost)
    path.write_text(text, encoding='utf-8')
path = root / 'common/static_modifiers/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
if 'chi_adm_negotiated_integration_honors_patronage =' not in text:
    text += '\nchi_adm_negotiated_integration_honors_patronage = {\n\ticon = gfx/interface/icons/timed_modifier_icons/modifier_statue_negative.dds\n\tcountry_authority_add = -50\n}\n'
path.write_text(text, encoding='utf-8')
path = root / 'common/scripted_guis/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
start = text.index('chi_adm_negotiated_integration_offer_honors = {')
end = text.index('\nchi_adm_negotiated_integration_', start + 1)
block = text[start:end]
if 'name = chi_adm_negotiated_integration_honors_patronage' not in block:
    block = block.replace('hidden_effect = {', 'show_as_tooltip = { c:CHI = { add_modifier = { name = chi_adm_negotiated_integration_honors_patronage years = 5 } } }\n hidden_effect = {', 1)
text = text[:start] + block + text[end:]
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
if ' chi_adm_negotiated_integration_honors_patronage:' not in text:
    text += '\n chi_adm_negotiated_integration_honors_patronage: "Imperial Honors Patronage"\n chi_adm_negotiated_integration_honors_patronage_desc: "Maintaining the honors promised to provincial governors occupies the attention and patronage of the imperial court."\n'
path.write_text(text, encoding='utf-8-sig')
