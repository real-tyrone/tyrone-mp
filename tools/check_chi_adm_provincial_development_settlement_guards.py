from pathlib import Path
R=Path(__file__).resolve().parents[1]
def read(p):return (R/p).read_text(encoding='utf-8-sig')
def write(p,s):(R/p).write_text(s,encoding='utf-8-sig')
p='common/war_goal_types/chi_adm_provincial_development.txt';s=read(p)
s=s.replace('possible = { scope:target_country = { has_variable = chi_adm_provincial_development_enforcement_target } }','possible = { c:CHI ?= root scope:target_country = { has_variable = chi_adm_provincial_development_enforcement_target } }')
s=s.replace('valid = { scope:target_country = { has_variable = chi_adm_provincial_development_enforcement_target } }','valid = { c:CHI ?= root scope:target_country = { has_variable = chi_adm_provincial_development_enforcement_target } }')
s=s.replace('possible = { always = yes }','possible = { has_variable = chi_adm_provincial_development_enforcement_target scope:target_country = { c:CHI ?= this } }')
s=s.replace('valid = { always = yes }','valid = { has_variable = chi_adm_provincial_development_enforcement_target scope:target_country = { c:CHI ?= this } }')
write(p,s)
p='events/chi_adm_negotiated_integration.txt';s=read(p)
key='option = { name = chi_adm_negotiated_integration_coerce '
pos=s.index(key);target=s.index('scope:chi_adm_negotiated_integration_target = {',pos)+len('scope:chi_adm_negotiated_integration_target = {')
if 'has_modifier = chi_adm_provincial_development_guarantee' not in s[target:target+90]:s=s[:target]+' NOT = { has_modifier = chi_adm_provincial_development_guarantee } '+s[target:]
write(p,s)
p='common/scripted_triggers/chi_adm_provincial_development.txt';s=read(p)
s=s.replace('OR = { is_at_war = yes any_scope_state = { turmoil >= 0.40 } }','OR = { is_at_war = yes has_any_secessionists_broken_out = yes any_scope_state = { turmoil >= 0.40 } }')
write(p,s)
