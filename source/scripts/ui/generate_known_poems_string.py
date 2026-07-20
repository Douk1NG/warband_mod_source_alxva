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

generate_known_poems_string_scripts = [
("generate_known_poems_string",
     [
        # Known poems string
        (assign, ":num_poems", 0),
        (str_store_string, s1, "str_s1__poems_known"),
        (try_begin),
            (gt, "$allegoric_poem_recitations", 0),
            (str_store_string, s1, "str_s1_storming_the_castle_of_love_allegoric"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$tragic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_kais_and_layali_tragic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$comic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_conversation_in_the_garden_comic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$heroic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_helgered_and_kara_epic"),
            (val_add, ":num_poems", 1),
        (try_end),
        (try_begin),
            (gt, "$mystic_poem_recitations", 0),
            (str_store_string, s1, "str_s1_a_hearts_desire_mystic"),
            (val_add, ":num_poems", 1),
        (try_end),

        # fill blank lines
        (try_for_range, ":num_poems", 5),
            (str_store_string, s1, "@{s1}^"),
        (try_end),
    ])
]
