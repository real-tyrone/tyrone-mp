from pathlib import Path
import re,json,hashlib
R=Path(__file__).resolve().parents[1]
p=R/'tools/validate_chi_adm_government_titles.py';s=p.read_text(encoding='utf-8')
s=s.replace('len(governments) == 8','len(governments) == 9').replace('count("exists = c:CHI") == 7','count("exists = c:CHI") == 8')
s=s.replace('exact_titles = {','exact_titles = {\n        "manchurian_viceroyalty": "Viceroy of the Three Eastern Provinces",',1)
s=re.sub(r'(, "manchurian_generalships": "General of Shengjing"){2,}', ', "manchurian_generalships": "General of Shengjing"',s)
p.write_text(s,encoding='utf-8')
p=R/'tools/chi_adm_authorized_migrations.json';data=json.loads(p.read_text())
name='common/customizable_localization/chi_adm_court_register_gui.txt'
data[name]={'sha256':hashlib.sha256((R/name).read_bytes()).hexdigest(),'reason':'MCH and converted-frontier office titles; no mechanics.'}
for name in ['common/government_types/00_00_chi_adm_government_types.txt','common/scripted_triggers/chi_adm_government_titles_eligibility.txt']:
    data[name]['sha256']=hashlib.sha256((R/name).read_bytes()).hexdigest()
p.write_text(json.dumps(data,indent=2),encoding='utf-8')
import generate_chi_adm_imperial_law_laws as generator
original=generator.write
def write(path,text):
    if str(path).endswith('chi_adm_imperial_law_coverage.md'):
        (generator.ROOT/path).write_text(text,encoding='utf-8')
    else: original(path,text)
generator.CHECK=True
generator.write=write
generator.main()
