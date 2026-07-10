set -e
cd "$(dirname "$0")"
export PYTHONPATH="$(pwd)"
python process/process_init.py
python process/process_global_variables.py
python process/process_strings.py
python process/process_skills.py
python process/process_music.py
python process/process_animations.py
python process/process_meshes.py
python process/process_sounds.py
python process/process_skins.py
python process/process_map_icons.py
python process/process_factions.py
python process/process_items.py
python process/process_scenes.py
python process/process_troops.py
python process/process_particle_sys.py
python process/process_scene_props.py
python process/process_tableau_materials.py
python process/process_presentations.py
python process/process_party_tmps.py
python process/process_parties.py
python process/process_quests.py
python process/process_info_pages.py
python process/process_scripts.py
python process/process_mission_tmps.py
python process/process_game_menus.py
python process/process_simple_triggers.py
python process/process_dialogs.py
python process/process_global_variables_unused.py
python process/process_postfx.py
rm -f *.pyc
echo
echo ______________________________
echo
echo Script processing has ended.
