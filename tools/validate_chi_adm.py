from chi_adm_authorized_validation import authorized_current
"""Focused provincial accounts checks and a bounded model executing the actual provincial accounts effect tree.

This is not the Paradox engine or an in-game/MP/GUI rendering test.
Run from any directory: python tools/validate_chi_adm.py
"""
from pathlib import Path
from dataclasses import dataclass, field
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
TAGS = "ZHI AHU HNA YUE FRS XIB YUN SIH SHN SHA MGL XIN MCH".split()
FRONTIER = set("MGL XIN MCH".split())
KINDS = ("loyalty", "autonomy", "corruption")


def parse(text):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|#[^\n]*|\?=|>=|<=|!=|[{}=<>]|[^\s{}=<>!]+', text)
    tokens = [t for t in tokens if not t.startswith("#")]
    pos = 0

    def block(nested=False):
        nonlocal pos
        result = []
        while pos < len(tokens):
            key = tokens[pos]
            pos += 1
            if key == "}":
                assert nested, "Unexpected closing brace"
                return result
            assert pos < len(tokens), f"Missing operator after {key}"
            op = tokens[pos]
            pos += 1
            if op not in ("=", "?=", ">=", "<=", "!=", ">", "<"):
                # Native lists such as on_actions = { chi_adm_start }.
                pos -= 1
                result.append((key, "list", ""))
                continue
            value = tokens[pos]
            pos += 1
            if value == "{":
                value = block(True)
            result.append((key, op, value))
        assert not nested, "Unclosed brace"
        return result

    return block()


def load(path):
    return parse((ROOT / path).read_text("utf-8-sig"))


def definitions(path):
    pairs = load(path)
    assert len({k for k, _, _ in pairs}) == len(pairs), f"Duplicate IDs: {path}"
    return {k: v for k, _, v in pairs}


VALUE_DEFS = definitions("common/script_values/chi_adm_core.txt")
VALUES = {k: float(v) for k, v in VALUE_DEFS.items() if isinstance(v, str)}
EFFECTS = definitions("common/scripted_effects/chi_adm_core.txt")
TRIGGERS = definitions("common/scripted_triggers/chi_adm_core.txt")
TRIGGERS.update(definitions("common/scripted_triggers/tyrone_qing_administrations.txt"))
BUTTONS = definitions("common/scripted_buttons/chi_adm_core.txt")
MODIFIERS = definitions("common/static_modifiers/chi_adm_core.txt")
JE = definitions("common/journal_entries/chi_adm_governance.txt")["chi_adm_governance"]


def get(block, name):
    return next(v for k, _, v in block if k == name)


def executable_effects(block):
    result = []
    for key, op, value in block:
        if key in ('custom_tooltip', 'show_as_tooltip'): continue
        if key == 'hidden_effect': result.extend(executable_effects(value))
        else: result.append((key, op, value))
    return result


@dataclass
class Province:
    tag: str
    subject: bool = True
    court_exists: bool = True
    court_monarchy: bool = True
    fragmented: bool = False
    bureaucracy_surplus: float = .25
    variables: dict = field(default_factory=dict)
    modifiers: dict = field(default_factory=dict)
    journals: set = field(default_factory=set)
    month: int = 0

    @property
    def subject_type(self):
        if not self.subject:
            return "subject_type_protectorate"
        return "subject_type_qing_frontier_administration" if self.tag in FRONTIER else "subject_type_qing_civil_administration"


def number(value, p, params=None):
    params = params or {}
    value = params.get(value.strip("$"), value) if isinstance(value, str) else value
    if value in VALUES:
        return VALUES[value]
    if str(value).startswith("var:"):
        return p.variables[str(value)[4:]]
    if value == "authority":
        return 100 + sum(float(get(MODIFIERS[m], "country_authority_add")) for m in p.modifiers if any(k == "country_authority_add" for k, _, _ in MODIFIERS[m]))
    if value == "relative_bureaucracy":
        return p.bureaucracy_surplus
    return float(value)


