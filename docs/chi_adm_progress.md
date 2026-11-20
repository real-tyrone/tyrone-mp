# Qing Imperial Administration progress

## regional works regional dispatches and historical works

2026-11-19. All 13 active administrations have a conditional regional
dispatch. Zhili reviews its embankments, Liangjiang handles Yangtze supply
and Henan grain accounts, Huguang oversees granaries, Liangguang considers
Canton shipping, and Min-Zhe reviews Taiwan's coastal stations. Shaan-Gan
handles Xining caravans, Yun-Gui surveys mining roads, Sichuan reviews
Chongqing tolls, Shanxi negotiates remittance books, and Shandong considers
Yellow River relief. Mongolia, Ili and Manchuria cover banner registers,
patrol supply and Shengjing's garrison rolls. The current 13-office map
already incorporates Henan, Inner Mongolia and Xining.

Regional Dispatches appears under Governor's Accounts. Each office gets one
settlement. Supervised works consume 3% Bureaucracy for a year and improve the
local site for two years. Delegation commits 20 Authority for a year and
affects the provincial accounts. Deferral sets an eighteen-month recess.
AI choices consider fiscal capacity, corruption, loyalty and the relevant
interest group. Human governors open their own dispatches and choose the terms.

### Historical works inside Provincial Self-Strengthening

| Project | Office and site | provincial development program | Native requirement |
| --- | --- | --- | --- |
| Kaiping Mining Company | ZHI, Zhili | Economy III | Established company and five coal mine levels |
| Hanyang Arsenal | HNA, Eastern Hubei | Military III | Established company and five arms industry levels |
| Foochow Naval Academy | FRS, Fujian | Education II | Established Foochow Arsenal company and five shipyard levels |
| Jingdezhen Porcelain | AHU, Jiangxi | Economy II | Established Jingdezhen company and five glassworks levels |
| Jiangnan Weaving Bureaus | AHU, Suzhou | Administration II | Charters of Commerce, established company and five textile mill levels |
| Lanzhou Woolen Mill | XIB, Ningxia | Economy II | Three textile mill levels |

The native companies are established through regular gameplay. State
incorporation, applicable technologies and funding are checked at endorsement
and ratification. Existing provincial development work can be endorsed while underway or complete.
The endorsement adds a choice between provincial subscriptions and imperial
accounts. Those choices carry Authority or Bureaucracy costs and affect
Autonomy, Loyalty and Corruption upon ratification. Imperial accounts require
cordial relations and sufficient Loyalty. Actual project sponsorship still
uses the provincial development request, approval and financing path.

The existing provincial development progress display, expense, twelve tiers, project transfer
and cancellation remain in use. A charter is tied to its original owning
office and site. Transfer or cancellation of the relevant unfinished provincial development work
closes the charter. Temporary imperial security detachment pauses eligibility while the
office holds the site. The court records each ratification once before the
site receives a four-year local modifier. Installed work may survive a
change of owner for its remaining term. The new owner cannot ratify it again.
An uncompleted charter can be withdrawn or expires after five years.
The historical names identify institutions or projects. The option text and
terms are scenario design.

### Files and validation

- Added `chi_adm_regional_works.txt` in `common/customizable_localization`,
  `common/journal_entries`, `common/on_actions`, `common/scripted_buttons`,
  `common/scripted_effects`, `common/scripted_guis`,
  `common/scripted_triggers` and `common/static_modifiers`.
- Added `events/chi_adm_regional_works.txt`, `gui/journal_entry_widgets/chi_adm_regional_works.gui`
  and `tools/validate_chi_adm_regional_works.py`. Extended the provincial development development entry in
  `common/journal_entries/chi_adm_provincial_development_extension.txt`. Added English strings only
  in `localization/english/chi_adm_l_english.yml`.
- Updated `tools/validate_chi_adm_provincial_development.py` and
  `tools/validate_chi_adm_provincial_development_complete.py` to read all installed modifier-type
  files. In 1.15.2, `building_training_rate_mult` is defined in
  `01_building_modifier_types.txt`. The earlier missing-modifier report came
  from the validator's narrower lookup.
- regional works, imperial security, provincial development funding and the provincial development settlement guard checks pass. The full provincial development
  validation now reaches its existing assertion against the birth-rate
  modifiers in the earlier frontier compacts. Those existing values remain in
  the build. provincial accounts–negotiated integration, remittance and tax-capacity checks still stop on their
  prior checksum or roster assertions. Historical baselines were retained.

### In-game checklist

1. Open Regional Dispatches as a civil and a frontier governor. Exercise
   both routes and deferral, then reload with a dispatch open.
2. Found Kaiping or Hanyang through Companies. Endorse the matching provincial development
   tier, request sponsorship through the regular provincial development controls and observe
   normal expenses, reviews and ratification. Try Jiangnan with its DLC
   enabled and disabled.
3. Before ratification, lose the site or cancel the provincial development project. Verify no
   regional works reward and confirm ownership transfer uses the normal provincial development controls.
   Test wartime pause and resumption from an imperial security save.
4. Check the journals and requirements at 1080p. Inspect the log for regional works
   script and GUI errors. Victoria 3 was not launched for this pass.

## imperial security dynastic conspiracy and throne contest

2026-11-19. imperial security is implemented in the China Branch for fresh test campaigns.
The current setup merged Henan into Liangjiang. Its ten Han claimant offices
are ZHI, AHU, HNA, YUE, FRS, XIB, YUN, SIH, SHN and SHA. MGL, XIN and MCH
may provide covert aid, declare neutrality or defend the court. Eligibility uses
office identity and Han political identity, so an provincial development conversion cannot make a
frontier office a claimant. The starting map and subject roster were kept as
configured for the test build.

- The founder needs three consecutive monthly reviews with Loyalty at most 20,
  Autonomy of at least 65, and army projection of at least 10 and one-fifth of
  Qing's. The Mandate must be at or below 3, with poor relations, crisis or low
  court Legitimacy. Organization opens recruitment at month four. Preparation
  can begin at month six with a second armed administration. An ultimatum
  requires at least twelve reviews, readiness of 75, two eligible armed offices,
  and 65 percent of Qing and its pledged loyalists' army projection.
- Governors can pledge troops, send covert aid, report the League, stand with
  the court, stay neutral or withdraw. Pledges are checked again at launch.
  Corruption, all four provincial development reform tracks, regional recruitment capabilities,
  relations and court measures affect preparation or exposure. AI weighs its
  own loyalty, autonomy, army, corruption, relations and commitments.
- The court can investigate, negotiate a general accord, offer individual
  pardons, pressure offices, muster loyalists and suppress an exposed weak
  network. Those choices carry Authority, Bureaucracy or political costs.
  A stronger League must be defeated militarily or persuaded to stand down.
- Imperial Security and Anti-Dynastic Conspiracy appear in the existing court
  and governor journals. When exposed, the League appears as an international
  situation where interested powers can spend Influence to back either side.
  War for the Dragon Throne takes over once the native play starts and maps
  provincial factions. Foreign backing creates diplomatic commitments.
  Foreign military participation uses the ordinary play interface.
- The claimant presses the throne demand in a native diplomatic play. For
  subject alignment, CHI is the technical initiator and the claimant holds the
  primary counter-demand. Armed governors authorize temporary suspension and
  eventual restoration of their original imperial pact. Human governors must
  confirm an AI-era pledge before launch and can explicitly accept or decline
  restoration if they took over after the previous governor went to war.
  Covert aid and neutrality carry no scripted military pledge.
- Only a native enforced goal can award victory. On rebel victory the Liu
  emperor and heir take over the existing CHI government, the empire adopts
  the Han imperial flag and Chinese Empire name, Mandate Centralisation falls
  by two, the new court operates with reduced Authority and Legitimacy, and
  rebel offices gain discretion. Laws, technologies, countries and state
  ownership carry through the succession. A Qing victory leaves the ruler and
  heir in place and opens a choice between general amnesty and supervision.
  White peace restores eligible offices without awarding a throne settlement.
- Court state permits one contest at a time, with a thirty-review preparation
  deadline and a five-year moratorium after closure. Independence, annexation
  and political invalidation remove affected participants or dissolve a case.
  Loss of the court or claimant invalidates the specific throne play. The
  scripts use a Qing review and a short administration list. negotiated integration coercion and
  provincial development enforcement refuse a competing play during the throne contest.

### imperial security files

- Added `chi_adm_qing_security.txt` in `common/customizable_localization`,
  `diplomatic_plays`, `dynamic_country_names`, `flag_definitions`,
  `journal_entries`, `on_actions`, `script_values`, `scripted_buttons`,
  `scripted_effects`, `scripted_guis`, `scripted_triggers`,
  `static_modifiers` and `war_goal_types` under `common`. The native play and
  settlement effects also use `common/scripted_effects/chi_adm_qing_security_war.txt`.
- Added `events/chi_adm_qing_security.txt`, `gui/journal_entry_widgets/chi_adm_qing_security.gui`
  and `tools/validate_chi_adm_qing_security.py`. Added English strings in
  `localization/english/chi_adm_l_english.yml`.
- Added competing-play guards in `common/diplomatic_plays/chi_adm_negotiated_integration.txt`,
  `common/diplomatic_plays/chi_adm_provincial_development.txt`,
  `common/scripted_effects/chi_adm_negotiated_integration.txt`,
  `common/scripted_effects/chi_adm_provincial_development_extension.txt`,
  `common/scripted_buttons/chi_adm_provincial_development_extension.txt` and
  `common/scripted_guis/chi_adm_provincial_development_extension.txt`.

### Validation and in-game acceptance

- `python -B tools/validate_chi_adm_qing_security.py` passes script and localization
  integrity, the ten-office political roster, recruitment, military strength,
  protected offices, AI decisions, both native goal branches, multiplayer
  consent guards, repeat protection, white peace and invalidation checks.
  The provincial development funding and settlement-guard checks also pass.
- provincial accounts and court register stop on the existing starting-setup checksum. office titles expects nine
  government definitions. imperial law reform and its GUI check stop on the existing law-trigger
  checksum. memorials and audits stops on the core-button checksum and negotiated integration on the law-trigger
  checksum. provincial development and its completion check stop because the installed modifier
  definitions lack the existing `building_training_rate_mult` used by provincial development.
  The older remittance and tax-capacity checks also stop on baseline assertions.
  These failures reproduced before the negotiated integration/provincial development competing-play guards were added.
- Installed Victoria 3 1.15.2 source examples establish contextless journals, scripted
  diplomatic plays, backers on both sides, native custom goals and monarch/heir
  creation. The engine chooses the play sides internally, so Qing appears as
  aggressor even though the claimant starts the contest through its journal.
  The armed governors temporarily lose overlord services while their pacts are
  suspended. Runtime checks are needed for the counter-goal at play creation,
  the subject join filter and explicit backers, save/load, faction map and GUI
  layout. Victoria 3 was not launched.

1. Start a fresh Qing campaign. Verify Imperial Security and the governor entry
   are nested and that the two international entries only appear in their
   phases. Check the flags, ruler portrait, roster and tooltips at 1080p.
2. Bring two Han offices to the political and military thresholds. Form a
   League, save and reload during recruitment, then try covert aid, a betrayal,
   withdrawal, a frontier loyalist and foreign diplomatic support.
3. As Qing, test investigation, pressure, the court's accord and individual
   pardons. Suppress a weak network and confirm its offices cannot immediately
   start a replacement plot.
4. Launch with two armed governors, a loyalist and a neutral human governor.
   Inspect both primary demands, exact backers, neutrality on the first day of
   war, and negotiated integration/provincial development play lockouts. Test a human takeover after an AI pledge.
5. Enforce each goal from separate saves and test white peace. Check ruler, heir,
   flag, pacts, Mandate, supervision or amnesty, and continued control of each
   human country. Inspect a saved provincial development project across the war and pact restoration.
6. Invalidate a separate test through annexation, independence or Qing's loss
   of monarchy. Confirm the dossier, war goals and member flags clear. Check
   the new game log for `chi_adm_qing_security` errors.

## provincial development project funding and review display correction

2026-11-18: A Victoria 3 1.15.1 autosave contained 42 active project states,
zero population weights and no project expense modifier. Project weights now
use state_population for each state and total_population for its country.
The monthly review tally now reads state progress after decrementing the
remaining reviews. Existing projects retain their saved state and use the
corrected formula on the next monthly pulse. In-game verification is pending.

## provincial development continuation completed in source — in-game acceptance pending

2026-11-17: Resumed from `docs/chi_adm_provincial_development_handoff.md`, without rebuilding the
earlier systems. The provincial development emergency, crisis/decentralization, three-tier projects,
regional compacts, eighteen-month conversion, enforcement, MCH titles and JE
interfaces are implemented. This entry supersedes the emergency powers-only status below.
No imperial security/regional works content and no game launch.

Resolved the handoff's funding mismatch: sponsorship now uses paired native
budget modifiers. Provincial credit is capped at half its matching project
expense; China's expense sums those exact credits. Both stop when eligibility
or funding conditions fail. Legacy fixed-rate sponsorship pacts are removed by
maintenance. This avoids the whole-province transfer exceeding a partial-state
project's actual cost. Existing negotiated integration subsidy pacts are unchanged.

New acquisitions no longer deadlock project progression. Explicit catch-up
projects affect only states below the chosen tier, preserve higher upgrades,
and retain territorial cost weighting. New owners can explicitly assume or
cancel unfinished works; completed improvements are never erased by cancellation.
Sponsorship's political refund now respects the actual Autonomy gained at the
100 cap. The existing emergency cap correction remains covered by 202 executed
effect-tree cases.

Regional compact requests and acceptance require continued ownership of their
regional territory; losing it closes the pending regional case. MCH retains its
Three Eastern Provinces name after negotiated viceroyalty conversion. Emergency
military benefits now expire through a guarded three-calendar-month event after
the crisis warning clears; resumed danger invalidates the older timer. Enforcement
respects truces and invalidated administrations release their single-play marker.

Changed in this resumed pass:
- common/scripted_effects/chi_adm_provincial_development.txt and chi_adm_provincial_development_extension.txt
- common/scripted_triggers/chi_adm_provincial_development_extension.txt
- common/script_values/chi_adm_provincial_development_extension.txt
- common/static_modifiers/chi_adm_provincial_development_extension.txt
- common/scripted_buttons/chi_adm_provincial_development_extension.txt and chi_adm_provincial_development_project_cancel.txt
- common/scripted_guis/chi_adm_provincial_development_extension.txt
- common/journal_entries/chi_adm_provincial_development_extension.txt
- common/dynamic_country_names/tyrone_qing_administrations.txt
- events/chi_adm_provincial_development.txt; localization/english/chi_adm_l_english.yml
- tools/validate_chi_adm_provincial_development{,_complete,_funding}.py and focused repair helpers
- docs/chi_adm_imperial_law_coverage.md (report refresh only), this progress report.

Validation: `python -B tools/validate_chi_adm.py`, `_court_register.py`, `_government_titles.py`, `_imperial_law.py`,
`_memorials.py`, `_negotiated_integration.py`, `_provincial_development.py` all PASS. provincial development includes 202 actual emergency-effect
cap/defiance/restoration cases and 60 funding arithmetic cases, plus source/ID/
localization/native-modifier/GUI-binding checks. Military overlap audit verifies
no duplicated combat/training modernization benefit; provisioning offsets a
small part of the existing artillery supply-cost penalty. Earlier historical
baselines were retained; no blanket baseline refresh was performed in this pass.

No confirmed engine blocker remains, but static/model checks do not establish
runtime correctness. Essential in-game acceptance:
1. Fund each project tier, sponsor it, pause funding, gain/lose territory, save/load,
   and verify matching court expense/provincial credit never exceeds half costs.
2. Annex a province with unfinished work; explicitly assume or cancel it. Verify
   completed state upgrades survive, higher-tier upgrades are not downgraded,
   and new territory receives nothing until an explicit funded project.
3. Request/counter/refuse/defy militia powers; end and resume danger during grace;
   verify exactly-once restoration at high Autonomy and no forced human acceptance.
4. Negotiate both MGL compacts and XIB's Xining compact, then lose relevant states.
   Convert MCH and another frontier office: eighteen reviews, correct title/type,
   unchanged laws, and one -20 Autonomy adjustment.
5. Test enforcement backdown, Qing victory, provincial victory and white peace;
   verify the opposing guarantee, three-year negotiated integration protection, truce respect and
   cleanup after independence/annexation. These native play/settlement paths have
   not been run in the game.
6. Inspect court/province status, progress bars, tooltips and long names at 1080p;
   exercise two-human consent and save/load while events are pending.

One-time migration helpers are not safe general-purpose rebuild commands. Current
game files are the authoritative implementation; do not rerun older builders
without consolidating their later fixes. Stop at provincial development and address runtime failures
before proceeding to any later features.

## emergency powers in progress — emergency powers foundation only

provincial development is NOT complete. Implemented a first emergency-powers workflow with three
governor requests, court approval/counter/refusal events, explicit provincial
acceptance or unilateral mobilization, a three-month post-crisis grace period,
and restoration/resistance choices. Uses existing clamped L/A/C helpers and
native scripted buttons in a provincial JE under the established group. Three
packages provide mobilization, recovery/organization, or supply-cost relief;
all carry a 5% Tax Collection cost. Authorized powers grant +5 Autonomy;
unilateral powers +10 Autonomy/-5 Loyalty/-10 relations. Restoration returns
the tracked grant; refusal retains discretion with fiscal and political costs.
One pending case per province, response deadlines, retry period, AI event weights,
monthly province checks, and cleanup after leaving imperial service are present.

