from pathlib import Path

root = Path(__file__).resolve().parents[1]
for relative in ('localization/english/chi_adm_l_english.yml', 'tools/build_chi_adm_negotiated_integration.py', 'tools/refine_chi_adm_negotiated_integration_status_loc.py'):
    path = root / relative
    encoding = 'utf-8-sig' if path.suffix == '.yml' else 'utf-8'
    text = path.read_text(encoding=encoding)
    text = text.replace('@aut![Nbsp]#v 50#! [concept_authority] and @bur!', '@aut![Nbsp]#v 10%#! [concept_authority] and @bur!')
    text = text.replace('@aut! #r −50#! [concept_authority] and @bur!', '@aut! #r −10%#! [concept_authority] and @bur!')
    text = text.replace('-50 Authority/-10% Bureaucracy commitment', '@aut! #r −10%#! [concept_authority] and @bur! #r −10%#! [concept_bureaucracy] commitment')
    # Preserve the user's live modifier change when regenerating negotiated integration files.
    text = text.replace('modifier_documents_negative.dds country_authority_add = -50 country_bureaucracy_mult = -0.10', 'modifier_documents_negative.dds country_authority_mult = -0.10 country_bureaucracy_mult = -0.10')
    path.write_text(text, encoding=encoding)
