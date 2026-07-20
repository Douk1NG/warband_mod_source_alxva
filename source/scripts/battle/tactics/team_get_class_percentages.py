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

team_get_class_percentages_scripts = [
("team_get_class_percentages",
    [
      (assign, ":num_infantry", 0),
      (assign, ":num_archers", 0),
      (assign, ":num_cavalry", 0),
      (assign, ":num_total", 0),
      (store_script_param, ":team_no", 1),
      (store_script_param, ":negate", 2),
      (try_for_agents,":cur_agent"),
        (agent_is_alive, ":cur_agent"),
        (agent_is_human, ":cur_agent"),
        (agent_get_team, ":agent_team", ":cur_agent"),
        (assign, ":continue", 0),
        (try_begin),
          (eq, ":negate", 1),
          (teams_are_enemies, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (else_try),
          (eq, ":agent_team", ":team_no"),
          (assign, ":continue", 1),
        (try_end),
        (eq, ":continue", 1),
        (val_add, ":num_total", 1),
        (agent_get_class, ":agent_class", ":cur_agent"),
        (try_begin),
          (eq, ":agent_class", grc_infantry),
          (val_add,  ":num_infantry", 1),
        (else_try),
          (eq, ":agent_class", grc_archers),
          (val_add,  ":num_archers", 1),
        (else_try),
          (eq, ":agent_class", grc_cavalry),
          (val_add,  ":num_cavalry", 1),
        (try_end),
      (try_end),
      (try_begin),
        (eq,  ":num_total", 0),
        (assign,  ":num_total", 1),
      (try_end),
      (store_mul, ":perc_infantry",":num_infantry",100),
      (val_div, ":perc_infantry",":num_total"),
      (store_mul, ":perc_archers",":num_archers",100),
      (val_div, ":perc_archers",":num_total"),
      (store_mul, ":perc_cavalry",":num_cavalry",100),
      (val_div, ":perc_cavalry",":num_total"),
      (assign, reg0, ":perc_infantry"),
      (assign, reg1, ":perc_archers"),
      (assign, reg2, ":perc_cavalry"),
  ])
]