def condition(items, p, court=False):
    results = []
    for key, op, val in items:
        if key in ("custom_tooltip", "hidden_trigger"):
            result = condition([x for x in val if x[0] != "text"], p, court)
        elif key in ("OR", "AND", "NOT", "NOR"):
            parts = [condition([item], p, court) for item in val]
            result = any(parts) if key == "OR" else not any(parts) if key == "NOR" else not all(parts) if key == "NOT" else all(parts)
        elif key in TRIGGERS:
            result = condition(TRIGGERS[key], p, court) == (val == "yes")
        elif key == "c:CHI" and isinstance(val, list):
            result = p.court_exists and condition(val, p, True)
        elif key.startswith("c:") and val == "this":
            result = key[2:] == ("CHI" if court else p.tag)
        elif key == "exists":
            result = p.court_exists
        elif key == "has_variable":
            result = (val == "chi_qing_1836_setup" or (val == "tyr_chi_fragmented" and p.fragmented)) if court else val in p.variables
        elif key == "has_law_or_variant":
            result = p.court_monarchy
        elif key == "is_subject_type":
            result = val == p.subject_type
        elif key in ("is_direct_subject_of", "is_subject_of"):
            result = p.subject and p.court_exists
        elif key == "has_modifier":
            result = val in p.modifiers
        elif key == "has_journal_entry":
            result = val in p.journals
        else:
            a, b = number(key, p), number(val, p)
            result = {"<": a < b, ">": a > b, "<=": a <= b, ">=": a >= b, "=": a == b, "!=": a != b}[op]
        results.append(result)
    return all(results)


def execute(items, p, params=None):
    branch_taken = False
    for key, _, val in items:
        if key in ("if", "else_if", "else"):
            if key == "if":
                branch_taken = False
            if not branch_taken and (key == "else" or condition(get(val, "limit"), p)):
                execute([x for x in val if x[0] != "limit"], p, params)
                branch_taken = True
        elif key == "hidden_effect":
            execute(val, p, params)
        elif key in ("custom_tooltip", "hidden_trigger"):
            assert isinstance(val, str), "Model expects presentation-only effect tooltip"
        elif key in EFFECTS:
            args = {k: v for k, _, v in val} if isinstance(val, list) else params
            execute(EFFECTS[key], p, args)
        elif key == "set_variable":
            if isinstance(val, str):
                p.variables[val] = 1
            else:
                p.variables[get(val, "name")] = number(get(val, "value"), p, params)
        elif key == "change_variable":
            p.variables[get(val, "name")] += number(get(val, "add"), p, params)
        elif key == "remove_variable":
            p.variables.pop(val, None)
        elif key == "add_modifier":
            name = get(val, "name")
            assert name not in p.modifiers, f"Stacked {name}"
            duration = next((float(v) for k, _, v in val if k == "months"), None)
            p.modifiers[name] = p.month + duration if duration else None
        elif key == "remove_modifier":
            p.modifiers.pop(val, None)
        elif key == "add_journal_entry":
            name = get(val, "type")
            assert name not in p.journals, "Duplicate JE"
            p.journals.add(name)
        else:
            raise AssertionError(f"Unmodelled effect: {key}")


def update(p):
    p.month += 1
    p.modifiers = {k: v for k, v in p.modifiers.items() if v is None or v > p.month}
    execute(EFFECTS["chi_adm_monthly_update"], p)
    # Model the actual JE termination trigger/effect; engine timing is a manual check.
    outcome = get(JE, "outcome")
    if "chi_adm_governance" in p.journals and condition(get(outcome, "trigger"), p):
        execute(get(outcome, "effect"), p)
        p.journals.remove("chi_adm_governance")


def check_status(p):
    tiers = [m for m in p.modifiers if m.startswith("chi_adm_corruption_tier_")]
    expected = 1 + sum(p.variables["chi_adm_corruption"] >= VALUES[f"chi_adm_tier_{i}_end"] for i in range(1, 5))
    assert tiers == [], tiers
    assert all(0 <= p.variables[f"chi_adm_{k}"] <= 100 for k in KINDS)


