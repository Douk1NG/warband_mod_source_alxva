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

debt_consequences_simple_triggers = [
(1, 																				
	[	
		(try_for_range, ":town_no", towns_begin, towns_end),							#	Floris Moneylenders // Not paying debts has consequences
			(party_get_slot, ":debt", ":town_no", slot_debt),
			(gt, ":debt", 0),															#	If a debt exists, a deadline exists
			(party_get_slot, ":deadline", ":town_no", slot_deadline),
			(store_current_hours, ":date"),
			(ge, ":date", ":deadline"),
			(call_script, "script_change_player_relation_with_center", ":town_no", -25, 0xff3333),
			(try_begin),
				(lt, ":debt", 100000),
				(val_mul, ":debt", 14),
				(val_div, ":debt", 10),
				(try_begin),
					(gt, ":debt", 100000),												#Debt doesnt get higher than 100000 denars
					(assign, ":debt", 100000),
				(try_end),
				(val_add, ":deadline", 24*14),
				(party_set_slot, ":town_no", slot_debt, ":debt"),
				(party_set_slot, ":town_no", slot_deadline, ":deadline"),
				(str_store_party_name, s1, ":town_no"),
				(display_message, "@You missed the deadline to pay back your debts in {s1}. They now grow at an interest of 50%."),
			(else_try),
				(assign, ":debt", 100000),												#If debt = 100000 denars, then additionally to -5 relation with town, you get -1 relation with Faction.
				(val_add, ":deadline", 24*14),
				(party_set_slot, ":town_no", slot_debt, ":debt"),
				(party_set_slot, ":town_no", slot_deadline, ":deadline"),
				(store_faction_of_party, ":faction_no", ":town_no"),
				(call_script, "script_change_player_relation_with_faction_ex", ":faction_no", -10),
				(str_store_party_name, s1, ":town_no"),
				(display_message, "@Your debt in {s1} is now so high that the King himself has taken notice. He has frozen your debt, but is extremely displeased with the situation.", 0xff3333),
			(try_end),
		(try_end),		
	 
	]),
]
