"""imperial security source and bounded rule checks. Native play, backer and GUI behavior need Victoria 3."""
from dataclasses import dataclass, field
from pathlib import Path
import re

from validate_chi_adm import ROOT, TAGS, FRONTIER, definitions, get


PREFIX = "chi_adm_qing_security_"
GAME = Path("C:/Program Files (x86)/Steam/steamapps/common/Victoria 3/game")
T = definitions("common/scripted_triggers/chi_adm_qing_security.txt")
V = definitions("common/script_values/chi_adm_qing_security.txt")
E = definitions("common/scripted_effects/chi_adm_qing_security.txt")
E.update(definitions("common/scripted_effects/chi_adm_qing_security_war.txt"))
B = definitions("common/scripted_buttons/chi_adm_qing_security.txt")
J = definitions("common/journal_entries/chi_adm_qing_security.txt")
G = definitions("common/war_goal_types/chi_adm_qing_security.txt")
P = definitions("common/diplomatic_plays/chi_adm_qing_security.txt")


def walk(block):
    for part in block:
        yield part
        if isinstance(part[2], list):
            yield from walk(part[2])


def all_values(block, key):
    return [value for name, _, value in walk(block) if name == key]


def named(block, key, value):
    return value in all_values(block, key)


def read(path):
    return (ROOT / path).read_text(encoding="utf-8-sig")


def source_checks():
    paths = list(ROOT.glob("common/*/chi_adm_qing_security*.txt")) + list(ROOT.glob("events/chi_adm_qing_security*.txt"))
    trees = [definitions(path) for path in paths]
    script = "\n".join(read(path) for path in paths)
    gui = read("gui/journal_entry_widgets/chi_adm_qing_security.gui")
    loc = read("localization/english/chi_adm_l_english.yml")
    assert (ROOT / "localization/english/chi_adm_l_english.yml").read_bytes().startswith(b"\xef\xbb\xbf")
    names = re.findall(r"^ ([\w.]+):(?:0)? ", loc, re.M)
    assert len(names) == len(set(names))
    keys = set(names)
    for je in J:
        assert {je, je + "_reason", je + "_status"} <= keys
    assert len([je for je in J.values() if get(je, "context") == "none"]) == 2
    linked = [button for je in J.values() for button in all_values(je, "scripted_button")]
    assert len(linked) == len(set(linked)) and set(linked) == set(B)
    for button in B:
        assert {button, button + "_desc"} <= keys
    for key in re.findall(r'(?:text|tooltip) = "(chi_adm_qing_security_\w+)"', gui):
        assert key in keys, key
    for key in re.findall(r"(?:localization_key|name|title|desc|custom_tooltip_no_bullet) = (chi_adm_qing_security(?:[._])[\w.]+)", script):
        if key.endswith(("_scope", "_pledge", "_pact")) or key in V:
            continue
        assert key in keys or re.search(rf"\b(?:name|variable)\s*=\s*{re.escape(key)}\b", script) and key not in T, key
    assert all(f"name = {name}" in gui for je in J.values() for name in all_values(je, "name"))
    sgui = definitions("common/scripted_guis/chi_adm_qing_security.txt")
    assert set(re.findall(r"GetScriptedGui\('([^']+)'\)", gui)) <= set(sgui)
    assert set(re.findall(r"\.ScriptValue\('(chi_adm_qing_security_\w+)'\)", gui + loc)) <= set(V)
    assert "JournalEntry.GetCountry" in gui and "AccessPlayer" not in gui
    assert gui.count("{") == gui.count("}")
    native = (GAME / "common/modifier_type_definitions/00_modifier_types.txt").read_text(encoding="utf-8-sig")
    modifiers = definitions("common/static_modifiers/chi_adm_qing_security.txt")
    for name, block in modifiers.items():
        assert {name, name + "_desc"} <= keys
        assert (GAME / get(block, "icon")).exists()
        for modifier, _, _ in block:
            if modifier != "icon":
                assert re.search(rf"^{modifier}\s*=", native, re.M), modifier
                assert "birth_rate" not in modifier
    for name in G:
        assert {"war_goal_" + name + suffix for suffix in ("", "_desc", "_type_name", "_type_desc")} <= keys
    assert P.keys() <= keys
    assert not re.search(r"\b(year|current_date|date|annex|change_tag|switch_country)\s*[=<>]", script)
    assert "every_country =" not in script and "on_weekly_pulse = {}" in script
    definitions_found = {key for tree in trees for key in tree}
    for tree in trees:
        for block in tree.values():
            if isinstance(block, list):
                for key, _, _ in walk(block):
                    if key.startswith(PREFIX):
                        assert key in definitions_found, key


