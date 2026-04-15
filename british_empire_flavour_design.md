# British Empire Flavour — Mod Design Document

**Purpose:** This document is a complete design specification for a Victoria 3 mod adding flavour to Britain (GBR) and her subjects. It is intended to be consumed by an LLM assisting in scripting, and should be treated as the authoritative source of truth for feature intent, scope, and mechanical logic. It does not contain implementation code — that is produced separately using the SKILL files.

---

## Table of Contents

1. The British Question (Path Selection)
2. Path A — Imperial Federation
3. Path B — The British Commonwealth
4. Governance of India (JE)
5. Governance Challenges (Player BIC)
6. The Socialist Option (GB Communist Event Override)

**Appendices:** Named Modifiers · Key Variables & Flags · Namespace Registry · Files to Create · Custom JE Group · Commonwealth Member Subject Type · Commonwealth Member Diplomatic Action · **Localization**

---

## Design Decisions Record

| Question | Decision |
|---|---|
| Q1 — Path selection timing | **Retire `imperial_events.1`. New `gbr_path.1` fires via `on_game_start`, unconditional. Formation effects (annexation + country name/colour) preserved in `on_complete`.** |
| Q2 — Shared-laws mechanic | **Dropped. Progress bar only. `imperial_federation_calculate_shared_laws` removed.** |
| Q3 — `bic_content.2` / `.3` fate | **Retired. A new "Honourable Company" progress bar is added to `je_governance_of_india` (AI BIC only), advancing on objective success and blocking the Sepoy Mutiny while active.** |
| Q4 — JE group | **New custom group `je_group_british_empire_affairs` created for all federation/commonwealth/governance JEs.** |
| Q5 — Federation JE timeout | **No timeout. JE stays open indefinitely until bar reaches 100 or button is used.** |
| Q6 — `canada_federated_var` / `australia_federated_var` | **Not required for completion. Instead, `can_aus.6` and `can_aus.8` advance the federation progress bar by +15 each when the federation path is active.** |
| Q7 — Honourable Company → Sepoy Mutiny | **Hard block (Option A). When `honourable_company_value >= 50`, the yearly pulse sets `invalidate_uneasy_raj` globally, disabling `je_uneasy_raj`. If bar drops below 50, the global variable is removed and the mutiny risk resumes.** |
| Q8 — Imperial Federation completion gate | **Pan-nationalism (`law_type:law_pan_nationalism`) required in the `complete` block alongside the bar reaching 100. Bar can progress freely before this law is enacted.** |
| Q9 — Commonwealth GBR migration modifier | **Replace `country_influence_mult` on all three GBR stage modifiers with `state_migration_pull_mult`: Stage 1 = 0.075 (7.5%), Stage 2 = 0.15 (15%), Stage 3 = 0.25 (25%).** |
| Q10 — Commonwealth Stage 3 subject type | **When a dominion's JE reaches Stage 3, that dominion is converted to new subject type `subject_type_commonwealth_member`: no overlord fees (autonomy_level 3), can be a great power, overlord can enforce laws, GUI icon = personal union icon.** |

---

## Implementation Context

The following existing files are affected by this feature set. All new content is additive unless the Action column says REPLACE or REMOVE.

| Existing File | Relevant Key(s) | Action |
|---|---|---|
| `events/RB_imperial_events.txt` | `imperial_events.1` | RETIRE — replaced by `gbr_path.1` in new namespace |
| `common/journal_entries/00_imperial.txt` | `je_imperial_federation` | REPLACE using `REPLACE:je_imperial_federation` |
| `common/scripted_buttons/imperial_federation_buttons.txt` | `enact_imperial_federation` | KEEP — formation effects called from `je_progress_to_federation`'s `on_complete` |
| `common/scripted_effects/imperial_fed_effects.txt` | `imperial_federation_calculate_shared_laws` | REMOVE — shared-laws mechanic dropped |
| `common/journal_entries/00_bic_content.txt` | `je_company_equity` | REPLACE using `REPLACE:je_company_equity` |
| `events/RB_bic_content.txt` | `bic_content.1` | KEEP — still fires the JE intro; update JE type reference if key changes |
| `events/RB_bic_content.txt` | `bic_content.2`, `bic_content.3` | RETIRE — removed, not repurposed |
| `localization/english/RB_imperial_l_english.yml` | All keys | KEEP — do not modify; all new/updated keys go in `gbr_l_english.yml` which loads after it |

**Syntax note for implementers:** Victoria 3 uses `set_variable = flag_name` (boolean, no value) and `has_variable = flag_name` for country-scoped flags. There is no `set_country_flag` effect in Vic3. All references to "country flag" in this document mean `set_variable` on the relevant country scope.

---

## 1. The British Question (Path Selection)

### Summary

On game start, GBR receives a **country_event** pop-up that forces the player to choose between two grand strategic paths for managing Britain's empire: the **Imperial Federation** (centralisation, annexation) or the **British Commonwealth** (partnership, devolution). This event fires unconditionally for GBR.

### Trigger

- Fires via `on_game_start` on_action, scoped to `c:GBR`.
- No conditions — always fires.

> **Implementation note:** `imperial_events.1` is retired. `gbr_path.1` is a new event in a new namespace, fired unconditionally from `on_game_start`. The existing `imperial_events.1` loc and visual assets can be ported into `gbr_path` loc keys to save writing time.

### Event Structure

- **Type:** `country_event`
- **Namespace:** `gbr_path`
- **Event ID:** `gbr_path.1`
- **Title:** *"The Shape of Empire"* (`gbr_path.1.t`)
- **Description:** (`gbr_path.1.d`) Flavour text framing the choice between a federated union of British peoples and a looser commonwealth of equal partners. Should reference the late 19th-century political debates around imperial consolidation vs. colonial autonomy.
- **Flavour:** (`gbr_path.1.f`) Reference the dominions — CAN, AST, and BIC — by name using `save_scope_as` in `immediate`.
- **Video background:** `europenorthamerica_capitalists_meeting`
- **Icon:** `gfx/interface/icons/event_icons/waving_flag.dds`
- **Duration:** `3`
- **No trigger block needed** — fired directly by on_action.

```
# common/on_actions/gbr_on_actions.txt
on_game_start = {
    on_actions = { gbr_on_game_start_action }
}

gbr_on_game_start_action = {
    effect = {
        c:GBR ?= {
            trigger_event = { id = gbr_path.1 }
        }
    }
}
```

```
# events/gbr_path_events.txt
namespace = gbr_path

gbr_path.1 = {
    type = country_event
    duration = 3

    title = gbr_path.1.t
    desc = gbr_path.1.d
    flavor = gbr_path.1.f

    event_image = {
        video = "europenorthamerica_capitalists_meeting"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    icon = "gfx/interface/icons/event_icons/waving_flag.dds"

    immediate = {
        c:CAN = { save_scope_as = can_scope }
        c:AST = { save_scope_as = aus_scope }
        c:BIC = { save_scope_as = raj_scope }
    }

    option = {
        name = gbr_path.1.a   # "Forge a Federal Empire"
        default_option = yes
        set_variable = gbr_imperial_federation_path
        add_journal_entry = { type = je_progress_to_federation }
    }

    option = {
        name = gbr_path.1.b   # "Build a Commonwealth of Nations"
        set_variable = gbr_commonwealth_path
        # Dominion JEs added here — see Section 3 for full list
        add_journal_entry = { type = je_can_commonwealth }
        add_journal_entry = { type = je_ast_commonwealth }
        add_journal_entry = { type = je_saf_commonwealth }
        if = {
            limit = { exists = c:IRE }
            add_journal_entry = { type = je_ire_commonwealth }
        }
        if = {
            limit = {
                NOT = { has_law = law_type:law_ethnostate }
                exists = c:BIC
            }
            add_journal_entry = { type = je_bic_commonwealth }
        }
    }
}
```

### Notes

- The two variables (`gbr_imperial_federation_path` / `gbr_commonwealth_path`) are the canonical guards for all downstream content. Every JE, event, and option gated to one path should check `has_variable = gbr_imperial_federation_path` (or commonwealth equivalent) on `c:GBR`.
- If a future designer wants to make the choice available mid-game (e.g. after a treaty event), the variable system supports this without structural change.
- The Ireland dominion (`c:IRE` or `c:ki_CEL`) — implementer must verify the correct tag at implementation time. Use `exists = c:IRE` as a guard.

---

## 2. Path A — Imperial Federation

### Summary

Already partially implemented. The existing annexation flow (Canada, Australia, South Africa auto-annexed via `enact_imperial_federation` scripted button, name changes to "Imperial Federation") remains **unchanged**. This document adds the **"Progress to Federation" journal entry** and replaces the existing `je_imperial_federation` definition with it.

> **Existing code note:** `je_imperial_federation` used a shared-laws mechanic (`imperial_federation_calculate_shared_laws`) which is now dropped. The new JE uses only the progress bar for completion. The `enact_imperial_federation` scripted button is preserved and remains visible for manual completion; the formation effects are also triggered automatically from `on_complete`.

### JE: `je_progress_to_federation` (replaces `je_imperial_federation`)

**Implementation:** `REPLACE:je_imperial_federation` in `common/journal_entries/gbr_je_federation.txt`

**Group:** `je_group_british_empire_affairs` (new custom group — see Appendix)

**Icon:** `gfx/interface/icons/event_icons/waving_flag.dds`

**should_be_involved:** Same as existing — all countries in the British Empire.

```
# common/journal_entries/gbr_je_federation.txt

REPLACE:je_imperial_federation = {
    icon = "gfx/interface/icons/event_icons/waving_flag.dds"

    group = je_group_british_empire_affairs

    should_be_involved = {
        is_in_british_empire = yes
    }

    should_show_when_not_involved = {
        OR = {
            capital = { region = sr:region_england }
            top_overlord ?= {
                capital = { region = sr:region_england }
            }
        }
    }

    is_shown_in_lobby = {
        c:GBR = THIS
    }

    possible = {
        c:GBR ?= { has_variable = gbr_imperial_federation_path }
    }

    invalid = {
        OR = {
            NOT = { exists = c:GBR }
            c:GBR ?= { has_variable = imp_fed_cancelled }   # keep for backwards compat
        }
    }

    immediate = {
        c:GBR = {
            set_variable = { name = federation_progress_value value = 0 }
        }
    }

    on_yearly_pulse = {
        events = {
            # Federation bar advance/regression events fired here
            # See namespace gbr_fed_events in events/gbr_federation_events.txt
        }
        random_events = {
            chance_to_happen = 60
            100 = gbr_fed_events.1
            100 = gbr_fed_events.2
            100 = gbr_fed_events.3
            100 = gbr_fed_events.4
            100 = gbr_fed_events.5
            100 = gbr_fed_events.6
            100 = 0
        }
    }

    complete = {
        # Pan-nationalism law required to unlock federation — bar can progress freely beforehand
        has_law = law_type:law_pan_nationalism
        c:GBR ?= {
            # scripted_bar_progress(bar_federation_progress) >= 100
            # OR check variable directly:
            custom_tooltip = {
                text = federation_progress_complete_tt
                check_variable = { name = federation_progress_value value >= 100 }
            }
        }
    }

    on_complete = {
        # Formation effects — replicate the logic from enact_imperial_federation button
        # and from imperial_events.2 option A:
        c:GBR = {
            annex_with_incorporation = c:CAN
            annex_with_incorporation = c:AST
            annex_with_incorporation = c:SAF
        }
        # Set the global variable that triggers the dynamic country name and colour change
        # ("Imperial Federation" name and IMP_ADJ adjective, defined in loc and dynamic_country_names)
        set_global_variable = imperial_federation_var
        # Apply formation modifiers (from imperial_events.2 option A)
        add_modifier = {
            name = imperial_federation_modifier
            years = 25
        }
        if = {
            limit = { exists = c:BIC }
            c:BIC = { add_modifier = imperial_jewel }
        }
        # Fire the formation flavour event
        trigger_event = { id = imperial_events.2 }
    }

    scripted_progress_bar = bar_federation_progress

    scripted_button = enact_imperial_federation   # manual completion shortcut; keeps same logic

    weight = 500
    should_be_pinned_by_default = yes
}
```

> **Implementer note on formation effects:** The `on_complete` block above duplicates the logic from `enact_imperial_federation`. The scripted button is kept as a manual shortcut for the player, but `on_complete` ensures the formation fires automatically when the bar reaches 100. Do not double-apply — add a guard (`NOT = { has_global_variable = imperial_federation_var }`) to the button's `possible` block if needed.

#### Progress Bar Definition

```
# common/scripted_progress_bars/gbr_bars.txt

bar_federation_progress = {
    name = "BAR_FEDERATION_PROGRESS"
    desc = "BAR_FEDERATION_LEFT"         # "Dominion Sentiment"
    second_desc = "BAR_FEDERATION_RIGHT" # "Federation Achieved"

    default_green = yes

    start_value = 0
    min_value = 0
    max_value = 100

    # The bar reads federation_progress_value on GBR.
    # Advance is driven entirely by events in namespace gbr_fed_events.
    # No auto-advance blocks — leave empty.
}
```

> **Implementer note on bar advancement:** Victoria 3's scripted_progress_bar advances via `weekly_progress`, `monthly_progress`, or `yearly_progress` blocks defined in the bar itself, not via effects in events. To advance the bar exclusively via events, use one of:
> - A `yearly_progress = { add = { value = 0 } }` block (inert) and keep the variable `federation_progress_value` as the canonical tracker, with the `complete` condition checking the variable directly (not the bar).
> - OR verify in vanilla whether `change_scripted_progress_bar_value` or similar effects exist.
> The recommended fallback: track progress as a variable on GBR; the `complete` block checks the variable; events modify the variable via `change_variable = { name = federation_progress_value add = X }`. The scripted_progress_bar is kept for visual display only, referencing the variable in its progress formula if the engine supports it.

#### Progress Variable

- **Variable:** `federation_progress_value` on `c:GBR` (integer, 0–100)
- **Initialised to:** 0 in `immediate`
- Events advance via: `c:GBR = { change_variable = { name = federation_progress_value add = X } }`
- **`complete` checks:** `check_variable = { name = federation_progress_value value >= 100 }`

#### Events that advance the bar

Namespace: `gbr_fed_events`, file: `events/gbr_federation_events.txt`

These fire via the JE's `on_yearly_pulse` random_events block. A subset fires each year at random. Some advance the bar; others reduce it under bad conditions.

| Event ID | Bar delta | Flavour | Condition for negative |
|---|---|---|---|
| `gbr_fed_events.1` | +10 | Colonial Conference held | — |
| `gbr_fed_events.2` | +5 | Imperial Penny Post established | — |
| `gbr_fed_events.3` | +8 | Joint military exercise | — |
| `gbr_fed_events.4` | +12 | Imperial preferential tariff agreed | — |
| `gbr_fed_events.5` | +10 | Dominion PM voices support | — |
| `gbr_fed_events.6` | +15 | Popular referendum passes in a dominion | — |
| `gbr_fed_events.10` | -10 | Dominion unrest / war | Any dominion `liberty_desire > 50` |
| `gbr_fed_events.11` | -5 | Colonial scandal | Random negative |
| `gbr_fed_events.12` | -15 | Dominion refuses envoy | Major dominion relations below threshold |

Negative events (`gbr_fed_events.10`–`.12`) should have `trigger` blocks checking relevant conditions and should only fire if those conditions are met. They are not included in the random_events pool unconditionally.

The bar should represent a ~15–25 year journey from game start if conditions go well, with genuine risk of setback.

