# Auto-Upgrade Skips Wounded Troops

Wounded troops are excluded from auto-upgrade because `party_stack_get_num_upgradeable` treats them as not ready to upgrade. A debug option "DEBUG: Run auto-upgrade" is available in the camp menu for testing. Needs fix.