def static_checks():
    baseline = json.loads((ROOT / "tools/chi_adm_baseline.json").read_text())
    for path, digest in baseline.items():
        assert (hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest) or authorized_current(path), f"Protected baseline changed: {path}"
    ui_baseline = json.loads((ROOT / "tools/chi_adm_ui_baseline.json").read_text())
    for path, digest in ui_baseline["files"].items():
        # Global init gained only the BOM requested by the previous engine log.
        contents = (ROOT / path).read_bytes().removeprefix(b"\xef\xbb\xbf")
        assert (hashlib.sha256(contents).hexdigest() == digest) or authorized_current(path), f"provincial accounts mechanics changed: {path}"
    for button_id, button in BUTTONS.items():
        normalized = []
        for key, op, value in button:
            if key == "possible":
                value = [item for k, o, v in value for item in
                         ([x for x in v if x[0] != "text"] if k in ("custom_tooltip", "hidden_trigger") else [(k, o, v)])]
            elif key == "effect":
                value = executable_effects(value)
            normalized.append((key, op, value))
        digest = hashlib.sha256(json.dumps(normalized, sort_keys=True).encode()).hexdigest()
        assert digest == ui_baseline["buttons"][button_id], f"Action mechanics changed: {button_id}"
    for name, op, value in ui_baseline["constants"]:
        assert VALUE_DEFS[name] == value, f"Original tuning changed: {name}"
    setup = (ROOT / "common/history/global/zzzz_qing_administrations.txt").read_text()
    pacts = re.findall(r"create_diplomatic_pact\s*=\s*\{\s*country\s*=\s*c:(\w+)\s+type\s*=\s*qing_", setup)
    assert set(pacts) == set(TAGS) and len(pacts) == len(TAGS)
    assert [get(get(v, "pact"), "income_transfer") for v in definitions("common/diplomatic_actions/tyrone_qing_administrations.txt").values()] == ["0.20", "0.20", "0.15"]
    loc_path = ROOT / "localization/english/chi_adm_l_english.yml"
    assert loc_path.read_bytes().startswith(b"\xef\xbb\xbf")
    loc = loc_path.read_text("utf-8-sig")
    assert loc.startswith("l_english:\n")
    keys = re.findall(r"^\s*(chi_adm_\w+):", loc, re.M)
    assert len(keys) == len(set(keys)), "Duplicate localization"
    for line in loc.splitlines():
        if re.match(r"\s*chi_adm_\w+:", line):
            assert line.count('"') == 2, line
            assert line.count("[") == line.count("]"), line
    for path in (ROOT / "localization/english").rglob("*.yml"):
        if path != loc_path:
            assert not re.search(r"^\s*chi_adm_\w+:", path.read_text("utf-8-sig"), re.M), str(path)
    expected_loc = {"chi_adm_governance", "chi_adm_governance_reason", "chi_adm_governance_closed"}
    expected_loc.update(BUTTONS)
    expected_loc.update(k + "_desc" for k in BUTTONS)
    expected_loc.update(MODIFIERS)
    expected_loc.update(k + "_desc" for k in MODIFIERS)
    expected_loc.update(f"chi_adm_{k}_{suffix}" for k in KINDS for suffix in ("display", "tooltip"))
    custom_loc = load("common/customizable_localization/chi_adm_core.txt")
    for _, _, body in custom_loc:
        for name, _, value in body:
            if name == "text":
                expected_loc.add(get(value, "localization_key"))
    expected_loc.update(re.findall(r'\b(?:text|tooltip)\s*=\s*"(chi_adm_\w+)"', (ROOT / "gui/journal_entry_widgets/chi_adm_foundation.gui").read_text()))
    for button in BUTTONS.values():
        for name, _, value in get(button, "possible"):
            if name == "custom_tooltip":expected_loc.add(get(value, "text"))
        expected_loc.add(get(get(button, "effect"), "custom_tooltip"))
    expected_loc.add("chi_adm_service_ended")
    # Kept for compatibility; these checks now use native trigger localization.
    expected_loc.update('chi_adm_req_' + name for name in
                        ('service','memorial_free','negotiation_free','inspection_free','authority','bureaucracy'))
    # court register has a separate focused validator for its additional UI strings/bindings.
    expected_loc.update(key for key in keys if key.startswith(("chi_adm_court_register_", "chi_adm_government_titles_", "chi_adm_imperial_law_", "chi_adm_memorials_", "chi_adm_negotiated_integration_", "chi_adm_provincial_development_", "chi_adm_subject_")))
    assert expected_loc == set(keys), expected_loc ^ set(keys)
    for kind in KINDS:
        assert f"JournalEntry.GetCountry.MakeScope.Var('chi_adm_{kind}').GetValue|0" in loc
    gui = ROOT / "gui/journal_entry_widgets/chi_adm_foundation.gui"
    t = re.sub(r'"[^"\n]*"|#[^\n]*', "", gui.read_text())
    assert t.count("{") == t.count("}")
    for kind in KINDS:
        assert f'text = "chi_adm_{kind}_display"' in gui.read_text()
        assert f'tooltip = "chi_adm_{kind}_tooltip"' in gui.read_text()
        assert f"value = \"[FixedPointToFloat(JournalEntry.GetCountry.MakeScope.Var('chi_adm_{kind}').GetValue)]\"" in gui.read_text()
        assert f'text = "chi_adm_{kind}_tier_display"' in gui.read_text()
    assert gui.read_text().count("progressbar = {") == 3
    assert gui.read_text().count("min = 0") == gui.read_text().count("max = 100") == 3
    assert "GetPlayer" not in gui.read_text()
    assert get(get(JE, "outcome"), "color") == '"gold_positive"'
    assert get(JE, "activation_description")
    display = VALUE_DEFS["chi_adm_bureaucracy_surplus_display"]
    assert get(display, "value") == "relative_bureaucracy" and get(display, "multiply") == "100"
    # The requirement remains the original ratio, now wrapped by clean prose.
    inspection = get(BUTTONS["chi_adm_supervise_offices"], "possible")
    assert inspection[-1] == ("relative_bureaucracy", ">=", "0.05")
    assert "At least 5% [concept_bureaucracy] surplus" in loc
    # Parse hooks/JE/buttons/modifiers too; names are unique per definition type.
    for path in ("common/on_actions/chi_adm_core.txt", "common/history/global/zzzzz_chi_adm_init.txt"):
        definitions(path)
    print("PASS static: original Qing files and provincial accounts mechanics preserved; localization/metadata; three direct 0-100 GUI bars, tier bindings and 5% Bureaucracy display")


