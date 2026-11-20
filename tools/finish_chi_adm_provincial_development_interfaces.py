from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def r(p):return (R/p).read_text(encoding='utf-8-sig')
def w(p,s):(R/p).write_text(s,encoding='utf-8-sig')
# Court can initiate regional reviews, not only answer governor petitions.
import validate_chi_adm as c
buttons=c.definitions('common/scripted_buttons/chi_adm_provincial_development_extension.txt')
p='common/scripted_guis/chi_adm_provincial_development_extension.txt';s=r(p)
for n in range(1,6):
    key=f'chi_adm_provincial_development_compact_{n}'
    def serialize(items):return ' '.join(k+' '+op+' '+('{ '+serialize(v)+' }' if isinstance(v,list) else v) for k,op,v in items)
    s+=key+' = { scope = country is_valid = { '+serialize(c.get(buttons[key],'possible'))+' } effect = { '+key+' = yes } }\n'
w(p,s)
p='gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui';s=r(p)
marker='textbox = { size = { 440 0 } max_width = 440 autoresize = yes multiline = yes text = "[Country.GetName]" }'
controls=''
for n in range(1,6):
    key=f'chi_adm_provincial_development_compact_{n}'
    controls+=f'''\nbutton = {{ size = {{ 440 48 }} using = default_button_action
visible = "[GetScriptedGui('{key}').IsValid(GuiScope.SetRoot(Country.MakeScope).End)]"
onclick = "[GetScriptedGui('{key}').Execute(GuiScope.SetRoot(Country.MakeScope).End)]"
tooltip = "[GetScriptedGui('{key}').ExecuteTooltip(GuiScope.SetRoot(Country.MakeScope).End)]"
textbox = {{ size = {{ 416 0 }} max_width = 416 autoresize = yes multiline = yes text = "{key}" }} }}'''
s=s.replace(marker,marker+controls,1);w(p,s)
# Resume an agreed sponsorship after a funding pause without another reward.
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=r(p)
start=s.index('chi_adm_provincial_development_refresh_payments = {');pos=s.index('\n    if',start)
resume='''
    if = { limit = { chi_adm_target_valid = yes chi_adm_provincial_development_project_affordable = yes c:CHI = { gold_reserves >= 0 } any_scope_state = { has_variable = chi_adm_provincial_development_project_sponsored } }
        save_scope_as = chi_adm_provincial_development_payee
        c:CHI = {
'''
for i in (1,2,3):
    resume+=f'''if = {{ limit = {{ scope:chi_adm_provincial_development_payee = {{ var:chi_adm_provincial_development_current_tier = {i} }} NOT = {{ has_diplomatic_pact = {{ who = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_{i} }} }} }} create_diplomatic_pact = {{ country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_{i} }} }}\n'''
resume+='} }\n'
s=s[:pos]+resume+s[pos:]
s=s.replace('NOT = { chi_adm_provincial_development_project_affordable = yes } } }','NOT = { chi_adm_provincial_development_project_affordable = yes } c:CHI = { gold_reserves < 0 } } }',1)
w(p,s)
# Guards for proposals expose concise custom terms, while native effects remain previews.
p='common/customizable_localization/chi_adm_provincial_development_status.txt'
w(p,'''chi_adm_provincial_development_conversion_status = {
type = country
text = { trigger = { var:chi_adm_provincial_development_conversion = -1 } localization_key = chi_adm_provincial_development_conversion_awaiting }
text = { trigger = { has_variable = chi_adm_provincial_development_conversion_repudiated } localization_key = chi_adm_provincial_development_conversion_disputed }
text = { trigger = { var:chi_adm_provincial_development_conversion > 0 } localization_key = chi_adm_provincial_development_conversion_active }
text = { trigger = { always = yes } localization_key = chi_adm_provincial_development_conversion_none }
}
chi_adm_provincial_development_emergency_status = {
type = country
text = { trigger = { has_variable = chi_adm_provincial_development_dispute } localization_key = chi_adm_provincial_development_emergency_disputed }
text = { trigger = { var:chi_adm_provincial_development_case = 1 } localization_key = chi_adm_provincial_development_emergency_petition }
text = { trigger = { var:chi_adm_provincial_development_case = 2 } localization_key = chi_adm_provincial_development_emergency_counter }
text = { trigger = { var:chi_adm_provincial_development_case = 3 } localization_key = chi_adm_provincial_development_emergency_refused }
text = { trigger = { var:chi_adm_provincial_development_case = 4 } localization_key = chi_adm_provincial_development_emergency_restoration }
text = { trigger = { has_variable = chi_adm_provincial_development_package } localization_key = chi_adm_provincial_development_emergency_active }
text = { trigger = { always = yes } localization_key = chi_adm_provincial_development_emergency_none }
}
''')
p='localization/english/chi_adm_l_english.yml';s=r(p)
loc={
'conversion_awaiting':'#bold Civil government:#! Awaiting provincial consent.',
'conversion_disputed':'#bold Civil government:#! Agreed conversion repudiated; preparation paused.',
'conversion_active':"#bold Civil government:#! #v [Country.MakeScope.Var('chi_adm_provincial_development_conversion').GetValue|0]#! monthly reviews remain.",
'conversion_none':'#bold Civil government:#! No conversion in progress.',
'emergency_disputed':'#bold Emergency powers:#! Restoration disputed; the court may negotiate or enforce.',
'emergency_petition':'#bold Emergency powers:#! Petition before the imperial court.',
'emergency_counter':'#bold Emergency powers:#! Counterproposal awaits the governor.',
'emergency_refused':'#bold Emergency powers:#! Authorization refused; unilateral mobilization remains possible during danger.',
'emergency_restoration':'#bold Emergency powers:#! Return of exceptional powers awaits a decision.',
'emergency_active':'#bold Emergency powers:#! Military warrant active; post-crisis benefits expire after three months.',
'emergency_none':'#bold Emergency powers:#! No active warrant.',
}
for k,v in loc.items():s+='\n chi_adm_provincial_development_'+k+': "'+v+'"\n'
status="[Country.GetCustom('chi_adm_provincial_development_emergency_status')]\\n[Country.GetCustom('chi_adm_provincial_development_conversion_status')]\\nProject reviews: #v [Country.MakeScope.Var('chi_adm_provincial_development_display_done').GetValue|0]#! / #v [Country.MakeScope.Var('chi_adm_provincial_development_display_total').GetValue|0]#!.\\n@chi_adm_loyalty! [concept_chi_adm_loyalty]: #v [Country.MakeScope.Var('chi_adm_loyalty').GetValue|0]#!; @chi_adm_autonomy! [concept_chi_adm_autonomy]: #v [Country.MakeScope.Var('chi_adm_autonomy').GetValue|0]#!."
s=re.sub(r'^ chi_adm_provincial_development_status:.*$',lambda _: ' chi_adm_provincial_development_status: "'+status+'"',s,flags=re.M)
w(p,s)
# Every court row shows its actual target's status as well as conditional actions.
p='gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui';s=r(p).replace(marker,marker+'\ntextbox = { size = { 440 0 } max_width = 440 autoresize = yes multiline = yes text = "chi_adm_provincial_development_status" }',1);w(p,s)