New files: tools/build_chi_adm_provincial_development.py, tools/validate_chi_adm_provincial_development.py;
common/{scripted_triggers,scripted_effects,script_values,static_modifiers,
scripted_buttons,journal_entries,on_actions}/chi_adm_provincial_development.txt; events/chi_adm_provincial_development.txt.
English strings added only to localization/english/chi_adm_l_english.yml.

Validation: focused emergency powers script parsing, English key uniqueness/references and
installed modifier-type checks PASS. All existing provincial accounts–negotiated integration validators were run:
provincial accounts/court register/imperial law reform stop on the previously changed starting-setup checksum; office titles expects
the former 15-subject roster; memorials and audits/negotiated integration stop on the previously changed core effect
checksum. These are not a full regression pass and baselines were not reset.
No game launch or runtime certification.

Remaining provincial development scope: sustained imperial internal-crisis detection and bounded
decentralization demands; self-strengthening with funded/sponsored three-tier
projects and ownership takeover; separate regional compacts; eighteen-month
civil/viceroyalty conversion and -20 Autonomy; enforcement play, victory
settlements and negotiated integration guarantee protection; MCH government/title wiring; full
court GUI/status/progress presentation; stronger focused execution/AI/MP tests.
Military bonuses must be checked against existing modernization stacking.
Emergency grant bookkeeping at the 100-Autonomy cap needs correction before
runtime acceptance. Enforcement feasibility and native budget expense types
were inspected, but those systems are not yet implemented.

Runtime checklist for this slice: request each package; approve/refuse/counter;
human defiance and no forced acceptance; AI reply; end crisis and advance grace;
restore/refuse; independence cleanup; save/load with a pending case. Review
deadline and repeated-emergency behavior before balancing. Resume provincial development, not imperial security.

## negotiated integration implemented: negotiated administrative integration (runtime testing pending)

Replaced the 15 `chi_qing_integrate_TAG` instant-annexation effects with proposals.
negotiated integration now provides event negotiations, unconditional acceptance, individually offered
or requested concessions, closer centralization, delay/refusal, one pressure
attempt followed by one improved offer, withdrawal and a contested coercive route.
All 15 administrations participate, including SHN and the four frontier offices.
The user's interview decisions override the brief's one-active-project restriction,
25% Bureaucracy gate, unrelated-war restrictions and AI-only annexation fallback.

Implementation starts after agreement: three base months of census and three of
transition. Each additional active commission adds three months to the required
total, without resetting elapsed work. Native hidden calendar events begin one
month after agreement/resumption; global monthly maintenance does not award work.
Pause/resume invalidates older clock generations and preserves completed work.
Each active commission commits -50 Authority/-10% Bureaucracy through a native
scaled JE modifier. Existing deficits do not stop work; current negative balances
block new agreements/resumption. Unrelated wars do not pause work; Qing-target
hostility, independence, fragmentation and Qing collapse invalidate safely.

Financial concessions are automatic native payment pacts (10%/20% provincial
income), not scripted weekly treasury transfers. Fiscal privileges begin at
-10%/-20% Tax Collection and decay over five/ten years on the original states.
Imperial honors give governor Popularity and Prominence. Closer centralization
applies -5 Autonomy immediately and a one-year retry window; no extra remittance
modifier is added. Failed negotiations use a six-month retry window. Suspensions,
revoked terms, cancellation by agreement and negotiated automatic repayment are
functional event branches. Native pacts are removed on cancellation/completion.

The coercive play uses a dedicated annexation-kind war goal with 25% of the full
installed native annexation Infamy formula. Other administrations react according
to Loyalty/Autonomy. A victorious settlement annexes immediately; the pre-existing
warlord reintegration route is unchanged. Negotiated completion transfers the
living governor to Qing without appointing an office, and invokes existing imperial law reform/memorials and audits
cleanup helpers. Human subjects require initial agreement AND explicit final
confirmation after the required work; they can be annexed while player-controlled,
as requested. No forced player switch or inference of consent from silence.

GUI: Governance of the Empire -> Administrative Integration; Governor's Accounts
-> Provincial Integration Commission when a case exists. One reusable JE per side,
not 15 definitions. Expandable court rows show the existing memorials and audits compact live L/A/C
bars, phase/response, terms, work progress and contextual actions. The Imperial
Ledger has a read-only integration status line. Controls bind each action once;
text wraps with dynamic height. Native requirement feedback and modifier previews
are used where applicable. All new English remains in chi_adm_l_english.yml.

New files:
- common/{scripted_effects,scripted_triggers,script_values,scripted_guis,
  static_modifiers,diplomatic_actions,diplomatic_plays,war_goal_types,
  journal_entries,customizable_localization,on_actions}/chi_adm_negotiated_integration.txt
- events/chi_adm_negotiated_integration.txt (seven decision events and one hidden calendar clock)
- gui/journal_entry_widgets/chi_adm_negotiated_integration.gui
- tools/build_chi_adm_negotiated_integration.py, tools/validate_chi_adm_negotiated_integration.py,
  tools/chi_adm_negotiated_integration_baseline.json and docs/chi_adm_negotiated_integration_design.md

Modified: common/scripted_buttons/tyrone_qing_administrations.txt (only the 15
integration definitions); gui/journal_entry_widgets/chi_adm_court_register_ledger.gui (one
status line); localization/english/chi_adm_l_english.yml; provincial accounts validator's feature
localization allowance; office titles validator's intentional negotiated integration button-migration exception;
applicable earlier preservation baselines, and this progress report. Baselines
advance only for the two authorized existing content files. negotiated integration independently
checks original warlord/non-integration button ASTs, all prior system hashes,
original ledger content and the exact proposal replacement in every integration
button. Starting setup, governments, 20% civil/15% frontier pact rates, stat scaling,
imperial law reform's 264-law registry, memorials and audits mechanics and army sharing remain unchanged.

Validation: all provincial accounts/court register/office titles/imperial law reform/memorials and audits/negotiated integration validators pass. Focused negotiated integration execution tests cover
all 15 offices, live timing/concurrency, acceptance/negotiation/refusal, once-only
pressure, stale event revisions, resource gates, automatic pact creation/removal,
suspension/resumption, Qing breach, human final consent while player-controlled,
repayment counters and expiry, territorial decay, independence/collapse/war cleanup,
coercion reactions, persisted scalars and all four AI negotiation factors.

Not runtime-certified; game was not launched. Verify actual weekly debit/credit and
income scaling, player handling after consensual annexation, former-governor roster
survival, coercive native settlement, scheduled-event persistence and 1080p layout.
The detailed design report documents native evidence, balance tuning, state model,
limitations and a manual test checklist. No provincial development-regional works work. Next action: user runtime
checks of negotiated integration, especially one human completion and a frontier negotiation.

## Loyalty/Autonomy remittances, modifier icons and starting offices

Added two separate native JE-scaled country modifiers on the provincial Governor's
Accounts. Loyalty uses `country_overlord_income_transfer_mult = 0.5` multiplied by
`Loyalty / 50 - 1`; Autonomy uses the same modifier type multiplied by
`1 - Autonomy / 50`. Each ranges from -50% to +50%, with 0% at 50.
They add together before multiplying the existing pact base: 100 Loyalty and
0 Autonomy give +100%, changing a 20% base to 40%, not to 100% of total income.
At 0 Loyalty and 100 Autonomy the combined adjustment is -100%. Other native
payment modifiers can still contribute to the final engine calculation.

Preserved the pact rates found at the start of this pass: 20% civil and 15%
frontier. Earlier progress entries and validators assumed 30%; updated the checks
to recognize the current user-edited rates without rewriting the pacts.

Added native documents/coins modifier icons to Corruption Tax Capacity and the
two new remittance modifiers. Verified the textures exist in the installed game.
Updated modifier descriptions and Loyalty/Autonomy concepts in the single English
localization file, including their builder sources. The JE owns dynamic updates
and cleanup; no new polling, transfer effects or periodic modifier reapplication.

Added starting Government Administration levels (not flat Bureaucracy grants):
Shanxi +10; Shaan-Gan +15 in Xian; Huguang +25 distributed as Western Hubei +10,
Eastern Hubei +10 and Hunan +5; Henan +15; Shandong +15. These use the existing
horizontal drawer cabinets/professional/religious bureaucrat production methods
and native state-history ownership syntax, inherited by the provinces at setup.
At full staffing, horizontal drawer cabinets nominally supply 50 Bureaucracy per
added level before other modifiers. The extra buildings also consume paper and
wages. They apply to new campaigns; existing saves retain their existing buildings.

Files: core static modifiers, script values and governance JE;
`common/history/buildings/11_tyrone_east_asia.txt`; memorials and audits builder and presentation
helper; English localization; provincial accounts/tax-capacity validators and protected baselines;
new `tools/validate_chi_adm_remittance.py` and pre-change AST fixture
`tools/chi_adm_remittance_original.json`. The fixture checks that only the intended
building blocks, two scaling definitions and icon/JE additions changed. Prior
Corruption regression checks remain active. No other mechanics were changed.

Validation: provincial accounts/court register/office titles/imperial law reform/memorials and audits validators pass; 10,201 Loyalty/Autonomy combinations,
the 20%-to-40% example, modifier binding uniqueness, native texture existence,
starting building additions and preservation checks pass.

Runtime checklist: in a NEW campaign check all five countries' initial Bureaucracy
and staffing after the economy updates (static checks cannot guarantee employment,
paper availability or the final balance). Confirm separate remittance modifiers at
0/50/100 and actual payments at both extremes, including signed native JE scaling,
save/load and cleanup after independence. Confirm all three modifier icons display.
Game was not launched. No later features work.

## Continuous Corruption Tax Capacity

Corruption now supplies one JE-owned, dynamically scaled Taxation Capacity modifier:
`+25% - (0.5 percentage points * Corruption)`. Values 0/25/50/75/100
produce +25%/+12.5%/0%/-12.5%/-25%. All 15 administrative subjects use
their own accounts. Removed the fixed +25% from the viceroyalty and governorate
pacts; frontier pact terms and the 30% remittance remain unchanged.

Replaced the old corruption-tier Bureaucracy penalties. Their legacy modifier
IDs remain empty for save compatibility and existing status refresh removes them.
The native `scaling_modifiers_while_active` system owns the new modifier on The
Governor's Accounts, recalculates at the JE's update frequency, and removes its
effect when that JE closes. No extra monthly synchronization or global loop.
Other Bureaucracy action costs, audit conditions and supervision terms are unchanged.

Changed core scripted effects, script values, static modifiers and governance JE;
Qing administration pact definitions; the memorials and audits builder/presentation localization
sources and generated English localization; provincial accounts validator and relevant preservation
baselines. Added `tools/validate_chi_adm_tax_capacity.py` and its pre-change AST
fixture `tools/chi_adm_tax_capacity_original.json`. Baseline changes authorize only
the five affected gameplay source files; the fixture independently checks that
all other pact, core effect, modifier and JE mechanics remain unchanged.

Validation: all provincial accounts/court register/office titles/imperial law reform/memorials and audits validators pass, including 264-law registry freshness.
The focused check evaluates every integer Corruption value 0 through 100 against
the linear formula and verifies native JE wiring, legacy cleanup and preservation.
Installed journal_entries.md verifies country propagation, dynamic script-value
scaling and update-frequency evaluation. Native localization verifies Taxation
Capacity concept and signed one-decimal formatting.

Runtime checks (game not launched): confirm +25%, 0%, -25% at Corruption 0/50/100
in state Taxation Capacity breakdowns, positive and negative scaling after a JE
update, existing-save migration, save/load, and removal after leaving imperial
service. The engine's signed scaling and actual refresh timing need in-game
confirmation; static/model validators do not execute Victoria 3.

## Memorial replies no longer charge Court Correspondence

Approval and counteroffers no longer call the court staff cost helper, require
available Authority, or create/refresh Court Correspondence. AI replies follow the
same rule. Treasury affordability, provincial filing costs/cooldowns, consent and
once-only rewards remain. Edict/audit costs are unchanged. Existing staff modifiers
are left to expire because they may belong to a valid edict or audit.

Changed the memorials and audits builder/presentation helper, generated memorials and audits triggers/effects/GUI/English,
memorials and audits validator and presentation baseline, and this report. The baseline advances only
the authorized memorial gates/effects. Tests cover multiple replies, low Authority,
no new staff modifier and no refresh of a pre-existing staff commitment.
All five feature validators pass; runtime check: approve/counter several memorials
and confirm no Court Correspondence gain appears in the tooltip or country modifiers.


## Memorial replies share Court Correspondence

Qing may now approve/counter multiple provincial memorials while Court
Correspondence is active. A dedicated memorial_capacity predicate permits an
existing staff commitment OR at least 25 available Authority to establish one.
Replies refresh the shared six-month modifier without stacking another Authority
penalty. Treasury checks and once-only payments remain. AI court replies use the
same capacity predicate. Edict/audit staff gates and intervention limits are unchanged.

Changed tools/build_chi_adm_memorials.py, tools/chi_adm_memorials_presentation.py,
common/scripted_triggers/chi_adm_memorials.txt, common/scripted_effects/chi_adm_memorials.txt,
common/scripted_guis/chi_adm_memorials.txt, localization/english/chi_adm_l_english.yml,
tools/validate_chi_adm_memorials.py, tools/chi_adm_memorials_presentation_baseline.json and this
report. The baseline advances only the explicitly changed trigger/effect files
and two memorial GUI eligibility blocks; other mechanics remain protected.
All five validators pass. New checks approve/counter three simultaneous memorials,
verify shared staff and zero-sum transfers, and distinguish initial Authority
requirements from an already-funded staff commitment. Runtime check: answer several
provinces in the same paused session and confirm no staff-related lockout.


## Conditional edict discussion buttons

Offer Revised Terms and Withdraw Edict now use the existing edict-detail visibility
predicate, appearing only when that province has a pending edict. Existing enabled
conditions remain: revised terms still require an appeal. Expanded rows ignore
invisible controls so hidden buttons leave no blank space. Changed the memorials and audits builder,
generated memorials and audits GUI and this report. No mechanics or localization changes; memorials and audits validation
passes. Runtime check: both buttons disappear without an edict and return during
an active discussion.


## Imperial Edicts compact accounts strip

The same live Loyalty/Autonomy/Corruption strip now appears in expanded Imperial
Edicts rows, using each target Country's values, icons, mini-bars and tier hovers.
Changed tools/build_chi_adm_memorials.py, generated gui/journal_entry_widgets/chi_adm_memorials.gui,
tools/validate_chi_adm_memorials.py and this report. memorials and audits validation passes, including protected
provincial accounts-imperial law reform hashes and unchanged gameplay. Runtime check: edict rows show their own
values and update after acceptance. No new localization or mechanics.


## Current audit panel addition: compact live accounts strip

Expanded Imperial Audits rows now show a 440x66 framed strip above the case text.
Three 136-pixel columns display the native-backed stat icon, L/A/C abbreviation,
current value and a 0-100 gold/blue/red mini-bar. Hover gives the linked concept,
full value/range and current tier. Bindings use the row Country, not the Qing
JournalEntry owner. No synchronized variables or gameplay changes are introduced.

Changed tools/build_chi_adm_memorials.py, gui/journal_entry_widgets/chi_adm_memorials.gui,
localization/english/chi_adm_l_english.yml, tools/validate_chi_adm_memorials.py and this
report. All five validators pass. Runtime check: each expanded province shows its
own three values, bars update after restitution/reform, and labels fit at 1080p.


## Current localization fix: corrupted question marks

The reported question marks were literal source characters replacing bullets,
not an intended uncertainty symbol. List markers now use ASCII dashes; damaged
possessive apostrophes are repaired, and a stale currency marker in builder text
uses native money formatting. UTF-8 source/UTF-8-BOM English output is preserved.
Changed tools/chi_adm_memorials_presentation.py, tools/build_chi_adm_memorials.py,
localization/english/chi_adm_l_english.yml, tools/validate_chi_adm_memorials.py and this
report. New checks reject question-mark bullets, possessives and currency markers.
All five validators pass. No gameplay changes. Runtime check: Discovery Risk,
compromise/restitution lists and cooldown requirements show clean punctuation.


## Current memorials and audits repair: delivered decisions and reliable replies

Source weaknesses: the governor notice had only a three-day acknowledgement and
no decisions; repeat cases relied on automatic reactivation of a concluded response
JE; AI governors relied entirely on scripted-button AI. These are repaired without
claiming the runtime failure has been independently reproduced in the game.

Every provincial dispatch now explicitly ensures Provincial Correspondence exists.
The monthly active-case review also repairs a missing/concluded response JE before
processing deadlines. A reopened human reply gets at least three reviews to act.
The province event now lasts 30 days and offers the same twelve response choices,
using their original eligibility, guarded helpers and AI weights. Unrelated options
are hidden; relevant but ineligible options use native show_as_unavailable. Default
acknowledgement never consents or pays. The JE remains the persistent alternative.

An AI-only monthly response fallback runs before deadline decrement: governors
accept or appeal/decline edicts, select cooperation/obstruction/concealment for an
audit, accept/decline memorial counters and settle/refuse findings using the same
costed helpers. Humans are never automatically accepted. Normal timeouts still
apply if a human deliberately leaves a delivered case unanswered.

On the first eligible review after this repair, an already expired edict (last
result 22) or audit settlement (23) gets its corresponding target cooldown cleared
once, allowing Qing to resend. This does not restore lost request types, refund
staff costs or retroactively force consent. A persistent repair marker prevents
repeated cooldown resets. Pending investigations and accepted decisions are kept.

Changed: tools/build_chi_adm_memorials.py, tools/chi_adm_memorials_presentation.py,
common/scripted_effects/chi_adm_memorials.txt, common/on_actions/chi_adm_memorials.txt,
events/chi_adm_memorials.txt, localization/english/chi_adm_l_english.yml,
tools/validate_chi_adm_memorials.py, tools/chi_adm_memorials_presentation_baseline.json and this
report. The presentation baseline advances only the explicitly repaired effects,
on-action and event files; mechanical trigger/modifier hashes remain unchanged.

