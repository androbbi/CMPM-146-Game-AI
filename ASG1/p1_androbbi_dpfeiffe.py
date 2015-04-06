# Dustin Pfeiffer dpfeiffe
# Antony Robbins androbbi

# Import necessities
from p1_support import load_level, show_level
from math import sqrt
from heapq import heappush, heappop
#PriorityQueue uses the first value in a tuple as the comparator,
#so I switched EVERY tuple to be (distance, coordinate) instead of
#the previous (coord, dist).
from Queue import PriorityQueue

# Find the shortest path
def dijkstras_shortest_path(src, dst, graph, adj):
	#Initiate source cell
	dist = {}
	prev = {}
	prev[src] = None
	dist[src] = 0
	source = (dist[src], src)
	heapq = PriorityQueue()
	heapq.put(source)
	
	finalpath = []
	path = []
	
	while not heapq.empty():
		# Set up current to current cell
		current = heapq.get()
		# Return the path to destination
		if current[1] == dst:
			end = current[1]
			path = []
			while end is not None:
				path.append(end)
				end = prev[end]
				
			printD ("total distance: " + str(dist[current[1]]))
			return path
			#finalpath.append(current)
			
		# Gets the neighbors and finds the shortest possible path
		neighbors = adj(graph, current)
		for neigh in neighbors:
			alt = dist[current[1]] + neigh[0]
			if neigh[1] not in dist or alt < dist[neigh[1]]:
				dist[neigh[1]] = alt
				prior = alt
				heapq.put((prior, neigh[1]))
				prev[neigh[1]] = current[1]
	
# Look at the possible 8 directions to move in
def navigation_edges(level, cell):
	# Coordinates and distance from previous cell
	# hold the tuple values
	# Can be accessed by [0] and [1]
	# [1] is coord
	# [0] is distance
	steps = []
	distance, coord = cell
	printD ("coord of cell: " + str(coord))
	printD ("distance to cell: " + str(distance))
	x, y = coord
	# specifically checks what is in each direction
	for dx in [-1,0,1]:
		for dy in [-1,0,1]:
			next_cell = x + dx, y + dy
			dist = sqrt(dx*dx+dy*dy)
			printD ("coord of next cell: " + str(next_cell))
			printD ("distance to next cell: " + str(dist))
			printD ("\n")
			# If next cell is a river, distance takes dist*delay turns
			if next_cell in level['obstacles']:
				dist*= int(delay)
				printD("delayed distance: " + str(dist))
			# If you have a distance of 0, you do not move, so skip
			if dist > 0 and next_cell in level['spaces']: 
				if (dist, next_cell) not in steps:
					steps.append((dist, next_cell))
			
	return steps
	
def test_route(filename, src_waypoint, dst_waypoint):
	level = load_level(filename)

	show_level(level)

	src = level['waypoints'][src_waypoint]
	dst = level['waypoints'][dst_waypoint]

	path = dijkstras_shortest_path(src, dst, level, navigation_edges)

	if path:
		show_level(level, path)
	else:
		print "No path possible!"

# Print debug statements
def printD (stri):
	if debug != "false":
		print str(stri)
		
# Delay value is required
if __name__ ==  '__main__':
	import sys
	_, filename, src_waypoint, dst_waypoint, delay, debug = sys.argv
	test_route(filename, src_waypoint, dst_waypoint)
