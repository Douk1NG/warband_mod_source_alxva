# -*- coding: cp1254 -*-
from header_common import *
from header_troops import *
from header_items import *
from header_skills import *
from ID_factions import *

from kingdom_custom_troop_tree_creator_constants import *

def build_custom_preset_skin(tree_index, units, skin_id, face_code_1, face_code_2):
	troop_list = []
	for node_index, (label, troop_level, _) in enumerate(units):
		troop_list.append([
			kct_custom_preset_troop_id(tree_index, skin_id, node_index),
			"Unit %s" % (label),
			"Unit %s" % (label),
			tf_guarantee_all|skin_id, 0, 0, fac_player_supporters_faction, [],
			level(troop_level)|def_attrib, 0, 0, face_code_1, face_code_2
		])
	return troop_list

def build_custom_preset_dummy_skin(tree_index, units, skin_id, face_code_1, face_code_2):
	facecode = average_face(face_code_1, face_code_2)
	troop_list = []
	for node_index, (label, troop_level, _) in enumerate(units):
		troop_list.append([
			kct_custom_preset_troop_id(tree_index, skin_id, node_index) + "_dummy",
			"Unit %s" % (label),
			"Unit %s" % (label),
			tf_guarantee_all|tf_hero|skin_id, 0, 0, fac_player_supporters_faction, [],
			level(troop_level)|def_attrib, 0, 0, facecode
		])
	return troop_list

def build_template_storage_troops():
	troop_list = []
	for slot_index in xrange(kct_template_slot_count):
		meta_id = kct_template_meta_troop_id(slot_index)
		troop_list.append([
			meta_id, "", "", tf_hero, 0, 0, fac_player_supporters_faction, [],
			level(1)|def_attrib, 0, 0, 0, 0
		])
		for node_index in xrange(kct_template_nodes_per_slot):
			node_id = kct_template_node_troop_id(slot_index, node_index)
			troop_list.append([
				node_id, "", "", tf_hero|tf_guarantee_all, 0, 0,
				fac_player_supporters_faction, [], level(1)|def_attrib,
				0, 0, man_face_younger_1, man_face_younger_2
			])
	return troop_list

def modmerge(var_set):
	try:
		orig_troops = var_set["troops"]
	except KeyError:
		raise ValueError("Variable set does not contain expected variable: \"troops\".")
	
	# Add KCTT custom preset troops at the very end of the troop list.
	insert_index = len(orig_troops)
	skins = [
		(0, man_face_younger_1, man_face_younger_2),
		(1, woman_face_1, woman_face_2),
	]
	ids = {}
	for tree_index, _, units in KCT_CUSTOM_PRESETS:
		for skin_id, face_code_1, face_code_2 in skins:
			for node_index, (label, _, _) in enumerate(units):
				ids[(tree_index, skin_id, label)] = kct_custom_preset_troop_id(tree_index, skin_id, node_index)
			for troop in build_custom_preset_skin(tree_index, units, skin_id, face_code_1, face_code_2):
				orig_troops.insert(insert_index, troop)
				insert_index += 1
		orig_troops.insert(insert_index, [
			"cstm_custom_troop_%d_end" % tree_index, "cstm_custom_troop_%d_end" % tree_index, "cstm_custom_troop_%d_end" % tree_index,
			tf_hero, 0, 0, fac_player_supporters_faction, [], level(1)|def_attrib, 0, 0, 0, 0
		])
		insert_index += 1

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
	for tree_index, _, units in KCT_CUSTOM_PRESETS:
		for skin_id, face_code_1, face_code_2 in skins:
			for troop in build_custom_preset_dummy_skin(tree_index, units, skin_id, face_code_1, face_code_2):
				orig_troops.append(troop)
	
	# Link upgrades by unit label
	for tree_index, _, units in KCT_CUSTOM_PRESETS:
		for skin_id, _, _ in skins:
			for node_index, (label, _, children) in enumerate(units):
				base = kct_custom_preset_troop_id(tree_index, skin_id, node_index)
				if len(children) == 0:
					continue
				elif len(children) == 1:
					upgrade(orig_troops, base, ids[(tree_index, skin_id, children[0])])
				else:
					upgrade2(orig_troops, base, ids[(tree_index, skin_id, children[0])], ids[(tree_index, skin_id, children[1])])

	for troop in build_template_storage_troops():
		orig_troops.append(troop)
