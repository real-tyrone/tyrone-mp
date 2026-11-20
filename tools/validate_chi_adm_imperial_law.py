from chi_adm_authorized_validation import authorized_current
"""imperial law reform source checks + bounded interpreter of the actual directive effects.

Native law legality is an injected engine result, not reimplemented here. This
does not prove Victoria 3 runtime, GUI rendering or multiplayer compatibility.
"""
from pathlib import Path
import hashlib
import json
import re
import sys

sys.dont_write_bytecode = True
import validate_chi_adm as core
import validate_chi_adm_court_register as ui
from validate_chi_adm_government_titles import Country

ROOT = Path(__file__).resolve().parents[1]
GAME = Path(r"C:\Program Files (x86)\Steam\steamapps\common\Victoria 3\game")
LAWS = json.loads((ROOT / "tools/chi_adm_imperial_law_catalog.json").read_text())
IDS = {x["law"]: x["id"] for x in LAWS}
GROUP = {x["id"]: x["group"] for x in LAWS}
EFFECTS = core.definitions("common/scripted_effects/chi_adm_imperial_law.txt")
TRIGGERS = core.definitions("common/scripted_triggers/chi_adm_imperial_law.txt")
# Compile the generated disjoint ID guards as a jump table. Each selected branch
# is still evaluated from its actual AST; this avoids a cubic Python scan that
# does not represent the engine's compiled scripted-trigger execution.
MATCH_BRANCHES = {int(core.get(core.get(body, 'owner'), 'var:chi_adm_imperial_law_law_id')): body
                  for _, _, body in core.get(TRIGGERS['chi_adm_imperial_law_matches_request'], 'OR')}
BUTTONS = core.definitions("common/scripted_buttons/chi_adm_imperial_law.txt")
VALUES = {k: float(v) for k, v in core.definitions("common/script_values/chi_adm_imperial_law.txt").items() if isinstance(v, str)}


def read(path):
    return (ROOT / path).read_text("utf-8-sig")


