# -*- coding: cp1254 -*-
# Thin aggregator: the tree-creator presentations were split out of this file
# into the presentations/ package (layout, branch_selector, branch_display,
# troop_editor). Each submodule builds its presentation tuple at import time;
# this file re-exports the three and keeps the original modmerge.

from kingdom_custom_troop_tree_creator.kct_presentations.branch_selector import new_presentation
from kingdom_custom_troop_tree_creator.kct_presentations.branch_display import new_create_presentation
from kingdom_custom_troop_tree_creator.kct_presentations.troop_editor import new_customise_presentation


def modmerge(var_set):
	try:
		orig_presentations = var_set["presentations"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"presentations\".")

	orig_presentations.append(new_presentation)
	orig_presentations.append(new_create_presentation)
	orig_presentations.append(new_customise_presentation)
