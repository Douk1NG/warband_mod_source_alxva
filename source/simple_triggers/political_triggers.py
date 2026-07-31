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



    #POLITICAL TRIGGERS
	#POLITICAL TRIGGER #1`
   

political_triggers_simple_triggers = [
(8, #increased from 12
    [
	(call_script, "script_cf_random_political_event"),

	#Added Nov 2010 begins - do this twice
	(call_script, "script_cf_random_political_event"),
	#Added Nov 2010 ends

	#This generates quarrels and occasional reconciliations and interventions
	]),
]
