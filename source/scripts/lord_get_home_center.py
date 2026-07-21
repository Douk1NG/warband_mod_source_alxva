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

lord_get_home_center_scripts = [
("lord_get_home_center",
	[
      (store_script_param, ":troop_no", 1),
      (assign, ":result", -1),

		##diplomacy start+
		(assign, ":best_score", -1),
		(troop_get_slot, ":troop_original_faction", ":troop_no", slot_troop_original_faction),
		#The default script prefers towns to castles, but aside from that is
		#fairly arbitrary.  Add scores that take into account original faction
		#and so forth.
      (try_for_range, ":center_no", walled_centers_begin, walled_centers_end),
        (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
		  (assign, ":center_score", 10),#10 for castles, 20 for towns
		  (try_begin),
		    (is_between, ":center_no", towns_begin, towns_end),
			(assign, ":center_score", 20),
		  (try_end),
		  (try_begin),
		    (troop_slot_eq, ":troop_no", slot_troop_home, ":center_no"),
			(val_add, ":center_score", 6),
          (else_try),
			(party_slot_eq, ":center_no", dplmc_slot_center_original_lord, ":troop_no"),
			(val_add, ":center_score", 5),
		  (else_try),
		    (is_between, ":troop_original_faction", kingdoms_begin, kingdoms_end),
			(party_slot_eq, ":center_no", slot_center_original_faction, ":troop_original_faction"),
			(val_add, ":center_score", 4),
		  (try_end),
		  (gt, ":center_score", ":best_score"),
          (assign, ":result", ":center_no"),
		  (assign, ":best_score", ":center_score"),
      (try_end),
		##diplomacy end+

      #SB : add loop breaks
      (try_begin),
        (eq, ":result", -1),
        (assign, ":limit", walled_centers_end),
        (try_for_range, ":center_no", walled_centers_begin, ":limit"),
          (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),
          (assign, ":result", ":center_no"),
          (assign, ":limit", walled_centers_begin),
        (try_end),
      (try_end),

      #NOTE : In old code if a lord has no walled center then home city of this lord is assigning to
      #faction leader's home city. Now I changed this to assign home cities more logical and homogeneous.
      #In new code if a lord has no walled center then his home city becomes his village's border_city.
      #This means his home city becomes owner city of his village. If he has no village then as last change
      #his home city become faction leader's home city.
      (try_begin),
        (eq, ":result", -1),

        #SB : add loop breaks
        (assign, ":limit", villages_end),
        (try_for_range, ":center_no", villages_begin, ":limit"),
          (eq, ":result", -1),
          (party_slot_eq, ":center_no", slot_town_lord, ":troop_no"),

          # (try_begin),
            # (neg|is_between, ":center_no", walled_centers_begin, walled_centers_end),
          (party_get_slot, ":bound_center", ":center_no", slot_village_bound_center),
          (assign, ":result", ":bound_center"),
          (assign, ":limit", villages_begin),
          # (try_end),
        (try_end),
      (try_end),

      #If lord has no walled center and is player faction, then assign player court
      (try_begin),
        (eq, ":result", -1),
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (eq, ":faction_no", "fac_player_supporters_faction"),
		(is_between, "$g_player_court", walled_centers_begin, walled_centers_end),
		(store_faction_of_party, ":player_court_faction", "$g_player_court"),
		(eq, ":player_court_faction", "fac_player_supporters_faction"),

        (assign, ":result", "$g_player_court"),
      (try_end),

      #If lord has no walled center and any not walled village then assign faction capital
      (try_begin),
        (eq, ":result", -1),
        (store_faction_of_troop, ":faction_no", ":troop_no"),
        (faction_get_slot, ":faction_leader", ":faction_no", slot_faction_leader),
        (neq, ":troop_no", ":faction_leader"),
        (ge, ":faction_leader", 0),#<- Fix for ticket 36.
        ##By the way, if this was Native, the following two lines would fix
        ##the weird bug where relatives of exiled lords start accumulating
        ##in the player's court:
        #(this_or_next|neq, ":faction_leader", ":troop_no"),
        #(eq, "$players_kingdom", ":faction_no"),
        ##This is unnecessary in Diplomacy, though, since I initialize slot_faction_leader to -1
        ##to distinguish factions led by the player from factions without actual leaders.
        (call_script, "script_lord_get_home_center", ":faction_leader"),
        (gt, reg0, -1),
        (assign, ":result", reg0),
      (try_end),

	  #Any center of the faction
      (try_begin),
        (eq, ":result", -1),
		(store_faction_of_troop, ":faction_no", ":troop_no"),

		(try_for_range, ":walled_center", walled_centers_begin, walled_centers_end),
		    (eq, ":result", -1),

			(store_faction_of_party, ":center_faction", ":walled_center"),
			(eq, ":faction_no", ":center_faction"),
			(assign, ":result", ":walled_center"),
		(try_end),
      (try_end),



      (assign, reg0, ":result"),
	])
]
