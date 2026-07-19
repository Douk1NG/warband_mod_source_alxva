from header_game_menus import *
from header_parties import *
from header_items import *
from header_mission_templates import *
from header_music import *
from header_terrain_types import *
#SB : optional menu toggles
from header_triggers import key_left_shift, key_right_shift
from module_constants import *

from compiler import *
####################################################################################################################
#  (menu-id, menu-flags, menu_text, mesh-name, [<operations>], [<options>]),
#
#   Each game menu is a tuple that contains the following fields:
#
#  1) Game-menu id (string): used for referencing game-menus in other files.
#     The prefix menu_ is automatically added before each game-menu-id
#
#  2) Game-menu flags (int). See header_game_menus.py for a list of available flags.
#     You can also specify menu text color here, with the menu_text_color macro
#  3) Game-menu text (string).
#  4) mesh-name (string). Not currently used. Must be the string "none"
#  5) Operations block (list). A list of operations. See header_operations.py for reference.
#     The operations block is executed when the game menu is activated.
#  6) List of Menu options (List).
#     Each menu-option record is a tuple containing the following fields:
#   6.1) Menu-option-id (string) used for referencing game-menus in other files.
#        The prefix mno_ is automatically added before each menu-option.
#   6.2) Conditions block (list). This must be a valid operation block. See header_operations.py for reference.
#        The conditions are executed for each menu option to decide whether the option will be shown to the player or not.
#   6.3) Menu-option text (string).
#   6.4) Consequences block (list). This must be a valid operation block. See header_operations.py for reference.
#        The consequences are executed for the menu option that has been selected by the player.
#
#
# Note: The first Menu is the initial character creation menu.
####################################################################################################################


from game_menus import *

import header_scenes
from template_tools import *
from module_scenes import scenes

sorted_scenes = sorted(scenes)
for i in xrange(len(sorted_scenes)):
  current_scene = list(sorted_scenes[i])
  current_scene[1] = get_flags_from_bitmap(header_scenes, "sf_", current_scene[1])
  sorted_scenes[i] = tuple(current_scene)

choose_scene_template = Game_Menu_Template(
  id="choose_scenes_",
  text="Choose a scene: (Page {current_page} of {num_pages})",
  optn_id="choose_scene_",
  optn_text="{list_item[0]}{list_item[1]}",
  optn_consq = [
    (jump_to_scene, "scn_{list_item[0]}"),
    (change_screen_mission)
  ]
)

game_menus += choose_scene_template.generate_menus(sorted_scenes)
# modmerger_start version=201 type=2
try:
    component_name = "game_menus"
    var_set = { "game_menus" : game_menus }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
try:
    var_set = { "game_menus" : game_menus }
    from xgm_mod_options_game_menus import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end
