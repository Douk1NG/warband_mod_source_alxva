# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

cheat_reports_menu = [
("cheat_reports",mnf_enable_hot_keys,
   "Select a cheat report:",
   "none",
   [],
    [
      ("cheat_faction_orders",[],"{!}Cheat: Faction orders.",
       [(jump_to_menu, "mnu_faction_orders"),
        ]
       ),

      ("status_check",[],"{!}NPC status check.",
       [
        (try_for_range, ":npc", companions_begin, companions_end),
            (main_party_has_troop, ":npc"),
            (str_store_troop_name, 4, ":npc"),
            (troop_get_slot, reg3, ":npc", slot_troop_morality_state),
            (troop_get_slot, reg4, ":npc", slot_troop_2ary_morality_state),
            (troop_get_slot, reg5, ":npc", slot_troop_personalityclash_state),
            (troop_get_slot, reg6, ":npc", slot_troop_personalityclash2_state),
            (troop_get_slot, reg7, ":npc", slot_troop_personalitymatch_state),
            (display_message, "@{!}{s4}: M{reg3}, 2M{reg4}, PC{reg5}, 2PC{reg6}, PM{reg7}"),
        (try_end),
        ]
       ),

      ("cheat_spawn_diagnostics",[],"{!}Bandit/pirate population & respawn diagnostics.",
       [(start_presentation, "prsnt_spawn_diagnostics"),
        ]
       ),

      ("rtr_cheat_reports",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
