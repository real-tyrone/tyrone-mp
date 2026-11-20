"""Validate regional works content, native dependencies and the charter lifecycle contract."""
import re

from validate_chi_adm import TAGS, definitions, get
from validate_chi_adm_qing_security import GAME, ROOT, all_values, named, read, walk


PREFIX = "chi_adm_regional_works_"
T = definitions("common/scripted_triggers/chi_adm_regional_works.txt")
E = definitions("common/scripted_effects/chi_adm_regional_works.txt")
B = definitions("common/scripted_buttons/chi_adm_regional_works.txt")
M = definitions("common/static_modifiers/chi_adm_regional_works.txt")
EVENTS = definitions("events/chi_adm_regional_works.txt")
TRACKS = {"military": 1, "economic": 2, "administrative": 3, "education": 4}


def database(folder):
    paths = [path for base in (GAME, ROOT) for path in (base / "common" / folder).rglob("*.txt")]
    return set(re.findall(
        r"^\s*(?:REPLACE:|INJECT:)?([\w-]+)\s*=\s*\{",
        "\n".join(path.read_text(encoding="utf-8-sig") for path in paths),
        re.M,
    ))


def sources():
    loc_path = ROOT / "localization/english/chi_adm_l_english.yml"
    assert loc_path.read_bytes().startswith(b"\xef\xbb\xbf")
    loc = loc_path.read_text(encoding="utf-8-sig")
    names = re.findall(r"^ ([\w.]+):(?:0)? ", loc, re.M)
    assert len(names) == len(set(names))
    keys = set(names)
    paths = list(ROOT.glob("common/*/chi_adm_regional_works.txt")) + [ROOT / "events/chi_adm_regional_works.txt"]
    for path in paths:
        definitions(path)
        for key in re.findall(
            r"(?:title|desc|localization_key|custom_tooltip|text)\s*=\s*(chi_adm_regional_works[._][\w.]+)",
            read(path),
        ):
            assert key in keys, (path, key)
    for event, block in EVENTS.items():
        if event == "namespace":
            continue
        options = all_values(block, "option")
        assert len(options) == 4
        assert sum(named(option, "default_option", "yes") for option in options) == 1
        for option in options:
            assert get(option, "name") in keys
            assert named(get(option, "trigger"), PREFIX + "offer_matches", [("KEY", "=", event.split(".")[-1])])
            assert get(option, "ai_chance")
        assert (GAME / get(block, "icon").strip('"')).exists()
    assert named(E[PREFIX + "offer_case"], "name", PREFIX + "offer_revision")
    assert named(T[PREFIX + "offer_matches"], "var:" + PREFIX + "offer_revision", "scope:" + PREFIX + "offer_revision")
    modifiers = database("modifier_type_definitions")
    for name, block in M.items():
        assert {name, name + "_desc"} <= keys
        assert (GAME / get(block, "icon")).exists()
        assert all(key == "icon" or key in modifiers and not key.startswith(("unit_", "ship_")) and "birth_rate" not in key
                   for key, _, _ in block), name
    gui = read("gui/journal_entry_widgets/chi_adm_regional_works.gui")
    assert gui.count("{") == gui.count("}") and "JournalEntry.GetCountry" in gui
    for key in re.findall(r'text = "(chi_adm_regional_works_\w+)"', gui):
        assert key in keys
    assert not re.search(r"\bevery_country\s*=|\bon_weekly_pulse", "\n".join(read(path) for path in paths))


def regional_coverage():
    setup = read("common/history/global/zzzz_qing_administrations.txt")
    sites = read("map_data/state_regions/11_east_asia.txt")
    buildings = database("buildings")
    found = set()
    petitions = [(name, block) for name, block in T.items() if name.endswith("_petition") and name != PREFIX + "open_petition"]
    assert len(petitions) == 13
    for index, (name, block) in enumerate(petitions, 1):
        tag = next(key[2:] for key, op, value in block if key.startswith("c:") and op == "?=" and value == "this")
        site = get(get(block, "any_scope_state"), "state_region")
        assert re.search(rf"^{site[2:]}\s*=", sites, re.M), site
        assert re.search(rf"{site}\b[^\n]*set_state_owner\s*=\s*c:{tag}\b", setup) or tag == "MCH", (tag, site)
        found.add(tag)
        for building in all_values(block, "is_building_type"):
            assert building in buildings, building
        event = EVENTS[f"chi_adm_regional_works.{index}"]
        assert named(E[PREFIX + "offer_petition"], "EVENT", f"chi_adm_regional_works.{index}")
        decisions = all_values(event, "option")[:2]
        for choice, outcome in zip(decisions, ("1", "2")):
            assert named(get(choice, "trigger"), name, "yes")
            assert named(choice, "OUTCOME", outcome)
        assert named(decisions[0], "state_region", site)
    assert found == set(TAGS)
    assert named(E[PREFIX + "close_petition"], "name", PREFIX + "petition_done")
    assert named(E[PREFIX + "defer_case"], "months", "18")


