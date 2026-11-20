# imperial law reform complete law registry coverage

264 effective laws; 27 law groups. Every row is requestable when Qing holds it. Automatic dispatch: all 15 administrations. Native manual interactions remain available; the court docket is retired. No law/group whitelist.

Legality is country- and time-dependent. Requestable does not mean enactable. Imperial adoption uses native law_is_available to retain technology, conflicting-law and custom restrictions while waiving political support. Gradual implementation blocks new enactments for 12 calendar months, then activates the law; instant adoption activates it immediately. This report records exact source restrictions, not a fabricated verdict for an unspecified save. An incompatible request stays blocked and permits petition/refusal. No unsupported laws are intentionally omitted.

Native manual exposure requires a can_impose definition; the court selector covers every law whether or not that native button exists. Runtime event ordering, native legality and actual save/load remain unverified. Only game/common/laws and this mod are included; other enabled mods require regeneration against their effective load order.

## law_chi_early_modernization (ID 49)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 is_china_tag_trigger = yes
 custom_tooltip = {
  text = tyr_army_modernization_required_tt
  has_variable = chi_early_army_early_law_unlocked
 }
 custom_tooltip = {
  text = tyr_self_strengthening_required_tt
  has_variable = tyr_ssm_started
 }
}
```

## law_chi_mass_conscription (ID 53)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 enlistment_offices
}
is_visible = {
 is_china_tag_trigger = yes
}
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 is_china_tag_trigger = yes
 custom_tooltip = {
  text = tyr_army_modernization_required_tt
  has_variable = chi_early_army_early_law_unlocked
 }
 custom_tooltip = {
  text = tyr_self_strengthening_required_tt
  has_variable = tyr_ssm_started
 }
 NOT = {
  has_law_or_variant = law_type:law_peasant_levies
 }
}
```

## law_chi_mintuan (ID 55)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 AND = {
  is_china_tag_trigger = yes
  NOT = {
   has_law_or_variant = law_type:law_monarchy
   has_law_or_variant = law_type:law_theocracy
  }
 }
}
can_enact = {
 OR = {
  has_law_or_variant = law_type:law_presidential_republic
  has_law_or_variant = law_type:law_parliamentary_republic
  has_law_or_variant = law_type:law_corporate_state
  has_law_or_variant = law_type:law_council_republic
 }
}
```

## law_chi_national_militia (ID 58)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 is_china_tag_trigger = yes
 custom_tooltip = {
  text = tyr_army_modernization_required_tt
  has_variable = chi_early_army_militia_law_unlocked
 }
 custom_tooltip = {
  text = tyr_self_strengthening_required_tt
  has_variable = tyr_ssm_started
 }
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_military_treaty_organization
   }
  }
 }
}
```

## law_chi_peoples_liberation_army (ID 63)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_revolutionary_army_variants.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 is_china_tag_trigger = yes
 custom_tooltip = {
  text = tyr_army_modernization_required_tt
  OR = {
   has_variable = chi_early_army_early_law_unlocked
   has_variable = chi_early_army_militia_law_unlocked
  }
 }
 custom_tooltip = {
  text = tyr_self_strengthening_required_tt
  has_variable = tyr_ssm_started
 }
}
unlocking_technologies = {
 enlistment_offices
}
```

## law_chi_tuanlian (ID 70)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
 NOT = {
  has_law = law_type:law_chi_mintuan
 }
 OR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_theocracy
 }
}
can_enact = {
 is_china_tag_trigger = yes
 OR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_theocracy
 }
}
```

## law_india_company_army (ID 123)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 general_staff
}
disallowing_laws = {
 law_strict_edo_system
 law_intermediate_edo_system
}
```

## law_india_company_corps (ID 126)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
```

## law_india_early_standing_army (ID 136)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 military_drill
}
disallowing_laws = {
 law_strict_edo_system
 law_intermediate_edo_system
}
```

## law_india_great_indian_army (ID 139)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 enlistment_offices
}
disallowing_laws = {
 law_strict_edo_system
 law_intermediate_edo_system
}
```

## law_india_peoples_army (ID 154)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_revolutionary_army_variants.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 enlistment_offices
}
```

## law_india_princely_garrison (ID 156)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
```

## law_mass_conscription (ID 177)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
unlocking_technologies = {
 enlistment_offices
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
```

## law_national_militia (ID 187)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 mandatory_service
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
can_enact = {
 NOT = {
  is_india_tag_trigger = yes
 }
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_military_treaty_organization
   }
  }
 }
}
```

## law_peasant_levies (ID 208)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
  c:JAP ?= this
 }
}
```

## law_professional_army (ID 215)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
unlocking_technologies = {
 military_drill
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
```

## law_qing_banner_army (ID 222)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 is_china_tag_trigger = yes
 country_has_monarchy_law = yes
}
```

## law_revolutionary_guard (ID 228)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 enlistment_offices
}
```

## law_warrior_caste (ID 258)

Group: `lawgroup_army_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_army_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 country_has_primary_culture = cu:japanese
}
```

## law_appointed_bureaucrats (ID 10)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
```

## law_chartered_appointed_bureaucrats (ID 21)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
}
is_visible = {
 is_india_tag_trigger = yes
}
```

## law_chartered_elected_bureaucrats (ID 25)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
disallowing_laws = {
 law_company_exploitation
 law_chartered_no_schools
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 NOT = {
  is_involved_in_journal_entry = je_uneasy_raj
 }
}
```

## law_chartered_hereditary_bureaucrats (ID 26)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
is_visible = {
 is_india_tag_trigger = yes
}
disallowing_laws = {
 law_council_republic
}
```

## law_chi_cadres (ID 44)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 has_law_or_variant = law_type:law_council_republic
}
```

## law_chi_purchaseof_office (ID 64)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
disallowing_laws = {
 law_traditionalism
 law_chi_industry_banned
 law_multicultural
 law_cultural_exclusion
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
}
```

## law_chi_republic_corruption (ID 67)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 AND = {
  is_china_tag_trigger = yes
  NOR = {
   has_law_or_variant = law_type:law_monarchy
   has_law_or_variant = law_type:law_theocracy
   has_law_or_variant = law_type:law_social_monarchy
  }
 }
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 NOR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_theocracy
  has_law_or_variant = law_type:law_social_monarchy
 }
}
disallowing_laws = {
 law_multicultural
 law_cultural_exclusion
}
```

## law_chi_state_directorate (ID 68)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 central_planning
}
is_visible = {
 is_china_tag_trigger = yes
 OR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_social_monarchy
  has_law_or_variant = law_type:law_presidential_republic
  has_law_or_variant = law_type:law_parliamentary_republic
 }
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 has_technology_researched = central_planning
 OR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_social_monarchy
  has_law_or_variant = law_type:law_presidential_republic
  has_law_or_variant = law_type:law_parliamentary_republic
 }
}
```

## law_chi_yinpriv (ID 72)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
 OR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_theocracy
  has_law_or_variant = law_type:law_social_monarchy
 }
}
disallowing_laws = {
 law_multicultural
 law_cultural_exclusion
 law_racial_segregation
 law_national_supremacy
 law_ethnostate
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 OR = {
  has_law_or_variant = law_type:law_monarchy
  has_law_or_variant = law_type:law_theocracy
 }
}
```

## law_communal_administration (ID 85)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 socialism
}
```

## law_crownland_diets (ID 93)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 OR = {
  c:AUS ?= this
  AND = {
   exists = c:AUS
   is_subject_of = c:AUS
  }
 }
}
disallowing_laws = {
 law_council_republic
}
```

## law_elected_bureaucrats (ID 99)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 country_has_voting_franchise = yes
}
```

## law_hereditary_bureaucrats (ID 112)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOR = {
  is_india_tag_trigger = yes
  c:AUS ?= this
  is_china_tag_trigger = yes
  AND = {
   exists = c:AUS
   is_subject_of = c:AUS
  }
 }
}
disallowing_laws = {
 law_council_republic
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 NOT = {
  is_china_tag_trigger = yes
 }
}
```

## law_imperial_federal_bureaucracy (ID 117)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\altys_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 OR = {
  always = no
  has_modifier = imperial_federation_modifier
 }
}
```

