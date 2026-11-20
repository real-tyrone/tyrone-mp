from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
p='common/static_modifiers/chi_adm_provincial_development_extension.txt';s=r(p)+'''
chi_adm_provincial_development_project_inspection = {
icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_negative.dds
country_authority_mult = -0.025
}
''';w(p,s)
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=r(p)
start=s.index('chi_adm_provincial_development_accept_sponsor = {');pos=s.index('every_scope_state = {',start);s=s[:pos]+'add_modifier = { name = chi_adm_provincial_development_project_inspection }\n'+s[pos:]
s=s.replace('chi_adm_provincial_development_refresh_payments = {','''chi_adm_provincial_development_refresh_payments = {
    if = { limit = { NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_project_sponsored } } } remove_modifier = chi_adm_provincial_development_project_inspection }
''',1)
start=s.index('chi_adm_provincial_development_censure = {');pos=s.index('limit = {',start)+len('limit = {');s=s[:pos]+' NOT = { has_modifier = chi_adm_provincial_development_sanctions } '+s[pos:]
w(p,s)
for p in ['common/scripted_buttons/chi_adm_provincial_development_extension.txt','common/scripted_guis/chi_adm_provincial_development_extension.txt']:
    s=r(p);start=s.index('chi_adm_provincial_development_censure = {');end=s.find('\nchi_adm_provincial_development_',start+1)
    if end<0:end=len(s)
    block=s[start:end].replace('chi_adm_target_valid = yes','chi_adm_target_valid = yes NOT = { has_modifier = chi_adm_provincial_development_sanctions }')
    s=s[:start]+block+s[end:];w(p,s)
# Province emergency JE now displays the same current-state dossier.
p='common/journal_entries/chi_adm_provincial_development.txt';s=r(p).replace('context = country','''context = country
    widget = { gui = "gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui" name = "chi_adm_provincial_development_status" container = "custom_widget_container_1" }''',1);w(p,s)
p='localization/english/chi_adm_l_english.yml';s=r(p)
s+='\n chi_adm_provincial_development_project_inspection: "Imperial Project Inspectors"\n'
s=s.replace('Accept inspections and shared funding. Shortens total work','Accept [GetStaticModifier(\'chi_adm_provincial_development_project_inspection\').GetName|v] and shared funding. Shortens total work')
w(p,s)
# Every provincial development JE owns an explicit invalidation condition; projects remain accessible
# to successor owners until they complete or are explicitly abandoned.
for p in ['common/journal_entries/chi_adm_provincial_development_extension.txt']:
    s=r(p)
    # Operate on parsed top-level blocks without changing their existing widgets.
    cursor=0
    while True:
        match=re.search(r'(?m)^chi_adm_provincial_development_\w+ = \{',s[cursor:])
        if not match:break
        start=cursor+match.start();opening=s.index('{',start);end=opening+1;depth=1
        while depth:
            depth+=(s[end]=='{')-(s[end]=='}');end+=1
        block=s[start:end]
        condition='c:CHI ?= this chi_adm_court_valid = yes' if 'chi_adm_provincial_development_court_extension =' in block else 'OR = { chi_adm_target_valid = yes any_scope_state = { has_variable = chi_adm_provincial_development_project } }'
        if 'outcome = {' not in block:
            block=block[:-1]+'\noutcome = { flags = { hidden invalid_outcome } conclusion_desc = chi_adm_provincial_development_closed trigger = { NOT = { '+condition+' } } }\n}'
            s=s[:start]+block+s[end:];end=start+len(block)
        cursor=end
    w(p,s)
