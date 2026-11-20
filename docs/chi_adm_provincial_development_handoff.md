# provincial development handoff — interrupted at user's usage limit

Historical handoff: superseded by the 2026-11-17 provincial development continuation entry in
`docs/chi_adm_progress.md`. The funding, catch-up progression, region ownership,
MCH conversion name and calendar-grace repairs described there are now applied.
All feature validators pass; in-game acceptance remains pending. The original
handoff below is retained as audit context, not a current list of unimplemented work.

## Authoritative design

Use the conversation's agreed provincial development design and docs/chi_adm_provincial_development_conversion_amendment.md. Current roster is 13 administrations after the user's mergers, not the original 15. MCH starts as Three Eastern Generalships/General of Shengjing, and its civil conversion becomes a viceroyalty. Conversion takes 18 months and reduces Autonomy by 20 once. All existing laws remain. Separate Inner Mongolian and Xining compacts exist within MGL and XIB.

Emergency packages: Recruitment, Defensive Readiness, Local Provisioning. Governor requests one; Qing approves/counters/refuses. Authorized +5 Autonomy; defiance +10 Autonomy/-5 Loyalty/-10 relations. Military benefits expire after a three-month post-crisis grace; restoration is negotiated. Broader danger lasts three months and compares a hostile neighbor with twice the combined Qing/subject army projection. Ignored demands capped at +10 Autonomy per 36 months. Direct war/revolt/severe turmoil may qualify immediately.

Projects: military/economic/administrative, three tiers, one active province-wide project. 12/18/24 months; sponsorship 9/12/18. Costs scale with income and tier. Sponsored projects split costs through native transfers and inspections, with smaller Autonomy gains. Completed state improvements persist through ownership changes; new acquisitions gain no free upgrades. Unfinished work requires explicit new-owner takeover.

Enforcement: political/fiscal pressure or one contested play empire-wide. Qing victory restores disputed powers, -5 Loyalty and two-year supervision. Provincial victory +5 Autonomy and three-year guarantee blocking repeat enforcement/negotiated integration coercion. Civil conversion can be enforced only after previously accepted agreement is repudiated. No imperial security/regional works.

## Work added in this continuation

- provincial development extension definitions in common/{scripted_effects,scripted_triggers,script_values,static_modifiers,scripted_buttons,scripted_guis,journal_entries,on_actions}/chi_adm_provincial_development_extension.txt.
- events/chi_adm_provincial_development_extension.txt: sponsorship, regional compact, conversion, crisis demand and dispute events.
- common/diplomatic_actions/chi_adm_provincial_development.txt: three native sponsorship pact rates.
- common/{diplomatic_plays,war_goal_types}/chi_adm_provincial_development.txt and common/on_actions/chi_adm_provincial_development_enforcement.txt: custom enforcement and opposing guarantee demand.
- gui/journal_entry_widgets/chi_adm_provincial_development_extension.gui: provincial status/progress and Qing subject-row controls; common/customizable_localization/chi_adm_provincial_development_status.txt.
- Existing emergency powers corrected for actual Autonomy granted at the 100 cap. **Verified formula uses `min = 0 max = 5/10`; earlier helper used reversed bounds.** Restoration removes only the recorded gain.
- Existing negotiated integration trigger/effect/GUI/event coercion paths now respect chi_adm_provincial_development_guarantee. Added missing MCH legacy integration proposal button.
- Native MCH generalships and modernized viceroyalty government/title definitions in existing office titles government file; native fallback eligibility helper regenerated from actual office predicates. court register office text follows conversion.
- Last completed operation: regional customary compacts now apply distinct two-year local modifiers on their actual regional states (Mongol pastoral capacity, banner/Ili infrastructure, Xining education, MCH administrative capacity), paired with -2% Tax Collection. These are applied when customary protections are accepted. All new English is in chi_adm_l_english.yml.

## Validation results

All provincial accounts, court register, office titles, imperial law reform, memorials and audits and negotiated integration validators passed in the last full run before the final provincial development-only presentation/compact additions. provincial development validator passed after the final regional compact changes.

