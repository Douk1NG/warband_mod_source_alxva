# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

reports_economy_menu = [
("reports_economy",mnf_enable_hot_keys,
   "Select a report:",
   "none",
   [],
    [
      ("view_weekly_budget_report",[],"View weekly budget report.",
       [
        (assign, "$g_apply_budget_report_to_gold", 0),
        (start_presentation, "prsnt_budget_report"),
        ]
       ),
      ("view_bank_report",[],"View Financial Report",
       [(start_presentation, "prsnt_bank_quickview"),]),
      ("dplmc_show_economic_report",[],"View prosperity report.",
        [
         (jump_to_menu, "mnu_dplmc_economic_report"),
         ]
        ),
      ("view_spawn_diagnostics",[],"View bandit/pirate population & respawn diagnostics.",
        [
          (start_presentation, "prsnt_spawn_diagnostics"),
        ]
        ),
      ("rtr_reports_economy",[],"Return.",
       [(jump_to_menu, "mnu_reports"),
        ]
       ),
      ]
  )
]
