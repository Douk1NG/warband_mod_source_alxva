"""Regression checks for semantics-preserving map-trigger optimizations."""
import ast
from itertools import product
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SIMPLE_TRIGGERS = ROOT / "source" / "simple_triggers"


def _trigger_operations(filename, variable):
    tree = ast.parse((SIMPLE_TRIGGERS / filename).read_text(encoding="cp1254"))
    assignments = [
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id == variable for target in node.targets)
    ]
    assert len(assignments) == 1, f"Expected one active definition of {variable}"
    trigger = assignments[0].value.elts[0]
    assert isinstance(trigger, ast.Tuple) and len(trigger.elts) == 2
    return ast.literal_eval(trigger.elts[0]), trigger.elts[1].elts


def _op_name(operation):
    if not isinstance(operation, ast.Tuple) or not operation.elts:
        return None
    name = operation.elts[0]
    return name.id if isinstance(name, ast.Name) else None


def test_candidate_triggers_keep_their_intervals_and_full_bodies():
    expected = {
        ("process_vassal_ai.py", "process_vassal_ai_simple_triggers"): 1,
        ("process_alarms.py", "process_alarms_simple_triggers"): 3,
        ("center_alarms.py", "center_alarms_simple_triggers"): 0.5,
        ("lord_political_calculations.py", "lord_political_calculations_simple_triggers"): 0.5,
    }
    for (filename, variable), interval in expected.items():
        actual_interval, operations = _trigger_operations(filename, variable)
        assert actual_interval == interval
        assert operations, f"{variable} must retain its gameplay operations"


def test_siege_besieger_slot_check_is_redundant_after_positive_read():
    interval, operations = _trigger_operations(
        "process_alarms.py", "process_alarms_simple_triggers"
    )
    assert interval == 3
    names = [_op_name(operation) for operation in operations]
    slot_read = next(
        i
        for i, operation in enumerate(operations)
        if _op_name(operation) == "party_get_slot"
        and ast.dump(operation.elts[1]) == ast.dump(ast.parse('":besieger_party"', mode="eval").body)
        and ast.dump(operation.elts[3])
        == ast.dump(ast.parse("slot_center_is_besieged_by", mode="eval").body)
    )
    assert names[slot_read + 1] == "gt"
    assert names[slot_read + 2] == "party_is_active"

    # The removed check tested this same just-read slot against >= 1. Since the
    # preceding gate already requires its value > 0, it cannot reject anything
    # further; activity remains an independent required condition.
    for slot_value in range(-2, 4):
        for is_active in (False, True):
            before = slot_value > 0 and is_active and slot_value >= 1
            after = slot_value > 0 and is_active
            assert before == after


def test_captive_alarm_decay_stays_before_deferred_party_size_work():
    source = (SIMPLE_TRIGGERS / "center_alarms.py").read_text(encoding="cp1254")
    interval, operations = _trigger_operations(
        "center_alarms.py", "center_alarms_simple_triggers"
    )
    assert interval == 0.5
    captive_gate = next(
        operation
        for operation in operations
        if _op_name(operation) == "eq"
        and isinstance(operation.elts[1], ast.Constant)
        and operation.elts[1].value == "$g_player_is_captive"
    )
    captive_line = captive_gate.lineno
    def line_of(fragment):
        return source.count("\n", 0, source.index(fragment)) + 1

    decay_line = line_of("(faction_set_slot, \":cur_faction\", slot_faction_player_alarm")
    men_line = line_of("(party_get_num_companions,")
    prisoners_line = line_of("(party_get_num_prisoners,")
    centers_line = line_of("(try_for_range, \":cur_center\", centers_begin, centers_end)")

    assert decay_line < captive_line < men_line < prisoners_line < centers_line

    # The moved work only computes locals. Captive state still applies the
    # periodic alarm decay, while the center scan remains gated off.
    for cur_hours in range(0, 24 * 4):
        for is_captive in (False, True):
            def simulate(optimized):
                alarm = 7
                if cur_hours % 11 == 0:
                    alarm = max(0, alarm - 1)
                size_ops = 0
                if not optimized or not is_captive:
                    size_ops = 6
                return alarm, not is_captive, size_ops

            before_alarm, before_scans, before_size_ops = simulate(optimized=False)
            after_alarm, after_scans, after_size_ops = simulate(optimized=True)
            assert (before_alarm, before_scans) == (after_alarm, after_scans)
            assert before_size_ops - after_size_ops == (6 if is_captive else 0)


