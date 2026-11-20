# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_troops import *
from module_constants import *


# Native has no savegame-loaded callback. Reuse the existing compatibility
# trigger slot and make its interval-zero check O(1): the full restore script
# marks this non-hero sentinel only after it finishes, so later frames exit
# before doing any troop scans or copies.
native_template_health_ops = [
	(troop_get_class, ":native_restore_marker_class", "trp_cstm_load_check"),
	(neq, ":native_restore_marker_class", grc_archers),
	(call_script, "script_kct_restore_troops_after_load", "p_main_party", 1),
]


def modmerge(var_set):
	# Keep the compatibility trigger count unchanged; the body is installed in
	# source/simple_triggers/dummy_empty_triggers.py.
	return
