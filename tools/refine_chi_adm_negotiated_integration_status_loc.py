from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
updates = {
 'stage_display': "#gold #bold [Country.GetCustom('chi_adm_negotiated_integration_stage')]#!#!\n[Country.GetCustom('chi_adm_negotiated_integration_response')]\n[Country.GetCustom('chi_adm_negotiated_integration_activity')]",
 'response_default': '#bold Provincial reply:#! No counterproposal.',
 'activity_2': '#bold Status:#! #g Implementation active#!\n@aut! #r −10%#! [concept_authority] and @bur! #r −10%#! [concept_bureaucracy] committed by the [concept_overlord]. Agreed payments continue.',
 'activity_1': '#bold Status:#! #v Suspended#!\nProgress retained; resource commitments and payments paused.',
 'activity_default': '#bold Status:#! Negotiations\nNo implementation costs or payments yet.',
 'terms_display': "#gold #bold Terms of agreement#!#!\n[Country.GetCustom('chi_adm_negotiated_integration_subsidy')]\n\n[Country.GetCustom('chi_adm_negotiated_integration_protection')]\n\n[Country.GetCustom('chi_adm_negotiated_integration_honors')]",
 'subsidy_default': '@money! #bold Financial support:#! None offered.',
 'subsidy_0': '@money! #bold Financial support:#! #g 20%#! of provincial [concept_treasury] income, paid weekly during active implementation.',
 'subsidy_1': '@money! #bold Financial support:#! #g 10%#! of provincial [concept_treasury] income, paid weekly during active implementation.',
 'protection_default': '#bold Fiscal privileges:#! None offered.',
 'protection_0': "#bold Fiscal privileges:#! [GetStaticModifier('chi_adm_negotiated_integration_local_privileges').GetName|v]\nTax Collection: #r −20%#! after annexation, fading over #v 10 years#!.",
 'protection_1': "#bold Fiscal privileges:#! [GetStaticModifier('chi_adm_negotiated_integration_local_privileges').GetName|v]\nTax Collection: #r −10%#! after annexation, fading over #v 5 years#!.",
 'honors_0': "#bold Imperial honors:#! [GetStaticModifier('chi_adm_negotiated_integration_honored').GetName|v]\nGovernor: #g +10#! [concept_popularity] and #g +10#! [concept_prominence] for #v 10 years#!.\nUpon agreement: @chi_adm_loyalty! [concept_chi_adm_loyalty] #g +3#!; [concept_relations] #g +5#!.\nCourt cost: [GetStaticModifier('chi_adm_negotiated_integration_honors_patronage').GetName|v] — @aut! #r −50#! [concept_authority] for #v 5 years#!.",
 'honors_default': '#bold Imperial honors:#! None offered.',
 'waiting_default': '#bold Consent:#! Peaceful annexation requires provincial agreement.',
 'requests_0': '#bold Pending petition:#! @money! Financial support.',
 'requests_1': '#bold Pending petition:#! Fiscal privileges.',
 'requests_2': '#bold Pending petition:#! Imperial honors.',
 'requests_default': '#bold Pending petition:#! None.',
 'progress_display': "#gold #bold Implementation progress#!#!\n#v [Country.MakeScope.Var('chi_adm_negotiated_integration_elapsed').GetValue|0]#! / #v [Country.MakeScope.ScriptValue('chi_adm_negotiated_integration_required')|0]#! monthly reviews completed.\n#bold First half:#! Census and registration.\n#bold Second half:#! Bureaucratic transition.\nConcurrent commissions adjust the required duration; completed reviews are retained.",
}
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
for key, value in updates.items():
    line = f' chi_adm_negotiated_integration_{key}: "' + value.replace('\n', r'\n') + '"'
    text, count = re.subn(r'^ chi_adm_negotiated_integration_' + key + r':.*$', lambda _: line, text, flags=re.M)
    assert count == 1, key
path.write_text(text, encoding='utf-8-sig')