def static_checks():
    mods=core.definitions('common/static_modifiers/chi_adm_imperial_law.txt')
    assert mods['chi_adm_imperial_law_enactment_support']==[]
    assert mods['chi_adm_imperial_law_implementation_lock']==[('country_cannot_start_law_enactment_bool','=','yes')]
    baseline = json.loads(read("tools/chi_adm_imperial_law_baseline.json"))
    for path, digest in baseline["files"].items():
        assert (hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest) or authorized_current(path), path
    original_on = core.load("common/on_actions/tyrone_qing_administrations.txt")
    untouched = [x for x in original_on if x[0] != "chi_qing_apply_imperial_law"]
    assert hashlib.sha256(json.dumps(untouched, sort_keys=True).encode()).hexdigest() == baseline["on_action_unmodified_ast_hash"]
    propagation = dict((k, v) for k, _, v in original_on)["chi_qing_apply_imperial_law"]
    assert core.get(propagation, "effect") == [("chi_adm_imperial_law_dispatch", "=", "yes")]
    assert "c:CHI ?= this" in read("common/on_actions/tyrone_qing_administrations.txt")
    native_event = (ROOT / "events/law_imposition_events.txt").read_bytes()
    guards = b'\n\t\tNOT = { chi_adm_imperial_law_native_request = yes }\n\t\tNOT = { has_variable = chi_adm_imperial_law_native_redirected }'
    assert native_event.count(guards) == 1
    assert hashlib.sha256(native_event.replace(guards, b"")).hexdigest() == baseline["old_native_event_hash"]
    native_rights = core.definitions("common/scripted_triggers/zz_chi_adm_imperial_law_native_rights.txt")["REPLACE:can_impose_law_default"]
    vanilla_rights = core.definitions(GAME / "common/scripted_triggers/00_scripted_triggers.txt")["can_impose_law_default"]
    assert core.get(native_rights, "OR")[0] == ("AND", "=", vanilla_rights)
    assert len(core.get(native_rights, "OR")) == 2
    assert "country_cannot_start_law_enactment_bool = yes" in read("common/static_modifiers/chi_adm_imperial_law.txt")
    assert "scope:law" in read("common/on_actions/chi_adm_imperial_law.txt") or "imposed_law" in read("common/on_actions/chi_adm_imperial_law.txt")
    import generate_chi_adm_imperial_law_laws as registry
    registry.CHECK = True
    registry.main()
    effective = registry.discover()
    assert set(IDS) == set(effective)
    assert len(IDS) == len(set(IDS.values()))
    assert {law:IDS[law] for law in ('law_local_police','law_dedicated_police','law_per_capita_based_taxation','law_proportional_taxation')} == dict(law_local_police=1,law_dedicated_police=2,law_per_capita_based_taxation=3,law_proportional_taxation=4)
    for row in LAWS:
        assert MATCH_BRANCHES[row['id']] == [('owner','=',[(f'var:chi_adm_imperial_law_law_id','=',str(row['id']))]),('type','=',f"law_type:{row['law']}")]
    assert {x['group'] for x in LAWS} == {core.get(body, 'group') for _, body in effective.values()}
    assert not re.search(r'chi_adm_frontier', g_dispatch := json.dumps(EFFECTS['chi_adm_imperial_law_dispatch']))
    assert "can_be_enacted = yes" in read("common/scripted_triggers/chi_adm_imperial_law.txt")
    assert "law_is_available = yes" in read("common/scripted_triggers/chi_adm_imperial_law.txt")
    for name, body in EFFECTS.items():
        encoded = json.dumps(body)
        if "activate_law" in encoded:
            assert name in ("chi_adm_imperial_law_immediate", "chi_adm_imperial_law_finish_implementation")
        if "cancel_enactment" in encoded:
            assert name == "chi_adm_imperial_law_prioritize"
        if "start_enactment" in encoded:
            assert name == "chi_adm_imperial_law_start"
    assert core.get(core.get(BUTTONS["chi_adm_imperial_law_immediate_button"], "effect"), "hidden_effect") == [("chi_adm_imperial_law_immediate", "=", "yes")]
    eligible = []
    for tag in core.TAGS + ["TIB", "KOR", "LAN", "JAP"]:
        country = Country(tag)
        core.execute(core.EFFECTS["chi_adm_initialize"], country)
        if core.condition(TRIGGERS["chi_adm_imperial_law_civil"], country):
            eligible.append(tag)
    assert set(eligible) == set(core.TAGS) and len(eligible) == len(core.TAGS)
    events = core.definitions("events/chi_adm_imperial_law.txt")
    for name in ("chi_adm_imperial_law_law.1",):
        option = core.get(events[name], "option")
        assert {k for k, _, _ in option} == {"name", "default_option"}, "Acknowledgement must never authorize a law"
    assert core.get(events["chi_adm_imperial_law_law.90"], "immediate") == [("chi_adm_imperial_law_start", "=", "yes")]
    entries = core.definitions("common/journal_entries/chi_adm_imperial_law.txt")
    assert len(entries) == 2
    assert core.get(entries["chi_adm_imperial_law_directive"], "group") == "je_group_chi_adm_court_register_province"
    assert core.get(entries["chi_adm_imperial_law_court_register"], "group") == "je_group_chi_adm_court_register_court"
    gui = read("gui/journal_entry_widgets/chi_adm_imperial_law.gui")
    ui.check_model_structure(gui)
    assert 'chi_adm_imperial_law_court_register' not in gui
    assert core.get(entries['chi_adm_imperial_law_court_register'], 'possible') == [('always','=','no')]
    assert 'datacontext = "[JournalEntry.GetCountry]"' in gui
    assert 'custom_widget_container_buttons' in read('common/journal_entries/chi_adm_imperial_law.txt')
    assert gui.count('JournalEntry.GetScriptedButtons') == 3
    assert 'ScriptedButton.ExecuteEffect' in gui
    loc = read("localization/english/chi_adm_l_english.yml")
    keys = re.findall(r'^\s*(chi_adm_imperial_law_\w+):', loc, re.M)
    assert len(keys) == len(set(keys))
    for line in loc.splitlines():
        if re.match(r"\s*chi_adm_imperial_law_\w+:", line):
            assert line.count('"') == 2 and line.count("[") == line.count("]"), line
    refs = set(re.findall(r'(?:text|tooltip|title|desc|name|conclusion_desc)\s*=\s*"?(chi_adm_imperial_law_\w+)"?', gui))
    for path in [*ROOT.glob("common/*/chi_adm_imperial_law*.txt"), ROOT / "events/chi_adm_imperial_law.txt"]:
        source = path.read_text("utf-8-sig")
        core.definitions(path)
        refs.update(re.findall(r'(?:text|title|desc|name|localization_key|conclusion_desc)\s*=\s*"?(chi_adm_imperial_law_\w+)"?', source))
    # 'name' is also used for internal variables; only direct string references need loc.
    refs = {key for key in refs if key in keys or key.endswith(("_button", "_desc", "_result", "_title", "_tooltip"))}
    assert refs <= set(keys), refs - set(keys)
    for path in (ROOT / "localization/english").rglob("*.yml"):
        if path.name != "chi_adm_l_english.yml":
            assert not re.search(r'^\s*chi_adm_imperial_law_\w+:', path.read_text("utf-8-sig"), re.M), path
    for x in LAWS:
        assert f"[GetLawType('{x['law']}').GetName]" in loc
        assert f"[Country.GetActiveLawFromGroup('{x['group']}').GetName]" in loc
    timers=core.definitions('events/chi_adm_imperial_law_implementation.txt')
    for row in LAWS:
        event=timers['chi_adm_imperial_law_law.'+str(1000+row['id'])]
        assert ('var:chi_adm_imperial_law_law_id','=',str(row['id'])) in core.get(event,'trigger')
        assert core.get(event,'immediate')==[('chi_adm_imperial_law_finish_implementation','=','yes')]
    schedules=EFFECTS['chi_adm_imperial_law_schedule_implementation']
    assert len(schedules)==len(LAWS)
    for key,op,body in schedules:
        assert core.get(core.get(body,'trigger_event'),'months')=='12'
    assert 'start_enactment' not in json.dumps(EFFECTS)
    assert 'add_enactment_modifier' not in json.dumps(EFFECTS)
    print(f"PASS imperial law reform static: all {len(LAWS)} effective laws, all law groups; generator freshness, stable IDs, native route, automatic requests to all 15, retired docket and preserved setup/GUI/governments")


