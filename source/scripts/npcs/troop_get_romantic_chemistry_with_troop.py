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

troop_get_romantic_chemistry_with_troop_scripts = [
("troop_get_romantic_chemistry_with_troop", #source is lady, target is man
    [
      ##diplomacy start+ (players of either gender may marry opposite-gender lords)
      #Note: the above is misleading even in Native, since when target_lord is the player,
      #target_lord can be female and source_lady can be male.
	  (assign, ":save_reg1", reg1),
      ##diplomacy end+
      (store_script_param, ":source_lady", 1),
      (store_script_param, ":target_lord", 2),

      (store_add, ":chemistry_sum", ":source_lady", ":target_lord"),
      (val_add, ":chemistry_sum", "$romantic_attraction_seed"),

      #This calculates (modula ^ 2) * 3
      (store_mod, ":chemistry_remainder", ":chemistry_sum", 5),
      (val_mul, ":chemistry_remainder", ":chemistry_remainder"), #0, 1, 4, 9, 16
      (val_mul, ":chemistry_remainder", 3), #0, 3, 12, 27, 48

      (store_attribute_level, ":romantic_chemistry", ":target_lord", ca_charisma),
      (val_sub, ":romantic_chemistry", ":chemistry_remainder"),

      (val_mul, ":romantic_chemistry", 2),
      ##diplomacy start+ ensure companion compatability
      (try_begin),
         (is_between, ":source_lady", companions_begin, companions_end),
         (troop_slot_eq, ":source_lady", slot_troop_personalitymatch_object, ":target_lord"),
         (val_max, ":romantic_chemistry", 15),
      (else_try),
         (is_between, ":target_lord", companions_begin, companions_end),
         (troop_slot_eq, ":target_lord", slot_troop_personalitymatch_object, ":source_lady"),
         (val_max, ":romantic_chemistry", 15),
	  #...and companion incompatibility.
	  (else_try),
  	     (is_between, ":source_lady", companions_begin, companions_end),
		 (this_or_next|troop_slot_eq, ":source_lady", slot_troop_personalityclash_object, ":target_lord"),
			(troop_slot_eq, ":source_lady", slot_troop_personalityclash2_object, ":target_lord"),
		 (val_min, ":romantic_chemistry", -15),
  	  (else_try),
  	     (is_between, ":target_lord", companions_begin, companions_end),
		 (this_or_next|troop_slot_eq, ":target_lord", slot_troop_personalityclash_object, ":source_lady"),
			(troop_slot_eq, ":target_lord", slot_troop_personalityclash2_object, ":source_lady"),
		(val_min, ":romantic_chemistry", -15),
	  #Prevent glitches.  This can be enabled explicitly if intentional.
      (else_try),
	     (call_script, "script_dplmc_store_is_female_troop_1_troop_2", ":source_lady", ":target_lord"),
         (eq, reg0, reg1),#different genders
         #(val_min, ":romantic_chemistry", -15), #dckplmc
      (try_end),
	  (assign, reg1, ":save_reg1"),
      ##diplomacy end+
      (assign, reg0, ":romantic_chemistry"),

      #examples :
      #For a charisma of 18, yields (18 - 0) * 2 = 36, (18 - 3) * 2 = 30, (18 - 12) * 2 = 12, (18 - 27) * 2 = -18, (18 - 48) * 2 = -60
      #For a charisma of 10, yields (10 - 0) * 2 = 20, (10 - 3) * 2 = 14, (10 - 12) * 2 = -4, (10 - 27) * 2 = -34, (10 - 48) * 2 = -76
      #For a charisma of 7, yields  (7 - 0) * 2 = 14,  (7 - 3) * 2 = 8,   (7 - 12) * 2 = -10, (7 - 27) * 2 = -40,  (7 - 48) * 2 = -82

      #15 is high attraction, 0 is moderate attraction, -76 is lowest attraction
	])
]
