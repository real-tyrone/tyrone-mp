from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=r(p)
# Record and pay actual sponsorship only during eligible, solvent development.
s=s.replace('chi_adm_provincial_development_extension_monthly = {','''chi_adm_provincial_development_extension_monthly = {
if = { limit = { NOT = { chi_adm_target_valid = yes } }
 remove_variable = chi_adm_provincial_development_sponsor_case
 remove_variable = chi_adm_provincial_development_compact_case
 remove_variable = chi_adm_provincial_development_compact_offer
 remove_variable = chi_adm_provincial_development_crisis_demand
 remove_variable = chi_adm_provincial_development_conversion
 remove_variable = chi_adm_provincial_development_conversion_agreed
 remove_variable = chi_adm_provincial_development_conversion_repudiated
}
if = { limit = { c:CHI ?= this has_variable = chi_adm_provincial_development_enforcement NOT = { any_country = { has_variable = chi_adm_provincial_development_enforcement_target } } } remove_variable = chi_adm_provincial_development_enforcement }
''',1)
# Ensure every improved tier also requires actual provincial development.
for branch in ['military','economic','administrative']:
    for tier,lit in [(2,.25),(3,.40)]:
        key='chi_adm_provincial_development_start_'+branch+'_'+str(tier)+' = {'
        start=s.index(key);pos=s.index('limit = {',start)+len('limit = {');s=s[:pos]+f' literacy >= {lit} '+s[pos:]
w(p,s)
p='common/scripted_buttons/chi_adm_provincial_development_extension.txt';s=r(p)
for branch in ['military','economic','administrative']:
    for tier,lit in [(2,.25),(3,.40)]:
        start=s.index('chi_adm_provincial_development_start_'+branch+'_'+str(tier)+' = {');end=s.find('\nchi_adm_provincial_development_',start+1)
        if end<0:end=len(s)
        block=s[start:end].replace('visible = {','visible = { literacy >= '+str(lit),1).replace('possible = {','possible = { literacy >= '+str(lit),1)
        s=s[:start]+block+s[end:]
w(p,s)
# MCH's modernized office receives its historically reserved title.
p='common/government_types/00_00_chi_adm_government_types.txt';s=r(p)
s=s.replace('c:YUN ?= this c:SIH ?= this c:MCH ?= this }','c:YUN ?= this c:SIH ?= this }',1)
s+='''
chi_adm_government_titles_gov_manchurian_viceroyalty = {
 transfer_of_power = hereditary
 male_ruler = chi_adm_provincial_development_title_manchurian_viceroy
 female_ruler = chi_adm_provincial_development_title_manchurian_viceroy
 male_heir = ""
 female_heir = ""
 possible = {
  c:MCH ?= this
  exists = c:CHI
  c:CHI = { has_law_or_variant = law_type:law_monarchy }
  is_direct_subject_of = c:CHI
  is_subject_type = subject_type_qing_viceroyalty_administration
  has_law_or_variant = law_type:law_monarchy
  has_gov_regency = no
 }
}
'''
w(p,s)
p='common/customizable_localization/chi_adm_court_register_gui.txt';s=r(p)
s=s.replace('chi_adm_court_register_office_title = {\n type = country','''chi_adm_court_register_office_title = {
 type = country
 text = { trigger = { c:MCH ?= this is_subject_type = subject_type_qing_frontier_administration } localization_key = chi_adm_court_register_title_manchuria }
 text = { trigger = { c:MCH ?= this is_subject_type = subject_type_qing_viceroyalty_administration } localization_key = chi_adm_provincial_development_title_manchurian_viceroy }''')
s=s.replace('trigger = { c:XIN ?= this }','trigger = { c:XIN ?= this is_subject_type = subject_type_qing_frontier_administration }').replace('trigger = { c:MGL ?= this }','trigger = { c:MGL ?= this is_subject_type = subject_type_qing_frontier_administration }')
w(p,s)
p='localization/english/chi_adm_l_english.yml';s=r(p)
for key,value in {
'chi_adm_provincial_development_title_manchurian_viceroy':'Viceroy of the Three Eastern Provinces',
'chi_adm_government_titles_gov_manchurian_viceroyalty':'Viceroyalty of the Three Eastern Provinces',
'chi_adm_government_titles_gov_manchurian_viceroyalty_desc':"Civil reorganization unifies the three northeastern generalships beneath an imperial viceroy. Existing regional compacts remain binding until separately renegotiated.\\n\\n$TRANSFER_OF_POWER_NAME_DESC$",
}.items():
 if not re.search(r'^ '+key+':',s,re.M):s+='\n '+key+': "'+value+'"\n'
w(p,s)