## law_india_communal_administration (ID 122)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 has_law_or_variant = law_type:law_council_republic
}
can_enact = {
 is_india_tag_trigger = yes
 has_law_or_variant = law_type:law_council_republic
}
```

## law_india_company_directorate (ID 127)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_india_company_directorate
  is_enacting_law = law_type:law_india_company_directorate
  has_variable = tyrone_sc_directorate_chosen
 }
}
can_enact = {
 custom_tooltip = {
  text = tyrone_sc_directorate_chosen_tt
  has_variable = tyrone_sc_directorate_chosen
 }
}
```

## law_india_company_governors (ID 129)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_india_company_governors
  is_enacting_law = law_type:law_india_company_governors
  has_variable = tyrone_sc_governors_chosen
 }
}
can_enact = {
 custom_tooltip = {
  text = tyrone_sc_governors_chosen_tt
  has_variable = tyrone_sc_governors_chosen
 }
}
```

## law_india_crown_administration (ID 132)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_india_crown_administration
  is_enacting_law = law_type:law_india_crown_administration
  is_involved_in_journal_entry = je_tyrone_csr_crown_path
  is_involved_in_journal_entry = je_tyrone_jewel_of_the_empire
 }
}
disallowing_laws = {
 law_company_exploitation
 law_chartered_no_schools
}
```

## law_india_federal_administration (ID 137)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_civil_service = yes
 country_has_voting_franchise = yes
 is_subject = no
}
disallowing_laws = {
 law_company_exploitation
 law_chartered_no_schools
}
```

## law_india_federal_secretariats (ID 138)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_india_federal_secretariats
  is_enacting_law = law_type:law_india_federal_secretariats
  has_variable = tyrone_nim_federal_chosen
 }
}
can_enact = {
 custom_tooltip = {
  text = tyrone_nim_federal_chosen_tt
  has_variable = tyrone_nim_federal_chosen
 }
}
```

## law_india_imperial_provincial_administration (ID 145)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_india_imperial_provincial_administration
  is_enacting_law = law_type:law_india_imperial_provincial_administration
  has_variable = tyrone_eoi_civil_done
 }
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_eoi_civil_unlocked_tt
  has_variable = tyrone_eoi_civil_done
 }
}
```

## law_india_national_secretariat (ID 152)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_india_national_secretariat
  is_enacting_law = law_type:law_india_national_secretariat
  has_variable = tyrone_nim_central_chosen
 }
}
can_enact = {
 custom_tooltip = {
  text = tyrone_nim_central_chosen_tt
  has_variable = tyrone_nim_central_chosen
 }
}
```

## law_military_bureaucrats (ID 182)

Group: `lawgroup_bureaucracy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_bureaucracy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_affirmative_action (ID 5)

Group: `lawgroup_caste_hegemony`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_caste_hegemony.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {

}
```

## law_hindu_caste_codified (ID 113)

Group: `lawgroup_caste_hegemony`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_hindu_caste_enforced (ID 114)

Group: `lawgroup_caste_hegemony`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_hindu_caste_not_enforced (ID 115)

Group: `lawgroup_caste_hegemony`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_child_labor_allowed (ID 75)

Group: `lawgroup_childrens_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_childrens_rights.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_compulsory_primary_school (ID 87)

Group: `lawgroup_childrens_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_childrens_rights.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_no_schools
 law_terakoya
}
unlocking_technologies = {
 human_rights
}
```

## law_restricted_child_labor (ID 227)

Group: `lawgroup_childrens_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_childrens_rights.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 labor_movement
}
```

## law_caesaropapism (ID 13)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 OR = {
  c:RUS ?= this
  AND = {
   exists = c:RUS
   is_subject_of = c:RUS
   country_is_subject_type_valid_for_caesaropapism = yes
  }
 }
 NOT = {
  has_law_or_variant = law_type:law_theocracy
 }
}
```

## law_chi_confucius (ID 47)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {

}
```

## law_freedom_of_conscience (ID 106)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
unlocking_technologies = {
 rationalism
}
disallowing_laws = {
 law_theocracy
}
```

## law_india_colonial_religious_neutrality (ID 120)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_theocracy
}
can_enact = {
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_religious
   }
  }
 }
}
```

## law_india_hindu_favored (ID 141)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_theocracy
}
can_enact = {
 NOT = {
  is_involved_in_journal_entry = je_uneasy_raj
 }
 OR = {
  has_variable = has_done_homerule_var
  has_variable = tyrone_eoi_council_done
 }
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_religious
   }
  }
 }
}
```

## law_india_muslim_favored (ID 151)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_theocracy
}
can_enact = {
 NOT = {
  is_involved_in_journal_entry = je_uneasy_raj
 }
 OR = {
  has_law = law_type:law_hindu_caste_enforced
  has_law = law_type:law_hindu_caste_codified
 }
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_religious
   }
  }
 }
}
```

## law_india_revolutionary_secularism (ID 157)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 has_variable = tyrone_cp_started
}
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_theocracy
}
can_enact = {
 is_india_tag_trigger = yes
 has_variable = tyrone_cp_started
 ig:ig_devout ?= {
  is_in_government = no
 }
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_religious
   }
  }
 }
}
```

## law_millet_system (ID 183)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 c:TUR ?= this
}
```

## law_people_of_the_book (ID 210)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 country_is_islamic = yes
 NOT = {
  c:TUR ?= this
 }
}
```

## law_state_atheism (ID 241)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_theocracy
}
can_enact = {
 ig:ig_devout ?= {
  is_in_government = no
 }
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_religious
   }
  }
 }
}
```

## law_state_religion (ID 243)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOR = {
  has_law = law_type:law_millet_system
  has_law = law_type:law_people_of_the_book
 }
}
```

## law_total_separation (ID 251)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_church_and_state.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_theocracy
}
can_enact = {
 OR = {
  is_power_bloc_leader = no
  power_bloc ?= {
   NOT = {
    has_identity = identity:identity_religious
   }
  }
 }
}
```

## law_tyr_heavenly_religion (ID 255)

Group: `lawgroup_church_and_state`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_heavenly.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 has_variable = tyr_heavenly_path
}
can_enact = {
 custom_tooltip = {
  text = tyr_heavenly_path_tt
  has_variable = tyr_heavenly_path
 }
}
```

## law_cultural_exclusion (ID 94)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
```

## law_ethnostate (ID 100)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
unlocking_technologies = {
 nationalism
}
```

## law_india_company_citizenship (ID 125)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {

}
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 custom_tooltip = {
  text = tyrone_sc_citizenship_unlocked_tt
  has_variable = tyrone_sc_started
 }
}
```

## law_india_cultural_exclusion (ID 135)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
```

## law_india_imperial_citizenship (ID 142)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_eoi_council_law_unlocked_tt
  has_variable = tyrone_eoi_council_done
 }
}
unlocking_technologies = {
 human_rights
}
```

## law_india_multicultural (ID 150)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 human_rights
}
```

## law_india_national_supremacy (ID 153)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
```

## law_india_subjecthood (ID 159)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
```

## law_multicultural (ID 185)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
unlocking_technologies = {
 human_rights
}
```

## law_national_supremacy (ID 188)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
```

## law_official_nationality (ID 200)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:RUS ?= this
}
```

## law_racial_segregation (ID 223)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
```

## law_subjecthood (ID 245)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_citizenship.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
}
```

## law_tyr_heavenly_covenant (ID 254)

Group: `lawgroup_citizenship`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_heavenly.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 has_variable = tyr_heavenly_path
}
can_enact = {
 custom_tooltip = {
  text = tyr_heavenly_path_tt
  has_variable = tyr_heavenly_path
 }
}
```

## law_colonial_exploitation (ID 79)

