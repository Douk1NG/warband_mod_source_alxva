# -*- coding: cp1254 -*-
from header_common import *
from header_troops import *
from header_items import *
from header_skills import *
from ID_factions import *

from kingdom_custom_troop_tree_creator_constants import *

def build_preset_4_skin(skin_id, face_code_1, face_code_2):
	troop_list = []
	for node_index, (label, troop_level, _) in enumerate(PRESET_4_UNITS):
		troop_list.append([
			preset_4_troop_id(skin_id, node_index),
			"Unit %s" % (label),
			"Unit %s" % (label),
			tf_guarantee_all|skin_id, 0, 0, fac_player_supporters_faction, [],
			level(troop_level)|def_attrib, 0, 0, face_code_1, face_code_2
		])
	return troop_list

def build_preset_4_dummy_skin(skin_id, face_code_1, face_code_2):
	facecode = average_face(face_code_1, face_code_2)
	troop_list = []
	for node_index, (label, troop_level, _) in enumerate(PRESET_4_UNITS):
		troop_list.append([
			preset_4_troop_id(skin_id, node_index) + "_dummy",
			"Unit %s" % (label),
			"Unit %s" % (label),
			tf_guarantee_all|tf_hero|skin_id, 0, 0, fac_player_supporters_faction, [],
			level(troop_level)|def_attrib, 0, 0, facecode
		])
	return troop_list

def modmerge(var_set):
	try:
		orig_troops = var_set["troops"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"troops\".")
	
	# Add preset 4 troops at the very end of the troop list, all together (skin 0 then skin 1)
	insert_index = len(orig_troops)
	skins = [
		(0, man_face_younger_1, man_face_younger_2),
		(1, woman_face_1, woman_face_2),
	]
	ids = {}
	for skin_id, face_code_1, face_code_2 in skins:
		for node_index, (label, _, _) in enumerate(PRESET_4_UNITS):
			ids[(skin_id, label)] = preset_4_troop_id(skin_id, node_index)
		for troop in build_preset_4_skin(skin_id, face_code_1, face_code_2):
			orig_troops.insert(insert_index, troop)
			insert_index += 1

	# Sentinel right after the real preset 4 troops so the (tree, skin 1) range
	# has an end marker (mirrors cstm_custom_troops_end for the base trees).
	orig_troops.insert(insert_index, [
		"cstm_custom_troop_4_end", "cstm_custom_troop_4_end", "cstm_custom_troop_4_end",
		tf_hero, 0, 0, fac_player_supporters_faction, [], level(1)|def_attrib, 0, 0, 0, 0
	])

	# Blank the prefix sentinel's name/plural (inserted by the base mod as
	# blank_troop("cstm_custom_troops_end"), whose default name IS that id
	# string). The prefix is stored in this troop's name; with an empty name the
	# KCT's str_is_empty guards fall back to "Custom" on new games instead of
	# showing the sentinel id as the tree prefix.
	for troop in orig_troops:
		if troop[0] == "cstm_custom_troops_end":
			troop[1] = ""
			troop[2] = ""
			break

	# Dummy troops (used by the presentation for name/equipment display) go at the
	# very end of the troop list, like the base mod's dummies.
	for skin_id, face_code_1, face_code_2 in skins:
		for troop in build_preset_4_dummy_skin(skin_id, face_code_1, face_code_2):
			orig_troops.append(troop)
	
	# Link upgrades by unit label
	for skin_id, _, _ in skins:
		for node_index, (label, _, children) in enumerate(PRESET_4_UNITS):
			base = preset_4_troop_id(skin_id, node_index)
			if len(children) == 0:
				continue
			elif len(children) == 1:
				upgrade(orig_troops, base, ids[(skin_id, children[0])])
			else:
				upgrade2(orig_troops, base, ids[(skin_id, children[0])], ids[(skin_id, children[1])])

