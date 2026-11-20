"""Use event country context for court-side settlement previews."""
from pathlib import Path
import re

root = Path(__file__).resolve().parents[1]
loc_path = root / 'localization/english/chi_adm_l_english.yml'
event_path = root / 'events/chi_adm_negotiated_integration.txt'
loc = loc_path.read_text(encoding='utf-8-sig')
events = event_path.read_text(encoding='utf-8')
additions = []
for key, value in re.findall(r'^ (chi_adm_negotiated_integration_\w+): "(.*)"$', loc, re.M):
    if key.endswith('_court_event') or '[ROOT.GetCountry.GetOverlord.' not in value:
        continue
    if not re.search(r'\b' + re.escape(key) + r'\b', events):
        continue
    event_key = key + '_court_event'
    value = value.replace('[ROOT.GetCountry.GetOverlord.', '[ROOT.GetCountry.')
    events = re.sub(r'\b' + re.escape(key) + r'\b', event_key, events)
    if not re.search(r'^ ' + event_key + ':', loc, re.M):
        additions.append(f' {event_key}: "{value}"')
if additions:
    loc += '\n' + '\n'.join(additions) + '\n'
loc_path.write_text(loc, encoding='utf-8-sig')
event_path.write_text(events, encoding='utf-8')