Group: `lawgroup_colonization`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_colonial_affairs.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_sakoku
}
unlocking_technologies = {
 colonization
}
```

## law_colonial_resettlement (ID 80)

Group: `lawgroup_colonization`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_colonial_affairs.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_sakoku
}
unlocking_technologies = {
 colonization
}
```

## law_frontier_colonization (ID 107)

Group: `lawgroup_colonization`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_colonial_affairs.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 OR = {
  AND = {
   country_is_colonial_or_company = yes
   any_decentralized_country = {
    is_adjacent_to_country = root
   }
  }
  any_scope_state = {
   is_homeland_of_country_cultures = ROOT
   any_neighbouring_state = {
    owner = {
     is_country_type = decentralized
    }
   }
  }
 }
}
disallowing_laws = {
 law_sakoku
}
unlocking_technologies = {
 colonization
}
```

## law_india_internal_colonization (ID 148)

Group: `lawgroup_colonization`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 colonization
}
```

## law_internal_colonization (ID 163)

Group: `lawgroup_colonization`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_colonial_affairs.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 colonization
}
can_enact = {
 OR = {
  is_country_type = colonial
  any_scope_state = {
   is_incorporated = no
  }
 }
}
```

## law_no_colonial_affairs (ID 191)

Group: `lawgroup_colonization`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_colonial_affairs.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 custom_tooltip = {
  modifier:country_disallow_law_no_colonial_affairs_bool = no
  text = disallow_law_no_colonial_affairs_tt
 }
}
```

## law_anarchy (ID 7)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 anarchism
}
can_enact = {
 has_law_or_variant = law_type:law_council_republic
}
```

## law_ancien_regime (ID 8)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:FRA ?= this
 OR = {
  has_journal_entry = je_house_of_bourbon
  has_modifier = ancien_regime_restored
 }
}
```

## law_autocracy (ID 11)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_parliamentary_republic
}
is_visible = {
 NOR = {
  has_law = law_type:law_neo_absolutism
  has_law = law_type:law_bakufu
 }
}
can_enact = {
 trigger_if = {
  limit = {
   c:BIC ?= ROOT
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   has_variable = britain_granted_dop_permission
  }
 }
}
```

## law_bakufu (ID 12)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:JAP ?= this
 NOT = {
  has_law = law_type:law_autocracy
 }
}
```

## law_census_voting (ID 19)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 democracy
}
disallowing_laws = {
 law_chiefdom
 law_command_economy
}
can_enact = {
 trigger_if = {
  limit = {
   c:BIC ?= ROOT
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   has_variable = britain_granted_dop_permission
  }
 }
}
```

## law_elder_council (ID 98)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_country_type = decentralized
}
```

## law_india_company_technocracy (ID 130)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 central_archives
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_sc_main_unlocked_tt
  has_variable = tyrone_sc_main_done
 }
}
is_visible = {
 is_india_tag_trigger = yes
 has_law = law_type:law_india_company_technocracy
}
```

## law_india_shareholder_voting (ID 158)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 democracy
}
disallowing_laws = {
 law_chiefdom
 law_command_economy
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_sc_main_unlocked_tt
  has_variable = tyrone_sc_main_done
 }
}
is_visible = {
 is_india_tag_trigger = yes
 has_law = law_type:law_india_shareholder_voting
}
```

## law_labour_suffrage (ID 167)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 socialism
}
```

## law_landed_voting (ID 172)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 democracy
}
disallowing_laws = {
 law_chiefdom
 law_command_economy
}
can_enact = {
 trigger_if = {
  limit = {
   c:BIC ?= ROOT
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   has_variable = britain_granted_dop_permission
  }
 }
}
```

## law_neo_absolutism (ID 189)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:AUS ?= this
 has_global_variable = neo_absolutism_victory
}
```

## law_oligarchy (ID 204)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NAND = {
  country_has_primary_culture = cu:romanian
  is_subject = yes
 }
}
can_enact = {
 trigger_if = {
  limit = {
   root = {
    is_india_tag_trigger = yes
   }
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   NOT = {
    root = {
     is_india_tag_trigger = yes
    }
   }
  }
 }
}
```

## law_organic_regulation (ID 205)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 country_has_primary_culture = cu:romanian
 is_subject = yes
}
can_enact = {
 country_has_primary_culture = cu:romanian
 is_subject = yes
}
```

## law_single_party_state (ID 237)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 OR = {
  custom_tooltip = {
   text = ruler_in_party_tt
   exists = ruler
   OR = {
    ruler = {
     this.interest_group ?= {
      has_party = yes
     }
    }
   }
  }
  custom_tooltip = {
   text = sps_no_party_tt
   country_has_voting_franchise = no
  }
 }
 trigger_if = {
  limit = {
   root = {
    is_india_tag_trigger = yes
   }
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   has_variable = britain_granted_dop_permission
  }
 }
}
unlocking_technologies = {
 political_agitation
}
```

## law_technocracy (ID 246)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 central_archives
}
```

## law_universal_suffrage (ID 256)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 egalitarianism
}
disallowing_laws = {
 law_chiefdom
 law_command_economy
}
can_enact = {
 trigger_if = {
  limit = {
   c:BIC ?= ROOT
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   has_variable = britain_granted_dop_permission
  }
 }
}
```

## law_wealth_voting (ID 259)

Group: `lawgroup_distribution_of_power`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\00_distribution_of_power.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 democracy
}
disallowing_laws = {
 law_chiefdom
 law_command_economy
}
can_enact = {
 trigger_if = {
  limit = {
   c:BIC ?= ROOT
   is_subject = yes
   NOT = {
    has_law = scope:law
   }
  }
  custom_tooltip = {
   text = BIC_not_able_to_change_distribution_of_power_tt
   has_variable = britain_granted_dop_permission
  }
 }
}
```

## law_agrarianism (ID 6)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_anarchy
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 romanticism
}
```

## law_chartered_industrialization (ID 28)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_raj_interventionism_unlocked_tt
  OR = {
   has_variable = tyrone_company_self_rule_unlocked
   has_variable = tyrone_unstable_raj_failed
   AND = {
    has_variable = tyrone_raj_nation_done
    has_variable = tyrone_raj_nation_result
    var:tyrone_raj_nation_result = 1
   }
  }
 }
}
disallowing_laws = {
 law_serfdom
 law_anarchy
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 manufacturies
}
```

## law_chartered_land_administration (ID 29)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_raj_agrarianism_unlocked_tt
  OR = {
   has_variable = tyrone_company_self_rule_unlocked
   has_variable = tyrone_unstable_raj_failed
   AND = {
    has_variable = tyrone_raj_nation_done
    has_variable = tyrone_raj_nation_result
    var:tyrone_raj_nation_result = -1
   }
  }
 }
}
disallowing_laws = {
 law_anarchy
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 romanticism
}
```

## law_chi_cooperative_ownership (ID 48)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_women_in_the_fields
}
is_visible = {
 is_china_tag_trigger = yes
}
```

## law_chi_industry_banned (ID 51)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {

}
unlocking_technologies = {
 romanticism
}
```

## law_chi_mixed_economic_policy (ID 56)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
unlocking_technologies = {
 romanticism
}
can_enact = {

}
disallowing_laws = {
 law_serfdom
}
```

## law_chi_national_resources_commission (ID 59)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 NOT = {
  has_law_or_variant = law_type:law_monarchy
 }
}
unlocking_technologies = {
 central_planning
}
```

## law_chi_offical_supervision (ID 61)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
unlocking_technologies = {
 mutual_funds
}
can_enact = {

}
```

## law_command_economy (ID 83)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_anarchy
 law_women_in_the_fields
}
unlocking_technologies = {
 central_planning
}
```

## law_company_exploitation (ID 86)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
disallowing_laws = {
 law_anarchy
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 colonization
}
can_enact = {
 is_subject = yes
 is_india_tag_trigger = yes
}
```

## law_cooperative_ownership (ID 89)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_women_in_the_fields
}
```

