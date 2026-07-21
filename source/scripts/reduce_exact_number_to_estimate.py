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
from ID_strings import str_key_0
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin

reduce_exact_number_to_estimate_scripts = [
##diplomacy end
(
	"reduce_exact_number_to_estimate",
	#This is used to simulate limited intelligence
	#It is roughly analogous to the descriptive strings which the player will receive from alarms
	#Information is presumed to be accurate for four days
	#This is obviously cheating for the AI, as the AI will have exact info for four days, and no info at all after that.
	#It would be fairly easy to log the strength at a center when it is scouted, if we want, but I have not done that at this point,
	#The AI also has a hive mind -- ie, each party knows what its allies are thinking. In this, AI factions have an advantage over the player
	#It would be a simple matter to create a set of arrays in which each party's knowledge is individually updated, but that would also take up a lot of data space

	[
		(store_script_param, ":exact_number", 1),

		(try_begin),
			(lt, ":exact_number", 500),
			(assign, ":estimate", 0),
		(else_try),
			(lt, ":exact_number", 1000),
			(assign, ":estimate", 750),
		(else_try),
			(lt, ":exact_number", 2000),
			(assign, ":estimate", 1500),
		(else_try),
			(lt, ":exact_number", 4000),
			(assign, ":estimate", 3000),
		(else_try),
			(lt, ":exact_number", 8000),
			(assign, ":estimate", 6000),
		(else_try),
			(lt, ":exact_number", 16000),
			(assign, ":estimate", 12000),
		(else_try),
			(assign, ":estimate", 24000),
		(try_end),
		##diplomacy start+
		#This currently isn't used anywhere, but modify it if we're thinking about changing that.
		#Take into account campaign AI difficulty -- assume that the difference is either a good
		#spy network or intelligent inference.
		(game_get_reduce_campaign_ai, reg0),
		(try_begin),
			(lt, reg0, 1),#Hard mode
			(assign, ":estimate", ":exact_number"),
		(else_try),
			(eq, reg0, 1),#Medium Mode
			(val_add, ":estimate", ":exact_number"),
			(val_div, ":estimate", 2),
		(try_end),
		##diplomacy end+

		(assign, reg0, ":estimate"),
	])
]
