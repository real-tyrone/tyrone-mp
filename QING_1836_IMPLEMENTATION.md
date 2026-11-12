# Qing administrative start, 1836

Start a **new 1836 campaign**. This setup runs in global history after the existing population, building, character, and military histories; it does not migrate an existing save.

The Qing imperial court (`CHI`) directly owns **Beijing and all five Manchurian state regions**: Shengjing, Southern Manchuria, Northern Manchuria, Amur, and Outer Manchuria. All other original Qing provinces are assigned to 15 subordinate administrations. Portugal's Macau province, Kokand's provinces, and all other foreign ownership remain unchanged. Portugal's country history schedules a delayed startup event to create the Macau treaty port after `YUE` is initialized. Tibet retains its existing separate Qing-dependent government.

All starting states owned by Qing, its 15 administrations, and Tibet are **incorporated**. This is applied after the administrative transfers, including Mongolia, Tuva, Altai, Manchuria, Inner Mongolia, Xinjiang, and Qinghai. Foreign-owned state parts retain their existing incorporation status.

| Subject class | Governments | Autonomy | Income remitted | Ruler | Joins Qing wars |
|---|---:|---:|---:|---|---|
| Qing Viceroyalty | 8 | 1 | 30% | Local governor | All |
| Qing Provincial Administration | 3 | 1 | 30% | Local governor | All |
| Qing Frontier Administration | 4 | 2 | 30% | Local ruler | All |

The eight viceroyalties have their own subject type, `subject_type_qing_viceroyalty_administration`. All starting subject classes use `income_transfer = 0.30`, with the subject paying the court, and `join_overlord_wars = yes`. They share the imperial market and cannot start independent diplomatic plays. Their pacts cost no diplomatic maintenance and cannot be traded in sway offers or targeted by transfer-subject war goals. The military subject type remains defined for compatibility but has no starting country assigned.

All four types use `category = same_as_vassal` and `use_overlord_ruler = no`. Each administration has its own local ruler subordinate to the Qing emperor; none uses personal-union subject settings.

Weekly liberty desire reductions remain 0.75 for viceroyalties and provincial administrations, and 0.25 for frontier administrations.

## Territorial allocation

Names below refer to the existing `STATE_` keys. Each assignment transfers only the originally Qing-owned state part.

| Tag | Administration | Assigned state regions |
|---|---|---|
| ZHI | Zhili Viceroyalty | ZHILI |
| QLJ | Liangjiang Viceroyalty | NANJING, JIANGSU, SUZHOU, NORTHERN_ANHUI, SOUTHERN_ANHUI, JIANGXI |
| QHG | Huguang Viceroyalty | WESTERN_HUBEI, EASTERN_HUBEI, HUNAN |
| YUE | Liangguang Viceroyalty | GUANGDONG, SHAOZHOU, GUANGXI |
| QMZ | Min-Zhe Viceroyalty | FUJIAN, ZHEJIANG, FORMOSA |
| QSG | Shaan-Gan Viceroyalty | XIAN, GANSU, NINGXIA |
| YUN | Yun-Gui Viceroyalty | YUNNAN, GUIZHOU |
| SIH | Sichuan Viceroyalty | SICHUAN, CHONGQING |
| QSX | Shanxi Governorate | SHANXI |
| SHA | Shandong Governorate | SHANDONG |
| QHN | Henan Governorate | HENAN |
| MGL | Mongolian Administration | ULIASTAI, URGA, TUVA, ALTAI |
| QIM | Inner Mongolian Banners | ALXA, HINGGAN |
| XIN | Ili General | DZUNGARIA, TIANSHAN, JETISY, KIRGHIZIA |
| QXN | Xining Imperial Minister | QINGHAI |

`MGL` unifies Outer Mongolia, Tuva, and Altai. `MCH` is not created at the start; its former territories remain directly under `CHI`. `QIM` unifies Alxa and all of HINGGAN/Monan. No province-level administrative splits remain.