## law_extraction_economy (ID 102)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_anarchy
 law_factory_councils
}
unlocking_technologies = {
 colonization
}
disallowing_laws = {
 law_anarchy
 law_women_in_the_fields
}
can_enact = {
 is_subject = yes
}
```

## law_india_command_economy (ID 121)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_anarchy
 law_women_in_the_fields
}
is_visible = {
 is_india_tag_trigger = yes
 NOT = {
  is_china_tag_trigger = yes
 }
}
unlocking_technologies = {

}
can_enact = {
 is_india_tag_trigger = yes
 is_subject = no
 OR = {
  custom_tooltip = {
   text = tyrone_india_command_empire_completed_tt
   has_variable = tyrone_eoi_main_done
  }
  has_law_or_variant = law_type:law_council_republic
  has_law_or_variant = law_type:law_corporate_state
  has_technology_researched = central_planning
 }
}
```

## law_india_cooperative_ownership (ID 131)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 NOT = {
  is_china_tag_trigger = yes
 }
}
disallowing_laws = {
 law_serfdom
 law_women_in_the_fields
}
can_enact = {
 is_india_tag_trigger = yes
 OR = {
  AND = {
   is_subject = no
   has_law_or_variant = law_type:law_council_republic
  }
  custom_tooltip = {
   text = tyrone_india_collective_revolution_won_tt
   has_variable = tyrone_nim_socialist_started
   has_variable = tyrone_nim_civil_war_done
  }
 }
}
```

## law_india_industry_banned (ID 147)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_anarchy
 law_factory_councils
}
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 NOT = {
  has_modifier = modifier_india_company_rule
 }
}
unlocking_technologies = {
 romanticism
}
```

## law_india_laissez_faire (ID 149)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 custom_tooltip = {
  text = tyrone_india_laissez_faire_automatic_tt
  always = no
 }
}
is_visible = {
 is_india_tag_trigger = yes
 NOT = {
  has_law = law_type:law_laissez_faire_plus
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
disallowing_laws = {
 law_serfdom
 law_isolationism
 law_anarchy
 law_guild_system
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 international_trade
}
```

## law_industry_banned (ID 161)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_anarchy
 law_factory_councils
}
unlocking_technologies = {
 romanticism
}
```

## law_interventionism (ID 164)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_anarchy
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 manufacturies
}
```

## law_laissez_faire (ID 168)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_isolationism
 law_anarchy
 law_guild_system
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 international_trade
}
```

## law_laissez_faire_plus (ID 169)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_economy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 has_variable = laissez_faire_expanded_var
}
disallowing_laws = {
 law_serfdom
 law_isolationism
 law_anarchy
 law_guild_system
 law_factory_councils
 law_women_in_the_fields
}
unlocking_technologies = {
 investment_banks
}
```

## law_laissez_faire_subject (ID 170)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_subject = yes
 NOT = {
  is_india_tag_trigger = yes
 }
}
disallowing_laws = {
 law_serfdom
 law_isolationism
 law_anarchy
 law_guild_system
 law_women_in_the_fields
 law_factory_councils
}
unlocking_technologies = {
 international_trade
}
```

## law_neofeudalism (ID 190)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_grappes_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 always = no
}
```

## law_sic_agrarian_reform (ID 235)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 always = no
}
can_enact = {
 always = no
}
```

**Ordinary enactment is unconditionally prohibited by this law's `can_enact = { always = no }` clause.** The request remains possible; acceptance cannot bypass this restriction.

## law_state_capitalism (ID 242)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_economy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_serfdom
 law_anarchy
 law_women_in_the_fields
}
is_visible = {
 NOT = {
  is_india_tag_trigger = yes
 }
 NOT = {
  is_china_tag_trigger = yes
 }
}
unlocking_technologies = {
 mutual_funds
}
```

## law_traditionalism (ID 252)

Group: `lawgroup_economic_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_economic_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_per_capita_based_taxation
 law_proportional_taxation
 law_graduated_taxation
 law_anarchy
 law_factory_councils
}
```

## law_intermediate_edo_system (ID 162)

Group: `lawgroup_edo_social_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_caste_hegemony.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_lax_edo_system (ID 174)

Group: `lawgroup_edo_social_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_caste_hegemony.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_strict_edo_system (ID 244)

Group: `lawgroup_edo_social_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_caste_hegemony.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_chartered_imperial_public_schools (ID 27)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 civilizing_mission
}
disallowing_laws = {
 law_state_religion
 law_serfdom
}
```

## law_chartered_no_schools (ID 31)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
disallowing_laws = {
 law_compulsory_primary_school
}
can_enact = {
 custom_tooltip = {
  modifier:country_disallow_law_no_schools_bool = no
  text = disallow_law_no_schools_tt
 }
}
```

## law_chartered_orientalist_schools (ID 34)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 central_archives
}
disallowing_laws = {
 law_hindu_caste_enforced
 law_hindu_caste_codified
}
```

## law_chartered_private_schools (ID 37)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 identification_documents
}
disallowing_laws = {
 law_state_religion
}
```

## law_chartered_public_schools (ID 39)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 identification_documents
}
disallowing_laws = {
 law_state_religion
 law_serfdom
}
```

## law_chartered_religious_schools (ID 40)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 central_archives
}
disallowing_laws = {
 law_hindu_caste_not_enforced
 law_affirmative_action
}
```

## law_chi_merchent_led (ID 54)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 banking
}
disallowing_laws = {
 law_traditionalism
 law_chi_industry_banned
}
is_visible = {
 is_china_tag_trigger = yes
}
```

## law_chi_no_schools (ID 60)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
disallowing_laws = {
 law_compulsory_primary_school
 law_freedom_of_conscience
 law_total_separation
 law_state_atheism
}
```

## law_chi_religious_focus (ID 65)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
unlocking_technologies = {
 rationalism
}
disallowing_laws = {
 law_total_separation
 law_state_atheism
 law_serfdom
}
```

## law_chi_state_led (ID 69)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
unlocking_technologies = {
 central_archives
}
disallowing_laws = {
 law_traditionalism
 law_chi_confucius
}
can_enact = {

}
```

## law_no_schools (ID 196)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_compulsory_primary_school
}
can_enact = {
 custom_tooltip = {
  modifier:country_disallow_law_no_schools_bool = no
  text = disallow_law_no_schools_tt
 }
}
```

## law_private_schools (ID 214)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 academia
}
disallowing_laws = {
 law_state_religion
}
is_visible = {
 NAND = {
  c:JAP ?= this
  has_law = law_type:law_terakoya
 }
}
```

## law_public_schools (ID 221)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 empiricism
}
disallowing_laws = {
 law_state_religion
 law_serfdom
}
```

## law_religious_schools (ID 226)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 rationalism
}
disallowing_laws = {
 law_total_separation
 law_state_atheism
 law_serfdom
}
```

## law_terakoya (ID 248)

Group: `lawgroup_education_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `game/common\laws\01_education_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 academia
}
is_visible = {
 c:JAP ?= this
 NOT = {
  has_law = law_type:law_private_schools
 }
}
```

## law_censorship (ID 18)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_free_speech.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 NAND = {
  is_china_tag_trigger = yes
  has_law_or_variant = law_type:law_monarchy
 }
}
unlocking_technologies = {
 law_enforcement
}
```

## law_chi_associations_assemble (ID 43)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_free_speech.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 has_law_or_variant = law_type:law_monarchy
}
```

## law_chi_palacememorials (ID 62)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_free_speech.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 has_law_or_variant = law_type:law_monarchy
}
```

## law_outlawed_dissent (ID 206)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_free_speech.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NAND = {
  is_china_tag_trigger = yes
  has_law_or_variant = law_type:law_monarchy
 }
}
unlocking_technologies = {
 political_agitation
}
```

## law_protected_speech (ID 217)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_free_speech.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 human_rights
}
```

