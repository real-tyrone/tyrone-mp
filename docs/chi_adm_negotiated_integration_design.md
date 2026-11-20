# negotiated integration implementation contract and runtime checks

negotiated integration only. The user's interview decisions supersede the original brief's one-project
limit, 25% Bureaucracy gate, war-pausing rules and AI-only annexation fallback.
No provincial development–regional works systems are implemented. Current pact bases remain 20% civil / 15% frontier.

## Architecture and state ownership

Qing negotiates the transfer of provincial authority through events, with the
ordinary diplomatic-play system as the contested alternative. One court JE lists
the 15 administrations; one reusable provincial JE appears for an open case.
Both use the existing court register groups, so their existing native nested collections
display the new entries. The Imperial Ledger gets one read-only integration line.

Province-owned variables store phase, elapsed work, offered concessions, response,
pressure/final-offer use, consent, suspension, breach, repayment and retry windows.
Proposal revision values are saved into event chains; stale event options cannot
change a newer proposal. A separate clock generation invalidates paused/restarted
work events. These two monotonic revision counters intentionally survive cleanup.
Qing owns only a derived active-project count. State scopes own decaying fiscal
privileges. No global selected-country variable or global daily iterator is used.

| State | Player lever | Timing / exit |
| --- | --- | --- |
| Proposal | Accept, request subsidy/protection/honors, offer centralization, delay, refuse | Events; silence is never consent. After six unanswered monthly reviews Qing can withdraw or escalate. |
| Court reply | Offer a specific concession, apply pressure once, accept centralization, grant time, withdraw or escalate | One improved offer after pressure; a further refusal permits withdrawal/coercion only. |
| Census | Request agreed suspension or cancellation; revoke terms in breach | First half of required work. Monthly calendar events start at agreement, not the next global pulse. |
| Transition | Same administrative choices | Second half; elapsed work never resets when project count changes. |
| Final review | AI completes; human must explicitly confirm annexation | Final confirmation directly permits annexation while player-controlled. No forced player switch. |
| Confirmation withheld | Qing holds the process open or declares provincial breach | No annexation inferred from waiting or a timeout. |
| Agreed suspension | Resume with nonnegative current resources | Work, subsidies and commitments stop. Completed whole work-months remain; resumed work starts a fresh monthly clock. |
| Qing breach | Governor maintains consent or withdraws | Unilateral suspension/revocation permits withdrawal without repayment. |
| Cancellation / repayment | Demand, accept, counter, refuse, forgive or escalate | Native temporary payment pacts start only after agreement. |

## Timing and costs

Required work is `6 + 3 * (active integrations - 1)` months; census ends at half
that total, rounded naturally by whole-month reviews. Once reached, transition
does not regress to census. Adding a project can move a completed-but-unconfirmed
case back into transition; the old final-response event is invalidated on review.
Each due calendar review uses the current active count. Completions may therefore
allow another project to finish at its next due review, including reviews on the
same date. Suspended projects and negotiations do not count. Completed projects
awaiting human confirmation remain committed until resolution.

Each active project supplies -50 Authority and -10% Bureaucracy through one native
JE-scaled court modifier. This stacks by count without repeated timed modifiers.
Initial proposals require nonnegative current Authority/Bureaucracy; agreement and
resumption check them again. A new commitment may cause a deficit; existing work
continues. Central Archives, unlocked Mandate centralization, Liberty Desire <=25,
direct administrative-subject status, peace and no committed play gate proposals.
Unrelated wars do not stop work. Hostility between Qing and the target cancels it.

## Negotiation and balance tuning

Loyalty, Autonomy, Corruption, relations, consolidated imperial authority, frontier
status and offered terms alter AI event weights, not work speed. Favorable offices
can accept without concessions. Frontier offices prefer centralization/protection;
proposals never overwrite their laws. Tibet, Korea and Lanfang are excluded.

- Financial support: a native automatic pact pays 10%, or 20%, of provincial
  income from Qing during active implementation. Existing remittances are separate.
  There are no scripted treasury grants, manual weekly payments or arrears.
- Fiscal privileges: -10% state Tax Collection for 60 monthly decay steps, or -20%
  for 120. The multiplier falls linearly to zero. It starts on the province's
  original states before negotiated annexation and follows those states afterward.
  A one-day marker prevents same-pulse initial decay. Native `state_tax_collection_mult`
  affects final collected tax revenue, rather than adding Taxation Capacity.
