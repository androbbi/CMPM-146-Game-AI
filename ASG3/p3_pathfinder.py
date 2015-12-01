# Returns path: a list of points like ((x1,y1),(x2,y2))
# visited_nodes: a list of boxes explored by your algorithm
# identified by their bounds (x1,x2,y1,y2) (this is the same as in the mesh format)
from Queue import Queue
from math import *
from heapq import heappush, heappop
from Queue import PriorityQueue
'''
# breadth first search
def find_path(source_point, destination_point, mesh):
	sourceX = source_point[0]
	sourceY = source_point[1]
	destX = destination_point[0]
	destY = destination_point[1]
	
	detail_points = {}
	
	path = []
	visited_nodes = []

	box_list = mesh['boxes']
	#adj_list = mesh['adj']
	
	for box in box_list:
		if sourceX > box[0] and sourceX < box[1] and sourceY > box[2] and sourceY < box[3]:
			#print ("source box" + repr(box))
			srcbox = box

		if destX > box[0] and destX < box[1] and destY > box[2] and destY < box[3]:
			#print ("dest box" + repr(box))
			destbox = box
	
	
	
	q = Queue()
	q.put(srcbox)
	visited_nodes.append(srcbox)
	curr_pnt = source_point
	while not q.empty():	
		curr_box = q.get()
		# If we reach the destination, break
		if curr_box == destbox:
			break
		# Else, we move into an edge box
		adj_list = mesh['adj'][curr_box]
		for edge in adj_list:
			# If we have yet to visit this edge
			# Visit it, and search through it
			if edge not in visited_nodes:
				#detail_points.update({'curr_box', curr_pnt})
				next_pnt = constraint(curr_pnt, edge)
				euc_dist = euclidean(curr_box, next_pnt) 
				path.append([curr_pnt, next_pnt])
				q.put(edge)
				visited_nodes.append(edge)
				curr_pnt = next_pnt

	return (path, visited_nodes)
'''

'''
#Dijkstra's algorithm
def find_path(source_point, destination_point, mesh):
	#Initiate source cell
	dist = {}
	prev = {}
	INF = float('inf')
	#prev[source_point] = None
	#dist[source_point] = 0
	box_list = mesh['boxes']
	
	detail_points = {}
	path = []
	visited_nodes = []

	sourceX = source_point[0]
	sourceY = source_point[1]
	destX = destination_point[0]
	destY = destination_point[1]
	
	pQ = []
	# Initialization
	for box in box_list:
		if sourceX > box[0] and sourceX < box[1] and sourceY > box[2] and sourceY < box[3]:
			srcbox = box
			visited_nodes.append(srcbox)
			prev[srcbox] = None
			dist[srcbox] = 0
			heappush(pQ, (srcbox, dist[srcbox]))
		else:
			dist[box] = INF
			prev[box] = None
			
		if destX > box[0] and destX < box[1] and destY > box[2] and destY < box[3]:
			destbox = box
			
		# All nodes initially in Q (unvisited nodes)
		#heappush(pQ, (box, dist[box]))
	
	#visited_nodes.append(srcbox)
	#curr_pnt = source_point
	while pQ:
		curr = heappop(pQ)
		print curr[0]
		if curr[0] == destbox:s
			break	
		curr_pnt = curr[0]
		# For each neighbor of curr
		adj_list = mesh['adj'][curr[0]]
		for edge in adj_list:
			visited_nodes.append(edge)
			next_pnt = constraint(curr[0], edge)
			euc_dist = euclidean(curr[0], next_pnt)
			alt = dist[curr[0]] + euc_dist
			print alt
			if alt < dist[edge]:
				#avisited_nodes.append(edge)
				dist[edge] = alt
				prev[edge] = curr[0]
				#Decrease priority of v and alt
				heappush(pQ, (edge,alt))
		
		path.append([(curr_pnt[0], curr_pnt[1]),(next_pnt[0],next_pnt[1])])
		
	return (path, visited_nodes)
'''
# A*

def find_path(source_point, destination_point, mesh):
	#Initiate source cell
	cost_so_far = {}
	came_from = {}
	INF = float('inf')
	box_list = mesh['boxes']
	
	detail_points = {}
	path = []
	visited_nodes = {}

	sourceX = source_point[0]
	sourceY = source_point[1]
	destX = destination_point[0]
	destY = destination_point[1]
	
	pQ = []
	# Initialization
	for box in box_list:
		if sourceX > box[0] and sourceX < box[1] and sourceY > box[2] and sourceY < box[3]:
			srcbox = box
			visited_nodes[srcbox] = True
			detail_points[srcbox] = source_point
			came_from[srcbox] = None
			cost_so_far[srcbox] = 0
			heappush(pQ, (0, srcbox))
		else:
			cost_so_far[box] = INF
			came_from[box] = None
			
		if destX > box[0] and destX < box[1] and destY > box[2] and destY < box[3]:
			destbox = box
	
	while pQ:
		_, curr = heappop(pQ)
		#print curr[0]
		if curr == destbox:
			break	
		curr_pnt = curr
		# For each neighbor of curr
		adj_list = mesh['adj'][curr]
		for edge in adj_list:
			next_pnt = constraint(curr, edge)
			euc_dist = euclidean(curr, next_pnt)
			new_cost = cost_so_far[curr] + euc_dist
			if edge not in cost_so_far or new_cost < cost_so_far[edge]:
				visited_nodes[edge] = True
				detail_points[edge] = next_pnt
				rem_dist = euclidean(next_pnt, destination_point)
				cost_so_far[edge] = new_cost
				priority = new_cost + rem_dist
				heappush(pQ, (priority, edge))
				came_from[edge] = curr
	# dict iterator ex:
	#for key, value in d.iteritems():	
	'''if curr[0] == destbox:
		#point = destination_point
		for point, box in detail_points.iteritems():
			path.append((detail_points[box], point))
			point = detail_points[box]
			print box
		path.append((source_point, point))
	else:'''
	if curr[0] != destbox:
		print "Path not found"
	
	return (path, visited_nodes.keys())
	
def constraint(curr, next):
	x, y = curr[0], curr[1]
	nextX1, nextX2 = next[0], next[1]
	nextY1, nextY2 = next[2], next[3]
	# Calculate the path X
	x_next = min(nextX2-1,max(nextX1, x))
	# Calculate the path Y
	y_next = min(nextY2-1,max(nextY1, y))
	return (x_next, y_next)

def euclidean(curr, next):
	# Calculate the  Euclidean distances
	calcC = curr[0] - next[0]
	calcC = calcC * calcC
	calcN = curr[1] - next[1]
	calcN = calcN * calcN
	calcXY = calcN + calcC
	euclidean = sqrt(calcXY)
	return euclidean