`ZHI`, `SIH`, `YUN`, `XIN`, `MGL`, and `YUE` reuse their existing game country definitions and flags. Dynamic names identify them as Qing administrations while they hold an appointed subject status. Their normal names remain available after that status ends. `YUN` retains both Yunnan and Guizhou from the previous Yun-Gui Viceroyalty.

## Laws and journals

Qing, all 15 starting administrations, and Tibet start with **Yin Privileges** (`law_chi_yinpriv`) and **Tuanlian Army** (`law_chi_tuanlian`). Qing retains Tenant Farmers, monarchy, autocracy, land taxation, the Canton System, Palace Memorials, junk fleet, and apothecary laws.

Viceroyalties and provincial governors implement subsequent imperial law changes. Frontier governments retain their local institutions and faiths. All starting administrations explicitly remove Manchu primary culture after adding their local cultures; only the main Qing retains Manchu primary culture. Ili uses Uighur, Mongolia and Inner Mongolia use Mongol, Qinghai uses Tibetan and Mongol, and civil administrations use Han (Liangguang also uses Yue).

| Starting country | State religion |
|---|---|
| Qing and all civil administrations | Confucian (`confucian`) |
| Mongolian Administration, Inner Mongolian Banners, Xining/Qinghai, Tibet | Gelugpa (`gelugpa`) |
| Ili General | Sunni (`sunni`), as a population-based gameplay abstraction |

These assignments set the country's state religion; they do not convert its population.

Shared imperial modifiers are added **once, indefinitely**, with a `has_modifier` guard. Monthly checks leave existing modifiers untouched; a changed reform stage replaces the previous stage, and a resolved imperial effect is removed. A once-per-subject cleanup clears old stacked copies before installing the corrected modifiers. This runs at the startup hook or the next monthly synchronization. Subject tooltip localization includes the generated `_no_icon` and `concept_..._desc` keys.

The Fragile Unity counter starts at 0, matching the main mod. Later crises can still trigger the warlord collapse, which converts appointed administrations to the mod's warlord subject type. The integration and reintegration journals use the consolidated tags, with no duplicate canonical-tag warlord buttons.

Missionaries, Taiping unrest and state transfers, Opium War state events, and homeland development can reach appointed administrations' territory. National military, industrial, literacy, and fleet requirements count the administrative realm. Relevant imperial modifiers and military reform unlocks reach subjects. Viceroyalties participate in imperial law propagation alongside provincial and military administrations.

The imperial administrations journal offers peaceful integration after Central Archives, at least 25% relative bureaucracy, centralisation of 6 or consolidated imperial authority, peace, and subject liberty desire at most 25. One administration can be integrated every six months. Tibet is outside this integration system.

## Verification

Run `python tools/validate_qing.py`. It checks country-tag reuse and collisions, script structure, database references, assigned capitals, all province transfers, foreign ownership, 30% payments, and compulsory participation in Qing's wars. It simulates both possible seed-state transfer behaviors and requires identical final ownership.

Validation passes: 3,422 original Qing provinces, 15 landed administrations, and 772 provinces in Beijing and Manchuria retained by `CHI`. Foreign ownership is unchanged. Starting laws, state religions, primary cultures, incorporation, and subject tooltip keys are verified. The validator separately reports 61 pre-existing duplicate province entries outside Qing; this revision does not change them.

Run `python tools/test_qing_modifiers.py` for the modifier regression test. It interprets the actual sharing and army-stage scripts, clears pre-existing stacks, and checks 240 monthly pulses plus reform transitions and resolved penalties. Existing modifiers receive no repeated additions, and all shared copies are indefinite.

In-game startup and campaign testing has **not** been performed. Runtime military formations, subject budgets, and AI behavior still need observation in a new game. Earlier edited files are archived under `tools/qing_originals/`; the immediately preceding setup is archived under `tools/qing_revision_originals/`. The latest pre-fix sources are archived under `tools/qing_start_fix_originals/`. All archives use `.bak` extensions outside the game's loaded script directories.