Run `python -B tools/validate_chi_adm_provincial_development.py`; it invokes validate_chi_adm_provincial_development_complete.py. Checks parse all provincial development files, IDs, localization references, GUI scripted bindings, installed modifier types, military modernization overlap, 202 actual-effect Autonomy cap/defiance/restoration cases, and structural project/conversion/enforcement guarantees. These are NOT engine or complete lifecycle simulation tests.

Earlier validator failures were reconciled without replacing historical baseline JSONs. tools/chi_adm_authorized_migrations.json records exact current hashes and named reasons for specifically authorized setup/core/government changes; tools/chi_adm_authorized_validation.py recognizes those snapshots. Original semantic checks still run. Current roster expectations are 13; MCH initialization is 85/15/25; archived office titles runtime fixture is not fabricated for MCH. negotiated integration fiscal decay test now expects both tiers to last 60 monthly reviews. imperial law reform localization freshness compares keys/values, allowing later appended sections; its coverage report was refreshed. Inspect these adjustments if continuing validation—do not blindly regenerate hashes.

## Important remaining audit before claiming completion

1. **Project funding/sponsorship:** inspect actual expense scaling versus sponsorship. Bill weight is state-population weighted, while native sponsorship rates are 2.5/5/7.5% of whole provincial income. Territory gained/lost mid-project may make them diverge; ensure sponsorship cannot exceed the intended half-cost or yield free income. Funding pauses/resumption need stronger execution tests. Verify inspection modifier cleanup and inactive/dead payee cleanup.
2. **Enforcement:** custom `kind = custom` and add_war_goal are native-supported. Actual creation against one's own subject, opposing guarantee goal, backing down, white peace, target independence/annexation, and resetting the single-play lock need runtime testing and fuller source lifecycle tests. Do not assert engine success from parser checks.
3. **Project state persistence:** country objects are stored in state variables as project_owner; progress requires equality with root. Test save/load, annexation, split ownership, explicit takeover, overlapping inherited projects, cancellation and current_tier handling. Higher tiers currently require all current states to hold the preceding tier, Central Archives and literacy_rate 25%/40%; reconsider handling newly acquired unupgraded states without granting free upgrades.
4. **Consent and replay:** action helpers guard stage values; compact and sponsorship refusal cooldowns were added. Audit stale events, unsolicited counters, simultaneous court/provincial clicks, expiry/default options, and no repeated rewards. Civil reorganization is initially voluntary; repudiation notifies the court.
5. **Crisis completeness:** local war/secession/severe turmoil and sustained neighboring danger exist; weak-court wartime pressure exists. Check internal revolution detection, current broad-danger semantics, and grace-period timing. Monthly grace countdown can approximate rather than exactly match three calendar months.
6. **GUI/status:** uses verified AccessPlayer.GetSubjects and Country bindings. Actual rendering/scrolling not checked. Court actions expose native script effects but may still produce verbose bookkeeping tooltips. Conversion uses conditional status; project bars conditional. Ensure package choice and compact proposal details are sufficiently clear before player acceptance.
7. **Regional customs:** separate per-region agreement variables and distinct local customary modifiers exist. Check regional actions require continued ownership of their relevant states and that state loss does not allow irrelevant compact bargains. Current selection is mostly tag-based.
8. **Military stacking:** compared against chi_early_army.txt. No duplicate combat/training modernization bonuses. Only common field is military goods cost: existing artillery +50% cost, provincial development provisioning -5% offset. This interaction is intentional and tested structurally.
9. **Historical naming:** MCH generalships/viceroyalty government and court register title wiring added. Confirm dynamic country name also follows MCH conversion correctly; existing conditional name definitions may still be restricted to frontier status.
10. Re-run all feature validators after any changes, inspect final files, and update docs/chi_adm_progress.md with an accurate final report. The existing progress header still describes emergency powers and needs superseding—not wholesale deletion of historical notes.

## Tooling caution

Numerous tools/*chi_adm_provincial_development*.py and completion/wiring helpers were used as **one-time migrations**. Many are not idempotent and some initial builders omit later fixes. **Do not rerun builders/migrations blindly:** they may duplicate definitions, restore old bugs or overwrite refinements. Treat current generated game files as the current implementation until tooling is consolidated safely. Validation scripts are safe to run.

No imperial security–regional works content was implemented. Continue auditing and finishing provincial development only.
