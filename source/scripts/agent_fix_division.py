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

agent_fix_division_scripts = [
("agent_fix_division", [
      (store_script_param_1, ":agent"),
      (agent_set_slot, ":agent", slot_agent_new_division, -1),
      (get_player_agent_no, ":player"),	#after_mission_start triggers are called after spawn, so globals can't be used
      #yet

      (try_begin),
        (ge, ":player", 0),
        (neq, ":agent", ":player"),
        (agent_is_human, ":agent"),
        (agent_get_group, ":player_team", ":player"),
        (agent_get_group, ":team", ":agent"),
        (this_or_next | main_hero_fallen),
        (neq, ":team", ":player_team"),

        (assign, ":target_division", grc_infantry),
        (agent_get_horse, ":horse", ":agent"),
        (agent_get_troop_id, ":troop_no", ":agent"),

        #logic from script_troop_default_division
        #limited to the three divisions the AI currently uses
        (try_begin),
          (this_or_next | ge, ":horse", 0),
          (troop_is_guarantee_horse, ":troop_no"),
          (assign, ":target_division", grc_cavalry),

          #(troop_is_guarantee_ranged, ":troop_no"),
          # (try_for_range, ":ranged", "itm_darts", "itm_flintlock_pistol"),
              # (agent_has_item_equipped, ":agent", ":ranged"),
              # (agent_get_ammo, reg1, ":agent", 0),
              # (gt, reg1, 0),
              # (assign, ":target_division", sdt_harcher),
          # (try_end),


          # (try_begin),
          # (eq, ":flag_0_for_expanded", 0),
          # (try_for_range, reg0, 0, ":inv_cap"),
          # (troop_get_inventory_slot, ":item", ":troop_no", reg0),
          # (call_script, "script_cf_is_weapon_ranged", ":item", 1),
          # (assign, ":target_division", sdt_harcher),
          # (try_end),
          # (try_end),

        (else_try),
          (troop_is_guarantee_ranged, ":troop_no"),
          # (assign, ":has_ranged", 0),

          (try_for_range, ":item_slot", ek_item_0, ek_head),
            (agent_get_item_slot, ":item", ":agent", ":item_slot"),
            (call_script, "script_cf_is_weapon_ranged", ":item", 1),
            (agent_get_ammo, reg1, ":agent", 0),
            (ge, reg1, minimum_ranged_ammo),  #more than two to throw on a charge?
            # (item_get_type, reg1, ":item"),
            # (try_begin),
            # (eq, reg1, itp_type_thrown),
            # (eq, ":flag_0_for_expanded", 0),
            # (neq, ":target_division", grc_archers),
            # (assign, ":target_division", sdt_skirmisher),
            # (else_try),
            (assign, ":target_division", grc_archers),
            # (try_end),
            # (assign, ":has_ranged", 1),
          (try_end),

          # (neq, ":has_ranged", 0),

          # (else_try),
          # (eq, ":flag_0_for_expanded", 0),
          # (try_for_range, reg0, 0, ":inv_cap"),
          # (troop_get_inventory_slot, ":item", ":troop_no", reg0),
          # (call_script, "script_cf_is_thrusting_weapon", ":item"),
          # (item_get_type, reg1, ":item"),
          # (eq, reg1, itp_type_polearm),
          # (assign, ":target_division", sdt_polearm),
          # (try_end),
        (try_end),

        (agent_get_division, ":division", ":agent"),
        (neq, ":division", ":target_division"),
        (agent_set_division, ":agent", ":target_division"),
        (agent_set_slot, ":agent", slot_agent_new_division, ":target_division"),
      (try_end),])
]
