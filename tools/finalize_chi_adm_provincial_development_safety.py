from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
for p in ['common/scripted_effects/chi_adm_provincial_development_extension.txt','common/scripted_buttons/chi_adm_provincial_development_extension.txt']:
    s=r(p)
    s=s.replace('NOT = { has_variable = chi_adm_provincial_development_sponsor_case }','NOT = { has_variable = chi_adm_provincial_development_sponsor_case } NOT = { has_variable = chi_adm_provincial_development_sponsor_retry }')
    if 'scripted_effects' in p:
        key='chi_adm_provincial_development_decline_sponsor = {';start=s.index(key);end=s.index('\n}',start)
        block=s[start:end].replace('remove_variable = chi_adm_provincial_development_sponsor_case','remove_variable = chi_adm_provincial_development_sponsor_case set_variable = { name = chi_adm_provincial_development_sponsor_retry value = yes months = 12 }')
        s=s[:start]+block+s[end:]
        key='chi_adm_provincial_development_decline_conversion = {';start=s.index(key);end=s.index('\n}',start)
        block=s[start:end].replace('remove_variable = chi_adm_provincial_development_conversion','remove_variable = chi_adm_provincial_development_conversion set_variable = { name = chi_adm_provincial_development_conversion_retry value = yes months = 12 }')
        s=s[:start]+block+s[end:]
    w(p,s)
p='common/scripted_triggers/chi_adm_provincial_development_extension.txt';s=r(p).replace('NOT = { has_variable = chi_adm_provincial_development_conversion }','NOT = { has_variable = chi_adm_provincial_development_conversion } NOT = { has_variable = chi_adm_provincial_development_conversion_retry }');w(p,s)
# Native events keep player agency; AI acceptance responds to existing account values.
p='events/chi_adm_provincial_development_extension.txt';s=r(p)
s=re.sub(r'(name = chi_adm_provincial_development_accept_\w+.*?ai_chance = \{ base = \d+)( \})',r'\1 modifier = { trigger = { var:chi_adm_loyalty >= 70 } factor = 2 } modifier = { trigger = { var:chi_adm_autonomy >= 60 } factor = 0.5 }\2',s,flags=re.S)
w(p,s)
# No inactive annexation placeholder is displayed as progress.
p='common/scripted_guis/chi_adm_provincial_development_extension.txt';s=r(p)+'''
chi_adm_provincial_development_project_visible = { scope = country is_valid = { any_scope_state = { has_variable = chi_adm_provincial_development_project } } }
chi_adm_provincial_development_conversion_visible = { scope = country is_valid = { var:chi_adm_provincial_development_conversion > 0 } }
''';w(p,s)
p='gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui';s=r(p)
lines=s.splitlines()
for i,line in enumerate(lines):
    if 'progressbar = {' in line:
        key='project' if 'project_progress' in line else 'conversion'
        lines[i]=line.replace('progressbar = {',f'''progressbar = {{ visible = "[GetScriptedGui('chi_adm_provincial_development_{key}_visible').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"''',1)
w(p,'\n'.join(lines)+'\n')
# Current roster assertion, not a hardcoded historical subject count.
p='tools/validate_chi_adm_imperial_law.py';s=r(p).replace('len(eligible) == 15','len(eligible) == len(core.TAGS)');w(p,s)
# Accurate test output avoids claiming the archived 15-country snapshot is current.
for p in ['tools/validate_chi_adm.py','tools/validate_chi_adm_court_register.py','tools/validate_chi_adm_government_titles.py','tools/validate_chi_adm_memorials.py','tools/validate_chi_adm_negotiated_integration.py']:
    s=r(p).replace('15 x 240','13 x 240').replace('15-subject','current-roster').replace('15 subjects','13 subjects').replace('15 offices','13 offices').replace('all 15 proposal','all 13 proposal')
    w(p,s)
print('Added replay cooldowns, AI account weights and valid progress visibility.')