class Simulation:
    """Execute actual imperial law reform effect/trigger trees with a small native-engine adapter."""
    def __init__(self):
        self.v = {"chi_adm_loyalty": 70, "chi_adm_autonomy": 25, "chi_adm_corruption": 25}
        self.eligible = True
        self.monarchy = True
        self.court_monarchy = True
        self.court_ai = False
        self.court_exists = True
        self.native = False
        self.frontier = False
        self.foreign_je = False
        self.actual = {"lawgroup_policing": 1, "lawgroup_taxation": 0}
        self.court_laws = {"lawgroup_policing": 2, "lawgroup_taxation": 4}
        self.legal = {1, 2, 3, 4}
        self.available = {1, 2, 3, 4}
        self.enacting = None
        self.bound = None
        self.bonus = False
        self.mods = set()
        self.court_mods = set()
        self.journals = set()
        self.relations = 80
        self.history = []

    def num(self, value, actor="province"):
        if value in VALUES:
            return VALUES[value]
        if value.startswith("var:"):
            return self.v.get(value[4:], 0)
        if value == "authority":
            return 100 - (25 if "chi_adm_imperial_law_court_workload" in self.court_mods else 0)
        if value == "relative_bureaucracy":
            return .25
        if value.endswith("target_law.type"):
            return self.bound
        return float(value)

    def cond(self, items, actor="province", law=None, owner="province"):
        out = []
        for key, op, value in items:
            if key == "custom_tooltip":
                result = self.cond([x for x in value if x[0] != "text"], actor, law, owner)
            elif key in ("OR", "AND", "NOT"):
                parts = (self.cond([x], actor, law, owner) for x in value)
                result = any(parts) if key == "OR" else not all(parts) if key == "NOT" else all(parts)
            elif key == "chi_adm_imperial_law_civil":
                result = (self.eligible and self.court_exists) == (value == "yes")
            elif key == 'chi_adm_frontier':
                result = self.frontier == (value == 'yes')
            elif key == 'chi_adm_imperial_law_matches_request':
                branch = MATCH_BRANCHES.get(self.v.get('chi_adm_imperial_law_law_id'))
                result = (branch is not None and self.cond(branch,actor,law,owner)) == (value == 'yes')
            elif key in TRIGGERS:
                result = self.cond(TRIGGERS[key], actor, law, owner) == (value == "yes")
            elif key == "owner":
                result = self.cond(value, owner)
            elif key == "c:CHI":
                result = (actor == "court") if value == "this" else self.court_exists and self.cond(value, "court")
            elif key == "scope:chi_adm_imperial_law_native_law":
                result = self.cond(value, "law", self.bound)
            elif key == "imposed_law":
                result = self.native and self.cond(value, "law", 2)
            elif key == "imposer_of_law":
                result = self.native and self.cond(value, "court")
            elif key == "any_law":
                result = any(self.cond(value, "law", x["id"], actor) for x in LAWS)
            elif key == "currently_enacting_law":
                result = self.enacting is not None and self.cond(value, "law", self.enacting)
            elif key == "type":
                result = law == IDS[value.removeprefix("law_type:")]
            elif key == "can_be_enacted":
                result = (law in self.legal and self.enacting is None) == (value == "yes")
            elif key == "law_is_available":
                result = (law in self.available) == (value == "yes")
            elif key == "has_law":
                ident = IDS[value.removeprefix("law_type:")]
                result = (self.court_laws if actor == "court" else self.actual).get(GROUP[ident]) == ident
            elif key == "enacting_any_law":
                result = (self.enacting is not None) == (value == "yes")
            elif key == "has_variable":
                result = value in self.v
            elif key == "has_journal_entry":
                result = self.foreign_je if value == "je_law_imposition" else value in self.journals
            elif key == "has_modifier":
                result = value in (self.court_mods if actor == "court" else self.mods)
            elif key == "exists":
                result = self.court_exists if value == "c:CHI" else self.native
            elif key == "is_ai":
                result = self.court_ai == (value == "yes")
            elif key == "is_at_war":
                result = value == "no"
            elif key.startswith("modifier:"):
                result = value == "no"
            else:
                a, b = self.num(key, actor), self.num(value, actor)
                result = {"=": a == b, "<=": a <= b, ">=": a >= b, "<": a < b, ">": a > b}[op]
            out.append(result)
        return all(out)

    def run(self, items, actor="province", law=None, params=None, owner="province"):
        params = params or {}
        def expand(value):
            if isinstance(value, list):
                return [(expand(k), op, expand(v)) for k, op, v in value]
            for key, replacement in params.items():
                value = value.replace("$" + key + "$", str(replacement))
            return value
        items = expand(items)
        taken = False
        for key, _, value in items:
            if key in ("if", "else_if", "else"):
                if key == "if":
                    taken = False
                if not taken and (key == "else" or self.cond(core.get(value, "limit"), actor, law, owner)):
                    self.run([x for x in value if x[0] != "limit"], actor, law, owner=owner)
                    taken = True
            elif key in EFFECTS:
                args = {k: v for k, _, v in value} if isinstance(value, list) else {}
                self.run(EFFECTS[key], actor, law, args, owner)
            elif key.startswith("chi_adm_adjust_"):
                target = key.removeprefix("chi_adm_adjust_")
                self.v["chi_adm_" + target] = max(0, min(100, self.v["chi_adm_" + target] + self.num(core.get(value, "AMOUNT"))))
            elif key == "set_variable":
                if isinstance(value, str):
                    self.v[value] = 1
                else:
                    self.v[core.get(value, "name")] = self.num(next((v for k, _, v in value if k == "value"), "1"))
            elif key == "remove_variable":
                self.v.pop(value, None)
            elif key == "change_variable":
                target = core.get(value, "name")
                for operation, _, amount in value:
                    if operation == "add":
                        self.v[target] += self.num(amount)
                    elif operation == "subtract":
                        self.v[target] -= self.num(amount)
            elif key == "every_law":
                for candidate in LAWS:
                    if self.cond(core.get(value, "limit"), "law", candidate["id"], actor):
                        self.run([x for x in value if x[0] != "limit"], "law", candidate["id"], owner=actor)
            elif key == "save_scope_as":
                if actor == "law":
                    self.bound = law
            elif key == "c:CHI":
                self.run(value, "court")
            elif key == "owner":
                self.run(value, owner)
            elif key == "imposed_law":
                assert self.native
                self.run(value, "law", 2)
            elif key == "cancel_imposition":
                self.native = False
            elif key == "every_subject_or_below":
                if self.cond(core.get(value, "limit")):
                    self.run([x for x in value if x[0] != "limit"])
            elif key == "start_enactment":
                assert self.enacting is None, "Unaccepted replacement of active enactment"
                self.enacting = self.num(value)
                self.history.append(("start", self.enacting))
            elif key == "cancel_enactment":
                self.history.append(("cancel", self.enacting))
                self.enacting = None
            elif key == "activate_law":
                ident = self.num(value)
                self.actual[GROUP[ident]] = ident
                self.history.append(("activate", ident))
            elif key == "add_enactment_modifier":
                assert self.enacting == self.v["chi_adm_imperial_law_law_id"]
                self.bonus = True
            elif key == "remove_enactment_modifier":
                self.bonus = False
            elif key == "remove_modifier":
                self.mods.discard(value)
            elif key == "add_modifier":
                (self.court_mods if actor == "court" else self.mods).add(core.get(value, "name"))
            elif key == "add_journal_entry":
                self.journals.add(core.get(value, "type"))
            elif key == "trigger_event":
                # The real acknowledgement events are source-checked to have no effects.
                pass
            elif key == "change_relations":
                self.relations += self.num(core.get(value, "value"))
            elif key == "hidden_effect":
                self.run(value, actor, law, owner=owner)
            elif key == "custom_tooltip":
                pass
            else:
                raise AssertionError("Unmodelled effect: " + key)

    def effect(self, name, **params):
        self.run(EFFECTS["chi_adm_imperial_law_" + name], params=params)

    def receive(self, ident=2):
        self.effect("receive", ID=ident)

    def tick(self, count=1):
        for _ in range(count):
            if "chi_adm_imperial_law_active" in self.v:
                self.effect("monthly")


