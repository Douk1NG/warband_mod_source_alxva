# -*- coding: cp1254 -*-
from presentations import presentations

# modmerger_start version=201 type=2
try:
    component_name = "presentations"
    var_set = { "presentations" : presentations }
    from modmerger import modmerge
    modmerge(var_set)
except:
    raise
# modmerger_end

try:
    var_set = { "presentations" : presentations }
    from xgm_mod_options_presentations import modmerge
    modmerge(var_set)
except:
    raise
