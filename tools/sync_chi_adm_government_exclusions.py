from pathlib import Path
import validate_chi_adm as c
root=Path(__file__).resolve().parents[1]
def render(items,level=0):
    lines=[]
    for key,op,value in items:
        if isinstance(value,list):lines.append(' '*level+key+' '+op+' {\n'+render(value,level+1)+'\n'+' '*level+'}')
        else:lines.append(' '*level+key+' '+op+' '+value)
    return '\n'.join(lines)
governments=c.definitions('common/government_types/00_00_chi_adm_government_types.txt')
branches=[('AND','=',c.get(body,'possible')) for key,body in governments.items() if key!='chi_adm_government_titles_gov_celestial_empire']
path=root/'common/scripted_triggers/chi_adm_government_titles_eligibility.txt'
path.write_text(render([('chi_adm_government_titles_office_government_available','=',[('OR','=',branches)])])+'\n',encoding='utf-8')