@dataclass
class Country:
    tag: str
    fields: dict = field(default_factory=dict)
    variables: dict = field(default_factory=dict)
    modifiers: set = field(default_factory=set)


def compare(left, op, right):
    if left is None or right is None:
        return False
    return {
        "=": lambda: left == right, "?=": lambda: left == right,
        ">=": lambda: left >= right, "<=": lambda: left <= right,
        ">": lambda: left > right, "<": lambda: left < right,
    }[op]()


class Fixture:
    """Evaluate the relevant predicates against country fixtures and script values."""

    def __init__(self):
        self.court = Country("CHI", {
            "chi_adm_court_valid": True, "has_journal_entry": "je_mandate_of_heaven",
            "centralisation": 3, "government_legitimacy": 40, "army_power_projection": 100,
        })
        self.leader = self.office("ZHI", loyalty=20, autonomy=65, army=40)
        self.ally = self.office("AHU", loyalty=33, autonomy=52, army=35)
        self.loyal = self.office("MCH", loyalty=80, autonomy=15, army=15)
        self.subjects = [self.leader, self.ally, self.loyal]

    @staticmethod
    def office(tag, loyalty, autonomy, army):
        return Country(tag, {
            "chi_adm_target_valid": True, "country_has_primary_culture": "cu:han",
            "chi_adm_frontier": tag in FRONTIER, "army_power_projection": army,
            "relations:c:CHI": 0, "claimant_relations": 0, "authority": 100,
        }, {"chi_adm_loyalty": loyalty, "chi_adm_autonomy": autonomy, "chi_adm_corruption": 25})

    def value(self, token, country):
        if isinstance(token, list):
            amount = 0
            for key, _, value in token:
                if key == "value":
                    amount = self.value(value, country)
                elif key == "multiply":
                    amount *= self.value(value, country)
                elif key == "divide":
                    amount /= self.value(value, country)
                elif key == "min":
                    amount = max(amount, self.value(value, country))
                elif key == "add":
                    amount += self.value(value, country)
                elif key == "every_subject_or_below":
                    amount += sum(
                        self.value(get(value, "add"), subject)
                        for subject in self.subjects if self.test(get(value, "limit"), subject)
                    )
                else:
                    raise AssertionError(key)
            return amount
        if token in V:
            return self.value(V[token], country)
        if token.startswith("var:"):
            return country.variables.get(token[4:])
        if token.startswith("c:CHI."):
            return self.value(token[6:], self.court)
        if token.startswith("relations_threshold:"):
            return {"poor": -20, "hostile": -50, "amicable": 50}[token.split(":")[1]]
        if token in ("yes", "no"):
            return token == "yes"
        try:
            return float(token)
        except ValueError:
            return country.fields.get(token, token)

    def test(self, block, country, previous=None):
        return all(self.condition(item, country, previous) for item in block)

    def condition(self, item, country, previous):
        key, op, value = item
        if key == "OR":
            return any(self.condition(child, country, previous) for child in value)
        if key == "NOR":
            return not any(self.condition(child, country, previous) for child in value)
        if key == "NOT":
            return not self.test(value, country, previous)
        if key == "AND":
            return self.test(value, country, previous)
        if key in T:
            return self.test(T[key], country, previous) == (value == "yes")
        if key == "c:CHI" and isinstance(value, list):
            return self.test(value, self.court, country)
        if key.startswith("c:") and value == "this":
            return key[2:] == country.tag
        if key.startswith("var:") and isinstance(value, list):
            target = self.value(key, country)
            return target is not None and self.test(value, target, country)
        if key.startswith("var:") and value == "prev":
            return self.value(key, country) is previous
        if key == "has_variable":
            return value in country.variables
        if key == "has_modifier":
            return value in country.modifiers
        if key == "exists":
            return self.value(value, country) is not None
        if key == "je:je_mandate_of_heaven":
            return compare(country.fields["centralisation"], value[0][1], float(value[0][2]))
        if key == "any_civil_war":
            return False
        if key == "save_temporary_scope_as":
            return True
        if key == '"relations(scope:chi_adm_qing_security_contact)"':
            key = "claimant_relations"
        if key in ("is_subject", "is_at_war", "is_diplomatic_play_committed_participant", "has_truce_with", "chi_adm_provincial_development_crisis"):
            left = country.fields.get(key, False)
        elif key in ("is_ai",):
            left = country.fields.get(key, True)
        else:
            left = self.value(key, country)
        return compare(left, op, self.value(value, country))


