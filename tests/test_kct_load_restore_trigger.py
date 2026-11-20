"""Regression checks for WSE and Native KCT load restoration paths."""
import os
import re
import unittest


ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRIGGER = os.path.join(
    ROOT, "modmerger", "mods", "kingdom_custom_troop_tree_creator",
    "kingdom_custom_troop_tree_creator_simple_triggers.py",
)
RESTORE = os.path.join(
    ROOT, "modmerger", "mods", "kingdom_custom_troop_tree_creator",
    "kct_scripts", "load_restore.py",
)
SCRIPTS = os.path.join(
    ROOT, "modmerger", "mods", "kingdom_custom_troop_tree_creator",
    "kingdom_custom_troop_tree_creator_scripts.py",
)
MAP_ICONS = os.path.join(ROOT, "source", "module_map_icons.py")
WSE_CALLBACK = os.path.join(ROOT, "source", "scripts", "wse_game_saved.py")
TREE_IO = os.path.join(
    ROOT,
    "modmerger", "mods", "kingdom_custom_troop_tree_creator",
    "kct_scripts", "tree_io.py",
)
NATIVE_TRIGGER_SLOT = os.path.join(
    ROOT, "source", "simple_triggers", "dummy_empty_triggers.py",
)


def read_source(path):
    with open(path, "r", encoding="cp1254") as source_file:
        return source_file.read()


