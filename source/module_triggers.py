# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *

from module_constants import *

from compiler import *
####################################################################################################################
#  Each trigger contains the following fields:
# 1) Check interval: How frequently this trigger will be checked
# 2) Delay interval: Time to wait before applying the consequences of the trigger
#    After its conditions have been evaluated as true.
# 3) Re-arm interval. How much time must pass after applying the consequences of the trigger for the trigger to become active again.
#    You can put the constant ti_once here to make sure that the trigger never becomes active again after it fires once.
# 4) Conditions block (list). This must be a valid operation block. See header_operations.py for reference.
#    Every time the trigger is checked, the conditions block will be executed.
#    If the conditions block returns true, the consequences block will be executed.
#    If the conditions block is empty, it is assumed that it always evaluates to true.
# 5) Consequences block (list). This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################
# Granular layout: one file per trigger block in source/triggers/.

# Some constants for use below
merchant_inventory_space = 30
num_merchandise_goods = 36



from triggers.tutorial_map1 import tutorial_map1_triggers
from triggers.refresh_center_inventories import refresh_center_inventories_triggers
from triggers.refresh_center_armories import refresh_center_armories_triggers
from triggers.refresh_center_weaponsmiths import refresh_center_weaponsmiths_triggers
from triggers.refresh_center_stables import refresh_center_stables_triggers
from triggers.track_down_bandits_quest import track_down_bandits_quest_triggers
from triggers.prisoner_train_ai import prisoner_train_ai_triggers
from triggers.caravan_escort_cancel import caravan_escort_cancel_triggers
from triggers.messenger_party_ai import messenger_party_ai_triggers
from triggers.kingdom_parties import kingdom_parties_triggers
from triggers.incriminate_loyal_commander_quest import incriminate_loyal_commander_quest_triggers
from triggers.bring_back_runaway_serfs_quest import bring_back_runaway_serfs_quest_triggers
from triggers.follow_spy_quest import follow_spy_quest_triggers
from triggers.merchants_guild_debt_interest import merchants_guild_debt_interest_triggers
from triggers.escort_merchant_caravan_mode1 import escort_merchant_caravan_mode1_triggers
from triggers.escort_merchant_caravan_mode0 import escort_merchant_caravan_mode0_triggers
from triggers.escort_merchant_caravan_abort import escort_merchant_caravan_abort_triggers
from triggers.troublesome_bandits_abort import troublesome_bandits_abort_triggers
from triggers.troublesome_bandits_succeed import troublesome_bandits_succeed_triggers
from triggers.kidnapped_girl_quest import kidnapped_girl_quest_triggers
from triggers.rebellion_pretender_relocation import rebellion_pretender_relocation_triggers
from triggers.companion_candidates_taverns import companion_candidates_taverns_triggers
from triggers.npc_morale_clashes import npc_morale_clashes_triggers
from triggers.lady_of_the_lake import lady_of_the_lake_triggers
from triggers.appoint_chamberlain import appoint_chamberlain_triggers
from triggers.appoint_constable import appoint_constable_triggers
from triggers.appoint_chancellor import appoint_chancellor_triggers
from triggers.autoloot_initialize import autoloot_initialize_triggers
from triggers.move_fast_reset import move_fast_reset_triggers
from triggers.zaitenko_reinforcements import zaitenko_reinforcements_triggers
from triggers.feast_relations import feast_relations_triggers
from triggers.transfer_mode_reset import transfer_mode_reset_triggers

triggers = []
triggers.extend(tutorial_map1_triggers)
triggers.extend(refresh_center_inventories_triggers)
triggers.extend(refresh_center_armories_triggers)
triggers.extend(refresh_center_weaponsmiths_triggers)
triggers.extend(refresh_center_stables_triggers)
triggers.extend(track_down_bandits_quest_triggers)
triggers.extend(prisoner_train_ai_triggers)
triggers.extend(caravan_escort_cancel_triggers)
triggers.extend(messenger_party_ai_triggers)
triggers.extend(kingdom_parties_triggers)
triggers.extend(incriminate_loyal_commander_quest_triggers)
triggers.extend(bring_back_runaway_serfs_quest_triggers)
triggers.extend(follow_spy_quest_triggers)
triggers.extend(merchants_guild_debt_interest_triggers)
triggers.extend(escort_merchant_caravan_mode1_triggers)
triggers.extend(escort_merchant_caravan_mode0_triggers)
triggers.extend(escort_merchant_caravan_abort_triggers)
triggers.extend(troublesome_bandits_abort_triggers)
triggers.extend(troublesome_bandits_succeed_triggers)
triggers.extend(kidnapped_girl_quest_triggers)
triggers.extend(rebellion_pretender_relocation_triggers)
triggers.extend(companion_candidates_taverns_triggers)
triggers.extend(npc_morale_clashes_triggers)
triggers.extend(lady_of_the_lake_triggers)
triggers.extend(appoint_chamberlain_triggers)
triggers.extend(appoint_constable_triggers)
triggers.extend(appoint_chancellor_triggers)
triggers.extend(autoloot_initialize_triggers)
triggers.extend(move_fast_reset_triggers)
triggers.extend(zaitenko_reinforcements_triggers)
triggers.extend(feast_relations_triggers)
triggers.extend(transfer_mode_reset_triggers)

# modmerger_start version=201 type=2
try:
    component_name = "triggers"
    var_set = { "triggers" : triggers }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