#### Canada and Australia unification advances the bar

`can_aus.6` (GBR receives unified Canada) and `can_aus.8` (GBR receives unified Australia) each advance the federation bar by **+15** when the federation path is active. Add the following to the option block in each event, guarded by the path variable:

```
# In can_aus.6 option.a and can_aus.8 option.a:
if = {
    limit = { has_variable = gbr_imperial_federation_path }
    change_variable = { name = federation_progress_value add = 15 }
    if = {
        limit = { check_variable = { name = federation_progress_value value > 100 } }
        set_variable = { name = federation_progress_value value = 100 }
    }
}
```

This means a player who actively unifies both dominions gains 30 bar progress from these events alone, on top of what accrues from `gbr_fed_events`.

**Event skeleton (positive example):**
```
# events/gbr_federation_events.txt
namespace = gbr_fed_events

gbr_fed_events.1 = {
    type = country_event
    duration = 3

    title = gbr_fed_events.1.t
    desc = gbr_fed_events.1.d
    flavor = gbr_fed_events.1.f

    event_image = {
        video = "europenorthamerica_capitalists_meeting"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    icon = "gfx/interface/icons/event_icons/waving_flag.dds"

    trigger = {
        has_variable = gbr_imperial_federation_path
        has_journal_entry = je_imperial_federation
    }

    option = {
        name = gbr_fed_events.1.a
        default_option = yes
        change_variable = { name = federation_progress_value add = 10 }
    }
}
```

**Negative event skeleton:**
```
gbr_fed_events.10 = {
    type = country_event
    duration = 3

    title = gbr_fed_events.10.t
    desc = gbr_fed_events.10.d
    flavor = gbr_fed_events.10.f

    event_image = {
        video = "unspecific_politicians_arguing"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    icon = "gfx/interface/icons/event_icons/event_protest.dds"

    trigger = {
        has_variable = gbr_imperial_federation_path
        OR = {
            c:CAN ?= { liberty_desire > 50 }
            c:AST ?= { liberty_desire > 50 }
            c:SAF ?= { liberty_desire > 50 }
        }
    }

    option = {
        name = gbr_fed_events.10.a
        default_option = yes
        change_variable = { name = federation_progress_value add = -10 }
    }
}
```

---

## 3. Path B — The British Commonwealth

### Summary

Instead of annexation, the Commonwealth path maintains the dominions as distinct entities but binds them economically, politically, and culturally through journal entries. Each dominion gets its own JE that is **visible in both GBR's journal and the dominion's own journal**. All JEs are added simultaneously when Option B is chosen.

### Shared Visibility Mechanism

> **Implementation pattern:** Victoria 3 JEs are added to a single country (GBR) and made visible to other countries via the `should_be_involved` trigger — exactly how `je_company_equity` shows in both GBR's and BIC's journal. Do NOT add the same JE type to both countries via `add_journal_entry`; instead use `should_be_involved` to show it in the dominion's journal.

```
should_be_involved = {
    OR = {
        c:GBR = THIS
        c:CAN = THIS    # replace per-dominion
    }
}
```

The JE is added only to GBR. It appears in the dominion's journal automatically because of `should_be_involved`.

### Dominion JEs — Shared Structure

Four (or five) JEs, one per dominion, all following the same pattern.

**JE keys:** `je_can_commonwealth`, `je_ast_commonwealth`, `je_saf_commonwealth`, `je_ire_commonwealth` (conditional), `je_bic_commonwealth` (conditional).

**Group:** `je_group_british_empire_affairs` (new custom group — see Appendix).

**Stage variable:** `gbr_X_commonwealth_stage` on GBR (integer 1–3, X = CAN/AST/SAF/IRE/BIC). Initialised to 1 in `immediate`.

**JE skeleton (Canada as example; replicate for each dominion):**

```
# common/journal_entries/gbr_je_commonwealth.txt

je_can_commonwealth = {
    icon = "gfx/interface/icons/event_icons/waving_flag.dds"

    group = je_group_british_empire_affairs

    should_be_involved = {
        OR = {
            c:GBR = THIS
            c:CAN = THIS
        }
    }

    possible = {
        c:GBR ?= { has_variable = gbr_commonwealth_path }
        c:CAN ?= {
            exists = yes
            is_subject_of = c:GBR
        }
    }

    invalid = {
        OR = {
            NOT = { exists = c:GBR }
            c:CAN ?= { NOT = { is_subject_of = c:GBR } }
        }
    }

    immediate = {
        c:GBR = {
            set_variable = { name = gbr_CAN_commonwealth_stage value = 1 }
        }
    }

    on_monthly_pulse = {
        # Modifiers are re-applied here based on current stage variable
        # OR use modifiers_while_active with scripted conditional modifiers
    }

    # Stage-based modifiers applied in events, not inline here.
    # See gbr_commonwealth_events namespace for stage advance events.

    status_desc = {
        first_valid = {
            triggered_desc = {
                desc = je_can_commonwealth_stage3_desc
                trigger = {
                    c:GBR ?= { check_variable = { name = gbr_CAN_commonwealth_stage value >= 3 } }
                }
            }
            triggered_desc = {
                desc = je_can_commonwealth_stage2_desc
                trigger = {
                    c:GBR ?= { check_variable = { name = gbr_CAN_commonwealth_stage value >= 2 } }
                }
            }
            triggered_desc = {
                desc = je_can_commonwealth_stage1_desc
            }
        }
    }

    weight = 300
    should_be_pinned_by_default = yes
}
```

### Dominion JE — Content

Each dominion JE represents the evolving relationship between Britain and that dominion. It has **three stages**, tracked by a variable on GBR (`gbr_X_commonwealth_stage`, values 1–3). The JE text changes based on stage. Stage advances are triggered by events in namespace `gbr_commonwealth_events`.

> **Modifier application pattern:** Stage modifiers are applied via events when a stage advances. Use `add_modifier = { name = modifier_key days = stupidly_long_modifier_time }` on the relevant country. Remove the previous stage modifier on advance. Alternatively, use a `modifiers_while_active` block with scripted triggers checking the stage variable — verify in vanilla whether `modifiers_while_active` supports conditional modifiers.

#### Stage 1 — "Loyal Dominion" (starting state)

GBR modifiers (applied on JE start, permanent while stage = 1):
```
gbr_commonwealth_stage1_gbr = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
    country_authority_mult = 0.05
    country_prestige_mult = 0.05
    state_migration_pull_mult = 0.075    # 7.5% — applied on country scope, affects all GBR states
}
```

Dominion modifiers (applied on JE start):
```
gbr_commonwealth_stage1_dominion = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds
    country_law_enactment_success_add = 0.05
    country_authority_mult = 0.05
}
```

#### Stage 2 — "Partner Nation" (mid-game, triggered by event)

Prerequisite event to advance: Fires when the dominion reaches GDP above a threshold or passes a major law. GBR player is offered a choice: grant greater autonomy (→ Stage 2) or maintain close oversight (→ Stage 1 retained + short liberty desire penalty on dominion).

GBR modifiers (Stage 2):
```
gbr_commonwealth_stage2_gbr = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
    country_prestige_mult = 0.10
    state_migration_pull_mult = 0.15    # 15% — replaces influence bonus from Stage 1
}
```

Dominion modifiers (Stage 2):
```
gbr_commonwealth_stage2_dominion = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds
    country_law_enactment_success_add = 0.10
    country_authority_mult = 0.10
    country_weekly_innovation_mult = 0.05
}
```

Stage 2 advance event skeleton:
```
# events/gbr_commonwealth_events.txt
namespace = gbr_commonwealth_events

# Canada stage 1→2 advance event (replicate per dominion)
gbr_commonwealth_events.1 = {
    type = country_event
    duration = 5

    title = gbr_commonwealth_events.1.t
    desc = gbr_commonwealth_events.1.d
    flavor = gbr_commonwealth_events.1.f

    event_image = {
        video = "europenorthamerica_capitalists_meeting"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    icon = "gfx/interface/icons/event_icons/waving_flag.dds"

    trigger = {
        has_variable = gbr_commonwealth_path
        has_journal_entry = je_can_commonwealth
        check_variable = { name = gbr_CAN_commonwealth_stage value = 1 }
        NOT = { has_variable = gbr_CAN_stage2_offered }
        c:CAN ?= {
            # GDP threshold or law condition — implementer to decide exact trigger
            gdp >= 5000   # placeholder — adjust based on playtesting
        }
    }

    immediate = {
        set_variable = gbr_CAN_stage2_offered
        c:CAN = { save_scope_as = dominion_scope }
    }

    option = {
        name = gbr_commonwealth_events.1.a  # "Grant greater autonomy"
        default_option = yes
        set_variable = { name = gbr_CAN_commonwealth_stage value = 2 }
        # Remove stage 1 modifiers, apply stage 2 modifiers
        remove_modifier = gbr_commonwealth_stage1_gbr
        add_modifier = { name = gbr_commonwealth_stage2_gbr }
        c:CAN = {
            remove_modifier = gbr_commonwealth_stage1_dominion
            add_modifier = { name = gbr_commonwealth_stage2_dominion }
        }
    }

    option = {
        name = gbr_commonwealth_events.1.b  # "Maintain close oversight"
        # Stage stays at 1; short liberty desire penalty
        c:CAN = {
            add_modifier = {
                name = gbr_oversight_maintained_penalty
                days = normal_modifier_time
            }
        }
    }
}
```

#### Stage 3 — "Equal Partner" (late-game, triggered by event)

Prerequisite: Fires when the dominion has recognised status, high HDI equivalent, and GBR has `law_democratic_backsliding` or better (implementer: verify exact law key). GBR player chooses to "affirm equal partnership" or "defer the question."

**Stage 3 key effect:** On "affirm equal partnership", the dominion is converted to `subject_type_commonwealth_member` — a new custom subject type with no overlord fees, equal great-power eligibility, and the personal union GUI icon. See the Commonwealth Member subject type definition in the Appendix.

GBR modifiers (Stage 3):
```
gbr_commonwealth_stage3_gbr = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
    country_prestige_mult = 0.15
    country_authority_mult = 0.05
    state_migration_pull_mult = 0.25                            # 25% — peak Commonwealth migration draw
    country_allow_enacting_decrees_in_subject_bool = yes        # GBR can enact decrees in Commonwealth Member subjects
}
```

> **Note on `country_allow_enacting_decrees_in_subject_bool`:** This modifier is applied to GBR when any dominion reaches Stage 3. It enables GBR to enact decrees in all its subject countries (not exclusively Commonwealth Members), so it is contextually earned through the mature Commonwealth relationship. Multiple dominions reaching Stage 3 will apply the same modifier multiple times, but since it is boolean the duplicate applications are harmless.

Dominion modifiers (Stage 3):
```
gbr_commonwealth_stage3_dominion = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds
    country_law_enactment_success_add = 0.15
    country_authority_mult = 0.15
    country_weekly_innovation_mult = 0.10
    country_prestige_mult = 0.10
}
```

Stage 3 advance event — option A ("affirm equal partnership") effect skeleton:
```
option = {
    name = gbr_commonwealth_events.X.a  # "Affirm Equal Partnership"
    default_option = yes
    set_variable = { name = gbr_CAN_commonwealth_stage value = 3 }   # replace CAN per-dominion
    # Remove stage 2 modifiers, apply stage 3 modifiers
    remove_modifier = gbr_commonwealth_stage2_gbr
    add_modifier = { name = gbr_commonwealth_stage3_gbr }
    c:CAN = {   # replace CAN per-dominion
        remove_modifier = gbr_commonwealth_stage2_dominion
        add_modifier = { name = gbr_commonwealth_stage3_dominion }
        # Convert subject type to Commonwealth Member
        change_subject_type = subject_type_commonwealth_member
    }
}
```

> **Implementation note:** The `change_subject_type` effect runs on the dominion country scope. Each dominion converts individually when its own JE reaches Stage 3 — they do NOT all convert simultaneously.

#### Invalidity

Each dominion JE becomes invalid if:
- The dominion is no longer a subject of GBR, OR
- GBR no longer exists.

When invalid, all modifiers applied by the JE are removed. Use `on_invalid` effect block with `remove_modifier` calls on both GBR and the dominion.

```
on_invalid = {
    remove_modifier = gbr_commonwealth_stage1_gbr
    remove_modifier = gbr_commonwealth_stage2_gbr
    remove_modifier = gbr_commonwealth_stage3_gbr
    c:CAN ?= {
        remove_modifier = gbr_commonwealth_stage1_dominion
        remove_modifier = gbr_commonwealth_stage2_dominion
        remove_modifier = gbr_commonwealth_stage3_dominion
    }
}
```

### Notes on Visibility

The JE is added only to GBR. The `should_be_involved` trigger shows it in the dominion's journal. JE description text should be written from a neutral third-party perspective (e.g. "The bond between Britain and Canada deepens" not "our bond with Canada") so it reads naturally from both sides.

---

## 4. Governance of India

### Summary

Replaces the existing `je_company_equity` JE (currently defined in `common/journal_entries/00_bic_content.txt`). This JE is always active regardless of path chosen. It governs the relationship between GBR and BIC (the East India Company / British India).

**Implementation:** `REPLACE:je_company_equity` in `common/journal_entries/gbr_je_india.txt`

**JE key:** `je_governance_of_india` — however, since we REPLACE `je_company_equity`, the key in the file should be `je_company_equity` (overriding the definition) unless the namespace is changed. If the key is changed to `je_governance_of_india`, all references to `je_company_equity` elsewhere (in `bic_content.1`, any loc, any trigger) must also be updated.

> **Recommendation:** Use `REPLACE:je_company_equity` and keep the key as `je_company_equity` internally, with the JE title and description loc changed to reflect the new "Governance of India" framing. This avoids cascading reference updates.

