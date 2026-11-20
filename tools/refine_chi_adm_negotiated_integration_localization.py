"""Keep generated and live integration localization consistent."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
replacements = {
    'Qing has researched #v Central Archives#!.': "[ROOT.GetCountry.GetOverlord.GetName] has researched [GetTechnology('central_archives').GetName].",
    'Qing has nonnegative [concept_authority].': '[ROOT.GetCountry.GetOverlord.GetName] has nonnegative @aut! [concept_authority].',
    'Qing has nonnegative unused [concept_bureaucracy].': '[ROOT.GetCountry.GetOverlord.GetName] has nonnegative unused @bur! [concept_bureaucracy].',
    'Qing has unlocked the required Mandate centralization.': '[ROOT.GetCountry.GetOverlord.GetName] has at least #v 6#! Mandate centralization, or Consolidated Imperial Authority.',
    'Qing has not unlocked the required Mandate centralization.': '[ROOT.GetCountry.GetOverlord.GetName] needs at least #v 6#! Mandate centralization, or Consolidated Imperial Authority.',
    '! [concept_chi_adm_autonomy] is at most': '! @chi_adm_autonomy! [concept_chi_adm_autonomy] is at most',
    'and #v 10%#! [concept_bureaucracy]': 'and @bur![Nbsp]#v 10%#! [concept_bureaucracy]',
    'Loyalty, Autonomy, Corruption, relations and offered concessions': '@chi_adm_loyalty! [concept_chi_adm_loyalty], @chi_adm_autonomy! [concept_chi_adm_autonomy], @chi_adm_corruption! [concept_chi_adm_corruption], [concept_relations] and offered concessions',
}
for relative in ('localization/english/chi_adm_l_english.yml', 'tools/build_chi_adm_negotiated_integration.py'):
    path = root / relative
    encoding = 'utf-8-sig' if path.suffix == '.yml' else 'utf-8'
    text = path.read_text(encoding=encoding)
    for before, after in replacements.items():
        text = text.replace(before, after)
    path.write_text(text, encoding=encoding)
print('Updated integration country/technology links, thresholds and concept icons.')
