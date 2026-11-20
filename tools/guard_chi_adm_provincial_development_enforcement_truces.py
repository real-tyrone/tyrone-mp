from pathlib import Path
import re
R=Path(__file__).resolve().parents[1]
for relative in ('common/scripted_effects/chi_adm_provincial_development_extension.txt','common/scripted_buttons/chi_adm_provincial_development_extension.txt','common/scripted_guis/chi_adm_provincial_development_extension.txt'):
    p=R/relative;s=p.read_text(encoding='utf-8-sig')
    start=s.index('chi_adm_provincial_development_enforce = {');opening=s.index('{',start);end=opening+1;depth=1
    while depth:depth+=(s[end]=='{')-(s[end]=='}');end+=1
    block=s[start:end]
    block=block.replace('chi_adm_target_valid = yes','chi_adm_target_valid = yes NOT = { has_truce_with = c:CHI }')
    s=s[:start]+block+s[end:];p.write_text(s,encoding='utf-8-sig')
