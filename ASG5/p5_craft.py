import json
from collections import namedtuple
from heapq import heappush, heappop           
from math import *   
with open('Crafting.json') as f:
    Crafting = json.load(f)

# List of items that can be in your inventory:
#print "LIST OF ITEMS:", Crafting['Items']
# List of items in your initial inventory with amounts:
#print "LIST OF INITIAL:", Crafting['Initial']
# List of items needed to be in your inventory at the end of the plan:
# (okay to have more than this; some might be satisfied by initial inventory)
#print "LIST OF ITEMS NEEDED:", Crafting['Goal']
# Dictionary of crafting recipes:
#print "DICTIONARY:",Crafting['Recipes']['craft stone_pickaxe at bench']

Recipe = namedtuple('Recipe',['name','check','effect','cost'])
all_recipes = []
#edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}
graph = Crafting['Recipes']
initial = Crafting['Initial']
goal = Crafting['Goal']
Items = Crafting['Items']

#Creates a dictionary that pairs an item with its position
#Goes from 0 to 16
def item_format(items):
    items_list = {}
    for i in range(len(items)):
        items_list[items[i]] = i
    return items_list

item_index = item_format(Crafting['Items'])

def make_checker(rule):
    consumes, requires = rule.get('Consumes',{}), rule.get('Requires',{})
    consumption_pairs = [(item_index[item],consumes[item]) for item in consumes]
    requirement_pairs = [(item_index[item],1) for item in requires]
    both_pairs = consumption_pairs + requirement_pairs    
    #print both_pairs
    def check(state):
        return all([state[i] >= v for i,v in both_pairs])
    return check


def make_effector(rule):
    # use rule to build a list of pairs:
    # (index of item, how much to shift that item count) that covers all items
    produces, consumes = rule.get('Produces',{}), rule.get('Consumes',{})
    production_pairs = [(item_index[item], produces[item]) for item in produces]
    consumption_pairs = [(item_index[item], consumes[item] * -1) for item in consumes]
    delta_pairs = production_pairs + consumption_pairs
    #print "produce: " , production_pairs
    #print "consume: ", consumption_pairs
    #print "delta: " , delta_pairs
    def effect(state):
        #tuple([state[i] + delta for i,delta in delta_pairs])
        stateList = list(state)
        for i, delta in delta_pairs:
            #print i
            #print delta
            stateList[i] += delta
        return tuple(stateList)
    return effect

for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)


def inventory_to_set(d):
    return frozenset(d.items())

def make_state(inv):        
    return tuple(inv.get(name,0) for i,name in enumerate(Items))	

initial_state = make_state(Crafting['Initial'])
goal_state = make_state(Crafting['Goal'])

def graph(state):
    for next_state in all_recipes:
        if next_state.check(state):
            yield (next_state.name, next_state.effect(state), next_state.cost)

def is_goal(state):
    for item in range(0, len(goal_state)):
		#Checking if a string item is in a tuple of numbers
        if state[item] < goal_state[item]:
            return False
    return True
    
# For non consumable items, we only need 1
# For consumable items, we need no more than max amount that is consumed
def heuristic(next_state):
    inf = float('inf')
    if next_state[0] > 1: #bench
        return inf
    elif next_state[1] > 1: #cart
        return inf
    elif next_state[2] > 1: #coal
        return inf
    elif next_state[3] > 8: #cobble
        return inf
    elif next_state[4] > 1: #furnace
        return inf
    elif next_state[5] > 6: #ingot
        return inf
    elif next_state[6] > 1: #iron_axe
        return inf
    elif next_state[7] > 1: #iron_pickaxe
        return inf
    elif next_state[8] > 1: #ore
        return inf
    elif next_state[9] > 6: #plank
        return inf
    elif next_state[10] > 38: #rail
        return inf
    elif next_state[11] > 8: #stick
        return inf
    elif next_state[12] > 1: #stone_axe
        return inf
    elif next_state[13] > 1: #stone_pickaxe
        return inf
    elif next_state[14] > 6: #wood
        return inf
    elif next_state[15] > 1: #wooden_axe
        return inf
    elif next_state[16] > 1: #wooden_pickaxe
        return inf
    else:
        total_dist = 0
        for item in next_state:
            dist = goal_state[item] - next_state[item]
            if dist > 0:
                total_dist += dist
        return total_dist
            			

def search(graph, initial, is_goal, limit, heuristic):
    frontier = []
    path = []
    came_from = {}
    cost_so_far = {}
    heappush(frontier,(0, initial))
    heappush(path, (0, initial))
    came_from[initial] = None
    cost_so_far[initial] = 0
    total = 0
    while frontier:
        dist, curr = heappop(frontier)
        #print "CURR", curr
        if is_goal(curr):
            print "we made it"
            break
        if dist == float('inf'):
            print "!!!REACHED LIMIT!!!"
            break
        currDist = cost_so_far[curr]
        neigh = graph(curr)
        for name, next, cost in neigh:
            new_cost = currDist + cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                #print "NEXT", next
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(next)
                heappush(frontier, (priority, next))
                came_from[next] = (name, curr, cost)
				
    if is_goal(curr) or dist == float('inf'):
        while came_from[curr] is not None:
            print "path: " , curr
            print "cost: " , came_from[curr][2]
            print "action: ", came_from[curr][0]
            path.append(came_from[curr])
            total += came_from[curr][2]
            curr = came_from[curr][1]
        print "start path: " , initial
        print "Total Cost: ", total

    #print came_from
    return path, total

search(graph, initial_state, is_goal, 500, heuristic)