# -*- coding: cp1254 -*-
from header_common import *
from header_troops import *
from header_items import *
from header_skills import *
from ID_factions import *

tf_guarantee_all = tf_guarantee_boots|tf_guarantee_armor|tf_guarantee_gloves|tf_guarantee_helmet|tf_guarantee_horse|tf_guarantee_shield|tf_guarantee_ranged

man_face_younger_1 = 0x0000000000000001124000000020000000000000001c00800000000000000000
man_face_younger_2 = 0x000000003f0052064deeffffffffffff00000000001efff90000000000000000
woman_face_1 = 0x0000000000000001000000000000000000000000001c00000000000000000000
woman_face_2 = 0x00000003bf0030067ff7fbffefff6dff00000000001f6dbf0000000000000000

# Preset 4 - 22 units matching extended_progression_tree.md (A -> B.1/B.2 ->
# C.1-C.4 -> D1-D6 -> E1-E6 -> F1-F3, one level per quality tier). Each entry:
# (unit label, troop level, [upgrade target labels]).
PRESET_4_UNITS = [
	("A",  2,  ["B1", "B2"]),
	("B1", 10, ["C1", "C2"]),
	("B2", 10, ["C3", "C4"]),
	("C1", 18, ["D1"]),
	("C2", 18, ["D2"]),
	("C3", 18, ["D3", "D4"]),
	("C4", 18, ["D5", "D6"]),
	("D1", 26, ["E1"]),
	("D2", 26, ["E2"]),
	("D3", 26, ["E3"]),
	("D4", 26, ["E4"]),
	("D5", 26, ["E5"]),
	("D6", 26, ["E6"]),
	("E1", 34, ["F1"]),
	("E2", 34, []),
	("E3", 34, ["F2"]),
	("E4", 34, []),
	("E5", 34, []),
	("E6", 34, ["F3"]),
	("F1", 40, []),
	("F2", 40, []),
	("F3", 40, []),
]

def preset_4_troop_id(skin_id, node_index):
	return "cstm_custom_troop_4_%d_%d_0" % (skin_id, node_index)

def average_face(face_1, face_2):
	age_and_skin_mask = 0xfffffffffffffffff00000000000000000000000000000000000000000000000
	average_features  = 0x000000000000000006db6db6db6db6db00000000000db6db0000000000000000
	return (((face_1 + face_2) / 2) & age_and_skin_mask) + average_features

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
