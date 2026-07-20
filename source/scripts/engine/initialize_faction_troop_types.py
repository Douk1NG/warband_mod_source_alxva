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

initialize_faction_troop_types_scripts = [
#script_game_get_quest_note
("initialize_faction_troop_types",
    [

      (try_for_range, ":faction_no", kingdoms_begin, kingdoms_end),
        (faction_get_slot, ":culture", ":faction_no", slot_faction_culture),

        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_1_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_1_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_2_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_2_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_3_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_3_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_4_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_4_troop, ":troop"),
        (faction_get_slot, ":troop", ":culture",  slot_faction_tier_5_troop),
        (faction_set_slot, ":faction_no",  slot_faction_tier_5_troop, ":troop"),

        (try_begin),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_1"),

          (faction_set_slot, ":faction_no",  slot_faction_deserter_troop, "trp_swadian_deserter"),
          (faction_set_slot, ":faction_no",  slot_faction_guard_troop, "trp_swadian_sergeant"),
          (faction_set_slot, ":faction_no",  slot_faction_messenger_troop, "trp_swadian_messenger"),
          (faction_set_slot, ":faction_no",  slot_faction_prison_guard_troop, "trp_swadian_prison_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_castle_guard_troop, "trp_swadian_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_1_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_1_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_1_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_2"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_vaegir_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_vaegir_guard"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_vaegir_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_vaegir_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_vaegir_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_2_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_2_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_2_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_3"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_khergit_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_khergit_horseman"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_khergit_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_khergit_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_khergit_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_3_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_3_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_3_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_4"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_nord_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_nord_warrior"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_nord_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_nord_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_nord_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_4_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_4_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_4_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_5"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_rhodok_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_rhodok_veteran_spearman"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_rhodok_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_rhodok_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_rhodok_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_5_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_5_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_5_reinforcements_c"),
        (else_try),
          (faction_slot_eq, ":faction_no", slot_faction_culture, "fac_culture_6"),

          (faction_set_slot, ":faction_no", slot_faction_deserter_troop, "trp_sarranid_deserter"),
          (faction_set_slot, ":faction_no", slot_faction_guard_troop, "trp_sarranid_castle_guard"),
          (faction_set_slot, ":faction_no", slot_faction_messenger_troop, "trp_sarranid_messenger"),
          (faction_set_slot, ":faction_no", slot_faction_prison_guard_troop, "trp_sarranid_prison_guard"),
          (faction_set_slot, ":faction_no", slot_faction_castle_guard_troop, "trp_sarranid_castle_guard"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_a, "pt_kingdom_6_reinforcements_a"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_b, "pt_kingdom_6_reinforcements_b"),
          (faction_set_slot, ":faction_no",  slot_faction_reinforcements_c, "pt_kingdom_6_reinforcements_c"),
        (try_end),
      (try_end),
	])
]
