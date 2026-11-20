"""office titles focused native-government and Shanxi migration checks; no engine claims."""
from pathlib import Path
import hashlib
import json
import re
import sys
from chi_adm_authorized_validation import authorized_current

sys.dont_write_bytecode = True
import validate_chi_adm as foundation

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
GOV_PATH = "common/government_types/00_00_chi_adm_government_types.txt"
VICEROYS = set("ZHI AHU HNA YUE FRS XIB YUN SIH".split())
GOVERNORS = {"SHN", "SHA"}
FRONTIERS = {"MGL": "uliastai_generalship", "XIN": "ili_generalship", "MCH": "manchurian_generalships"}


def read(path):
    return (ROOT / path).read_text("utf-8-sig")


class Country(foundation.Province):
    monarchy = True
    regency = False
    wrong_subject_type = False

    @property
    def subject_type(self):
        if not self.subject or self.wrong_subject_type:
            return "subject_type_protectorate"
        if self.tag in VICEROYS:
            return "subject_type_qing_viceroyalty_administration"
        return super().subject_type


def possible(items, country):
    results = []
    for key, op, value in items:
        if key == "OR":
            result = any(possible([item], country) for item in value)
        elif key == "AND":
            result = all(possible([item], country) for item in value)
        elif key == "has_law_or_variant":
            assert value == "law_type:law_monarchy"
            result = country.monarchy
        elif key == "has_gov_regency":
            result = country.regency == (value == "yes")
        elif key == "is_subject":
            result = country.subject == (value == "yes")
        else:
            result = foundation.condition([(key, op, value)], country)
        results.append(result)
    return all(results)


