# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_presentations import *
from header_items import *
from header_skills import *
from header_troops import *
from ID_items import *
from ID_meshes import *
from module_constants import *

from custom_troops_constants import *
from kingdom_custom_troop_tree_creator_constants import *

# KCT existing-troops update (toggle "Update existing garrisons & party on
# save"). The original custom_troops mod ran a full automatic reset every time
# the customisation screen was opened; that was removed (quick_changes.md) and
# the two reset scripts (cstm_reset_lord_armies_in_player_faction /
# cstm_reset_garrisons_in_player_faction) are now dead code. This restores a
# scoped version, gated by the persistent toggle $cstm_update_existing_troops
# (default 0 = off) on the creator screen, and covers only what the user asked:
# player-owned garrisons + the player's own party (lord armies / village
# recruits are deliberately NOT touched).
#
# Garrisons - count + balanced auto-upgrade (no party_clear, nothing is
# wiped): every non-hero member stack of each player-owned walled centre is
# counted and removed, the same number of the tree's tier-1 recruit is added,
# and then the balanced auto-upgrade cascade runs: num_tiers-1 waves, each
# splitting every tree troop half/half along its two upgrade paths (all down
# the single path when there is only one) - exactly the "Balanced" logic of
# the player-party auto-upgrade feature, but structural (no gold, no XP).
# After the cascade every unit sits at a leaf of the tree. Prisoners, lords
# and heroes in the garrison are untouched.

