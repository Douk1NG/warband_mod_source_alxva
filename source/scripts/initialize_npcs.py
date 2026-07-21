# -*- coding: cp1254 -*-
from header_common import *
from header_operations import *
from module_constants import *
from module_constants import *
from header_parties import *
from header_skills import *
from header_mission_templates import *
from header_items import *
from header_triggers import *
from header_terrain_types import *
from header_music import *
from header_map_icons import *
from ID_animations import *

initialize_npcs_scripts = [
#script_get_improvement_details
("initialize_npcs",
    [

# set strings

        (troop_set_slot, "trp_npc1", slot_troop_morality_type, tmt_egalitarian),  #borcha
        (troop_set_slot, "trp_npc1", slot_troop_morality_value, 4),  #borcha
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_type, tmt_aristocratic),  #borcha
        (troop_set_slot, "trp_npc1", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash_object, "trp_npc7"),  #borcha - deshavi
        (troop_set_slot, "trp_npc1", slot_troop_personalityclash2_object, "trp_npc16"),  #borcha - klethi
        (troop_set_slot, "trp_npc1", slot_troop_personalitymatch_object, "trp_npc2"),  #borcha - marnid
        (troop_set_slot, "trp_npc1", slot_troop_home, "p_village_25"), #Dashbiga
        (troop_set_slot, "trp_npc1", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc1", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc1", slot_troop_kingsupport_opponent, "trp_npc14"), #lezalit
		(troop_set_slot, "trp_npc1", slot_troop_town_with_contacts, "p_town_17"),
		(troop_set_slot, "trp_npc1", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc1", slot_lord_reputation_type, lrep_roguish), #



        (troop_set_slot, "trp_npc2", slot_troop_morality_type, tmt_humanitarian), #marnid
        (troop_set_slot, "trp_npc2", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc2", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash_object, "trp_npc5"), #marnid - beheshtur
        (troop_set_slot, "trp_npc2", slot_troop_personalityclash2_object, "trp_npc9"), #marnid - alayen
        (troop_set_slot, "trp_npc2", slot_troop_personalitymatch_object, "trp_npc1"),  #marnid - borcha
        (troop_set_slot, "trp_npc2", slot_troop_home, "p_town_1"), #Sargoth
        (troop_set_slot, "trp_npc2", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc2", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc2", slot_troop_kingsupport_opponent, "trp_npc16"), #klethi
		(troop_set_slot, "trp_npc2", slot_troop_town_with_contacts, "p_town_1"), #Sargoth
		(troop_set_slot, "trp_npc2", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc2", slot_lord_reputation_type, lrep_custodian), #

#
        (troop_set_slot, "trp_npc3", slot_troop_morality_type, tmt_humanitarian), #Ymira
        (troop_set_slot, "trp_npc3", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_type, tmt_aristocratic),
        (troop_set_slot, "trp_npc3", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash_object, "trp_npc14"), #Ymira - artimenner
        (troop_set_slot, "trp_npc3", slot_troop_personalityclash2_object, "trp_npc8"), #Ymira - matheld
        (troop_set_slot, "trp_npc3", slot_troop_personalitymatch_object, "trp_npc9"), #Ymira - alayen
        (troop_set_slot, "trp_npc3", slot_troop_home, "p_town_3"), #Veluca
        (troop_set_slot, "trp_npc3", slot_troop_payment_request, 0),
		(troop_set_slot, "trp_npc3", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc3", slot_troop_kingsupport_opponent, "trp_npc5"), #klethi
		(troop_set_slot, "trp_npc3", slot_troop_town_with_contacts, "p_town_15"), #yalen
		(troop_set_slot, "trp_npc3", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc3", slot_lord_reputation_type, lrep_benefactor), #



        (troop_set_slot, "trp_npc4", slot_troop_morality_type, tmt_aristocratic), #Rolf
        (troop_set_slot, "trp_npc4", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc4", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash_object, "trp_npc10"), #Rolf - bunduk
        (troop_set_slot, "trp_npc4", slot_troop_personalityclash2_object, "trp_npc7"), #Rolf - deshavi
        (troop_set_slot, "trp_npc4", slot_troop_personalitymatch_object, "trp_npc5"), #Rolf - beheshtur
        (troop_set_slot, "trp_npc4", slot_troop_home, "p_village_34"), #Ehlerdah
        (troop_set_slot, "trp_npc4", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc4", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc4", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc4", slot_troop_kingsupport_opponent, "trp_npc6"), #firentis
		(troop_set_slot, "trp_npc4", slot_troop_town_with_contacts, "p_town_3"), #veluca
		(troop_set_slot, "trp_npc4", slot_troop_original_faction, 0),
		(troop_set_slot, "trp_npc4", slot_lord_reputation_type, lrep_cunning), #


        (troop_set_slot, "trp_npc5", slot_troop_morality_type, tmt_egalitarian),  #beheshtur
        (troop_set_slot, "trp_npc5", slot_troop_morality_value, 3),  #beheshtur
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc5", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash_object, "trp_npc2"),  #beheshtur - marnid
        (troop_set_slot, "trp_npc5", slot_troop_personalityclash2_object, "trp_npc11"),  #beheshtur- katrin
        (troop_set_slot, "trp_npc5", slot_troop_personalitymatch_object, "trp_npc4"),  #beheshtur - rolf
        (troop_set_slot, "trp_npc5", slot_troop_home, "p_town_14"), #Halmar
        (troop_set_slot, "trp_npc5", slot_troop_payment_request, 400),
        (troop_set_slot, "trp_npc5", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc5", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc5", slot_troop_kingsupport_opponent, "trp_npc9"), #firentis
		(troop_set_slot, "trp_npc5", slot_troop_town_with_contacts, "p_town_10"), #tulga
		(troop_set_slot, "trp_npc5", slot_troop_original_faction, "fac_kingdom_3"), #khergit
		(troop_set_slot, "trp_npc5", slot_lord_reputation_type, lrep_cunning), #



        (troop_set_slot, "trp_npc6", slot_troop_morality_type, tmt_humanitarian), #firenz
        (troop_set_slot, "trp_npc6", slot_troop_morality_value, 2),  #beheshtur
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc6", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash_object, "trp_npc11"), #firenz
        (troop_set_slot, "trp_npc6", slot_troop_personalityclash2_object, "trp_npc13"), #firenz - nizar
        (troop_set_slot, "trp_npc6", slot_troop_personalitymatch_object, "trp_npc12"),  #firenz - jeremus
        (troop_set_slot, "trp_npc6", slot_troop_home, "p_town_4"), #Suno
        (troop_set_slot, "trp_npc6", slot_troop_payment_request, 0),
        (troop_set_slot, "trp_npc6", slot_troop_renown, 50), #SB : renown
		(troop_set_slot, "trp_npc6", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc6", slot_troop_kingsupport_opponent, "trp_npc8"), #firentis
		(troop_set_slot, "trp_npc6", slot_troop_town_with_contacts, "p_town_7"), #uxkhal
		(troop_set_slot, "trp_npc6", slot_troop_original_faction, "fac_kingdom_1"), #swadia
		(troop_set_slot, "trp_npc6", slot_lord_reputation_type, lrep_upstanding), #



        (troop_set_slot, "trp_npc7", slot_troop_morality_type, tmt_egalitarian),  #deshavi
        (troop_set_slot, "trp_npc7", slot_troop_morality_value, 3),  #beheshtur
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc7", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash_object, "trp_npc1"),  #deshavi
        (troop_set_slot, "trp_npc7", slot_troop_personalityclash2_object, "trp_npc4"),  #deshavi - rolf
        (troop_set_slot, "trp_npc7", slot_troop_personalitymatch_object, "trp_npc16"),  #deshavi - klethi
        (troop_set_slot, "trp_npc7", slot_troop_home, "p_village_5"), #Kulum
#        (troop_set_slot, "trp_npc7", slot_troop_payment_request, 300),
		(troop_set_slot, "trp_npc7", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc7", slot_troop_kingsupport_opponent, "trp_npc3"), #ymira
		(troop_set_slot, "trp_npc7", slot_troop_town_with_contacts, "p_town_2"), #tihr
		(troop_set_slot, "trp_npc7", slot_troop_original_faction, 0), #swadia
		(troop_set_slot, "trp_npc7", slot_lord_reputation_type, lrep_custodian), #



        (troop_set_slot, "trp_npc8", slot_troop_morality_type, tmt_aristocratic), #matheld
        (troop_set_slot, "trp_npc8", slot_troop_morality_value, 3),  #beheshtur
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc8", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash_object, "trp_npc12"), #matheld
        (troop_set_slot, "trp_npc8", slot_troop_personalityclash2_object, "trp_npc3"), #matheld - ymira
        (troop_set_slot, "trp_npc8", slot_troop_personalitymatch_object, "trp_npc13"),  #matheld - nizar
        (troop_set_slot, "trp_npc8", slot_troop_home, "p_village_35"), #Fearichen
        (troop_set_slot, "trp_npc8", slot_troop_payment_request, 500),
        (troop_set_slot, "trp_npc8", slot_troop_renown, 75), #SB : renown
		(troop_set_slot, "trp_npc8", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc8", slot_troop_kingsupport_opponent, "trp_npc2"), #marnid
		(troop_set_slot, "trp_npc8", slot_troop_town_with_contacts, "p_town_12"), #wercheg
		(troop_set_slot, "trp_npc8", slot_troop_original_faction, "fac_kingdom_4"), #nords
		(troop_set_slot, "trp_npc8", slot_lord_reputation_type, lrep_martial), #


        (troop_set_slot, "trp_npc9", slot_troop_morality_type, tmt_aristocratic), #alayen
        (troop_set_slot, "trp_npc9", slot_troop_morality_value, 2),  #beheshtur
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc9", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash_object, "trp_npc13"), #alayen vs nizar
        (troop_set_slot, "trp_npc9", slot_troop_personalityclash2_object, "trp_npc2"), #alayen vs marnid
        (troop_set_slot, "trp_npc9", slot_troop_personalitymatch_object, "trp_npc3"),  #alayen - ymira
        (troop_set_slot, "trp_npc9", slot_troop_home, "p_town_13"), #Rivacheg
        (troop_set_slot, "trp_npc9", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc9", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc9", slot_troop_kingsupport_argument, argument_lords),
		(troop_set_slot, "trp_npc9", slot_troop_kingsupport_opponent, "trp_npc1"), #borcha
		(troop_set_slot, "trp_npc9", slot_troop_town_with_contacts, "p_town_8"), #reyvadin
		(troop_set_slot, "trp_npc9", slot_troop_original_faction, "fac_kingdom_2"), #vaegirs
		(troop_set_slot, "trp_npc9", slot_lord_reputation_type, lrep_martial), #


        (troop_set_slot, "trp_npc10", slot_troop_morality_type, tmt_humanitarian), #bunduk
        (troop_set_slot, "trp_npc10", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc10", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash_object, "trp_npc4"), #bunduk vs rolf
        (troop_set_slot, "trp_npc10", slot_troop_personalityclash2_object, "trp_npc14"), #bunduk vs lazalet
        (troop_set_slot, "trp_npc10", slot_troop_personalitymatch_object, "trp_npc11"),  #bunduk likes katrin
        (troop_set_slot, "trp_npc10", slot_troop_home, "p_castle_28"), #Grunwalder Castle
        (troop_set_slot, "trp_npc10", slot_troop_payment_request, 200),
        (troop_set_slot, "trp_npc10", slot_troop_renown, 75), #SB : renown
		(troop_set_slot, "trp_npc10", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc10", slot_troop_kingsupport_opponent, "trp_npc7"), #nizar
		(troop_set_slot, "trp_npc10", slot_troop_town_with_contacts, "p_town_5"), #jelkala
		(troop_set_slot, "trp_npc10", slot_troop_original_faction, "fac_kingdom_5"), #rhodoks
		(troop_set_slot, "trp_npc10", slot_lord_reputation_type, lrep_benefactor), #



        (troop_set_slot, "trp_npc11", slot_troop_morality_type, tmt_egalitarian),  #katrin
        (troop_set_slot, "trp_npc11", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc11", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash_object, "trp_npc6"),  #katrin vs firenz
        (troop_set_slot, "trp_npc11", slot_troop_personalityclash2_object, "trp_npc5"),  #katrin - beheshtur
        (troop_set_slot, "trp_npc11", slot_troop_personalitymatch_object, "trp_npc10"),  #katrin likes bunduk
        (troop_set_slot, "trp_npc11", slot_troop_home, "p_town_6"), #Praven
        (troop_set_slot, "trp_npc11", slot_troop_payment_request, 100),
		(troop_set_slot, "trp_npc11", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc11", slot_troop_kingsupport_opponent, "trp_npc15"), #borcha
		(troop_set_slot, "trp_npc11", slot_troop_town_with_contacts, "p_town_6"), #praven
		(troop_set_slot, "trp_npc11", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc11", slot_lord_reputation_type, lrep_custodian), #


        (troop_set_slot, "trp_npc12", slot_troop_morality_type, tmt_humanitarian), #jeremus
        (troop_set_slot, "trp_npc12", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc12", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash_object, "trp_npc8"), #jerem
        (troop_set_slot, "trp_npc12", slot_troop_personalityclash2_object, "trp_npc15"), #jeremus - artimenner
        (troop_set_slot, "trp_npc12", slot_troop_personalitymatch_object, "trp_npc6"),  #jeremus - firenz
        (troop_set_slot, "trp_npc12", slot_troop_home, "p_castle_16"), #undetermined #University
        (troop_set_slot, "trp_npc12", slot_troop_payment_request, 0),
        (troop_set_slot, "trp_npc12", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc12", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc12", slot_troop_kingsupport_opponent, "trp_npc13"), #nizar
		(troop_set_slot, "trp_npc12", slot_troop_town_with_contacts, "p_town_14"), #halmar
		(troop_set_slot, "trp_npc12", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc12", slot_lord_reputation_type, lrep_benefactor), #



        (troop_set_slot, "trp_npc13", slot_troop_morality_type, tmt_aristocratic), #nizar
        (troop_set_slot, "trp_npc13", slot_troop_morality_value, 3),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_type, -1),
        (troop_set_slot, "trp_npc13", slot_troop_2ary_morality_value, 0),
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash_object, "trp_npc9"), #nizar
        (troop_set_slot, "trp_npc13", slot_troop_personalityclash2_object, "trp_npc6"), #nizar - firenz
        (troop_set_slot, "trp_npc13", slot_troop_personalitymatch_object, "trp_npc8"), #nizar - matheld
        (troop_set_slot, "trp_npc13", slot_troop_home, "p_castle_15"), #Ergellon Castle
        (troop_set_slot, "trp_npc13", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc13", slot_troop_renown, 75), #SB : renown
		(troop_set_slot, "trp_npc13", slot_troop_kingsupport_argument, argument_claim),
		(troop_set_slot, "trp_npc13", slot_troop_kingsupport_opponent, "trp_npc10"), #nizar
		(troop_set_slot, "trp_npc13", slot_troop_town_with_contacts, "p_town_4"), #suno
		(troop_set_slot, "trp_npc13", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc13", slot_lord_reputation_type, lrep_roguish), #



        (troop_set_slot, "trp_npc14", slot_troop_morality_type, tmt_aristocratic), #lezalit
        (troop_set_slot, "trp_npc14", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_type, tmt_egalitarian),
        (troop_set_slot, "trp_npc14", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash_object, "trp_npc3"), #lezalit
        (troop_set_slot, "trp_npc14", slot_troop_personalityclash2_object, "trp_npc10"), #lezalit - bunduk
        (troop_set_slot, "trp_npc14", slot_troop_personalitymatch_object, "trp_npc15"), #lezalit - artimenner
        (troop_set_slot, "trp_npc14", slot_troop_home, "p_castle_18"), #Ismirala Castle
        (troop_set_slot, "trp_npc14", slot_troop_payment_request, 400),
        (troop_set_slot, "trp_npc14", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc14", slot_troop_kingsupport_argument, argument_victory),
		(troop_set_slot, "trp_npc14", slot_troop_kingsupport_opponent, "trp_npc11"), #nizar
		(troop_set_slot, "trp_npc14", slot_troop_town_with_contacts, "p_town_16"), #dhirim
		(troop_set_slot, "trp_npc14", slot_troop_original_faction, 0), #
		(troop_set_slot, "trp_npc14", slot_lord_reputation_type, lrep_selfrighteous), #


        (troop_set_slot, "trp_npc15", slot_troop_morality_type, tmt_egalitarian),  #artimenner
        (troop_set_slot, "trp_npc15", slot_troop_morality_value, 2),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_type, tmt_honest),
        (troop_set_slot, "trp_npc15", slot_troop_2ary_morality_value, 1),
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash_object, "trp_npc16"), #artimenner - klethi
        (troop_set_slot, "trp_npc15", slot_troop_personalityclash2_object, "trp_npc12"), #artimenner - jeremus
        (troop_set_slot, "trp_npc15", slot_troop_personalitymatch_object, "trp_npc14"), #lazalit - artimenner
        (troop_set_slot, "trp_npc15", slot_troop_home, "p_castle_1"), #Culmarr Castle
        (troop_set_slot, "trp_npc15", slot_troop_payment_request, 300),
        (troop_set_slot, "trp_npc15", slot_troop_renown, 100), #SB : renown
		(troop_set_slot, "trp_npc15", slot_troop_kingsupport_argument, argument_ruler),
		(troop_set_slot, "trp_npc15", slot_troop_kingsupport_opponent, "trp_npc4"), #nizar
 		(troop_set_slot, "trp_npc15", slot_troop_town_with_contacts, "p_town_20"), #durquba
		(troop_set_slot, "trp_npc15", slot_lord_reputation_type, lrep_custodian), #


        (troop_set_slot, "trp_npc16", slot_troop_morality_type, tmt_aristocratic), #klethi
        (troop_set_slot, "trp_npc16", slot_troop_morality_value, 4),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_type, tmt_humanitarian),
        (troop_set_slot, "trp_npc16", slot_troop_2ary_morality_value, -1),
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash_object, "trp_npc15"), #klethi
        (troop_set_slot, "trp_npc16", slot_troop_personalityclash2_object, "trp_npc1"), #klethi - borcha
        (troop_set_slot, "trp_npc16", slot_troop_personalitymatch_object, "trp_npc7"),  #deshavi - klethi
        (troop_set_slot, "trp_npc16", slot_troop_home, "p_village_20"), #Uslum
        (troop_set_slot, "trp_npc16", slot_troop_payment_request, 200),
        (troop_set_slot, "trp_npc16", slot_troop_kingsupport_argument, argument_lords),
        (troop_set_slot, "trp_npc16", slot_troop_kingsupport_opponent, "trp_npc12"), #nizar
        (troop_set_slot, "trp_npc16", slot_troop_town_with_contacts, "p_town_9"), #khudan
        (troop_set_slot, "trp_npc16", slot_lord_reputation_type, lrep_roguish), #



        (store_sub, "$number_of_npc_slots", slot_troop_strings_end, slot_troop_intro),

        (try_for_range, ":npc", companions_begin, companions_end),


            (try_for_range, ":slot_addition", 0, "$number_of_npc_slots"),
                (store_add, ":slot", ":slot_addition", slot_troop_intro),

                (store_mul, ":string_addition", ":slot_addition", 16),
                (store_add, ":string", "str_npc1_intro", ":string_addition"),
                (val_add, ":string", ":npc"),
                (val_sub, ":string", companions_begin),

                (troop_set_slot, ":npc", ":slot", ":string"),
            (try_end),
        (try_end),


#Post 0907 changes begin
        (call_script, "script_add_log_entry", logent_game_start, "trp_player", -1, -1, -1),
#Post 0907 changes end

    #Rebellion changes begin
        (troop_set_slot, "trp_kingdom_1_pretender",  slot_troop_original_faction, "fac_kingdom_1"),
        (troop_set_slot, "trp_kingdom_2_pretender",  slot_troop_original_faction, "fac_kingdom_2"),
        (troop_set_slot, "trp_kingdom_3_pretender",  slot_troop_original_faction, "fac_kingdom_3"),
        (troop_set_slot, "trp_kingdom_4_pretender",  slot_troop_original_faction, "fac_kingdom_4"),
        (troop_set_slot, "trp_kingdom_5_pretender",  slot_troop_original_faction, "fac_kingdom_5"),
        (troop_set_slot, "trp_kingdom_6_pretender",  slot_troop_original_faction, "fac_kingdom_6"),

    #        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_support_base,     "p_town_4"), #suno
    #        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_support_base,     "p_town_11"), #curaw
    #        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_support_base,     "p_town_18"), #town_18
    #        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_support_base,     "p_town_12"), #wercheg
    #        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_support_base,     "p_town_3"), #veluca
        ##diplomacy start+
        (troop_set_slot, "trp_kingdom_1_pretender", slot_troop_home, "p_town_4"),#Lady Isolle - Suno
        (troop_set_slot, "trp_kingdom_2_pretender", slot_troop_home, "p_town_11"),#Prince Valdym - Curaw
        (troop_set_slot, "trp_kingdom_3_pretender", slot_troop_home, "p_town_18"),#Dustum Khan - Narra
        (troop_set_slot, "trp_kingdom_4_pretender", slot_troop_home, "p_town_12"),#Lethwin Far-Seeker - Wercheg
        (troop_set_slot, "trp_kingdom_5_pretender", slot_troop_home, "p_town_3"),#Lord Kastor - Veluca
        (troop_set_slot, "trp_kingdom_6_pretender", slot_troop_home, "p_town_20"),#Arwa the Pearled One - Durquba
        ##diplomacy end+
        (try_for_range, ":pretender", pretenders_begin, pretenders_end),
            (troop_set_slot, ":pretender", slot_lord_reputation_type, lrep_none),
            ##diplomacy start+
            (troop_get_slot, ":home", ":pretender", slot_troop_home),
            (ge, ":home", 1),
            (neg|party_slot_ge, ":home", dplmc_slot_center_original_lord, 1),
            (party_set_slot, ":home", dplmc_slot_center_original_lord, ":pretender"),
            ##diplomacy end+
        (try_end),
#Rebellion changes end
     ])
]