All five feature validators pass. New tests cover explicit JE creation/reopening,
last-review AI replies, recovered human response time and no automatic human
compliance; event checks cover all twelve guarded options and the 30-day notice.
Runtime tests still needed: new and repeated edicts/audits in an existing save,
AI replies, human event choices, one-time retry of old expired cases, investigation
progress and court settlement responses. No game launch or negotiated integration-regional works work.


## Current court tooltip fix: explicit failed requirements

Court-button ExecuteTooltip previously showed only descriptive terms and effects,
not the is_valid conditions used to disable the button. Tooltips now separate
Requirements from Immediate effects. Display-only if/else checks are generated from
the actual is_valid trigger tree and show native green-check/red-cross icons for
staff availability, Qing Authority/reserves, intervention capacity, target cooldown,
existing interventions, case stages and stat thresholds. The supervision check
shows Corruption >=40 alongside the current province value. General service
validity remains hidden because invalid subjects are not displayed in the list.

Installed scripted-GUI documentation exposes ExecuteTooltip, not a verified
IsValidTooltip API. Therefore these are read-only checked lines inside the native
show_as_tooltip path, not invented GUI methods. The original is_valid and hidden
live helper are unchanged; native resource/modifier effect previews remain below.
Future governor consent and proposed terms stay in the introductory description.

Changed: tools/chi_adm_memorials_presentation.py, generated
common/scripted_guis/chi_adm_memorials.txt, localization/english/chi_adm_l_english.yml,
tools/validate_chi_adm_memorials.py and this report. All five validators pass. Focused
checks verify the supervision tooltip fails at Corruption 25, passes at 50 with
free staff, and fails when the Qing clerks are committed. Gameplay is unchanged.
Runtime check: hover each disabled court button and confirm the red line explains
its blocker; confirm the requirements/effects sections remain readable at 1080p.


## Current memorials and audits court text readability pass

Shortened approval/rejection introductions to avoid repeating native effects.
Compromise, restitution and audit tooltips now separate proposed terms, deadlines
and limits into paragraphs and bullets. Edict tooltips separate revised terms.
Removed the repeated 0-100 clamping parenthetical from account-change previews;
the concept descriptions retain that explanation. Court JE instructions are now
specific to memorials, edicts or audits. Native payment/modifier lines remain.
Changed tools/chi_adm_memorials_presentation.py, tools/build_chi_adm_memorials.py, generated
localization/english/chi_adm_l_english.yml and this report. All five validators pass.
No gameplay changes. Runtime tooltip wrapping and readability still need checking.


## Current Desk polish: native relations display

The Desk now shows the native relations icon, colored relationship category
(GetRelationsWithDesc) and signed score, e.g. Friendly (+80). Hover uses the native
GetRelationsTooltip with the province and its overlord, supplying both country
names/flags and live relationship details. Country-panel and diplomatic-overview
GUI precedents were inspected. GetPlayer is not used as the other party: the
player is the province here, so that would display self-relations.

Changed: gui/journal_entry_widgets/chi_adm_court_register_memorial_desk.gui,
tools/chi_adm_memorials_presentation.py, localization/english/chi_adm_l_english.yml,
tools/validate_chi_adm_court_register.py, tools/chi_adm_memorials_baseline.json and this report.
Only the Desk GUI source checksum was advanced; gameplay is unchanged.
All five validators pass. Runtime check: correct colored category/icon and signed
score, native hover naming province plus Qing, and no clipping at 1080p.


## Current localization polish: outcome and Memorial Desk status

The shared service-ending header now aliases vanilla je_standard_completion_header
and its effect header aliases je_standard_on_completion_header. This supplies native
title styling and the missing line break before the checkbox. The condition is
present tense: "This administration is no longer in imperial service."

The Desk uses native Overlord/Relations concept labels and the existing live
relations value. Staff status is shortened to Memorials/Supervision/Inspections,
with verified native green_checkmark/red_cross icons and Ready/Committed labels.
Hover text reads actual modifier definitions through GetStaticModifier.GetDesc;
redundant instructions about hovering and plain numerical staff costs are removed.

Changed: tools/chi_adm_memorials_presentation.py,
localization/english/chi_adm_l_english.yml and this report. All five validators pass.
No script mechanics or GUI layout changes. Runtime checks: native header spacing,
concept links, status-row fit and the commitments hover. Game was not launched.


## Current tooltip fix: one private-case line, hidden service gate

memorials and audits requirement expansion previously wrapped each nested private helper separately,
producing two or three identical case/cooldown sentences. The final expansion now
combines those predicates into at most one private-case line. Constant always=yes
checks are omitted, and general administrative eligibility is retained in a native
hidden_trigger instead of a visible generic sentence. Native Authority, reserves,
war, modifiers and formatted custom-stat requirements stay separate.

The three older Desk buttons now also retain their service predicate inside
hidden_trigger: chi_adm_req_service is no longer displayed on those buttons. Its
localization remains for other callers. Gameplay gates, effects and costs are
unchanged. Hidden-trigger syntax was verified in installed trigger documentation.

Changed: tools/chi_adm_memorials_presentation.py, generated
common/scripted_buttons/chi_adm_memorials.txt, common/scripted_buttons/chi_adm_core.txt,
tools/validate_chi_adm.py, tools/validate_chi_adm_memorials.py,
tools/chi_adm_court_register_baseline.json, tools/chi_adm_imperial_law_baseline.json,
tools/chi_adm_memorials_baseline.json and this report. Only the older button-file source
checksum was advanced; original mechanical hashes and semantic predicate checks
remain unchanged and pass. Tests reject duplicated private-case summaries and
visible service lines. All five feature validators pass. Runtime check: each
button has no duplicate generic checkboxes and no service tooltip; invalid service
must still disable it. No game launch or later features work.


## Current tooltip correction: native modifier-gain lines

All three older Memorial Desk buttons now execute their existing add_modifier
at the visible effect level, after the hidden custom account change. Their result
localization contains only the custom stat delta; GetStaticModifier name/description
and manually written modifier duration were removed. Native effect localization
now supplies the modifier name, duration and effects. Each modifier is still applied
once, for the same 24 months, in the same execution order. memorials and audits's existing native
show_as_tooltip previews remain; future proposals are still described as conditional.

Changed: common/scripted_buttons/chi_adm_core.txt,
tools/chi_adm_memorials_presentation.py, localization/english/chi_adm_l_english.yml,
tools/validate_chi_adm.py, tools/validate_chi_adm_memorials.py,
tools/chi_adm_court_register_baseline.json, tools/chi_adm_imperial_law_baseline.json,
tools/chi_adm_memorials_baseline.json and this report.
Only the button source checksum was updated in the three manifests. The original
mechanical AST hashes still pass; effect normalization flattens hidden blocks while
excluding tooltip metadata and proves identical live effects. Tests verify one
visible modifier per older button, unchanged costs/cooldowns and no modifier getter
in their result text. All five feature validators PASS. Runtime check: each Desk
button should show one native modifier-gain line and no duplicate manual card.
No gameplay changes or later features work.


## Current localization correction: use native checks where available

Authority, Bureaucracy, gold-reserve, war and modifier requirements in the Desk's
provincial accounts/memorials and audits buttons now use their native predicates directly wherever they are simple
checks. They no longer need a custom sentence that masks the engine's country,
resource icon, concept, comparison and value. memorials and audits helper predicates are expanded
through AND branches to separate public native requirements from private case,
cooldown and phase rules. Mixed OR case rules remain summarized rather than
exposing request-ID variables or incorrectly promoting an alternative requirement.

Loyalty/Autonomy/Corruption retain distinct custom concepts because their values
are mod-owned variables. Their threshold labels now follow native Authority's
layout: current country name, icon, linked concept, comparison and formatted value.
provincial accounts thresholds read the existing script values, not copied numerical constants.
memorials and audits literal thresholds are generated from the actual predicates. Public comparison
checks keep native engine checkboxes; no values or eligibility are altered.

Added namespaced inline icons using the installed texticon schema and Authority's
82-fontsize/0,22 offset. Assets are native population_loyalist.dds, diplomatic
increase-autonomy.dds and modifier_documents_negative.dds. Concept definitions use
these textures too. Concept labels stay distinct from native IG loyalty or subject
Liberty Desire. Native add_modifier/remove_modifier/treasury previews from the
previous pass remain; no additional custom wrapper replaces native modifier text.

Changed: common/scripted_buttons/chi_adm_core.txt (native trigger unwrapping only),
common/scripted_buttons/chi_adm_memorials.txt, common/game_concepts/chi_adm.txt,
localization/english/chi_adm_l_english.yml, tools/chi_adm_memorials_presentation.py,
tools/build_chi_adm_memorials.py, tools/validate_chi_adm.py, tools/validate_chi_adm_memorials.py,
tools/chi_adm_court_register_baseline.json, tools/chi_adm_imperial_law_baseline.json,
tools/chi_adm_memorials_baseline.json and this report.
Created: gui/chi_adm_texticons.gui, tools/chi_adm_native_tooltip_baseline.json.

Only the provincial accounts button-file source checksum was rebased in the three preservation
manifests. The original AST is retained in the new fixture: tests prove the old
and new predicates logically identical after removing text wrappers, and require
all other button fields/effects to match exactly. The original provincial accounts mechanical AST
hashes still pass without rebasing. memorials and audits tests similarly normalize helper expansion
and presentation wrappers, preserving conditions, AI and effects. There are no
changes to resources, cooldowns, balances, progress, laws or outcomes.

All five feature validators PASS. Native texticon assets and concept links are
checked, as are direct authority >=25 checks for old and new memorial buttons.
Runtime acceptance still needs the game's tooltip renderer: verify country/icon/
concept/value comparison lines and icon sizes at 1080p, plus native modifier cards
and the unchanged costs. The game was not launched; no later features work.


## Current memorials and audits presentation rework: live accounts, concepts and native effects

The Provincial Memorial Desk and Provincial Correspondence now include the three
live Loyalty/Autonomy/Corruption bars. They reuse the established 0-100 country
variables, tier labels, native textures and frame pattern, with no monthly UI
synchronization. Labels and hovers link distinct game concepts:
concept_chi_adm_loyalty, concept_chi_adm_autonomy and concept_chi_adm_corruption.
Their Vickypedia descriptions explain what each statistic measures, its range and
important interactions, without equating provincial loyalty with IG loyalty or
Liberty Desire. Existing account labels/hover text receive the same links.

The previous memorials and audits buttons showed the same authored description as introduction,
requirement and effect, while hiding actual resource/modifier helpers. The builder
now generates a presentation-only projection of the real helper effects:

- Native show_as_tooltip blocks show actual add/remove_modifier, add_treasury and
  change_relations effects with native names, durations, formatting and symbols.
  The installed Christ of Nations scripted button and exported effects reference
  establish that show_as_tooltip does not execute its contents.
- The actual helper stays in hidden_effect and retains its existing guards.
  Preview generation strips only the outer availability gate so consequences stay
  readable on disabled buttons. Conditional settlement variants are retained, with
  localized condition labels instead of exposing private request IDs.
- Custom account changes use colored deltas and the new concept links. They are
  custom variables, so no unrelated native IG-loyalty concept is substituted.
- Court buttons use native ScriptedGui.ExecuteTooltip, passing the same row Country
  root used by Execute. Their real actions remain hidden, and tooltip-only effects
  supply the native preview. Informational future proposals remain explicitly
  conditional on provincial acceptance, not presented as immediate payments.
- The three older provincial accounts Desk buttons are unchanged in script. Their result localization
  now includes GetStaticModifier.GetName/GetDesc and the existing 24-month term,
  rather than authored copies of minus-25 Authority or minus-3% Bureaucracy. Native
  concepts_l_english.yml uses GetStaticModifier.GetDesc to show modifier effects.
- Money prose uses the native @money! icon and formatted amounts, with reserves,
  treasury and Authority/Bureaucracy/Prestige concept links. Duplicate long memorials and audits
  button descriptions are replaced by a short purpose, requirements and native
  effect preview. Future requested aid amounts/concessions remain explained.

Empty memorial/last-result fields are hidden when no case has been filed. The
account panel remains visible so governors can see what their choices affect.
All new English, including concept names/descriptions, remains exclusively in
localization/english/chi_adm_l_english.yml.

Files created:

- common/game_concepts/chi_adm.txt
- tools/chi_adm_memorials_presentation.py
- tools/chi_adm_memorials_presentation_baseline.json

Files modified:

- tools/build_chi_adm_memorials.py
- common/scripted_buttons/chi_adm_memorials.txt (tooltips only)
- common/scripted_guis/chi_adm_memorials.txt (tooltip wrappers and a read-only display gate)
- gui/journal_entry_widgets/chi_adm_memorials.gui
- localization/english/chi_adm_l_english.yml
- tools/validate_chi_adm.py (5% Bureaucracy text check now expects a concept link)
- tools/validate_chi_adm_memorials.py
- docs/chi_adm_progress.md

Gameplay is unchanged. A new presentation baseline preserves the memorials and audits effects,
mechanical triggers, modifiers, on-actions and events byte-for-byte; tests compare
old/new live button actions, eligibility and AI after excluding tooltip metadata.
The same check unwraps court presentation layers and compares the original live
helper. A model executes the button/GUI wrappers to confirm previews do not double
payments. The older provincial accounts button script is still at its original checksum; temporary
concurrent edits observed during validation were not overwritten by this task.

PASS: all five feature validators, including memorials and audits's live-state model and new
presentation checks. Checks cover six live stat bars across the two province
widgets, custom concept definitions/localization, native concept references,
modifier description lookups, treasury formatting, and unchanged execution.
imperial law reform generated registry freshness also passes. No preservation baseline was rebased.

User runtime checks: open the Desk/Correspondence at 1920x1080; hover all three
concept labels and tiers; verify bars update after a choice; inspect all six Desk
buttons for single, native modifier previews and correct terms; verify court
hover previews use the selected subject's terms; accept a fiscal compromise and
check both treasury balances exactly once. Check long tooltips, scrolling and
error.log for unresolved concepts or ExecuteTooltip scope errors. Rendering and
actual native tooltip layout remain unverified; the game was not launched.
No negotiated integration-regional works work.


## Feature status: memorials and audits memorials, edicts and corruption

memorials and audits implementation and source/model validation are finished; runtime acceptance
is pending. No negotiated integration-regional works work. Existing provincial accounts-imperial law reform scripts/GUI are protected by hashes;
office titles offices and SHN remain unchanged. The only functional earlier-file extension
is three memorial buttons and a status widget in the existing Memorial Desk.

### Design and scope

Play the relationship between the Dragon Throne and appointed provincial offices:
request concessions, answer court instructions, inspect accounts and negotiate
settlements. Architecture is a small portfolio of four nested JEs sharing
country-owned request state. Three memorial types and three edicts follow the
brief's first-release limit; this is not the later regional works flavor catalog. Military
assistance is funded emergency discretion with a payroll burden; no new units,
army modernization buffs or provincial development militia/reorganization system is introduced.
Honors are a proactive edict; appointment/dismissal is not implemented.

Court: Governance of the Empire -> Imperial Memorials / Imperial Edicts /
Imperial Audits. Each uses the repaired AccessPlayer.GetSubjects pattern with
collapsed target rows and real scripted-GUI actions. Province: Provincial Memorial
Desk files requests; Governor's Accounts -> Provincial Correspondence contains
replies, edict terms and the live audit progress bar. Existing ruler portraits,
progress bars, native titles and imperial law reform Directive remain intact.

### Memorials

One pending memorial per subject; filing needs 25 provincial Authority and commits
it for six calendar months. A 730-day target cooldown prevents repeated filing.
Court has six monthly reviews to answer; a compromise gets three for acceptance.

| Memorial | Full approval | Negotiated version |
| --- | --- | --- |
| Fiscal relief | Qing pays province GBP 20,000; Loyalty +5 | GBP 10,000; Loyalty +3 |
| Administrative latitude | Bureaucracy +2% for 12 months, Autonomy +5, Corruption +2, Loyalty +2 | Autonomy +3, Loyalty +1; no Bureaucracy bonus |
| Emergency assistance, at war | Qing pays GBP 10,000; Autonomy +3, Loyalty +3, military wages +5% for 12 months | GBP 5,000, Autonomy +2, Loyalty +2, same wage obligation |

Approval or counteroffer commits 25 Qing Authority for six months. Both gate on
available Authority and no current memorials and audits court-staff commitment. Cash approval and
counter acceptance check gold reserves at the moment of payment. Every transfer
subtracts exactly what it adds to the other country; these are finite subsidies,
not new taxes or a duplicate of the existing 30% remittance. Filing itself grants
nothing. A counteroffer never pays before provincial consent. Refusal costs the
province 3 Loyalty and 3 relations; withdrawal/expiry pays nothing. Historical
memorial rows and the last register entry remain available.

### Edicts and court capacity

Three proactive actions, each with a two-year/730-day target cooldown and the same
six-month, 25-Authority Qing staff cost:

- Supervision, requiring Corruption >=40: on consent, Corruption -5, Autonomy -3
  (-1 in frontier offices), Bureaucracy -2% for twelve months. Revised terms:
  Corruption -3, no Autonomy loss, Bureaucracy -1% for twelve months.
- Commendation, requiring Loyalty >=60 and Corruption <60: Loyalty +5, Autonomy -2,
  Prestige +5% for twelve months. Revised terms keep the prestige recognition but
  give Loyalty +3 and no Autonomy loss.
