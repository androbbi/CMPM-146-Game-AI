# Brandon Gomez brlgomez
# Antony Robbins androbbi
from heapq import heappush, heappop 
from collections import namedtuple
import json
with open('Crafting.json') as f:
	Crafting = json.load(f)

def make_checker(rule):
	# this code runs once
	# do something with rule['Consumes'] and rule['Requires']
	def check(state):
		# this code runs millions of times
		return True # or False
	
	return check

def make_effector(rule):
	# this code runs once
    # do something with rule['Produces'] and rule['Consumes']
	def effect(state):
		next_state = rule['Produces']
		# this code runs millions of times
		return next_state
	
	return effect


Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []

# name prints the name of recipes
# rule contains Time, Requires, Consumes, Produces
for name, rule in Crafting['Recipes'].items():
	checker = make_checker(rule)
	effector = make_effector(rule)
	recipe = Recipe(name, checker, effector, rule['Time'])
	all_recipes.append(recipe)

# graph: a function that can be called on a node to get adjacent nodes
# the result should be a sequence/list of (action, next_state, cost) tuples
edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}
def t_graph(state):
	for next_state, cost in edges[state].items():
		yield ((state,next_state), next_state, cost)

# graph = Crafting['Recipes']
# initial = Crafting['Initial']
# is_goal = Crafting['Goal']

# initial: an initial state
t_initial = 'a'

# limit a float or integer representing the maximum search distance
# without this, your algorithm has no way of terminating if the goal conditions are impossible
t_limit = 20

# is_goal: a function that takes a state and returns True or Fase
def t_is_goal(state):
	return state == 'c'
	
# heuristic: a function that takes some next_state and returns an estimated cost
def t_heuristic(state):
	return 0

def search(graph, initial, is_goal, limit, heuristic):
	#initialize   
	heapQ = []
	came_from = {}
	cost_so_far = {}
	heappush(heapQ,(initial, 0))
	# dictionary[key] = value
	came_from[heapQ[0]] = initial
	cost_so_far[heapQ[0]] = 0
	print "EDGES", edges
	while heapQ:
		curr = heappop(heapQ)
		# if we reached our goal
		if curr == is_goal:
			break   
		edges = t_graph(curr)
		#for e in edges:
			#new_cost = cost_so_far[curr] + e[2]
	return "hi mom"

search(t_graph, t_initial, t_is_goal, t_limit, t_heuristic)

# List of items that can be in your inventory:
#print Crafting['Items']
# example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

# List of items in your initial inventory with amounts:
#print Crafting['Initial']
# {'coal': 4, 'plank': 1}

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
#print Crafting['Goal']
# {'stone_pickaxe': 2}

# Dictionary of crafting recipes:
#print Crafting['Recipes']['craft stone_pickaxe at bench']
# example:
# {	'Produces': {'stone_pickaxe': 1},
#	'Requires': {'bench': True},
#	'Consumes': {'cobble': 3, 'stick': 2},
#	'Time': 1
# }