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

change_player_relation_with_faction_ex_scripts = [
# script_change_player_relation_with_faction_ex
# changes relations with other factions also (according to their relations between each other)
# Input: arg1 = faction_no, arg2 = relation difference
# Output: none
("change_player_relation_with_faction_ex",
    [
      (store_script_param_1, ":faction_no"),
      (store_script_param_2, ":difference"),

      (store_relation, ":player_relation", ":faction_no", "fac_player_supporters_faction"),
      (assign, reg1, ":player_relation"),
      (val_add, ":player_relation", ":difference"),
      (assign, reg2, ":player_relation"),
      (set_relation, ":faction_no", "fac_player_faction", ":player_relation"),
      (set_relation, ":faction_no", "fac_player_supporters_faction", ":player_relation"),

      (str_store_faction_name_link, s1, ":faction_no"),
      #SB : positive/negative messages
      (try_begin),
        (gt, ":difference", 0),
        (display_message, "str_faction_relation_increased", message_positive),
      (else_try),
        (lt, ":difference", 0),
        (display_message, "str_faction_relation_detoriated", message_negative),
      (try_end),
      #SB : morale adjustments
      (store_mul, ":morale_change", ":difference", 50), #instead of x100
      (call_script, "script_change_faction_troop_morale", ":faction_no", ":morale_change", 0),

      (try_for_range, ":other_faction", kingdoms_begin, kingdoms_end),
        (faction_slot_eq, ":other_faction", slot_faction_state, sfs_active),
        (neq, ":faction_no", ":other_faction"),
        (store_relation, ":other_faction_relation", ":faction_no", ":other_faction"),
        (store_relation, ":player_relation", ":other_faction", "fac_player_supporters_faction"),
        (store_mul, ":relation_change", ":difference", ":other_faction_relation"),
        (val_div, ":relation_change", 100),
        (val_add, ":player_relation", ":relation_change"),
        ##diplomacy start
        (try_begin),
            (store_add, ":truce_slot", "fac_player_supporters_faction", slot_faction_truce_days_with_factions_begin),
  		    (val_sub, ":truce_slot", kingdoms_begin),
  		    (faction_get_slot, ":truce_days", ":other_faction", ":truce_slot"),
			##nested diplomacy start+ Changed "eq 0", to "le 0", since now negative truce days track war length
            (this_or_next|le, ":truce_days", 0), #other faction only affected if no truce
			##nested diplomacy end+
            (gt, ":difference", 0), #or change > 0
            (store_relation, ":cur_relation", ":other_faction", "fac_player_supporters_faction"),

            #display relation change message
            (store_sub,  ":relation_change", ":player_relation", ":cur_relation"),
            (str_store_faction_name_link, s1, ":other_faction"),
            (assign, reg1, ":cur_relation"),
            (assign, reg2, ":player_relation"),
            (try_begin),
              (gt, ":relation_change", 0),
              (display_message, "str_faction_relation_increased", message_positive),
            (else_try),
              (lt, ":relation_change", 0),
              (display_message, "str_faction_relation_detoriated", message_negative),
            (try_end),

            #display war declaration
            (try_begin),
                (ge, ":cur_relation", 0), #old relation > 0 -> peace
                (lt, ":player_relation", 0), #new relation < 0 -> war
                ##nested diplomacy start+
                #This is the source of the "fake war" bug.  I think this should get rid of it:
                (try_begin),
                    (this_or_next|eq, "$players_kingdom", "fac_player_faction"),
                       (eq, "$players_kingdom", "fac_player_supporters_faction"),
                ##nested diplomacy end+
                (call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":other_faction", "$players_kingdom"),
                ##nested diplomacy start+
				(else_try),
					(is_between, "$players_kingdom", kingdoms_begin, kingdoms_end),
					(store_relation, ":players_kingdom_relation", ":other_faction", "$players_kingdom"),
					(lt, ":players_kingdom_relation", 0),
					(call_script, "script_add_notification_menu", "mnu_notification_war_declared", ":other_faction", "$players_kingdom"),
				(else_try),
					#Display some sort of message so you know something happened
				    (display_message, "@{!} There is widespread ill-will towards you in the {s1}."),
                (try_end),
                ##nested diplomacy end+
            (try_end),
        ##diplomacy end
        (set_relation, ":other_faction", "fac_player_faction", ":player_relation"),
        (set_relation, ":other_faction", "fac_player_supporters_faction", ":player_relation"),
        ##diplomacy begin
        (try_end),
        ##diplomacy end
      (try_end),
      (try_begin),
        (faction_slot_eq, "fac_player_supporters_faction", slot_faction_state, sfs_active),
        (try_for_range, ":kingdom_no", kingdoms_begin, kingdoms_end),
          (faction_slot_eq, ":kingdom_no", slot_faction_state, sfs_active),
          (call_script, "script_update_faction_notes", ":kingdom_no"),
        (try_end),
      (try_end),
  ])
]