def model_checks():
    for row in LAWS:
        s=Simulation(); ident=row['id']; s.actual={row['group']:0}; s.court_laws={row['group']:ident}; s.available={ident}
        s.run(EFFECTS['chi_adm_imperial_law_dispatch'],'law',ident,owner='court')
        assert s.v['chi_adm_imperial_law_law_id']==ident and not s.history
        s.legal.clear(); s.effect('start')
        assert s.enacting is None and not s.history and not s.bonus
        assert 'chi_adm_imperial_law_implementation_lock' in s.mods
        s.effect('finish_implementation'); assert not s.history
        s.v.pop('chi_adm_imperial_law_implementation_wait') # delivered calendar event after 12 months
        s.effect('finish_implementation')
        assert s.actual[row['group']]==ident and s.v['chi_adm_loyalty']==73
        assert 'chi_adm_imperial_law_implementation_lock' not in s.mods
        s.effect('finish_implementation'); assert s.v['chi_adm_loyalty']==73
    s=Simulation(); s.enacting=99; s.receive(); s.effect('queue'); s.tick(3)
    assert s.enacting==99 and not s.history
    s.enacting=None; s.tick(); assert s.v['chi_adm_imperial_law_status']==3 and s.enacting is None
    s.v=json.loads(json.dumps(s.v)); s.tick(12)
    assert not s.history and 'chi_adm_imperial_law_implementation_lock' in s.mods
    s.v.pop('chi_adm_imperial_law_implementation_wait'); s.effect('finish_implementation'); assert s.actual[GROUP[2]]==2
    s=Simulation(); s.receive(); s.effect('start'); s.available.clear(); s.v.pop('chi_adm_imperial_law_implementation_wait'); s.effect('finish_implementation')
    assert s.v['chi_adm_imperial_law_status']==8 and not s.history and not s.mods
    s=Simulation(); s.enacting=99; s.receive(); s.effect('refuse'); s.effect('refuse')
    assert s.enacting==99 and s.v['chi_adm_loyalty']==55 and not s.mods
    s=Simulation(); s.receive(); s.effect('delay'); s.effect('delay'); assert s.v['chi_adm_loyalty']==67
    s=Simulation(); s.receive(); s.effect('petition'); s.effect('court_grant'); assert s.v['chi_adm_imperial_law_status']==6
    s=Simulation(); s.receive(); s.effect('start'); s.eligible=False; s.tick(); assert 'chi_adm_imperial_law_implementation_lock' not in s.mods
    s=Simulation(); s.enacting=99; s.receive(); s.effect('prioritize'); assert s.history==[('cancel',99)] and s.v['chi_adm_imperial_law_status']==3
    print(f'PASS timed implementation: all {len(LAWS)} laws, no normal enactment/bonus, locked until calendar completion, queue, refusal, hard restrictions, cleanup and once-only rewards')

if __name__ == '__main__':
    from validate_chi_adm_imperial_law_gui import checks as gui_checks
    gui_checks()
    static_checks()
    model_checks()
    print('PENDING: actual 12-month scheduling, native enactment lock, old-save migration and UI in game.')
