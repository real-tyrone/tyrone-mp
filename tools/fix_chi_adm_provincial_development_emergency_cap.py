from pathlib import Path
root = Path(__file__).resolve().parents[1]
path = root/'common/script_values/chi_adm_provincial_development.txt'
text = path.read_text(encoding='utf-8-sig')
for grant in (5,10):
    key = f'chi_adm_provincial_development_grant_{grant}'
    if key+' =' not in text:
        text += f'\n{key} = {{ value = 100 subtract = var:chi_adm_autonomy min = {grant} max = 0 }}\n'
path.write_text(text,encoding='utf-8-sig')
path = root/'common/scripted_effects/chi_adm_provincial_development.txt'
text = path.read_text(encoding='utf-8-sig')
for grant in (5,10):
    text = text.replace(f'name = chi_adm_provincial_development_autonomy_grant value = {grant}', f'name = chi_adm_provincial_development_autonomy_grant value = chi_adm_provincial_development_grant_{grant}')
path.write_text(text,encoding='utf-8-sig')
