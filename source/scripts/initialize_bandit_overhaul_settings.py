# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *

initialize_bandit_overhaul_settings_scripts = [
  ("initialize_bandit_overhaul_settings", [
    # The old default of 10 meant 1% per level. Move that default to the new
    # requested 0.5%; non-default user values already map to the same rate.
    (try_begin),
      (neq, "$g_bo_growth_scale_migrated", 1),
      (try_begin),
        (eq, "$g_bandit_overhaul_settings_initialized", 1),
        (eq, "$g_bo_growth_per_10_levels", 10),
        (assign, "$g_bo_growth_per_10_levels", bandit_overhaul_default_growth_per_level_tenths),
      (try_end),
      (assign, "$g_bo_growth_scale_migrated", 1),
    (try_end),
    # Migrate the saved value from the misleading legacy global name.
    (try_begin),
      (neq, "$g_bo_party_growth_name_migrated", 1),
      (try_begin),
        (eq, "$g_bandit_overhaul_settings_initialized", 1),
        (assign, "$g_bo_party_growth_per_level_tenths", "$g_bo_growth_per_10_levels"),
      (try_end),
      (assign, "$g_bo_party_growth_name_migrated", 1),
    (try_end),
    # Keep the already-initialized path inside a conditional block. A bare
    # failed condition here aborts the caller's remaining script on the game
    # runtime, which prevented spawn_bandits/regeneration from continuing.
    (try_begin),
      (neq, "$g_bandit_overhaul_settings_initialized", 1),
    (assign, "$g_bo_party_growth_per_level_tenths", bandit_overhaul_default_growth_per_level_tenths),
    (assign, "$g_bo_land_size_lair_inactive", bandit_overhaul_default_land_size_lair_inactive),
    (assign, "$g_bo_land_parties_per_type", bandit_overhaul_default_land_parties_per_type),
    (assign, "$g_bo_land_respawn_hours", bandit_overhaul_default_land_respawn_hours),
    (assign, "$g_bo_land_respawn_amount", bandit_overhaul_default_land_respawn_amount),
    (assign, "$g_bo_ship_party_size", bandit_overhaul_default_ship_party_size),
    (assign, "$g_bo_ship_parties_per_type", bandit_overhaul_default_ship_parties_per_type),
    (assign, "$g_bo_ship_respawn_hours", bandit_overhaul_default_ship_respawn_hours),
    (assign, "$g_bo_ship_respawn_amount", bandit_overhaul_default_ship_respawn_amount),
    (assign, "$g_bo_looter_party_size", bandit_overhaul_default_looter_party_size),
    (assign, "$g_bo_looter_parties", bandit_overhaul_default_looter_parties),
    (assign, "$g_bo_looter_respawn_hours", bandit_overhaul_default_looter_respawn_hours),
    (assign, "$g_bo_looter_respawn_amount", bandit_overhaul_default_looter_respawn_amount),
    (assign, "$g_bo_manhunter_party_size", bandit_overhaul_default_manhunter_party_size),
    (assign, "$g_bo_manhunter_parties", bandit_overhaul_default_manhunter_parties),
    (assign, "$g_bo_manhunter_respawn_hours", bandit_overhaul_default_manhunter_respawn_hours),
    (assign, "$g_bo_manhunter_respawn_amount", bandit_overhaul_default_manhunter_respawn_amount),
    (assign, "$g_bo_deserter_party_size", bandit_overhaul_default_deserter_party_size),
    (assign, "$g_bo_deserter_parties", bandit_overhaul_default_deserter_parties),
    (assign, "$g_bo_deserter_respawn_hours", bandit_overhaul_default_deserter_respawn_hours),
    (assign, "$g_bo_deserter_respawn_amount", bandit_overhaul_default_deserter_respawn_amount),
    # Set the first configured spawn time when migrating old saves so the new
    # helper does not mistake an existing population for an unseeded world.
    (store_current_hours, ":current_hours"),
    (val_max, ":current_hours", 0),
    (store_add, ":next_spawn", ":current_hours", "$g_bo_land_respawn_hours"),
    (try_for_range, ":template", bandit_party_templates_begin, bandit_party_templates_end),
      (party_template_set_slot, ":template", slot_party_template_respawn_cooldown, ":next_spawn"),
    (try_end),
    (store_add, ":next_spawn", ":current_hours", "$g_bo_ship_respawn_hours"),
    (party_template_set_slot, "pt_sea_raiders_ship", slot_party_template_respawn_cooldown, ":next_spawn"),
    (party_template_set_slot, "pt_corsair_ship", slot_party_template_respawn_cooldown, ":next_spawn"),
    (party_template_set_slot, "pt_pirate_ship", slot_party_template_respawn_cooldown, ":next_spawn"),
    (store_add, ":next_spawn", ":current_hours", "$g_bo_looter_respawn_hours"),
    (party_template_set_slot, "pt_looters", slot_party_template_respawn_cooldown, ":next_spawn"),
    (store_add, ":next_spawn", ":current_hours", "$g_bo_manhunter_respawn_hours"),
    (party_template_set_slot, "pt_manhunters", slot_party_template_respawn_cooldown, ":next_spawn"),
    (store_add, ":next_spawn", ":current_hours", "$g_bo_deserter_respawn_hours"),
    (party_template_set_slot, "pt_deserters", slot_party_template_respawn_cooldown, ":next_spawn"),
    (assign, "$g_bandit_overhaul_settings_initialized", 1),
    (try_end),
  ]),
]
