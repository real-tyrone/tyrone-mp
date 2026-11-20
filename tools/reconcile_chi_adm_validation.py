"""Explicit, reasoned compatibility layer for approved post-baseline changes.

Historical baselines remain untouched. New fingerprints cover only named files
with an authorized migration reason; semantic assertions still run afterward.
"""
from pathlib import Path
import json,hashlib,ast,re
R=Path(__file__).resolve().parents[1]
reasons={
'common/scripted_triggers/chi_adm_core.txt':'User-added Russian treaty-partner predicate; original core eligibility remains intact.',
'common/history/global/zzzz_qing_administrations.txt':'User merged Henan/Inner Mongolia/Xining, added MCH and Amur, and migrated canonical tags.',
'common/scripted_effects/chi_adm_core.txt':'User requested special MCH initial accounts; preserve other core effects.',
'common/scripted_triggers/tyrone_qing_administrations.txt':'Current 13-office roster and removed military subject type.',
'common/country_definitions/tyrone_qing_administrations.txt':'Canonical tag migration, XIB Ningxia/Mongol, FRS Han/Min.',
'common/subject_types/tyrone_qing_administrations.txt':'Removed military subject type; allow frontier transfers.',
'common/diplomatic_actions/tyrone_qing_administrations.txt':'Removed military administration pact; preserve 20%/15% rates.',
'common/government_types/00_00_chi_adm_government_types.txt':'MCH generalships and provincial development negotiated civil/viceroyalty conversion.',
'common/scripted_triggers/chi_adm_government_titles_eligibility.txt':'MCH and converted frontier native government exclusions.',
'common/dynamic_country_names/tyrone_qing_administrations.txt':'Conditional canonical names and standalone XIB/FRS blocks.',
'common/coat_of_arms/coat_of_arms/tyrone_qing_administrations.txt':'User removed custom viceroyalty flags.',
'common/scripted_buttons/tyrone_qing_administrations.txt':'negotiated integration negotiated canonical-tag proposal entrypoints.',
'common/journal_entries/tyrone_qing_administrations.txt':'User merged the integration JE with imperial administrations.',
'common/scripted_effects/chi_adm_negotiated_integration.txt':'Canonical roster, current fiscal duration, agreed offers and provincial development guarantee gate.',
'common/scripted_triggers/chi_adm_negotiated_integration.txt':'Autonomy gate and provincial development coercion guarantee.',
'common/scripted_guis/chi_adm_negotiated_integration.txt':'Approved tooltip refinements, native modifier previews and guarantee gate.',
}
records={p:{'sha256':hashlib.sha256((R/p).read_bytes()).hexdigest(),'reason':reason} for p,reason in reasons.items()}
(R/'tools/chi_adm_authorized_migrations.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
for filename in ['validate_chi_adm.py','validate_chi_adm_court_register.py','validate_chi_adm_government_titles.py','validate_chi_adm_imperial_law.py','validate_chi_adm_memorials.py','validate_chi_adm_negotiated_integration.py']:
    p=R/'tools'/filename;s=p.read_text(encoding='utf-8');tree=ast.parse(s);lines=s.splitlines();edits=[]
    for node in ast.walk(tree):
        if isinstance(node,ast.Assert) and node.lineno==node.end_lineno:
            line=lines[node.lineno-1]
            if 'hexdigest()' in line and 'authorized_current' not in line and 'path' in line:
                test=ast.get_source_segment(s,node.test)
                edits.append((node.lineno-1,line.replace('assert '+test,'assert ('+test+') or authorized_current(path)',1)))
    for i,line in edits:lines[i]=line
    if edits and 'from chi_adm_authorized_validation import authorized_current' not in s:
        lines.insert(0,'from chi_adm_authorized_validation import authorized_current')
    s='\n'.join(lines)+'\n'
    if filename=='validate_chi_adm.py':
        s=s.replace('ZHI AHU HNA YUE FRS XIB YUN SIH SHN SHA QHN MGL QIM XIN QXN','ZHI AHU HNA YUE FRS XIB YUN SIH SHN SHA MGL XIN MCH').replace('MGL QIM XIN QXN','MGL XIN MCH')
        s=s.replace('len(pacts) == 15','len(pacts) == len(TAGS)').replace('["0.20", "0.20", "0.15", "0.15"]','["0.20", "0.20", "0.15"]')
        s=s.replace('"chi_adm_negotiated_integration_"))','"chi_adm_negotiated_integration_", "chi_adm_provincial_development_", "chi_adm_subject_"))')
    if filename=='validate_chi_adm_court_register.py':s=s.replace('len(visible) == 15','len(visible) == len(foundation.TAGS)')
    if filename=='validate_chi_adm_government_titles.py':
        s=s.replace('== 15 and set(pacts)', '== len(foundation.TAGS) and set(pacts)')
        s=s.replace('"xining_commission": "Imperial Minister",','"xining_commission": "Imperial Minister", "manchurian_generalships": "General of Shengjing",')
    p.write_text(s,encoding='utf-8')
print('Recorded named authorized migrations without replacing historical baseline data.')
