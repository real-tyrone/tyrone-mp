from pathlib import Path
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
regions=[
(1,'pasture','Mongol League and Pasture Compact',['ULIASTAI','URGA','TUVA','ALTAI'],'state_tax_capacity_mult = 0.03 state_tax_collection_mult = -0.02'),
(2,'banners','Inner Mongolian Banner Compact',['ALXA','HINGGAN'],'state_infrastructure_add = 2 state_tax_collection_mult = -0.02'),
(3,'ili','Ili Garrison and Merchant Compact',['DZUNGARIA','TIANSHAN','JETISY','KIRGHIZIA'],'state_infrastructure_add = 2 state_tax_collection_mult = -0.02'),
(4,'xining','Xining Religious and Elite Compact',['QINGHAI'],'state_education_access_add = 0.02 state_tax_collection_mult = -0.02'),
(5,'manchuria','Eastern Generalships and Banner Compact',['SHENGJING','SOUTHERN_MANCHURIA','NORTHERN_MANCHURIA','OUTER_MANCHURIA','AMUR'],'state_tax_capacity_mult = 0.03 state_tax_collection_mult = -0.02'),
]
p='common/static_modifiers/chi_adm_provincial_development_extension.txt';s=r(p)
for n,key,title,states,body in regions:
    s+=f'\nchi_adm_provincial_development_regional_{key} = {{ icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds {body} }}\n'
w(p,s)
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=r(p)
marker='chi_adm_provincial_development_apply_compact_customs = {'
extra=''
for n,key,title,states,body in regions:
    conditions=' '.join('state_region = s:STATE_'+state for state in states)
    extra+=f'''\nif = {{ limit = {{ var:chi_adm_provincial_development_compact_case = {n} }}
every_scope_state = {{ limit = {{ OR = {{ {conditions} }} }}
remove_modifier = chi_adm_provincial_development_regional_{key}
add_modifier = {{ name = chi_adm_provincial_development_regional_{key} years = 2 }}
}} }}'''
s=s.replace(marker,marker+extra,1);w(p,s)
p='common/customizable_localization/chi_adm_provincial_development_status.txt';s=r(p)+'\nchi_adm_provincial_development_compact_identity = { type = country\n'
for n,key,title,states,body in regions:s+=f'text = {{ trigger = {{ var:chi_adm_provincial_development_compact_case = {n} }} localization_key = chi_adm_provincial_development_regional_{key} }}\n'
s+='text = { trigger = { always = yes } localization_key = chi_adm_provincial_development_regional_none }\n}\n';w(p,s)
p='localization/english/chi_adm_l_english.yml';s=r(p)
for n,key,title,states,body in regions:s+=f'\n chi_adm_provincial_development_regional_{key}: "{title}"\n'
s+='\n chi_adm_provincial_development_regional_none: "Regional Customs"\n'
s=s.replace('Accepting changes only the specified administrative obligations; it does not overwrite local law.',"The proposal concerns [ROOT.GetCountry.GetCustom('chi_adm_provincial_development_compact_identity')]. Accepting changes only the specified administrative obligations; it does not overwrite local law.")
s=s.replace('Protect existing laws and customary institutions; gain Loyalty at the cost of local discretion.','Protect existing laws and customary institutions; gain Loyalty at the cost of local discretion. For two years, the affected region receives its distinct customary-administration modifier, with a modest institutional benefit and reduced Tax Collection.')
w(p,s)
