# Recruit Lords Increases Right to Rule

Recruiting lords now grants a Right to Rule bonus.

## source/module_dialogs.py
- Companion leaves party with fief: `script_change_player_right_to_rule(1)`
- Lord recruited through dialog: `script_change_player_right_to_rule(3)`
- Lord recruited via emissary: `script_change_player_right_to_rule(1)` (changed from 2)
- Lord recruited through the recruit-lord dialog: `script_change_player_right_to_rule(1)`
