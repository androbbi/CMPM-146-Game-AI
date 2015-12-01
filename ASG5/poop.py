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
edges = {'a': {'b':1,'c':10}, 'b':{'c':1}}
graph = Crafting['Recipes']
initial = Crafting['Initial']
goal = Crafting['Goal']
Items = Crafting['Items']

def item_format(items):
    items_list = {}
    for i in range(len(items)):
        items_list[items[i]] = i
    return items_list

item_index = item_format(Crafting['Items'])
#print item_index

def make_checker(rule):
    consumes, requires = rule.get('Consumes',{}), rule.get('Requires',{})
    consumption_pairs = [(item_index[item],consumes[item]) for item in consumes]
    requirement_pairs = [(item_index[item],1) for item in requires]
    both_pairs = consumption_pairs + requirement_pairs    
    def check(state):
        #print "check:", state[0]
        return all([state[i] >= v for i,v in both_pairs])
    return check

def make_effector(rule):
    produces, consumes = rule.get('Produces',{}), rule.get('Consumes',{})
    for i in Items:
        if i not in produces:
            produces[i] = 0
    production_pairs = [(item_index[item], produces[item]) for item in Items]
    consumption_pairs = [(item_index[item], 1) for item in consumes]
    both_pairs = production_pairs + consumption_pairs
    def effect(state):
        #print "effect:", state[0]
        return tuple([state[i] + v for i,v in both_pairs])
    return effect

for name, rule in Crafting['Recipes'].items():
    checker = make_checker(rule)
    effector = make_effector(rule)
    recipe = Recipe(name, checker, effector, rule['Time'])
    all_recipes.append(recipe)

def inventory_to_tuple(d):
    return tuple(d.get(name,0) for i,name in enumerate(Items))

def inventory_to_set(d):
    return frozenset(d.items())

def make_initial_state(inventory):
    state = inventory_to_tuple(inventory)
    #print state
    #hashable_state = inventory_to_set(inventory)                                        
    #print hashable_state                                                                
    return state

initial_state = make_initial_state(Crafting['Initial'])
goal_state = make_initial_state(Crafting['Goal'])

def graph(state):
    for next_state in all_recipes:
        if next_state.check(state):
            yield (next_state.name, next_state.effect(state), next_state.cost)

def is_goal(state):
    for item, amount in Crafting['Goal'].items():
        if item in state:
            if state[1] < amount:
                return False
        else:
            return False
    return True
    
def heuristic(next):
     inf = float('inf')
     if next[0] is 2: #bench
         return inf
     elif next[1] > 2: #cart
         return inf
     elif next[2] > 5: #coal
         return inf
     elif next[3] > 8: #cobble
         return inf
     elif next[4] is 2: #furnace
         return inf
     elif next[5] > 6: #ingot
         return inf
     elif next[6] is 2: #iron_axe
         return inf
     elif next[7] is 2: #iron_pickaxe
         return inf
     elif next[8] is 7: #ore
         return inf
     elif next[9] > 8: #plank
         return inf
     elif next[10] > 32: #rail
         return inf
     elif next[11] > 6: #stick
         return inf
     elif next[12] is 2: #stone_axe
         return inf
     elif next[13] is 2: #stone_pickaxe
         return inf
     elif next[14] > 2: #wood
         return inf
     elif next[15] is 2: #wooden_axe
         return inf
     elif next[16] is 2: #wooden_pickaxe
         return inf
     else:
         return 0

def search(graph, initial, is_goal, limit, heuristic):
    path = []
    came_from = {}
    cost_so_far = {}
    frontier = [(initial, 0)]
    came_from[initial] = None
    cost_so_far[initial] = 0
    total = 0
    while frontier:
        curr, dist = heappop(frontier)
        #print "CURR", curr, dist
        if curr == goal_state:
            break
        if dist == float('inf'):
            #print "!!!REACHED LIMIT!!!"
            break
        
        currDist = cost_so_far[curr]
        neigh = graph(curr)
        for name, next, cost in neigh:
            new_cost = currDist + cost
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(curr)
                came_from[next] = (name, curr, cost)
                heappush(frontier, (next, priority))
                
    if curr == goal_state or dist == float('inf'):
        while came_from[curr] is not None:
            path.append(came_from[curr])
            total += came_from[curr][2]
            curr = came_from[curr][1]

    return path, total

print search(graph, initial_state, is_goal, 50, heuristic)