## law_right_of_assembly (ID 229)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_free_speech.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NAND = {
  is_china_tag_trigger = yes
  has_law_or_variant = law_type:law_monarchy
 }
}
```

## law_tyr_heavenly_censorship (ID 253)

Group: `lawgroup_free_speech`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_heavenly.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 has_variable = tyr_heavenly_path
}
can_enact = {
 custom_tooltip = {
  text = tyr_heavenly_path_tt
  has_variable = tyr_heavenly_path
 }
}
```

## law_chiefdom (ID 73)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 is_country_type = decentralized
}
is_visible = {
 is_country_type = decentralized
}
```

## law_colonial_administration (ID 78)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_anarchy
}
can_enact = {
 country_is_colonial_or_company = yes
}
is_visible = {
 country_is_colonial_or_company = yes
}
```

## law_corporate_state (ID 90)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 corporatism
}
```

## law_council_republic (ID 92)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 socialism
}
can_enact = {
 trigger_if = {
  limit = {
   is_subject = no
  }
  NOT = {
   has_government_type = gov_chartered_company
  }
 }
 trigger_if = {
  limit = {
   c:POL ?= THIS
  }
  NOT = {
   has_journal_entry = je_congress_poland
  }
 }
 OR = {
  any_political_movement = {
   movement_is_socialist = yes
   political_movement_radicalism > 0.75
  }
  AND = {
   custom_tooltip = {
    text = has_factory_councils_law_or_amendment_tt
    has_factory_councils_law_or_amendment = yes
   }
   custom_tooltip = {
    text = had_proletarian_revolution_tt
    has_global_variable_map = first_proletarian_revolution
   }
  }
 }
}
```

## law_monarchy (ID 184)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  has_law = law_type:law_colonial_administration
 }
}
disallowing_laws = {
 law_anarchy
}
can_enact = {
 trigger_if = {
  limit = {
   is_subject = no
  }
  NOT = {
   has_government_type = gov_chartered_company
  }
 }
}
```

## law_parliamentary_republic (ID 207)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_autocracy
}
can_enact = {
 NOT = {
  has_government_type = gov_chartered_company
 }
}
unlocking_technologies = {
 democracy
}
```

## law_presidential_republic (ID 212)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\00_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 democracy
}
can_enact = {
 trigger_if = {
  limit = {
   is_subject = no
  }
  NOT = {
   has_government_type = gov_chartered_company
  }
 }
 trigger_if = {
  limit = {
   c:POL ?= THIS
  }
  NOT = {
   has_journal_entry = je_congress_poland
  }
 }
}
```

## law_social_monarchy (ID 240)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 corporatism
}
can_enact = {
 trigger_if = {
  limit = {
   is_subject = no
  }
  NOT = {
   has_government_type = gov_chartered_company
  }
 }
}
```

## law_theocracy (ID 249)

Group: `lawgroup_governance_principles`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_governance_principles.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_total_separation
}
can_enact = {
 NOT = {
  has_government_type = gov_chartered_company
 }
}
```

## law_caste_charitable_health_system (ID 15)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
unlocking_technologies = {
 pharmaceuticals
}
```

## law_caste_private_health_insurance (ID 16)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
unlocking_technologies = {
 labor_movement
}
```

## law_caste_public_health_insurance (ID 17)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
unlocking_technologies = {
 civilizing_mission
}
```

## law_charitable_health_system (ID 20)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 medical_degrees
}
```

## law_chartered_charitable_health_system (ID 24)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 pharmaceuticals
}
```

## law_chartered_no_health_system (ID 30)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
```

## law_chartered_private_health_insurance (ID 36)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 labor_movement
}
```

## law_chartered_public_health_insurance (ID 38)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 civilizing_mission
}
```

## law_chi_apothecary (ID 42)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_chi_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_china_tag_trigger = yes
}
```

## law_chi_national_healthcare (ID 57)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_chi_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 pharmaceuticals
}
is_visible = {
 is_china_tag_trigger = yes
}
```

## law_chi_religious_practices (ID 66)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_chi_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 medical_degrees
}
is_visible = {
 is_china_tag_trigger = yes
}
```

## law_chi_urban_healthcare (ID 71)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_chi_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 pharmaceuticals
}
is_visible = {
 is_china_tag_trigger = yes
}
can_enact = {
 NAND = {
  has_law_or_variant = law_type:law_traditionalism
  has_law_or_variant = law_type:law_agrarianism
  has_law_or_variant = law_type:law_industry_banned
 }
}
```

## law_no_health_system (ID 192)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_private_health_insurance (ID 213)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 pharmaceuticals
}
```

## law_public_health_insurance (ID 219)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_health_system.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 pharmaceuticals
}
```

## law_public_health_insurance_bismarck (ID 220)

Group: `lawgroup_health_system`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_bismark.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 has_journal_entry = je_bismarck_reform
}
unlocking_technologies = {
 pharmaceuticals
}
```

## law_india_chartered_manufactures (ID 119)

Group: `lawgroup_india_chartered_obligations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_corporations = yes
 is_india_tag_trigger = yes
}
```

## law_india_crown_industrial_obligations (ID 134)

Group: `lawgroup_india_chartered_obligations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_cr_corporations_unlocked_tt
  has_variable = tyrone_cr_started
 }
}
```

## law_india_guaranteed_railway_companies (ID 140)

Group: `lawgroup_india_chartered_obligations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_corporations = yes
 is_india_tag_trigger = yes
}
```

## law_india_imperial_revenue_guarantees (ID 146)

Group: `lawgroup_india_chartered_obligations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_corporations = yes
 is_india_tag_trigger = yes
}
```

## law_india_plantation_guarantees (ID 155)

Group: `lawgroup_india_chartered_obligations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_corporations = yes
 is_india_tag_trigger = yes
}
```

## law_india_unaided_enterprise (ID 160)

Group: `lawgroup_india_chartered_obligations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 tyrone_cr_can_leave_corporations = yes
 is_india_tag_trigger = yes
}
```

## law_extraordinary_commission (ID 103)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 philosophical_pragmatism
}
```

## law_guaranteed_liberties (ID 110)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_national_guard (ID 186)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 law_enforcement
}
```

## law_no_home_affairs (ID 193)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_okhrana (ID 201)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:RUS ?= this
 country_has_monarchy_law = yes
}
unlocking_technologies = {
 central_archives
}
```

## law_secret_police (ID 232)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NAND = {
  c:RUS ?= this
  country_has_monarchy_law = yes
 }
}
unlocking_technologies = {
 central_archives
}
```

## law_shinsengumi (ID 234)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 law_enforcement
}
is_visible = {
 country_has_primary_culture = cu:japanese
}
```

## law_third_section (ID 250)

Group: `lawgroup_internal_security`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\00_internal_security.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:RUS ?= this
 country_has_monarchy_law = yes
 NAND = {
  has_technology_researched = central_archives
  NOT = {
   has_law = law_type:law_third_section
  }
 }
}
unlocking_technologies = {
 law_enforcement
}
```

## law_india_imperial_factory_inspectorate (ID 143)

Group: `lawgroup_labor_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 labor_movement
}
```

## law_india_imperial_labour_protections (ID 144)

Group: `lawgroup_labor_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 human_rights
}
```

## law_no_workers_rights (ID 199)

Group: `lawgroup_labor_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_labor_rights.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_regulatory_bodies (ID 224)

Group: `lawgroup_labor_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_labor_rights.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 labor_movement
}
```

## law_regulatory_bodies_bismarck (ID 225)

Group: `lawgroup_labor_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_bismark.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 has_journal_entry = je_bismarck_reform
}
unlocking_technologies = {
 labor_movement
}
```

## law_worker_protections (ID 264)

Group: `lawgroup_labor_rights`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_labor_rights.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 human_rights
}
```

## law_anti_strike_laws (ID 9)

Group: `lawgroup_labour_associations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_labour_associations.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_combination_acts (ID 82)

Group: `lawgroup_labour_associations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_labour_associations.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_corporatized_unions (ID 91)