**Added to:** GBR (and visible on BIC's journal via `should_be_involved`).

**Group:** `je_group_british_empire_affairs` (new custom group — see Appendix)

**Icon:** `gfx/interface/icons/event_icons/event_portrait.dds` or `event_map.dds`

> **Existing events note:**
> - `bic_content.1` fires the intro event and adds the JE. It is kept but must reference the correct JE key (`je_company_equity` if using REPLACE, or the new key if renamed).
> - `bic_content.2` (Government of India Act) and `bic_content.3` (Repeal of Charter Act) are **retired** — they belonged to the completion/failure paths of the old equity JE, which no longer exist. Verify no other script references them before removal.

### JE Skeleton

```
# common/journal_entries/gbr_je_india.txt

REPLACE:je_company_equity = {
    icon = "gfx/interface/icons/event_icons/event_portrait.dds"

    group = je_group_british_empire_affairs

    should_be_involved = {
        OR = {
            c:GBR = THIS
            c:BIC = THIS
        }
    }

    should_show_when_not_involved = {
        OR = {
            is_in_geographic_region = geographic_region_india
            any_subject_or_below = {
                is_in_geographic_region = geographic_region_india
            }
        }
    }

    possible = {
        c:BIC ?= {
            exists = yes
            is_subject_of = c:GBR
        }
    }

    invalid = {
        OR = {
            NOT = { exists = c:GBR }
            NOT = { exists = c:BIC }
            c:BIC ?= { NOT = { is_subject_of = c:GBR } }
        }
    }

    immediate = {
        c:GBR = {
            save_scope_as = gbr_scope
            set_variable = { name = bic_gbr_ownership_pct value = 50 }  # placeholder — updated on pulse
            set_variable = { name = gbr_india_active_objective value = 0 }
            # gbr_india_objective_year initialised 5 years out
            # Implementer: use a script value for current_year + 5
        }
        c:BIC = {
            save_scope_as = raj_scope
            save_scope_as = company_scope
        }
    }

    on_yearly_pulse = {
        effect = {
            # 1. Update bic_gbr_ownership_pct (see Section B below)
            # 2. Check 5-year objective deadline
            c:GBR = {
                if = {
                    limit = {
                        # current_year >= gbr_india_objective_deadline
                        # Implementer: use check_variable with global year variable or
                        # a timed variable approach for the 5-year cycle
                        NOT = { has_variable = gbr_india_objective_cooldown }
                        has_variable = gbr_india_active_objective
                        check_variable = { name = gbr_india_active_objective value > 0 }
                    }
                    # Fire resolution check — see Section C
                    trigger_event = { id = gbr_india_objectives.9 }  # internal resolution router
                }
            }
        }
    }

    # Objective progress bars — defined per objective in common/scripted_progress_bars/gbr_bars.txt
    # scripted_progress_bar = bar_india_objective_X (one per active objective type)

    weight = 1000
    should_be_pinned_by_default = yes
}
```

---

### Section A — BIC AI Bonuses

When BIC is **AI-controlled**, apply a passive modifier to BIC at all times while the JE is active. When BIC is **player-controlled**, this modifier must NOT be applied.

**Modifier definition:**
```
# common/static_modifiers/gbr_modifiers.txt

bic_ai_administration_bonus = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds
    political_movement_radicalism_add = -0.50
}
```

**Application pattern (via `on_monthly_pulse` in the JE or via a scripted effect):**
```
on_monthly_pulse = {
    effect = {
        c:BIC ?= {
            if = {
                limit = { is_player_controlled = no }
                if = {
                    limit = { NOT = { has_modifier = bic_ai_administration_bonus } }
                    add_modifier = { name = bic_ai_administration_bonus }
                }
            }
            else = {
                # Player took control — remove AI bonus
                if = {
                    limit = { has_modifier = bic_ai_administration_bonus }
                    remove_modifier = bic_ai_administration_bonus
                }
            }
        }
    }
}
```

---

### Section A.2 — The Honourable Company Bar (AI BIC Only)

When BIC is **AI-controlled**, a second progress bar `bar_honourable_company` is displayed on the JE. This bar represents the degree to which the East India Company is administering India effectively under British guidance. It advances when 5-year objectives (Section C) succeed, and **blocks the Sepoy Mutiny from firing** while it holds value.

**This bar is entirely suppressed when BIC is player-controlled** — it should not display or advance.

#### Bar Definition

```
# common/scripted_progress_bars/gbr_bars.txt

bar_honourable_company = {
    name = "BAR_HONOURABLE_COMPANY"
    desc = "BAR_HC_LEFT"          # "Misrule"
    second_desc = "BAR_HC_RIGHT"  # "Exemplary Administration"

    default_green = yes

    start_value = 0
    min_value = 0
    max_value = 100
    # No auto-advance — advances via objective success events only
}
```

#### Bar Advancement

- Each **successful** objective completion: `change_variable = { name = honourable_company_value add = 15 }`
- Each **failed** objective: `change_variable = { name = honourable_company_value add = -5 }`
- The variable `honourable_company_value` is stored on GBR (int 0–100, clamped in effect).
- Variable initialised to 0 in the JE `immediate` block.

Add to each objective success event (`.10`–`.14`), inside the `c:GBR` scope, with the guard:
```
if = {
    limit = { c:BIC ?= { is_player_controlled = no } }
    change_variable = { name = honourable_company_value add = 15 }
    # Clamp to 100
    if = {
        limit = { check_variable = { name = honourable_company_value value > 100 } }
        set_variable = { name = honourable_company_value value = 100 }
    }
}
```

Add to each objective failure event (`.15`–`.19`):
```
if = {
    limit = { c:BIC ?= { is_player_controlled = no } }
    change_variable = { name = honourable_company_value add = -5 }
    if = {
        limit = { check_variable = { name = honourable_company_value value < 0 } }
        set_variable = { name = honourable_company_value value = 0 }
    }
}
```

#### Blocking the Sepoy Mutiny

The Sepoy Mutiny is driven by `je_uneasy_raj` (`common/journal_entries/04_sepoy_mutiny.txt`). The old `je_company_equity` blocked it by setting the global variable `invalidate_uneasy_raj` on completion or failure, which invalidates `je_uneasy_raj`. The new governance JE never completes, so it must manage this variable directly via its yearly pulse.

**Threshold:** `honourable_company_value >= 50`. Below this the mutiny system runs normally. At game start the bar is 0, so the mutiny is **not** initially blocked — it becomes blocked only after ~3–4 successful objectives (+15 each).

```
# In je_governance_of_india on_yearly_pulse:
c:BIC ?= {
    if = {
        limit = {
            is_player_controlled = no
            c:GBR ?= { check_variable = { name = honourable_company_value value >= 50 } }
        }
        # Bar is healthy — block the mutiny
        if = {
            limit = { NOT = { has_global_variable = invalidate_uneasy_raj } }
            set_global_variable = invalidate_uneasy_raj
        }
    }
    else_if = {
        limit = {
            is_player_controlled = no
            c:GBR ?= { check_variable = { name = honourable_company_value value < 50 } }
        }
        # Bar has dropped — restore mutiny risk
        if = {
            limit = { has_global_variable = invalidate_uneasy_raj }
            remove_global_variable = invalidate_uneasy_raj
        }
    }
    # When BIC is player-controlled: do not touch invalidate_uneasy_raj.
    # The player faces the natural mutiny system regardless of the bar.
}
```

> **Note:** `invalidate_uneasy_raj` is a global variable already used by the existing codebase (set by the old equity JE on complete/fail). The governance JE takes over exclusive responsibility for setting/removing it. Grep the full codebase for `invalidate_uneasy_raj` before implementation to confirm there are no other writers that could conflict.

---

### Section B — British Ownership Scaling Buff

GBR receives a scaling buff to BIC's productivity based on the approximate percentage of BIC's GDP owned by British-culture pops or GBR-controlled companies.

**Implementation note:** Vic3 does not expose a native "% of GDP owned by foreign country" value as a script value. Use the proxy: proportion of GBR company throughput contribution in BIC states vs. total BIC throughput. Store as variable `bic_gbr_ownership_pct` on GBR (integer 0–100). Update via the JE's `on_yearly_pulse`. The formula for the update will require implementer research into available script values for company ownership ratios.

**Scaling modifier applied to BIC.** At 100% British ownership, BIC receives the following. Values scale linearly (0% → all values 0; 50% → all values half):

| Modifier | Value at 100% |
|---|---|
| `building_group_bg_agriculture_throughput_add` | +0.20 |
| `building_group_bg_extraction_throughput_add` | +0.20 |
| `country_law_enactment_success_add` | +0.10 |
| `country_law_enactment_time_mult` | -0.10 |
| `building_group_bg_agriculture_laborers_mortality_mult` | +0.05 |
| `building_group_bg_extraction_laborers_mortality_mult` | +0.05 |

**Framing note:** The tooltip for this modifier should be titled *"Imperial Dividend"*. The `laborers_mortality_mult` keys are intentional — they reflect exploitative colonial extraction and are not bugs.

**Implementation pattern (applied on BIC via scripted modifier with multiply):**

```
# In yearly pulse, after updating bic_gbr_ownership_pct:
c:BIC ?= {
    # Remove previous modifier instance
    remove_modifier = bic_imperial_dividend
    # Reapply scaled modifier
    # Implementer: use a script_value to interpolate based on bic_gbr_ownership_pct
    # Exact pattern depends on engine support for dynamic modifier scaling
    add_modifier = {
        name = bic_imperial_dividend
        # If dynamic scaling isn't supported, apply one of several
        # threshold-based modifier variants (0-25%, 25-50%, 50-75%, 75-100%)
    }
}
```

> **Implementer note:** If continuous scaling is not supportable via `multiply` on modifier values, use four named threshold modifiers (`bic_imperial_dividend_low`, `_medium`, `_high`, `_full`) and apply the appropriate one based on the variable value range.

---

### Section C — Five-Year Objectives

Every **5 years**, GBR receives a `country_event` offering a choice of strategic objective for BIC.

**Timing mechanism:** Use a timed variable `gbr_india_objective_cooldown` with a 5-year duration, set after each resolution. When the variable expires, the yearly pulse fires the selection event.

```
# In JE immediate:
c:GBR = {
    set_variable = { name = gbr_india_active_objective value = 0 }
    set_variable = { name = gbr_india_objective_cooldown days = 1825 }  # 5 years
    trigger_event = { id = gbr_india_objectives.1 days = 30 }           # first selection after 1 month
}
```

```
# In JE on_yearly_pulse:
c:GBR = {
    if = {
        limit = {
            NOT = { has_variable = gbr_india_objective_cooldown }
            # No objective currently active that is unresolved:
            OR = {
                check_variable = { name = gbr_india_active_objective value = 0 }
            }
        }
        trigger_event = { id = gbr_india_objectives.1 }
    }
}
```

**Event namespace:** `gbr_india_objectives`, file: `events/gbr_india_objective_events.txt`

---

#### Objective Selection Event (`gbr_india_objectives.1`)

```
namespace = gbr_india_objectives

gbr_india_objectives.1 = {
    type = country_event
    duration = 5

    title = gbr_india_objectives.1.t   # "Directives for India"
    desc = gbr_india_objectives.1.d
    flavor = gbr_india_objectives.1.f

    event_image = {
        video = "ep1_persian_court"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    icon = "gfx/interface/icons/event_icons/event_portrait.dds"

    trigger = {
        # Triggered by on_yearly_pulse — leave empty
    }

    immediate = {
        c:BIC = { save_scope_as = raj_scope }
    }

    option = {
        name = gbr_india_objectives.1.a   # "Plantation Expansion"
        default_option = yes
        set_variable = { name = gbr_india_active_objective value = 1 }
        set_variable = { name = gbr_india_objective_cooldown days = 1825 }
    }

    option = {
        name = gbr_india_objectives.1.b   # "Resource Extraction"
        set_variable = { name = gbr_india_active_objective value = 2 }
        set_variable = { name = gbr_india_objective_cooldown days = 1825 }
    }

    option = {
        name = gbr_india_objectives.1.c   # "Industrialisation Mandate"
        set_variable = { name = gbr_india_active_objective value = 3 }
        set_variable = { name = gbr_india_objective_cooldown days = 1825 }
    }

    option = {
        name = gbr_india_objectives.1.e   # "Administrative Reform"
        # NOTE: option keys go .a .b .c .e — NEVER .d (conflicts with desc key)
        set_variable = { name = gbr_india_active_objective value = 4 }
        set_variable = { name = gbr_india_objective_cooldown days = 1825 }
        c:BIC = {
            add_modifier = {
                name = bic_reform_mandate_active
                days = 1825
            }
        }
    }

    option = {
        name = gbr_india_objectives.1.f   # "Frontier Expansion"
        set_variable = { name = gbr_india_active_objective value = 5 }
        set_variable = { name = gbr_india_objective_cooldown days = 1825 }
        c:BIC = {
            add_modifier = {
                name = bic_frontier_mandate_active
                days = 1825
            }
        }
        add_modifier = {
            name = gbr_frontier_infamy_buffer
            days = 1825
        }
    }
}
```

> **⚠️ Option key warning:** Never use `.d` as an option suffix — it is reserved for the description (`desc`) loc key. Options should use `.a`, `.b`, `.c`, `.e`, `.f`, etc.

---

#### Objective Definitions

##### Objective 1 — "Plantation Expansion"
- **Goal:** BIC builds 10 plantation buildings within 5 years.
- **Tracking:** Yearly pulse counts `count_buildings` of plantation type in BIC states.

**Success effects** (`gbr_india_objectives.10`):
```
c:BIC = {
    add_modifier = { name = bic_plantation_success days = very_long_modifier_time }
}
add_modifier = { name = gbr_india_objective_authority days = normal_modifier_time }
```

**Failure effects** (`gbr_india_objectives.15`):
```
c:BIC = {
    add_modifier = { name = bic_plantation_failure days = normal_modifier_time }
}
add_modifier = { name = gbr_india_objective_disappointment days = short_modifier_time }
```

##### Objective 2 — "Resource Extraction"
- **Goal:** BIC builds 8 logging camps or mines within 5 years.

**Success effects** (`gbr_india_objectives.11`):
```
c:BIC = {
    add_modifier = { name = bic_extraction_success days = very_long_modifier_time }
}
add_modifier = { name = gbr_india_objective_authority days = normal_modifier_time }
```

**Failure effects** (`gbr_india_objectives.16`):
```
c:BIC = {
    add_modifier = { name = bic_extraction_failure days = normal_modifier_time }
}
add_modifier = { name = gbr_india_objective_disappointment days = short_modifier_time }
```

##### Objective 3 — "Industrialisation Mandate"
- **Goal:** BIC builds 6 manufacturing buildings within 5 years.

**Success effects** (`gbr_india_objectives.12`):
```
c:BIC = {
    add_modifier = { name = bic_industry_success days = very_long_modifier_time }
}
add_modifier = { name = gbr_india_objective_authority days = normal_modifier_time }
add_modifier = { name = gbr_india_innovation_bonus days = normal_modifier_time }
```

**Failure effects** (`gbr_india_objectives.17`):
```
c:BIC = {
    add_modifier = { name = bic_industry_failure days = normal_modifier_time }
}
add_modifier = { name = gbr_india_objective_disappointment days = short_modifier_time }
add_modifier = { name = gbr_india_authority_loss days = short_modifier_time }
```

##### Objective 4 — "Administrative Reform"
- **Goal:** BIC enacts at least 1 law during the 5-year period.
- **Tracking:** Use `on_law_enactment_started` on_action scoped to BIC — set variable `bic_objective_law_enacted` when a law is enacted during the objective window. Check in the resolution event.
- **During-period modifier on BIC:** `bic_reform_mandate_active` — applied in the option block for 5 years.

```
bic_reform_mandate_active = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_documents_positive.dds
    country_law_enactment_success_add = 0.15
    country_law_enactment_time_mult = -0.15
}
```

**Success effects** (`gbr_india_objectives.13`):
```
c:BIC = {
    add_modifier = { name = bic_reform_success days = very_long_modifier_time }
}
add_modifier = { name = gbr_india_objective_authority days = normal_modifier_time }
add_modifier = { name = gbr_india_reform_prestige days = normal_modifier_time }
```

**Failure effects** (`gbr_india_objectives.18`):
```
c:BIC = {
    remove_modifier = bic_reform_mandate_active
    add_modifier = { name = bic_reform_failure days = normal_modifier_time }
}
add_modifier = { name = gbr_india_prestige_loss days = short_modifier_time }
```

##### Objective 5 — "Frontier Expansion"
- **Goal:** BIC annexes at least 1 unrecognised power subject or territory during the 5-year period.
- **Tracking:** `on_country_annexed` on_action scoped to BIC — set variable `bic_objective_territory_annexed`.
- **During-period modifiers:**

```
bic_frontier_mandate_active = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_rifle_positive.dds
    unit_offense_mult = 0.05    # HARD CAP for event modifiers
    unit_defense_mult = 0.05    # HARD CAP for event modifiers
}

gbr_frontier_infamy_buffer = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds
    country_infamy_decay_mult = 0.10
}
```

**Success effects** (`gbr_india_objectives.14`):
```
c:BIC = {
    add_modifier = { name = bic_frontier_success days = very_long_modifier_time }
    every_scope_state = {
        limit = { is_homeland_of = cu:british }
        add_loyalists = { value = 0.05 }   # implementer: verify exact effect syntax
    }
}
add_modifier = { name = gbr_india_frontier_prestige days = normal_modifier_time }
```

**Failure effects** (`gbr_india_objectives.19`):
```
c:BIC = {
    remove_modifier = bic_frontier_mandate_active
    add_modifier = { name = bic_frontier_failure days = short_modifier_time }
}
add_modifier = { name = gbr_india_objective_disappointment days = short_modifier_time }
```

---

#### Objective Resolution

At the end of the 5-year window (when `gbr_india_objective_cooldown` expires, checked on yearly pulse):

1. Fire internal resolution router `gbr_india_objectives.9` on GBR.
2. `gbr_india_objectives.9` checks `gbr_india_active_objective` and evaluates the success condition for that objective.
3. Fires appropriate success (`.10`–`.14`) or failure (`.15`–`.19`) event.
4. Resolution event resets `gbr_india_active_objective = 0` and schedules `gbr_india_objectives.1` in 30 days.

```
# Resolution router (internal, no UI — fires silently)
gbr_india_objectives.9 = {
    type = country_event
    duration = 1
    hidden = yes   # if supported; otherwise use immediate only

    immediate = {
        if = {
            limit = { check_variable = { name = gbr_india_active_objective value = 1 } }
            # Check plantation success condition
            if = {
                limit = { c:BIC ?= { /* plantation count >= 10 */ } }
                trigger_event = { id = gbr_india_objectives.10 }
            }
            else = {
                trigger_event = { id = gbr_india_objectives.15 }
            }
        }
        # ... repeat for objectives 2-5
        set_variable = { name = gbr_india_active_objective value = 0 }
        trigger_event = { id = gbr_india_objectives.1 days = 30 }
    }

    option = {
        name = gbr_india_objectives.9.a   # empty "dismiss" option for non-hidden version
    }
}
```

---

#### On_actions for BIC objective tracking

```
# common/on_actions/gbr_on_actions.txt (add to existing file)

on_law_enactment_started = {
    on_actions = { gbr_bic_law_track_action }
}

gbr_bic_law_track_action = {
    effect = {
        if = {
            limit = {
                c:BIC = THIS
                c:GBR ?= {
                    check_variable = { name = gbr_india_active_objective value = 4 }
                    has_variable = gbr_india_objective_cooldown
                }
            }
            c:GBR = { set_variable = bic_objective_law_enacted }
        }
    }
}

on_country_annexed = {
    on_actions = { gbr_bic_annex_track_action }
}

gbr_bic_annex_track_action = {
    effect = {
        if = {
            limit = {
                c:BIC = THIS
                c:GBR ?= {
                    check_variable = { name = gbr_india_active_objective value = 5 }
                    has_variable = gbr_india_objective_cooldown
                }
            }
            c:GBR = { set_variable = bic_objective_territory_annexed }
        }
    }
}
```

---

## 5. Governance Challenges (Player BIC)

### Summary

When BIC is **player-controlled**, a set of periodic challenge events and journal entries fires to make managing India genuinely difficult. These are intentional nerfs: AI-BIC is left unaffected. All content in this section is gated on `c:BIC = { is_player_controlled = yes }`.

Two categories of content:
- **The Unemployment Crisis** — a reactive JE that triggers when unemployment exceeds a threshold, building toward a famine if not resolved.
- **Periodic Hard Choices** — a pool of flavour events firing yearly on BIC, each presenting a lose/lose trade-off.

---

### 5A — The Unemployment Crisis

#### Trigger

An event `bic_challenges.1` fires when BIC has more than 5% unemployment. It starts a journal entry `je_bic_unemployment_crisis`.

```
# Trigger guard (in on_yearly_pulse_country, or a dedicated on_action for BIC)
c:BIC ?= {
    if = {
        limit = {
            is_player_controlled = yes
            NOT = { has_journal_entry = je_bic_unemployment_crisis }
            # Implementer: verify exact unemployment trigger key.
            # Candidates: country_unemployment_rate > 0.05, OR
            # fraction of unemployed pops vs total workforce pops.
            unemployment_rate > 0.05
        }
        trigger_event = { id = bic_challenges.1 }
    }
}
```

#### Event `bic_challenges.1` — "Unemployment Crisis"

- **Type:** `country_event`, BIC
- **Namespace:** `bic_challenges`
- **Title:** *"An Unemployment Crisis"*
- **Desc:** Flavour about the swelling ranks of unemployed workers in the cities of India, idle hands threatening unrest, and the spectre of famine if the situation is not resolved.
- **Video:** `ip2_india_protest` or `ip2_india_urban_scene`
- **Effect:** `add_journal_entry = { type = je_bic_unemployment_crisis }`

#### JE: `je_bic_unemployment_crisis`

**Group:** `je_group_british_empire_affairs`

**`possible`:** `c:BIC = { is_player_controlled = yes }`

**`invalid`:** BIC ceases to exist.

**Modifiers while active** (`modifiers_while_active`):

```
bic_unemployment_crisis_active = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_gear_positive.dds
    building_group_bg_construction_construction_efficiency_add = 0.15   # Urgency drives building boom
}

bic_unemployment_crisis_radicalism = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_fire_negative.dds
    state_radicals_from_political_movements_mult = 0.25   # Unemployed and hungry pops radicalise
    state_loyalists_from_political_movements_mult = -0.15
}
```

> **Design note:** The construction bonus is an intentional silver lining — the crisis pressures the player to build new industries rapidly to absorb unemployment, which is the intended mitigation path. The radicalism penalty punishes inaction.

**`complete`:**
```
complete = {
    # BIC unemployment falls below 3% — crisis resolved
    c:BIC = { unemployment_rate <= 0.03 }   # implementer: verify trigger key
}
```

**`on_complete`:**
```
on_complete = {
    remove_modifier = bic_unemployment_crisis_active
    remove_modifier = bic_unemployment_crisis_radicalism
    trigger_event = { id = bic_challenges.2 }    # "The Crisis Passes" — small reward event
}
```

#### The Famine Counter

Each year BIC fails to reduce unemployment below 3%, a counter variable increments. If it reaches 5 (five consecutive failing years), the famine event fires.

**Yearly pulse logic:**

```
# In common/on_actions/gbr_on_actions.txt — appended to on_yearly_pulse_country

gbr_bic_unemployment_pulse = {
    effect = {
        c:BIC ?= {
            if = {
                limit = {
                    is_player_controlled = yes
                    has_journal_entry = je_bic_unemployment_crisis
                }
                if = {
                    limit = { unemployment_rate > 0.03 }    # still above threshold
                    if = {
                        limit = { NOT = { has_variable = bic_famine_counter } }
                        set_variable = { name = bic_famine_counter value = 0 }
                    }
                    change_variable = { name = bic_famine_counter add = 1 }
                    if = {
                        limit = { check_variable = { name = bic_famine_counter value >= 5 } }
                        trigger_event = { id = bic_challenges.3 }    # Famine breaks
                    }
                }
                else = {
                    set_variable = { name = bic_famine_counter value = 0 }    # Reset streak on good year
                }
            }
        }
    }
}
```

#### Event `bic_challenges.3` — "The Great Famine"

- **Title:** *"Famine Grips India"*
- **Desc:** Flavour about the catastrophic failure to absorb India's population into productive labour. Fields lie fallow, granaries empty, and millions face starvation. Whole communities in Bengal are dissolving, the desperate boarding ships for the New World.
- **Video:** `ip2_india_poor_people_moving` or `asia_poor_people_moving`

**Effects:**
```
# Apply the famine modifier to all BIC states
every_scope_state = {
    add_modifier = {
        name = bic_great_famine
        days = 1825      # 5 years
        is_decaying = yes
    }
}
# Invalidate the unemployment JE (crisis has become a catastrophe)
set_variable = bic_famine_struck
remove_journal_entry = je_bic_unemployment_crisis   # implementer: verify effect name

# Mass emigration — push bengali pops out of Bengal, pull toward New York
every_scope_state = {
    limit = { state_region = s:STATE_BENGAL }
    add_modifier = {
        name = bic_famine_emigration_push
        days = 1825
        is_decaying = yes
    }
}
every_country = {
    limit = {
        any_scope_state = { state_region = s:STATE_NEW_YORK }
    }
    random_scope_state = {
        limit = { state_region = s:STATE_NEW_YORK }
        add_modifier = {
            name = bic_famine_bengali_pull_newyork
            days = 1825
            is_decaying = yes
        }
    }
}
```

#### Famine Modifier Definition

```
bic_great_famine = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_fire_negative.dds
    state_birth_rate_mult = -0.15                                       # Demographic collapse
    state_mortality_mult = 0.20                                         # Mass deaths
    building_group_bg_manufacturing_laborers_mortality_mult = 0.10      # Dangerous conditions in remaining industries
    building_group_bg_subsistence_agriculture_throughput_add = 0.10     # Desperate subsistence farming surge
}
```

> **Balance note:** These values intentionally exceed the standard event modifier caps (birth rate max ±0.05, mortality max ±0.10). This is a catastrophe event — the extreme values are the punishment for five consecutive years of inaction. The `is_decaying` flag softens the impact over the 5-year duration.

#### Emigration Modifier Definitions

```
bic_famine_emigration_push = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_fire_negative.dds
    state_migration_push_mult = 1.0     # Strong push out of Bengal — predominantly bengali pops will emigrate
}

bic_famine_bengali_pull_newyork = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_flag_positive.dds
    state_migration_pull_mult = 0.75    # New York draws the displaced
}
```

> **Implementation note on culture targeting:** Vic3 migration modifiers apply to all pops in a state, not a specific culture. Since Bengal is the predominantly bengali state, most emigrants will be bengali in practice. If a culture-specific push effect exists in vanilla (e.g. `state_culture_migration_push_mult` or a pop-type variant), use it for precision — but the state-level approach is the safe fallback.

---

### 5B — Periodic Hard Choices

A pool of flavour events that fire annually on player-BIC via `on_yearly_pulse_country`, with a moderate `chance_to_happen`. Each event presents a binary choice with no good answer — both options apply a negative modifier, differing only in which sector is hurt.

**Events pool:** `bic_challenges` namespace (IDs `.10`–`.19`)

**On_action entry:**
```
gbr_bic_challenges_yearly = {
    random_events = {
        chance_to_happen = 40      # 40% chance per year — fires roughly 2-3 times per decade
        chance_of_no_event = { value = 50 }
        100 = bic_challenges.10
        100 = bic_challenges.11
        100 = bic_challenges.12
        100 = bic_challenges.13
        100 = bic_challenges.14
        100 = 0
    }
}
```

**Trigger guard** on each event: `c:BIC = { is_player_controlled = yes }`

#### Event Pool

| ID | Title | Option A | Option B |
|---|---|---|---|
| `bic_challenges.10` | *"The Factory Question"* | Lower plantation throughput -10% (`agriculture_throughput_add -0.10`, `normal_modifier_time`) | Dangerous working conditions (`manufacturing_laborers_mortality_mult +0.10`, `normal_modifier_time`) |
| `bic_challenges.11` | *"Tax Collection Disputes"* | Accept reduced revenue: `country_authority_mult -0.05` for 1 year | Crack down: `state_radicals_from_political_movements_mult +0.25` in random BIC states for 1 year |
| `bic_challenges.12` | *"The Sahib's Salary"* | Pay British administrators: `country_expenses_add = 5` for 2 years | Reduce British staff: `country_bureaucracy_add -200` for 2 years |
| `bic_challenges.13` | *"Opium Trade Controversy"* | Continue trade: `country_prestige_mult -0.05`, `country_influence_mult -0.10` for 1 year | Restrict trade: `building_group_bg_plantations_throughput_add -0.10` for 2 years |
| `bic_challenges.14` | *"Sepoy Recruitment Drive"* | Accept the expansion: `building_group_bg_agriculture_laborers_mortality_mult +0.05` for 1 year | Decline: `country_authority_mult -0.10` for 1 year |

> **Design note:** All options are intentionally negative. The player cannot "win" these events — they can only choose which cost to pay. This is the core nerf philosophy: a player-controlled BIC must actively manage a stream of structural problems that an AI-BIC simply ignores.

#### Event Skeleton (example)

```
# events/gbr_bic_challenge_events.txt
namespace = bic_challenges

bic_challenges.10 = {
    type = country_event
    duration = 5

    title = bic_challenges.10.t
    desc = bic_challenges.10.d
    flavor = bic_challenges.10.f

    event_image = {
        video = "ip2_india_factory_floor"
    }

    on_created_soundeffect = "event:/SFX/UI/Alerts/event_appear"
    icon = "gfx/interface/icons/event_icons/event_industry.dds"

    trigger = {
        c:BIC = THIS
        is_player_controlled = yes
    }

    option = {
        name = bic_challenges.10.a    # "Ease the plantation quotas"
        default_option = yes
        add_modifier = {
            name = bic_plantation_output_throttled
            days = normal_modifier_time
        }
    }

    option = {
        name = bic_challenges.10.b    # "Keep quotas — accept the conditions"
        add_modifier = {
            name = bic_factory_dangerous_conditions
            days = normal_modifier_time
        }
    }
}
```

---

### Notes

- All content in Section 5 is BIC `is_player_controlled = yes` gated. AI-BIC is unaffected.
- The unemployment threshold (5%/3%) and the famine counter (5 years) are the primary tuning knobs. Adjust based on playtesting — if the famine fires too frequently reduce the 40% yearly pulse chance or raise the famine year threshold to 7.
- The `bic_challenges` namespace is reserved for all BIC player challenge content.
- `bic_famine_struck` variable on BIC is a one-time guard preventing `je_bic_unemployment_crisis` from re-triggering immediately after the famine.

---

## 6. The Socialist Option (GB Communist Event Override)

### Summary

If GBR has researched the Socialism technology, GBR receives a custom additional option in the vanilla event **"Oppressor and Oppressed"** (fired by *The Spectre Haunting the World* journal entry). If chosen, it sets a variable on GBR and unlocks a fifth option in the later vanilla event **"A World to Win"**.

> **Implementer task:** Search vanilla `events/` for event text "Oppressor and Oppressed" and "A World to Win" to identify the exact event IDs before implementation. The IDs `spectre.X` and `spectre.Y` are placeholders in this document.

> **Implementer task:** Identify the Socialism technology's exact script key (`tech_socialism` is a placeholder — search `common/technology/` for the correct key). Similarly identify the communism bar variable/progress bar key used by the vanilla spectre JE.

---

### Step 1 — Override "Oppressor and Oppressed"

Use `REPLACE_OR_CREATE:spectre.X` (replace with verified event ID).

Add the following option block to the replacement definition, after all vanilla options are copied:

```
# events/gbr_spectre_overrides.txt
# Implementer: copy all vanilla options for spectre.X here before adding the new option

REPLACE_OR_CREATE:spectre.X = {
    # ... (all vanilla content copied here) ...

    option = {
        name = spectre.X.gbr   # "Socialism under one Empire"

        trigger = {
            c:GBR ?= THIS
            has_technology_researched = tech_socialism   # verify exact key
        }

        # Advance communism bar — implementer: match exact vanilla mechanism
        # change_variable = { name = spectre_communism_progress add = 3 }   # placeholder

        c:GBR = { set_variable = gbr_socialism_one_empire }
    }
}
```

**Option name loc:** *"Socialism under one Empire"*
**Option flavour:** *"As the global hegemon, Britain stands as the only power capable of bringing revolution to this world. We will gladly fulfill this duty."*

**Effects:**
- Advances the communism bar by +3 (match vanilla mechanism exactly — implementer must verify the variable/effect used).
- Sets variable `gbr_socialism_one_empire` on GBR.

---

### Step 2 — Override "A World to Win"

Use `REPLACE_OR_CREATE:spectre.Y` (replace with verified event ID).

```
REPLACE_OR_CREATE:spectre.Y = {
    # ... (all vanilla content copied here) ...

    option = {
        name = spectre.Y.gbr   # "Initiate General Order One"

        trigger = {
            c:GBR ?= THIS
            has_variable = gbr_socialism_one_empire
        }

        # PLACEHOLDER: Effects for "Initiate General Order One" to be specified by designer.
        # Do not implement effects until confirmed.
    }
}
```

---

## Appendix — All Named Modifiers

All modifiers defined in `common/static_modifiers/gbr_modifiers.txt`.

| Modifier Key | Scope | Contents | Duration when applied |
|---|---|---|---|
| `gbr_commonwealth_stage1_gbr` | Country (GBR) | `authority_mult +0.05`, `prestige_mult +0.05`, `migration_pull_mult +0.075` | Permanent until stage changes |
| `gbr_commonwealth_stage1_dominion` | Country (Dominion) | `law_enactment_success_add +0.05`, `authority_mult +0.05` | Permanent until stage changes |
| `gbr_commonwealth_stage2_gbr` | Country (GBR) | `prestige_mult +0.10`, `migration_pull_mult +0.15` | Permanent until stage changes |
| `gbr_commonwealth_stage2_dominion` | Country (Dominion) | `law_enactment_success_add +0.10`, `authority_mult +0.10`, `innovation_mult +0.05` | Permanent until stage changes |
| `gbr_commonwealth_stage3_gbr` | Country (GBR) | `prestige_mult +0.15`, `authority_mult +0.05`, `migration_pull_mult +0.25`, `allow_enacting_decrees_in_subject_bool = yes` | Permanent until stage changes |
| `gbr_commonwealth_stage3_dominion` | Country (Dominion) | `law_enactment_success_add +0.15`, `authority_mult +0.15`, `innovation_mult +0.10`, `prestige_mult +0.10` | Permanent until stage changes |
| `gbr_oversight_maintained_penalty` | Country (Dominion) | TBD — small liberty desire proxy | `normal_modifier_time` |
| `bic_ai_administration_bonus` | Country (BIC) | `political_movement_pop_attraction_mult +0.15` | Permanent (re-applied each pulse) |
| `bic_imperial_dividend` | Country (BIC) | Scaling agriculture/extraction buffs + mortality malus | Refreshed yearly |
| `bic_reform_mandate_active` | Country (BIC) | `law_enactment_success_add +0.15`, `law_enactment_time_mult -0.15` | 1825 days (5 years) |
| `bic_frontier_mandate_active` | Country (BIC) | `unit_offense_mult +0.05`, `unit_defense_mult +0.05` | 1825 days |
| `gbr_frontier_infamy_buffer` | Country (GBR) | `infamy_decay_mult +0.10` | 1825 days |
| `bic_plantation_success` | Country (BIC) | `agriculture_throughput_add +0.10`, `agriculture_mortality_mult +0.05` | `very_long_modifier_time` |
| `bic_plantation_failure` | Country (BIC) | `authority_mult -0.05` | `normal_modifier_time` |
| `bic_extraction_success` | Country (BIC) | `extraction_throughput_add +0.10`, `mining_throughput_add +0.10`, `extraction_mortality_mult +0.05` | `very_long_modifier_time` |
| `bic_extraction_failure` | Country (BIC) | `authority_mult -0.05` | `normal_modifier_time` |
| `bic_industry_success` | Country (BIC) | `manufacturing_throughput_add +0.10`, `light_industry_throughput_add +0.05` | `very_long_modifier_time` |
| `bic_industry_failure` | Country (BIC) | `authority_mult -0.05` | `normal_modifier_time` |
| `bic_reform_success` | Country (BIC) | `law_enactment_success_add +0.10`, `authority_mult +0.10` | `very_long_modifier_time` |
| `bic_reform_failure` | Country (BIC) | `authority_mult -0.10` | `normal_modifier_time` |
| `bic_frontier_success` | Country (BIC) | `unit_offense_mult +0.05` | `very_long_modifier_time` |
| `bic_frontier_failure` | Country (BIC) | `prestige_mult -0.05` | `short_modifier_time` |
| `gbr_india_objective_authority` | Country (GBR) | `authority_mult +0.10` | `normal_modifier_time` |
| `gbr_india_objective_disappointment` | Country (GBR) | `prestige_mult -0.05` | `short_modifier_time` |
| `gbr_india_innovation_bonus` | Country (GBR) | `weekly_innovation_mult +0.05` | `normal_modifier_time` |
| `gbr_india_authority_loss` | Country (GBR) | `authority_mult -0.05` | `short_modifier_time` |
| `gbr_india_reform_prestige` | Country (GBR) | `prestige_mult +0.05`, `authority_mult +0.10` | `normal_modifier_time` |
| `gbr_india_prestige_loss` | Country (GBR) | `prestige_mult -0.10` | `short_modifier_time` |
| `gbr_india_frontier_prestige` | Country (GBR) | `prestige_mult +0.10`, `authority_mult +0.05` | `normal_modifier_time` |
| `bic_unemployment_crisis_active` | Country (BIC) | `construction_efficiency_add +0.15` | While JE active |
| `bic_unemployment_crisis_radicalism` | Country (BIC) | `radicals_mult +0.25`, `loyalists_mult -0.15` | While JE active |
| `bic_great_famine` | State (all BIC states) | `birth_rate_mult -0.15`, `mortality_mult +0.20`, `laborers_mortality_mult +0.10`, `subsistence_throughput +0.10` | 1825 days, decaying |
| `bic_famine_emigration_push` | State (Bengal) | `migration_push_mult +1.0` | 1825 days, decaying |
| `bic_famine_bengali_pull_newyork` | State (New York) | `migration_pull_mult +0.75` | 1825 days, decaying |
| `bic_plantation_output_throttled` | Country (BIC) | `agriculture_throughput_add -0.10` | `normal_modifier_time` |
| `bic_factory_dangerous_conditions` | Country (BIC) | `manufacturing_laborers_mortality_mult +0.10` | `normal_modifier_time` |

---

## Appendix — Key Variables & Flags Reference

| Variable / Flag | Scope | Purpose |
|---|---|---|
| `gbr_imperial_federation_path` | GBR variable (boolean) | Set when player chooses Imperial Federation path |
| `gbr_commonwealth_path` | GBR variable (boolean) | Set when player chooses Commonwealth path |
| `federation_progress_value` | GBR variable (int 0–100) | Tracks Imperial Federation bar progress |
| `gbr_CAN_commonwealth_stage` | GBR variable (int 1–3) | Canada dominion JE stage |
| `gbr_AST_commonwealth_stage` | GBR variable (int 1–3) | Australia dominion JE stage |
| `gbr_SAF_commonwealth_stage` | GBR variable (int 1–3) | South Africa dominion JE stage |
| `gbr_IRE_commonwealth_stage` | GBR variable (int 1–3) | Ireland dominion JE stage (if eligible) |
| `gbr_BIC_commonwealth_stage` | GBR variable (int 1–3) | India dominion JE stage (if eligible) |
| `gbr_CAN_stage2_offered` | GBR variable (boolean) | Guard — prevents stage 2 event re-firing |
| `bic_gbr_ownership_pct` | GBR variable (int 0–100) | Approximated % of BIC GDP owned by GBR |
| `honourable_company_value` | GBR variable (int 0–100) | Honourable Company bar progress (AI BIC only) |
| `invalidate_uneasy_raj` | Global variable (boolean) | Set by governance JE yearly pulse when `honourable_company_value >= 50`; invalidates `je_uneasy_raj` (Sepoy Mutiny system) |
| `gbr_india_active_objective` | GBR variable (int 0–5) | Currently active India objective (0 = none) |
| `gbr_india_objective_cooldown` | GBR variable (timed) | 5-year timed lock between objective cycles |
| `bic_objective_law_enacted` | GBR variable (boolean) | Set when BIC enacts a law during objective window |
| `bic_objective_territory_annexed` | GBR variable (boolean) | Set when BIC annexes during objective window |
| `gbr_socialism_one_empire` | GBR variable (boolean) | Set when GBR picks the socialist hegemony option |
| `bic_famine_counter` | BIC variable (int 0–5) | Counts consecutive years unemployment > 3%; famine fires at 5 |
| `bic_famine_struck` | BIC variable (boolean) | One-time guard; prevents `je_bic_unemployment_crisis` re-triggering post-famine |

---

## Appendix — Namespace Registry

| Namespace | File | Purpose |
|---|---|---|
| `gbr_path` | `events/gbr_path_events.txt` | Path selection event (gbr_path.1) |
| `gbr_fed_events` | `events/gbr_federation_events.txt` | Imperial Federation bar advance/regression events |
| `gbr_commonwealth_events` | `events/gbr_commonwealth_events.txt` | Commonwealth dominion stage advance events |
| `gbr_india_objectives` | `events/gbr_india_objective_events.txt` | India 5-year objective selection and resolution |
| `spectre` | — | Vanilla namespace; override only, do not create new events in this namespace |
| `bic_challenges` | `events/gbr_bic_challenge_events.txt` | Player-BIC unemployment crisis events and periodic hard choice events |

---

## Appendix — Files to Create or Override

| File path | Action | Contents |
|---|---|---|
| `common/journal_entry_groups/gbr_je_groups.txt` | Create | `je_group_british_empire_affairs` custom group definition |
| `common/journal_entries/gbr_je_federation.txt` | Create | `REPLACE:je_imperial_federation` → `je_progress_to_federation` skeleton |
| `common/journal_entries/gbr_je_commonwealth.txt` | Create | Five dominion JEs (`je_can_commonwealth`, `je_ast_commonwealth`, `je_saf_commonwealth`, `je_ire_commonwealth`, `je_bic_commonwealth`) |
| `common/journal_entries/gbr_je_india.txt` | Create | `REPLACE:je_company_equity` → governance JE |
| `common/scripted_progress_bars/gbr_bars.txt` | Create | `bar_federation_progress`, `bar_honourable_company`, BIC objective progress bars |
| `common/static_modifiers/gbr_modifiers.txt` | Create | All named modifiers listed in Appendix above |
| `events/gbr_path_events.txt` | Create | `gbr_path.1` |
| `events/gbr_federation_events.txt` | Create | Federation bar events (`gbr_fed_events.1`–`.12`) |
| `events/gbr_commonwealth_events.txt` | Create | Commonwealth dominion stage events |
| `events/gbr_india_objective_events.txt` | Create | Objective selection, resolution router, and success/failure events |
| `events/gbr_spectre_overrides.txt` | Create | `REPLACE_OR_CREATE` of "Oppressor and Oppressed" and "A World to Win" |
| `events/gbr_bic_challenge_events.txt` | Create | `bic_challenges` namespace — unemployment crisis events (`.1`–`.3`) and periodic hard choice pool (`.10`–`.14`) |
| `common/journal_entries/gbr_je_bic_challenges.txt` | Create | `je_bic_unemployment_crisis` JE |
| `common/on_actions/gbr_on_actions.txt` | Create | `on_game_start` hook for `gbr_path.1`; `on_law_enactment_started` and `on_country_annexed` hooks for BIC tracking |
| `localization/english/gbr_l_english.yml` | Create | All new loc keys — see Appendix: Localization for full file content |
| `events/RB_imperial_events.txt` | Retire `imperial_events.1` | Namespace kept for `imperial_events.2` (formation event) — `imperial_events.3` is also retired (no timeout on new JE) |
| `events/canada_australia_events.txt` | Modify `can_aus.6`, `can_aus.8` | Add federation bar advance (+15 each) when `gbr_imperial_federation_path` is set on GBR |
| `events/RB_bic_content.txt` | Retire `bic_content.2`, `bic_content.3` | Keep `bic_content.1` (JE intro); delete `.2` and `.3` after verifying no other script references them |
| `common/scripted_effects/imperial_fed_effects.txt` | REMOVE | `imperial_federation_calculate_shared_laws` no longer used |
| `common/journal_entries/04_sepoy_mutiny.txt` | No change needed | `je_uneasy_raj` already uses `invalidate_uneasy_raj` as its invalid condition — the governance JE manages this variable directly |
| `common/subject_types/gbr_subject_types.txt` | Create | `subject_type_commonwealth_member` — new subject type for Stage 3 Commonwealth dominions |
| `common/diplomatic_actions/altys_commonwealth_member.txt` | Create | `altys_commonwealth_member` — custom diplomatic action for the Commonwealth Member subject type |

---

## Appendix — Custom JE Group Definition

All British Empire flavour JEs use a single custom group. Define it in `common/journal_entry_groups/gbr_je_groups.txt`.

```
# common/journal_entry_groups/gbr_je_groups.txt

je_group_british_empire_affairs = {
    # Implementer: verify the fields available for je_group definitions in vanilla
    # common/journal_entry_groups/ — copy structure from an existing vanilla group file.
    # At minimum, a group definition requires a name loc key.
}
```

**Loc key:** `je_group_british_empire_affairs` → *"British Empire Affairs"* (or equivalent)

JEs using this group:
- `je_imperial_federation` (federation path)
- `je_can_commonwealth`, `je_ast_commonwealth`, `je_saf_commonwealth`, `je_ire_commonwealth`, `je_bic_commonwealth` (commonwealth path)
- `je_company_equity` (governance of India, key preserved via REPLACE)

---

## Appendix — Commonwealth Member Subject Type

Defined in `common/subject_types/gbr_subject_types.txt`. Applied via `change_subject_type = subject_type_commonwealth_member` when a dominion's Commonwealth JE reaches Stage 3.

**Design intent:**
- No fees paid to overlord (like protectorate — `autonomy_level = 3`)
- Subject country can be a great power (`great_power` in `valid_subject_ranks`)
- Overlord retains law enforcement rights (like dominion/puppet/colony)
- GUI icon matches personal union (`diplomatic_action = personal_union`)

```
# common/subject_types/gbr_subject_types.txt

subject_type_commonwealth_member = {
    allow_change_country_flag = yes
    use_overlord_map_color = no             # Commonwealth members keep their own map colour
    use_overlord_ruler = no
    annex_on_country_formation = no
    can_start_own_diplomatic_plays = yes
    breaks_if_subject_not_protected = no
    join_overlord_wars = yes
    can_have_subjects = yes
    overlord_must_be_higher_rank = no       # No rank requirement — equals
    overlord_must_be_same_country_type = no
    use_for_release_country = no
    gives_prestige_to_overlord = yes

    diplomatic_action = altys_commonwealth_member   # Custom action — see Appendix for full definition

    autonomy_level = 3                      # Protectorate-level autonomy — no overlord fees
    category = same_as_personal_union

    # Implementer: verify the exact property for "overlord can enforce laws".
    # In vanilla, this is believed to be: overlord_can_enact_laws = yes
    # Check common/subject_types/ vanilla files for the correct field name.
    overlord_can_enact_laws = yes

    valid_overlord_country_types = {
        recognized
    }

    valid_subject_country_types = {
        recognized
    }

    valid_overlord_ranks = {
        great_power
        major_power
    }

    valid_subject_ranks = {
        great_power             # Allows subject to remain or become a great power
        major_power
        minor_power
        insignificant_power
    }

    ai_value = {
        value = 1.5
    }
}
```

> **Implementer notes:**
> - `autonomy_level = 3` gives protectorate-tier autonomy which in vanilla corresponds to zero tribute fees. Verify this holds in the modded build by checking `common/subject_types/00_subject_types.txt` for the vanilla protectorate definition.
> - The `overlord_can_enact_laws` field name is inferred from context — verify the exact property name against the vanilla subject type files before finalising.
> - `diplomatic_action = altys_commonwealth_member` references a fully custom diplomatic action (see Appendix — Commonwealth Member Diplomatic Action). This action uses `texture = personal_union.dds` for the personal union icon while carrying none of the personal union break-on-republic mechanics. It also carries `income_transfer = 0` ensuring no tribute flows to GBR.
> - The `same_autonomy_subject_type_alternatives` block is intentionally omitted — Commonwealth Members cannot be downgraded to another same-autonomy type through normal diplomacy.

---

## Appendix — Commonwealth Member Diplomatic Action

Defined in `common/diplomatic_actions/altys_commonwealth_member.txt`. Referenced by `subject_type_commonwealth_member` via its `diplomatic_action` field. This action is never available through normal diplomatic plays — it is applied exclusively by script (`change_subject_type`).

**Design intent:**
- No income transfer (equal partners pay no tribute)
- Personal union GUI icon via `texture` field
- No monarchy requirement — avoids the vanilla personal union break-on-republic mechanic
- Subject receives a modest charter bonus reflecting continued market integration

```
# common/diplomatic_actions/altys_commonwealth_member.txt

altys_commonwealth_member = {
    groups = {
        general    # for breaking only
    }
    show_in_lens = no

    texture = "gfx/interface/icons/diplomatic_action_icons/personal_union.dds"

    potential = {    # Only ever set through script (change_subject_type)
        always = no
    }

    pact = {
        cost = 0

        has_junior_participant = yes
        maintenance_paid_by = first_country
        income_transfer = 0                             # No tribute — equal partners
        second_country_gets_income_transfer = no
        income_transfer_based_on_second_country = yes

        relations_progress_per_day = 5
        relations_improvement_max = 100                 # Higher ceiling — warm relationship

        subject_type = subject_type_commonwealth_member

        second_modifier = {
            country_free_charters_add = 1               # Subject retains access to Empire market infrastructure
        }

        actor_can_break = {
            is_diplomatic_play_committed_participant = no
        }

        target_can_break = {    # Must use diplomatic play to declare independence
            always = no
        }

        manual_break_effect = {
            create_bidirectional_truce = { country = scope:target_country months = 60 }
        }

        auto_break_effect = {
            create_bidirectional_truce = { country = scope:target_country months = 60 }
        }
    }

    ai = {
        will_break = {
            always = no
        }
    }
}
```

> **Implementer notes:**
> - The `texture` path `personal_union.dds` must be verified against the actual file present in `gfx/interface/icons/diplomatic_action_icons/`. Check that the file exists in vanilla before using; fall back to `protectorate.dds` or `dominion.dds` if not.
> - `relations_improvement_max = 100` is raised above the vanilla 50 to reflect the warm, equal-partner nature of the Commonwealth relationship.
> - `second_modifier` gives the subject `country_free_charters_add = 1`. This is intentionally lower than the dominion's +2, since Commonwealth Members are more autonomous and the relationship is less extractive. Adjust based on playtesting.
> - `maintenance_paid_by = first_country` follows vanilla convention (overlord pays maintenance for the pact). This should not cause GBR to pay tribute to the subject — `income_transfer = 0` already zeroes that out.

---

## Appendix — Localization

**File:** `localization/english/gbr_l_english.yml`
**Encoding:** UTF-8 with BOM.
**Load order note:** Keys defined here that share a name with keys in `RB_imperial_l_english.yml` (e.g. `je_imperial_federation_reason`) will override the RB file if `gbr_l_english.yml` loads after it. This is intentional — the JE content has changed and the old reason/lobby text no longer fits.

**Commonwealth event numbering scheme** (used in loc and referenced in Section 3):
- `gbr_commonwealth_events.1`–`.5` = Stage 1→2 for CAN, AST, SAF, IRE, BIC respectively
- `gbr_commonwealth_events.10`–`.14` = Stage 2→3 for CAN, AST, SAF, IRE, BIC respectively

```yaml
l_english:

 ###############################################
 # JE Group
 ###############################################

 je_group_british_empire_affairs: "British Empire Affairs"

 ###############################################
 # Subject Type & Diplomatic Action
 ###############################################

 subject_type_commonwealth_member: "Commonwealth Member"

 altys_commonwealth_member: "Commonwealth Membership"
 altys_commonwealth_member_desc: "A formal arrangement of equal partnership within the British Commonwealth of Nations. The member state retains full sovereignty over its internal affairs while remaining bound to the Crown by ties of kinship, commerce, and shared destiny."

 ###############################################
 # Progress Bar Labels
 ###############################################

 BAR_FEDERATION_PROGRESS: "Federation Progress"
 BAR_FEDERATION_LEFT: "Division"
 BAR_FEDERATION_RIGHT: "Unity"

 BAR_HONOURABLE_COMPANY: "The Honourable Company"
 BAR_HC_LEFT: "Misrule"
 BAR_HC_RIGHT: "Exemplary Administration"

 ###############################################
 # Tooltip Keys
 ###############################################

 federation_progress_complete_tt: "The dominions' sentiment for federation must reach 100 before the Imperial Federation can be proclaimed."

 ###############################################
 # Section 1 — Path Selection (gbr_path)
 ###############################################

 gbr_path.1.t: "The Shape of Empire"

 gbr_path.1.d: "The sun never sets upon the British Empire — or so they say in the halls of Westminster and in the drawing rooms of a hundred colonial governors. Across the vast expanse of sea and continent, the dominions are bound to the mother country by ties of loyalty, commerce, and history.\n\nYet the empire is changing. The dominions grow in population, wealth, and confidence. Colonial statesmen speak with increasing boldness in their own parliaments. The question is no longer whether these peoples will demand a greater voice, but what form that voice shall take."

 gbr_path.1.f: "From the frozen shores of [SCOPE.sCountry('can_scope').GetName] to the sun-baked plains of [SCOPE.sCountry('aus_scope').GetName], from the minarets of [SCOPE.sCountry('raj_scope').GetName] to the Cape of Good Hope — [ROOT.GetCountry.GetName] governs one quarter of the world's surface. Shall we draw the empire tighter, binding the dominions into one Federal crown? Or shall we loosen the bonds, trusting that partnership and common purpose shall prove stronger than any constitution?"

 gbr_path.1.a:0 "Forge a Federal Empire"
 gbr_path.1.b:0 "Build a Commonwealth of Nations"

 ###############################################
 # Section 2 — Imperial Federation
 # (Updated keys that override RB_imperial_l_english.yml)
 ###############################################

 je_imperial_federation: "An Imperial Federation"

 je_imperial_federation_reason: "Across the world the dominions and colonies of the [ROOT.GetCountry.GetAdjective] Empire stretch across continents and oceans, bound by loyalty to the Crown and a shared heritage. Now, inspired by a growing spirit of imperial unity, voices throughout the empire have begun calling for something greater: a federation of the Crown's global dominions.\n\nFrom Ottawa to Sydney and from Cape Town to Calcutta, advocates argue that the empire must evolve into a closer political union if it is to endure in an age of rising nations. Conferences are held, tariffs negotiated, and armies drilled together — but the great question of formal union remains unanswered.\n\n@information! The federation can only be proclaimed once the sentiment of the dominions reaches a sufficient pitch — and once the idea of pan-national identity has taken hold in [ROOT.GetCountry.GetAdjective] political life."

 je_imperial_federation_lobby: "The vast #bold [ROOT.GetCountry.GetAdjective] Empire#! spans continents but lacks true political unity. As global tensions rise and rival powers consolidate, the vision of binding its dominions into a single federation grows ever more urgent."

 ###############################################
 # Federation Bar Events (gbr_fed_events)
 ###############################################

 gbr_fed_events.1.t: "The Imperial Colonial Conference"
 gbr_fed_events.1.d: "Delegates from Britain and the dominions have gathered in London for the latest Colonial Conference. Over weeks of deliberation, statesmen from Canada, Australia, and South Africa have hammered out protocols on imperial defence, trade, and postal communications. Sentiment for closer union is palpable in the corridors."
 gbr_fed_events.1.f: "The conference closes with no binding resolution — federation, as ever, remains a matter for the future. Yet the very act of gathering breeds familiarity, and familiarity breeds trust."
 gbr_fed_events.1.a:0 "Progress, however slow, is still progress."

 gbr_fed_events.2.t: "The Imperial Penny Post"
 gbr_fed_events.2.d: "A new postal arrangement has been agreed across the empire, fixing the price of a letter between any two imperial territories at a single penny stamp. From London to Sydney, from Cape Town to Quebec, the same coin carries a message halfway around the world."
 gbr_fed_events.2.f: "Critics call it a trifle. The advocates of imperial federation call it something more: the first true common institution of empire, a thread binding dominion to dominion as surely as any constitution."
 gbr_fed_events.2.a:0 "A small step — but steps matter."

 gbr_fed_events.3.t: "Imperial Manoeuvres"
 gbr_fed_events.3.d: "British, Canadian, and Australian military units have conducted joint exercises on the plains of Canada. Officers from three continents drilled together, shared tactics, and learned the same bugle calls. The experiment has been judged a considerable success."
 gbr_fed_events.3.f: "Soldiers who train together tend to fight together. Whether in Imperial Federation or Commonwealth, the bonds forged here may prove sturdier than any paper union."
 gbr_fed_events.3.a:0 "A united defence is the beginning of a united empire."

 gbr_fed_events.4.t: "The Imperial Preference Agreement"
 gbr_fed_events.4.d: "After extended negotiations in Westminster and the colonial capitals, a framework for imperial preferential tariffs has been agreed. Goods moving between Britain and the dominions shall enjoy reduced customs duties, creating in effect a single internal market of empire."
 gbr_fed_events.4.f: "Commerce is the sinew of empire. The factories of Birmingham and the farms of Ontario are now bound by something older and stronger than sentiment: profit."
 gbr_fed_events.4.a:0 "A common market is the foundation of a common polity."

 gbr_fed_events.5.t: "A Voice for Federation"
 gbr_fed_events.5.d: "A prominent colonial statesman has made a landmark speech calling for closer union between Britain and the dominions. The address, reported verbatim in the imperial press, has reinvigorated public discussion of federal union on both sides of the Atlantic — and on the far side of the Pacific."
 gbr_fed_events.5.f: "Words are not constitutions. But words spoken by men of authority have a habit of becoming law."
 gbr_fed_events.5.a:0 "History is made by those bold enough to demand it."

 gbr_fed_events.6.t: "The Dominion Referendum"
 gbr_fed_events.6.d: "A popular referendum held in one of the dominions has returned a majority in favour of closer union with Britain. The result is non-binding — formal federation requires an act of parliament in London — but it signals clearly that the people of the dominions are prepared to move forward."
 gbr_fed_events.6.f: "Mandates do not guarantee success. But they silence those who claim the people are not ready."
 gbr_fed_events.6.a:0 "The people have spoken. Now we must act."

 gbr_fed_events.10.t: "Voices of Dissent"
 gbr_fed_events.10.d: "Reports from the dominions describe growing resentment toward the centralising tendencies of Westminster. Colonial newspapers accuse London of treating the dominions as provinces to be managed rather than partners to be consulted. Liberty sentiment in one of the major dominions has reached a fever pitch."
 gbr_fed_events.10.f: "Empires built on compulsion do not endure. The architects of federation must answer not only how to govern the dominions, but why those dominions should consent to be governed."
 gbr_fed_events.10.a:0 "A setback. We must do better."

 gbr_fed_events.11.t: "Scandal in the Colonies"
 gbr_fed_events.11.d: "A colonial administrator has been implicated in serious misconduct — the details are suppressed from the public press but widely known in Whitehall. The affair has given ammunition to those who argue that imperial federation would simply entrench corruption across a wider stage."
 gbr_fed_events.11.f: "Men of empire are not immune to the failings of men. The federation project suffers for it."
 gbr_fed_events.11.a:0 "An embarrassment we shall have to weather."

 gbr_fed_events.12.t: "The Envoy Refused"
 gbr_fed_events.12.d: "An envoy dispatched to discuss the terms of closer union has been received with conspicuous coldness. The colonial government has declined to participate in the imperial federation talks, citing concerns over parliamentary sovereignty and the erosion of self-government."
 gbr_fed_events.12.f: "Federation by consent requires that both parties consent. Today, at least, that consent is withheld."
 gbr_fed_events.12.a:0 "A frank rebuke. We must rebuild trust first."

 ###############################################
 # Section 3 — Commonwealth JEs
 ###############################################

 # --- Canada ---
 je_can_commonwealth: "The Canadian Partnership"
 je_can_commonwealth_reason: "[ROOT.GetCountry.GetName] and [SCOPE.sCountry('can_scope').GetName] share a common history of British settlement, a border with the restless republic to the south, and the vast northern wilderness that has shaped both peoples. The ties between them are old and deep — but ties can fray if they are not tended.\n\nAs the dominion grows in population and confidence, the relationship between mother country and colony must evolve into something more equal, more durable, and more genuinely mutual."
 je_can_commonwealth_lobby: "#bold [SCOPE.sCountry('can_scope').GetName]#! stands as the eldest of the [ROOT.GetCountry.GetAdjective] dominions. How the relationship with Canada develops will set the pattern for the entire Commonwealth project."
 je_can_commonwealth_stage1_desc: "[SCOPE.sCountry('can_scope').GetName] stands as [ROOT.GetCountry.GetName]'s most loyal dominion — a vast country of British and French settlers bound to the Crown by tradition, trade, and treaty. The relationship is close, though the terms remain decidedly unequal."
 je_can_commonwealth_stage2_desc: "The partnership between [ROOT.GetCountry.GetName] and [SCOPE.sCountry('can_scope').GetName] has deepened. Canadian ministers now sit alongside British counterparts at imperial conferences, and the dominion exercises growing autonomy over its own affairs while remaining a cornerstone of the empire."
 je_can_commonwealth_stage3_desc: "[SCOPE.sCountry('can_scope').GetName] has become a true equal partner within the British Commonwealth — governing herself in all domestic matters, maintaining warm ties of kinship and commerce with [ROOT.GetCountry.GetName], and taking her place beside the mother country as an independent voice in world affairs."

 # --- Australia ---
 je_ast_commonwealth: "The Australian Partnership"
 je_ast_commonwealth_reason: "Half a world away across the Southern Ocean, [SCOPE.sCountry('aus_scope').GetName] has grown from a collection of penal settlements into a prosperous, self-governing dominion. The distance has bred self-reliance; the self-reliance has bred ambition.\n\nAustralia's place within the empire is not in question — but what kind of place it shall be is a matter the current generation must decide."
 je_ast_commonwealth_lobby: "Separated from [ROOT.GetCountry.GetName] by the longest sea-lane in the empire, #bold [SCOPE.sCountry('aus_scope').GetName]#! charts an increasingly independent course."
 je_ast_commonwealth_stage1_desc: "[SCOPE.sCountry('aus_scope').GetName] remains a loyal part of the [ROOT.GetCountry.GetAdjective] Empire, though the great distance of the Southern Ocean and the confidence of her people give the dominion a distinctly independent character."
 je_ast_commonwealth_stage2_desc: "The relationship between [ROOT.GetCountry.GetName] and [SCOPE.sCountry('aus_scope').GetName] has matured. Australian statesmen negotiate as partners rather than petitioners, and the dominion exercises meaningful influence over the policies that govern her."
 je_ast_commonwealth_stage3_desc: "[SCOPE.sCountry('aus_scope').GetName] stands today as a full equal within the British Commonwealth — a Pacific power in her own right, bound to the mother country by choice rather than by circumstance."

 # --- South Africa ---
 je_saf_commonwealth: "The South African Partnership"
 je_saf_commonwealth_reason: "[SCOPE.sCountry('saf_scope').GetName] is the most complex of the [ROOT.GetCountry.GetAdjective] dominions — a land where Briton and Boer, settler and indigenous population, must somehow share a single future. The ties to London are real but strained; the wounds of recent conflict have not fully healed.\n\nBuilding a genuine partnership here will require patience, generosity, and a willingness on Britain's part to make concessions she has not always offered."
 je_saf_commonwealth_lobby: "The most complicated of the [ROOT.GetCountry.GetAdjective] dominions, #bold [SCOPE.sCountry('saf_scope').GetName]#! requires careful cultivation if it is to remain willingly within the Commonwealth."
 je_saf_commonwealth_stage1_desc: "[SCOPE.sCountry('saf_scope').GetName] maintains its ties to the [ROOT.GetCountry.GetAdjective] Empire, though the legacy of conflict and the diversity of its peoples make the relationship more complicated than in other dominions."
 je_saf_commonwealth_stage2_desc: "A more equal footing has been established between [ROOT.GetCountry.GetName] and [SCOPE.sCountry('saf_scope').GetName]. The dominion's various communities have found in Commonwealth partnership a framework that protects them without demanding uniformity."
 je_saf_commonwealth_stage3_desc: "[SCOPE.sCountry('saf_scope').GetName] has found its own voice within the Commonwealth — a nation of many peoples, bound to Britain not by conquest but by a freely chosen fellowship of nations."

 # --- Ireland ---
 je_ire_commonwealth: "The Irish Question"
 je_ire_commonwealth_reason: "The relationship between [ROOT.GetCountry.GetName] and Ireland is the oldest wound in the empire — centuries of conquest, rebellion, famine, and remembered grievance. That Ireland remains within the imperial structure at all is testament to the pragmatic politics of men who have found accommodation more profitable than separation.\n\nWhether the Commonwealth path can transform that accommodation into genuine partnership is the central question of the [ROOT.GetCountry.GetAdjective]-Irish relationship."
 je_ire_commonwealth_lobby: "Ireland's place within the [ROOT.GetCountry.GetAdjective] Empire has always been contested. The Commonwealth offers a framework where the old wound may begin, at last, to heal."
 je_ire_commonwealth_stage1_desc: "Ireland remains part of the [ROOT.GetCountry.GetAdjective] Empire, though the relationship is freighted with centuries of difficult history. A wary peace holds — for now."
 je_ire_commonwealth_stage2_desc: "A more equitable footing has been found between [ROOT.GetCountry.GetName] and Ireland. The recognition of Irish interests as distinct and worthy of respect has done much to ease the historic tensions."
 je_ire_commonwealth_stage3_desc: "Ireland stands today as a willing partner within the British Commonwealth — her autonomy acknowledged, her dignity respected, her ancient grievances at last, perhaps, beginning to recede."

 # --- British India ---
 je_bic_commonwealth: "India Within the Commonwealth"
 je_bic_commonwealth_reason: "India is not a dominion in the ordinary sense — it is an empire within an empire, a subcontinent of hundreds of millions of people, a dozen faiths, and a thousand languages, held together by the machinery of the East India Company and the bayonets of the Indian Army.\n\nThat this vast entity might find a place within a Commonwealth of equal nations is a vision as bold as it is uncertain. The path forward, if it exists at all, will require [ROOT.GetCountry.GetName] to make promises in Delhi that it has never made elsewhere."
 je_bic_commonwealth_lobby: "Whether the great subcontinent can find a dignified place within the [ROOT.GetCountry.GetAdjective] Commonwealth — rather than remaining a possession to be administered — is a question that will define the empire's moral character."
 je_bic_commonwealth_stage1_desc: "India remains governed through the mechanisms of the East India Company, a dependency rather than a partner. The language of Commonwealth has been spoken in London; whether it will be heard in Calcutta and Delhi remains to be seen."
 je_bic_commonwealth_stage2_desc: "Meaningful steps toward partnership have been taken. Indian voices are increasingly heard in the councils of empire, and the relationship between [ROOT.GetCountry.GetName] and the subcontinent has taken on a more genuinely consultative character."
 je_bic_commonwealth_stage3_desc: "India has taken her place as an equal partner within the British Commonwealth — a transformation as profound as any in the history of empire. Whether this partnership endures will be one of the defining questions of the coming century."

 ###############################################
 # Commonwealth Stage Events
 # (.1-.5 = Stage 1→2 per dominion; .10-.14 = Stage 2→3)
 ###############################################

 # --- CAN Stage 1→2 ---
 gbr_commonwealth_events.1.t: "Canada Comes of Age"
 gbr_commonwealth_events.1.d: "[SCOPE.sCountry('dominion_scope').GetName]'s growing prosperity and the confidence of her statesmen have made it increasingly difficult to treat the dominion as a mere dependency of the Crown. The choice now presents itself: acknowledge Canada's maturity and grant her a greater voice in imperial affairs, or maintain the current arrangements and risk driving her toward a cooler independence."
 gbr_commonwealth_events.1.f: "Dominions are not children who must be governed forever. They are peoples who, given the chance, may choose freely to remain [ROOT.GetCountry.GetAdjective] — or may choose something else entirely."
 gbr_commonwealth_events.1.a:0 "Recognise [SCOPE.sCountry('dominion_scope').GetName] as a Partner Nation."
 gbr_commonwealth_events.1.b:0 "Maintain present arrangements — it is too soon."

 # --- AST Stage 1→2 ---
 gbr_commonwealth_events.2.t: "Australia Asserts Herself"
 gbr_commonwealth_events.2.d: "The statesmen of [SCOPE.sCountry('dominion_scope').GetName] have made clear that they expect a greater voice in the decisions that govern the empire — especially those that affect the Pacific. They do not demand independence, but they will no longer accept being governed from the other side of the world without consultation."
 gbr_commonwealth_events.2.f: "Distance and prosperity have made Australians a self-reliant people. London must decide whether to acknowledge this or risk a cooler relationship with the dominion that guards [ROOT.GetCountry.GetAdjective] interests in the Pacific."
 gbr_commonwealth_events.2.a:0 "Grant [SCOPE.sCountry('dominion_scope').GetName] greater standing within the empire."
 gbr_commonwealth_events.2.b:0 "Defer the question for the present."

 # --- SAF Stage 1→2 ---
 gbr_commonwealth_events.3.t: "South Africa at the Crossroads"
 gbr_commonwealth_events.3.d: "In [SCOPE.sCountry('dominion_scope').GetName], a new generation of statesmen — Briton and Boer alike — is demanding that the dominion be treated as a genuine partner rather than a territory administered from London. The wounds of the recent past are still raw; the question of how much trust to extend is a delicate one."
 gbr_commonwealth_events.3.f: "There are two ways to hold a complicated country. You may hold it by force, and breed resentment for generations. Or you may hold it by trust, and make of your former enemies your firmest partners."
 gbr_commonwealth_events.3.a:0 "Extend genuine partnership to [SCOPE.sCountry('dominion_scope').GetName]."
 gbr_commonwealth_events.3.b:0 "The situation requires continued close oversight."

 # --- IRE Stage 1→2 ---
 gbr_commonwealth_events.4.t: "An Olive Branch to Ireland"
 gbr_commonwealth_events.4.d: "An opportunity has presented itself to deepen the relationship between [ROOT.GetCountry.GetName] and Ireland on genuinely equal terms. Irish political leaders have signalled a willingness to engage with a more genuine partnership, provided that London is prepared to make meaningful concessions on the question of self-governance."
 gbr_commonwealth_events.4.f: "Every generation of [ROOT.GetCountry.GetAdjective] statesmen has had to decide anew what Ireland is to Britain. This generation faces the same choice — and the same possibility of getting it right."
 gbr_commonwealth_events.4.a:0 "Accept the terms. Grant Ireland genuine partnership."
 gbr_commonwealth_events.4.b:0 "This is not the right moment for concessions."

 # --- BIC Stage 1→2 ---
 gbr_commonwealth_events.5.t: "A Question for India"
 gbr_commonwealth_events.5.d: "Prominent voices from the educated classes of [SCOPE.sCountry('raj_scope').GetName] have begun, with growing confidence, to articulate the demand for a meaningful Indian role in the governance of the subcontinent. They do not yet speak of independence — but they speak of partnership, of representation, of dignity. Whether [ROOT.GetCountry.GetName] is prepared to listen is now the question."
 gbr_commonwealth_events.5.f: "A hundred million educated men and women asking to be partners rather than subjects is not a request that can be refused forever. The only question is whether [ROOT.GetCountry.GetName] grants it generously, or surrenders it reluctantly."
 gbr_commonwealth_events.5.a:0 "Acknowledge the Indian claim to greater partnership."
 gbr_commonwealth_events.5.b:0 "The subcontinent is not ready for a greater voice."

 # --- CAN Stage 2→3 ---
 gbr_commonwealth_events.10.t: "Equal Partners at Last"
 gbr_commonwealth_events.10.d: "[SCOPE.sCountry('dominion_scope').GetName] has grown into a nation of remarkable maturity — a recognised power in her own right, with a foreign policy, an army, and a people who have proved themselves in every trial the century has offered. The question is now whether [ROOT.GetCountry.GetName] will affirm what is already practically true: that Canada stands alongside Britain as an equal within the Commonwealth."
 gbr_commonwealth_events.10.f: "There is a point at which refusing to name what already exists becomes a source of resentment, not strength. [ROOT.GetCountry.GetName] has always governed best when it was honest about what it was doing."
 gbr_commonwealth_events.10.a:0 "Affirm [SCOPE.sCountry('dominion_scope').GetName] as an Equal Partner."
 gbr_commonwealth_events.10.b:0 "The current arrangements serve us well enough. Defer the question."

 # --- AST Stage 2→3 ---
 gbr_commonwealth_events.11.t: "Australia, Equal Among Nations"
 gbr_commonwealth_events.11.d: "[SCOPE.sCountry('dominion_scope').GetName] has long governed herself in practice. She raises her own revenue, fields her own army, conducts her own trade, and maintains her own relations with the powers of Asia and the Pacific. The formal recognition of her equal status within the Commonwealth is now the final step."
 gbr_commonwealth_events.11.f: "The empire has always been more than the sum of its territories. It has been an idea. Recognising Australia as an equal is not a weakening of that idea — it is its fulfilment."
 gbr_commonwealth_events.11.a:0 "Affirm [SCOPE.sCountry('dominion_scope').GetName] as an Equal Partner."
 gbr_commonwealth_events.11.b:0 "Equal status must be earned through further cooperation."

 # --- SAF Stage 2→3 ---
 gbr_commonwealth_events.12.t: "South Africa, a Nation Forged"
 gbr_commonwealth_events.12.d: "Out of conquest and conflict, [SCOPE.sCountry('dominion_scope').GetName] has built something extraordinary — a nation of many peoples, holding together by choice rather than compulsion. The Commonwealth framework has given this unlikely nation room to grow. Recognising it as a full equal would be the crowning act of that process."
 gbr_commonwealth_events.12.f: "Some nations are made by geography, some by ethnicity, and some by the shared experience of building something from almost nothing. South Africa belongs to the last category."
 gbr_commonwealth_events.12.a:0 "Affirm [SCOPE.sCountry('dominion_scope').GetName] as an Equal Partner."
 gbr_commonwealth_events.12.b:0 "The relationship requires further consolidation first."

 # --- IRE Stage 2→3 ---
 gbr_commonwealth_events.13.t: "Ireland, Freely Joined"
 gbr_commonwealth_events.13.d: "The history between [ROOT.GetCountry.GetName] and Ireland is not easily forgotten. But the generation now governing in Dublin has demonstrated, through consistent cooperation within the Commonwealth framework, that a genuinely voluntary partnership is possible. The decision before [ROOT.GetCountry.GetName] is whether to seal that partnership formally and finally."
 gbr_commonwealth_events.13.f: "It took centuries to make the problem. It will not be solved in a generation. But this is, perhaps, the closest [ROOT.GetCountry.GetName] and Ireland have come to peace on equal terms."
 gbr_commonwealth_events.13.a:0 "Affirm Ireland as an Equal Partner within the Commonwealth."
 gbr_commonwealth_events.13.b:0 "The process requires more time before we can take this step."

 # --- BIC Stage 2→3 ---
 gbr_commonwealth_events.14.t: "India's Hour"
 gbr_commonwealth_events.14.d: "The subcontinent has moved, slowly but inexorably, toward the moment when the claim of its people to equal partnership can no longer be deferred. Indian statesmen, educated in [ROOT.GetCountry.GetAdjective] universities, are demanding not charity but equity. Recognising India as an equal within the Commonwealth would be the most consequential act of the entire imperial project."
 gbr_commonwealth_events.14.f: "An empire that can transform itself into a partnership of free peoples is something the world has not yet seen. [ROOT.GetCountry.GetName] has the chance — if it chooses — to be the first."
 gbr_commonwealth_events.14.a:0 "Affirm India's equal place within the Commonwealth."
 gbr_commonwealth_events.14.b:0 "The question must be deferred — the time is not yet right."

 ###############################################
 # Section 4 — Governance of India
 ###############################################

 # je_company_equity REPLACE — updated title, reason, lobby
 je_company_equity: "The Governance of India"

 je_company_equity_reason: "The [SCOPE.sCountry('raj_scope').GetName] is the greatest single prize of the [ROOT.GetCountry.GetAdjective] Empire — a subcontinent of hundreds of millions of people, vast agricultural wealth, and strategic importance unmatched anywhere on earth. Governing it well is a responsibility and a challenge that no generation of [ROOT.GetCountry.GetAdjective] statesmen has fully met.\n\nThe choice of how to administer India — through Company rule or direct Crown governance, through exploitation or development, through force or consent — will determine not only India's future but [ROOT.GetCountry.GetName]'s place in history.\n\n@information! Every five years the India Office will issue a strategic directive for [SCOPE.sCountry('raj_scope').GetName]. The success or failure of these objectives determines both India's economic trajectory and the stability of [ROOT.GetCountry.GetAdjective] rule."

 je_company_equity_lobby: "The governance of #bold [SCOPE.sCountry('raj_scope').GetName]#! — the jewel of the [ROOT.GetCountry.GetAdjective] Empire — demands constant attention. A well-administered India strengthens the empire; a neglected one breeds the conditions for revolt."

 # India Objective Selection Event
 gbr_india_objectives.1.t: "Directives for the Raj"
 gbr_india_objectives.1.d: "The India Office requires a strategic directive for the coming five years. With the vast resources of the subcontinent at [ROOT.GetCountry.GetAdjective] disposal, the question is how best to deploy them for the benefit of empire and the governance of India's hundreds of millions."
 gbr_india_objectives.1.f: "India is the jewel in the crown — but jewels must be properly set, and settings must be maintained."
 gbr_india_objectives.1.a:0 "Plantation Expansion — expand cultivation across the river deltas."
 gbr_india_objectives.1.b:0 "Resource Extraction — prioritise coal, iron, and timber."
 gbr_india_objectives.1.c:0 "Industrialisation Mandate — build the factories India needs."
 gbr_india_objectives.1.e:0 "Administrative Reform — modernise the apparatus of governance."
 gbr_india_objectives.1.f:0 "Frontier Expansion — advance the bounds of [ROOT.GetCountry.GetAdjective] India."

 # Resolution Router (hidden — only needs a dismiss key)
 gbr_india_objectives.9.a:0 "Noted."

 # Objective Success Events
 gbr_india_objectives.10.t: "The Plantations Flourish"
 gbr_india_objectives.10.d: "Under the mandate set five years ago, the plantations of India have expanded substantially. New fields of indigo, cotton, and tea cover the hillsides and river deltas of Bengal and Assam. The exports pour into [ROOT.GetCountry.GetAdjective] markets, and the revenues of the Raj climb accordingly."
 gbr_india_objectives.10.f: "The subcontinent bends its back. The empire benefits. The arrangement endures — for now."
 gbr_india_objectives.10.a:0 "Excellent progress. Continue the work."

 gbr_india_objectives.11.t: "The Mines Run Deep"
 gbr_india_objectives.11.d: "The five-year extraction directive has borne fruit. New mines and logging operations have opened across the subcontinent, and the flow of coal, iron, and timber into the imperial supply chain has increased substantially."
 gbr_india_objectives.11.f: "India's subsurface riches are vast. Whether they are inexhaustible is a question for another generation."
 gbr_india_objectives.11.a:0 "A sound investment in imperial capacity."

 gbr_india_objectives.12.t: "Industry Takes Hold"
 gbr_india_objectives.12.d: "The factories mandated five years ago have been built, and India's industrial base has grown. The mills of Bombay and the workshops of Bengal now contribute meaningfully to both local employment and imperial revenues."
 gbr_india_objectives.12.f: "Industrialising India is not merely good policy — it is the only way an empire of this size can be governed sustainably in the long run."
 gbr_india_objectives.12.a:0 "A promising foundation for the future."

 gbr_india_objectives.13.t: "Reform Enacted"
 gbr_india_objectives.13.d: "The administrative reforms directed five years ago have been carried through. The machinery of [ROOT.GetCountry.GetAdjective] governance in India has been modernised, rationalised, and — in several important respects — made more responsive to the needs of those it governs."
 gbr_india_objectives.13.f: "Good governance is not glamorous. But it is the difference between an empire that lasts and one that collapses under the weight of its own contradictions."
 gbr_india_objectives.13.a:0 "A sound and necessary achievement."

 gbr_india_objectives.14.t: "The Frontier Advanced"
 gbr_india_objectives.14.d: "The frontier directive has been carried out. [ROOT.GetCountry.GetAdjective] India has extended its reach, consolidating territory and establishing the security of the empire's north-west and eastern borders."
 gbr_india_objectives.14.f: "Frontiers are never truly secure — they are merely further away. But further away is better than close."
 gbr_india_objectives.14.a:0 "The empire is larger and more secure. For now."

 # Objective Failure Events
 gbr_india_objectives.15.t: "The Plantations Fall Short"
 gbr_india_objectives.15.d: "Despite the directives from the India Office, the plantation expansion targets have not been met. Land disputes, poor harvests, and resistance from local zamindars have frustrated efforts to bring new acreage under cultivation within the five-year window."
 gbr_india_objectives.15.f: "India does not always do what London tells it to. It is worth remembering this before issuing the next set of instructions."
 gbr_india_objectives.15.a:0 "A disappointment. Recalibrate the approach."

 gbr_india_objectives.16.t: "The Mines Lag"
 gbr_india_objectives.16.d: "The extraction targets set five years ago have not been reached. Difficult terrain, logistical failures, and a shortage of trained engineers have all taken their toll. The empire's supply chains will feel the shortfall."
 gbr_india_objectives.16.f: "India is not easily exploited by those who do not understand it. The India Office should acquire more of the former."
 gbr_india_objectives.16.a:0 "A failure we will need to account for."

 gbr_india_objectives.17.t: "Industry Stalls"
 gbr_india_objectives.17.d: "The industrial construction mandate has not been fulfilled. Capital did not flow where it was directed; local conditions proved less favourable than the planners assumed; the mills that were promised remain unbuilt."
 gbr_india_objectives.17.f: "Building an industrial base takes more than a directive. It takes investment, patience, and understanding — none of which were supplied in sufficient quantity."
 gbr_india_objectives.17.a:0 "A setback. The work must continue nonetheless."

 gbr_india_objectives.18.t: "Reforms Delayed"
 gbr_india_objectives.18.d: "The administrative reforms directed five years ago have stalled. Bureaucratic resistance, vested interests, and the sheer complexity of governing a subcontinent of this size have conspired to prevent meaningful change."
 gbr_india_objectives.18.f: "Reform in India has been promised many times. The promise matters less than the follow-through."
 gbr_india_objectives.18.a:0 "The opportunity was there. It was not seized."

 gbr_india_objectives.19.t: "The Frontier Holds"
 gbr_india_objectives.19.d: "The frontier directive has not produced the expansion anticipated. Resistance was stiffer than expected, the terrain less forgiving, and the political complications greater than the planners had modelled. The frontiers of [ROOT.GetCountry.GetAdjective] India remain where they were."
 gbr_india_objectives.19.f: "Not every frontier advance is possible. Knowing when not to push is as important as knowing when to push."
 gbr_india_objectives.19.a:0 "Hold the current line. Prepare for the next opportunity."

 ###############################################
 # Section 5A — BIC Unemployment Crisis
 ###############################################

 je_bic_unemployment_crisis: "Unemployment in India"

 je_bic_unemployment_crisis_reason: "The streets of Calcutta, Bombay, and Dacca are swelling with the idle. Workers displaced from fields and workshops wander the cities in search of livelihood, unable to find employment in industries that have not yet been built. The mills cannot absorb them fast enough, and the situation grows more precarious with each passing year.\n\nIf the crisis is not resolved — if new industries are not built, new employment not created — the idle will become the hungry, and the hungry will become something far more dangerous.\n\n@information! If BIC's unemployment rate remains above 3% for #bold five consecutive years#!, a famine will break out across the subcontinent."

 je_bic_unemployment_crisis_lobby: "The unemployed masses of [ROOT.GetCountry.GetName]'s India idle in the cities. Build industries to absorb them — or face the consequences."

 # Unemployment Crisis Intro Event
 bic_challenges.1.t: "An Unemployment Crisis"
 bic_challenges.1.d: "The situation in [ROOT.GetCountry.GetName]'s Indian territories has reached a critical point. Unemployment is rampant in the cities — former agricultural workers who have left the land find no place for themselves in the limited urban economy. The administrators report that without intervention, social order cannot be maintained indefinitely."
 bic_challenges.1.f: "There is a simple rule of empires: when people cannot work, they grow restless. And when they starve, they burn."
 bic_challenges.1.a:0 "We must build our way out of this."

 # Crisis Resolution Event
 bic_challenges.2.t: "The Crisis Resolves"
 bic_challenges.2.d: "Through a determined programme of construction and investment, India's unemployed masses have found work. The streets are quieter, the granaries fuller, and the threat of famine has retreated. The crisis that threatened to destabilise [ROOT.GetCountry.GetAdjective] rule in India has been averted — at considerable effort."
 bic_challenges.2.f: "An empire that can absorb its surplus population into productive labour is an empire that endures. For now, at least, [ROOT.GetCountry.GetName] has proved itself capable of the task."
 bic_challenges.2.a:0 "A difficult chapter closed. Do not allow it to reopen."

 # Famine Event
 bic_challenges.3.t: "Famine Grips India"
 bic_challenges.3.d: "The long crisis of unemployment has broken at last into outright catastrophe. Harvests have failed across Bengal. Granaries emptied by years of neglect stand hollow against the weight of hunger. The roads out of the worst-affected districts are filled with the desperate and the dying, whole communities dissolving as families board any ship that will carry them — to New York, to London, to anywhere but here.\n\nThe world is watching. History is recording. [ROOT.GetCountry.GetName] must now live with what its governance of India has produced."
 bic_challenges.3.f: "Famines are not natural disasters. They are the consequence of policy — or the absence of it."
 bic_challenges.3.a:0 "We must face what we have allowed to come to pass."

 ###############################################
 # Section 5B — Periodic Hard Choice Events
 ###############################################

 bic_challenges.10.t: "The Factory Question"
 bic_challenges.10.d: "A dispute has broken out between British plantation owners and the administrators of India's growing factory sector. The planters insist their labour quotas must be met regardless of the conditions required in the factories. The factory managers warn that without relief, workers will not survive to fill the mills next season."
 bic_challenges.10.f: "India's wealth is built on labour. The only question is whose labour — and at what price to those who provide it."
 bic_challenges.10.a:0 "Ease the plantation quotas — the people cannot bear both."
 bic_challenges.10.b:0 "Maintain the quotas — the factories must keep pace."

 bic_challenges.11.t: "Tax Collection Disputes"
 bic_challenges.11.d: "The tax collectors of three Bengal districts have reported systematic resistance from local landowners refusing to pay their assessments. The collectors request authority to enforce collection by force. The district officers warn that force will inflame a situation that is already volatile."
 bic_challenges.11.f: "Revenue makes empire possible. But empires that tax too harshly discover, in time, that they have made their own undoing."
 bic_challenges.11.a:0 "Accept reduced revenue — ease enforcement this season."
 bic_challenges.11.b:0 "Crack down. The law must be enforced without exception."

 bic_challenges.12.t: "The Sahib's Salary"
 bic_challenges.12.d: "The Indian Civil Service is discontented. [ROOT.GetCountry.GetAdjective] administrators posted to India earn substantially less in real terms than their counterparts at home, while managing a far larger and more complex territory. A delegation of senior civil servants has formally petitioned for salary increases sufficient to attract and retain men of quality."
 bic_challenges.12.f: "[ROOT.GetCountry.GetName] governs India through men. Those men must be paid adequately, or they will govern it badly — or not at all."
 bic_challenges.12.a:0 "Raise the salaries — quality governance requires quality administrators."
 bic_challenges.12.b:0 "Reduce the British presence — govern through local administrators instead."

 bic_challenges.13.t: "The Opium Trade Controversy"
 bic_challenges.13.d: "Pressure is mounting from church groups, from a vocal faction in Parliament, and from China through diplomatic channels for [ROOT.GetCountry.GetName] to curtail or end the export of Indian opium. The trade is enormously profitable and deeply integrated into Bengal's plantation economy. But the diplomatic and reputational costs are mounting."
 bic_challenges.13.f: "Empire has always rested on commerce. Not all commerce bears close examination. The question is how much examination [ROOT.GetCountry.GetName] is prepared to endure."
 bic_challenges.13.a:0 "Continue the trade — commerce must not yield to sentiment."
 bic_challenges.13.b:0 "Restrict the trade — the costs outweigh the revenues."

 bic_challenges.14.t: "The Sepoy Recruitment Drive"
 bic_challenges.14.d: "The Commander-in-Chief of India has requested authority to expand the Indian Army through a major recruitment drive drawing from agricultural communities across the subcontinent. The expansion will draw men away from the fields at harvest time, disrupting local food production — but the security situation, the General insists, demands it."
 bic_challenges.14.f: "The sword that guards the Raj must be kept sharp. The price of sharpness falls, as it always has, on those who till the earth."
 bic_challenges.14.a:0 "Approve the recruitment — security must come first."
 bic_challenges.14.b:0 "Decline — the agricultural sector cannot bear the disruption."

 ###############################################
 # Section 6 — The Socialist Option
 ###############################################

 spectre.X.gbr:0 "Socialism under one Empire"
 spectre.X.gbr_desc: "As the global hegemon, [ROOT.GetCountry.GetName] stands as the only power capable of bringing revolution to the whole of this world. We will gladly fulfil this duty. The instruments of capital are already gathered in our hands — it remains only to place them in the hands of the people."

 spectre.Y.gbr:0 "Initiate General Order One"
 spectre.Y.gbr_desc: "As the dominant power of the world, [ROOT.GetCountry.GetName] shall not merely witness the transformation of history — she shall direct it. The General Order goes out to every corner of empire: the instruments of capital shall be placed under the common ownership of the people of the world."

 ###############################################
 # Modifier Display Names
 # (Key name = display name shown in tooltip)
 ###############################################

 # Commonwealth GBR Modifiers
 gbr_commonwealth_stage1_gbr: "Loyal Dominion"
 gbr_commonwealth_stage2_gbr: "Partner Nation"
 gbr_commonwealth_stage3_gbr: "Equal Partners of Empire"

 # Commonwealth Dominion Modifiers
 gbr_commonwealth_stage1_dominion: "Commonwealth Partnership"
 gbr_commonwealth_stage2_dominion: "Greater Autonomy"
 gbr_commonwealth_stage3_dominion: "Equal Partnership"

 # Penalty Modifier
 gbr_oversight_maintained_penalty: "Restricted Autonomy"

 # India — BIC AI Bonus
 bic_ai_administration_bonus: "Honourable Company Administration"

 # India — Imperial Dividend
 bic_imperial_dividend: "Imperial Dividend"

 # India — Objective Active Modifiers
 bic_reform_mandate_active: "Reform Mandate"
 bic_frontier_mandate_active: "Frontier Directive"
 gbr_frontier_infamy_buffer: "Imperial Warrant"

 # India — Objective Outcome Modifiers (BIC)
 bic_plantation_success: "Plantation Prosperity"
 bic_plantation_failure: "Plantation Shortfall"
 bic_extraction_success: "Extraction Boom"
 bic_extraction_failure: "Extraction Shortfall"
 bic_industry_success: "Industrial Progress"
 bic_industry_failure: "Industrial Stagnation"
 bic_reform_success: "Administrative Reforms Enacted"
 bic_reform_failure: "Reform Opportunity Missed"
 bic_frontier_success: "Frontier Expanded"
 bic_frontier_failure: "Frontier Stalled"

 # India — Objective Outcome Modifiers (GBR)
 gbr_india_objective_authority: "Imperial Authority Affirmed"
 gbr_india_objective_disappointment: "Imperial Disappointment"
 gbr_india_innovation_bonus: "Imperial Innovation Stimulus"
 gbr_india_authority_loss: "Loss of Imperial Authority"
 gbr_india_reform_prestige: "Prestige of Reform"
 gbr_india_prestige_loss: "Loss of Imperial Prestige"
 gbr_india_frontier_prestige: "Frontier Prestige"

 # BIC Challenge Modifiers
 bic_unemployment_crisis_active: "Unemployment Emergency"
 bic_unemployment_crisis_radicalism: "Social Unrest"
 bic_great_famine: "The Great Famine"
 bic_famine_emigration_push: "Famine Flight"
 bic_famine_bengali_pull_newyork: "New World Beckons"
 bic_plantation_output_throttled: "Plantation Quotas Eased"
 bic_factory_dangerous_conditions: "Dangerous Working Conditions"
```

> **Implementer note on key conflicts:** `spectre.X.gbr` and `spectre.Y.gbr` use a non-standard format for event option keys because the vanilla event IDs `spectre.X` and `spectre.Y` are placeholders — the implementer must substitute the verified vanilla IDs before these keys will resolve. The option loc key pattern is `[event_id].[suffix]` where the suffix is defined in the option's `name` field.

> **Implementer note on JE status descriptions:** Keys like `je_can_commonwealth_stage1_desc` are referenced inside `triggered_desc = { desc = key }` blocks in the JE's `status_desc` block. They are plain descriptive strings, not event loc format — no `:0` suffix needed.
