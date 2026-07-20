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

bank = ("bank", 0, mesh_load_window, [ 													#	Floris Overhaul
    (ti_on_presentation_load,
      [
        (presentation_set_duration, 999999),
        (set_fixed_point_multiplier, 1000),

		(try_begin),
			(party_get_slot, ":assets", "$current_town", slot_assets),
			(troop_add_gold, "trp_player", ":assets"),
			(party_set_slot, "$current_town", slot_assets, 0),
		(try_end),

		(str_store_party_name, s1, "$current_town"),


	    (create_text_overlay, reg0,
"@This area of {s1} can best be described as the very core of the town.^^\
 You can almost see the strings that are being pulled from here, the money that comes and goes at seemingly endless rates. \
 Here you can buy the land that is cultivated outside the towns gates and benefit from the ones working hard.\
 Of course you might not have the denars required to do so, but the moneylenders are known to have some spare change.",tf_center_justify),
        (position_set_x, pos1, 475),
        (position_set_y, pos1, 600),
        (overlay_set_position, reg0, pos1),

        (position_set_x, pos2, 800),
        (position_set_y, pos2, 900),
		(overlay_set_size, reg0, pos2),

		(party_get_slot, ":population", "$current_town", slot_center_population),
		(party_get_slot, ":land_town", "$current_town", slot_town_acres),
		(party_get_slot, ":land_player", "$current_town", slot_player_acres),
		(store_add, ":land_total", ":land_town", ":land_player"),
		(assign, reg1, ":population"),
		(assign, reg2, ":land_total"),
		(assign, reg3, ":land_player"),

		(party_get_slot, ":debt", "$current_town", slot_debt),
		(assign, reg4, ":debt"),

		(assign, reg5, 0),														#Slider storage / acres		Buy
		(assign, reg6, 0),														#Slider storage / money		Borrow
		(assign, reg7, 0),														#Slider storage / acres		Build
		(assign, reg8, 0),														#Slider storage / money		Pay back

		(party_get_slot, ":prosp_mod", "$current_town", slot_town_prosperity),
		(store_mul, ":price_mod", ":prosp_mod", 10),
		(val_sub, ":price_mod", 500),
		(store_add, reg9, 1000, ":price_mod"),									#Buy Price
		(store_add, reg10, 750, ":price_mod"),									#Sell Price
		(store_add, reg11, 2000, ":price_mod"),									#Build Price
		#reg12 used for buy/sell switch
		(store_sub, ":rent_mod", ":prosp_mod", 50),
		(store_add, reg13, ":rent_mod", 100),									#Rent Revenue

		(create_text_overlay, "$g_presentation_obj_19", "@{reg1} people live in {s1}. There are currently {reg2} acres of land available for cultivation to provide them with \
 food and other goods. You own {reg3} acres of land in this town. You currently owe the moneylenders of {s1} {reg4} denars. The interest rate is 20% and the contract period amounts \
 to 2 weeks. If you dont manage to pay off your debt until the deadline, the interest is raised to 40%. Buying an existing acre costs {reg9} denars, while it sells for {reg10} denars. Building a new one requires {reg11} denars.\
 The rent paid to landowners currently accumulates to {reg13} denars per acre every 2 weeks and has to be collected in the town. Land wont be rented if a town is already well supplied.",tf_center_justify),
        (position_set_x, pos1, 475),
        (position_set_y, pos1, 450),
        (overlay_set_position, "$g_presentation_obj_19", pos1),

        (position_set_x, pos2, 900),
        (position_set_y, pos2, 1000),
		(overlay_set_size, "$g_presentation_obj_19", pos2),

		(try_begin),
			(eq, reg12, 2222),
			(str_store_string, s2, "@Choose how many acres you wish to sell :"),
		(else_try),
			(str_store_string, s2, "@Choose how many acres you wish to buy :"),
		(try_end),

	(create_button_overlay, "$g_presentation_obj_16", "@{s2}",tf_center_justify),				#	Landlords buy
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 350),
        (overlay_set_position, "$g_presentation_obj_16", pos1),

		(store_troop_gold, ":funds", "trp_player"),
		(store_div, ":funds_build", ":funds", reg11),
		(val_div, ":funds", reg9),
		(val_min, ":funds", ":land_town"),

		(try_begin),
			(eq, reg12, 2222),
			(party_get_slot, ":sell_no", "$current_town", slot_player_acres),
			(assign, ":funds", ":sell_no"),
		(try_end),

	(create_slider_overlay, "$g_presentation_obj_1", 0, ":funds"),
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 310),
        (overlay_set_position, "$g_presentation_obj_1", pos1),

	(create_text_overlay, "$g_presentation_obj_2", "@0"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 300),
        (overlay_set_position, "$g_presentation_obj_2", pos1),

	(create_button_overlay, "$g_presentation_obj_3", "@Verify",tf_center_justify),
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 275),
        (overlay_set_position, "$g_presentation_obj_3", pos1),



	(create_text_overlay, reg0, "@Choose how much money you wish to borrow :",tf_center_justify),			#	Moneylenders borrow
        (position_set_x, pos1, 725),
        (position_set_y, pos1, 350),
        (overlay_set_position, reg0, pos1),

		(assign, ":fief_count", 0),																				#	Money = 250*Prosperity + Relationship*100 - Debt, IF Player owns fief or is renowned,
		(try_for_range, ":cur_center", centers_begin, centers_end),												#	otherwise not more than 5000 + Relationship*100 - Debt
			(party_slot_eq, ":cur_center", slot_town_lord, "trp_player"),
			(val_add, ":fief_count", 1),
		(try_end),
		(troop_get_slot, ":renown", "trp_player", slot_troop_renown),
		(party_get_slot, ":prosperity", "$current_town", slot_town_prosperity),
		(store_mul, ":money", ":prosperity", 250),
		(try_begin),
			(lt, ":fief_count", 1),
			(lt, ":renown", 500),
			(gt, ":money", 5000),
			(assign, ":money", 5000),
		(try_end),
		(party_get_slot, ":player_relation", "$current_town", slot_center_player_relation),
		(store_mul, ":trust", ":player_relation", 100),
		(val_add, ":money", ":trust"),
		(val_sub, ":money", ":debt"),
		(try_begin),																							#	Money lending cant turn negative
			(lt, ":money", 0),
			(assign, ":money", 0),
		(try_end),

		(try_begin),
			(assign, reg25, 0),
			(try_for_range, ":town_no", towns_begin, towns_end),													#	Too much debt overall or in a single bank will stop banks from lending you money
				(party_get_slot, ":debt_all", ":town_no", slot_debt),
				(val_add, reg25, ":debt_all"),
			(try_end),
			(ge, reg25, 50000),
			(assign, ":money", 0),
		(try_end),

	(create_slider_overlay, "$g_presentation_obj_4", 0, ":money"),
        (position_set_x, pos1, 700),
        (position_set_y, pos1, 310),
        (overlay_set_position, "$g_presentation_obj_4", pos1),

	(create_text_overlay, "$g_presentation_obj_5", "@0"),
        (position_set_x, pos1, 850),
        (position_set_y, pos1, 300),
        (overlay_set_position, "$g_presentation_obj_5", pos1),

	(create_button_overlay, "$g_presentation_obj_6", "@Verify",tf_center_justify),
        (position_set_x, pos1, 700),
        (position_set_y, pos1, 275),
        (overlay_set_position, "$g_presentation_obj_6", pos1),



	(create_text_overlay, "$g_presentation_obj_7", "@Buy and prepare uncultivated land :",tf_center_justify),		#	Landlord / Buy and Build
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 200),
        (overlay_set_position, "$g_presentation_obj_7", pos1),


	(create_slider_overlay, "$g_presentation_obj_8", 0, ":funds_build"),											#	Choose acres to build
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 160),
        (overlay_set_position, "$g_presentation_obj_8", pos1),

	(create_text_overlay, "$g_presentation_obj_9", "@0"),
        (position_set_x, pos1, 400),
        (position_set_y, pos1, 150),
        (overlay_set_position, "$g_presentation_obj_9", pos1),

	(create_button_overlay, "$g_presentation_obj_10", "@Verify",tf_center_justify),
        (position_set_x, pos1, 250),
        (position_set_y, pos1, 125),
        (overlay_set_position, "$g_presentation_obj_10", pos1),


	(create_text_overlay, "$g_presentation_obj_11", "@Pay off your debt :",tf_center_justify),		#	Pay off your debt
        (position_set_x, pos1, 700),
        (position_set_y, pos1, 200),
        (overlay_set_position, "$g_presentation_obj_11", pos1),

		(store_troop_gold, ":funds", "trp_player"),
		(try_begin),
			(lt, ":debt", ":funds"),
			(assign, ":funds", ":debt"),
		(try_end),

	(create_slider_overlay, "$g_presentation_obj_12", 0, ":funds"),
        (position_set_x, pos1, 700),
        (position_set_y, pos1, 160),
        (overlay_set_position, "$g_presentation_obj_12", pos1),

	(create_text_overlay, "$g_presentation_obj_13", "@0"),
        (position_set_x, pos1, 850),
        (position_set_y, pos1, 150),
        (overlay_set_position, "$g_presentation_obj_13", pos1),

	(create_button_overlay, "$g_presentation_obj_14", "@Verify",tf_center_justify),
        (position_set_x, pos1, 700),
        (position_set_y, pos1, 125),
        (overlay_set_position, "$g_presentation_obj_14", pos1),



	(create_game_button_overlay, "$g_presentation_obj_15", "@Done", 0),										#	Leave
        (position_set_x, pos1, 880),
        (position_set_y, pos1, 25),
        (overlay_set_position, "$g_presentation_obj_15", pos1),

        ]),

	(ti_on_presentation_event_state_change,
		[
        (store_trigger_param_1, ":object"),
        (store_trigger_param_2, ":value"),

		(try_begin),
			(eq, ":object", "$g_presentation_obj_1"),															#	Show chosen amount of land
			(assign, reg5, ":value"),
			(overlay_set_text, "$g_presentation_obj_2", "@{reg5}"),
		(else_try),
			(eq, ":object", "$g_presentation_obj_3"),															#	Sell/Buy chosen amount of land
			(try_begin),
				(eq, reg12, 2222),
				(try_begin),
					(gt, reg5, 0),
					(store_mul, ":price", reg5, reg10),
					(troop_add_gold, "trp_player", ":price"),
					(party_get_slot, ":land_town", "$current_town", slot_town_acres),
					(val_add, ":land_town", reg5),
					(party_set_slot, "$current_town", slot_town_acres, ":land_town"),
					(party_get_slot, ":land_player", "$current_town", slot_player_acres),
					(val_sub, ":land_player", reg5),
					(party_set_slot, "$current_town", slot_player_acres, ":land_player"),
					(start_presentation, "prsnt_bank"),
				(else_try),
					(display_message, "@You cant sell 0 acres of land."),
				(try_end),
			(else_try),
				(try_begin),
					(gt, reg5, 0),
					(store_mul, ":cost", reg5, reg9),
					(troop_remove_gold, "trp_player", ":cost"),
					(party_get_slot, ":land_town", "$current_town", slot_town_acres),
					(val_sub, ":land_town", reg5),
					(party_set_slot, "$current_town", slot_town_acres, ":land_town"),
					(party_get_slot, ":land_player", "$current_town", slot_player_acres),
					(val_add, ":land_player", reg5),
					(party_set_slot, "$current_town", slot_player_acres, ":land_player"),
					(start_presentation, "prsnt_bank"),
				(else_try),
					(display_message, "@You cant buy 0 acres of land."),
				(try_end),
			(try_end),
		(else_try),
			(eq, ":object", "$g_presentation_obj_4"),															#	Show chosen amount of money
			(assign, reg6, ":value"),
			(overlay_set_text, "$g_presentation_obj_5", "@{reg6}"),
		(else_try),
			(eq, ":object", "$g_presentation_obj_6"),															#	Borrow chosen amount of money
			(try_begin),
				(gt, reg6, 0),
				(party_get_slot, ":debt", "$current_town", slot_debt),
				(try_begin),
					(le, ":debt", 0),
					(store_current_hours, ":date"),
					(val_add, ":date", 24*14*2), 								#	First Deadline / 4 weeks / then 2 weeks (see simple_triggers)
					(party_set_slot, "$current_town", slot_deadline, ":date"),
				(try_end),
				(troop_add_gold, "trp_player", reg6),
				(val_mul, reg6, 120),
				(val_div, reg6, 100),
				(val_add, ":debt", reg6),
				(party_set_slot, "$current_town", slot_debt, ":debt"),
				(start_presentation, "prsnt_bank"),
			(else_try),
				(display_message, "@You cant borrow 0 denars."),
			(try_end),
		(else_try),
			(eq, ":object", "$g_presentation_obj_8"),															#	Show chosen amount of land	//	2nd Option
			(assign, reg7, ":value"),
			(overlay_set_text, "$g_presentation_obj_9", "@{reg7}"),
		(else_try),
			(eq, ":object", "$g_presentation_obj_10"),															#	Buy chosen amount of land	//	2nd Option
			(try_begin),
				(gt, reg7, 0),
				(store_mul, ":cost", reg7, reg11),
				(troop_remove_gold, "trp_player", ":cost"),
				(party_get_slot, ":land_player", "$current_town", slot_player_acres),
				(val_add, ":land_player", reg7),
				(party_set_slot, "$current_town", slot_player_acres, ":land_player"),
				(start_presentation, "prsnt_bank"),
			(else_try),
				(display_message, "@You cant buy 0 acres of land."),
			(try_end),
		(else_try),
			(eq, ":object", "$g_presentation_obj_12"),															#	Show chosen amount of money
			(assign, reg8, ":value"),
			(overlay_set_text, "$g_presentation_obj_13", "@{reg8}"),
		(else_try),
			(eq, ":object", "$g_presentation_obj_14"),															#	Pay back chosen amount of money
			(try_begin),
				(gt, reg8, 0),
				(troop_remove_gold, "trp_player", reg8),
				(party_get_slot, ":debt", "$current_town", slot_debt),
				(val_sub, ":debt", reg8),
				(party_set_slot, "$current_town", slot_debt, ":debt"),
				(try_begin),
					(le, ":debt", 0),
					(party_set_slot, "$current_town", slot_deadline, 0),
				(try_end),
				(start_presentation, "prsnt_bank"),
			(else_try),
				(display_message, "@You cant pay back 0 denars."),
			(try_end),
		(else_try),																								#	Switch Buy/Sell
			(eq, ":object", "$g_presentation_obj_16"),
			(try_begin),
				(neq, reg12, 2222),
				(assign, reg12, 2222),
				(start_presentation, "prsnt_bank"),
			(else_try),
				(assign, reg12, 0),
				(start_presentation, "prsnt_bank"),
			(try_end),
		(else_try),
			(eq, ":object", "$g_presentation_obj_15"),															#	Leave
			(presentation_set_duration, 0),
		(try_end),

		]),
      ])
