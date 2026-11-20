# Qing Administration — Current Status

The China Branch includes provincial government, reform, integration,
development, imperial security and regional works. The renamed build is
intended for fresh campaigns because Victoria 3 stores scripted identifiers
with active campaign state.

## File map

Game files stay in the engine's native directories. Find a feature by its
shared filename across `common`, `events` and `gui/journal_entry_widgets`.

| Feature | File family | Contents |
| --- | --- | --- |
| Provincial accounts | `chi_adm_core*`, `chi_adm_foundation*`, `chi_adm_governance*` | Account values, initialization, actions and the governor dossier |
| Court register | `chi_adm_court_register*` | Court ledger, memorial desk, journal groups and subentries |
| Office titles | `*chi_adm_government_titles*` | Provincial eligibility, government fallbacks and validation fixtures |
| Imperial law reform | `*chi_adm_imperial_law*` | Requests, directives, implementation, law icons and native law rights |
| Memorials and audits | `chi_adm_memorials*` | Petitions, edicts, audits, and replies |
| Negotiated integration | `chi_adm_negotiated_integration*` | Agreements, implementation, fiscal terms and contested integration |
| Provincial development | `chi_adm_provincial_development*` | Emergency powers, Self-Strengthening, budgets, compacts and enforcement |
| Imperial security | `chi_adm_qing_security*` | Conspiracies, factions, international entries and the throne contest |
| Regional works | `chi_adm_regional_works*` | Regional dispatches and historical charters |

`localization/english/chi_adm_l_english.yml` contains the full English
localization. The corresponding `validate_chi_adm_*.py` files in `tools`
use the same feature names. Review the [progress log](chi_adm_progress.md)
for feature history and the latest runtime checklists.

## Implemented systems

- **provincial accounts:** Loyalty, Autonomy, Corruption accounts, corruption-linked tax capacity,
  provincial actions and Governor’s Accounts JE.
- **court register/office titles:** Qing administration ledger and memorial desk, subject government
  types and titles, including Shanxi’s `SHN` setup and frontier offices.
- **imperial law reform:** Expanded law reform requests across installed laws, central directives,
  negotiated provincial responses and enactment handling.
- **memorials and audits:** Memorials, edicts, audits, responses, costs and corruption outcomes.
- **negotiated integration:** Negotiated administrative integration, concessions, implementation,
  peaceful annexation and contested enforcement paths.
- **provincial development:** Emergency powers and crisis decentralization; three-tier funded
  self-strengthening projects with sponsorship and ownership takeover; regional
  frontier compacts; civil conversion; enforcement play and settlements; MCH
  government/title support; court and provincial JEs.
- **Imperial security:** Provincial factions, court responses, international
  journal entries and the dynastic succession settlement.
- **Regional works:** Conditional dispatches for each active government and
  historical works tied to the four provincial modernization tracks.

These are source implementations. Validators and local models are not proof of
Victoria 3 runtime behavior.

## provincial development project funding and review display correction

2026-11-18: A Victoria 3 1.15.1 autosave contained 42 active project states,
zero population weights and no project expense modifier. Project weights now
use state_population for each state and total_population for its country.
The monthly review tally now reads state progress after decrementing the
remaining reviews. Existing projects retain their saved state and use the
corrected formula on the next monthly pulse. In-game verification is pending.

## Latest provincial development funding repair

The monthly country pulse now installs current project expense modifiers before
running project reviews. The review advances only when ownership, affordability
and the installed expense modifier are valid. Expense calculations now pass
through temporary variables before applying scaled modifiers. Focused provincial development,
completion and funding validators passed on 2026-11-18. In-game expense and
progress remain unverified.

## Outstanding runtime checks

- Confirm a subject-funded project charges its treasury and advances from 0/N on
  the next monthly review. Confirm sponsor expense and subject credit match the
  eligible project costs, including after funding pauses or territory changes.
- Exercise project save/load, annexation takeover/cancellation, territory splits,
  tier upgrades and completion persistence.
- Test militia requests, counteroffers, defiance, crisis grace and restoration,
  including at 100 Autonomy and with human-controlled provinces.
- Test MGL and XIB regional compacts, regional territory loss, and MCH/frontier
  civil conversion duration, government/title, preserved laws and −20 Autonomy.
- Test enforcement play creation, backdown, Qing/provincial victories, white peace,
  truce handling and the negotiated integration guarantee protection.
- Inspect provincial development JE panels, bars, tooltips and long names at 1920×1080. Test pending
  events, save/load and consent in a two-human session.
- Review a fresh `error.log` for provincial development script, GUI, localization and event errors.

## Architecture and dependencies

- provincial development extends shared provincial accounts Loyalty/Autonomy/Corruption helpers and provincial accounts–negotiated integration subject
  setup. Preserve the current 13-office roster, MCH/Manchuria setup, merged
  territories, `SHN`, and existing negotiated integration terms.
- The monthly provincial development on-action synchronizes native budget modifiers before project
  review and AI decisions. Project progress is stored on states with an explicit
  project owner; valid ownership and installed funding gate monthly progress.
- Sponsorship uses paired native budget modifiers. Provincial sponsor credit is
  capped at half the matching eligible project bill and Qing’s cost aggregates
  those credits. Existing negotiated integration subsidy pacts are separate.
- Regional compacts are tracked separately for Inner Mongolia within MGL and
  Xining within XIB. Enforcement uses native diplomatic-play/war-goal definitions
  and negotiated integration guarantee variables. Conversion preserves laws and has an 18-month term.
- Do not rerun one-time provincial development builders or migration helpers blindly. Current game
  scripts are authoritative because later repair refinements may not exist in
  builders.

## Key files and safe validators

- Historical record: `docs/chi_adm_progress.md`
- provincial development effects/triggers/values/buttons/JEs: `common/scripted_effects/chi_adm_provincial_development*.txt`,
  `common/scripted_triggers/chi_adm_provincial_development_extension.txt`,
  `common/script_values/chi_adm_provincial_development_extension.txt`,
  `common/scripted_buttons/chi_adm_provincial_development_extension.txt`,
  `common/journal_entries/chi_adm_provincial_development_extension.txt`
- Budget and monthly hook: `common/scripted_effects/chi_adm_provincial_development_budget.txt`,
  `common/on_actions/chi_adm_provincial_development_extension.txt`
- Events, modifiers and UI: `events/chi_adm_provincial_development*.txt`,
  `common/static_modifiers/chi_adm_provincial_development_extension.txt`,
  `gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui`
- All added English localization: `localization/english/chi_adm_l_english.yml`
- Validators: `python -B tools/validate_chi_adm.py`, then `_court_register.py`, `_government_titles.py`,
  `_imperial_law.py`, `_memorials.py`, `_negotiated_integration.py`, `_provincial_development.py`. provincial development invokes completion/funding checks.
  They were not rerun for this documentation-only handoff.

## Next steps

1. User tests the latest subject funding/progress fix in-game.
2. Resolve runtime errors and complete the provincial development checklist.
3. Re-run provincial accounts–provincial development validators after code changes and record findings in both docs.
4. Keep development within provincial development until runtime issues are resolved. Do not begin
   imperial security–regional works without a separate instruction.