def political_checks():
    f = Fixture()
    court, leader, ally, loyal = f.court, f.leader, f.ally, f.loyal
    roster = {tag for tag in TAGS if f.test(T[PREFIX + "han_office"], f.office(tag, 20, 65, 10))}
    assert roster == set(TAGS) - FRONTIER and len(roster) == 10
    assert not f.test(T[PREFIX + "can_found"], leader)
    leader.variables[PREFIX + "grievance"] = 3
    assert f.test(T[PREFIX + "can_found"], leader)
    for key, bad in (("chi_adm_loyalty", 21), ("chi_adm_autonomy", 64)):
        original = leader.variables[key]
        leader.variables[key] = bad
        assert not f.test(T[PREFIX + "can_found"], leader)
        leader.variables[key] = original
    court.fields["centralisation"] = 4
    assert not f.test(T[PREFIX + "can_found"], leader)
    court.fields["centralisation"] = 3
    court.variables.update({PREFIX + k: v for k, v in {
        "claimant": leader, "phase": 1, "months": 3, "readiness": 75, "evidence": 50,
    }.items()})
    assert not f.test(T[PREFIX + "can_found"], ally)
    leader.variables[PREFIX + "faction"] = 1
    assert not f.test(T[PREFIX + "can_arm"], ally)
    review = get(E[PREFIX + "court_review"], "else")
    stages = [branch for key, _, branch in review if key in ("if", "else_if") and named(branch, "name", PREFIX + "phase")]
    for expected, month in ((2, 4), (3, 6)):
        if expected == 3:
            ally.variables[PREFIX + "faction"] = 1
        court.variables[PREFIX + "months"] = month - 1
        stage = next(stage for stage in stages if named(stage, "value", str(expected)))
        assert not f.test(get(stage, "limit"), court)
        court.variables[PREFIX + "months"] = month
        assert f.test(get(stage, "limit"), court)
        court.variables[PREFIX + "phase"] = expected

    loyal.variables[PREFIX + "faction"] = 3
    court.variables[PREFIX + "months"] = 12
    assert f.value(PREFIX + "armed_count", court) == 2
    assert abs(f.value(PREFIX + "force_ratio", court) - 75 / 115 * 100) < 0.001
    assert f.test(T[PREFIX + "can_issue"], leader)
    loyal.fields["army_power_projection"] = 20
    assert not f.test(T[PREFIX + "can_issue"], leader)
    loyal.fields["army_power_projection"] = 15
    ally.fields["is_ai"] = False
    assert f.value(PREFIX + "armed_count", court) == 1
    assert not f.test(T[PREFIX + "can_issue"], leader)
    ally.variables[PREFIX + "human_pledge"] = True
    assert f.test(T[PREFIX + "can_issue"], leader)
    ally.modifiers.add("chi_adm_provincial_development_guarantee")
    assert not f.test(T[PREFIX + "can_issue"], leader)
    ally.modifiers.clear()
    court.variables[PREFIX + "phase"] = 4
    court.variables[PREFIX + "ultimatum"] = True
    assert not f.test(T[PREFIX + "can_launch"], leader)
    del court.variables[PREFIX + "ultimatum"]
    assert f.test(T[PREFIX + "can_launch"], leader)
    ally.fields["chi_adm_target_valid"] = False
    assert not f.test(T[PREFIX + "can_launch"], leader)


