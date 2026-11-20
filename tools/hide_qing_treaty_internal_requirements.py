from pathlib import Path

root = Path(__file__).resolve().parents[1]
check = 'c:CHI = { NOT = { has_variable = chi_qing_treaty_pending } NOT = { has_variable = chi_qing_treaty_retry } }'
for relative in ('common/scripted_buttons/04_russia_buttons.txt', 'tools/build_qing_treaty_approval.py'):
    path = root / relative
    text = path.read_text(encoding='utf-8')
    text = text.replace(check, 'hidden_trigger = { ' + check + ' }')
    path.write_text(text, encoding='utf-8')