def main():
    governments = foundation.definitions(GOV_PATH)
    expected = {
        "CHI": "celestial_empire",
        **{tag: "imperial_viceroyalty" for tag in VICEROYS},
        **{tag: "imperial_governorate" for tag in GOVERNORS},
        **FRONTIERS,
    }
    assert set(foundation.TAGS) == VICEROYS | GOVERNORS | set(FRONTIERS) and len(foundation.TAGS) == 13
    assert len(governments) == 9
    for tag, suffix in expected.items():
        country = Country(tag, subject=tag != "CHI")
        selected = [key for key, body in governments.items() if possible(foundation.get(body, "possible"), country)]
        assert selected == ["chi_adm_government_titles_gov_" + suffix], (tag, selected)
        for attr, value in (("monarchy", False), ("regency", True)):
            setattr(country, attr, value)
            assert not any(possible(foundation.get(body, "possible"), country) for body in governments.values()), (tag, attr)
            setattr(country, attr, not value)
        if tag != "CHI":
            for attr, value in (("subject", False), ("court_exists", False), ("court_monarchy", False), ("wrong_subject_type", True)):
                setattr(country, attr, value)
                assert not any(possible(foundation.get(body, "possible"), country) for body in governments.values()), (tag, attr)
                setattr(country, attr, not value)
            # Native office display follows the actual pact, not the journal's
            # startup/fragmentation markers. No provincial accounts initialization is performed.
            country.variables.clear()
            country.fragmented = True
            assert [key for key, body in governments.items() if possible(foundation.get(body, "possible"), country)] == ["chi_adm_government_titles_gov_" + suffix]
    for tag in ("TIB", "KOR", "LAN", "JAP", "RUS", "TPG", "FRA"):
        country = Country(tag)
        assert not any(possible(foundation.get(body, "possible"), country) for body in governments.values()), tag

    loc = read("localization/english/chi_adm_l_english.yml")
    localized = dict(re.findall(r'^\s*(\w+):\s*"(.*)"$', loc, re.M))
    exact_titles = {
        "manchurian_viceroyalty": "Viceroy of the Three Eastern Provinces",
        "celestial_empire": "Son of Heaven", "imperial_viceroyalty": "Viceroy",
        "imperial_governorate": "Governor", "uliastai_generalship": "General of Uliastai",
        "banner_administration": "Imperial Commissioner", "ili_generalship": "General of Ili",
        "xining_commission": "Imperial Minister", "manchurian_generalships": "General of Shengjing",
    }
    for key, body in governments.items():
        assert foundation.get(body, "transfer_of_power") == "hereditary"
        assert not any(k.startswith("on_") or k in ("new_leader_on_reform_government", "effect") for k, _, _ in body)
        assert key in localized and "$TRANSFER_OF_POWER_NAME_DESC$" in localized[key + "_desc"]
        for sex in ("male_ruler", "female_ruler"):
            title = foundation.get(body, sex).strip('"')
            assert localized[title] == exact_titles[key.removeprefix("chi_adm_government_titles_gov_")]
    # Match native specialized-first/generic-later ordering; do not invent weight fields.
    assert not re.search(r"\b(?:priority|weight)\s*=", read(GOV_PATH))
    assert "chi_adm_eligible =" not in read(GOV_PATH)
    assert "has_variable =" not in read(GOV_PATH)
    assert read(GOV_PATH).count("is_subject_of = c:CHI") == 6
    assert read(GOV_PATH).count("exists = c:CHI") == 8
    assert Path(GOV_PATH).name < min(p.name for p in (GAME / "common/government_types").glob("*.txt"))
    native = (GAME / "common/government_types/01_monarchies.txt").read_text("utf-8-sig")
    assert native.index("gov_tsardom =") < native.index("gov_absolute_empire =")
    assert 'transfer_of_power = hereditary' in native and 'male_ruler = "RULER_TITLE_EMPEROR"' in native

    # Exactly one vanilla SHN identity; no mod duplicate and no remaining QSX in active data.
    countries = (GAME / "common/country_definitions/00_countries.txt").read_text("utf-8-sig")
    assert len(re.findall(r"(?m)^SHN\s*=", countries)) == 1
    for folder in ("common", "events", "gui", "localization"):
        for path in (ROOT / folder).rglob("*"):
            if path.suffix in (".txt", ".gui", ".yml"):
                source = path.read_text("utf-8-sig")
                assert "QSX" not in source, str(path)
                if path.parent.name == "country_definitions":
                    assert not re.search(r"(?m)^SHN\s*=", source), "Duplicate vanilla Shanxi definition"
    assert "INJECT:SHN = {" in read("common/dynamic_country_names/tyrone_qing_administrations.txt")
    assert "adjective = SHN_ADJ" in read("common/dynamic_country_names/tyrone_qing_administrations.txt")
    assert not re.search(r"^\s*SHN:", read("localization/english/chi_adm_l_english.yml"), re.M), "Do not override vanilla base name"
    setup = read("common/history/global/zzzz_qing_administrations.txt")
    assert setup.count("tag = SHN") == 1
    assert "state_region = s:STATE_SHANXI } } set_state_owner = c:SHN" in setup
    assert "country = c:SHN type = qing_civil_administration" in setup
    pacts = re.findall(r"create_diplomatic_pact\s*=\s*\{\s*country\s*=\s*c:(\w+)\s+type\s*=\s*qing_", setup)
    assert len(pacts) == len(set(pacts)) == len(foundation.TAGS) and set(pacts) == set(foundation.TAGS)
    # Do not silently refresh hashes: prove every rebased baseline was only a tag rename.
    migration = json.loads(read("tools/chi_adm_government_titles_migration_baseline.json"))
    for path, record in migration["rebased"].items():
        current = (ROOT / path).read_bytes()
        if path == 'common/scripted_buttons/tyrone_qing_administrations.txt' and (ROOT/'tools/chi_adm_negotiated_integration_baseline.json').exists():
            # negotiated integration intentionally replaces the 15 integration bodies. Preserve the
            # original migration evidence and prove every other body is unchanged.
            original = json.loads(read('tools/chi_adm_negotiated_integration_baseline.json'))['buttons']
            original = {k:v for k,_,v in original if not k.startswith('chi_qing_integrate_')}
            now = {k:json.loads(json.dumps(v)) for k,_,v in foundation.parse(current.decode('utf-8-sig')) if not k.startswith('chi_qing_integrate_')}
            assert original == now
            assert 'chi_qing_integrate_SHN' in current.decode('utf-8-sig')
            continue
        assert hashlib.sha256(current).hexdigest() == record["after"] or authorized_current(path)
        assert hashlib.sha256(current.replace(b"SHN", b"QSX")).hexdigest() == record["before"] or authorized_current(path)
    for key in ("chi_qing_integrate_SHN", "tyr_chi_reintegrate_SHN"):
        assert key in localized and key in read("common/scripted_buttons/tyrone_qing_administrations.txt")
    for path in (ROOT / "localization/english").rglob("*.yml"):
        if path.name != "chi_adm_l_english.yml":
            assert not re.search(r"^\s*(?:chi_adm_government_titles_|chi_qing_integrate_SHN:|tyr_chi_reintegrate_SHN:)", path.read_text("utf-8-sig"), re.M), path
    # Runtime regression: the subjects qualified for generic monarchies as well.
    # The last repair did not test those competing candidates at all.
    helper = foundation.definitions("common/scripted_triggers/chi_adm_government_titles_eligibility.txt")["chi_adm_government_titles_office_government_available"]
    expected_branches = [("AND", "=", foundation.get(body, "possible")) for key, body in governments.items() if key != "chi_adm_government_titles_gov_celestial_empire"]
    assert helper == [("OR", "=", expected_branches)], "Exclusion must exactly match office eligibility"
    originals = foundation.definitions(GAME / "common/government_types/01_monarchies.txt")
    fallbacks = foundation.definitions("common/government_types/zz_chi_adm_government_titles_fallbacks.txt")
    expected_ids = {"gov_absolute_kingdom", "gov_feudal_kingdom", "gov_kingdom", "gov_constitutional_kingdom", "gov_absolute_principality", "gov_principality", "gov_constitutional_principality"}
    assert set(fallbacks) == {"REPLACE:" + key for key in expected_ids}
    for replacement, body in fallbacks.items():
        cleaned = []
        for key, op, value in body:
            if key == "possible":
                assert value[-1] == ("NOT", "=", [("chi_adm_government_titles_office_government_available", "=", "yes")])
                value = value[:-1]
            cleaned.append((key, op, value))
        assert cleaned == originals[replacement.removeprefix("REPLACE:")], "Unrelated native government behavior changed"
    for tag in foundation.TAGS:
        country = Country(tag)
        assert possible(helper, country), tag
        country.subject = False
        assert not possible(helper, country), tag
        country.subject = True
        country.monarchy = False
        assert not possible(helper, country), tag
        country.monarchy = True
        country.wrong_subject_type = True
        assert not possible(helper, country), tag
    for tag in ("CHI", "TIB", "KOR", "LAN", "FRA", "RUS", "JAP"):
        assert not possible(helper, Country(tag)), tag
    fixture = json.loads(read("tools/chi_adm_government_titles_runtime_fixture.json"))
    # Historical runtime fixture predates the merged roster; do not invent MCH observations.
    assert {item["tag"] for item in fixture["subjects"]} - set(foundation.TAGS) <= {'QHN','QIM','QXN'}
    for item in fixture["subjects"]:
        if item['tag'] not in foundation.TAGS:
            continue
        assert item["monarchy_active"] and item["accounts_active"] and item["pact"]
        assert item["government"] in expected_ids, item
        # Every generic type actually observed in the save now excludes offices.
        assert "REPLACE:" + item["government"] in fallbacks
        assert possible(helper, Country(item["tag"]))
    print("PASS office titles: native office governments plus competing-generic exclusions; exact preservation of 7 native fallbacks outside Qing offices; current-roster saved-game regression; titles, migration and mechanics")
    print("PENDING: native government precedence/refresh and tooltip/title displays in a new campaign; old QSX saves are not migrated.")


if __name__ == "__main__":
    main()