Group: `lawgroup_labour_associations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_labour_associations.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 corporatism
}
can_enact = {
 OR = {
  has_law_or_variant = law_type:law_corporate_state
  has_law_or_variant = law_type:law_social_monarchy
 }
}
```

## law_factory_councils (ID 104)

Group: `lawgroup_labour_associations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_labour_associations.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 socialism
}
can_enact = {
 OR = {
  is_revolutionary = yes
  has_law_or_variant = law_type:law_council_republic
 }
}
```

## law_guild_system (ID 111)

Group: `lawgroup_labour_associations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_labour_associations.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_laissez_faire
}
```

## law_right_to_associate (ID 230)

Group: `lawgroup_labour_associations`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_labour_associations.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_collectivized_agriculture (ID 77)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 socialism
}
```

## law_commercialized_agriculture (ID 84)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_traditionalism
}
unlocking_technologies = {
 mutual_funds
}
```

## law_cultuurstelsel (ID 95)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_grappes_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 always = no
}
```

## law_expanded_latifundias (ID 101)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 any_primary_culture = {
  OR = {
   has_discrimination_trait = language_hispanophone
   has_discrimination_trait = language_lusophone
   has_discrimination_trait = language_italian
  }
 }
 hidden_trigger = {
  has_variable = upgraded_latifundias_law_var
 }
}
can_enact = {
 always = yes
}
disallowing_laws = {
 law_council_republic
}
```

## law_homesteading (ID 116)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 OR = {
  NOT = {
   is_india_tag_trigger = yes
  }
  NOT = {
   active_law:lawgroup_land_reform = {
    has_amendment = amendment_type:amendment_plantation_labor_obligations
   }
  }
 }
}
is_visible = {
 NOT = {
  has_law = law_type:law_peasant_proprietorship
 }
 OR = {
  country_is_colonial_or_company = yes
  capital ?= {
   is_in_geographic_region = geographic_region_new_world
  }
 }
}
```

## law_latifundias (ID 173)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 any_primary_culture = {
  OR = {
   has_discrimination_trait = language_hispanophone
   has_discrimination_trait = language_lusophone
   has_discrimination_trait = language_italian
  }
 }
 hidden_trigger = {
  NOT = {
   has_variable = upgraded_latifundias_law_var
  }
 }
 NOT = {
  has_law = law_type:law_tenant_farmers
 }
}
can_enact = {
 always = yes
}
disallowing_laws = {
 law_council_republic
}
```

## law_manorialism (ID 176)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 OR = {
  c:AUS ?= this
  AND = {
   exists = c:AUS
   is_subject_of = c:AUS
   OR = {
    is_subject_type = subject_type_crown_land
    is_subject_type = subject_type_personal_union
   }
   c:AUS ?= {
    has_law = law_type:law_manorialism
   }
  }
  country_has_primary_culture = cu:romanian
  country_has_primary_culture = cu:polish
 }
}
```

## law_peasant_proprietorship (ID 209)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  has_law = law_type:law_homesteading
 }
 NOT = {
  country_is_colonial_or_company = yes
 }
 capital ?= {
  is_in_geographic_region = geographic_region_old_world
 }
}
```

## law_serfdom (ID 233)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 OR = {
  NOT = {
   is_india_tag_trigger = yes
  }
  NOT = {
   active_law:lawgroup_land_reform = {
    has_amendment = amendment_type:amendment_plantation_labor_obligations
   }
  }
 }
}
is_visible = {
 NOR = {
  c:AUS ?= this
  AND = {
   exists = c:AUS
   is_subject_of = c:AUS
   OR = {
    is_subject_type = subject_type_crown_land
    is_subject_type = subject_type_personal_union
   }
   c:AUS ?= {
    has_law = law_type:law_manorialism
   }
  }
  country_has_primary_culture = cu:romanian
 }
}
disallowing_laws = {
 law_interventionism
 law_laissez_faire
 law_command_economy
}
```

## law_sic_serfdom (ID 236)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_land_reform.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 always = no
}
disallowing_laws = {

}
```

## law_tenant_farmers (ID 247)

Group: `lawgroup_land_reform`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_tenant_farmers.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 OR = {
  NOT = {
   is_india_tag_trigger = yes
  }
  NOT = {
   active_law:lawgroup_land_reform = {
    has_amendment = amendment_type:amendment_plantation_labor_obligations
   }
  }
 }
}
is_visible = {
 NOR = {
  has_law = law_type:law_latifundias
  has_law = law_type:law_expanded_latifundias
 }
}
```

## law_closed_borders (ID 76)

Group: `lawgroup_migration`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_migration.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_migration_controls (ID 180)

Group: `lawgroup_migration`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_migration.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_sakoku
}
```

## law_no_migration_controls (ID 194)

Group: `lawgroup_migration`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_migration.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_sakoku
}
```

## law_chi_coastal_defense_navy (ID 45)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 military_drill
}
is_visible = {
 tyr_ssm_is_chinese_country = yes
}
can_enact = {
 custom_tooltip = {
  text = tyr_ssm_naval_unlock_tt
  OR = {
   NOT = {
    tyr_ssm_is_chinese_country = yes
   }
   has_variable = tyr_ssm_naval_unlocked
  }
 }
}
```

## law_chi_coastal_flotilla (ID 46)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 jeune_ecole
}
is_visible = {
 tyr_ssm_is_chinese_country = yes
}
can_enact = {
 custom_tooltip = {
  text = tyr_ssm_naval_unlock_tt
  OR = {
   NOT = {
    tyr_ssm_is_chinese_country = yes
   }
   has_variable = tyr_ssm_naval_unlocked
  }
 }
}
```

## law_chi_imperial_dockyards (ID 50)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 military_drill
}
is_visible = {
 tyr_ssm_is_chinese_country = yes
}
can_enact = {
 custom_tooltip = {
  text = tyr_ssm_naval_imperial_unlock_tt
  OR = {
   NOT = {
    tyr_ssm_is_chinese_country = yes
   }
   has_variable = tyr_ssm_naval_unlocked
   has_variable = chi_imperial_dockyards_unlocked
  }
 }
}
```

## law_chi_junk_fleet (ID 52)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 tyr_ssm_is_chinese_country = yes
}
```

## law_diplomatic_navy (ID 97)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 military_drill
}
is_visible = {
 AND = {
  tyr_ssm_is_chinese_country = no
  any_scope_state = {
   is_coastal = yes
  }
 }
}
can_enact = {
 custom_tooltip = {
  text = tyr_ssm_naval_unlock_tt
  OR = {
   NOT = {
    tyr_ssm_is_chinese_country = yes
   }
   has_variable = tyr_ssm_naval_unlocked
  }
 }
}
```

## law_jeune_ecole (ID 166)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\00_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 jeune_ecole
}
is_visible = {
 any_scope_state = {
  is_coastal = yes
 }
}
```

## law_merchant_navy (ID 179)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 AND = {
  tyr_ssm_is_chinese_country = no
  any_scope_state = {
   is_coastal = yes
  }
 }
}
```

## law_professional_navy (ID 216)

Group: `lawgroup_navy_model`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_navy_model.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 military_drill
}
is_visible = {
 AND = {
  tyr_ssm_is_chinese_country = no
  any_scope_state = {
   is_coastal = yes
  }
 }
}
can_enact = {
 custom_tooltip = {
  text = tyr_ssm_naval_imperial_unlock_tt
  OR = {
   NOT = {
    tyr_ssm_is_chinese_country = yes
   }
   has_variable = tyr_ssm_naval_unlocked
   has_variable = chi_imperial_dockyards_unlocked
  }
 }
}
```

## law_dedicated_police (ID 2)

Group: `lawgroup_policing`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_police = yes
}
unlocking_technologies = {
 law_enforcement
}
```

## law_india_crown_constabulary (ID 133)

