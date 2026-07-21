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

initialize_economic_information_scripts = [
("initialize_economic_information",
    [
	    #All towns produce tools, pottery, and wool cloth for sale in countryside
	(try_for_range, ":town_no", towns_begin, towns_end),
		(store_random_in_range, ":random_average_20_variation_10", 10, 31), #10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29 or 30
		(party_set_slot, ":town_no", slot_center_wool_looms, ":random_average_20_variation_10"),

		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_breweries, ":random_average_2_variation_1"),

		(store_random_in_range, ":random_average_5_variation_3", 3, 9), #2,3,4,5,6,7 or 8
		(party_set_slot, ":town_no", slot_center_pottery_kilns, ":random_average_5_variation_3"),

		(store_random_in_range, ":random_average_15_variation_9", 6, 25), #6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23 or 24
		(party_set_slot, ":town_no", slot_center_smithies, ":random_average_15_variation_9"),

		(store_random_in_range, ":random_average_5_variation_3", 3, 9), #2,3,4,5,6,7 or 8
		(party_set_slot, ":town_no", slot_center_mills, ":random_average_5_variation_3"),

		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_tanneries, ":random_average_2_variation_1"),

		(store_random_in_range, ":random_average_1_variation_1", 0, 3), #0,1 or 2
		(party_set_slot, ":town_no", slot_center_wine_presses, ":random_average_1_variation_1"),

		(store_random_in_range, ":random_average_2_variation_1", 1, 4), #1,2 or 3
		(party_set_slot, ":town_no", slot_center_olive_presses, ":random_average_2_variation_1"),

		(store_random_in_range, ":random_average_1000_variation_1000", 0, 2001), #0..2000
		(party_set_slot, ":town_no", slot_center_acres_grain, ":random_average_1000_variation_1000"), #0..2000

		(store_random_in_range, ":random_average_1000_variation_1000", 0, 2001), #0..2000
		(party_set_slot, ":town_no", slot_center_acres_vineyard, ":random_average_1000_variation_1000"), #0..2000
    (try_end),

	#Sargoth (linen, wine)
	(party_set_slot, "p_town_1", slot_center_linen_looms, 15),
	(party_set_slot, "p_town_1", slot_center_wine_presses, 4),

	#Tihr (salt, smoked fish, linen)
	(party_set_slot, "p_town_2", slot_center_salt_pans, 3),
	(party_set_slot, "p_town_2", slot_center_fishing_fleet, 25),
	(party_set_slot, "p_town_2", slot_center_linen_looms, 15),

	#Veluca	(wine, velvet)
	(party_set_slot, "p_town_3", slot_center_wine_presses, 10),
	(party_set_slot, "p_town_3", slot_center_silk_looms, 12),

	#Suno (velvet, oil)
	(party_set_slot, "p_town_4", slot_center_silk_looms, 12),
	(party_set_slot, "p_town_4", slot_center_olive_presses, 15),

	#Jelkala (velvet, smoked fish)
	(party_set_slot, "p_town_5", slot_center_silk_looms, 24),
	(party_set_slot, "p_town_5", slot_center_fishing_fleet, 30),

	#Praven (ale, leatherwork, smoked fish)
	(party_set_slot, "p_town_6", slot_center_breweries, 10),
	(party_set_slot, "p_town_6", slot_center_tanneries, 4),
	(party_set_slot, "p_town_6", slot_center_fishing_fleet, 10),

	#Uxkhal (bread, leatherwork, oil)
	(party_set_slot, "p_town_7", slot_center_mills, 15),
	(party_set_slot, "p_town_7", slot_center_tanneries, 4),
	(party_set_slot, "p_town_7", slot_center_olive_presses, 5),

	#Reyvadin (tools, wool cloth, wine)
	(party_set_slot, "p_town_8", slot_center_smithies, 25),
	(party_set_slot, "p_town_8", slot_center_wool_looms, 35),
	(party_set_slot, "p_town_8", slot_center_wine_presses, 4),

	#Khudan (tools, leatherwork, smoked fish)
	(party_set_slot, "p_town_9", slot_center_smithies, 18),
	(party_set_slot, "p_town_9", slot_center_tanneries, 3),
	(party_set_slot, "p_town_9", slot_center_fishing_fleet, 5),

	#Tulga (salt, spice)
	(party_set_slot, "p_town_10", slot_center_salt_pans, 2),
	#also produces 100 spice

	#Curaw (tools, iron, smoked fish)
	(party_set_slot, "p_town_11", slot_center_smithies, 19),
	(party_set_slot, "p_town_11", slot_center_iron_deposits, 10),
	(party_set_slot, "p_town_11", slot_center_fishing_fleet, 10),

	#Wercheg (salt, smoked fish)
    (party_set_slot, "p_town_12", slot_center_salt_pans, 3),
	(party_set_slot, "p_town_12", slot_center_fishing_fleet, 25),

	#Rivacheg (wool cloth, leatherwork, smoked fish)
	(party_set_slot, "p_town_13", slot_center_wool_looms, 30),
	(party_set_slot, "p_town_13", slot_center_tanneries, 5),
	(party_set_slot, "p_town_13", slot_center_fishing_fleet, 20),

	#Halmar (leatherwork, pottery)
	(party_set_slot, "p_town_14", slot_center_tanneries, 3),
	(party_set_slot, "p_town_14", slot_center_pottery_kilns, 18),

	#Yalen (tools, wine, oil, smoked fish)
	(party_set_slot, "p_town_15", slot_center_smithies, 20),
	(party_set_slot, "p_town_15", slot_center_wine_presses, 6),
	(party_set_slot, "p_town_15", slot_center_olive_presses, 5),
	(party_set_slot, "p_town_15", slot_center_fishing_fleet, 25),

	#Dhirim (tools, leatherwork)
	(party_set_slot, "p_town_16", slot_center_smithies, 30),
	(party_set_slot, "p_town_16", slot_center_tanneries, 4),

	#Ichamur (wool cloth, spice)
	(party_set_slot, "p_town_17", slot_center_wool_looms, 40),
	#also produces 50 spice

	#Narra (wool cloth, oil)
	(party_set_slot, "p_town_18", slot_center_wool_looms, 35),
	(party_set_slot, "p_town_18", slot_center_olive_presses, 10),

	#Shariz (leatherwork, smoked fish, oil)
	(party_set_slot, "p_town_19", slot_center_tanneries, 5),
	(party_set_slot, "p_town_19", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_19", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_19", slot_center_fishing_fleet, 5),
	(party_set_slot, "p_town_19", slot_center_olive_presses, 5),
	#also produces 50 spice

	#Darquba (linen, pottery, oil)
	(party_set_slot, "p_town_20", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_20", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_20", slot_center_linen_looms, 15),
	(party_set_slot, "p_town_20", slot_center_pottery_kilns, 12),
	(party_set_slot, "p_town_19", slot_center_olive_presses, 3),

	#Ahmerrad (pottery, salt)
	(party_set_slot, "p_town_21", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_21", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_21", slot_center_pottery_kilns, 24),
	(party_set_slot, "p_town_21", slot_center_salt_pans, 1),

	#Bariyye (salt, pottery, spice)
	(party_set_slot, "p_town_22", slot_center_breweries, 0), 	    #no alcohol (ale) in arabic region
	(party_set_slot, "p_town_22", slot_center_wine_presses, 0), 	#no alcohol (wine) in arabic region
	(party_set_slot, "p_town_22", slot_center_pottery_kilns, 12),
	(party_set_slot, "p_town_22", slot_center_salt_pans, 2),


  #Zendar (iron, leatherwork, tools )
  (party_set_slot, "p_town_23", slot_center_smithies, 19),
	(party_set_slot, "p_town_23", slot_center_iron_deposits, 10),
	(party_set_slot, "p_town_23", slot_center_tanneries, 5),

	#also produces 50 spice

    (try_for_range, ":village_no", villages_begin, villages_end),
      (try_begin),
      ##diplomacy start+ Replace the explicit "is desert" list with a terrain check.
      ##This is less brittle to map changes.
            (ge, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW),#In Diplomacy this is true at the start of the module, but the player could re-initialize economic stats during the game with cheat codes, or derived mods could change the default.
            (party_get_current_terrain, ":village_is_at_desert", ":village_no"),#Will be changed to either 0 or 1
	    (this_or_next|eq, ":village_is_at_desert", rt_desert),
	    (eq, ":village_is_at_desert", rt_desert_forest),#If false, will fall through and be assigned to 0 below
	    (assign, ":village_is_at_desert", 1),
      (else_try),
	    (lt, "$g_dplmc_gold_changes", DPLMC_GOLD_CHANGES_LOW), #Fall back to old behavior
      ##diplomacy end+
	    (this_or_next|eq, ":village_no", "p_village_93"), #mazigh
		(this_or_next|eq, ":village_no", "p_village_94"), #sekhtem
		(this_or_next|eq, ":village_no", "p_village_95"), #qalyut
		(this_or_next|eq, ":village_no", "p_village_96"), #tilimsal
		(this_or_next|eq, ":village_no", "p_village_97"), #shibal zumr
		(this_or_next|eq, ":village_no", "p_village_102"), #tamnuh
		(this_or_next|eq, ":village_no", "p_village_109"), #habba
		(this_or_next|eq, ":village_no", "p_village_98"), #mawiti
		(this_or_next|eq, ":village_no", "p_village_103"), #mijayet
		(this_or_next|eq, ":village_no", "p_village_105"), #aab
		(this_or_next|eq, ":village_no", "p_village_99"), #fishara
		(this_or_next|eq, ":village_no", "p_village_100"), #iqbayl
		(this_or_next|eq, ":village_no", "p_village_107"), #unriya
		(this_or_next|eq, ":village_no", "p_village_101"), #uzgha
		(this_or_next|eq, ":village_no", "p_village_104"), #tazjunat
        (this_or_next|eq, ":village_no", "p_village_110"), #rushdigh
		(this_or_next|eq, ":village_no", "p_village_108"), #mit nun
		(eq, ":village_no", "p_village_92"), #dhibbain

		(assign, ":village_is_at_desert", 1),
	  (else_try),
		(assign, ":village_is_at_desert", 0),
	  (try_end),

      (store_random_in_range, ":random_cattle", 20, 100),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_cattle", 5),
	  (try_end),
      (party_set_slot, ":village_no", slot_center_head_cattle, ":random_cattle"), #average : 50, min : 25, max : 75

      (store_random_in_range, ":random_sheep", 40, 200),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_sheep", 5),
	  (try_end),
      (party_set_slot, ":village_no", slot_center_head_sheep, ":random_sheep"), #average : 100, min : 50, max : 150

	  #grain production
      (store_random_in_range, ":random_value_between_0_and_40000", 0, 40000),
	  (store_random_in_range, ":random_value_between_0_and_average_20000", 0, ":random_value_between_0_and_40000"),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_value_between_0_and_average_20000", 5),
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_acres_grain, ":random_value_between_0_and_average_20000"), #average : 10000, min : 0, max : 40000

      #grape production
	  (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_value_between_0_and_average_1000", 5),
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_acres_vineyard, ":random_value_between_0_and_average_1000"), #average : 500, min : 0, max : 2000

	  #olive production
      (store_random_in_range, ":random_value_between_0_and_2000", 0, 2000),
	  (store_random_in_range, ":random_value_between_0_and_average_1000", 0, ":random_value_between_0_and_2000"),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_div, ":random_value_between_0_and_average_1000", 5),
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_acres_olives, ":random_value_between_0_and_average_1000"), #average : 500, min : 0, max : 2000

	  #honey production
	  (store_random_in_range, ":random_value_between_0_and_3", 0, 3),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(assign, ":random_value_between_0_and_3", 0), #at desert regions no honey production
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_apiaries, ":random_value_between_0_and_3"),

	  #cabbage and fruit production
	  (store_random_in_range, ":random_value_between_0_and_5", 0, 5),
	  (try_begin),
	    (eq, ":village_is_at_desert", 1),
		(assign, ":random_value_between_0_and_5", 0), #at desert regions no cabbage and fruit production
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_household_gardens, ":random_value_between_0_and_5"),

	  #bread production
      (store_random_in_range, ":random_value_between_0_and_3", 0, 3),
	  (party_set_slot, ":village_no", slot_center_mills, ":random_value_between_0_and_3"),

	  #pottery production
	  (store_random_in_range, ":random_value_between_0_and_5", 0, 5),
		(try_begin),
	    (eq, ":village_is_at_desert", 1),
		(val_mul, ":random_value_between_0_and_5", 5), #at desert regions pottery production 4x more than normal (totally 5x)
	  (try_end),
	  (party_set_slot, ":village_no", slot_center_pottery_kilns, ":random_value_between_0_and_5"),

	  #Sargoth (village productions : Ambean, Fearichen and Fenada)
	  (try_begin),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_1"),
		(party_set_slot, ":village_no", slot_center_acres_flax, 4000),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),

	  #Tihr (village productions : Kulum, Haen and Aldelen)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_2"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),
		(party_set_slot, ":village_no", slot_center_household_gardens, 10),

	  #Veluca (village productions : Emer, Fedner, Chaeza and Sarimish)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_3"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 6000),
		(party_set_slot, ":village_no", slot_center_acres_olives, 6000),

	  #Suno (village productions : Ruluns and Lyindah)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_4"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
		(party_set_slot, ":village_no", slot_center_acres_olives, 8000),

	  #Jelkala (village productions : Buvran, Ruldi and Chelez)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_5"),
		(party_set_slot, ":village_no", slot_center_silk_farms, 1500),
		(party_set_slot, ":village_no", slot_center_kirmiz_farms, 1500),

	  #Praven (village productions : Azgad, Veidar, Elberl and Gisim)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_6"),
		(party_set_slot, ":village_no", slot_center_acres_flax, 4000),
		(party_set_slot, ":village_no", slot_center_breweries, 4),

	  #Uxkhal (village productions : Nomar, Ibiran and Tahlberl)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_7"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 1),
		(party_set_slot, ":village_no", slot_center_acres_olives, 8000),
		(party_set_slot, ":village_no", slot_center_apiaries, 8),

      #Reyvadin (village productions : Ulburban and Ayyike)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_8"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
			(party_set_slot, ":village_no", slot_center_head_cattle, 100),
		(party_set_slot, ":village_no", slot_center_iron_deposits, 6),

      #Khudan (village productions : Uslum, Shulus and Tismirr)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_9"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
		(party_set_slot, ":village_no", slot_center_acres_olives, 4000),

      #Tulga (village productions : Dusturil and Dashbigha)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_10"),
			(party_set_slot, ":village_no", slot_center_head_sheep, 150),
			(party_set_slot, ":village_no", slot_center_salt_pans, 1),
			(party_set_slot, ":village_no", slot_center_fur_traps, 1),
		(party_set_slot, ":village_no", slot_center_apiaries, 8),

      #Curaw (village productions : Bazeck and Rebache)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_11"),
		(party_set_slot, ":village_no", slot_center_iron_deposits, 6),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),

      #Wercheg (village productions : Ruvar and Odasan)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_12"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),
		(party_set_slot, ":village_no", slot_center_household_gardens, 10),
		(party_set_slot, ":village_no", slot_center_salt_pans, 1),

      #Rivacheg (village productions : Shapeshte, Vezin and Fisdnar)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_13"),
		(party_set_slot, ":village_no", slot_center_fur_traps, 2),
		(party_set_slot, ":village_no", slot_center_head_cattle, 100),
		(party_set_slot, ":village_no", slot_center_silk_farms, 1500),

      #Halmar (village productions : Peshmi)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_14"),
		(party_set_slot, ":village_no", slot_center_acres_grain, 40000),
		(party_set_slot, ":village_no", slot_center_mills, 5),

      #Yalen (village productions : Ilvia, Glunmar, Epeshe and Istiniar)
		(else_try),
	    (party_slot_eq, ":village_no", slot_village_market_town, "p_town_15"),
		(party_set_slot, ":village_no", slot_center_acres_vineyard, 8000),
		(party_set_slot, ":village_no", slot_center_acres_olives, 8000),
		(party_set_slot, ":village_no", slot_center_household_gardens, 10),

      #Dhirim (village productions : Burglen, Amere, Ushkuru, Tshibtin and Yalibe)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_16"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 40000),
        (party_set_slot, ":village_no", slot_center_iron_deposits, 3),
		(party_set_slot, ":village_no", slot_center_mills, 5),

      #Ichamur (village productions : Ada Kulun and Drigh Aban)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_17"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 20000),
			(party_set_slot, ":village_no", slot_center_fur_traps, 1),

      #Narra (village productions : Zagush and Kedelke)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_18"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 20000),
        (party_set_slot, ":village_no", slot_center_iron_deposits, 3),
		(party_set_slot, ":village_no", slot_center_apiaries, 8),
		(party_set_slot, ":village_no", slot_center_acres_flax, 4000),

      #Shariz (village productions : Ayn Assuadi, Dhibbain, Qalyut, Tilimsal and Rushdigh)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_19"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 6000), #low grain (partially desert)
			(party_set_slot, ":village_no", slot_center_acres_flax, 2000),
			(party_set_slot, ":village_no", slot_center_acres_olives, 3000),
        (party_set_slot, ":village_no", slot_center_acres_dates, 5000),

      #Durquba (village productions : Tamnuh and Sekhtem)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_20"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 3000), #low grain (heavy desert)
        (party_set_slot, ":village_no", slot_center_acres_dates, 10000),
			(party_set_slot, ":village_no", slot_center_salt_pans, 1),

      #Ahmerrad (village productions : Mawiti, Uzgha and Mijayet)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_21"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 3000), #low grain (heavy desert)
        (party_set_slot, ":village_no", slot_center_acres_dates, 5000),
		(party_set_slot, ":village_no", slot_center_kirmiz_farms, 1500),

      #Bariyye (village productions : Fishara and Iqbayl)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_22"),
        (party_set_slot, ":village_no", slot_center_acres_grain, 2000), #low grain (heavy desert)
			(party_set_slot, ":village_no", slot_center_acres_flax, 2000),
        (party_set_slot, ":village_no", slot_center_acres_dates, 10000),
        (party_set_slot, ":village_no", slot_center_salt_pans, 1),
        (party_set_slot, ":village_no", slot_center_kirmiz_farms, 1500),

      #Zendar (village productions : Hrafnvik and Vargdal)
		(else_try),
        (party_slot_eq, ":village_no", slot_village_market_town, "p_town_23"),
		    (party_set_slot, ":village_no", slot_center_acres_flax, 4000),
		    (party_set_slot, ":village_no", slot_center_fur_traps, 2),
        (party_set_slot, ":village_no", slot_center_iron_deposits, 3),
		(try_end),
    (try_end),

	#determining village productions which are bounded by castle by nearby village productions which are bounded by a town.
	(try_for_range, ":village_no", villages_begin, villages_end),
	  (party_get_slot, ":bound_center", ":village_no", slot_village_bound_center),
	  (is_between, ":bound_center", castles_begin, castles_end),

	  (try_for_range, ":cur_production_source", slot_production_sources_begin, slot_production_sources_end),

		(assign, ":total_averaged_production", 0),
		(try_for_range, ":effected_village_no", villages_begin, villages_end),
		  (party_get_slot, ":bound_center", ":effected_village_no", slot_village_bound_center),
	      (is_between, ":bound_center", towns_begin, towns_end),

		  (store_distance_to_party_from_party, ":dist", ":village_no", ":effected_village_no"),
		  (le, ":dist", 72),

		  (party_get_slot, ":production", ":village_no", ":cur_production_source"),

		  (store_add, ":dist_plus_24", ":dist", 24),
		  (store_mul, ":production_mul_12", ":production", 12),
		  (store_div, ":averaged_production", ":production_mul_12", ":dist_plus_24"), #if close (12/24=1/2) else (12/96=1/8)
		  (val_div, ":averaged_production", 2), #if close (1/4) else (1/16)
		  (val_add, ":total_averaged_production", ":averaged_production"),
		(try_end),

		(party_set_slot, ":village_no", ":cur_production_source", ":total_averaged_production"),
      (try_end),
	(try_end),

	#Ocean and river villages, new map
    (party_set_slot, "p_village_1", slot_center_fishing_fleet, 15), #Yaragar
    (party_set_slot, "p_village_3", slot_center_fishing_fleet, 15), #Azgad
    (party_set_slot, "p_village_5", slot_center_fishing_fleet, 15), #Kulum

    (party_set_slot, "p_village_8", slot_center_fishing_fleet, 15), #Haen
    (party_set_slot, "p_village_9", slot_center_fishing_fleet, 15), #Buvran

    (party_set_slot, "p_village_20", slot_center_fishing_fleet, 15), #Uslum
    (party_set_slot, "p_village_21", slot_center_fishing_fleet, 15), #Bazeck
    (party_set_slot, "p_village_23", slot_center_fishing_fleet, 15), #Ilvia
    (party_set_slot, "p_village_27", slot_center_fishing_fleet, 15), #Glunmar

    (party_set_slot, "p_village_30", slot_center_fishing_fleet, 20), #Ruvar
    (party_set_slot, "p_village_31", slot_center_fishing_fleet, 15), #Ambean
    (party_set_slot, "p_village_35", slot_center_fishing_fleet, 15), #Feacharin

    (party_set_slot, "p_village_47", slot_center_fishing_fleet, 15), #Epeshe
    (party_set_slot, "p_village_49", slot_center_fishing_fleet, 15), #Tismirr

    (party_set_slot, "p_village_51", slot_center_fishing_fleet, 15), #Jelbegi
    (party_set_slot, "p_village_56", slot_center_fishing_fleet, 15), #Fenada

    (party_set_slot, "p_village_66", slot_center_fishing_fleet, 15), #Fisdnar
    (party_set_slot, "p_village_68", slot_center_fishing_fleet, 15), #Ibdeles
    (party_set_slot, "p_village_69", slot_center_fishing_fleet, 15), #Kwynn

    (party_set_slot, "p_village_77", slot_center_fishing_fleet, 25), #Rizi - Estuary
    (party_set_slot, "p_village_79", slot_center_fishing_fleet, 15), #Istiniar

	(party_set_slot, "p_village_81", slot_center_fishing_fleet, 15), #Odasan
    (party_set_slot, "p_village_85", slot_center_fishing_fleet, 15), #Ismirala
    (party_set_slot, "p_village_87", slot_center_fishing_fleet, 15), #Udiniad

    (party_set_slot, "p_village_90", slot_center_fishing_fleet, 15), #Jamiche

	#Initialize pastureland
	(try_for_range, ":center", centers_begin, centers_end),
		(party_get_slot, ":head_cattle", ":center", slot_center_head_cattle),
		(party_get_slot, ":head_sheep", ":center", slot_center_head_sheep),
		(store_mul, ":num_acres", ":head_cattle", 4),
		(val_add, ":num_acres", ":head_sheep"),
		(val_add, ":num_acres", ":head_sheep"),
		(val_mul, ":num_acres", 6),
		(val_div, ":num_acres", 5),

		(store_random_in_range, ":random", 60, 150),
		(val_mul, ":num_acres", ":random"),
		(val_div, ":num_acres", 100),

		(party_set_slot, ":center", slot_center_acres_pasture, ":num_acres"),
	(try_end),

	#Initialize prices based on production, etc
    (try_for_range, ":unused", 0, 3), #15 cycles = 45 days. For a village with -20 production, this should lead to approximate +1000, modified
        (call_script, "script_update_trade_good_prices"), #changes prices based on production
    (try_end),

	#Initialize prosperity based on final prices
    (try_for_range, ":center_no", centers_begin, centers_end),
      (neg|is_between, ":center_no", castles_begin, castles_end),
      (store_random_in_range, ":random_prosperity_adder", -10, 10),
      (call_script, "script_get_center_ideal_prosperity", ":center_no"),
      (assign, ":prosperity", reg0),
      (val_add, ":prosperity", ":random_prosperity_adder"),
      (val_clamp, ":prosperity", 0, 100),
      (party_set_slot, ":center_no", slot_town_prosperity, ":prosperity"),
	(try_end),

	(call_script, "script_calculate_castle_prosperities_by_using_its_villages"),
    ])
]
