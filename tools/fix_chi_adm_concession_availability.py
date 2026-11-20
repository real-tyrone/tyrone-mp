"""Keep unused concession types available after another offer is refused."""
from pathlib import Path

root = Path(__file__).resolve().parents[1]
for relative in (
    'common/scripted_effects/chi_adm_negotiated_integration.txt',
    'common/scripted_guis/chi_adm_negotiated_integration.txt',
    'events/chi_adm_negotiated_integration.txt',
    'tools/build_chi_adm_negotiated_integration.py',
):
    path = root / relative
    text = path.read_text(encoding='utf-8')
    text = text.replace('NOT = { has_variable = chi_adm_negotiated_integration_final_offer } ', '')
    path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
text = text.replace('another refusal permits one revised offer, withdrawal or a [concept_diplomatic_play].', 'after a refusal, unused concessions remain available up to their individual limits. The court may also withdraw or initiate a [concept_diplomatic_play].')
text = text.replace('Previously used pressure and final-offer limits still apply; leaving the papers open does not renew them.', 'Unused financial support, fiscal privileges and imperial honors remain available up to their individual limits. Pressure may be used only once.')
text = text.replace('One pressure attempt is permitted, then one improved offer. Further refusal leaves withdrawal or coercion.', 'One pressure attempt is permitted. Each concession remains available up to its own limit; the court may also withdraw or seek coercion.')
path.write_text(text, encoding='utf-8-sig')