- Emergency military assistance, while the province is at war: Qing-funded
  GBP 10,000, Autonomy +3, military wages +5% for twelve months. Revised terms:
  GBP 5,000 and Autonomy +2, same wage burden. Funding/war are checked on acceptance.

Governors accept, appeal once, postpone once (-2 Loyalty), or decline (-6 Loyalty,
-5 relations). Initial response window is six reviews; appeal, delay and revised
terms allow three. An expired edict costs 3 Loyalty and closes without compliance.
Qing can negotiate the reduced terms or withdraw. Human non-response never accepts
an edict, changes a government or authorizes a payment.

A live subject-count predicate permits at most **two outstanding edicts or audits
combined**, with one such intervention per province. There is no global counter
that can leak on annexation. Invalid/former subjects no longer occupy capacity.
Memorials are separate and still limited to one per subject.

### Audits and settlements

Censorate dispatch costs the same Qing staff commitment and starts a 1,095-day
province cooldown (three years). It shares the two-intervention capacity cap.
Province chooses:

| Conduct | Monthly progress | Cost / tradeoff |
| --- | --- | --- |
| Cooperate | +25/100: four investigation reviews | Bureaucracy -2% while investigating; better disclosure; a clean finding gives Loyalty +2, Corruption -3 |
| Obstruct | +10/100: ten reviews | Loyalty -3; cannot prevent completion |
| Conceal | +20/100: five reviews | GBP 5,000 spent, Corruption >=40; lower detection, but successful concealment adds Corruption +3, Autonomy +2 and four years of suspicion |

No response for three reviews becomes obstruction, not consent to restitution.
The bar reads the actual 0-100 country variable; only an active inquiry shows it.
Progress clamps at 100. No separate monthly UI synchronization is used.

Native random_list has detected/clean weights. Detection starts at 50 against a
clean weight of 50: +60 at Corruption >=60; -40 below Corruption 20; -20 at Loyalty
>=60; +20 cooperation; -30 concealment; +40 prior suspicion; -10 war; +10 Bureaucracy
deficit. Detection weight is clamped 10-150, so both outcomes remain possible.
Example: loyal, highly corrupt cooperation is 110/(110+50), about 69%; concealment
is 60/(60+50), about 55%. Low-corruption loyal cooperation is 10/(10+50), about 17%.
These are source-derived weights; native random interpretation still needs testing.

Exposed accounts cost 2% Bureaucracy for up to twelve months. Qing has six reviews
for a finding, then can request restitution, propose administrative reform, or
recognize local patronage. A proposed settlement requires a provincial reply within
three reviews:

- Restitution: governor authorizes GBP 10,000 transferred from provincial reserves
  to Qing, Corruption -12, Loyalty -4, Autonomy -3. Removes exposed-account burden.
- Administrative reform: governor accepts Corruption -10, Loyalty -2, Autonomy -3
  (-1 frontier), Bureaucracy -2% for twelve months; no treasury payment. Available
  instead of a restitution demand when funds are short; removes exposure burden.
- Refusal: Loyalty -8, Autonomy +3, relations -5; existing exposure penalty remains.
- Court tolerance: Corruption +3, Loyalty +2; costs Qing another free staff
  commitment and leaves suspicion/exposure burdens. It creates no treasury income.

An expired finding or settlement costs 3 Loyalty and closes without forced reform
or money. Suspicion costs 1% Bureaucracy for 48 months and raises later detection;
48 months deliberately exceeds the 36-month audit cooldown, making future risk
real. Named modifiers are explicitly removed before reapplication to prevent
stacking. provincial accounts's existing corruption tiers remain authoritative and are not duplicated.

### State, AI and cleanup

Memorial: inactive -> filed -> approve/reject/counter -> accept/withdraw/expire.
Edict: inactive -> offered -> accept/appeal/delay/decline -> revised terms or close.
Audit: inactive -> await registers -> investigate -> no finding or exposed -> court
proposal -> governor settlement/refusal, or court tolerance/expiry.
Invalidity takes priority over rewards and payments. All mutations are guarded;
repeat calls cannot pay or reward a resolved case. Flags/cooldowns persist through
scalar save serialization; actual engine save/load remains untested.

Country state stores numeric type/stage/progress/deadline and use flags. Saved
country scope is used only by immediate informational events, whose acknowledgement
has no gameplay effect. Durable decisions remain in JEs and revalidate live state.
A monthly country helper runs only for pending cases, relevant temporary modifiers,
or valid administrations with an AI Qing court. No daily/weekly/global country scan.

AI governors use native scripted-button decisions: poor reserves favor fiscal
requests; bureaucracy deficits favor latitude; high loyalty favors compliance;
autonomy favors appeals/obstruction; low loyalty favors refusal; high corruption
raises concealment willingness. Same costs and gates apply to humans and AI.
AI court grants/counters affordable memorials when staff are free, negotiates edict
appeals, proposes restitution for rich corrupt offices or reform otherwise. It can
proactively audit high corruption, fund wartime aid, order supervision when existing
Mandate Centralisation >=6, or commend loyal clean offices. It uses the same global
capacity, cooldowns and staff costs, without a new imperial authority variable.

All fifteen original tags including SHN can participate. Frontier cooperation has
smaller Autonomy reductions for supervision/reform, and no customary laws or offices
are changed. Tibet, Korea, Lanfang and unrelated countries remain excluded through
provincial accounts target validity. Independence, incompatible Qing court, fragmentation and
revolution clear pending protocols and contextual memorials and audits modifiers on the next active
review; cooldowns/history remain to prevent reset exploits. Annexed countries leave
the live UI/capacity count; no global money obligation or reference counter remains.
Spent money and timed court/provincial clerical costs are not refunded.

### Exact files

Created:

- common/scripted_triggers/chi_adm_memorials.txt
- common/scripted_effects/chi_adm_memorials.txt
- common/scripted_buttons/chi_adm_memorials.txt
- common/scripted_guis/chi_adm_memorials.txt
- common/static_modifiers/chi_adm_memorials.txt
- common/on_actions/chi_adm_memorials.txt
- common/journal_entries/chi_adm_memorials.txt
- common/customizable_localization/chi_adm_memorials.txt
- events/chi_adm_memorials.txt
- gui/journal_entry_widgets/chi_adm_memorials.gui
- tools/build_chi_adm_memorials.py
- tools/validate_chi_adm_memorials.py
- tools/chi_adm_memorials_baseline.json

Modified:

- common/journal_entries/chi_adm_court_register_governance.txt (desk buttons/widget only).
- localization/english/chi_adm_l_english.yml (all new memorials and audits English).
- tools/validate_chi_adm.py (allow memorials and audits localization prefix).
- tools/validate_chi_adm_court_register.py (expect exactly the three new desk buttons).
- docs/chi_adm_progress.md (this report).

The memorials and audits baseline hashes earlier content and compares the court register JE AST after removing
only the authorized additions. Existing baselines were not rebased. imperial law reform localization
mappings remain generated at EOF; the memorials and audits builder inserts its block ahead of them,
so both builders are idempotent without deleting imperial law reform English.

### Validation and limits

PASS:

```text
python tools/validate_chi_adm.py
python -B tools/validate_chi_adm_court_register.py
python -B tools/validate_chi_adm_government_titles.py
python -B tools/validate_chi_adm_imperial_law.py
python -B tools/validate_chi_adm_memorials.py
python -B tools/generate_chi_adm_imperial_law_tables.py --check
```

memorials and audits's bounded interpreter executes the actual effect/trigger AST with a small native
adapter. It tests fifteen offices, zero-sum payments, depleted reserves, one pending
memorial, counter consent, repeat rewards/cooldowns, two edicts, frontier supervision,
all audit conduct modes and both finding branches, restitution/reform, inactivity,
AI decisions, scalar serialization and invalidation. Static checks parse native
syntax, localization, GUI models/actions, modifier assets and protected file hashes.
Native modifier timing, AI click cadence and random distribution are not simulated.

Source-only rubric: agency 4/5, legibility 3, integration 4, pacing 3, consequence 4,
reactivity 4, lifecycle 4, narrative 4: 74/100. Meaningful cost/consent paths are
present; legibility/pacing ratings are provisional until actual GUI and AI testing.
This is a bounded first release, not claimed runtime-verified flagship content.

User in-game checklist (game was NOT launched):

1. Open the three court subentries and the extended provincial Desk at 1920x1080;
   verify collapse/scrolling, country contexts, cost tooltips and no clipped text.
2. Each memorial: full grant, counter acceptance/withdrawal, rejection, insufficient
   court cash, no repeat transfer and six/three-review expiry.
3. Each edict: acceptance/revised terms, one appeal/delay, refusal, expiration,
   war-ending/affordability checks and maximum two interventions across targets.
4. Each audit conduct mode, live 0-100 bar, random findings, every settlement,
   suspicion affecting a later audit, no stacking and cleanup of temporary burdens.
5. All fifteen subjects including SHN and four frontier offices; independence,
   annexation, fragmentation and Qing collapse while correspondence is pending.
6. Save/reload midway through a case and audit; a two-human Qing/province session;
   AI court/gov behavior and error.log for scopes, random weights, GUI and assets.
7. Regression: provincial accounts statistics/actions, court register portraits/ledger, office titles governments/titles,
   imperial law reform instant/12-month adoption, all-law icons/queues, 30% remittances, military
   sharing and the unchanged existing integration system.

No essential native scripting blocker was found. Installed native patterns are
reused for weighted random lists, country money/reserve checks, timed modifiers,
country notifications, nested JE groups and progress bars. memorials and audits uses its own request
state because imperial law reform is exclusively a law-adoption commitment. Emergency aid does not
pretend to be a full native militia/recruitment authorization system; that remains
provincial development. No appointments, integration, dynasty or rebellion systems were implemented.

Next prompt: "Repair memorials and audits runtime results only using error.log and screenshots;
preserve provincial accounts-imperial law reform and do not begin negotiated integration-regional works." Changelog: added three two-way memorials,
three consent-based edicts, bounded corruption investigations, court/province views,
AI, cleanup and focused memorials and audits validation. STOP after memorials and audits.


## Current imperial law reform gameplay change: instant or twelve-month adoption

Supersedes all earlier normal-enactment and enactment-bonus behavior. Provincial
compliance now offers immediate adoption or a 12-calendar-month implementation
period followed by direct adoption. Both retain native law_is_available checks
for technology, conflicting laws and special restrictions, but do not require
ordinary political enactment support. Instant adoption is offered to all eligible
administrations without the old Loyalty/Autonomy/Corruption/Centralisation gates;
it retains its existing once-only rewards and transition modifier.

Gradual acceptance no longer calls start_enactment or adds enactment modifiers.
It enters status 3, applies an untimed Imperial Reform Implementation lock using
the installed country_cannot_start_law_enactment_bool, and schedules a hidden event
months = 12. This rule is used by native cannot-start-enactment modifiers. The lock
is removed on completion, invalidity, supersession, independent adoption or a
blocked completion. At the end, availability is rechecked before activate_law;
if incompatible, the law stays unchanged and a new response is requested.
Other scripts can still activate laws directly; this locks ordinary enactment starts.

No +10 success, stall reduction, speed or extra setback bonus remains. The old
modifier ID is retained as an empty definition for safe old-save cleanup; its
remaining enactment attachment is removed on the next active-directive review.
An old save already enacting a law is not cancelled: it is converted to accepted
queue status, then starts the new period when free. Queued compliance still
preserves another reform; only explicit prioritization cancels one. Petitions,
delays, refusals, court events and all 264-law/15-subject coverage remain.

Generated per-law hidden events check the active request ID/status and a 360-day
minimum-age flag. The actual adoption schedule is 12 calendar months, not 360 days
or 12 monthly reviews. Together with the existing 365-day per-law reissue guard,
the age flag prevents an obsolete event adopting a newly reissued same-law request;
different-law obsolete events fail their ID check. The UI counter remains an
approximate monthly-review countdown; acceptance text states the calendar term.
No unaccepted timeout changes a law. Save/load retains normal event scheduling,
country variables and modifiers; actual engine persistence still needs testing.

Changed: common/scripted_effects/chi_adm_imperial_law.txt,
common/scripted_buttons/chi_adm_imperial_law.txt,
common/static_modifiers/chi_adm_imperial_law.txt,
common/on_actions/chi_adm_imperial_law.txt,
common/customizable_localization/chi_adm_imperial_law.txt,
localization/english/chi_adm_l_english.yml,
tools/generate_chi_adm_imperial_law_tables.py, tools/validate_chi_adm_imperial_law.py,
tools/chi_adm_imperial_law_gui_mechanics_baseline.json,
docs/chi_adm_imperial_law_coverage.md and this report.
Created: events/chi_adm_imperial_law_implementation.txt.
The imperial law reform GUI baseline was rebased only because this request explicitly changes imperial law reform
mechanics. provincial accounts/court register/office titles preservation baselines remain unchanged.

Validation: generator freshness and all four feature validators PASS. New tests
cover all 264 dispatch/implementation/adoption IDs, 12-month event schedules,
no normal enactment or bonus additions, blocking during the period, queue/consent,
refusal, availability failures, invalidation and once-only completion rewards.
These replace tests that required ordinary enactment. Native calendar passage,
rule enforcement and save/load are not simulated by the model.
User runtime checks: both adoption choices, full twelve-month timing, blocked
Politics enactment buttons, unlock on success/invalidity/supersession, no bonus
modifier, save/reload halfway through, stale events, and old-save migration.
The game was not launched. No memorials and audits work.


## Current imperial law reform display change: hide unavailable response section

The response widget now uses a read-only scripted GUI checking the existing
chi_adm_imperial_law_can_answer predicate. Its title and Compliance/Negotiation/Refusal
headings therefore disappear during enactment, accepted queues, petitions and
exemptions, when no response can be chosen. They return when a response is available.
The JE status prompt uses the same predicate through customizable localization,
returning an empty string when no response is due. Native journal_entry.gui hides
the status panel when JournalEntry.GetStatusDesc is empty (lines 355-356).
Administrative Status and all mechanics remain unchanged.

Changed: common/scripted_guis/chi_adm_imperial_law.txt,
common/customizable_localization/chi_adm_imperial_law.txt,
gui/journal_entry_widgets/chi_adm_imperial_law.gui,
localization/english/chi_adm_l_english.yml, tools/validate_chi_adm_imperial_law_gui.py,
and this report. All validators pass. Runtime check: start imperial enactment and
confirm both the choose-response prompt panel and response group headings vanish;
a blocked/ended enactment requiring a reply should restore them. No memorials and audits work.


## Current icon-only repair: direct native law textures

The user's screenshot confirms the previous Country.GetCustom-to-texture path
still displayed no icons. Its source asset paths all exist, so asset existence
alone was an insufficient test. No matching icon error was found in the available
error.log. The exact engine failure is not established; the failed text-to-image
bridge is removed from the actual widget rather than claimed fixed again.

The two 48x48 icon slots now bind directly to native GUI objects, without passing
texture paths through localization. Requested-law images use
GetLawType('law_key').GetTexture. Current-law images use
Country.GetActiveLawFromGroup('group_key').GetTexture, so the engine reads the
province's current law afresh. These combine already-used native GetLawType and
GetActiveLawFromGroup getters with LawType.GetTexture/Law.GetTexture from the
installed custom_tooltip.gui. The icon primitive is also used in native JE widgets.

The complete registry generates 264 requested-law icons and 27 current-group icons.
Each slot is a fixed 48x48 widget with overlapping centered icons, not a flow that
reserves space for every hidden icon. Pure country-scoped scripted GUI predicates
show exactly one requested ID and one requested group; the group predicates use
existing directive state. Current textures change directly with the active law.
These are native law objects and textures, not static placeholders or a monthly
synchronization system. Presentation checks run on UI evaluation; the fixed
registry has 291 read-only selectors. Runtime performance still needs observation.

Changed: tools/generate_chi_adm_imperial_law_tables.py,
gui/journal_entry_widgets/chi_adm_imperial_law.gui,
tools/validate_chi_adm_imperial_law_gui.py and this report.
Created: common/scripted_guis/chi_adm_imperial_law_icons.txt.
No localization or gameplay file changes in this repair. Existing unused texture
localization lookups remain harmless but are no longer connected to the GUI.

Generator freshness and all four feature validators PASS. Focused checks now
reject Country.GetCustom image bindings, assert every requested native texture
getter exactly once, assert every current-group getter exactly once, verify all
291 selectors are read-only country predicates, and preserve gameplay hashes.
In-game acceptance remains pending: verify both icons initially, after a request
changes, after provincial law changes, and for modded laws. Confirm no overlapping
icons or error.log getter failures. The game was not launched; memorials and audits not started.


## Current imperial law reform GUI-only bugfix: response filters, frames and native textures

Causes found in source: all three HasTag expressions were missing the closing
single quote around their tag. These malformed visibility expressions could not
filter the three copies of the native scripted-button collection, matching the
reported repetition. The expressions are corrected using the exact native
ScriptedButton.HasTag syntax from tsarpoints_widgets.gui. Each of the seven possible
buttons has exactly one group; the ordinary five appear once, while busy subjects
retain queue/prioritize choices. Existing native eligibility/tooltips/ExecuteEffect
and all button definitions are unchanged.

The previous icon lookup passed GetTexture expressions through localization and
then through Country.GetCustom into a texture property. This relied on nested
localization getter evaluation in an image context, which did not render in the
reported game. Replaced it with a generated lookup of actual effective law icon
paths from installed/mod common/laws definitions. Requested icon selects by the
existing directive ID; current icon selects by that ID's group AND the province's
live has_law. This is a dynamic selection of real native textures, not placeholder
art, and requires no synchronized variable or saved law scope. All 264 referenced
texture files were verified to exist in the mod or installed game. The native
icon component and texture string property are retained; nested GetTexture
localization is removed. New pure presentation predicates live in
common/scripted_triggers/chi_adm_imperial_law_icons.txt.

