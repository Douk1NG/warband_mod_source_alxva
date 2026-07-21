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

remove_cattles_if_herd_is_close_to_party_scripts = [
("remove_cattles_if_herd_is_close_to_party",
    [
      (store_script_param, ":party_no", 1),
      (store_script_param, ":max_req", 2),
      (assign, ":cur_req", ":max_req"),
      (try_for_parties, ":cur_party"),
        (gt, ":cur_req", 0),
        (party_slot_eq, ":cur_party", slot_party_type, spt_cattle_herd),
        (store_distance_to_party_from_party, ":dist", ":cur_party", ":party_no"),
        (lt, ":dist", 3),

        #Do not use the quest herd for "move cattle herd"
        (assign, ":subcontinue", 1),
        (try_begin),
          (check_quest_active, "qst_move_cattle_herd"),
          (quest_slot_eq, "qst_move_cattle_herd", slot_quest_target_party, ":cur_party"),
          (assign, ":subcontinue", 0),
        (try_end),
        (eq, ":subcontinue", 1),
        #Do not use the quest herd for "move cattle herd" ends

        (party_count_companions_of_type, ":num_cattle", ":cur_party", "trp_cattle"),
        (try_begin),
          (le, ":num_cattle", ":cur_req"),
          (assign, ":num_added", ":num_cattle"),
          (remove_party, ":cur_party"),
        (else_try),
          (assign, ":num_added", ":cur_req"),
          (party_remove_members, ":cur_party", "trp_cattle", ":cur_req"),
        (try_end),
        (val_sub, ":cur_req", ":num_added"),


        (try_begin),
          (party_slot_eq, ":party_no", slot_party_type, spt_village),
          (party_get_slot, ":village_cattle_amount", ":party_no", slot_village_number_of_cattle),
          (val_add, ":village_cattle_amount", ":num_added"),
          (party_set_slot, ":party_no", slot_village_number_of_cattle, ":village_cattle_amount"),
        (try_end),

        (assign, reg3, ":num_added"),
        (str_store_party_name_link, s1, ":party_no"),
        (display_message, "@You brought {reg3} heads of cattle to {s1}."),
		(try_begin),
			(gt, "$cheat_mode", 0),
			(assign, reg4, ":village_cattle_amount"),
			(display_message, "@{!}Village now has {reg4}"),
		(try_end),
      (try_end),
      (store_sub, reg0, ":max_req", ":cur_req"),
     ])
]
