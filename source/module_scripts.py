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
from scripts.music.music_scripts import music_scripts
from scripts.battle.formation_orders.formation_orders_scripts import formation_orders_scripts
from scripts.siege.siege_scripts import siege_scripts
from scripts.training_ground.training_ground_scripts import training_ground_scripts
from scripts.multiplayer.multiplayer_scripts import multiplayer_scripts
from scripts.economy.economy_scripts import economy_scripts
from scripts.quests.quest_scripts import quest_scripts
from scripts.morale.morale_scripts import morale_scripts
from scripts.banners.banners_scripts import banners_scripts
from scripts.arena.arena_scripts import arena_scripts
from scripts.encounters.encounters_scripts import encounters_scripts
from scripts.party_ai.party_ai_scripts import party_ai_scripts
from scripts.centers.centers_scripts import centers_scripts
from scripts.npcs.npcs_scripts import npcs_scripts
from scripts.faction_ai.faction_ai_scripts import faction_ai_scripts
from scripts.engine.engine_scripts import engine_scripts
from scripts.diplomacy.diplomacy_scripts import diplomacy_scripts
from scripts.player.player_scripts import player_scripts
from scripts.ui.ui_scripts import ui_scripts
from scripts.battle.tactics.tactics_scripts import tactics_scripts
from scripts.quests.courtship_scripts import courtship_scripts
from scripts.quests.feast_scripts import feast_scripts
from scripts.faction_ai.rebellion_scripts import rebellion_scripts
from scripts.dickplomacy.dickplomacy_scripts import dickplomacy_scripts
from scripts.centers.tavern_scripts import tavern_scripts
from scripts.features.item_modifiers_scripts import item_modifiers_scripts
from scripts.features.inventory_scripts import inventory_scripts
from scripts.features.weapon_toggle_scripts import weapon_toggle_scripts

##diplomacy start+
from module_factions import dplmc_factions_begin, dplmc_factions_end, dplmc_non_generic_factions_begin
##diplomacy end+

##diplomacy begin
##jrider reports
from header_presentations import tf_left_align
  #### Autoloot improved by rubik begin
from module_items import *

## deprecated due to 1.165 operations
# ibf_item_type_mask = 0x000000ff

# def set_item_difficulty():
  # item_difficulty = []
  # for i_item in xrange(len(items)):
    # item_difficulty.append((item_set_slot, i_item, dplmc_slot_item_difficulty, get_difficulty(items[i_item][6])))
  # return item_difficulty[:]

# def set_item_base_score():
  # item_base_score = []
  # for i_item in xrange(len(items)):
    # if items[i_item][3] & ibf_item_type_mask == itp_type_two_handed_wpn and items[i_item][3] & itp_two_handed == 0:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_two_handed_one_handed, 1))
    # type = items[i_item][3] & ibf_item_type_mask
    # if type >= itp_type_head_armor and type <= itp_type_hand_armor:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_head_armor, get_head_armor(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_body_armor, get_body_armor(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_leg_armor, get_leg_armor(items[i_item][6])))
    # elif type >= itp_type_one_handed_wpn and type <= itp_type_thrown and type != itp_type_shield:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_thrust_damage, get_thrust_damage(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_swing_damage, get_swing_damage(items[i_item][6])))
    # elif type == itp_type_horse:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_horse_speed, get_missile_speed(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_horse_armor, get_body_armor(items[i_item][6])))
    # elif type == itp_type_shield:
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_shield_size, get_weapon_length(items[i_item][6])))
      # item_base_score.append((item_set_slot, i_item, dplmc_slot_item_shield_armor, get_body_armor(items[i_item][6])))
  # return item_base_score[:]
  # #### Autoloot improved by rubik end

##diplomacy end

####################################################################################################################
# scripts is a list of script records.
# Each script record contns the following two fields:
# 1) Script id: The prefix "script_" will be inserted when referencing scripts.
# 2) Operation block: This must be a valid operation block. See header_operations.py for reference.
####################################################################################################################


scripts = [
]
scripts.extend(music_scripts)
scripts.extend(formation_orders_scripts)
scripts.extend(siege_scripts)
scripts.extend(training_ground_scripts)
scripts.extend(multiplayer_scripts)
scripts.extend(economy_scripts)
scripts.extend(quest_scripts)
scripts.extend(morale_scripts)
scripts.extend(banners_scripts)
scripts.extend(arena_scripts)
scripts.extend(encounters_scripts)
scripts.extend(party_ai_scripts)
scripts.extend(centers_scripts)
scripts.extend(tavern_scripts)
scripts.extend(npcs_scripts)
scripts.extend(faction_ai_scripts)
scripts.extend(rebellion_scripts)
scripts.extend(engine_scripts)
scripts.extend(diplomacy_scripts)
scripts.extend(dickplomacy_scripts)
scripts.extend(player_scripts)
scripts.extend(ui_scripts)
scripts.extend(tactics_scripts)
scripts.extend(quest_scripts)
scripts.extend(courtship_scripts)
scripts.extend(feast_scripts)
scripts.extend(item_modifiers_scripts)
scripts.extend(inventory_scripts)
scripts.extend(weapon_toggle_scripts)


# modmerger_start version=201 type=2
try:
    component_name = "scripts"
    var_set = { "scripts" : scripts }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