Summary and Administrative Status now have independent framed flow panels, each
with 16 horizontal / 14 vertical child margins and 10-pixel spacing. Text has
440-pixel wrapping width; icon rows reserve 48 pixels plus 12 spacing and 380 for
text, totaling the same width. Panels therefore occupy 472 pixels including
margins. Text remains multiline and height-auto-sized, with no fixed panel height.
Buttons are 472x68 with centered 440-pixel wrapped labels. Native layout properties
were checked against tsarpoints_widgets.gui and journal_entry.gui. Content can
extend vertically through the journal's scrolling area instead of spilling through
one fixed frame. Actual text/font/UI-scale behavior still needs runtime testing.

Changed: gui/journal_entry_widgets/chi_adm_imperial_law.gui,
common/customizable_localization/chi_adm_imperial_law.txt,
localization/english/chi_adm_l_english.yml, tools/generate_chi_adm_imperial_law_tables.py,
tools/validate_chi_adm_imperial_law.py and this progress report.
Created: common/scripted_triggers/chi_adm_imperial_law_icons.txt,
tools/validate_chi_adm_imperial_law_gui.py, tools/chi_adm_imperial_law_gui_mechanics_baseline.json.
All localization remains in the designated English file. No gameplay changes.

Validation: all four feature validators and generator freshness PASS. The imperial law reform
validator now invokes the focused GUI checks: balanced expression quotes and
parentheses, exact unique filters/group membership, free/busy one-copy rendering,
panel widths/padding and auto-height rows, all native icon assets and live
current-law selection. Hashes prove imperial law reform effects, mechanical triggers, scripted
buttons, modifiers, on-actions and court events are byte-for-byte unchanged.

User runtime checks remain: all five responses appear once in the correct groups;
busy queue/prioritize also appear once; long/custom law names and active-support
text wrap within both panels at 1920x1080; icons load initially and update on
request supersession and provincial law changes; tooltips, eligibility and scrolling
work with UI scaling. Source checks cannot prove rendering. No game launch or memorials and audits.


## Current imperial law reform refinement: dossier layout and assisted enactment

Supersedes earlier +5-point and ordinary-political-eligibility notes below.
The Directive now has Reform Summary, Administrative Status and Provincial
Responses sections. Requested/current icons use generated country custom
localization with native GetLawType.GetTexture and
Country.GetActiveLawFromGroup.GetTexture. Names/groups remain native bindings.
Multiline/autoresize/max_width replaces cramped fixed-height text. Status shows
remaining reviews, all active bonuses, and whether an enactment is in progress.

Response buttons use the native custom_widget_container_buttons, three nested
JournalEntry.GetScriptedButtons models and native ScriptedButton tags. Compliance,
Negotiation and Refusal have full-width buttons with native IsValid/ExecuteEffect
and SCRIPTED_ACTION_TOOLTIP. Original scripted-button AI and costs remain; no
presentation synchronization or duplicate action implementation was introduced.

Gradual starts now require law_is_available rather than can_be_enacted, waiving
ordinary political support. Native imposition events also start enactment without
that political guard. The exported start_enactment effect has no verified force
or selective ignore flag. Technology, conflicting-law and custom availability
restrictions remain safety checks: arbitrary custom can_enact restrictions are
NOT bypassed. A native refusal to start is checked and becomes a notified blocked
case. Immediate adoption retains its stricter original conditions.

The four verified installed modifiers are:

- country_law_enactment_success_add = 0.10 (+10 percentage points).
- country_law_enactment_stall_mult = -0.20 (-20% multiplicative stall chance).
- country_law_enactment_speed_mult = 0.50 (+50% enactment speed).
- country_law_enactment_max_setbacks_add = 1 (one extra setback tolerated).

Installed modifiers_l_english.yml defines maximum setbacks as the number that
can be suffered before enactment fails. No current setback is inflicted.
Support remains once per directive, non-stacking, restricted to the intended
reform and at most 12 monthly reviews. Original cleanup removes it after success,
failure, cancellation, invalidity, supersession or changing enactment. Busy
acceptance queues; only explicit prioritization cancels the existing enactment.
Petitions/refusal, court events, all 264 laws/all 15 subjects and provincial accounts/court register/office titles remain.
No memorials and audits work.

Changed files: common/static_modifiers/chi_adm_imperial_law.txt,
common/scripted_effects/chi_adm_imperial_law.txt,
common/scripted_buttons/chi_adm_imperial_law.txt,
common/customizable_localization/chi_adm_imperial_law.txt,
common/journal_entries/chi_adm_imperial_law.txt,
gui/journal_entry_widgets/chi_adm_imperial_law.gui,
localization/english/chi_adm_l_english.yml,
tools/generate_chi_adm_imperial_law_tables.py, tools/validate_chi_adm_imperial_law.py,
docs/chi_adm_imperial_law_coverage.md and this progress report.

Generator freshness and all four feature validators PASS. New assertions cover
exact modifiers, native grouped-button models and politically unsupported starts;
existing queue, hard-availability failure and law-specific cleanup tests pass.
Still requires user runtime testing: 1920x1080 sizing/scrolling, localized icon
texture expansion and custom laws; native button groups/tooltips; unsupported
political start versus blocked technology/custom restrictions; actual four bonus
values, maximum setback allowance, expiry and removal on every termination path;
court events and queued consent across actual save/load and multiplayer.
Source/model checks do not establish engine behavior. The game was not launched.


## Current correction: automatic directives; Reform Docket retired

Supersedes the docket and manual-only frontier behavior described below.
Every supported Qing law activation now automatically dispatches a provincial
Imperial Reform Directive to all **15** unique administrative subjects, including
the four frontier administrations, when they do not already hold the law.
The complete 264-law / 27-group registry remains. This issues requests, never
forces adoption or cancels an existing enactment. Normal eligibility, repeat
guards, accepted queues, conflicts and bounded backlog behavior remain unchanged.

The Imperial Reform Docket widget is removed. Its JE definition is retained only
as an invisible, impossible-to-start retirement stub with an immediate hidden
outcome, so already-active copies can close in existing saves. It has no buttons
or widget. No manual court selection is required to dispatch new Qing laws.
The existing native manual law interaction remains available where supported.

Petitions/refusals now give the Qing player court response options directly in
the notification event: exemption, renewed gradual offer, or maintain/censure,
using the same guarded effects, costs and one-use limits. Default acknowledgement
does nothing; existing AI court handling remains. These event options use native
trigger/show_as_unavailable syntax. Frontier governors retain normal enactment
requirements and explicit consent; immediate direct adoption stays unavailable
to them. The working provincial Directive widget is preserved.

Changed: `tools/generate_chi_adm_imperial_law_tables.py`, generated
`common/scripted_effects/chi_adm_imperial_law.txt`,
`common/journal_entries/chi_adm_imperial_law.txt`,
`gui/journal_entry_widgets/chi_adm_imperial_law.gui`, `events/chi_adm_imperial_law.txt`,
`localization/english/chi_adm_l_english.yml`, `tools/validate_chi_adm_imperial_law.py`,
`docs/chi_adm_imperial_law_coverage.md`, and this progress report.

Validation: generator freshness and all four feature validators pass. Expanded
imperial law reform model tests now expect automatic frontier delivery in every law group and
verify the docket has no active GUI or possible activation. Runtime still needs:
Qing law activation reaching all 15 subjects, already-adopted subjects skipped,
frontier refusal/queue, petition event options/costs, and closure of a docket
already stored in a save. The game was not launched. memorials and audits was not started.

## Current correction: imperial law reform full law coverage

This section supersedes the four-law scope and frontier/monarchy restrictions in
the historical imperial law reform report below. **Implementation and automated checks are complete;
Victoria 3 runtime acceptance is pending.** No memorials and audits work was started.

### Coverage and request paths

imperial law reform now registers **all 264 effective laws in all 27 installed law groups**, including
this mod's custom laws. There is no category whitelist. Native files are overlaid
by same-named mod files; explicit `REPLACE:` definitions override their originals.
Generated mappings include dispatch, native request conversion, legal-law binding,
adoption detection, government support, court selection, backlog dispatch and names.

The full per-law report is `docs/chi_adm_imperial_law_coverage.md`. It lists every law's
registry ID, group, source, requestability, presence/absence of a native imposition
predicate, exact declared enactment/visibility/technology/conflicting-law conditions,
and referenced scripted eligibility predicates. Unconditional `can_enact` prohibitions
are explicitly flagged. A country-specific legal verdict cannot be determined from
source alone: technology, institutions, flags, politics and other laws depend on the
current save. The report records exact potential blockers rather than inventing a
universal compatible/incompatible verdict. Native `can_be_enacted` is authoritative.

- Automatic: each actual Qing law activation can request that law from the eleven
  civil administrations that do not already hold it. Provincial activation cannot
  recursively dispatch to the empire.
- Manual native: existing imposition controls are extended through the full registry
  where the law already exposes `can_impose`. The existing redirection prevents a
  competing Foreign Legal Imposition commitment.
- Manual court: open **Imperial Reform Docket**, expand a subject, click **Next
  Imperial Law** to cycle through laws Qing currently holds, then **Send Reform
  Request**. This is functional for every registered law, even with no native
  imposition button. Selection does not authorize provincial adoption.
- Manual requests are available to all fifteen administrations. Frontier subjects
  receive **no automatic civil directive** and cannot use immediate adoption;
  genuine gradual enactment requires their own negotiated response and normal
  legality. Their customary law definitions are untouched.

The docket shows every eligible subject, including subjects without a previous
directive, so the manual path is accessible before the first reform. It displays
the selected imperial law, current directive, current provincial law, and live
eligibility feedback. Feedback distinguishes missing special availability conditions,
an existing enactment, other political/enactment restrictions and satisfied conditions;
Politics provides the native detailed law explanation. Impossible requests remain
available for petition/refusal and cannot bypass native restrictions.

### Persistence and lifecycle preservation

`tools/generate_chi_adm_imperial_law_tables.py` generates the comprehensive registry. Numeric
IDs are permanent allocations in `tools/chi_adm_imperial_law_ids.json`; original IDs 1-4
remain unchanged. New laws append IDs, and removed-law allocations remain reserved.
No delayed law scope is stored. `--check` checks freshness without writing files.
Run the generator after changing installed/mod law definitions, then run validation.
Other enabled mods are not silently assumed part of this folder's load order; their
effective law definitions must be incorporated before generating for that loadout.

Law-group conflict detection now uses generated group mappings rather than numeric
comparisons specific to IDs 1-4. On receiving a new request it derives the existing
record's group too, so prior four-law pending saves need no ID migration. Same-group
contradictions supersede tracking without cancelling actual enactment. The existing
bounded capacity remains: one active request and one later unaccepted cross-group
decree behind an accepted queue/enactment. The newest later decree replaces the
backlog; an unanswered active request can be superseded by a newer directive.

All negotiated responses, one-use petition/delay/refusal limits, court costs, success
rewards, repeat guards, temporary support and no-forced-timeout policy remain.
Human queue acceptance still explicitly authorizes future native enactment. Only
voluntary prioritization cancels another enactment. An incompatible queued law is
not started; it returns a blocked response requiring attention. Snapshot tests verify
scalar serialization only, not the actual engine's save/load behavior.

imperial law reform eligibility no longer requires provincial/Qing monarchy or provincial accounts initialization:
governance and power-distribution requests must not disappear merely because those
laws change. It still requires the original administrative tag, direct relationship,
Qing setup and no fragmentation. The imperial law reform court JE uses its own matching court-valid
predicate. Existing provincial accounts/court register court eligibility is unchanged: if Qing ceases to be a
monarchy, their original monarchic-court conditions can make those systems dormant;
imperial law reform does not rewrite their behavior or government/title definitions. Native law
activation callbacks, including their intentional secondary law changes, remain
authoritative. Existing army sharing is also unchanged.

### Exact files in this correction

Created:

- `tools/generate_chi_adm_imperial_law_tables.py`
- `tools/chi_adm_imperial_law_ids.json`
- `docs/chi_adm_imperial_law_coverage.md`

Modified:

- `tools/chi_adm_imperial_law_catalog.json`
- `tools/validate_chi_adm_imperial_law.py`
- `common/scripted_triggers/chi_adm_imperial_law.txt`
- `common/scripted_effects/chi_adm_imperial_law.txt`
- `common/on_actions/chi_adm_imperial_law.txt`
- `common/customizable_localization/chi_adm_imperial_law.txt`
- `common/scripted_guis/chi_adm_imperial_law.txt`
- `common/scripted_buttons/chi_adm_imperial_law.txt`
- `common/journal_entries/chi_adm_imperial_law.txt`
- `gui/journal_entry_widgets/chi_adm_imperial_law.gui`
- `localization/english/chi_adm_l_english.yml`
- `docs/chi_adm_progress.md`

No changes to the 15 subjects, territory, 30% remittances, government/title
definitions, provincial accounts values/actions, court register widgets, military sharing, integration or other
features. New English remains exclusively in the designated localization file.

### Checks and required user runtime tests

Run and passing:

```text
python -B tools/generate_chi_adm_imperial_law_tables.py --check
python tools/validate_chi_adm.py
python -B tools/validate_chi_adm_court_register.py
python -B tools/validate_chi_adm_government_titles.py
python -B tools/validate_chi_adm_imperial_law.py
```

Expanded tests check exact effective-law/group coverage, generated freshness,
permanent ID allocation and preservation of IDs 1-4. All 264 identities are dispatched
and tested against denied native legality and refusal. All 27 groups have queued
serialization/restoration, native enactment initiation, same-group supersession and
manual frontier participation checks. The manual selector is checked against all
laws currently held by the simulated court. Original lifecycle tests still pass.
The model executes actual effect/trigger branches; disjoint generated law-match
branches use a checked ID jump table to avoid an artificial cubic Python scan.
Custom restrictions are verified as present in the source report and delegated to
native legality, whose results are injected into the model. These tests do not
evaluate Paradox's actual enactability, native callbacks or networking.

User runtime acceptance remains required; the game was not launched:

1. New and existing four-law saves: verify old pending IDs and queued consent persist.
2. Request examples from all 27 groups, including custom Qing education/health,
   economy, military, citizenship/religion, governance and power distribution.
   Verify both legal and deliberately ineligible cases against native Politics.
3. Manual selector/button rendering, disabled reasons, all fifteen target rows,
   native interaction routing and absence of duplicate native/imperial law reform commitments.
4. Busy/queued/rejected requests, cancellation only by explicit prioritization,
   conflicting laws, backstage backlog and two-human save/reload.
5. Frontier manual consent with no automatic requests or immediate adoption;
   existing customary protections and native custom-law restrictions remain intact.
6. Native GUI error.log, scope/order errors, actual support modifier removal,
   court decisions and regression of completed provincial accounts/court register/office titles content.

No known engine limitation intentionally excludes any registered law from requests.
Native legality can prohibit enactment; this produces a negotiated blocked case.
Native law-reference persistence remains unverified, which is why the complete
generated registry is used. Rendering, native event ordering and true save/load
remain unverified engine behavior, not claimed complete.

Next prompt: **"Repair imperial law reform full-law runtime results only; read the coverage report
and supplied error.log. Preserve prior features and do not begin memorials and audits."**
Changelog: full registry, permanent ID allocator, real group conflicts, full manual
court path, manual frontier negotiation, live eligibility and comprehensive coverage
tests/report. Stop after this imperial law reform expansion.

## Current work: imperial law reform negotiated imperial law reforms

Implementation saved; source and bounded effect-model checks pass. **Runtime
acceptance remains pending.** provincial accounts/court register/office titles were reported tested by the user; their
historical repair notes below are retained. No memorials and audits-regional works work was started.

### Supported slice and changed behavior

The old `chi_qing_apply_imperial_law` callback no longer directly activates laws
in civil administrations. Qing's activation now issues voluntary directives for
this explicit whitelist:

| Persistent ID | Law | Group |
| --- | --- | --- |
| 1 | Local Police Force (`law_local_police`) | Policing |
| 2 | Dedicated Police Force (`law_dedicated_police`) | Policing |
| 3 | Per-Capita Taxation (`law_per_capita_based_taxation`) | Taxation |
| 4 | Proportional Taxation (`law_proportional_taxation`) | Taxation |

Other laws do not propagate through this callback. Government forms, Qing-only
variants, protected customary laws and other unverified laws are excluded.
Eligible recipients are the eight viceroyalties and three civil governorates,
including **SHN**. MGL/QIM/XIN/QXN, Tibet, Korea, Lanfang and unrelated subjects
are excluded. Each recipient must still be a valid direct Qing administration
with a monarchy. Provincial activation cannot redispatch an empire-wide decree.

Initial laws, all 15 subjects and territories, 30% remittances, army/technology
sharing, Mandate Centralisation, integration, governments/titles, succession,
provincial accounts statistics/actions, portraits and court register GUI layouts remain preserved.

### Native mechanics reused and custom state required

Inspected installed Victoria 3 1.15.1 law definitions, native law-imposition JE,
events/buttons, `can_impose_law_default`, and law on-actions. The native default
rights predicate omitted the Qing custom subject types. Its replacement retains
the original branch and adds only Qing-to-eligible-civil rights for the whitelist.

Native manual law requests enter through `on_impose_law`. Supported Qing demands
are converted to the same directive, cancelling the **imposition**, never the
province's enactment. Two narrow guards in `law_imposition_events.1` suppress its
normal event for redirected Qing demands. Other countries retain its original
behavior and the native imposition cooldown remains. Existing Foreign Legal
Imposition commitments are excluded rather than creating a second commitment.

