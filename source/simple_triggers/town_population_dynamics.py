# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from header_terrain_types import *
from module_factions import dplmc_factions_end

from module_constants import *

from compiler import *

town_population_dynamics_simple_triggers = [
(24*14,
	[
		(try_for_range, ":town_no", towns_begin, towns_end),							#	Floris	//	Adjust Population Depending on Prosperity
			(party_get_slot, ":prosperity", ":town_no", slot_town_prosperity),
			(party_get_slot, ":population", ":town_no", slot_center_population),
			(assign,":change",0),
			(try_begin),
				(ge, ":prosperity", 60),
				(store_sub, ":change", ":prosperity",60),
				(val_div, ":change", 5),
				(val_add, ":change", 3),
			(else_try),
				(le, ":prosperity", 40),
				(store_sub, ":change", ":prosperity", 40),
				(val_div, ":change", 5),
				(val_sub, ":change", 3),
			(try_end),
			(store_div,":base",":population",100),										#	Base population change is 1% of pop
			(val_mul,":change",":base"),				
			(val_add,":population", ":change"),			
			(try_begin),
				(gt, ":population", 30000),
				(assign, ":population", 30000),
				(party_set_slot, ":town_no", slot_center_population, ":population"),
			(else_try),
				(lt, ":population", 5000),
				(assign, ":population", 5000),
				(party_set_slot, ":town_no", slot_center_population, ":population"),
			(else_try),
				(party_set_slot, ":town_no", slot_center_population, ":population"),
			(try_end),
		(try_end),	
 
		(try_for_range, ":town_no", towns_begin, towns_end),							#	Floris	//	Calculating Land Demand and Consequences for supply, pricing and renting
			(party_get_slot, ":population", ":town_no", slot_center_population),
			(party_get_slot, ":land_town", ":town_no", slot_town_acres),
			(party_get_slot, ":land_player", ":town_no", slot_player_acres),
			(party_get_slot, ":prosperity", ":town_no", slot_town_prosperity),
			(store_sub, ":revenue", ":prosperity", 50),
			(val_add, ":revenue", 100),
			(try_begin),
				(store_div, ":acres_needed", ":population", 200),						#	200 People warrant 1 acre of cultivated land
				(store_add, ":total_land", ":land_town", ":land_player"),
				(store_sub, ":surplus", ":total_land", ":acres_needed"),
 
				(try_begin),															#	AI Consequences
					(lt, ":total_land", ":acres_needed"),
					(store_sub, ":new_acres", ":acres_needed", ":total_land"),
					(val_add, ":land_town", ":new_acres"),
					(party_set_slot, ":town_no", slot_town_acres, ":land_town"),
				(else_try),
					(ge, ":surplus", 20),
					(val_sub, ":land_town", 2),
					(party_set_slot, ":town_no", slot_town_acres, ":land_town"),
				(try_end),
 
				(try_begin),															#	Player Consequences
					(le, ":total_land", ":acres_needed"),
					(val_mul, ":land_player", ":revenue"),										
					(party_set_slot, ":town_no", slot_rent, ":land_player"),
				(else_try),
					(store_mul, ":penalty", ":surplus", -1),
					(val_add, ":penalty", ":revenue"),
					(try_begin),
						(ge, ":penalty", 85),
						(val_mul, ":land_player", ":penalty"),
						(party_set_slot, ":town_no", slot_rent, ":land_player"),
					(else_try),
						(store_sub, ":non_rented", ":surplus", 15),
						(val_sub, ":land_player", ":non_rented"),
						(try_begin),													#	Safety check // No penalty on rent should turn rent negative.
							(lt, ":penalty", 0),
							(assign, ":penalty", 0),
						(try_end),
						(val_mul, ":land_player", ":penalty"),
						(party_set_slot, ":town_no", slot_rent, ":land_player"),
						(val_mul, ":non_rented", -50),
						(party_set_slot, ":town_no", slot_upkeep, ":non_rented"),
					(try_end),
				(try_end),
 
			(try_end),
			(party_get_slot, ":assets", ":town_no", slot_assets),						#	Adding/Subtracting profits/losses
			(party_get_slot, ":rent", ":town_no", slot_rent),
			(party_get_slot, ":upkeep", ":town_no", slot_upkeep),
			(val_add, ":assets", ":rent"),
			(val_add, ":assets", ":upkeep"),
			(party_set_slot, ":town_no", slot_assets, ":assets"),			
		(try_end),
 
	]),
]