EXISTING_TROOPS_SCRIPTS = [
	# script_kct_reset_garrisons_focused - the garrison update (toggle ON):
	# for every player-owned walled centre, count and remove ALL non-hero
	# member stacks, re-fill the same number with the tree's tier-1 recruit,
	# then run the balanced auto-upgrade cascade (num_tiers-1 waves of
	# half/half splits along each upgrade path) so the garrison spreads
	# across the whole tree. Prisoners, lords and heroes in the centre are
	# untouched (no party_clear); native troops are converted too.
	("kct_reset_garrisons_focused",
	[
		(assign, ":grand_total", 0),
		(assign, ":centres", 0),
		(try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
			(store_faction_of_party, ":faction", ":center_no"),
			(eq, ":faction", "fac_player_supporters_faction"),

			# 1. Count and remove every non-hero member stack (backwards so
			# removing stacks cannot shift the iteration). Prisoners live in
			# separate stacks and are never touched.
			(assign, ":total", 0),
			(party_get_num_companion_stacks, ":num_stacks", ":center_no"),
			(try_for_range_backwards, ":stack", 0, ":num_stacks"),
				(party_stack_get_troop_id, ":st_troop", ":center_no", ":stack"),
				(neg|troop_is_hero, ":st_troop"),
				(party_stack_get_size, ":st_size", ":center_no", ":stack"),
				(party_remove_members, ":center_no", ":st_troop", ":st_size"),
				(val_add, ":total", ":st_size"),
			(try_end,),

			(try_begin,),
				(gt, ":total", 0),
				# 2. Refill with the tree's tier-1 recruit.
				(party_add_members, ":center_no", "$cstm_troops_begin", ":total"),
				# 3. Balanced auto-upgrade cascade.
				(store_sub, ":waves", "$cstm_num_tiers", 1),
				(try_for_range, ":wave", 0, ":waves"),
					(try_for_range, ":troop", "$cstm_troops_begin", "$cstm_troops_end"),
						(store_troop_count_companions, ":sz", ":troop", ":center_no"),
						(gt, ":sz", 0),
						(troop_get_upgrade_troop, ":up0", ":troop", 0),
						(gt, ":up0", 0),
						(troop_get_upgrade_troop, ":up1", ":troop", 1),
						(store_div, ":cnt0", ":sz", 2),
						(store_sub, ":cnt1", ":sz", ":cnt0"),
						(try_begin,),
							(eq, ":up1", 0),
							(assign, ":cnt0", ":sz"),
							(assign, ":cnt1", 0),
						(try_end,),
						(party_remove_members, ":center_no", ":troop", ":sz"),
						(try_begin,),
							(gt, ":cnt0", 0),
							(party_add_members, ":center_no", ":up0", ":cnt0"),
						(try_end,),
						(try_begin,),
							(gt, ":cnt1", 0),
							(party_add_members, ":center_no", ":up1", ":cnt1"),
						(try_end,),
					(try_end,),
				(try_end,),
				(val_add, ":grand_total", ":total"),
				(val_add, ":centres", 1),
			(try_end,),
		(try_end,),

		# 4. Confirmation message.
		(try_begin,),
			(gt, ":centres", 0),
			(assign, reg6, ":grand_total"),
			(assign, reg7, ":centres"),
			(display_message, "@Kingdom garrison update: {reg6} troops converted in {reg7} garrisons."),
		(try_end,),
	]),

	# script_kct_update_player_party - converts the player's whole party to
	# the selected tree (same as the garrisons, on p_main_party): count and
	# remove every non-hero member stack, re-fill the same number with the
	# tree's tier-1 recruit, then run the balanced auto-upgrade cascade
	# (num_tiers-1 waves of half/half splits along each upgrade path).
	# Companions (heroes) and prisoners are untouched; native troops (e.g.
	# Swadian) and other trees' troops are converted too. Uses the proven
	# stack-iteration pattern on p_main_party (same as the auto-upgrade
	# feature); each wave snapshots the stack count and iterates backwards,
	# so stacks added by a split are only processed in the next wave.
	("kct_update_player_party",
	[
		(assign, ":total", 0),
		(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
		(try_for_range_backwards, ":stack", 0, ":num_stacks"),
			(party_stack_get_troop_id, ":st_troop", "p_main_party", ":stack"),
			(neg|troop_is_hero, ":st_troop"),
			(party_stack_get_size, ":st_size", "p_main_party", ":stack"),
			(party_remove_members, "p_main_party", ":st_troop", ":st_size"),
			(val_add, ":total", ":st_size"),
		(try_end,),

		(try_begin,),
			(gt, ":total", 0),
			(party_add_members, "p_main_party", "$cstm_troops_begin", ":total"),
			(store_sub, ":waves", "$cstm_num_tiers", 1),
			(try_for_range, ":wave", 0, ":waves"),
				(party_get_num_companion_stacks, ":num_stacks", "p_main_party"),
				(try_for_range_backwards, ":stack", 0, ":num_stacks"),
					(party_stack_get_troop_id, ":st_troop", "p_main_party", ":stack"),
					(is_between, ":st_troop", "$cstm_troops_begin", "$cstm_troops_end"),
					(party_stack_get_size, ":sz", "p_main_party", ":stack"),
					(gt, ":sz", 0),
					(troop_get_upgrade_troop, ":up0", ":st_troop", 0),
					(gt, ":up0", 0),
					(troop_get_upgrade_troop, ":up1", ":st_troop", 1),
					(store_div, ":cnt0", ":sz", 2),
					(store_sub, ":cnt1", ":sz", ":cnt0"),
					(try_begin,),
						(eq, ":up1", 0),
						(assign, ":cnt0", ":sz"),
						(assign, ":cnt1", 0),
					(try_end,),
					(party_remove_members, "p_main_party", ":st_troop", ":sz"),
					(try_begin,),
						(gt, ":cnt0", 0),
						(party_add_members, "p_main_party", ":up0", ":cnt0"),
					(try_end,),
					(try_begin,),
						(gt, ":cnt1", 0),
						(party_add_members, "p_main_party", ":up1", ":cnt1"),
					(try_end,),
				(try_end,),
			(try_end,),
			(assign, reg6, ":total"),
			(display_message, "@Player party rebalanced: {reg6} troops."),
		(try_end,),
	]),
]
