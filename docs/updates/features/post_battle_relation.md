# Post-Battle Lord Relation

Allied lords who fought alongside the player receive a small relation boost after battle.

## source/module_game_menus.py, encounters_scripts.py
- Scans `p_collective_friends` for active NPC kingdom heroes present in the player-side battle group
- Default: +1 relation
- Martial lords (`lrep_martial`): +2
- Lords with relation below -5: 0 (no change)
- Triggered from: field battle victory, castle capture, siege success paths
