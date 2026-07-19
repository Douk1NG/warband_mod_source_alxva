# -*- coding: cp1254 -*-
# Game menus package initializer

from game_menus.character_creation import character_creation_menus
from game_menus.reports import reports_menus
from game_menus.kingdom_management import kingdom_management_menus
from game_menus.camp import camp_menus
from game_menus.misc import misc_menus
from game_menus.encounter import encounter_menus
from game_menus.join_battle import join_battle_menus
from game_menus.battle_results import battle_results_menus
from game_menus.locations import locations_menus
from game_menus.siege import siege_menus
from game_menus.castle import castle_menus
from game_menus.faction_battle import faction_battle_menus
from game_menus.village import village_menus
from game_menus.center_management import center_management_menus
from game_menus.misc_town import misc_town_menus
from game_menus.town import town_menus
from game_menus.tournament import tournament_menus
from game_menus.taxes_training import taxes_training_menus
from game_menus.sneak import sneak_menus
from game_menus.training import training_menus
from game_menus.captivity import captivity_menus
from game_menus.notifications import notifications_menus
from game_menus.dplmc import dplmc_menus

game_menus = []
game_menus.extend(character_creation_menus)
game_menus.extend(reports_menus)
game_menus.extend(kingdom_management_menus)
game_menus.extend(camp_menus)
game_menus.extend(misc_menus)
game_menus.extend(encounter_menus)
game_menus.extend(join_battle_menus)
game_menus.extend(battle_results_menus)
game_menus.extend(locations_menus)
game_menus.extend(siege_menus)
game_menus.extend(castle_menus)
game_menus.extend(faction_battle_menus)
game_menus.extend(village_menus)
game_menus.extend(center_management_menus)
game_menus.extend(misc_town_menus)
game_menus.extend(town_menus)
game_menus.extend(tournament_menus)
game_menus.extend(taxes_training_menus)
game_menus.extend(sneak_menus)
game_menus.extend(training_menus)
game_menus.extend(captivity_menus)
game_menus.extend(notifications_menus)
game_menus.extend(dplmc_menus)

