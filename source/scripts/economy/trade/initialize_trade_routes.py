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

initialize_trade_routes_scripts = [
#script_game_event_buy_item:
("initialize_trade_routes",
	[
	  #SARGOTH - 10 routes
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_2"), #Sargoth - Tihr
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_4"), #Sargoth - Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_12"), #Sargoth - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_11"), #Sargoth - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_8"), #Sargoth - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_13"), #Sargoth - Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_7"), #Sargoth - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_9"), #Sargoth - Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_6"), #Sargoth - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_15"), #Sargoth - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_1", "p_town_16"), #Sargoth - Dhirim

	  #TIHR- 8 Routes
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_4"), #Tihr- Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_6"), #Tihr - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_7"), #Tihr - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_15"), #Tihr - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_12"), #Tihr - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_8"), #Tihr - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_11"), #Tihr - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_2", "p_town_16"), #Thir - Dhirim

	  #VELUCA - 8 Routes
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_7"), #Veluca- Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_5"), #Veluca - Jelkala
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_15"), #Veluca - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_16"), #Veluca - Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_14"), #Veluca - Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_4"), #Veluca - Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_19"), #Veluca - Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_3", "p_town_6"), #Veluca - Praven

	  #SUNO - 11 routes
	  #Sargoth, Tihr, Veluca
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_12"), #Suno - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_8"), #Suno - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_11"), #Suno - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_6"), #Suno - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_7"), #Suno - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_16"), #Suno - Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_5"), #Suno - Jelkala
      (call_script, "script_set_trade_route_between_centers", "p_town_4", "p_town_15"), #Suno - Yalen

	  #JELKALA - 6 ROUTES
      #Veluca, Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_15"), #Jelkala - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_6"), #Jelkala - Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_7"), #Jelkala - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_5", "p_town_19"), #Jelkala - Shariz

	  #PRAVEN - 7 ROUTES
	  #Tihr, Veluca, Suno, Jelkala
      (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_7"), #Praven - Uxkhal
      (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_15"), #Praven - Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_6", "p_town_16"), #Praven - Dhirim

	  #UXKHAL - 9 Routes
	  #Sargoth, Tihr, Suno, Jelkala, Praven
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_15"), #Yalen
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_19"), #Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_7", "p_town_14"), #Halmar

	  #REYVADIN - 9 Routes
	  #Suno, Sargoth
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_9"), #Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_11"), #Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_12"), #Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_13"), #Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_8", "p_town_17"), #Ichamur

	  #KHUDAN - 9 Routes
	  #Sargoth, Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_11"), #Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_13"), #Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_12"), #Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_17"), #Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_10"), #Tulga
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_9", "p_town_18"), #Narra

	  #TULGA - 7 Routes
	  #Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_17"), #Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_22"), #Bariyye
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_14"), #Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_10", "p_town_20"), #Durquba

	  #CURAW - 9 Routes
	  #Khudan, Reyvadin, Sargoth, Suno
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_12"), #Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_13"), #Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_14"), #Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_16"), #Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_11", "p_town_17"), #Ichamur

	  #WERCHEG - 7 Routes
	  #Sargoth, Suno, Reyvadin, Khudan, Curaw, Tihr
      (call_script, "script_set_trade_route_between_centers", "p_town_12", "p_town_13"), #Rivacheg

	  #RIVACHEG - 6 Routes
	  #Sargoth, Reyvadin, Khudan, Curaw, Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_13", "p_town_17"), #Ichamur

	  #HALMAR- 11 Routes
	  #Veluca, Uxkhal, Tulga, Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_17"), #Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_22"), #Bariyye
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_19"), #Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_14", "p_town_16"), #Dhirim

	  #YALEN - 7 Routes
	  #Sargoth, Tihr, Veluca, Suno, Jelkala, Praven, Uxkhal

	  #DHIRIM - 13 Routes
	  #Sargoth, Thir, Veluca, Suno, Praven, Uxkhal, Reyvadin, Khudan, Curaw, Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_18"), #Narra
      (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_16", "p_town_19"), #Shariz

	  #ICHAMUR - 7 Routes
      #Reyvadin, Khudan, Tulga, Curaw, Rivacheg, Halmar
      (call_script, "script_set_trade_route_between_centers", "p_town_17", "p_town_18"), #Narra

	  #NARRA - 9 Routes
      #Reyvadin, Khudan, Tulga, Halmar, Dhirim, Ichamur
      (call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_18", "p_town_22"), #Bariyye

	  #SHARIZ - 8 Routes
      #Veluca, Jelkala, Uxkhal, Halmar, Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_20"), #Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_19", "p_town_22"), #Bariyye

	  #DURQUBA - 7 Routes
      #Tulga, Halmar, Dhirim, Narra, Shariz
      (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_21"), #Ahmerrad
      (call_script, "script_set_trade_route_between_centers", "p_town_20", "p_town_22"), #Bariyye

	  #AHMERRAD - 6 Routes
      #Tulga, Halmar, Narra, Shariz, Durquba
      (call_script, "script_set_trade_route_between_centers", "p_town_21", "p_town_22"), #Bariyye

	  #BARIYYE - 6 Routes
      #Tulga, Halmar, Narra, Shariz, Durquba, Ahmerrad

    #ZENDAR - 8 Routes
      #Sargoth, Tihr, Wercheg,Reyvadin, Curaw, Khudan, Rivacheg, Dhirim
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_1"), #Zendar - Sargoth
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_2"), #Zendar - Tihr
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_12"), #Zendar - Wercheg
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_8"), #Zendar - Reyvadin
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_11"), #Zendar - Curaw
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_9"), #Zendar - Khudan
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_13"), #Zendar - Rivacheg
      (call_script, "script_set_trade_route_between_centers", "p_town_23", "p_town_16"), #Zendar - Dhirim
	])
]
