# Berlin Conference — File Reference

All files that make up the Berlin Conference system, for standalone migration.

---

## Core Scripting

| File | Purpose |
|------|---------|
| `common/journal_entries/tyrone_berlin_conference.txt` | Main JE: `should_be_involved`, `immediate_all_involved` (inits all per-country vars + snatch vars + fires event 49), `on_monthly_pulse` (month counter, month-24 fallback trigger), `complete` trigger |
| `common/scripted_effects/africa_conference_effects.txt` | `assign_conference_gp_number_effect` — sets `conference_gp_number`, `remaining_claims_var`, `african_claims_var`, `africa_lock_left_var` per GP rank |
| `common/scripted_triggers/berlin_conference_claim_triggers.txt` | `can_claim_XXX_africa` triggers — one per area, just checks `NOT has treaty_blocked_XXX` |
| `common/scripted_guis/berlinConf_tyrone_scriptedguis.txt` | All 19 player claim buttons (`berlin_conf_claim_XXX`), one per area — `ai_is_valid = { always = no }` |
| `common/scripted_buttons/berlin_conference.txt` | Claim button shown in JE panel, triggers `berlin_conference.2` |

## Diplomacy

| File | Purpose |
|------|---------|
| `common/treaty_articles/berlin_block_claims.txt` | All 19 `berlin_block_XXX` treaties (player blocks an AI from an area) + `berlin_approve_distribution` (acceptance treaty). Congo and East Africa entries have snatch guard on `can_ratify` |

## Events

| File | Purpose |
|------|---------|
| `events/berlin_conference.txt` | `event 1` — conference invite; `event 3` — conference end (awards claims as state claims); `event 4` — free colonial law; `event 49` — AI historical + snatch start claims (hidden, fired from `immediate_all_involved`); `event 50` — monthly AI claiming via weighted `random_list` (hidden, on_actions); `event 51` — AI acceptance after 12 months (hidden, on_actions); `event 52` — month-24 fallback distribution + force-accept (hidden, fired from JE pulse) |

## AI Hooks

| File | Purpose |
|------|---------|
| `common/on_actions/berlin_conference_on_actions.txt` | Empty placeholder (events 50 and 51 are fired from the JE `on_monthly_pulse` directly) |
| `common/on_actions/tyrone_on_actions.txt` | Sets `berlin_conference_happening` global when conditions are met (triggers JE `possible`). **Shared file — only the Berlin Conference block needs migrating** |

## Settings

| File | Purpose |
|------|---------|
| `common/game_rules/berlin_conference_rules.txt` | `historical_africa_berlin` gamerule — `enabled` makes AI claim historical territories at conference start via event 49 |

## GUI

| File | Purpose |
|------|---------|
| `gui/berlin_conference.gui` | Main conference panel — map overlay, area claim buttons, vote/accept UI |
| `gui/scripted_widgets/berlin_scripted_widgets.txt` | Reusable GUI widgets used by the conference panel |

## Assets & Localization

| File | Purpose |
|------|---------|
| `gfx/interface/icons/event_icons/berlin_conference.dds` | Event icon |
| `localization/english/berlin_conference_l_english.yml` | All loc keys: event text, treaty names, tooltip strings, area names |

## Partial Dependencies (shared files — extract only the marked blocks)

| File | What to extract |
|------|----------------|
| `common/scripted_triggers/00_scripted_triggers.txt` | `european_colonies_south_africa` trigger (used in event 3 for South Africa claim distribution) |
| `common/on_actions/tyrone_on_actions.txt` | The `if = { # Berlin Conference ... }` block inside `on_yearly_pulse` that sets `berlin_conference_happening` |

---

## Key Variables Reference

| Variable | Scope | Purpose |
|----------|-------|---------|
| `conference_gp_number` | per-country | GP rank (1 = highest). Set by `assign_conference_gp_number_effect` |
| `remaining_claims_var` | per-country | Claim budget. GP1=10, GP2-3=8, GP4-5=6, GP6-8=3, GP9-10=2, GP11+=1 |
| `african_claims_var` | per-country | Same as above (used for button visibility) |
| `berlin_claimed_count` | per-country | How many areas this country has claimed (AI tracking) |
| `claimed_XXX_var` | per-country | Set when a country claims area XXX |
| `treaty_blocked_XXX` | per-country | Set by `berlin_block_XXX` treaty; blocks that country from claiming XXX |
| `accepted_conf_var` | per-country | Set when country approves the final distribution |
| `visible_berlin_conf_treaty_article` | per-country | Gates treaty article visibility |
| `snatching_congo` | per-country | Set on AI BEL if GP4+. Locks Congo for BEL, blocks player treaties against them |
| `snatching_east_africa` | per-country | Set on AI GER if GP4+. Locks East Africa for GER, blocks player treaties against them |
| `berlin_months_elapsed` | global | Month counter, incremented in JE monthly pulse. Event 51 checks >= 12, event 52 fires at = 24 |
| `berlin_conference_happening` | global | Set by on_actions when conditions met; gates JE `possible` |
| `berlin_conference_ended` | global | Set in event 3 `immediate`; used by all claim SGUIs and treaties |
| `locked_XXX` | global | Set when a GP uses their lock action on area XXX. GP4+ cannot claim locked areas |
| `XXX_claimed_countries_list` | global list | All countries that claimed area XXX (used for GUI map overlay visibility) |
| `part_of_berlin_conf_list` | global list | All currently involved countries; refreshed monthly |
| `berlin_conf_top3_gp_list` | global list | GP1-3 only; refreshed monthly |
| `berlin_accept_conf_list` | global list | All countries that have accepted the distribution |
