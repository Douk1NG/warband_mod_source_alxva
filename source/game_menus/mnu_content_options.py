# -*- coding: cp1254 -*-
from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

content_options_menu = [
("content_options",0,
   "Diplomacy Content Options",
   "none",
   [     (set_background_mesh, "mesh_pic_camp"), ],
    [
      ("camp_fuck_setting",[
        #(eq,0,1),
        (try_begin),
            (eq, "$g_sexual_content", 2),
            (str_store_string, s0, "@Consensual and non-consensual sex are enabled"),
        (else_try),
            (eq, "$g_sexual_content", 1),
            (str_store_string, s0, "@Consensual sex is enabled"),
        (else_try),
            (str_store_string, s0, "@Sexual content is disabled"),
        (try_end),
      ],"{s0}",
       [
       (try_begin),
            (ge, "$g_sexual_content", 2),
            (assign, "$g_sexual_content", 0),
       (else_try),
            (store_add, "$g_sexual_content", 1, "$g_sexual_content"),
       (try_end),
        ]
       ),

      ("camp_dark_hunters",[(assign, reg0, "$g_dark_hunters_enabled"),],"{reg0?Dis:En}able Dark Hunter's and Black Khergit Raider's spawning script",
       [
           (val_clamp, "$g_dark_hunters_enabled", 0, 2), #in case of other values
           (store_sub, "$g_dark_hunters_enabled", 1, "$g_dark_hunters_enabled"),
        ]
       ),
      ("camp_remove_dark_hunters",[(eq, "$g_dark_hunters_enabled", 0),],"Remove all Dark Hunters and Black Khergit Raider parties from the map",
       [
           (assign, ":removed", 0),
           (try_for_parties, ":party_no"),
                (party_get_template_id, ":ptid", ":party_no"),
                (this_or_next|eq, ":ptid", "pt_dark_hunters"),
                (eq, ":ptid", "pt_black_khergit_raiders"),
                (remove_party, ":party_no"),
                (val_add, ":removed", 1),
           (try_end),
           (assign, reg0, ":removed"),
           (display_message, "@{reg0} parties removed from the map."),
        ]
       ),
      ("camp_realistic_wounding",[(assign, reg0, "$g_realistic_wounding"),],"{reg0?Dis:En}able realistic casualties",
       [
           (val_clamp, "$g_realistic_wounding", 0, 2), #in case of other values
           (store_sub, "$g_realistic_wounding", 1, "$g_realistic_wounding"),
        ]
       ),
      ("camp_same_sex_on",[(neq, "$g_disable_condescending_comments", 2)],"Enable same sex marriage",
       [
           (assign,"$g_disable_condescending_comments", 2),
        ]
       ),
      ("camp_same_sex_off", [(neq, "$g_disable_condescending_comments", 0)],
        "Disable same sex marriage",
        [(assign, "$g_disable_condescending_comments", 0),
        ]
       ),
      ("camp_polygamy",[(assign, reg0, "$g_polygamy"),],"{reg0?Dis:En}able polygamy",
       [
           (val_clamp, "$g_polygamy", 0, 2), #in case of other values
           (store_sub, "$g_polygamy", 1, "$g_polygamy"),
        ]
       ),
      ("camp_nohomobro",[(assign, reg0, "$g_nohomo"),],"{reg0?Dis:En}able gay scenes",
       [
           (val_clamp, "$g_nohomo", 0, 2), #in case of other values
           (store_sub, "$g_nohomo", 1, "$g_nohomo"),
        ]
       ),
       ("back",[],"Back",
       [(jump_to_menu, "mnu_camp"),
        ]
       ),
      ]
  )
]
