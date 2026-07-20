# -*- coding: cp1254 -*-
# Game menus package initializer (granular split)

from game_menus.battle import battle_menus
from game_menus.camp import camp_menus
from game_menus.captivity import captivity_menus
from game_menus.castle import castle_menus
from game_menus.center_management import center_management_menus
from game_menus.character_creation import character_creation_menus
from game_menus.cheats import cheats_menus
from game_menus.court import court_menus
from game_menus.custom_battle import custom_battle_menus
from game_menus.diplomacy import diplomacy_menus
from game_menus.dickplomacy import dickplomacy_menus
from game_menus.kingdom_management import kingdom_management_menus
from game_menus.notifications import notifications_menus
from game_menus.reports import reports_menus
from game_menus.scenes import scenes_menus
from game_menus.siege import siege_menus
from game_menus.town import town_menus
from game_menus.training import training_menus
from game_menus.village import village_menus
from game_menus.taxes import taxes_menus
from game_menus.tournament import tournament_menus

game_menus = []
game_menus.extend(battle_menus)
game_menus.extend(camp_menus)
game_menus.extend(captivity_menus)
game_menus.extend(castle_menus)
game_menus.extend(center_management_menus)
game_menus.extend(character_creation_menus)
game_menus.extend(cheats_menus)
game_menus.extend(court_menus)
game_menus.extend(custom_battle_menus)
game_menus.extend(diplomacy_menus)
game_menus.extend(dickplomacy_menus)
game_menus.extend(kingdom_management_menus)
game_menus.extend(notifications_menus)
game_menus.extend(reports_menus)
game_menus.extend(scenes_menus)
game_menus.extend(siege_menus)
game_menus.extend(town_menus)
game_menus.extend(training_menus)
game_menus.extend(village_menus)
game_menus.extend(taxes_menus)
game_menus.extend(tournament_menus)

