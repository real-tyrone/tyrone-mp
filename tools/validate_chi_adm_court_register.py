from chi_adm_authorized_validation import authorized_current
"""court register structural/binding/regression checks. Not an engine or rendering test."""
from pathlib import Path
import hashlib
import json
import re
import sys

sys.dont_write_bytecode = True
import validate_chi_adm as foundation

ROOT = Path(__file__).resolve().parents[1]
GUI = ROOT / "gui/journal_entry_widgets"
LOC = ROOT / "localization/english/chi_adm_l_english.yml"


def text(path):
    return (ROOT / path).read_text("utf-8-sig")


def gui_nodes(source):
    """Small GUI block/attribute scanner; intentionally not a Jomini parser."""
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|#[^\n]*|[{}=]|[^\s{}=]+', source)
    tokens = [token for token in tokens if not token.startswith("#")]
    stack, nodes = [], []
    for i, token in enumerate(tokens):
        if token == "{":
            kind = tokens[i - 2] if i >= 2 and tokens[i - 1] == "=" else tokens[i - 1]
            node = {"kind": kind, "attrs": {}, "parent": stack[-1] if stack else None, "start": i, "children": []}
            if stack:
                stack[-1]["children"].append(node)
            nodes.append(node)
            stack.append(node)
        elif token == "}":
            assert stack, "Unexpected closing GUI brace"
            node = stack.pop()
            node["tokens"] = tokens[node["start"] + 1:i]
        elif stack and i + 2 < len(tokens) and tokens[i + 1] == "=" and tokens[i + 2] != "{":
            stack[-1]["attrs"][token] = tokens[i + 2].strip('"')
    assert not stack, "Unclosed GUI block"
    return nodes


def check_model_structure(source):
    nodes = gui_nodes(source)
    for node in nodes:
        attrs = node["attrs"]
        if "datamodel" in attrs:
            # Confirmed runtime failure: named root-model construction differs
            # from native Great Game/Promise's nested model/item structure.
            assert not ("name" in attrs and node["parent"] is None), "Named GUI root has a direct datamodel"
            # Confirmed crash-session rejection at ledger line 217. Use the
            # installed diplomatic-overview's AccessPlayer subject accessor.
            if "GetSubjects" in attrs["datamodel"]:
                assert attrs["datamodel"] == "[AccessPlayer.GetSubjects]", "Unverified read-only subject model"
        if node["kind"] == "item":
            assert node["parent"] and "datamodel" in node["parent"]["attrs"], "Orphaned GUI item"
        if node["kind"] == "journal_entry" and "datacontext" in attrs:
            assert attrs["datacontext"] == "[AccessPlayer.GetJournalEntry(JournalEntryType.Self)]", "Avoid a self-referencing JournalEntry datacontext"
    return nodes


def repair_regression_fixtures():
    broken = [
        'flowcontainer = { name = "broken" datamodel = "[AccessPlayer.GetGroupsForActiveJournalEntries]" item = { widget = {} } }',
        'flowcontainer = { flowcontainer = { datamodel = "[JournalEntry.GetCountry.GetSubjects]" item = { widget = {} } } }',
        'flowcontainer = { item = { widget = {} } }',
    ]
    for source in broken:
        try:
            check_model_structure(source)
        except AssertionError:
            pass
        else:
            raise AssertionError("Validator accepted a known broken GUI pattern")


