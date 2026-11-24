# China Branch progress

## M7 presentation and discovery

Evidence was independent of Imperial Security before the rework and remains independent. Qing owns the single active case. The founder sets evidence to 10 through `chi_adm_qing_security_found`. The country pulse calls `chi_adm_qing_security_court_review`, which adds `chi_adm_qing_security_monthly_evidence`: 1 base, 2 per eligible armed office (including the claimant), 1 per eligible covert office, and 1 extra per armed office at 70 or more Corruption. Pledges change subsequent monthly evidence. Promotion to phase 3 at month six or later with two valid armed governors sets a minimum of 50. Betrayal adds 30, an inquiry adds 25 to an active prewar case, and pressure adds 15 after discovery. Evidence is capped at 100 and cleared on closure. No effect subtracts from the running total.

One reachable route is a claimant who remains eligible and a second eligible governor who joins in phase 2 after month four. At the month-six review, two valid armed governors advance the case to phase 3 and raise evidence to at least 50. A single eligible claimant also produces 3 per month and can reach 52 at month 14, before the 30-month expiry. A recruited governor can expose a case by reporting once at least 20 evidence has accumulated.

`chi_adm_qing_security_brief` dispatches the discovery notification once at 50. Founding does not dispatch it. Imperial Security activates for a valid Qing court when `chi_adm_qing_security_court_threat` is true: a prewar case at 50 or more, an open phase-five contest at 50 or more, or a pending restoration settlement. Loss of eligibility deactivates the entry. Closure clears evidence, case state and the briefing marker; pending restoration keeps the court actions available until resolved or expired.

The preventive inquiry lives in Governance of the Empire. Qing and Qing AI can initiate an inquiry based on public provincial warnings, subject to the existing Bureaucracy and inquiry restrictions. The effect always commits Bureaucracy and only adds evidence if a prewar case exists. The AI uses the existing Qing monthly pulse. Its inquiry decision no longer uses hidden evidence.

The provincial journal presents Provincial Political Affairs until the governor is the claimant, has access to recruitment, sees an exposed case, or has a wartime pact. The existing dossier and roster permissions still control its detailed information.

### Validation

Focused static source and rule checks cover startup, founding, hidden monthly accumulation, discovery, inquiry with and without a case, betrayal, AI routing, and closure. Save/load and two-human secrecy still require runtime checks. No M1–M8 validator suite was present in this checkout.