- Honors: +10 governor Popularity and Prominence for ten years, +3 Loyalty and
  +5 relations on full agreement. The modifier is replaced, never stacked.
- Closer centralization: immediate -5 Autonomy, +3 relations, one-year retry period.
  Pressure gives -3 Loyalty; otherwise offered honors give +3 Loyalty and are
  actually granted. No subsidy or post-annexation privilege starts without annexation.
- Pressure: once, -5 Loyalty and -10 relations. It never forces peaceful consent.
- Unsuccessful peaceful proposals: six-month retry window.
- Repayment tuning: full claim offers 10% provincial income for twelve months;
  mutual cancellation offers 5% for six months. The governor can counter with
  5% for six months, requiring Qing approval, or refuse. These are negotiated
  settlements, not an assertion that a calculated sum of prior payments is owed.
- Coercion: a dedicated annexation-kind war goal retains the installed native
  annexation validation and complete Infamy formula, multiplied by 0.25. Resistant
  other administrations lose 8 Loyalty/15 relations; ordinary offices 3/5;
  loyal centralized offices lose only 2 relations. These are initial tuning values.

Negotiated annexation transfers the current living governor with native
`remove_character_role = ruler` and `transfer_character = c:CHI`, without granting
an office. Other compatible existing character roles are not rewritten. Coercive
annexation provides no guaranteed governor transfer. Final peaceful integration
clears negotiated integration payments/state and calls the existing imperial law reform/memorials and audits cleanup helpers before annexation.
The old warlord reintegration buttons/play are unchanged.

## Native evidence and limitations

Installed `journal_entries.md` documents scaled active modifiers and country
propagation. `17_war_reparations.txt` and `30_fund_lobby.txt` demonstrate native
income-transfer flags/directions. The exported 1.15.1 effect log documents pact
creation/removal, character transfer/role removal and saved numeric event scopes.
Native `1848.txt` and `africa_colonial_events_03.txt` demonstrate modifier multipliers.
imperial law reform supplies the existing hidden calendar-event scheduling precedent. Native
`00_annex_country.txt` and `war_goal_types.md` verify annexation-kind behavior and
the Infamy calculation. GUI layouts reuse working memorials and audits controls and court register nesting.

No game was launched. Static parsing/model execution cannot prove:

1. Engine weekly payment accounting, income-base calculation or interaction with
   other native payment modifiers; confirm real debit and credit in both budgets.
2. Post-annexation player handling. Explicit final consent permits annexation as
   requested, but no `play_as` effect or guaranteed multiplayer handoff is supplied.
3. Whether transferred former rulers remain visible in Qing's national cast after
   native character cleanup. No appointment/dismissal system or new office is added.
4. Native diplomatic-play support/peace resolution for these custom subject types,
   exact calendar scheduling through save/load, or final GUI geometry at 1080p.

## Validation and runtime checklist

`python -B tools/validate_chi_adm_negotiated_integration.py` parses the owned script files, checks GUI
brace/binding/width/button uniqueness, English localization and native texture
references, and proves provincial accounts–memorials and audits source preservation. Original warlord button ASTs and
the original ledger are checked independently of advanced hash baselines. The
bounded interpreter executes the actual negotiated integration effects/triggers/script values: all 15
offices, stage timing, concurrency, human final consent, negotiation/pressure,
payments, suspension, repayment, decay, collapse/war/independence and persisted scalars.
It also checks that AI acceptance decreases with each adverse factor.

Run the existing provincial accounts/court register/office titles/imperial law reform/memorials and audits validators. Prior preservation baselines advance
only for the 15 replaced integration entry points and one ledger status line;
office titles now uses structural preservation for that intentionally replaced button file.

In game: propose to SHN and a frontier administration; test all responses and a
six-month unanswered human offer. Start a second project halfway through the first;
confirm 3/6 becomes 3/9. Suspend/resume, including refusal and Qing breach. Verify
resource commitments and both subsidy levels. Complete an AI integration and a
human integration with final confirmation; inspect the governor afterward. Try
withholding consent, repayment counter/refusal and the coercive play. Inspect tax
privileges at annexation, midway and expiry. Save/load during negotiation, paused
work and final review. Check collapse, independence and hostility cleanup.

Design-only rubric (0–5, not a runtime certification): agency 4, legibility 3,
system integration 4, pacing 4, consequences 4, reactivity 4, lifecycle 3,
narrative coherence 4: weighted 74.8/100. GUI/player/character runtime checks limit
the assessment; this is an implemented test candidate, not a runtime-certified release.
