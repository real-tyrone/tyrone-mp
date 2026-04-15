# British Empire Flavour — Mod Design Document

**Purpose:** This document is a complete design specification for a Victoria 3 mod adding flavour to Britain (GBR) and her subjects. It is intended to be consumed by an LLM assisting in scripting, and should be treated as the authoritative source of truth for feature intent, scope, and mechanical logic. It does not contain implementation code — that is produced separately using the SKILL files.

---

## Table of Contents

1. The British Question (Path Selection)
2. Path A — Imperial Federation
3. Path B — The British Commonwealth
4. Governance of India (JE)
5. The Socialist Option (GB Communist Event Override)

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
| `localization/english/RB_imperial_l_english.yml` | All keys | EXTEND — add new loc keys; keep all existing loc |

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
    icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds
    country_authority_mult = 0.05
    country_prestige_mult = 0.05
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
    icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds
    country_prestige_mult = 0.10
    country_influence_mult = 0.05
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

GBR modifiers (Stage 3):
```
gbr_commonwealth_stage3_gbr = {
    icon = gfx/interface/icons/timed_modifier_icons/modifier_statue_positive.dds
    country_prestige_mult = 0.15
    country_influence_mult = 0.10
    country_authority_mult = 0.05
}
```

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
    political_movement_pop_attraction_mult = 0.15
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

## 5. The Socialist Option (GB Communist Event Override)

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
| `gbr_commonwealth_stage1_gbr` | Country (GBR) | `authority_mult +0.05`, `prestige_mult +0.05` | Permanent until stage changes |
| `gbr_commonwealth_stage1_dominion` | Country (Dominion) | `law_enactment_success_add +0.05`, `authority_mult +0.05` | Permanent until stage changes |
| `gbr_commonwealth_stage2_gbr` | Country (GBR) | `prestige_mult +0.10`, `influence_mult +0.05` | Permanent until stage changes |
| `gbr_commonwealth_stage2_dominion` | Country (Dominion) | `law_enactment_success_add +0.10`, `authority_mult +0.10`, `innovation_mult +0.05` | Permanent until stage changes |
| `gbr_commonwealth_stage3_gbr` | Country (GBR) | `prestige_mult +0.15`, `influence_mult +0.10`, `authority_mult +0.05` | Permanent until stage changes |
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

---

## Appendix — Namespace Registry

| Namespace | File | Purpose |
|---|---|---|
| `gbr_path` | `events/gbr_path_events.txt` | Path selection event (gbr_path.1) |
| `gbr_fed_events` | `events/gbr_federation_events.txt` | Imperial Federation bar advance/regression events |
| `gbr_commonwealth_events` | `events/gbr_commonwealth_events.txt` | Commonwealth dominion stage advance events |
| `gbr_india_objectives` | `events/gbr_india_objective_events.txt` | India 5-year objective selection and resolution |
| `spectre` | — | Vanilla namespace; override only, do not create new events in this namespace |

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
| `common/on_actions/gbr_on_actions.txt` | Create | `on_game_start` hook for `gbr_path.1`; `on_law_enactment_started` and `on_country_annexed` hooks for BIC tracking |
| `localization/english/gbr_l_english.yml` | Create | All new loc keys |
| `events/RB_imperial_events.txt` | Retire `imperial_events.1` | Namespace kept for `imperial_events.2` (formation event) — `imperial_events.3` is also retired (no timeout on new JE) |
| `events/canada_australia_events.txt` | Modify `can_aus.6`, `can_aus.8` | Add federation bar advance (+15 each) when `gbr_imperial_federation_path` is set on GBR |
| `events/RB_bic_content.txt` | Retire `bic_content.2`, `bic_content.3` | Keep `bic_content.1` (JE intro); delete `.2` and `.3` after verifying no other script references them |
| `common/scripted_effects/imperial_fed_effects.txt` | REMOVE | `imperial_federation_calculate_shared_laws` no longer used |
| `common/journal_entries/04_sepoy_mutiny.txt` | No change needed | `je_uneasy_raj` already uses `invalidate_uneasy_raj` as its invalid condition — the governance JE manages this variable directly |

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