def main():
    foundation.static_checks()
    foundation.model_checks()
    baseline = json.loads(text("tools/chi_adm_court_register_baseline.json"))
    for path, digest in baseline.items():
        assert (hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest) or authorized_current(path), path

    # There are three functional UI JEs, not one JE per administration.
    entries = foundation.definitions("common/journal_entries/chi_adm_court_register_governance.txt")
    assert set(entries) == {"chi_adm_court_register_court", "chi_adm_court_register_ledger", "chi_adm_court_register_memorial_desk"}
    groups = foundation.definitions("common/journal_entry_groups/chi_adm_court_register_groups.txt")
    assert set(groups) == {"je_group_chi_adm_court_register_court", "je_group_chi_adm_court_register_province"}
    native = text("gui/journal_entry_widgets/chi_adm_court_register_subentries.gui")
    assert native.count("journal_entry = {") == 2
    assert native.count('[AccessPlayer.GetGroupsForActiveJournalEntries]') == 2
    assert native.count('[JournalEntryGroup.GetActiveJournalEntryTypes(GetPlayer.Self)]') == 2
    assert native.count('[AccessPlayer.GetJournalEntry(JournalEntryType.Self)]') == 2
    assert "JournalEntry.GetCountry.GetJournalEntry" not in native
    check_model_structure(native)
    repair_regression_fixtures()

    parent = foundation.definitions("common/journal_entries/chi_adm_governance.txt")["chi_adm_governance"]
    assert foundation.get(parent, "group") == "je_group_chi_adm_court_register_province"
    desk = entries["chi_adm_court_register_memorial_desk"]
    assert [v for k, _, v in desk if k == "scripted_button"] == list(foundation.BUTTONS) + ["chi_adm_memorials_file_" + kind for kind in ("relief", "discretion", "military")]
    assert not any(k == "scripted_button" for k, _, _ in parent), "Duplicate action section"
    assert 'name = "chi_adm_foundation"' in text("common/journal_entries/chi_adm_governance.txt")

    # Check eligibility against the actual core helpers and actual initial tags.
    gui_filter = foundation.definitions("common/scripted_guis/chi_adm_court_register_gui.txt")
    valid = foundation.get(gui_filter["chi_adm_court_register_subject_visible"], "is_valid")
    assert valid == [("chi_adm_target_valid", "=", "yes")]
    visible = []
    for tag in foundation.TAGS + ["TIB", "KOR", "LAN", "CHI", "JAP"]:
        p = foundation.Province(tag)
        foundation.execute(foundation.EFFECTS["chi_adm_initialize"], p)
        if foundation.condition(valid, p):
            visible.append(tag)
        p.subject = False
        assert not foundation.condition(valid, p), "Former subject left in ledger"
    assert visible == foundation.TAGS and len(visible) == len(foundation.TAGS)
    starting_pacts = dict(re.findall(r"create_diplomatic_pact\s*=\s*\{\s*country\s*=\s*c:(\w+)\s+type\s*=\s*(qing_\w+)", text("common/history/global/zzzz_qing_administrations.txt")))
    for tag in foundation.TAGS:
        expected = "qing_frontier_administration" if tag in foundation.FRONTIER else "qing_civil_administration" if tag in {"SHN", "SHA", "QHN"} else "qing_viceroyalty_administration"
        assert starting_pacts[tag] == expected, (tag, starting_pacts[tag])
    for key in ("chi_adm_court_register_court", "chi_adm_court_register_ledger"):
        assert ("c:CHI", "?=", "this") in foundation.get(entries[key], "possible")
    assert ("chi_adm_target_valid", "=", "yes") in foundation.get(desk, "possible")

    ledger = text("gui/journal_entry_widgets/chi_adm_court_register_ledger.gui")
    assert ledger.count('datamodel = "[AccessPlayer.GetSubjects]"') == 2
    assert "GetScriptedGui('chi_adm_court_register_subject_visible')" in ledger
    assert "GetVariableSystem.Set('chi_adm_court_register_selected', Country.GetNameNoFormatting)" in ledger
    assert "GetVariableSystem.HasValue('chi_adm_court_register_selected', Country.GetNameNoFormatting)" in ledger
    assert "JournalEntry.GetCountry.GetSubjects" not in ledger
    for kind in foundation.KINDS:
        assert ledger.count(f"value = \"[FixedPointToFloat(Country.MakeScope.Var('chi_adm_{kind}').GetValue)]\"") == 2
    # Single shared portrait definition; not fifteen hardcoded portrait widgets.
    assert ledger.count("character_portrait_base_torso = {") == 1
    assert 'datacontext = "[Country.GetRuler]"' in ledger
    assert "Character.GetFullNameNoFormatting" in ledger
    assert "Character.GetInterestGroup.GetName" not in ledger  # localized instead
    assert "Character.AccessTraits" in ledger and "FancyTooltip_CharacterTrait" in ledger
    assert "Country.GetRuler.IsValid" in ledger and "Character.GetInterestGroup.IsValid" in ledger
    portrait = next(node for node in gui_nodes(ledger) if node["kind"] == "character_portrait_base_torso")
    assert any(child["kind"] == "size" and child["tokens"] == ["160", "188"] for child in portrait["children"]), "Zero-sized portrait wrapper"
    assert 'blockoverride "portrait_size" { size = { 160 188 } }' in ledger
    assert "set_variable" not in ledger and "Execute(" not in ledger

    localization = LOC.read_text("utf-8-sig")
    keys = set(re.findall(r"^\s*(\w+):", localization, re.M))
    assert "[Character.GetInterestGroup.GetName]" in localization
    assert "[Country.GetRelationsWith(Country.GetOverlord)|+=]" in localization
    desk_gui=text("gui/journal_entry_widgets/chi_adm_court_register_memorial_desk.gui")
    assert "Country.GetRelationsTooltip(Country.GetOverlord.Self)" in desk_gui
    assert "Country.GetRelationsIconTexture(Country.GetOverlord.Self)" in desk_gui
    assert "Country.GetRelationsWithDesc(Country.GetOverlord)" in localization
    custom = foundation.definitions("common/customizable_localization/chi_adm_court_register_gui.txt")
    refs = set()
    for body in custom.values():
        for key, _, value in body:
            if key == "text":
                refs.add(foundation.get(value, "localization_key"))
    for name, body in entries.items():
        refs.update((name, name + "_reason", name + "_status"))
        refs.add(foundation.get(body, "group"))
        refs.add(foundation.get(foundation.get(foundation.get(body, "activation_description"), "custom_tooltip"), "text"))
        for key, _, widget in body:
            if key == "widget":
                source = text(foundation.get(widget, "gui").strip('"'))
                assert f'name = {foundation.get(widget, "name")}' in source
    game = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
    # Installed native precedents, not a claim that static checks render a GUI.
    character_templates = (game / "gui/shared/character.gui").read_text("utf-8-sig")
    assert 'type character_portrait_base_torso = character_portrait_base {' in character_templates
    assert "Character.GetAnimatedPortrait('characters_portrait_environment', 'camera_torso'" in character_templates
    check_model_structure((game / "gui/journal_entry_widgets/great_game_widgets.gui").read_text("utf-8-sig"))
    for path in sorted(GUI.glob("chi_adm_court_register*.gui")):
        source = path.read_text("utf-8")
        check_model_structure(source)
        # Narrow structural checks on GUI templates without pretending to parse Jomini.
        tokens = re.sub(r'"[^"\n]*"|#[^\n]*', "", source)
        balance = 0
        for char in tokens:
            balance += (char == "{") - (char == "}")
            assert balance >= 0, path
        assert balance == 0 and source.count("[") == source.count("]"), path
        refs.update(re.findall(r'(?:text|tooltip)\s*=\s*"(chi_adm_court_register_\w+)"', source))
        for asset in re.findall(r'(?:texture|progresstexture|noprogresstexture)\s*=\s*"(gfx/[^"\[]+)"', source):
            assert (ROOT / asset).exists() or (game / asset).exists(), asset
        for local_var in re.findall(r"GetCustom\('(chi_adm_court_register_\w+)'\)", source):
            assert local_var in custom
    assert refs <= keys, f"Missing localization: {refs - keys}"
    for key in keys:
        if key.startswith("chi_adm_court_register_") or key.startswith("je_group_chi_adm_court_register_"):
            assert len(re.findall(r"^\s*" + key + r":", localization, re.M)) == 1
    for path in (ROOT / "localization/english").rglob("*.yml"):
        if path != LOC:
            assert not re.search(r"^\s*(?:chi_adm_court_register_|je_group_chi_adm_court_register_)\w*:", path.read_text("utf-8-sig"), re.M), path
    # No new simulation effect, polling, money transfer, or province-changing action.
    for path in (ROOT / "common").glob("*/chi_adm_court_register*.txt"):
        source = path.read_text("utf-8")
        assert not re.search(r"\b(?:effect|on_monthly_pulse|on_daily_pulse|set_variable|annex|income_transfer)\s*=", source), path
    outcome = foundation.get(parent, "outcome")
    assert foundation.get(outcome, "header") == "chi_adm_court_register_service_end_header"
    assert foundation.get(foundation.get(outcome, "effect"), "hidden_effect") == [("chi_adm_cleanup", "=", "yes")]
    assert foundation.get(foundation.get(outcome, "effect"), "custom_tooltip") in keys
    print("PASS court register repair: known broken model fixtures rejected; native nested models/accessors; nonzero torso portrait; hidden cleanup; 13 subjects and provincial accounts mechanics preserved")
    print("PENDING: native JE activation/expansion, scrolling, portrait framing, ruler succession and 1080p/MP checks in Victoria 3.")


if __name__ == "__main__":
    main()