The native Foreign Legal Imposition JE itself is not reused: it blocks ordinary
enactment choices and its event may cancel a current reform. Neither provides the
required accepted queue with preserved enactment. No exported scripted
`impose_law` effect was found in the 1.15.1 generated effect documentation.
Custom scalar state therefore records consent, the law ID, replies and deadlines.
It reuses native `start_enactment`, `cancel_enactment`, enactment modifiers,
law-availability/enactability checks and enactment/activation on-actions.
Only an immediate explicit provincial choice uses `activate_law`.

Manual native UI access additionally depends on each law's own `can_impose`
definition. Policing laws expose this; the taxation definitions inspected do not.
Extending default subject rights alone does not promise native manual tax buttons.
All four laws support automatic dispatch when Qing actually adopts them. Arbitrary
law support and native manual tax exposure are outside this verified slice.

### Provincial responses and court decisions

- **Immediate implementation:** ordinary legal enactability, no current enactment,
  peace, Loyalty >=80, Autonomy <=20, Corruption <40, Bureaucracy surplus >=5%,
  and existing Mandate Centralisation >=6. Adopts only the requested law;
  administrative transition costs 2% Bureaucracy for 12 months.
- **Gradual implementation:** genuine native enactment, ordinary legality and no
  current enactment. Adds +5 percentage points success chance for at most 12
  monthly reviews, once per directive, and only while enacting that law.
- **Petition:** one per directive; keeps law and enactment, notifies Qing and
  awaits a court decision for 12 monthly reviews.
- **Political delay:** one per directive, only when not busy enacting; -3 Loyalty
  and a 12-review response window. Expiry never forces adoption.
- **Refusal:** once per directive; keeps law and enactment, removes any commitment
  to start it, -15 Loyalty, +5 Autonomy and -10 relations; notifies the court.
- **Busy administration default/recommended choice:** explicitly accept for later.
  Status becomes **Awaiting Completion of Current Reform**, with no Loyalty loss
  or deliberate-delay use. After the existing enactment ends, a one-day deferred
  native event attempts genuine enactment; the monthly review is a fallback.
  Legality is checked again. Failure leaves a notified, blocked response case.
- **Optional prioritize:** the only imperial law reform `cancel_enactment` path. Explicitly abandons
  the current enactment and its progress, then rechecks and starts the requested
  law if legal. Native cancellation restrictions apply. Failure after cancellation
  remains blocked; the tooltip warns about lost progress.

Successful adoption, including independent adoption of the requested law, gives
+3 Loyalty and -2 Autonomy exactly once. provincial accounts helpers clamp the values. Corruption
affects AI willingness but is not modified or replaced by imperial law reform.

Qing's **Imperial Reform Docket** has real actions for unsettled petitions/refusals:
grant a 24-review exemption (+5 provincial Autonomy), offer a renewed gradual
reform invitation, or maintain the decree/censure a refusal. Exemption and offer
each require 25 available Authority and occupy 25 Authority for six months,
blocking another paid concession until the workload ends. An invitation still
requires provincial consent. Maintaining a petition reopens a 12-review response
window; censuring refusal costs a further 3 Loyalty and 10 relations once.
No court choice forces adoption, annexation, deposition or war.

Notification event defaults merely acknowledge the notice. **A human must click
Accept, but Enact Later to authorize future enactment**; neither ignoring an event
nor its default acknowledgement grants consent. This is the safe interpretation
of default deferral. AI strongly favors that queue while busy (weight 1000), and
never automatically prioritizes/cancels (weight 0).

### AI, lifecycle and interface

AI weights use Loyalty, Autonomy, Corruption, government interest-group law stance,
relations, Bureaucracy deficit, war and existing Mandate Centralisation. Normal
enactment still needs the same legal conditions as a human's. AI court decisions
use the same guarded helpers and costs: loyal autonomous/blocked governors favor
exemption, otherwise an available law favors negotiation, otherwise maintain.
No new imperial authority variable was introduced.

Pending records store numeric IDs, never delayed temporary law scopes. A law
instance is rebound only for immediate use. State includes one accepted active
reform and at most one later, **unaccepted** cross-group decree. A later decree
waits behind an accepted queued/enacting reform, is displayed in both interfaces,
and requires a fresh response after dispatch. Newer cross-group demands replace
that bounded backlog. Same-group contradictions supersede old tracking safely
without cancelling an actual enactment. The court's current law is rechecked.

Per-law 365-day repeat guards and active-ID checks prevent duplicate requests,
deadline resets and reward farming. Petition, delay, refusal and court-answer flags
limit repeat actions. Support is removed on enactment end/change, success,
supersession or invalidity, and expires after at most 12 monthly reviews.
Independence, incompatible government, invalid Qing court/fragmentation or loss
of administrative eligibility clears active state without cancelling enactment.
Annexed subjects disappear from the live court list; state is nontransferable.

Only countries with active directives run the added monthly helper. Response,
petition and exemption durations count monthly reviews (12/24), explicitly labelled
as such; they are not exact anniversary dates. Unanswered/expired requests become
Response Required; expired refusal remains refused. No timeout silently adopts
a law. Completed/withdrawn records remain visible for court reference.

Province: Governor's Accounts group -> **Imperial Reform Directive**. Court:
Governance of the Empire group -> **Imperial Reform Docket**, using the repaired
native `AccessPlayer.GetSubjects` list and collapsible country records. The widgets
show actual requested law/category, current provincial law, status, remaining
reviews, support and later decree. Court buttons execute real scripted GUIs.
The existing court register ledger row tooltip also includes reform status; its layout and
portrait bindings are unchanged. All new English is in `chi_adm_l_english.yml`.

### Exact files

Created:

- `common/script_values/chi_adm_imperial_law.txt`
- `common/scripted_triggers/chi_adm_imperial_law.txt`
- `common/scripted_triggers/zz_chi_adm_imperial_law_native_rights.txt`
- `common/static_modifiers/chi_adm_imperial_law.txt`
- `common/scripted_effects/chi_adm_imperial_law.txt`
- `common/on_actions/chi_adm_imperial_law.txt`
- `common/scripted_buttons/chi_adm_imperial_law.txt`
- `common/scripted_guis/chi_adm_imperial_law.txt`
- `common/journal_entries/chi_adm_imperial_law.txt`
- `common/customizable_localization/chi_adm_imperial_law.txt`
- `events/chi_adm_imperial_law.txt`
- `gui/journal_entry_widgets/chi_adm_imperial_law.gui`
- `tools/chi_adm_imperial_law_catalog.json`
- `tools/chi_adm_imperial_law_baseline.json`
- `tools/validate_chi_adm_imperial_law.py`

Modified:

- `common/on_actions/tyrone_qing_administrations.txt` — only the civil law callback.
- `events/law_imposition_events.txt` — only the two Qing redirection guards.
- `localization/english/chi_adm_l_english.yml` — imperial law reform strings and court register row status text.
- `tools/validate_chi_adm.py` — permits the imperial law reform localization prefix.
- `tools/chi_adm_baseline.json` — rebases only the authorized callback file hash.
- `docs/chi_adm_progress.md` — this report.

The imperial law reform baseline separately proves the original on-action AST outside the replaced
callback is unchanged, and removing the event guards recovers its original hash.
Protected setup, subject/pact/army/integration, government and GUI hashes remain
unchanged. The baseline change does not waive these preservation checks.

### Validation and outstanding runtime acceptance

All four commands pass:

```text
python tools/validate_chi_adm.py
python -B tools/validate_chi_adm_court_register.py
python -B tools/validate_chi_adm_government_titles.py
python -B tools/validate_chi_adm_imperial_law.py
```

imperial law reform checks parse real script effects/triggers and run a bounded interpreter against
them: four dispatch IDs, native conversion, unaccepted timeout, busy queue,
snapshot restoration, legal failure, explicit prioritization, petition/offer/
exemption/censure, once-only refusal/delay/rewards, contradictory supersession,
cross-group backlog, support expiry and invalidation. Static checks cover the
whitelist, 11 civil/4 frontier split, original-content preservation, localization,
GUI models and the exclusive cancellation/direct-activation paths. Mocked native
legality and snapshot restoration **do not prove engine legality or save/load**.

The user will test in Victoria 3; the game was not launched. Still required:

1. New and existing saves: activate each supported Qing law, verify the right
   law/group/current-law names and no provincial change before acceptance.
2. Province and court JE activation, native grouping, expansion, collapse,
   scrolling/1080p clipping, tooltips, cost indicators and all three court actions.
   Confirm unchanged provincial accounts bars, court register ledger/desk, portraits and government titles.
3. Native policing interaction: verify subject rights, callback ordering and event
   guards, exactly one directive and **no** competing Foreign Legal Imposition JE.
   Regression-test the normal interaction for an unrelated subject.
4. Immediate legal/illegal choices; native gradual start, +5-point bonus and removal
   on completion, failure, cancellation, unrelated law change and 12-review expiry.
5. Busy province: accept queue, preserve current enactment and stats, save/reload,
   finish the old reform, then confirm only the accepted request starts. Recheck
   blocked legality, explicit prioritize and refusal preserving the old enactment.
6. Petition/offer/exemption/refusal/censure costs and notifications, expiry without
   forced law, repeat guards, supersession, backlog and independent adoption.
7. All 11 civil tags including SHN; no normal directives to the four frontier tags
   or Tibet/Korea/Lanfang. Test independence, annexation, government change,
   fragmentation and invalid Qing cleanup without unintended enactment cancellation.
8. AI governor/court behavior and a two-human Qing/province session, including
   queued consent across save/load. Check error.log for GUI, scope, effect or trigger
   errors; source/model tests cannot establish native event ordering or networking.

Next prompt: **"Test/repair imperial law reform only using these runtime results and error.log.
Preserve provincial accounts/court register/office titles; do not begin memorials and audits or expand the law whitelist."** No full
reference document is needed for the present slice; remaining uncertainty is engine
runtime behavior. Changelog: replaced forced civil law propagation with bounded
voluntary reform directives, native interaction adaptation, accepted queues,
provincial/court controls, localized widgets and focused validation.

## Current repair: competing generic governments (saved-game diagnosis)

User supplied a screenshot of Shandong as Absolute Monarchy with King Li Kong,
then made `great qing_1836_01_10.v3` available locally. The save was READ ONLY and
was not converted or edited. This replaces the earlier speculative explanation
that journal initialization was the reason subject governments failed.

### Confirmed runtime evidence

- CHI (saved country 157) uses `chi_adm_government_titles_gov_celestial_empire` as intended.
- All 15 administrative subjects have active monarchy, the correct Qing
  administrative pact with CHI, and active provincial accounts accounts.
- SHA (880) stores `gov_absolute_kingdom`, despite its initialized accounts and
  `qing_civil_administration` pact. AHU (872) stores `gov_absolute_principality`;
  MGL (882) also stores `gov_absolute_kingdom`.
- The full 15-row relevant-state extract is retained as a lightweight regression
  fixture, `tools/chi_adm_government_titles_runtime_fixture.json`. The actual save is untouched.
- Previous tests proved only that custom candidates could qualify in a model.
  They did not prevent the existing generic candidates from qualifying as well.
  Altering the journal predicate therefore did not resolve the competing match.
  The saved government field establishes the selected type, not whether the
  engine retained a cached candidate versus selecting it again.

### Correction

Added `chi_adm_government_titles_office_government_available`, exactly the union of the six
subject-office eligibility blocks, with no startup variables or periodic effects.
Seven generic native government definitions now add only:

`NOT = { chi_adm_government_titles_office_government_available = yes }`

The seven are absolute/feudal/ordinary/constitutional kingdom and
absolute/ordinary/constitutional principality. These cover every generic type
observed for the 15 subjects in the supplied save, as well as their normal
franchise/serfdom variants. The dedicated Celestial Empire and six office definitions
retain their laws, relationship checks, titles and transfer category.

The fallback definitions use supported `REPLACE:` syntax, already used by this
mod's government types. Each copies the installed 1.15.1 original exactly except
for this one extra possible-condition. Tests remove that condition and compare the
entire parsed definition to native data, including every title, heir and succession
callback. Outside eligible Qing offices, the condition is false and native behavior
is unchanged. Independence or incompatible laws restore the normal generic choices.
No native names have been relocalized, and no global law/ruler-refresh workaround
or save editing is used.

### Files

Added:

- `common/scripted_triggers/chi_adm_government_titles_eligibility.txt`
- `common/government_types/zz_chi_adm_government_titles_fallbacks.txt`
- `tools/chi_adm_government_titles_runtime_fixture.json`

Modified:

- `common/government_types/00_00_chi_adm_government_types.txt` (corrected header comment only)
- `tools/validate_chi_adm_government_titles.py`
- `docs/chi_adm_progress.md`

No localization, GUI, law, pact, succession effect, country setup or saved-game
file was changed by this correction. The Shanxi migration remains unchanged.

### Validation and next runtime check

- `python -B tools/validate_chi_adm_government_titles.py` - PASS; now covers actual competing
  generic government definitions, the 15-subject save fixture, exact helper/custom
  predicate correspondence and unchanged native behavior outside Qing offices.
- `python -B tools/validate_chi_adm_court_register.py` - PASS, including provincial accounts regression and all
  original action/GUI/mechanical checks.

Restart Victoria 3 and load the supplied post-migration save; a new campaign is
not required for this repair. Advance a day to permit normal government refresh.
Check SHA = Imperial Governorate/Governor, AHU = Imperial Viceroyalty/Viceroy,
then the four frontier offices; CHI must remain Celestial Empire/Son of Heaven.
If a cached native government does not refresh, report it rather than changing laws
or rulers as a workaround. No fresh in-engine verification is claimed by Codex.

STOP after this government-display repair. No imperial law reform work.

## Previous repair: subject-government eligibility after office titles runtime report

User runtime result: CHI's Celestial Empire and Son of Heaven display correctly;
the six government definitions covering the 15 subjects do not. The native display
path and localization therefore work for CHI; the subject predicates need isolation.

Changed only:

1. `common/government_types/00_00_chi_adm_government_types.txt`
2. `tools/validate_chi_adm_government_titles.py`
3. `docs/chi_adm_progress.md`

The subject definitions no longer call the journal-oriented `chi_adm_eligible`.
That helper includes the Qing setup marker, fragmentation flag and further nested
administration triggers. Native government selection should follow the actual
political relationship without depending on journal initialization state. The
replacement follows installed Congress Poland government definitions: correct tag,
subject's monarchy law, existing Qing overlord with monarchy, `is_subject_of = c:CHI`,
and the exact existing administrative subject type. No-regency checks remain.
The working CHI definition, file precedence, titles, transfer category, laws,
characters, subject pacts, SHN migration and all GUI definitions are unchanged.

This removes a timing/state dependency and brings qualification into the native
subject-government pattern. It is a targeted correction, NOT a reproduced engine
proof of the original failure's precise cause. No government-selection refresh
effect, ruler replacement or temporary law change is used to force a label.

Office titles still cease to apply on independence, wrong subject type, incompatible
subject laws or a non-monarchical Qing court. The journal's fragmentation flag alone
now does not remove a native office title while the actual Qing administrative pact
remains in force. Changing the pact to a warlord/other subject type removes it.

Validation: `python -B tools/validate_chi_adm_government_titles.py` and
`python -B tools/validate_chi_adm_court_register.py` PASS. court register's command also runs provincial accounts regression.
Added checks require six explicit native Qing relationship predicates, prohibit
journal/setup-variable predicates in the government file, and test every office
without provincial accounts variable initialization. All original actions/GUI/economic checks pass.

User test: fully restart, then check native government/ruler displays for a civil
viceroyalty, SHN/SHA/QHN and each frontier office in a new SHN-based campaign (or a
reloaded post-migration save). Confirm Celestial Empire still works. Runtime
selection/refresh remains unverified by this run; if any subject still fails, the
exact native government type/title currently displayed is needed to distinguish
remaining law/transfer/selection causes. Do not alter laws to force a test.

STOP: office titles repair only, no imperial law reform.

## Previous delivery: office titles native governments and Shanxi migration

Scope: office titles only. The user reports court register and its repairs completed and tested in game;
that supersedes the older pending-court register notes below. This run did not launch the game
or claim new runtime verification. imperial law reform-regional works remain unstarted. This folder has no Git
repository; no commit or branch verification is claimed.

### Native government flavor

New native definitions are in
`common/government_types/00_00_chi_adm_government_types.txt`:

| Countries | Native government | Male and female ruler title |
|---|---|---|
| CHI | Celestial Empire | Son of Heaven |
| ZHI, AHU, HNA, YUE, FRS, XIB, YUN, SIH | Imperial Viceroyalty | Viceroy |
| SHN, SHA, QHN | Imperial Governorate | Governor |
| MGL | Uliastai Generalship | General of Uliastai |
| QIM | Banner Administration | Imperial Commissioner |
| XIN | Ili Generalship | General of Ili |
| QXN | Xining Imperial Commission | Imperial Minister |

These are genuine `government_types` entries and native ruler-title localization,
not journal-only labels. Government descriptions explain delegated civil/frontier
appointments and distinguish them from the Son of Heaven's supreme sovereignty.
Great Qing's existing country name is not overridden.

Eligibility: all require a monarchy law (including supported variants) and no
native regency. CHI must be independent. Subjects must have the correct exact tag
and matching existing subject type and satisfy provincial accounts `chi_adm_eligible`: active direct
Qing administration, valid monarchical court, and no fragmentation. Independence,
non-administrative subordination, incompatible laws, a republic at court, or a
regency invalidates the relevant special display; normal native governments then
remain available. Tibet and unrelated countries cannot qualify. A still-monarchical,
independent CHI may retain Celestial Empire during fragmentation; former provincial
administrations lose their delegated office display.

