from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *
from header_music import *
from module_constants import *

from cstm_header_simple_triggers import *
from cstm_constants import *

####################################################################################################################
# Simple triggers are the alternative to old style triggers. They do not preserve state, and thus simpler to maintain.
#
#	Each simple trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference. 
####################################################################################################################

# Build comprehensive save-game fix operations (runs once on first load after mod update)
fix_operations = [
	(try_begin),
		(neq, "$g_cstm_save_fix_applied", 1),
		
		# Rebuild item arrays from scratch (fixes invalid item IDs like 1938 in old saves)
		(call_script, "script_cstm_setup_item_arrays"),
]

# Recalculate equipment funds for all troop levels (fixes negative funds on old saves)
# 1.5x multiplier to compensate for the corrected price calculation
for i in xrange(64):
	inventory_value = equipment_funds_available(i)
	inventory_value = int(round(inventory_value * 1.5))
	fix_operations.append((troop_set_slot, "trp_cstm_inventory_values", i, inventory_value))

# Recalculate proficiency requirements (in case they changed between versions)
previous_requirement = 0
for i in xrange(max(cstm_proficiency_requirements.keys()) + 1):
	requirement = previous_requirement
	if i in cstm_proficiency_requirements:
		requirement = cstm_proficiency_requirements[i]
		previous_requirement = requirement
	fix_operations.append((troop_set_slot, "trp_cstm_proficiency_requirements", i, requirement))

# Re-set item types on each array troop (ensures arrays are correctly categorized)
for item_type in cstm_item_type_strings.keys():
	fix_operations.append((troop_set_slot, "trp_" + cstm_items_array_id(item_type), cstm_slot_array_item_type, item_type))

fix_operations.append((assign, "$g_cstm_save_fix_applied", 1))
fix_operations.append((try_end,))

new_simple_triggers = [

	# This trigger will activate upon the game being loaded
	(0, fix_operations),
	
]

def modmerge(var_set):
	try:
		var_name_1 = "simple_triggers"
		orig_simple_triggers = var_set[var_name_1]
	except KeyError:
		errstring = "Variable set does not contain expected variable: \"%s\"." % var_name_1
		raise ValueError(errstring)
	
	orig_simple_triggers.extend(new_simple_triggers)
	
	simple_triggers = [SimpleTrigger(*st_tuple) for st_tuple in orig_simple_triggers]
	
	del orig_simple_triggers[:]
	orig_simple_triggers.extend([simple_trigger.convert_to_tuple() for simple_trigger in simple_triggers])
