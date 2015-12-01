import json
from collections import namedtuple
from heapq import heappush, heappop           
from math import *   
with open('Crafting.json') as f:
    Crafting = json.load(f)

# List of items that can be in your inventory:
#print "LIST OF ITEMS:", Crafting['Items']
# example: ['bench', 'cart', ..., 'wood', 'wooden_axe', 'wooden_pickaxe']

# List of items in your initial inventory with amounts:
#print "LIST OF INITIAL:", Crafting['Initial']
# {'coal': 4, 'plank': 1}

# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
#print "LIST OF ITEMS NEEDED:", Crafting['Goal']
# {'stone_pickaxe': 2}

# Dictionary of crafting recipes:
#print "DICTIONARY:",Crafting['Recipes']['craft stone_pickaxe at bench']
# example:
# {'Produces': {'stone_pickaxe': 1},
#'Requires': {'bench': True},
#'Consumes': {'cobble': 3, 'stick': 2},
#'Time': 1
# }

item_index = {}
Items = Crafting['Items']
'''
graph = Crafting['Recipes']
is_goal = Crafting['Goal']
'''

'''
hashable_state = inventory_to_frozenset(state_dict) # --> frozenset({('coal':5)})
dist[h] = 6
'''

def inventory_to_tuple(d):
	return tuple(d.get(name,0) for i,name in enumerate(Items))

def inventory_to_set(d):
	return frozenset(d.items())
	
def make_initial_state(inventory):
	state = inventory_to_tuple(inventory)
	print state
	#hashable_state = inventory_to_set(inventory)
	#print hashable_state
	return state

initial_state = make_initial_state(Crafting['Initial'])

def make_checker(rule):                                                             
    # do something with rule['Consumes'] and rule['Requires']                            
    consumes, requires = rule.get('Consumes',{}), rule.get('Requires',{})
    consumption_pairs = [(item_index[item],consumes[item]) for item in consumes]
    requirement_pairs = [(item_index[item],1) for item in requires]
    both_pairs = consumption_pairs + requirement_pairs
	
    def check(state):
        return all([state[i] >= v for i,v in both_pairs])                                                          
    
	return check

def make_effector(rule):
    # this code runs once                                                                
    # do something with rule['Produces'] and rule['Consumes']                            
    def effect(state):
        # this code runs millions of times                                               
        next_state = rule['Produces']
        return next_state
    return effect
	
Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

def search(graph, initial, is_goal, limit, heuristic):
    heapq = []
    path = []
    came_from = {}
    cost_so_far = {}
    heappush(path, (initial, 0))
    heappush(heapq,(initial, 0))
    came_from[initial] = None
    cost_so_far[initial] = 0
    print "EDGES", edges
    while heapq:
        curr = heappop(heapq)
        if is_goal(curr[0]):
            break
        neighbors = t_graph(curr[0])
        for next in neighbors:
            new_cost = cost_so_far[curr[0]] + next[2]
            if next[1] not in cost_so_far or new_cost < cost_so_far[next[1]]:
                cost_so_far[next[1]] = new_cost
                priority = new_cost + heuristic(curr)
                heappush(heapq, (next[1], priority))
                came_from[next[1]] = curr
        heappush(path, (next[1], priority))
    return cost_so_far[curr[0]], path

#print search(graph, initial, is_goal, limit, heuristic)

#test material
'''
t_initial = 'a'
t_limit = 20
edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}
def t_graph(state):
    try:
        for next_state, cost in edges[state].items():
            yield ((state,next_state), next_state, cost)
    except KeyError:
        return
		
def t_is_goal(state):
	return state == 'c'
	
def t_heuristic(state):
	return 0
'''	