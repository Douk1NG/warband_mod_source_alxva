# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

# g_auto_upgrade_mode:
# 0 = Off, 1 = Balanced, 2 = Infantry, 3 = Archers, 4 = Cavalry

auto_upgrade_troops_scripts = [
("auto_upgrade_troops",
    [
      (try_begin),
        (neq, "$g_auto_upgrade_mode", 0),
        (store_troop_gold, ":player_gold", "trp_player"),
        (gt, ":player_gold", 0),

        (assign, ":total_upgraded", 0),
        (assign, ":gold_spent", 0),
        (party_get_num_companion_stacks, ":num_stacks", "p_main_party"),

        (try_for_range_backwards, ":i_stack", 0, ":num_stacks"),
          (party_stack_get_troop_id, ":troop_id", "p_main_party", ":i_stack"),
          (neg|troop_is_hero, ":troop_id"),

          (troop_get_upgrade_troop, ":upg0", ":troop_id", 0),
          (gt, ":upg0", 0),

          (party_stack_get_num_upgradeable, ":num_ready", "p_main_party", ":i_stack"),
          (gt, ":num_ready", 0),

          (party_stack_get_size, ":sz", "p_main_party", ":i_stack"),
          (party_stack_get_num_wounded, ":wn", "p_main_party", ":i_stack"),
          (store_sub, ":avail", ":sz", ":wn"),
          (gt, ":num_ready", 0),

          (troop_get_upgrade_troop, ":upg1", ":troop_id", 1),
          (assign, ":has_two", 0),
          (try_begin),
            (gt, ":upg1", 0),
            (assign, ":has_two", 1),
          (try_end),

          # Determine counts per path
          (assign, ":cnt0", 0),
          (assign, ":cnt1", 0),
          (try_begin),
            (eq, "$g_auto_upgrade_mode", 1),
            (try_begin),
              (eq, ":has_two", 1),
              (store_div, ":cnt0", ":num_ready", 2),
              (store_sub, ":cnt1", ":num_ready", ":cnt0"),
            (else_try),
              (assign, ":cnt0", ":num_ready"),
            (try_end),
          (else_try),
            (try_begin),
              (eq, "$g_auto_upgrade_mode", 2),
              (assign, ":target_class", grc_infantry),
            (else_try),
              (eq, "$g_auto_upgrade_mode", 3),
              (assign, ":target_class", grc_archers),
            (else_try),
              (assign, ":target_class", grc_cavalry),
            (try_end),
            (assign, ":matched", 0),
            (try_begin),
              (call_script, "script_cf_troop_is_class", ":target_class", ":upg0"),
              (assign, ":cnt0", ":num_ready"),
              (assign, ":matched", 1),
            (try_end),
            (try_begin),
              (eq, ":matched", 0),
              (eq, ":has_two", 1),
              (call_script, "script_cf_troop_is_class", ":target_class", ":upg1"),
              (assign, ":cnt1", ":num_ready"),
              (assign, ":matched", 1),
            (try_end),
            (try_begin),
              (eq, ":matched", 0),
              (assign, ":cnt0", ":num_ready"),
            (try_end),
          (try_end),

          # Total to upgrade this stack
          (store_add, ":to_upgrade", ":cnt0", ":cnt1"),
          (gt, ":to_upgrade", 0),

          # Gold check
          (call_script, "script_game_get_upgrade_cost", ":troop_id"),
          (assign, ":cpt", reg0),
          (store_mul, ":cost", ":to_upgrade", ":cpt"),
          (store_add, ":total_after", ":gold_spent", ":cost"),
          (try_begin),
            (le, ":total_after", ":player_gold"),

            # Compute how many wounded will be removed (party_remove_members removes healthy first)
            (try_begin),
              (le, ":to_upgrade", ":avail"),
              (assign, ":wounded_removed", 0),
            (else_try),
              (store_sub, ":wounded_removed", ":to_upgrade", ":avail"),
              (val_min, ":wounded_removed", ":wn"),
            (try_end),

            (store_sub, ":wounded_kept", ":wn", ":wounded_removed"),
            (store_sub, ":keep", ":sz", ":to_upgrade"),

            # Remove ALL troops from this stack (clears the XP pool)
            (party_remove_members, "p_main_party", ":troop_id", ":sz"),

            # Add back the non-upgraded ones (fresh, 0 XP, no flag)
            (try_begin),
              (gt, ":keep", 0),
              (party_add_members, "p_main_party", ":troop_id", ":keep"),
            (try_end),

            # Re-wound the ones that WEREN'T upgraded
            (try_begin),
              (gt, ":wounded_kept", 0),
              (party_wound_members, "p_main_party", ":troop_id", ":wounded_kept"),
            (try_end),

            # Add upgraded path 0
            (try_begin),
              (gt, ":cnt0", 0),
              (party_add_members, "p_main_party", ":upg0", ":cnt0"),
            (try_end),

            # Add upgraded path 1
            (try_begin),
              (gt, ":cnt1", 0),
              (party_add_members, "p_main_party", ":upg1", ":cnt1"),
            (try_end),

            # Re-wound the upgraded troops that came from wounded
            (try_begin),
              (gt, ":wounded_removed", 0),
              (assign, ":wnd_rem", ":wounded_removed"),
              (try_begin),
                (gt, ":cnt0", 0),
                (val_min, ":wnd_rem", ":cnt0"),
                (party_wound_members, "p_main_party", ":upg0", ":wnd_rem"),
                (val_sub, ":wounded_removed", ":wnd_rem"),
              (try_end),
              (try_begin),
                (gt, ":cnt1", 0),
                (gt, ":wounded_removed", 0),
                (val_min, ":wounded_removed", ":cnt1"),
                (party_wound_members, "p_main_party", ":upg1", ":wounded_removed"),
              (try_end),
            (try_end),

            (val_add, ":gold_spent", ":cost"),
            (val_add, ":total_upgraded", ":to_upgrade"),
          (try_end),
        (try_end),

        (try_begin),
          (gt, ":total_upgraded", 0),
          (troop_remove_gold, "trp_player", ":gold_spent"),
          (assign, reg6, ":total_upgraded"),
          (assign, reg7, ":gold_spent"),
          (display_message, "@Auto-upgrade complete: {reg6} troops upgraded for {reg7} denars."),
        (try_end),
      (try_end),
  ])
]
