# -*- coding: cp1254 -*-
import string
from header_common import *
from header_presentations import *
from header_mission_templates import *
from ID_meshes import *
from header_operations import *
from header_triggers import *
#SB: import skills from ID_skills import *
from module_constants import *
##diplomacy start+ Import for use with terrain advantage
from header_terrain_types import *
from module_items import *
#SB : import colors
from module_factions import *
from header_items import *
##diplomacy end
from compiler import *

dplmc_policy_management = ("dplmc_policy_management",0,mesh_load_window,[
      (ti_on_presentation_load,
        [
        (set_fixed_point_multiplier, 1000),
        (presentation_set_duration, 999999),
        ##nested diplomacy start+ insert g_presentation_obj_5, g_presentation_obj_6 and increment others

        ##Moved up here from below
        (faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
        (faction_get_slot, ":aristocracy", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
        (faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
        (faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
        (faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_quality),#<- dplmc+ added

        # done
        (create_game_button_overlay, "$g_presentation_obj_12", "str_done"),#<- dplmc+ changed obj_10 to obj_12
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_12", pos1),#<- dplmc_ changed obj_10 to obj_12

        #SB : add randomize
        (create_game_button_overlay, "$g_presentation_obj_11", "str_randomize"),
        (position_set_x, pos1, 900),
        (position_set_y, pos1, 125),
        (overlay_set_position, "$g_presentation_obj_11", pos1),

        # title
        (create_text_overlay, reg1, "@Select your domestic policy", tf_center_justify|tf_vertical_align_center),
        (position_set_x, pos1, 445),
        (position_set_y, pos1, 700),
        (overlay_set_position, reg1, pos1),

        (create_slider_overlay, "$g_presentation_obj_sliders_1", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_2", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_3", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_4", -3, 3),
        (create_slider_overlay, "$g_presentation_obj_sliders_5", -3, 3),#<-dplmc+ added
        (assign, reg1, 25),
        ##dplmc+ start incremented sliders by 1... (and changed since things might not be at their initial values)
        (store_add, ":text", "str_dplmc_neither_centralize_nor_decentralized", ":centralization"),
        (create_text_overlay, "$g_presentation_obj_sliders_6", ":text"),
        (store_add, ":text", "str_dplmc_neither_aristocratic_nor_plutocratic", ":aristocracy"),
        (create_text_overlay, "$g_presentation_obj_sliders_7", ":text"),
        (store_add, ":text", "str_dplmc_mixture_serfs", ":serfdom"),
        (create_text_overlay, "$g_presentation_obj_sliders_8", ":text"),
        (store_add, ":text", "str_dplmc_mediocre_quality", ":quality"),
        (create_text_overlay, "$g_presentation_obj_sliders_9", ":text"),
        ##dplmc+ end incremented sliders by 1
        (store_add, ":text", "str_dplmc_neither_mercantilist_nor_laissez_faire", ":mercantilism"),
        (create_text_overlay, "$g_presentation_obj_sliders_10", ":text"),#<- dplmc+ added

        (create_text_overlay, "$g_presentation_obj_1", "@Centralization:"),
        (create_text_overlay, "$g_presentation_obj_2", "@Aristocracy:"),
        (create_text_overlay, "$g_presentation_obj_3", "@Serfdom:"),
        (create_text_overlay, "$g_presentation_obj_4", "@Troop quality:"),
        (create_text_overlay, "$g_presentation_obj_5", "@Mercantilism:"),#<-- dplmc+ added
        #dplmc+ start incremented obj by 1...
        (create_text_overlay, "$g_presentation_obj_6", "@High centralization reduces tax inefficiency for the king and raises it for vassals. This will interfere with relations between ruler and vassals."),
        (create_text_overlay, "$g_presentation_obj_7", "@High aristocracy will improve the relations between the king and his vassals who will be able to raise bigger armies but it will decreased trade."),
        (create_text_overlay, "$g_presentation_obj_8", "@High serfdom reduces tax inefficiency for the king and his vassals and vassals can maintain bigger armies but troops lose morale."),
        (create_text_overlay, "$g_presentation_obj_9", "@High troop quality increases the combat strength of troops but decreases army size."),
        #dplmc+ end incremented obj by 1
        (create_text_overlay, "$g_presentation_obj_10", "@High mercantilistic policies maximize exports while minimizing imports, and increase government regulation of industry."),#<-dplmc+ added

        ##Moved earlier
        #(faction_get_slot, ":centralization", "fac_player_supporters_faction", dplmc_slot_faction_centralization),
        #(faction_get_slot, ":aristocracy", "fac_player_supporters_faction", dplmc_slot_faction_aristocracy),
        #(faction_get_slot, ":serfdom", "fac_player_supporters_faction", dplmc_slot_faction_serfdom),
        #(faction_get_slot, ":quality", "fac_player_supporters_faction", dplmc_slot_faction_quality),
        #(faction_get_slot, ":mercantilism", "fac_player_supporters_faction", dplmc_slot_faction_quality),#<- dplmc+ added

        (overlay_set_val, "$g_presentation_obj_sliders_1", ":centralization"),
        (overlay_set_val, "$g_presentation_obj_sliders_2", ":aristocracy"),
        (overlay_set_val, "$g_presentation_obj_sliders_3", ":serfdom"),
        (overlay_set_val, "$g_presentation_obj_sliders_4", ":quality"),
        (overlay_set_val, "$g_presentation_obj_sliders_5", ":mercantilism"),#<- dplmc+ added
        (position_set_x, pos1, 200),

        ##SLIDERS
        #dplmc start+ pushed all items by 150, then dropped all items by 75, then decreased the spacing from 150 to 100
        (position_set_y, pos1, 575),#750),
        (overlay_set_position, "$g_presentation_obj_sliders_1", pos1),
        (position_set_y, pos1, 450),#600),
        (overlay_set_position, "$g_presentation_obj_sliders_2", pos1),
        (position_set_y, pos1, 325),#450),
        (overlay_set_position, "$g_presentation_obj_sliders_3", pos1),
        (position_set_y, pos1, 200),#300),
        (overlay_set_position, "$g_presentation_obj_sliders_4", pos1),
        #dplmc end+ end pushed all items by 150
        (position_set_y, pos1, 75),#150), #<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_sliders_5", pos1),#<- dplmc+ added


        ##HEADERS
        (position_set_x, pos1, 100),
        #dplmc+ start pushed all items by 150, then dropped all items by 75, then changed the spacing to 100
        (position_set_y, pos1, 625),#800),
        (overlay_set_position, "$g_presentation_obj_1", pos1),
        (position_set_y, pos1, 500),#650),
        (overlay_set_position, "$g_presentation_obj_2", pos1),
        (position_set_y, pos1, 375),#500),
        (overlay_set_position, "$g_presentation_obj_3", pos1),
        (position_set_y, pos1, 250),#350),
        (overlay_set_position, "$g_presentation_obj_4", pos1),
        #dplmc+ end pushed all items by 150
        (position_set_y, pos1, 125),#200), #<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_5", pos1), #<- dplmc+ added

        ##SLIDER DESCRIPTIONS
        (position_set_x, pos1, 50),
        #dplmc+ start pushed all items by 150, and incremented obj by 1, then dropped all items by 75, then raised it 10, then changed the spacing to 100
        (position_set_y, pos1, 550),#700),
        (overlay_set_position, "$g_presentation_obj_6", pos1),
        (position_set_y, pos1, 425),#550),
        (overlay_set_position, "$g_presentation_obj_7", pos1),
        (position_set_y, pos1, 300),#400),
        (overlay_set_position, "$g_presentation_obj_8", pos1),
        (position_set_y, pos1, 175),#250),
        (overlay_set_position, "$g_presentation_obj_9", pos1),
        #dplmc+ end pushed all items by 150, and incremented obj by 1
        (position_set_y, pos1, 50),#100), #<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_10", pos1), #<- dplmc+ added

        (position_set_x, pos1, 775),
        (position_set_y, pos1, 775),
        #dplmc+ start increment obj by 1
        (overlay_set_size, "$g_presentation_obj_6", pos1),
        (overlay_set_size, "$g_presentation_obj_7", pos1),
        (overlay_set_size, "$g_presentation_obj_8", pos1),
        (overlay_set_size, "$g_presentation_obj_9", pos1),
        #dplmc+ end increment obj by 1
        (overlay_set_size, "$g_presentation_obj_10", pos1),#<- dplmc+ added

        ##SLIDER LEVEL TEXT
        (position_set_x, pos1, 400),#400),
        #dplmc+ start pushed all items by 150, and incremented sliders by 1, then dropped all items by 75, then changed the spacing to 100
        (position_set_y, pos1, 575),#750),
        (overlay_set_position, "$g_presentation_obj_sliders_6", pos1),
        (position_set_y, pos1, 450),#600),
        (overlay_set_position, "$g_presentation_obj_sliders_7", pos1),
        (position_set_y, pos1, 325),#450),
        (overlay_set_position, "$g_presentation_obj_sliders_8", pos1),
        (position_set_y, pos1, 200),#300),
        (overlay_set_position, "$g_presentation_obj_sliders_9", pos1),
        #dplmc+ end pushed all items by 150, and incremented sliders by 1
        (position_set_y, pos1, 75),#150),#<- dplmc+ added
        (overlay_set_position, "$g_presentation_obj_sliders_10", pos1),#<- dplmc+ added

        (position_set_x, pos1, 925),
        (position_set_y, pos1, 925),
        #dplmc+ start incremented sliders by 1
        (overlay_set_size, "$g_presentation_obj_sliders_6", pos1),
        (overlay_set_size, "$g_presentation_obj_sliders_7", pos1),
        (overlay_set_size, "$g_presentation_obj_sliders_8", pos1),
        (overlay_set_size, "$g_presentation_obj_sliders_9", pos1),
        #dplmc+ end incremented sliders by 1
        (overlay_set_size, "$g_presentation_obj_sliders_10", pos1),#<- dplmc+ added
        ]),
      # (ti_on_presentation_run,
       # [
        # ]),
      (ti_on_presentation_event_state_change,
       [(store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),
        ##nested diplomacy start+
        #Added new option, so had to increment some sliders
        (try_begin),
          (eq, ":object", "$g_presentation_obj_sliders_1"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_centralization, ":value"),
          (val_add, ":value", "str_dplmc_neither_centralize_nor_decentralized"),
          (overlay_set_text, "$g_presentation_obj_sliders_6", ":value"),#dplmc+ incremented "sliders"
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_2"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_aristocracy, ":value"),
          (val_add, ":value", "str_dplmc_neither_aristocratic_nor_plutocratic"),
          (overlay_set_text, "$g_presentation_obj_sliders_7", ":value"),#dplmc+ incremented "sliders"
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_3"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_serfdom, ":value"),
          (val_add, ":value", "str_dplmc_mixture_serfs"),
          (overlay_set_text, "$g_presentation_obj_sliders_8", ":value"),#dplmc+ incremented "sliders"
        (else_try),
          (eq, ":object", "$g_presentation_obj_sliders_4"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_quality, ":value"),
          (val_add, ":value", "str_dplmc_mediocre_quality"),
          (overlay_set_text, "$g_presentation_obj_sliders_9", ":value"),#dplmc+ incremented "sliders"
        #Finished incremented sliders.
        (else_try),
          #dplmc+ new option: mercantilism
          (eq, ":object", "$g_presentation_obj_sliders_5"),
          (faction_set_slot,  "fac_player_supporters_faction", dplmc_slot_faction_mercantilism, ":value"),
          (val_add, ":value", "str_dplmc_neither_mercantilist_nor_laissez_faire"),
          (overlay_set_text, "$g_presentation_obj_sliders_10", ":value"),
        #Change variable associated with "Done" button.
        (else_try),
          (eq, ":object", "$g_presentation_obj_12"),#dplmc+ changed 10 to 12
          (assign, "$g_players_policy_set", 1),
          (presentation_set_duration, 0),
        (else_try), #SB : randomize and restart presentation
          (eq, ":object", "$g_presentation_obj_11"),#dplmc+ changed 10 to 12
          (call_script, "script_dplmc_randomize_faction_domestic_policy", "fac_player_supporters_faction"),
          (start_presentation, "prsnt_dplmc_policy_management"),
        (try_end),
        ##nested diplomacy end+
      ]),
    ])
