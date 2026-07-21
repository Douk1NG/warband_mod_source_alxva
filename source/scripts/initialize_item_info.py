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

initialize_item_info_scripts = [
("initialize_item_info",
    [
	  # Setting food bonuses - these have been changed to incentivize using historical rations. Bread is the most cost-efficient
	  #Staples
      (item_set_slot, "itm_bread", slot_item_food_bonus, 8), #brought up from 4
      (item_set_slot, "itm_grain", slot_item_food_bonus, 2), #new - can be boiled as porridge

	  #Fat sources - preserved
      (item_set_slot, "itm_smoked_fish", slot_item_food_bonus, 4),
      (item_set_slot, "itm_dried_meat", slot_item_food_bonus, 5),
      (item_set_slot, "itm_cheese", slot_item_food_bonus, 5),
      (item_set_slot, "itm_sausages", slot_item_food_bonus, 5),
      (item_set_slot, "itm_butter", slot_item_food_bonus, 4), #brought down from 8

	  #Fat sources - perishable
      (item_set_slot, "itm_chicken", slot_item_food_bonus, 8), #brought up from 7
      (item_set_slot, "itm_cattle_meat", slot_item_food_bonus, 7), #brought down from 7
      (item_set_slot, "itm_pork", slot_item_food_bonus, 6), #brought down from 6

	  #Produce
      (item_set_slot, "itm_raw_olives", slot_item_food_bonus, 1),
      (item_set_slot, "itm_cabbages", slot_item_food_bonus, 2),
      (item_set_slot, "itm_raw_grapes", slot_item_food_bonus, 3),
      (item_set_slot, "itm_apples", slot_item_food_bonus, 4), #brought down from 5

	  #Sweet items
      (item_set_slot, "itm_raw_date_fruit", slot_item_food_bonus, 4), #brought down from 8
      (item_set_slot, "itm_honey", slot_item_food_bonus, 6), #brought down from 12

      (item_set_slot, "itm_wine", slot_item_food_bonus, 5),
      (item_set_slot, "itm_ale", slot_item_food_bonus, 4),

	  #Item economic settings
	  (item_set_slot, "itm_grain", slot_item_urban_demand, 20),
      (item_set_slot, "itm_grain", slot_item_rural_demand, 20),
      (item_set_slot, "itm_grain", slot_item_desert_demand, 20),
      (item_set_slot, "itm_grain", slot_item_production_slot, slot_center_acres_grain),
      (item_set_slot, "itm_grain", slot_item_production_string, "str_acres_grain"),
      (item_set_slot, "itm_grain", slot_item_base_price, 30),

      (item_set_slot, "itm_bread", slot_item_urban_demand, 30),
      (item_set_slot, "itm_bread", slot_item_rural_demand, 30),
      (item_set_slot, "itm_bread", slot_item_desert_demand, 30),
      (item_set_slot, "itm_bread", slot_item_production_slot, slot_center_mills),
      (item_set_slot, "itm_bread", slot_item_production_string, "str_mills"),
      (item_set_slot, "itm_bread", slot_item_primary_raw_material, "itm_grain"),
      (item_set_slot, "itm_bread", slot_item_input_number, 6),
      (item_set_slot, "itm_bread", slot_item_output_per_run, 6),
      (item_set_slot, "itm_bread", slot_item_overhead_per_run, 60),
      (item_set_slot, "itm_bread", slot_item_base_price, 50),
      (item_set_slot, "itm_bread", slot_item_enterprise_building_cost, 1500),

	  (item_set_slot, "itm_ale", slot_item_urban_demand, 10),
	  (item_set_slot, "itm_ale", slot_item_rural_demand, 15),
      (item_set_slot, "itm_ale", slot_item_desert_demand, 0),
      (item_set_slot, "itm_ale", slot_item_production_slot, slot_center_breweries),
      (item_set_slot, "itm_ale", slot_item_production_string, "str_breweries"),
      (item_set_slot, "itm_ale", slot_item_base_price, 120),
      (item_set_slot, "itm_ale", slot_item_primary_raw_material, "itm_grain"),
	  (item_set_slot, "itm_ale", slot_item_input_number, 1),
      (item_set_slot, "itm_ale", slot_item_output_per_run, 2),
      (item_set_slot, "itm_ale", slot_item_overhead_per_run, 110),
      (item_set_slot, "itm_ale", slot_item_base_price, 120),
      (item_set_slot, "itm_ale", slot_item_enterprise_building_cost, 2500),

	  (item_set_slot, "itm_wine", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_wine", slot_item_rural_demand, 10),
      (item_set_slot, "itm_wine", slot_item_desert_demand, 25),
      (item_set_slot, "itm_wine", slot_item_production_slot, slot_center_wine_presses),
      (item_set_slot, "itm_wine", slot_item_production_string, "str_presses"),
      (item_set_slot, "itm_wine", slot_item_primary_raw_material, "itm_raw_grapes"),
      (item_set_slot, "itm_wine", slot_item_input_number, 3),
      (item_set_slot, "itm_wine", slot_item_output_per_run, 2),
	  (item_set_slot, "itm_wine", slot_item_overhead_per_run, 15),
      (item_set_slot, "itm_wine", slot_item_base_price, 220),
      (item_set_slot, "itm_wine", slot_item_enterprise_building_cost, 5000),

	  (item_set_slot, "itm_raw_grapes", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_grapes", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_grapes", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_grapes", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_raw_grapes", slot_item_production_string, "str_acres_orchard"),
      (item_set_slot, "itm_raw_grapes", slot_item_is_raw_material_only_for, "itm_wine"),
      (item_set_slot, "itm_raw_grapes", slot_item_base_price, 75),

	  (item_set_slot, "itm_apples", slot_item_urban_demand, 4),
	  (item_set_slot, "itm_apples", slot_item_rural_demand, 4),
	  (item_set_slot, "itm_apples", slot_item_desert_demand, 0),
      (item_set_slot, "itm_apples", slot_item_production_slot, slot_center_acres_vineyard),
      (item_set_slot, "itm_apples", slot_item_production_string, "str_acres_orchard"),
      (item_set_slot, "itm_apples", slot_item_base_price, 44),

      (item_set_slot, "itm_smoked_fish", slot_item_urban_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_rural_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_desert_demand, 16),
      (item_set_slot, "itm_smoked_fish", slot_item_production_slot, slot_center_fishing_fleet),
      (item_set_slot, "itm_smoked_fish", slot_item_production_string, "str_boats"),

      (item_set_slot, "itm_salt", slot_item_urban_demand, 5),
      (item_set_slot, "itm_salt", slot_item_rural_demand, 3),
      (item_set_slot, "itm_salt", slot_item_desert_demand, -1),
      (item_set_slot, "itm_salt", slot_item_production_slot, slot_center_salt_pans),
      (item_set_slot, "itm_salt", slot_item_production_string, "str_pans"),

      (item_set_slot, "itm_dried_meat", slot_item_urban_demand, 20),
      (item_set_slot, "itm_dried_meat", slot_item_rural_demand, 5),
      (item_set_slot, "itm_dried_meat", slot_item_desert_demand, -1),
      (item_set_slot, "itm_dried_meat", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_dried_meat", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_cattle_meat", slot_item_urban_demand, 12),
      (item_set_slot, "itm_cattle_meat", slot_item_rural_demand, 3),
      (item_set_slot, "itm_cattle_meat", slot_item_desert_demand, -1),
      (item_set_slot, "itm_cattle_meat", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_cattle_meat", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_cheese", slot_item_urban_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_rural_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_desert_demand, 10),
      (item_set_slot, "itm_cheese", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_cheese", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_butter", slot_item_urban_demand, 2),
      (item_set_slot, "itm_butter", slot_item_rural_demand, 2),
      (item_set_slot, "itm_butter", slot_item_desert_demand, 2),
      (item_set_slot, "itm_butter", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_butter", slot_item_production_string, "str_head_cattle"),

      (item_set_slot, "itm_leatherwork", slot_item_urban_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_rural_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_desert_demand, 10),
      (item_set_slot, "itm_leatherwork", slot_item_production_slot, slot_center_tanneries),
      (item_set_slot, "itm_leatherwork", slot_item_production_string, "str_tanneries"),
      (item_set_slot, "itm_leatherwork", slot_item_primary_raw_material, "itm_raw_leather"),
      (item_set_slot, "itm_leatherwork", slot_item_input_number, 2),
      (item_set_slot, "itm_leatherwork", slot_item_output_per_run, 3),
      (item_set_slot, "itm_leatherwork", slot_item_overhead_per_run, 100),
	  (item_set_slot, "itm_leatherwork", slot_item_base_price, 220),
	  (item_set_slot, "itm_leatherwork", slot_item_enterprise_building_cost, 8000),

      (item_set_slot, "itm_raw_leather", slot_item_urban_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_leather", slot_item_production_slot, slot_center_head_cattle),
      (item_set_slot, "itm_raw_leather", slot_item_production_string, "str_head_cattle"),
      (item_set_slot, "itm_raw_leather", slot_item_is_raw_material_only_for, "itm_leatherwork"),
	  (item_set_slot, "itm_raw_leather", slot_item_base_price, 120),

  	  (item_set_slot, "itm_sausages", slot_item_urban_demand, 12),
	  (item_set_slot, "itm_sausages", slot_item_rural_demand, 3),
	  (item_set_slot, "itm_sausages", slot_item_desert_demand, -1),
      (item_set_slot, "itm_sausages", slot_item_production_slot, slot_center_head_sheep),
      (item_set_slot, "itm_sausages", slot_item_production_string, "str_head_sheep"),

	  (item_set_slot, "itm_wool", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_wool", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_wool", slot_item_desert_demand, 0),
      (item_set_slot, "itm_wool", slot_item_production_slot, slot_center_head_sheep),
      (item_set_slot, "itm_wool", slot_item_production_string, "str_head_sheep"),
	  (item_set_slot, "itm_wool", slot_item_is_raw_material_only_for, "itm_wool_cloth"),
	  (item_set_slot, "itm_wool", slot_item_base_price,130),

	  (item_set_slot, "itm_wool_cloth", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_wool_cloth", slot_item_rural_demand, 20),
	  (item_set_slot, "itm_wool_cloth", slot_item_desert_demand, 5),
      (item_set_slot, "itm_wool_cloth", slot_item_production_slot, slot_center_wool_looms),
      (item_set_slot, "itm_wool_cloth", slot_item_production_string, "str_looms"),
	  (item_set_slot, "itm_wool_cloth", slot_item_primary_raw_material, "itm_wool"),
      (item_set_slot, "itm_wool_cloth", slot_item_input_number, 2),
      (item_set_slot, "itm_wool_cloth", slot_item_output_per_run, 2),
	  (item_set_slot, "itm_wool_cloth", slot_item_overhead_per_run, 0),
	  (item_set_slot, "itm_wool_cloth", slot_item_base_price, 250),
	  (item_set_slot, "itm_wool_cloth", slot_item_enterprise_building_cost, 6000),

	  (item_set_slot, "itm_raw_flax", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_flax", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_flax", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_flax", slot_item_production_slot, slot_center_acres_flax),
      (item_set_slot, "itm_raw_flax", slot_item_production_string, "str_acres_flax"),
      (item_set_slot, "itm_raw_flax", slot_item_is_raw_material_only_for, "itm_linen"),
	  (item_set_slot, "itm_raw_flax", slot_item_base_price, 150),

	  (item_set_slot, "itm_linen", slot_item_urban_demand, 7),
	  (item_set_slot, "itm_linen", slot_item_rural_demand, 3),
	  (item_set_slot, "itm_linen", slot_item_desert_demand, 15),
      (item_set_slot, "itm_linen", slot_item_production_slot, slot_center_linen_looms),
      (item_set_slot, "itm_linen", slot_item_production_string, "str_looms"),
      (item_set_slot, "itm_linen", slot_item_primary_raw_material, "itm_raw_flax"),
      (item_set_slot, "itm_linen", slot_item_input_number, 1),
      (item_set_slot, "itm_linen", slot_item_output_per_run, 2),
      (item_set_slot, "itm_linen", slot_item_overhead_per_run, 110),
	  (item_set_slot, "itm_linen", slot_item_base_price, 250),
	  (item_set_slot, "itm_linen", slot_item_enterprise_building_cost, 6000),

	  (item_set_slot, "itm_iron", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_iron", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_iron", slot_item_desert_demand, 0),
      (item_set_slot, "itm_iron", slot_item_production_slot, slot_center_iron_deposits),
      (item_set_slot, "itm_iron", slot_item_production_string, "str_deposits"),
      (item_set_slot, "itm_iron", slot_item_is_raw_material_only_for, "itm_tools"),
	  (item_set_slot, "itm_iron", slot_item_base_price, 264),

	  (item_set_slot, "itm_tools", slot_item_urban_demand, 7),
	  (item_set_slot, "itm_tools", slot_item_rural_demand, 7),
	  (item_set_slot, "itm_tools", slot_item_desert_demand, 7),
      (item_set_slot, "itm_tools", slot_item_production_slot, slot_center_smithies),
      (item_set_slot, "itm_tools", slot_item_production_string, "str_smithies"),
      (item_set_slot, "itm_tools", slot_item_primary_raw_material, "itm_iron"),
      (item_set_slot, "itm_tools", slot_item_input_number, 2),
      (item_set_slot, "itm_tools", slot_item_output_per_run, 2),
      (item_set_slot, "itm_tools", slot_item_overhead_per_run, 152),
	  (item_set_slot, "itm_tools", slot_item_base_price, 410),
	  (item_set_slot, "itm_tools", slot_item_enterprise_building_cost, 3500),

	  (item_set_slot, "itm_pottery", slot_item_urban_demand, 15),
	  (item_set_slot, "itm_pottery", slot_item_rural_demand, 5),
	  (item_set_slot, "itm_pottery", slot_item_desert_demand, -1),
      (item_set_slot, "itm_pottery", slot_item_production_slot, slot_center_pottery_kilns),
      (item_set_slot, "itm_pottery", slot_item_production_string, "str_kilns"),

	  (item_set_slot, "itm_oil", slot_item_urban_demand, 10),
	  (item_set_slot, "itm_oil", slot_item_rural_demand, 5),
	  (item_set_slot, "itm_oil", slot_item_desert_demand, -1),
      (item_set_slot, "itm_oil", slot_item_production_slot, slot_center_olive_presses),
      (item_set_slot, "itm_oil", slot_item_production_string, "str_presses"),
      (item_set_slot, "itm_oil", slot_item_primary_raw_material, "itm_raw_olives"),
      (item_set_slot, "itm_oil", slot_item_input_number, 6),
      (item_set_slot, "itm_oil", slot_item_output_per_run, 2),
      (item_set_slot, "itm_oil", slot_item_overhead_per_run, 120),
	  (item_set_slot, "itm_oil", slot_item_base_price, 450),
	  (item_set_slot, "itm_oil", slot_item_enterprise_building_cost, 4500),

	  (item_set_slot, "itm_raw_olives", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_olives", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_olives", slot_item_desert_demand, 0),
      (item_set_slot, "itm_raw_olives", slot_item_production_slot, slot_center_acres_olives),
      (item_set_slot, "itm_raw_olives", slot_item_production_string, "str_olive_groves"),
      (item_set_slot, "itm_raw_olives", slot_item_is_raw_material_only_for, "itm_oil"),
	  (item_set_slot, "itm_raw_olives", slot_item_base_price, 100),

	  (item_set_slot, "itm_velvet", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_velvet", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_velvet", slot_item_desert_demand, -1),
      (item_set_slot, "itm_velvet", slot_item_production_slot, slot_center_silk_looms),
      (item_set_slot, "itm_velvet", slot_item_production_string, "str_looms"),
	  (item_set_slot, "itm_velvet", slot_item_primary_raw_material, "itm_raw_silk"),
      (item_set_slot, "itm_velvet", slot_item_input_number, 1),
      (item_set_slot, "itm_velvet", slot_item_output_per_run, 2),
      (item_set_slot, "itm_velvet", slot_item_overhead_per_run, 850),
	  (item_set_slot, "itm_velvet", slot_item_base_price, 1025),
	  (item_set_slot, "itm_velvet", slot_item_secondary_raw_material, "itm_raw_dyes"),
	  (item_set_slot, "itm_velvet", slot_item_enterprise_building_cost, 10000),

	  (item_set_slot, "itm_raw_silk", slot_item_urban_demand, 0),
	  (item_set_slot, "itm_raw_silk", slot_item_rural_demand, 0),
      (item_set_slot, "itm_raw_silk", slot_item_production_slot, slot_center_silk_farms),
      (item_set_slot, "itm_raw_silk", slot_item_production_string, "str_mulberry_groves"),
      (item_set_slot, "itm_raw_silk", slot_item_is_raw_material_only_for, "itm_velvet"),
      (item_set_slot, "itm_raw_silk", slot_item_base_price, 600),

	  (item_set_slot, "itm_raw_dyes", slot_item_urban_demand, 3),
	  (item_set_slot, "itm_raw_dyes", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_raw_dyes", slot_item_desert_demand, -1),
	  (item_set_slot, "itm_raw_dyes", slot_item_production_string, "str_caravans"),
	  (item_set_slot, "itm_raw_dyes", slot_item_base_price, 200),

	  (item_set_slot, "itm_spice", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_spice", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_spice", slot_item_desert_demand, 5),
	  (item_set_slot, "itm_spice", slot_item_production_string, "str_caravans"),

	  (item_set_slot, "itm_furs", slot_item_urban_demand, 5),
	  (item_set_slot, "itm_furs", slot_item_rural_demand, 0),
	  (item_set_slot, "itm_furs", slot_item_desert_demand, -1),
	  (item_set_slot, "itm_furs", slot_item_production_slot, slot_center_fur_traps),
	  (item_set_slot, "itm_furs", slot_item_production_string, "str_traps"),

      (item_set_slot, "itm_honey", slot_item_urban_demand, 12),
      (item_set_slot, "itm_honey", slot_item_rural_demand, 3),
      (item_set_slot, "itm_honey", slot_item_desert_demand, -1),
      (item_set_slot, "itm_honey", slot_item_production_slot, slot_center_apiaries),
      (item_set_slot, "itm_honey", slot_item_production_string, "str_hives"),

      (item_set_slot, "itm_cabbages", slot_item_urban_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_rural_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_desert_demand, 7),
      (item_set_slot, "itm_cabbages", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_cabbages", slot_item_production_string, "str_gardens"),

      (item_set_slot, "itm_raw_date_fruit", slot_item_urban_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_rural_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_desert_demand, 7),
      (item_set_slot, "itm_raw_date_fruit", slot_item_production_slot, slot_center_household_gardens),
      (item_set_slot, "itm_raw_date_fruit", slot_item_production_string, "str_acres_oasis"),

      (item_set_slot, "itm_chicken", slot_item_urban_demand, 40),
      (item_set_slot, "itm_chicken", slot_item_rural_demand, 10),
      (item_set_slot, "itm_chicken", slot_item_desert_demand, -1),

      (item_set_slot, "itm_pork", slot_item_urban_demand, 40),
      (item_set_slot, "itm_pork", slot_item_rural_demand, 10),
      (item_set_slot, "itm_pork", slot_item_desert_demand, -1),

      # Setting book intelligence requirements
      (item_set_slot, "itm_book_tactics", slot_item_intelligence_requirement, 9),
      (item_set_slot, "itm_book_persuasion", slot_item_intelligence_requirement, 8),
      (item_set_slot, "itm_book_leadership", slot_item_intelligence_requirement, 7),
      (item_set_slot, "itm_book_intelligence", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_trade", slot_item_intelligence_requirement, 11),
      (item_set_slot, "itm_book_weapon_mastery", slot_item_intelligence_requirement, 9),
      (item_set_slot, "itm_book_engineering", slot_item_intelligence_requirement, 12),

      (item_set_slot, "itm_book_wound_treatment_reference", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_training_reference", slot_item_intelligence_requirement, 10),
      (item_set_slot, "itm_book_surgery_reference", slot_item_intelligence_requirement, 10),
	 ])
]
