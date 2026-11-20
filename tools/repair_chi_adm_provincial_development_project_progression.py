from pathlib import Path
import validate_chi_adm as c
R=c.ROOT
def read(p):return c.parse((R/p).read_text(encoding='utf-8-sig'))
def render(items,depth=0):
    lines=[]
    for key,op,val in items:
        prefix='\t'*depth+key+' '+op+' '
        lines.append(prefix+'{\n'+render(val,depth+1)+'\n'+'\t'*depth+'}' if isinstance(val,list) else prefix+val)
    return '\n'.join(lines)
bp='common/scripted_buttons/chi_adm_provincial_development_extension.txt';ep='common/scripted_effects/chi_adm_provincial_development_extension.txt'
b=read(bp);e=read(ep);bd={k:v for k,_,v in b};ed={k:v for k,_,v in e}
for branch in ('military','economic','administrative'):
    variable='chi_adm_provincial_development_'+branch
    for tier,gain in [(1,2),(2,3),(3,4)]:
        key=f'chi_adm_provincial_development_start_{branch}_{tier}'
        old=c.get(bd[key],'possible')
        # Replace only the old all-states tier test, preserving literacy/technology.
        gate=[x for x in old if x[0] != 'NOT']
        if tier==1:
            gate+=c.parse(f'any_scope_state = {{ NOT = {{ has_variable = {variable} }} }}')
        else:
            gate+=c.parse(f'any_scope_state = {{ var:{variable} = {tier-1} }} NOT = {{ any_scope_state = {{ OR = {{ NOT = {{ has_variable = {variable} }} var:{variable} < {tier-1} }} }} }}')
        bd[key][:]=[(k,op,gate if k in ('possible','visible') else v) for k,op,v in bd[key]]
        body=c.get(ed[key],'if')
        body[:]=[(k,op,gate if k=='limit' else v) for k,op,v in body]
        states=c.get(body,'every_scope_state')
        states.insert(0,('limit','=',c.parse(f'OR = {{ NOT = {{ has_variable = {variable} }} var:{variable} < {tier} }}')))
        # Record actual room at the cap before applying political costs.
        body.insert(1,('set_variable','=',c.parse(f'name = chi_adm_provincial_development_project_autonomy_grant value = {{ value = 100 subtract = var:chi_adm_autonomy min = 0 max = {gain} }}')))
# Takeover never refunds political costs paid by the previous governor.
c.get(ed['chi_adm_provincial_development_takeover'],'if').insert(1,('remove_variable','=','chi_adm_provincial_development_project_autonomy_grant'))
for p,tree in [(bp,b),(ep,e)]: (R/p).write_text(render(tree)+'\n',encoding='utf-8-sig')
p=R/ep;s=p.read_text(encoding='utf-8-sig')
# Replace the two original fixed sponsorship refunds with one cap-safe value.
start=s.index('chi_adm_provincial_development_accept_sponsor = {');end=s.index('\nchi_adm_provincial_development_decline_sponsor',start)
block=s[start:end]
block=block.replace('AMOUNT = -2','AMOUNT = chi_adm_provincial_development_sponsor_refund_3').replace('AMOUNT = -1','AMOUNT = chi_adm_provincial_development_sponsor_refund_12')
s=s[:start]+block+s[end:];p.write_text(s,encoding='utf-8-sig')
p=R/'common/script_values/chi_adm_provincial_development_extension.txt';s=p.read_text(encoding='utf-8-sig')
s+='''
chi_adm_provincial_development_sponsor_refund_3 = { value = var:chi_adm_provincial_development_project_autonomy_grant subtract = 2 min = 0 multiply = -1 }
chi_adm_provincial_development_sponsor_refund_12 = {
 value = var:chi_adm_provincial_development_project_autonomy_grant
 if = { limit = { var:chi_adm_provincial_development_current_tier = 1 } subtract = 1 }
 else = { subtract = 2 }
 min = 0
 multiply = -1
}
''';p.write_text(s,encoding='utf-8-sig')
