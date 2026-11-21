# Lord Recruitment Cheat

Forces any lord to accept recruitment into the player's kingdom without persuasion checks.

## source/module_dialogs.py
- New option under the lord suggestion cheat menu
- Requires player to be ruler of `$players_kingdom`
- Makes the target lord consider `trp_player` as the recruitment candidate
- Uses the claim argument, clears fief expectation flag, forces `$pledge_chance` to 100
- Reuses the normal final pledge flow (faction change + pledge consequences)
