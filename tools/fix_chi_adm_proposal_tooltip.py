from pathlib import Path

root = Path(__file__).resolve().parents[1]
for relative in ('common/scripted_guis/chi_adm_negotiated_integration.txt', 'common/scripted_triggers/chi_adm_negotiated_integration.txt', 'common/scripted_effects/chi_adm_negotiated_integration.txt'):
    path = root / relative
    text = path.read_text(encoding='utf-8').replace('liberty_desire <= 25', 'var:chi_adm_autonomy <= 25')
    path.write_text(text, encoding='utf-8')

checks = [
    ('autonomy', 'var:chi_adm_autonomy <= 25', '@chi_adm_autonomy! [concept_chi_adm_autonomy] is at most #v 25#!.'),
    ('archives', 'c:CHI = { has_technology_researched = central_archives }', "[ROOT.GetCountry.GetOverlord.GetName] has researched [GetTechnology('central_archives').GetName]."),
    ('authority', 'c:CHI = { authority >= 0 }', '[ROOT.GetCountry.GetOverlord.GetName] has nonnegative @aut! [concept_authority].'),
    ('bureaucracy', 'c:CHI = { relative_bureaucracy >= 0 }', '[ROOT.GetCountry.GetOverlord.GetName] has nonnegative unused @bur! [concept_bureaucracy].'),
    ('peace', 'is_at_war = no c:CHI = { is_at_war = no }', 'Both countries are at peace.'),
    ('plays', 'is_diplomatic_play_committed_participant = no c:CHI = { is_diplomatic_play_committed_participant = no }', 'Neither country is committed to a [concept_diplomatic_play].'),
]
path = root / 'common/scripted_guis/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
marker = 'custom_tooltip_no_bullet = chi_adm_negotiated_integration_propose_requirements_heading'
lines = []
loc = []
for key, trigger, label in checks:
    key = 'chi_adm_negotiated_integration_proposal_' + key
    lines.append(f'\n\t\t\tif = {{\n\t\t\t\tlimit = {{ {trigger} }}\n\t\t\t\tcustom_tooltip_no_bullet = {key}_yes\n\t\t\t}}\n\t\t\telse = {{\n\t\t\t\tcustom_tooltip_no_bullet = {key}_no\n\t\t\t}}')
    loc.extend([f' {key}_yes: "@green_checkmark! {label}"', f' {key}_no: "@red_cross! {label}"'])
if 'chi_adm_negotiated_integration_proposal_autonomy_yes' not in text:
    text = text.replace(marker, marker + ''.join(lines), 1)
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
if 'chi_adm_negotiated_integration_proposal_autonomy_yes:' not in text:
    text += '\n' + '\n'.join(loc) + '\n'
path.write_text(text, encoding='utf-8-sig')
