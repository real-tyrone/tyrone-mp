"""Keep the Ili treaty visible and expose territorial prerequisites as requirements."""
from pathlib import Path

path = Path(__file__).resolve().parents[1] / 'common/scripted_buttons/04_russia_buttons.txt'
text = path.read_text(encoding='utf-8')
start = text.index('je_the_eastern_border_russia_chuguchak_protocol = {')
visible = text.index('visible = {', start)
opening = text.index('{', visible)
end = opening + 1
depth = 1
while depth:
    depth += (text[end] == '{') - (text[end] == '}')
    end += 1
requirements = text[opening + 1:end - 1]
replacement = '''visible = {
        exists = c:RUS
        c:RUS = ROOT
        is_subject = no
        NOT = { has_global_variable = rus_chuguchak_protocol }
    }'''
text = text[:visible] + replacement + text[end:]
possible = text.index('possible = {', visible) + len('possible = {')
text = text[:possible] + '\n        # Territorial and technology gates remain enforced, but no longer hide the button.\n' + requirements + text[possible:]
path.write_text(text, encoding='utf-8')