class KctLoadRestoreTests(unittest.TestCase):
    def test_native_uses_original_compatibility_slot_with_content_validation(self):
        code = "\n".join(
            line.split("#", 1)[0] for line in read_source(TRIGGER).splitlines()
        )
        native_slot = read_source(NATIVE_TRIGGER_SLOT)
        self.assertIn("from kingdom_custom_troop_tree_creator_simple_triggers import native_template_health_ops", native_slot)
        self.assertRegex(native_slot, r"(?m)^\(1, native_template_health_ops\),?\s*$")
        self.assertIn('"trp_cstm_load_check"', code)
        self.assertIn('(this_or_next|neq, ":native_restore_marker_class", grc_cavalry)', code)
        self.assertNotIn("new_load_operations", code)
        self.assertNotIn("orig_simple_triggers.extend(new_simple_triggers)", code)

    def test_native_restore_check_is_throttled_and_marker_does_not_block_checks(self):
        code = read_source(TRIGGER)
        interval_source = read_source(NATIVE_TRIGGER_SLOT)
        self.assertIn('(1, native_template_health_ops)', interval_source)
        first_name_scan = code.index('(str_store_troop_name, s0, real_troop)')
        handled_marker = code.index('(troop_set_class, "trp_cstm_load_check", grc_cavalry)')
        self.assertGreater(handled_marker, first_name_scan)
        self.assertIn('(this_or_next|neq, ":native_restore_marker_class", grc_cavalry)', code)

    def test_native_repairs_only_when_falcon_or_calradian_data_is_incomplete(self):
        code = read_source(TRIGGER)
        self.assertIn('_default_template_health_ops(6, 11, 2, 12, "falcon")', code)
        self.assertIn('_default_template_health_ops(7, 21, 3, 22, "calradian")', code)
        self.assertIn('kct_custom_preset_troop_id(4, 0, node_index)', code)
        self.assertIn('"@[KCT] Restoring incomplete troop data"', code)
        reset_marker = code.index('(troop_set_class, "trp_kct_template_slot_0_meta", grc_infantry)')
        restore_call = code.index('(call_script, "script_kct_restore_troops_after_load", "p_main_party", 0)')
        self.assertLess(reset_marker, restore_call)
        self.assertNotIn('(call_script, "script_kct_restore_troops_after_load", "p_main_party", 1)', code)
        self.assertIn('(gt, ":calradian_placeholder_count", 0)', code)

    def test_wse_uses_the_successful_savegame_load_callback(self):
        callback = read_source(WSE_CALLBACK)
        self.assertIn('("wse_savegame_loaded", [', callback)
        self.assertIn('"script_kct_restore_troops_after_load", "p_main_party"', callback)

    def test_restore_script_is_registered_and_runs_once_for_main_party(self):
        restore = read_source(RESTORE)
        scripts = read_source(SCRIPTS)
        self.assertIn('("kct_restore_troops_after_load", load_restore_operations)', restore)
        self.assertIn("+ LOAD_RESTORE_SCRIPTS", scripts)
        self.assertIn('(eq, ":party_no", "p_main_party")', restore)
        self.assertIn('(neq, ":restore_marker_class", grc_cavalry)', restore)
        self.assertIn('(eq, ":force_restore", 1)', restore)
        self.assertIn('(troop_set_class, "trp_cstm_load_check", grc_cavalry)', restore)
        self.assertIn('"@[KCT] Restore complete: {reg0} troops updated from saved data."', restore)
        self.assertGreater(
            restore.index('(troop_set_class, "trp_cstm_load_check", grc_cavalry)'),
            restore.index('(try_for_range, ":troop", cstm_troops_begin, cstm_troops_end)'),
        )

    def test_map_icons_do_not_depend_on_load_initialization(self):
        icons = read_source(MAP_ICONS)
        self.assertNotIn("kct_load_restore_trigger", icons)

    def test_restoration_and_migrations_have_safe_order(self):
        restore = read_source(RESTORE)
        expected = [
            '"script_kct_replace_custom_troop_with_dummy"',
            '"script_kct_restore_native_guards"',
            '"script_kct_reapply_all_genders"',
            '"script_kct_seed_missing_default_template_slots"',
            '"script_kct_restore_custom_tree_default_slots"',
            '"script_kct_restore_calradian_missing_troops"',
            '"script_kct_migrate_legacy_v1"',
        ]
        offsets = [restore.index(operation) for operation in expected]
        self.assertEqual(offsets, sorted(offsets))
        marker_write = restore.index(
            '(troop_set_class, "trp_kct_template_slot_0_meta", grc_cavalry)'
        )
        first_restore = restore.index('"script_kct_replace_custom_troop_with_dummy"')
        self.assertGreater(marker_write, first_restore)

    def test_calradian_restores_each_unconfigured_troop_without_replacing_configured_ones(self):
        restore = read_source(RESTORE)
        tree_io = read_source(TREE_IO)
        repair = tree_io[tree_io.index("def _build_restore_calradian_missing_troops_ops():"):tree_io.index("TREE_IO_SCRIPTS = [")]
        self.assertIn("kct_custom_preset_troop_id(4, 0, node_index)", repair)
        self.assertIn('(str_compare, ":real_name_is_placeholder", s0, s1, 1)', repair)
        self.assertIn('(str_compare, ":dummy_name_is_placeholder", s0, s1, 1)', repair)
        self.assertIn('(this_or_next|eq, ":real_name_is_placeholder", 0)', repair)
        self.assertIn('(call_script, "script_kct_get_template_node_troop", 7, node_index)', repair)
        self.assertIn('_copy_troop_record_ops(":template_node", ":template_node", real_troop)', repair)
        self.assertIn('(call_script, "script_kct_copy_custom_troop_to_dummy", real_troop)', repair)
        self.assertIn('"kct_restore_calradian_missing_troops", _build_restore_calradian_missing_troops_ops()', tree_io)
        self.assertIn('"@[KCT] Initialized {reg0} Calradian troops"', tree_io)
    def test_load_migration_seeds_each_empty_builtin_slot_independently(self):
        tree_io = read_source(os.path.join(
            ROOT,
            "modmerger", "mods", "kingdom_custom_troop_tree_creator",
            "kct_scripts", "tree_io.py",
        ))
        self.assertIn('"kct_seed_missing_default_template_slots", _build_seed_missing_default_slots_ops()', tree_io)
        self.assertIn('"kct_seed_default_template_slot", _build_seed_default_slot_ops()', tree_io)
        self.assertIn("DEFAULT_SLOT_TEMPLATES[:CUSTOM_TREE_DEFAULT_SLOT_BEGIN]", tree_io)
        self.assertIn("seeding missing default slot %d: %s", tree_io)
        self.assertIn('_load_wse_json_template("Falcon.json")', tree_io)
        self.assertIn('_load_wse_json_template("Calradian.json")', tree_io)
        self.assertIn('"kct_restore_custom_tree_default_slots", _build_restore_custom_tree_default_slots_ops()', tree_io)
        self.assertIn('(neg|troop_slot_eq, ":meta", kct_slot_template_occupied, 1)', tree_io)
        self.assertIn('(neg|troop_slot_eq, ":template_node", cstm_slot_troop_configured, 1)', tree_io)
        self.assertIn('"@[KCT] Repairing missing built-in tree template: %s" % name', tree_io)
        restore_builder = tree_io[tree_io.index('def _build_restore_custom_tree_default_slots_ops():'):tree_io.index('TREE_IO_SCRIPTS = [')]
        self.assertLess(restore_builder.index('(eq, ":needs_seed", 1)'), restore_builder.index('"script_kct_seed_default_template_slot", slot_index'))

    def test_native_slot_import_restores_saved_tree_gender_before_range_lookup(self):
        tree_io = read_source(TREE_IO)
        tree_import = tree_io[tree_io.index('("kct_import_tree_from_slot",'):]
        tree_restore = tree_import.index('(troop_get_slot, "$cstm_selected_tree", ":meta", kct_slot_template_tree)')
        gender_restore = tree_import.index('(troop_get_slot, "$cstm_selected_gender", ":meta", kct_slot_template_gender)')
        range_lookup = tree_import.index('(call_script, "script_kct_compute_tree_range")')
        self.assertLess(tree_restore, gender_restore)
        self.assertLess(gender_restore, range_lookup)


if __name__ == "__main__":
    unittest.main()