Installed precedents inspected: `01_monarchies.txt` (country-specific offices,
Tsardom/Kaiser titles before generic monarchies), `01_regencies.txt`,
`01_colonial_administrations.txt`, `04_theocracies.txt` (Dalai Lama), and native
`government_l_english.yml`. Native definitions do not use a government weight or
priority field. The new early filename places the narrow conditional definitions
before generic matches, following the specialized-first arrangement of native data.
Actual engine precedence and government refresh still need the user's new-session
check; static tests do not establish those runtime details.

**Succession is deliberately preserved:** all these countries begin with the
monarchy/hereditary transfer category. New flavor definitions keep that category
and contain NO government-change effects, ruler/heir creation or succession hooks.
Office descriptions do not claim a separate hereditary sovereign dynasty. The
native `$TRANSFER_OF_POWER_NAME_DESC$` is retained in each description so the game
truthfully reports its existing transfer-of-power rules. This feature does not
implement historical appointments; doing so would change the forbidden mechanics.
Native heirs remain mechanical heirs; provincial heir-title fields are blank as in
native principality displays. CHI retains native Prince/Princess heir labels.

The existing custom dossier office labels are untouched, as requested; this pass
changes native country-government/ruler displays, not the completed GUI system.

### QSX to vanilla SHN migration

- Inspected installed `00_countries.txt`: vanilla SHN is unrecognized, Han,
  capital STATE_SHANXI, with a kingdom tier. No dedicated SHN country-history file
  or existing SHN history assignment was found. Its vanilla identity is reused;
  no replacement/duplicate SHN country definition or custom history is added.
- Removed only the obsolete QSX country-definition block and QSX-specific coat of
  arms. SHN retains its vanilla definition and arms, including its native kingdom
  tier; the conditional Imperial Governorate determines its office/ruler display.
- Global setup now creates SHN from exactly the previous Shanxi seed, transfers
  exactly STATE_SHANXI, and retains the same copied laws, technologies, Confucian
  religion, Han culture, ideologies, Qing civil-administration pact, -100 Liberty
  Desire adjustment, +80 relations and 70/25/25 account initialization.
- Integration/reintegration button IDs, subject tests, warlord JE references, core
  eligibility and validator lists now use SHN. The count remains exactly 15 with
  eight viceroyalties, three governorates and four frontier administrations.
  The ledger and portraits already filter live subjects through core eligibility;
  their GUI files need no changes.
- Added an `INJECT:SHN` conditional dynamic name, Shanxi Governorate, only while
  serving as a Qing administration. Its adjective reuses SHN_ADJ. Vanilla base
  SHN/Shanxi names and the vanilla Shanxi Clique dynamic name are not overwritten.
- Vanilla warlord content references SHN; this branch already replaces the vanilla
  warlord event file. No events were changed in this feature. Existing branch
  self-strengthening already recognizes SHN and remains intact.
- Removed obsolete QSX English labels from the old administration localization.
  New conditional-name and renamed button labels live only in chi_adm_l_english.yml.
  No QSX references remain in active common/events/gui/localization data.

**Save compatibility:** use a NEW CAMPAIGN for this tag migration. Existing QSX saves
are not converted: their setup marker prevents fresh country creation, and their
old saved country/reference IDs do not become SHN merely because scripts were
renamed. Removed QSX definitions and eligibility mean those saves are unsupported
with this version. No global save conversion or risky on-load territory transfer
was added. Keep the pre-office titles mod version with old saves. Modified-file backups are
recorded in `tools/chi_adm_government_titles_migration_baseline.json` (temporary backup directory).

### Exact files

Created:

1. `common/government_types/00_00_chi_adm_government_types.txt`
2. `tools/chi_adm_government_titles_migration_baseline.json`
3. `tools/validate_chi_adm_government_titles.py`

Modified:

1. `common/country_definitions/tyrone_qing_administrations.txt` (remove QSX only)
2. `common/coat_of_arms/coat_of_arms/tyrone_qing_administrations.txt` (remove QSX only)
3. `common/history/global/zzzz_qing_administrations.txt` (exact tag rename only)
4. `common/scripted_triggers/tyrone_qing_administrations.txt` (exact tag rename only)
5. `common/scripted_buttons/tyrone_qing_administrations.txt` (exact tag/ID rename only)
6. `common/journal_entries/tyrone_qing_administrations.txt` (renamed button reference)
7. `common/journal_entries/tyrone_chinese_warlords.txt` (renamed button reference)
8. `common/dynamic_country_names/tyrone_qing_administrations.txt` (conditional SHN name)
9. `localization/english/tyrone_qing_administrations_l_english.yml` (obsolete keys removed)
10. `localization/english/chi_adm_l_english.yml` (all new English)
11. `tools/validate_chi_adm.py` (SHN list; office titles localization recognition)
12. `tools/validate_chi_adm_court_register.py` (SHN governorate list)
13. `tools/chi_adm_baseline.json` (four explicitly authorized tag-only hash rebases)
14. `docs/chi_adm_progress.md`

### Validation and baseline handling

Commands, all PASS:

- `python tools/validate_chi_adm.py`
- `python -B tools/validate_chi_adm_court_register.py`
- `python -B tools/validate_chi_adm_government_titles.py`

office titles tests cover all sixteen countries across seven native governments, identical
male/female requested titles, subject/law/regency/court fallback conditions, 15
unique administration pacts, SHN territory/identity, no duplicate SHN definition,
absence of active QSX data and all new English in the single designated file.
Four protected files intentionally changed only by QSX-to-SHN substitution; tests
reverse that substitution and recover their original hashes. Other protected
mechanics/GUI baselines still pass, including unchanged costs, cooldowns, 30% pacts,
law/army sharing, Mandate and original integration mechanics. provincial accounts's bounded
15 x 240-month model and the court register GUI structural regression still pass.

### Concise user test checklist

1. Restart and start a NEW 1836 campaign. Confirm 15 administrations, SHN in Shanxi,
   no duplicate Shanxi/QSX, and unchanged starting laws, market, relations and pacts.
2. Check native country government screens for all seven names and title categories;
   check Qing male/female rulers both say exactly Son of Heaven. Inspect tooltip
   transfer-of-power text, title refresh and regency fallback where practical.
3. Open the tested court ledger/provincial GUI: SHN must have the former Shanxi
   accounts/actions and current ruler; verify existing integration eligibility.
4. In a disposable save test independence, republic and inappropriate subject-type
   transitions. Special provincial titles must fall back normally. Confirm Tibet's
   Religious Kingdom/Dalai Lama and unrelated countries' displays are unchanged.
5. Check fresh error.log for the new government IDs or SHN errors. Report native
   selection/refresh problems without altering succession to force a display.

STOP after office titles. No in-game testing or new appointment/negotiation mechanics are
claimed or implemented. imperial law reform requires a separate instruction.

## Previous pass: court register runtime/crash repair

Scope: repair the user's confirmed court register GUI failures only. imperial law reform-regional works remain untouched.
The user supplied screenshots and runtime logs and reported a crash when opening
Imperial Administrative Ledger. No game launch or computer control was attempted;
the user is responsible for fresh runtime verification.

### Evidence and root causes

| Pre-repair source | Evidence / cause | Correction | Fresh session? |
|---|---|---|---|
| `gui/journal_entry_widgets/chi_adm_court_register_subentries.gui:7` and `:21` | Supplied log rejects direct datamodel properties on the named court/province widget roots. Factory errors at `:1` and `:15` are consequences of those rejected constructions. The previous implementation skipped the native nested group-model layer. | Named roots are static wrappers. Nested model/item layers now use the installed Great Game / Imperialism of Promise accessors: `AccessPlayer.GetGroupsForActiveJournalEntries`, then `JournalEntryGroup.GetActiveJournalEntryTypes(GetPlayer.Self)`. | Yes |
| Same subentries file, native card datacontext | The old expression derived a JournalEntry from `JournalEntry.GetCountry` while establishing another JournalEntry context. It departed from the working native accessor and introduced avoidable context ambiguity. This was not independently identified by the log as the crash cause. | Native cards now use `AccessPlayer.GetJournalEntry(JournalEntryType.Self)` and retain native current-panel self-exclusion. | Yes |
| `gui/journal_entry_widgets/chi_adm_court_register_ledger.gui:217` (factory context `:213`) | The current crash-session error.log rejects `[JournalEntry.GetCountry.GetSubjects]` as that flowcontainer's datamodel. This error is immediately before the process crash. The previous validator checked the string's presence, not whether it followed the native subject-accessor contract. | Both register and selected-dossier subject models now use the installed diplomatic-overview accessor `[AccessPlayer.GetSubjects]`, with the same provincial accounts read-only eligibility filter on every item. | Yes |
| Ledger file shared `chi_adm_court_register_character_card`, old portrait block near line 11 | Screenshot shows live ruler text, IG and traits but no portrait. Character scope therefore reaches the card. The portrait's inner image was sized, but its outer widget was unsized and anchored/clipped by the native base. | Use native `character_portrait_base_torso`, with explicit outer `size = { 160 188 }` and matching inner `portrait_size`. Installed native torso template supplies animated texture, camera and mask. Shared court/provincial use means one correction covers both. | Yes |
| `common/journal_entries/chi_adm_governance.txt`, outcome effect | Screenshot exposes the cleanup helper's modifier-removal expansion, misleadingly showing a negative Bureaucracy line as a completion reward. | Unchanged cleanup executes in `hidden_effect`, with one localized explanation. Terminal headers describe closure of the register rather than an objective/reward. | Yes |

The newest crash folder inspected was
`crashes/victoria3_01261015_010452/exception.txt`: Victoria 3 1.15.1,
2026-11-15 01:04:53, null-address C0000005 access violation. Its stack has no function
symbols. This confirms a real crash, but cannot prove which C++ path caused it.
The rejected ledger binding immediately before it is repaired; crash freedom is
NOT claimed until the user opens the corrected interface in a fresh session.

The earlier log's contextless `add_journal_entry` errors identify
`events/RB_bic_content.txt:64` and `events/tyrone_netherlands.txt:103`, not chi_adm.
Older Mandate/India/Germany/Russia warnings and debug-mode pink JE identifiers
are outside this repair and have not been changed.

### Functionality retained

- Native grouped, expandable court ledger and provincial Memorial Desk cards remain.
  Only the principal JEs contain a subentry-list widget; ledger/desk children do not
  contain the list again, preventing recursive card nesting.
- Both court models enumerate the current local Qing player's native subject model.
  Qing court entries are country-scoped and restricted to CHI. Provincial native
  cards use the player's own JE, as in the installed game's implementation. This
  is UI context only; nothing writes a simulation country or character selection.
- Each subject row/dossier still reads that item's `Country` values and current
  ruler. The existing filter includes exactly the 15 provincial accounts administrative subjects
  and excludes Tibet/Korea/Lanfang/unrelated/departed subjects. Scroll/collapse,
  warnings, local selection, three progress bars and dynamic traits are retained.
- The provincial accounts provincial dossier widget is unchanged. The three action definitions,
  requirements, exact effects, economic costs and cooldowns remain unchanged.
- Original subject setup/territory, 30% pacts, Mandate, law propagation, army sharing
  and integration files remain unchanged. No new polling, synchronization or imperial law reform
  feature was introduced.
- The portrait hint was shortened to fit its existing column. The existing debug
  header is native debug-mode output and was not hidden through a global GUI edit.

### Exact modified files (no new feature files)

1. `gui/journal_entry_widgets/chi_adm_court_register_subentries.gui`
2. `gui/journal_entry_widgets/chi_adm_court_register_ledger.gui`
3. `common/journal_entries/chi_adm_governance.txt`
4. `common/journal_entries/chi_adm_court_register_governance.txt`
5. `localization/english/chi_adm_l_english.yml`
6. `tools/validate_chi_adm_court_register.py`
7. `docs/chi_adm_progress.md`

### Automated validation

- `python tools/validate_chi_adm.py` - PASS.
- `python -B tools/validate_chi_adm_court_register.py` - PASS.

The court register validator now scans block/attribute structure, rejects named root datamodels,
rejects the old read-only subject-model expression, detects orphaned `item` blocks,
and checks native JournalEntry card accessors. Negative fixtures verify that the
old bad patterns actually FAIL validation. It also checks nonzero outer portrait
geometry and the installed native torso camera/texture precedent; native Great
Game nested GUI is used as a positive structural reference.

Original 15-subject/type/exclusion checks, provincial accounts 240-month bounded effect model,
action/cooldown semantics, unchanged-file hashes, direct indicator bindings,
localization and asset checks continue to pass. Cleanup is verified to remain the
same helper inside its new presentation wrapper. This is focused source validation,
not a full GUI parser or evidence of successful engine rendering.

### Prioritized user runtime checklist

1. **Restart Victoria 3 fully**, then load the existing save. No new campaign is
   required by these presentation changes. Do not rely solely on hot reload after
   failed widget construction.
2. As Qing, open Governance of the Empire and expand Imperial Administrative Ledger;
   also open the ledger directly. Both must open without crashing. Verify 15 rows,
   scrolling, types, warnings, values, collapse controls and row selection.
3. Select several different administrations. Confirm correct current ruler portrait,
   name, IG/traits and values; check updated portrait after succession if practical.
4. As a province, open Governor's Accounts: verify the actual portrait is now visible,
   provincial accounts bars remain correct, and its Memorial Desk opens from the native subentry card
   with the same three actions/cooldowns. After console tag changes, reopen the JE
   for the newly controlled country, as native player-context lists expect.
5. Review register-closure text: no raw corruption modifier-removal reward expansion.
   Check fresh error.log for `chi_adm` errors, especially old datamodel lines. If a
   crash remains, provide the newest exception.txt and last relevant error.log lines.

**Status:** confirmed failing presentation paths patched; automated checks pass.
The ledger MUST open and be usable in the user's new runtime test before court register can be
called runtime-repaired. Portrait framing/rendering also remains to be confirmed.
STOP here; do not start imperial law reform or broaden repairs to unrelated systems.

## Previous delivery: court register court ledger and provincial memorial desk

court register is implemented in the opened folder, following the user's explicit court register pasted
request. This section supersedes previous provincial accounts-only stop/next-action notes as the
current delivery status. **imperial law reform-regional works are not implemented or started.** No Git repository
exists in this folder; no branch/commit verification or commit is claimed.

### Implemented architecture

- Qing: **Governance of the Empire** (`chi_adm_court_register_court`), with its native expandable
  **Imperial Administrative Ledger** subentry (`chi_adm_court_register_ledger`). A dedicated
  themed country-context journal group supplies the active-entry model.
- Provinces: existing **The Governor's Accounts** remains the principal JE, now in
  its own themed provincial group. Its provincial accounts dossier widget is byte-for-byte preserved.
  A shared native ruler card is added alongside it, plus the expandable **Provincial
  Memorial Desk** (`chi_adm_court_register_memorial_desk`).
- Exactly three new JE TYPES, not fifteen region-specific JEs. Country-context
  `possible` conditions activate the UI through the native journal system; no new
  start/monthly effects or global pollers are added. Parent/subentry conditions
  guard the current court/subject and the relevant principal JE.
- Native `journal_entry` cards use grouped `GetActiveJournalEntryTypes` and the
  current JE owner's `GetJournalEntry`, with the same native self-exclusion pattern
  used by Imperialism of Promise and existing Qing widgets. These cards provide
  descriptions, conditions and native expansion/action sections.
- The original three provincial actions are displayed ON the Memorial Desk card,
  rather than duplicated on the parent. Their definitions, effects, eligibility,
  costs and cooldowns are unchanged. The original instant-integration JE/buttons
  remain separately accessible in their existing Mandate group and are untouched.

### Imperial register and selected dossier

- Live `JournalEntry.GetCountry.GetSubjects` provides the country model. A read-only
  scripted GUI reuses provincial accounts `chi_adm_target_valid`: exact original tags, initialized
  accounts, current direct Qing subordination and valid imperial court. At start
  this yields the eight viceroyalties, three governors and four frontier offices.
  Tibet/Korea/Lanfang and unrelated subjects are excluded. Annexed or departed
  administrations disappear; nonexistent countries are not recreated as rows.
- Compact scrollable rows show dynamic country name, native subject type, current
  ruler name, three numeric mini-bars and a current warning/status. Hover text gives
  all values/tiers and explains existing consequences. No extra modifiers were added.
- Select a row to view its full dossier without opening a country screen. Selection
  is a client-local `GetVariableSystem` string, not a simulation variable or script
  effect; it cannot change another human player's country. Collapsible register and
  dossier sections keep the interface organized. The full account bars read current
  provincial accounts variables directly, with no synchronization state or timer.
- Selection follows the current unique administration name. If that name changes
  or the subject leaves, select its current row again. The always-visible hint
  explains selection; stale selections show no incorrect dossier or ruler.

### Dynamic ruler and provincial desk

- One reusable native `character_portrait_base` definition reads `Country.GetRuler`
  and `Character.GetAnimatedPortrait`; only the selected eligible subject's dossier
  is visible in the court list. Fifteen full portraits are not rendered together.
- The same card is used for the provincial player's own ruler. Full name, current
  interest group and `Character.AccessTraits` are dynamic, with native trait icons
  and `FancyTooltip_CharacterTrait`. Invalid rulers and absent affiliations have
  clean fallbacks. No historical names or static portrait art is assigned.
- Office titles distinguish viceroy/provincial governor and four frontier offices.
  These are mod UI titles, not changes to ruler appointment or character roles.
- Provincial Memorial Desk shows the actual overlord, current relations and all
  three existing staff commitments, then the existing actionable native buttons.
  It has no fake pending edicts, petitions or unimplemented communication controls.