def engine_wiring_checks():
    launch = E[PREFIX + "launch"]
    assert named(launch, PREFIX + "can_launch", "yes")
    assert len(all_values(launch, "create_diplomatic_play")) == 1
    assert named(launch, "type", "dp_chi_adm_qing_security_throne")
    assert named(launch, "type", PREFIX + "install_dynasty") and named(launch, "primary_demand", "yes")
    assert named(P["dp_chi_adm_qing_security_throne"], "war_goal", PREFIX + "restore_court")
    for goal, result in (("install_dynasty", "1"), ("restore_court", "2")):
        assert named(get(G[PREFIX + goal], "on_enforced"), "RESULT", result)
    record = E[PREFIX + "record_victory"]
    assert named(record, "has_variable", PREFIX + "pending_result")
    assert named(record, "id", "chi_adm_qing_security.3")
    resolve = E[PREFIX + "resolve"]
    assert named(resolve, PREFIX + "install_ruler", "yes")
    assert set(all_values(resolve, "RESULT")) == {"1", "2", "5", "6"}
    install = E[PREFIX + "install_ruler"]
    assert len(all_values(install, "create_character")) == 2
    assert named(install, "ruler", "yes") and named(install, "set_heir", "scope:chi_adm_qing_security_son")
    assert named(install, "AMOUNT", "-2")
    close = E[PREFIX + "close"]
    for variable in ("phase", "claimant", "readiness", "evidence", "terms", "native_started", "pending_result"):
        assert named(close, "remove_variable", PREFIX + variable), variable
    assert named(close, "clear_variable_list", PREFIX + "detached")
    assert named(E[PREFIX + "strip_unpledged"], "remove_initiator_backers", [("prev", "list", "")])
    assert named(E[PREFIX + "restore_office"], "has_variable", PREFIX + "human_pledge")
    court_review = E[PREFIX + "court_review"]
    assert named(court_review, "end_play", "yes")
    assert named(court_review, PREFIX + "live_play", "yes")
    ai = E[PREFIX + "ai_review"]
    for test in ("can_arm", "can_aid", "can_suppress", "can_offer", "can_issue", "can_launch"):
        assert named(ai, PREFIX + test, "yes")
    assert named(ai, "is_ai", "yes") and named(ai, "var:chi_adm_loyalty", "30")
    for feature in ("negotiated_integration", "provincial_development"):
        assert "NOT = { var:chi_adm_qing_security_phase = 5 }" in read(f"common/diplomatic_plays/chi_adm_{feature}.txt")


def choices_and_settlement_checks():
    f = Fixture()
    leader, ally, court = f.leader, f.ally, f.court
    court.variables.update({
        PREFIX + "phase": 2, PREFIX + "claimant": leader, PREFIX + "readiness": 40,
        PREFIX + "evidence": 75, PREFIX + "native_started": True,
    })
    leader.variables[PREFIX + "faction"] = 1
    ai_review = get(E[PREFIX + "ai_review"], "if")
    recruitment = get(ai_review, "every_subject_or_below")
    arm = next(
        get(branch, "limit") for _, _, branch in recruitment
        if isinstance(branch, list) and named(branch, "FACTION", "1")
    )
    assert not f.test(arm, ally), "Low loyalty alone must not enlist an AI province."
    ally.variables["chi_adm_loyalty"] = 30
    assert f.test(arm, ally)
    ally.variables["chi_adm_corruption"] = 65
    assert not f.test(arm, ally)
    ally.variables["chi_adm_corruption"] = 25
    ally.fields["claimant_relations"] = -60
    assert not f.test(arm, ally)

    court.variables[PREFIX + "phase"] = 5
    recording_gate = get(get(E[PREFIX + "record_victory"], "if"), "limit")
    assert f.test(recording_gate, court)
    outcomes = E[PREFIX + "resolve"]
    for pending, expected in ((1, "1"), (2, "2"), (None, "6")):
        if pending is None:
            court.variables.pop(PREFIX + "pending_result")
        else:
            court.variables[PREFIX + "pending_result"] = pending
            assert not f.test(recording_gate, court), "A later goal must not replace the first enforced result."
        branch = next(branch for key, _, branch in outcomes if key == "else" or f.test(get(branch, "limit"), court))
        assert all_values(branch, "RESULT") == [expected]
        assert named(branch, PREFIX + "install_ruler", "yes") == (pending == 1)
    court.fields["chi_adm_court_valid"] = False
    invalid = next(branch for key, _, branch in outcomes if key == "else" or f.test(get(branch, "limit"), court))
    assert all_values(invalid, "RESULT") == ["5"]


if __name__ == "__main__":
    source_checks()
    political_checks()
    engine_wiring_checks()
    choices_and_settlement_checks()
    print("PASS imperial security: sources, localization, journals, politics, coalition, strength, consent, play and settlement wiring.")
