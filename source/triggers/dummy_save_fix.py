# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from header_parties import *
from header_items import *
from header_skills import *
from header_triggers import *
from header_troops import *

from module_constants import *

from compiler import *

# Dummy trigger to restore save compatibility (38th trigger).
# Does nothing, fires once. Added to fix: "Number of triggers in file: 38, exceeds 37"
dummy_save_fix_triggers = [
  (0, 0, ti_once, [], []),
]
