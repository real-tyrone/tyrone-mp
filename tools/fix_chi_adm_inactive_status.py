from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'common/customizable_localization/chi_adm_negotiated_integration.txt'
text = path.read_text(encoding='utf-8')
marker = 'chi_adm_negotiated_integration_activity = { type = country'
extra = ''' text = {
    trigger = { NOT = { has_variable = chi_adm_negotiated_integration_stage } has_variable = chi_adm_negotiated_integration_retry }
    localization_key = chi_adm_negotiated_integration_activity_cooldown
} text = {
    trigger = { NOT = { has_variable = chi_adm_negotiated_integration_stage } has_variable = chi_adm_negotiated_integration_repayment_left }
    localization_key = chi_adm_negotiated_integration_activity_repayment
} text = {
    trigger = { NOT = { has_variable = chi_adm_negotiated_integration_stage } }
    localization_key = chi_adm_negotiated_integration_activity_inactive
}'''
if 'localization_key = chi_adm_negotiated_integration_activity_inactive' not in text:
    text = text.replace(marker, marker + extra, 1)
path.write_text(text, encoding='utf-8')
path = root / 'localization/english/chi_adm_l_english.yml'
text = path.read_text(encoding='utf-8-sig')
if ' chi_adm_negotiated_integration_activity_inactive:' not in text:
    text += '''
 chi_adm_negotiated_integration_activity_cooldown: "#bold Status:#! #v Proposal closed — cooldown active#!\\nThere are no ongoing negotiations. Another proposal may be made when the withdrawal or settlement cooldown expires."
 chi_adm_negotiated_integration_activity_repayment: "#bold Status:#! #v Repayment settlement active#!\\nThere are no ongoing integration negotiations. New proposals are blocked until repayment ends."
 chi_adm_negotiated_integration_activity_inactive: "#bold Status:#! No active negotiations.\\nOpen a new proposal when its requirements are met."
'''
text = text.replace('@red_cross! A proposal, retry period or repayment case is already active.', '@red_cross! No active proposal, withdrawal/settlement cooldown or repayment case. Withdrawal normally blocks a new proposal for #v 6 months#!; a closer-centralization settlement blocks it for #v 12 months#!.')
path.write_text(text, encoding='utf-8-sig')