Group: `lawgroup_policing`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 is_india_tag_trigger = yes
 custom_tooltip = {
  text = tyrone_cr_police_unlocked_tt
  has_variable = tyrone_cr_police_done
 }
}
```

## law_local_police (ID 1)

Group: `lawgroup_policing`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_police = yes
}
unlocking_technologies = {
 tech_bureaucracy
}
```

## law_militarized_police (ID 181)

Group: `lawgroup_policing`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\tyrone_policing.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_police = yes
}
unlocking_technologies = {
 political_agitation
}
```

## law_no_police (ID 195)

Group: `lawgroup_policing`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 tyrone_cr_can_leave_police = yes
 custom_tooltip = {
  modifier:country_disallow_law_no_police_bool = no
  text = disallow_law_no_police_tt
 }
}
```

## law_full_womens_rights (ID 108)

Group: `lawgroup_rights_of_women`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\altys_rights_of_women.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 feminism
}
is_visible = {
 country_has_voting_franchise = no
}
can_enact = {
 country_has_voting_franchise = no
}
```

## law_no_womens_rights (ID 198)

Group: `lawgroup_rights_of_women`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_rights_of_women.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  has_law = law_type:law_women_in_the_fields
 }
}
```

## law_women_in_the_fields (ID 260)

Group: `lawgroup_rights_of_women`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_rights_of_women.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:MON ?= this
 NOR = {
  has_law = law_type:law_no_womens_rights
  has_law_or_variant = law_type:law_women_own_property
  has_law_or_variant = law_type:law_women_in_the_workplace
  has_law_or_variant = law_type:law_womens_suffrage
 }
}
disallowing_laws = {

}
```

## law_women_in_the_workplace (ID 261)

Group: `lawgroup_rights_of_women`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_rights_of_women.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 feminism
}
```

## law_women_own_property (ID 262)

Group: `lawgroup_rights_of_women`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_rights_of_women.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_womens_suffrage (ID 263)

Group: `lawgroup_rights_of_women`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_rights_of_women.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 feminism
}
```

## law_colonial_slavery (ID 81)

Group: `lawgroup_slavery`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_slavery.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
can_enact = {
 any_scope_state = {
  is_incorporated = no
 }
}
```

## law_debt_slavery (ID 96)

Group: `lawgroup_slavery`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_slavery.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_multicultural
 law_affirmative_action
}
```

## law_legacy_slavery (ID 175)

Group: `lawgroup_slavery`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_slavery.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_slave_trade (ID 238)

Group: `lawgroup_slavery`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_slavery.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_cultural_exclusion
 law_multicultural
 law_affirmative_action
}
```

## law_slavery_banned (ID 239)

Group: `lawgroup_slavery`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_slavery.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_consumption_based_taxation (ID 88)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_taxation.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_graduated_taxation (ID 109)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_taxation.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_traditionalism
}
unlocking_technologies = {
 socialism
}
```

## law_india_chartered_excise (ID 118)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_variable = tyrone_csr_started
  has_law = law_type:law_india_chartered_excise
  is_enacting_law = law_type:law_india_chartered_excise
 }
}
can_enact = {
 is_india_tag_trigger = yes
}
```

## law_india_company_assessment (ID 124)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
 OR = {
  has_variable = tyrone_csr_started
  has_law = law_type:law_india_company_assessment
  is_enacting_law = law_type:law_india_company_assessment
 }
}
can_enact = {
 is_india_tag_trigger = yes
}
disallowing_laws = {
 law_traditionalism
}
unlocking_technologies = {
 currency_standards
}
```

## law_land_based_taxation (ID 171)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_taxation.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
# No additional conditions declared on this law.
```

## law_per_capita_based_taxation (ID 3)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_taxation.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_traditionalism
}
unlocking_technologies = {
 currency_standards
}
```

## law_proportional_taxation (ID 4)

Group: `lawgroup_taxation`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_taxation.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_traditionalism
}
unlocking_technologies = {
 egalitarianism
}
```

## law_canton_system (ID 14)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_trade_policy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 any_primary_culture = {
  has_discrimination_trait = heritage_han
 }
 any_scope_state = {
  state_region = s:STATE_GUANGDONG
  is_largest_state_in_region = yes
 }
}
```

## law_free_trade (ID 105)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_trade_policy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_command_economy
}
unlocking_technologies = {
 international_trade
}
```

## law_india_company_free_trade (ID 128)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **present**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_command_economy
}
unlocking_technologies = {
 international_trade
}
is_visible = {
 is_india_tag_trigger = yes
}
can_enact = {
 custom_tooltip = {
  text = tyrone_sc_main_unlocked_tt
  has_variable = tyrone_sc_main_done
 }
}
```

## law_isolationism (ID 165)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_trade_policy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
disallowing_laws = {
 law_laissez_faire
}
is_visible = {
 NOR = {
  AND = {
   any_primary_culture = {
    has_discrimination_trait = heritage_han
   }
   any_scope_state = {
    state_region = s:STATE_GUANGDONG
    is_largest_state_in_region = yes
   }
  }
  AND = {
   any_primary_culture = {
    cu:japanese = this
   }
   s:STATE_KYUSHU ?= {
    any_scope_state = {
     owner ?= ROOT
     is_largest_state_in_region = yes
    }
   }
  }
 }
}
```

## law_mercantilism (ID 178)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_trade_policy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 international_trade
}
```

## law_protectionism (ID 218)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_trade_policy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 stock_exchange
}
```

## law_sakoku (ID 231)

Group: `lawgroup_trade_policy`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\01_trade_policy.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 country_has_primary_culture = cu:japanese
 any_scope_state = {
  state_region = s:STATE_KYUSHU
  is_largest_state_in_region = yes
 }
}
```

## law_chartered_caste_labour_boards (ID 22)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 socialism
}
can_enact = {
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
```

## law_chartered_caste_relief_rolls (ID 23)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 labor_movement
}
can_enact = {
 OR = {
  has_law = law_type:law_hindu_caste_codified
  has_law = law_type:law_hindu_caste_enforced
 }
}
```

## law_chartered_no_social_security (ID 32)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
```

## law_chartered_old_age_pension (ID 33)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 human_rights
 civilizing_mission
}
```

## law_chartered_poor_laws (ID 35)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
disallowing_laws = {
 law_company_exploitation
}
unlocking_technologies = {
 labor_movement
}
```

## law_chartered_wage_subsidies (ID 41)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\04_india_rebalance_laws.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 is_india_tag_trigger = yes
}
unlocking_technologies = {
 socialism
}
```

## law_chiefs_distribute_aid (ID 74)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_welfare.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 c:MON ?= this
}
disallowing_laws = {

}
```

## law_no_social_security (ID 197)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_welfare.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
is_visible = {
 NOT = {
  c:MON ?= this
 }
}
```

## law_old_age_bismarck (ID 202)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `common\laws\tyrone_bismark.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 human_rights
}
is_visible = {
 OR = {
  has_journal_entry = je_bismarck_reform
  has_variable = var:bismarck_reforms_done
 }
}
```

## law_old_age_pension (ID 203)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_welfare.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 human_rights
}
```

