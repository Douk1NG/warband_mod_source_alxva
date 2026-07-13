@echo off
cd /d %~dp0..\source
set PYTHONPATH=%CD%;%~dp0
call python process\process_init.py
call python process\process_global_variables.py
call python process\process_strings.py
call python process\process_skills.py
call python process\process_music.py
call python process\process_animations.py
call python process\process_meshes.py
call python process\process_sounds.py
call python process\process_skins.py
call python process\process_map_icons.py
call python process\process_factions.py
call python process\process_items.py
call python process\process_scenes.py
call python process\process_troops.py
call python process\process_particle_sys.py
call python process\process_scene_props.py
call python process\process_tableau_materials.py
call python process\process_presentations.py
call python process\process_party_tmps.py
call python process\process_parties.py
call python process\process_quests.py
call python process\process_info_pages.py
call python process\process_scripts.py
call python process\process_mission_tmps.py
call python process\process_game_menus.py
call python process\process_simple_triggers.py
call python process\process_dialogs.py
call python process\process_global_variables_unused.py
call python process\process_postfx.py
@del /s /q *.pyc 2>nul
@echo.
@echo ______________________________
@echo.
@echo Script processing has ended.
@echo Press any key to exit. . .
pause > nul
