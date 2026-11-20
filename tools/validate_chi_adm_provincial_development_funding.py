"""Bounded arithmetic/definition checks for paired project sponsorship."""
import validate_chi_adm as core
from pathlib import Path
R=core.ROOT
values=core.definitions('common/script_values/chi_adm_provincial_development_extension.txt')
def number(raw, context):
    if isinstance(raw,list):return evaluate(raw,context)
    if raw in values:return evaluate(values[raw],context)
    if raw.startswith('var:'):return context[raw[4:]]
    if raw in context:return context[raw]
    return float(raw)
def evaluate(items,context):
    total=0
    for key,_,raw in items:
        if key=='if':continue # gated cases separately assert zero funding in source.
        if key=='every_scope_state':
            gate=core.get(raw,'limit')
            assert ('var:chi_adm_provincial_development_project_owner','?=','owner') in gate
            sponsored=('has_variable','=','chi_adm_provincial_development_project_sponsored') in gate
            for state in context['states']:
                if not sponsored or state['sponsored']:
                    total+=evaluate(raw[1:],state)
            continue
        value=number(raw,context)
        if key=='value':total=value
        elif key=='multiply':total*=value
        elif key=='add':total+=value
        elif key=='divide':total/=value
        elif key=='min':total=max(total,value)
        elif key=='max':total=min(total,value)
        else:raise AssertionError(key)
    return total
cases=0
for income in (0,100,10000,1000000):
    for tier in (1,2,3):
        for share in (0,.01,.25,.5,1):
            state = {
                'chi_adm_provincial_development_project_tier': tier,
                'state_population': int(100000 * share),
                'owner.total_population': 100000,
                'sponsored': True,
            }
            ctx = {'fixed_income': income, 'states': [state]}
            cost=number('chi_adm_provincial_development_project_bill',ctx)
            credit=number('chi_adm_provincial_development_sponsored_bill',ctx)
            assert abs(cost - income * share * 0.20) < 1e-8
            assert 0<=credit<=cost/2+1e-8
            assert abs(cost-credit-cost/2)<1e-8
            cases+=1
assert core.get(core.definitions('common/static_modifiers/chi_adm_provincial_development_extension.txt')['chi_adm_provincial_development_sponsorship_credit'],'country_expenses_add')=='-1'
assert core.get(core.definitions('common/static_modifiers/chi_adm_provincial_development_extension.txt')['chi_adm_provincial_development_sponsorship_cost'],'country_expenses_add')=='1'
effect=(R/'common/scripted_effects/chi_adm_provincial_development_extension.txt').read_text(encoding='utf-8-sig')
effect=' '.join(effect.split())
assert 'create_diplomatic_pact' not in effect
assert all('remove_diplomatic_pact = { country = scope:chi_adm_provincial_development_payee type = chi_adm_provincial_development_sponsorship_'+str(i) in effect for i in (1,2,3))
print(f'PASS provincial development funding: {cases} income/tier/territorial-share cases; sponsorship exactly half of matching costs, balanced signed native budget modifiers and legacy pact cleanup.')