def project_wiring():
    development = definitions("common/journal_entries/chi_adm_provincial_development_extension.txt")["chi_adm_provincial_development_development"]
    buttons = all_values(development, "scripted_button")
    assert len(buttons) == len(set(buttons))
    assert {f"chi_adm_provincial_development_start_{track}_{tier}" for track in TRACKS for tier in (1, 2, 3)} <= set(buttons)
    assert {"chi_adm_provincial_development_ask_sponsor", "chi_adm_provincial_development_takeover", "chi_adm_provincial_development_cancel_projects"} <= set(buttons)
    works = [button for button in buttons if button.startswith(PREFIX) and button.endswith("_button")]
    assert len(works) == 6 and set(works) <= B.keys()
    buildings, companies, tech = (database(kind) for kind in ("buildings", "company_types", "technology"))
    provincial_development = definitions("common/scripted_effects/chi_adm_provincial_development_extension.txt")
    used_tracks = set()
    for index, button in enumerate(works, 101):
        key = button.removesuffix("_button")
        industry, site, candidate = (T[key + suffix] for suffix in ("_industry", "_site", "_candidate"))
        site_gate = get(candidate, "any_scope_state")
        track_gate = get(site_gate, PREFIX + "track_available")
        track, tier = get(track_gate, "TRACK"), get(track_gate, "TIER")
        used_tracks.add(track)
        assert int(get(track_gate, "TYPE")) == TRACKS[track]
        required_tech = get(get(get(provincial_development[f"chi_adm_provincial_development_start_{track}_{tier}"], "if"), "limit"),
                            "has_technology_researched")
        assert required_tech in all_values(industry, "has_technology_researched")
        assert set(all_values(industry, "has_technology_researched")) <= tech
        assert set(all_values(site, "is_building_type")) <= buildings
        assert all(int(level) >= 3 for level in all_values(site, "level"))
        company_types = all_values(industry, "is_company_type")
        assert bool(company_types) == (not key.endswith("_lanzhou"))
        assert {name.split(":")[-1] for name in company_types} <= companies
        assert named(T[key + "_identity"], "has_variable", key + "_ratified")
        assert named(B[button], "EVENT", f"chi_adm_regional_works.{index}")
        for route, option in enumerate(all_values(EVENTS[f"chi_adm_regional_works.{index}"], "option")[:2], 1):
            params = get(get(option, "hidden_effect"), PREFIX + "endorse_charter")
            assert params == [("PROJECT", "=", key.removeprefix(PREFIX)), *track_gate,
                              ("KEY", "=", str(index)), ("ROUTE", "=", str(route))]
            assert named(get(option, "trigger"), key + "_candidate", "yes")
    assert used_tracks == set(TRACKS)
    # A commissioned project can observe the native track, but cannot award
    # progress, rewrite the bill or dispense companies and buildings.
    all_actions = {name for block in E.values() for name, _, _ in walk(block)}
    assert not all_actions.intersection({"create_company", "create_building", "annex", "add_treasury"})
    assert not any(name.startswith("chi_adm_provincial_development_start_") for name in all_actions)


def lifecycle():
    review = E[PREFIX + "review_charter"]
    expiry = get(E[PREFIX + "province_review"], "if")
    cancel = get(review, "if")
    assert named(expiry, "has_variable", PREFIX + "charter_key")
    assert named(expiry, "has_variable", "chi_adm_qing_security_pact")
    assert named(cancel, "owner", "prev")
    assert named(cancel, PREFIX + "track_available", [("TRACK", "=", "$TRACK$"),
                                                       ("TYPE", "=", "$TYPE$"), ("TIER", "=", "$TIER$")])
    award = get(review, "else_if")
    assert named(get(award, "limit"), "var:chi_adm_provincial_development_$TRACK$", "$TIER$")
    assert named(get(award, "limit"), PREFIX + "$PROJECT$_industry", "yes")
    steps = [name for name, _, _ in award]
    assert steps.index("c:CHI") < steps.index("var:" + PREFIX + "charter_site")
    assert named(award, "set_variable", PREFIX + "$PROJECT$_ratified")
    assert named(award, "years", "4") and named(award, PREFIX + "clear_charter", "yes")
    assert set(all_values(E[PREFIX + "clear_charter"], "remove_variable")) == {
        PREFIX + "charter_site", PREFIX + "charter_key", PREFIX + "charter_route",
    }
    assert named(T[PREFIX + "peacetime"], "var:chi_adm_qing_security_phase", "5")
    assert all(named(branch, "is_ai", "yes") for branch in all_values(E[PREFIX + "province_review"], "if")[-2:])


if __name__ == "__main__":
    sources()
    regional_coverage()
    project_wiring()
    lifecycle()
    print("PASS regional works: 13 regional dispatches, six charters, installed dependencies, all four provincial development tracks, AI, consent and lifecycle wiring.")
