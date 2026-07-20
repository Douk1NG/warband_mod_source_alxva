# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
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

store_battlegroup_type_scripts = [
("store_battlegroup_type", [
      (store_script_param_1, ":fteam"),
      (store_script_param_2, ":fdivision"),

      (assign, ":count_infantry", 0),
      (assign, ":count_archer", 0),
      (assign, ":count_cavalry", 0),
      (assign, ":count_harcher", 0),
      (assign, ":count_polearms", 0),
      (assign, ":count_skirmish", 0),
      (assign, ":count_support", 0),
      (assign, ":count_bodyguard", 0),

      (team_get_leader, ":leader", ":fteam"),

      (try_for_agents, ":cur_agent"),
        (call_script, "script_cf_valid_formation_member", ":fteam", ":fdivision", ":leader", ":cur_agent"),
        (agent_get_troop_id, ":cur_troop", ":cur_agent"),
        (agent_get_ammo, ":cur_ammo", ":cur_agent", 0),

        (try_begin),
          (neg | troop_is_hero, ":cur_troop"),
          (try_begin), #Cavalry
            (agent_get_horse, reg0, ":cur_agent"),
            (ge, reg0, 0),
            (try_begin),
              (ge, ":cur_ammo", minimum_ranged_ammo),
              (val_add, ":count_harcher", 1),
            (else_try),
              (val_add, ":count_cavalry", 1),
            (try_end),
          (else_try), #Archers
            (ge, ":cur_ammo", minimum_ranged_ammo),
            # #use when troops are equipped with ranged at start of battle
            # (agent_get_class, ":bgclass", ":cur_agent"),
            # (eq, ":bgclass", grc_archers),
            # #end use when troops equipped with ranged at start of battle
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (gt, ":item", 0),
              (item_get_type, ":weapontype", ":item"),
              (is_between, ":weapontype", itp_type_bow, itp_type_thrown),  # bow or crossbow
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find bow or crossbow
              (val_add, ":count_skirmish", 1),
            (else_try),
              (val_add, ":count_archer", 1),
            (try_end),
          (else_try), #Infantry
            (assign, ":end", ek_head),
            (try_for_range, ":i", ek_item_0, ":end"),
              (agent_get_item_slot, ":item", ":cur_agent", ":i"),
              (call_script, "script_cf_is_thrusting_weapon", ":item"),
              (item_get_type, ":weapontype", ":item"),
              (eq, ":weapontype", itp_type_polearm),
              (assign, ":end", ek_item_0), #loop Break
            (try_end),
            (try_begin),
              (eq, ":end", ek_head), #failed to find a polearm
              (val_add, ":count_infantry", 1),
            (else_try),
              (val_add, ":count_polearms", 1),
            (try_end),
          (try_end),
        (else_try), #Heroes
          (assign, ":support_skills", 0), #OPEN TO SUGGESTIONS HERE ?skl_trade, skl_spotting, skl_pathfinding,
          #skl_tracking?
          (store_skill_level, reg0, skl_engineer, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_first_aid, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_surgery, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (store_skill_level, reg0, skl_wound_treatment, ":cur_troop"),
          (val_add, ":support_skills", reg0),
          (try_begin),
            (gt, ":support_skills", 5),
            (val_add, ":count_support", 1),
          (else_try),
            (val_add, ":count_bodyguard", 1),
          (try_end),
        (try_end), #Regular v Hero
      (try_end), #Agent Loop

      #Do Comparisons With Counts, set ":div_type"
      (assign, ":slot", slot_team_d0_type),
      (team_set_slot, scratch_team, ":slot", ":count_infantry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_archer"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_cavalry"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_polearms"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_skirmish"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_harcher"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_support"),
      (val_add, ":slot", 1),
      (team_set_slot, scratch_team, ":slot", ":count_bodyguard"),

      (assign, ":count_to_beat", 0),
      (assign, ":count_total", 0),
      (try_for_range, ":type", sdt_infantry, sdt_infantry + 8), #only 8 sdt_types at the moment
        (store_add, ":slot", slot_team_d0_type, ":type"),
        (team_get_slot, ":count", scratch_team, ":slot"),
        (val_add, ":count_total", ":count"),
        (lt, ":count_to_beat", ":count"),
        (assign, ":count_to_beat", ":count"),
        (assign, ":div_type", ":type"),
      (try_end),

      (val_mul, ":count_to_beat", 2),
      (try_begin),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":count_to_beat", 0),
        (assign, ":div_type", -1),
        (try_for_range, ":type", sdt_infantry, sdt_infantry + 3), #check main types for a majority
          (store_add, ":slot", slot_team_d0_type, ":type"),
          (team_get_slot, ":count", scratch_team, ":slot"),
          (val_add, ":slot", 3),	#subtype is three more than main type
          (team_get_slot, reg0, scratch_team, ":slot"),
          (val_add, ":count", reg0),
          (lt, ":count_to_beat", ":count"),
          (assign, ":count_to_beat", ":count"),
          (assign, ":div_type", ":type"),
        (try_end),

        (val_mul, ":count_to_beat", 2),
        (lt, ":count_to_beat", ":count_total"), #Less than half of this division
        (assign, ":div_type", sdt_unknown), #Or 0
      (try_end),

      #hard-code traditional infantry division (avoid player confusion for mods
      #which arm troops with ranged at start of battle)
      (try_begin),
        (eq, ":fdivision", grc_infantry),
        (neq, ":div_type", sdt_polearm),
        (assign, ":div_type", sdt_infantry),
      (try_end),

      (store_add, ":slot", slot_team_d0_type, ":fdivision"),
      (team_set_slot, ":fteam", ":slot", ":div_type"),
      (assign, reg0, ":div_type"),])
]