## law_poor_laws (ID 211)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_welfare.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 democracy
}
```

## law_wage_subsidies (ID 257)

Group: `lawgroup_welfare`. Qing request: **yes**, if Qing holds this law. Native imposition predicate: **absent; use court selector**. Source: `game/common\laws\02_welfare.txt`.

Exact law-specific restrictions (in addition to engine-wide checks and referenced scripted triggers):

```paradox
unlocking_technologies = {
 labor_movement
}
```

# Referenced scripted eligibility predicates

These definitions are source evidence, not results evaluated for a particular country. Engine built-ins retain their native meaning.

## AND

Source: `common\scripted_triggers\chi_adm_provincial_development_extension.txt`.

```paradox
AND = {
 var:chi_adm_provincial_development_compact_case = 5
 chi_adm_provincial_development_region_5_held = yes
}
```

## NOT

Source: `common\scripted_triggers\chi_adm_provincial_development_extension.txt`.

```paradox
NOT = {
 any_scope_state = {
  turmoil >= 0.25
 }
}
```

## OR

Source: `common\scripted_triggers\tyrone_nim_triggers.txt`.

```paradox
OR = {
 state_region = s:STATE_GUJARAT
 state_region = s:STATE_CENTRAL_PROVINCES
 state_region = s:STATE_AWADH
 state_region = s:STATE_MALWA
 state_region = s:STATE_BUNDELKHAND
 state_region = s:STATE_RAJPUTANA
 state_region = s:STATE_MYSORE
 state_region = s:STATE_TRAVANCORE
 state_region = s:STATE_HYDERABAD
}
```

## country_has_monarchy_law

Source: `game/common\scripted_triggers\00_ep2_victoria_scripted_triggers.txt`.

```paradox
country_has_monarchy_law = {
 OR = {
  has_law = law_type:law_monarchy
  has_law = law_type:law_social_monarchy
 }
}
```

## country_has_voting_franchise

Source: `game/common\scripted_triggers\00_scripted_triggers.txt`.

```paradox
country_has_voting_franchise = {
 OR = {
  modifier:country_voting_power_base_add > 0
  modifier:country_voting_power_from_literacy_add > 0
  modifier:country_voting_power_wealth_threshold_add > 0
  modifier:country_academics_voting_power_add > 0
  modifier:country_aristocrats_voting_power_add > 0
  modifier:country_bureaucrats_voting_power_add > 0
  modifier:country_capitalists_voting_power_add > 0
  modifier:country_clergymen_voting_power_add > 0
  modifier:country_clerks_voting_power_add > 0
  modifier:country_engineers_voting_power_add > 0
  modifier:country_farmers_voting_power_add > 0
  modifier:country_laborers_voting_power_add > 0
  modifier:country_machinists_voting_power_add > 0
  modifier:country_officers_voting_power_add > 0
  modifier:country_peasants_voting_power_add > 0
  modifier:country_shopkeepers_voting_power_add > 0
  modifier:country_slaves_voting_power_add > 0
  modifier:country_soldiers_voting_power_add > 0
 }
}
```

## country_is_colonial_or_company

Source: `game/common\scripted_triggers\00_ip4_victoria_scripted_triggers.txt`.

```paradox
country_is_colonial_or_company = {
 OR = {
  is_country_type = company
  is_country_type = colonial
 }
}
```

## country_is_islamic

Source: `common\scripted_triggers\00_ip3_victoria_scripted_triggers.txt`.

```paradox
country_is_islamic = {
 OR = {
  country_has_state_religion = rel:sunni
  country_has_state_religion = rel:shiite
  country_has_state_religion = rel:ibadi
 }
}
```

## country_is_subject_type_valid_for_caesaropapism

Source: `game/common\scripted_triggers\00_ip5_victoria_scripted_triggers.txt`.

```paradox
country_is_subject_type_valid_for_caesaropapism = {
 religion = rel:orthodox
 OR = {
  is_subject_type = subject_type_colony
  is_subject_type = subject_type_dominion
  is_subject_type = subject_type_chartered_company
  is_subject_type = subject_type_crown_land
  is_subject_type = subject_type_personal_union
 }
}
```

## has_factory_councils_law_or_amendment

Source: `game/common\scripted_triggers\00_ip5_victoria_scripted_triggers.txt`.

```paradox
has_factory_councils_law_or_amendment = {
 OR = {
  has_law_or_variant = law_type:law_factory_councils
  active_law:lawgroup_labour_associations ?= {
   has_amendment = amendment_type:amendment_factory_councils
  }
 }
}
```

## is_china_tag_trigger

Source: `common\scripted_triggers\tyrone_scripted_triggers.txt`.

```paradox
is_china_tag_trigger = {
 OR = {
  chi_qing_administration_tag = yes
  c:CHI ?= this
  c:BEI ?= this
  c:TPG ?= this
 }
}
```

## is_india_tag_trigger

Source: `common\scripted_triggers\tyrone_scripted_triggers.txt`.

```paradox
is_india_tag_trigger = {
 OR = {
  c:BIC ?= this
  c:BHT ?= this
 }
}
```

## movement_is_socialist

Source: `game/common\scripted_triggers\00_scripted_triggers.txt`.

```paradox
movement_is_socialist = {
 custom_tooltip = {
  text = movement_is_socialist_tt
  OR = {
   is_political_movement_type = movement_nihilist
   is_political_movement_type = movement_socialist
   is_political_movement_type = movement_communist
   is_political_movement_type = movement_anarchist
  }
 }
}
```

## tyr_ssm_is_chinese_country

Source: `common\scripted_triggers\tyrone_self_strengthening.txt`.

```paradox
tyr_ssm_is_chinese_country = {
 OR = {
  chi_qing_administration_tag = yes
  c:CHI ?= this
  c:BEI ?= this
  c:TPG ?= this
  c:HNA ?= this
  c:AHU ?= this
  c:ZHI ?= this
  c:SHN ?= this
  c:GUI ?= this
  c:GNG ?= this
  c:SIH ?= this
  c:SHA ?= this
  c:XIB ?= this
  c:YUN ?= this
  c:YUE ?= this
  c:XIN ?= this
  c:MCH ?= this
  c:MGL ?= this
  c:TUV ?= this
  c:ALI ?= this
 }
}
```

## tyrone_cr_can_leave_civil_service

Source: `common\scripted_triggers\tyrone_crown_raj_triggers.txt`.

```paradox
tyrone_cr_can_leave_civil_service = {
 custom_tooltip = {
  text = tyrone_cr_civil_service_locked_tt
  NOT = {
   AND = {
    is_subject = yes
    has_variable = tyrone_cr_active
    has_law = law_type:law_india_crown_administration
    NOT = {
     has_variable = tyrone_cr_apparatus_done
    }
   }
  }
 }
}
```

## tyrone_cr_can_leave_corporations

Source: `common\scripted_triggers\tyrone_crown_raj_triggers.txt`.

```paradox
tyrone_cr_can_leave_corporations = {
 custom_tooltip = {
  text = tyrone_cr_corporations_locked_tt
  NOT = {
   AND = {
    is_subject = yes
    has_law = law_type:law_india_crown_industrial_obligations
   }
  }
 }
}
```

## tyrone_cr_can_leave_police

Source: `common\scripted_triggers\tyrone_crown_raj_triggers.txt`.

```paradox
tyrone_cr_can_leave_police = {
 custom_tooltip = {
  text = tyrone_cr_police_locked_tt
  NOT = {
   AND = {
    is_subject = yes
    has_law = law_type:law_india_crown_constabulary
   }
  }
 }
}
```

## c:CHI

Source: `common\scripted_triggers\chi_adm_provincial_development_extension.txt`.

```paradox
c:CHI = {
 has_technology_researched = central_archives
 relative_bureaucracy >= 0.10
}
```

## chi_adm_provincial_development_region_5_held

Source: `common\scripted_triggers\chi_adm_provincial_development_extension.txt`.

```paradox
chi_adm_provincial_development_region_5_held = {
 any_scope_state = {
  OR = {
   state_region = s:STATE_SHENGJING
   state_region = s:STATE_SOUTHERN_MANCHURIA
   state_region = s:STATE_NORTHERN_MANCHURIA
   state_region = s:STATE_OUTER_MANCHURIA
   state_region = s:STATE_AMUR
  }
 }
}
```

## chi_qing_administration_tag

Source: `common\scripted_triggers\tyrone_qing_administrations.txt`.

```paradox
chi_qing_administration_tag = {
 OR = {
  c:ZHI ?= this
  c:AHU ?= this
  c:HNA ?= this
  c:YUE ?= this
  c:FRS ?= this
  c:XIB ?= this
  c:YUN ?= this
  c:SIH ?= this
  c:SHN ?= this
  c:SHA ?= this
  c:MGL ?= this
  c:MCH ?= this
  c:XIN ?= this
 }
}
```

