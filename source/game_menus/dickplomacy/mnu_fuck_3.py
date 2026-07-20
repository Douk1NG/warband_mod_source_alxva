# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

fuck_3_menu = [
("fuck_3",0,
   "Who will be {s4}?^{s1}^{reg1}:",
   "none",
    [
      (assign, reg1, "$temp_2"),
      (troop_get_slot, "$temp_3", "trp_stack_selection_amounts", 0), #number of slots

	  (str_clear, s4),
	  (try_begin),
		  (eq, "$temp_2", 1),
		  (str_store_string, s4, "@getting fucked"),
	  (else_try),
		  (eq, "$temp_2", 4),
		  (str_store_string, s4, "@fucking the mouth"),
	  (else_try),
		  (eq, "$temp_2", 3),
		  (str_store_string, s4, "@watching"),
	  (else_try),
		  (str_store_string, s4, "@fucking"),
	  (try_end),

      #SB : show current list
      (str_clear, s1),
      (store_sub, ":end", "$temp_2", 1),
      (try_for_range, ":slot_index", 0, ":end"),
        (store_add, reg0, ":slot_index", 1),
        (troop_get_slot, ":troop_id", "trp_temp_array_a", ":slot_index"),
		(try_begin),
			(ge, ":troop_id", 0),
			(str_store_troop_name, s2, ":troop_id"),
			(str_store_string, s1, "@{s1}^{reg0}: {s2}"),
        (else_try),
			(str_store_string, s1, "@{s1}^{reg0}: No one"),
		(try_end),
      (try_end),
    ],
    [
      ("training_ground_selection_details_melee_random", [], "Choose randomly.",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details_fuck", -1),]),
      ("go_back_dot",[],"Go back.",
       [(jump_to_menu, "mnu_camp"),]
       ), #SB : stack built from loop
	  ("nobody", [], "No one.",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details_fuck", -2),]
	  ),
      ]+
      [("stack"+str(x), [(call_script, "script_cf_training_ground_sub_routine_1_for_melee_details", x),], "{s0}",
       [(call_script, "script_training_ground_sub_routine_2_for_melee_details_fuck", x),])
       for x in range(0, 20)]
  )
]