- Loyalty and Autonomy tooltips explicitly avoid claiming unimplemented bonuses.
  Corruption displays the existing Bureaucracy consequence; all remittances remain
  the original 30% pact. Both provincial accounts and court tooltips show current values and tiers.

### Exact changed files

Created:

1. `common/scripted_guis/chi_adm_court_register_gui.txt`
2. `common/journal_entry_groups/chi_adm_court_register_groups.txt`
3. `common/journal_entries/chi_adm_court_register_governance.txt`
4. `common/customizable_localization/chi_adm_court_register_gui.txt`
5. `gui/journal_entry_widgets/chi_adm_court_register_ledger.gui`
6. `gui/journal_entry_widgets/chi_adm_court_register_memorial_desk.gui`
7. `gui/journal_entry_widgets/chi_adm_court_register_subentries.gui`
8. `tools/chi_adm_court_register_baseline.json`
9. `tools/validate_chi_adm_court_register.py`

Modified:

1. `common/journal_entries/chi_adm_governance.txt` (group, native action placement,
   ruler and subentry widget slots; original cleanup/outcome unchanged)
2. `localization/english/chi_adm_l_english.yml` (all court register English; extended provincial accounts tooltips)
3. `tools/validate_chi_adm.py` (recognizes separately validated court register localization)
4. `docs/chi_adm_progress.md`

### Focused validation results

Commands:

- `python tools/validate_chi_adm.py` - PASS core static/model regression.
- `python -B tools/validate_chi_adm_court_register.py` - PASS core regression plus court register checks.

Checks cover all 15 original tags and their 8/3/4 pact types, excluded countries,
leaving-subject filtering, country-scoped GUI models and direct variable bindings,
local-only selection, grouped JE references, native ruler portrait/trait bindings,
localization uniqueness/references/assets, GUI structural checks, and preserved provincial accounts
widget/actions/effects/hooks/constants. The original 15 x 240 monthly bounded
model still passes. Existing setup/30% pacts/laws/army sharing/Mandate/integration
remain protected. No new simulation effects, dates or polling are introduced.

These checks verify source structure and regression properties. They are NOT a
Jomini parser, in-game simulation, screenshot inspection or multiplayer test.

### Remaining runtime tests / limitations

1. Start a new campaign and load an existing provincial accounts save. Confirm automatic activation
   of Governance, its ledger subentry, and each province's Memorial Desk; ensure no
   duplicate cards/JE recursion after native expansion or save/reload.
2. At 1920x1080 inspect the native journal scroll/expansion behavior, row scrollbars,
   portrait frame, trait-icon wrapping, gold headings, long names and tier text.
   The register is 300 pixels tall; detail sections are collapsible, and the native
   journal scrolls the combined content. Actual clipping has not been visually tested.
3. Verify 15 starting rows with 8/3/4 types. Click each, checking country, ruler,
   values and tiers against that subject's own Governor's Accounts. Verify current
   rulers update after succession and missing ruler/IG fallbacks display correctly.
4. Integrate or remove a subject in a disposable save: its row/selected dossier must
   disappear; the original integration behavior and cooldown must remain unchanged.
5. As a provincial player, open the Memorial Desk and use each original action.
   Check unchanged costs/cooldowns, live commitments and actual court relations.
   The prior inspection native remaining-duration issue still needs its provincial accounts live test;
   this UI pass does not alter that timer or globally override its formatter.
6. With two humans (Qing plus province), verify that local selection/collapse state
   never changes simulation state and each sees the correct owner's data. No MP
   validation is claimed. Native condition headings remain engine-controlled.
7. Inspect fresh error.log for new JE activation, widget scope or portrait errors.

No post-court register game launch, in-engine screenshot or multiplayer session was performed.
The full reference was not needed. **STOP after court register.** Resolve any failed runtime
checks before starting imperial law reform; do not start later political systems automatically.

## Previous delivery: provincial accounts GUI refinement

This section supersedes the original plain-text fallback UI notes below. court register and
later systems remain unstarted. The full reference was not required.

### What changed

- A 488x406 native dossier replaces the three plain lines: dark frame, Qing icon,
  gold heading, dividers and three horizontal 0-100 bars. Each shows a live value,
  live five-tier label and concise thematic tooltip. Province names elide if long.
  Loyalty uses gold fill, Autonomy the native default, Corruption warning fill.
- Bars read `FixedPointToFloat(JournalEntry.GetCountry.MakeScope.Var(...).GetValue)`
  directly, following `tyr_kk_widgets.gui`. No synchronization variables, scripted
  simulation bars or extra monthly work. All values use the JE owner's country.
- Country customizable-localization selects tiers from original shared thresholds.
- Each existing button condition is wrapped in a localized `custom_tooltip`, keeping
  native eligibility checkmarks without expanding variable/subject helper trees.
  Explicit localized outcomes replace generated effect dumps; original mechanics
  execute inside `hidden_effect`. Requirements and costs remain visible.
- The JE now has a concise activation description, a localized termination condition
  and required outcome color. These address provincial accounts warnings in existing `error.1.log`.
- Added UTF-8 BOM to the provincial accounts GLOBAL hook after its observed lexer warning. Script
  content and original administration setup are unchanged.
- All new English strings remain in `localization/english/chi_adm_l_english.yml`.

### Bureaucracy and duration investigation

`relative_bureaucracy >= 0.05` remains unchanged. Installed trigger-localization and
Morocco-button scripts verify this supported ratio trigger. A read-only display
value multiplies the ratio by 100: 0.05 appears as 5%, in both the dossier and the
localized inspection requirement. No absolute Bureaucracy-point cost was substituted.

All original actions already specified `months = 24`. No one-year inspection
application was found. Exact pre/post semantic checks now protect the timer and
-3% inspection Bureaucracy effect. Condensed tooltips explicitly state **24 months**;
modifier text distinguishes original term from remaining time. Existing modifiers
are not extended/reset on loading. Native `modifiers_panel.gui` uses
`TimedModifier.GetRemainingDuration`; a rounded remaining duration could explain the
reported one-year label, but this was NOT reproduced or established in engine.
No global formatter or simulation duration was changed. This discrepancy still
needs the focused live check below, rather than guessing a new timer implementation.

### Exact file changes for this pass

Modified:

- `gui/journal_entry_widgets/chi_adm_foundation.gui`
- `common/scripted_buttons/chi_adm_core.txt` (presentation wrappers)
- `common/journal_entries/chi_adm_governance.txt` (presentation metadata)
- `common/script_values/chi_adm_core.txt` (read-only percent value appended)
- `common/history/global/zzzzz_chi_adm_init.txt` (BOM only)
- `localization/english/chi_adm_l_english.yml`
- `tools/validate_chi_adm.py`
- `docs/chi_adm_progress.md`

Added:

- `common/customizable_localization/chi_adm_core.txt`
- `tools/chi_adm_ui_baseline.json`

### Validation

`python tools/validate_chi_adm.py`: PASS static and bounded model checks.

Checks cover three direct bars and ranges, tier bindings and boundary labels,
localization/BOM/placeholder integrity, required JE metadata, ratio-to-percent
presentation, and exact original action semantics after unwrapping UI annotations.
Original tuning, effects, subject eligibility, modifiers and hooks are protected;
initialization differs only by BOM. Existing 15-subject/30%/Mandate/army/law/integration
regressions and the 15 x 240 monthly model still pass. This is not engine validation.

### Runtime checks still pending

No post-change game launch, screenshot or multiplayer test was performed. Existing
logs informed the metadata fixes; they do not verify the current version.

1. At 1920x1080, inspect civil and frontier dossiers: fills, values, tiers, fonts,
   frame and tooltips must fit without clipping. Check existing Qing widgets too.
2. Use each action and reload a save: direct bars/tiers must reflect the owner,
   update immediately and retain existing costs/cooldowns.
3. Hover JE conditions/buttons: confirm concise checkmarks and no raw variable
   trees. Shared engine headings such as Requirements/Effects may remain.
4. Verify inspection availability below, exactly at and above 5% Bureaucracy
   surplus; dossier and requirement must show the same percent value.
5. Start a FRESH inspection, note current date and expiry: confirm the intended
   24-month term, -3% Bureaucracy and lockout. Compare the native remaining-duration
   label with the explicit original term. If still unexpectedly short, record dates
   before changing mechanics. Pre-existing inspections retain their remaining time.
6. Check fresh `error.log` for `chi_adm` GUI, localization and JE-metadata errors.

STOP after this provincial accounts refinement. Do not begin court register automatically. Resolve reported live
issues first; later features require a separate follow-up instruction.

## Original provincial accounts foundation delivery

2026-11-15: provincial accounts foundation implemented in the opened China Branch folder only.
The supplied optimized brief v2 explicitly requires one feature per run; court register-regional works
have not been started. The full reference is not needed for provincial accounts.
This folder has no `.git` repository: branch/HEAD cannot be verified and no commit
was made. The user's selected folder takes precedence over the brief's GitHub path.

provincial accounts implementation and bounded local acceptance checks are complete. In-engine
display, initialization timing, save/load and multiplayer acceptance remain pending.
The local model is not a Victoria 3 simulation or proof of engine correctness.

## Implemented provincial accounts behavior

- The 15 existing administrations initialize once, after the existing global setup.
  Civil Loyalty/Autonomy/Corruption starts at 70/25/25; frontier at 65/45/30.
  Initial values, bounds, tier thresholds and action adjustments are centralized in
  `common/script_values/chi_adm_core.txt`.
- Existing `chi_qing_administration_tag` and `chi_qing_administrative_subject`
  triggers are reused. Eligibility requires direct Qing subordination, completed
  existing setup, a monarchical Qing court, and no `tyr_chi_fragmented` marker.
  Tibet, Korea, Lanfang, Qing itself and later unrelated subjects are excluded.
- A narrow later-sorting GLOBAL hook initializes new campaigns. A guarded
  `on_game_started_after_lobby` hook handles late setup/existing saves when fired;
  the country monthly pulse repairs missing initialization. No global monthly
  country loop, daily poll, narrative event or calendar-year unlock was added.
- Governor JE `chi_adm_governance`, in the existing Qing Mandate group, embeds a
  small native widget with three live numeric indicators and explanatory tooltips.
  All bindings read `JournalEntry.GetCountry`, not the viewing player's country.
  This is the explicitly permitted provincial accounts native text fallback, not a progress-bar
  synchronization system. The court register court ledger and decorative polish are deferred.
- Values are separate from Liberty Desire and clamped to 0-100. There is no passive
  monthly drift. Status checks react to changed values and court/subject validity.
  Only corruption applies a foundation economic modifier: mutually exclusive
  tiers at 0/20/40/60/80 reduce local Bureaucracy by 0/1/3/5/8 percent. Loyalty and
  Autonomy have informative ranges, with no extra military/economic bonus in provincial accounts.
- Three optional provincial actions: loyal memorial (+5 Loyalty, -25 Authority for
  24 months); accept court supervision (-5 Autonomy and -5 Loyalty, -25 Authority
  for 24 months); supervise offices (-5 Corruption, -3% Bureaucracy for 24 months,
  requires 5% surplus). Each uses its own lasting cost modifier as its cooldown;
  used actions remain visible with native unmet-condition tooltips. AI usage is
  disabled pending later AI tuning. No money is created or separately transferred.
- Reusable scoped helpers adjust each value with a parameter and immediately
  clamp/refresh status. Public target-validity and court-validity triggers exist.
- Independence, a different subject relationship, court republicanization,
  fragmentation or Qing disappearance clears the active marker and corruption
  tiers. The JE's terminal outcome also performs cleanup. Country-pulse cleanup
  takes at most a monthly tick; JE outcome cleanup may occur sooner in engine.
  Initialization marker and accounts are retained to prevent reset farming.
  Action costs expire naturally and are deliberately not refunded by independence.
  Rejoining restores status and re-adds the JE without resetting accounts.
  Annexed countries have no live country pulse or persistent active UI to service.

## Exact files added

The original foundation pass modified no existing file; see current-pass changes above.

1. `common/script_values/chi_adm_core.txt`
2. `common/scripted_triggers/chi_adm_core.txt`
3. `common/scripted_effects/chi_adm_core.txt`
4. `common/history/global/zzzzz_chi_adm_init.txt`
5. `common/on_actions/chi_adm_core.txt`
6. `common/journal_entries/chi_adm_governance.txt`
7. `common/scripted_buttons/chi_adm_core.txt`
8. `common/static_modifiers/chi_adm_core.txt`
9. `gui/journal_entry_widgets/chi_adm_foundation.gui`
10. `localization/english/chi_adm_l_english.yml` (UTF-8 BOM, all new English strings)
11. `tools/chi_adm_baseline.json`
12. `tools/validate_chi_adm.py`
13. `docs/chi_adm_progress.md`

## Validation and regression

Command: `python tools/validate_chi_adm.py`

Final result: PASS static and PASS bounded model.

- Parses the actual provincial accounts effect/trigger/value/button/JE/hook definitions with a
  deliberately limited local parser; checks unique IDs in those definition files.
- Checks localization header, BOM, duplicate keys, quotes, balanced localization
  placeholder brackets, expected key set and each live country-variable binding.
  Checks the native widget's braces and indicator/tooltip references.
- Models the actual provincial accounts effect tree for 15 administrations x 240 monthly checks,
  including repeated initialization, one status tier, no cumulative modifiers,
  stable initial values and one active JE per eligible country.
- Models clamp/tier boundaries, every action's cooldown expiry, invalid-court and
  independence cleanup, preserved accounts on rejoining, and excluded tags.
- Confirms original 15 setup pacts and four original 30% income-transfer definitions.
  SHA-256 baselines verify 11 existing Qing files are untouched: setup, subject
  definitions, pacts, triggers, law/army-sharing on_actions and effects, instant
  integration buttons and JE, Mandate/reform JE and Centralisation bar, power bloc.
- Existing country creation, territory, initial laws, flags/names, forced civil-law
  propagation, customary frontier laws, instant integration and six-month cooldown,
  army sharing, 0-10 Centralisation and Tiāncháo remain unchanged.

Syntax/binding precedents inspected locally: original Qing `GLOBAL` setup and
`on_game_started_after_lobby`/`on_monthly_pulse_country` hooks; existing `outcome`
JEs and Qing widgets; `JournalEntry.GetCountry.MakeScope.Var(...).GetValue` in
`localization/english/india_administration_l_english.yml`; Authority/Bureaucracy
requirements in existing scripted buttons; installed game static modifiers for
`country_bureaucracy_mult` and existing mod `country_authority_add` usage.

## Pending in-engine acceptance / limitations

No Victoria 3 launch, runtime log check, screenshot or multiplayer test was run.
The validator does not claim that its parser proves Paradox syntax or UI correctness.

1. Start a fresh campaign in debug mode; inspect `error.log` for `chi_adm` issues.
   Qing must retain its original territory/15 subjects, 30% pacts, Tiāncháo, existing
   army sharing, forced law propagation and original integration eligibility.
2. Play/switch to Zhili and each other civil administration: open the Qing journal
   group and Governor's Accounts; verify 70/25/25. Repeat for the four frontier
   administrations: 65/45/30. Tibet/Korea/Lanfang must not receive this JE.
3. At 1920x1080 inspect all three live values/tooltips and action buttons; confirm
   no clipping and existing Mandate/Boxer/Self-Strengthening widgets remain intact.
4. Use each optional action. Confirm the advertised value change, actual Authority
   or Bureaucracy cost, unmet-condition tooltip and 24-month cooldown; revisit the
   JE after monthly ticks and confirm one corruption tier only.
5. Save/reload and advance multiple months. Values must persist without tier or JE
   duplication. Manually verify initialization timing on a pre-provincial accounts save.
6. In a disposable save test independence/subject-type change, loss of monarchy,
   Qing disappearance and fragmentation: JE and status penalties must clear.
   Re-establishing an eligible administration must preserve accounts and restore
   its JE. Re-adding a previously completed JE is especially a runtime check.
7. With two human players (Qing plus a province), verify both see the correct
   country's values and no automatic law/integration behavior changed by provincial accounts.

No known unsupported engine token blocks provincial accounts. Runtime behavior and rendering remain
unverified; if the checks above fail, repair provincial accounts before proceeding to court register.

## Next action

Run the current provincial accounts refinement runtime checklist above. court register is not started or
automatically authorized; address any live UI/timer issue before expanding scope.

## Tiny changelog

- 2026-11-15: Added provincial accounts accounts, scoped lifecycle helpers, restrained corruption
  tiers, three costed/cooldown actions, live native governor indicators and validator.
- court register-regional works remain unimplemented, as explicitly required by the single-feature rule.
- provincial accounts refinement: live dossier bars/tiers, clean requirement and outcome summaries,
  explicit inspection term, percentage display, JE metadata and init BOM. court register not started.

## 2026-11-18 follow-up: self-strengthening funding and monthly progress

The latest source repair fixes a funding/progress gate that left subject projects
at 0/N reviews and without a visible national expense. The monthly provincial development country
pulse now synchronizes the project budget before running monthly project reviews.
Budget amounts are copied from scripted values into temporary variables, then
tested and applied as native scaled modifiers. Project reviews now check for the
installed `chi_adm_provincial_development_project_expense` modifier before subtracting a review,
alongside ownership and affordability checks.

Changed files: `common/scripted_effects/chi_adm_provincial_development_budget.txt`,
`common/scripted_effects/chi_adm_provincial_development_extension.txt`, and
`common/on_actions/chi_adm_provincial_development_extension.txt`.

Focused provincial development, provincial development completion, and provincial development funding validators passed after this repair.
These checks do not verify the in-game budget display, subject treasury charge,
or monthly JE progress. Reload and advance one monthly review with a funded
subject project to confirm both the expense and progress change.