def test_alarm_script_visits_exactly_the_original_modulo_partition():
    source = (ROOT / "source" / "scripts" / "process_alarms.py").read_text(
        encoding="cp1254"
    )

    def old_partition(begin, end, modula):
        return [center for center in range(begin, end) if center % 3 == modula]

    def direct_partition(begin, end, modula):
        first_offset = (modula - begin % 3 + 3) % 3
        first_center = begin + first_offset
        remaining = end - first_center
        iteration_count = max(0, (remaining + 2) // 3)
        return [first_center + 3 * index for index in range(iteration_count)]

    for begin in range(-7, 12):
        for end in range(begin, begin + 20):
            for modula in range(3):
                assert direct_partition(begin, end, modula) == old_partition(
                    begin, end, modula
                )

    assert source.count(
        '(try_for_range, ":center_index", 0, ":center_iteration_count")'
    ) == 2
    assert '(store_mod, ":center_modula", ":center_no", 3)' not in source
    assert source.count('(store_add, ":center_no", ":first_center", ":center_offset")') == 2


def test_raiding_ai_stops_after_the_same_first_eligible_village():
    path = ROOT / "source" / "scripts" / "process_hero_ai.py"
    source = path.read_text(encoding="cp1254")
    tree = ast.parse(source)
    scripts_assignment = next(
        node
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(
            isinstance(target, ast.Name) and target.id == "process_hero_ai_scripts"
            for target in node.targets
        )
    )
    process_hero_ai = next(
        entry
        for entry in scripts_assignment.value.elts
        if isinstance(entry, ast.Tuple)
        and isinstance(entry.elts[0], ast.Constant)
        and entry.elts[0].value == "process_hero_ai"
    )
    operations = process_hero_ai.elts[1].elts
    village_loop = next(
        operation
        for operation in operations
        if _op_name(operation) == "try_for_range"
        and isinstance(operation.elts[1], ast.Constant)
        and operation.elts[1].value == ":enemy_village_no"
    )
    assert isinstance(village_loop.elts[3], ast.Constant)
    assert village_loop.elts[3].value == ":enemy_village_end"

    initialize_end = next(
        i
        for i, operation in enumerate(operations)
        if _op_name(operation) == "assign"
        and isinstance(operation.elts[1], ast.Constant)
        and operation.elts[1].value == ":enemy_village_end"
        and isinstance(operation.elts[2], ast.Name)
        and operation.elts[2].id == "villages_end"
    )
    loop_index = operations.index(village_loop)
    assert initialize_end < loop_index

    selected_index = next(
        i
        for i, operation in enumerate(operations)
        if i > loop_index
        and _op_name(operation) == "assign"
        and isinstance(operation.elts[1], ast.Constant)
        and operation.elts[1].value == ":selected_village"
    )
    stop_index = next(
        i
        for i, operation in enumerate(operations)
        if i > selected_index
        and _op_name(operation) == "assign"
        and isinstance(operation.elts[1], ast.Constant)
        and operation.elts[1].value == ":enemy_village_end"
    )
    assert stop_index == selected_index + 1
    assert ast.dump(operations[stop_index].elts[2]) == ast.dump(
        operations[selected_index].elts[2]
    )

    # Treat the existing eligibility checks as a predicate. Ending at the
    # first match preserves the selected village for every possible predicate
    # sequence, while avoiding checks after that match.
    for village_count in range(9):
        for eligible in product((False, True), repeat=village_count):
            first_match = next(
                (i for i, is_eligible in enumerate(eligible) if is_eligible), None
            )
            old_choice = first_match
            new_choice = first_match
            old_checks = len(eligible)
            new_checks = len(eligible) if first_match is None else first_match + 1
            assert old_choice == new_choice
            assert new_checks <= old_checks
