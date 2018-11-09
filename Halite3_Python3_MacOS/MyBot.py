#!/usr/bin/env python3

# Import the Halite SDK, which will let you interact with the game.
import hlt
from hlt import constants

import heapq
import random
import logging
import collections

# This game object contains the initial game state.
directions = ["n","s","e","w"]
game = hlt.Game()
# Respond with your name.
game.ready("Well")
goback = {}
yard = game.game_map[game.me.shipyard].position
halamounts = {}
target = []

def getHal(shippos):
	for j in range(int(shippos.x)-30,int(shippos.x)+30):
		for k in range(int(shippos.y)-30,int(shippos.y)+30):
			halamounts[(j,k)] = game_map[hlt.Position(j,k)].halite_amount
	return collections.OrderedDict(reversed(sorted(halamounts.items(), key=lambda t: t[1])))

def AssignTarget(shipsid):
	highesthal.popitem()
	highesthal.popitem()
	target.insert(shipsid,hlt.Position(highesthal.popitem()[0][0],highesthal.popitem()[0][1]))

while True:
	# Get the latest game state.
	game.update_frame()
	# You extract player metadata and the updated map metadata here for convenience.
	me = game.me
	game_map = game.game_map
	
	# A command queue holds all the commands you will run this turn.
	command_queue = []
	highesthal = getHal(game_map[game.me.shipyard].position)
	for ship in me.get_ships():
		if ship.halite_amount > 6*(constants.MAX_HALITE/7):
			goback[ship.id] = True
		elif game_map.calculate_distance(ship.position, yard) < 1:
			goback[ship.id] = False
		try:
			if game_cell[target[ship.id]].halite_amount < constants.MAX_HALITE/20:
				highesthal = getHal(ship.position)
				AssignTarget(ship.id)
			else:
				pass
		except:
			AssignTarget(ship.id)

		if game.turn_number > constants.MAX_TURNS*(8/9):
			try:
				command_queue.append(ship.move(random.choice(game_map.get_unsafe_moves(ship.position, yard))))
			except:
				command_queue.append(ship.move((0,0)))
		elif game_map[ship.position].halite_amount > constants.MAX_HALITE / 20 and ship.halite_amount < 8*(constants.MAX_HALITE/9):
			command_queue.append(ship.stay_still())
		elif goback[ship.id]:
			command_queue.append(ship.move(game_map.naive_navigate(ship, yard)))
		elif game_map[ship.position].halite_amount < constants.MAX_HALITE / 15:
			command_queue.append(ship.move(game_map.naive_navigate(ship,target[ship.id])))
		else:
			command_queue.append(ship.move(game_map.naive_navigate(ship, yard)))

	if game.turn_number >= 1 and (me.halite_amount >= constants.SHIP_COST or (len(me.get_ships()) < 1 and me.halite_amount >= constants.SHIP_COST)) and not game_map[me.shipyard].is_occupied:
			if game.turn_number < constants.MAX_TURNS/3 and len(me.get_ships()) < 12:
				command_queue.append(game.me.shipyard.spawn())
			elif len(me.get_ships()) < 1:
				command_queue.append(game.me.shipyard.spawn())
	# Send your moves back to the game environment, ending this turn
	game.end_turn(command_queue)