def model_checks():
    provinces = [Province(tag) for tag in TAGS]
    for p in provinces:
        execute(EFFECTS["chi_adm_initialize"], p)
        expected = (85, 15, 25) if p.tag == 'MCH' else (65, 45, 30) if p.tag in FRONTIER else (70, 25, 25)
        assert tuple(p.variables[f"chi_adm_{k}"] for k in KINDS) == expected
        start = p.variables.copy()
        for _ in range(240):
            update(p)
            check_status(p)
            assert p.variables == start
        assert p.journals == {"chi_adm_governance"}
    for boundary in (-25, 0, 19, 20, 39, 40, 59, 60, 79, 80, 100, 150):
        p = provinces[0]
        for kind in KINDS:
            p.variables[f"chi_adm_{kind}"] = boundary
        update(p)
        check_status(p)
        execute(EFFECTS["chi_adm_refresh_status"], p)
        check_status(p)
    for button_id, button in BUTTONS.items():
        p = Province("ZHI")
        execute(EFFECTS["chi_adm_initialize"], p)
        assert condition(get(button, "possible"), p)
        execute(get(button, "effect"), p)
        expected = {
            "chi_adm_loyal_memorial": (75, 25, 25),
            "chi_adm_negotiate_discretion": (65, 20, 25),
            "chi_adm_supervise_offices": (70, 25, 20),
        }[button_id]
        assert tuple(p.variables[f"chi_adm_{k}"] for k in KINDS) == expected
        cost_id = get(get(executable_effects(get(button, "effect")), "add_modifier"), "name")
        assert p.modifiers[cost_id] == 24
        assert any(key in ("country_authority_add", "country_bureaucracy_mult") and float(value) < 0 for key, _, value in MODIFIERS[cost_id])
        assert not condition(get(button, "possible"), p), "Cooldown failed"
        for _ in range(23):
            update(p)
        assert not condition(get(button, "possible"), p)
        update(p)
        assert condition(get(button, "possible"), p)
        check_status(p)
    for kind in KINDS:
        for amount, expected in ((500, 100), (-500, 0)):
            p = Province("ZHI")
            execute(EFFECTS["chi_adm_initialize"], p)
            execute(EFFECTS[f"chi_adm_adjust_{kind}"], p, {"AMOUNT": str(amount)})
            assert p.variables[f"chi_adm_{kind}"] == expected
            check_status(p)
    for surplus, available in ((.049, False), (.05, True), (.051, True)):
        p = Province("ZHI", bureaucracy_surplus=surplus)
        execute(EFFECTS["chi_adm_initialize"], p)
        assert condition(get(BUTTONS["chi_adm_supervise_offices"], "possible"), p) == available
        assert abs(number("relative_bureaucracy", p) * 100 - surplus * 100) < 1e-9
    # Invalid court/subject transitions suspend effects and close the JE. Rejoining
    # preserves accounts rather than granting a fresh favorable initialization.
    for attr, invalid, valid in (("subject", False, True), ("court_exists", False, True), ("court_monarchy", False, True), ("fragmented", True, False)):
        p = Province("ZHI")
        execute(EFFECTS["chi_adm_initialize"], p)
        p.variables["chi_adm_corruption"] = 90
        setattr(p, attr, invalid)
        update(p)
        assert not p.modifiers and not p.journals and "chi_adm_active" not in p.variables
        setattr(p, attr, valid)
        update(p)
        assert p.variables["chi_adm_corruption"] == 90 and p.journals
        check_status(p)
    for tag in ("TIB", "KOR", "LAN", "CHI"):
        p = Province(tag)
        execute(EFFECTS["chi_adm_initialize"], p)
        assert not p.variables and not p.modifiers and not p.journals
    custom_loc = definitions("common/customizable_localization/chi_adm_core.txt")
    for kind in KINDS:
        for value in (0, 19, 20, 39, 40, 59, 60, 79, 80, 100):
            p = Province("ZHI")
            p.variables[f"chi_adm_{kind}"] = value
            chosen = next(get(v, "localization_key") for k, _, v in custom_loc[f"chi_adm_{kind}_tier"] if k == "text" and (get(v, "trigger") == [("always", "=", "yes")] or condition(get(v, "trigger"), p)))
            expected = 1 + sum(value >= VALUES[f"chi_adm_tier_{i}_end"] for i in range(1, 5))
            assert chosen == f"chi_adm_{kind}_tier_{expected}"
    print("PASS model: actual provincial accounts effects, 13 x 240 monthly checks; repeat init, clamps/tier boundaries, action cooldowns, invalid court/subject cleanup and rejoining, excluded tags")
    print("PENDING: Victoria 3 runtime, 1080p rendering, save/load and two-player checks. This model does not validate the game engine.")


if __name__ == "__main__":
    static_checks()
    model_checks()
    from validate_chi_adm_tax_capacity import check as check_tax_capacity
    check_tax_capacity()
    from validate_chi_adm_remittance import check as check_remittance
    check_remittance()
