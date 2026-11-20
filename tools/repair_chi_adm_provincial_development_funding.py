"""Replace fixed-rate sponsorship with exactly matched native budget modifiers."""
from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8-sig')
def span(s,key):
    start=s.index(key+' = {');i=s.index('{',start)+1;depth=1
    while depth:depth+=(s[i]=='{')-(s[i]=='}');i+=1
    return start,i
p='common/scripted_effects/chi_adm_provincial_development_extension.txt';s=read(p)
# Retain old pact definitions for loading saves, but never create another one.
pattern=r'create_diplomatic_pact = \{ country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_[123] \}'
s=re.sub(pattern,'hidden_effect = { }',s)
start,end=span(s,'chi_adm_provincial_development_refresh_payments')
s=s[:start]+'''chi_adm_provincial_development_refresh_payments = {
    if = { limit = { NOT = { any_scope_state = { has_variable = chi_adm_provincial_development_project_sponsored } } }
        remove_modifier = chi_adm_provincial_development_project_inspection
    }
    # Existing-save migration: cancel legacy whole-income grants before matched funding.
    save_scope_as = chi_adm_provincial_development_payee
    c:CHI ?= {
        remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_1 }
        remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_2 }
        remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_3 }
    }
}'''+s[end:];write(p,s)
p='common/script_values/chi_adm_provincial_development_extension.txt';s=read(p);start,end=span(s,'chi_adm_provincial_development_sponsored_bill')
s=s[:start]+'''chi_adm_provincial_development_sponsored_bill = {
    value = fixed_income
    multiply = var:chi_adm_provincial_development_sponsor_weight
    multiply = 0.025
    min = 0
    max = { value = chi_adm_provincial_development_project_bill multiply = 0.5 }
    if = {
        limit = { OR = { NOT = { chi_adm_target_valid = yes } NOT = { chi_adm_provincial_development_project_affordable = yes } c:CHI = { gold_reserves < 0 } } }
        multiply = 0
    }
}'''+s[end:]
s+='''
chi_adm_provincial_development_court_sponsorship_bill = {
    value = 0
    every_subject_or_below = {
        limit = { chi_adm_target_valid = yes }
        add = chi_adm_provincial_development_sponsored_bill
    }
}
''';write(p,s)
p='common/static_modifiers/chi_adm_provincial_development_extension.txt';s=read(p)+'''
chi_adm_provincial_development_sponsorship_credit = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_positive.dds
    country_expenses_add = -1
}
chi_adm_provincial_development_sponsorship_cost = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_coins_negative.dds
    country_expenses_add = 1
}
''';write(p,s)
p='common/journal_entries/chi_adm_provincial_development_extension.txt';s=read(p)
s=s.replace('scaling_modifiers_while_active = { modifier = chi_adm_provincial_development_project_expense value = chi_adm_provincial_development_project_bill }','''scaling_modifiers_while_active = { modifier = chi_adm_provincial_development_project_expense value = chi_adm_provincial_development_project_bill }
scaling_modifiers_while_active = { modifier = chi_adm_provincial_development_sponsorship_credit value = chi_adm_provincial_development_sponsored_bill }''',1)
start=s.index('chi_adm_provincial_development_court_extension = {');pos=s.index('\n',start)+1
s=s[:pos]+'scaling_modifiers_while_active = { modifier = chi_adm_provincial_development_sponsorship_cost value = chi_adm_provincial_development_court_sponsorship_bill }\n'+s[pos:];write(p,s)
p='localization/english/chi_adm_l_english.yml';s=read(p)
s+='\n chi_adm_provincial_development_sponsorship_credit: "Imperial Project Contribution"\n chi_adm_provincial_development_sponsorship_cost: "Provincial Development Sponsorship"\n';write(p,s)
