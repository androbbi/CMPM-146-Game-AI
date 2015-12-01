from p6_game import Simulator
from Queue import Queue
ANALYSIS = {}

def analyze(design):
    sim = Simulator(design)
    init = sim.get_initial_state()
    q = Queue()
    disc = {}
    q.put(init)
    disc[init] = True
    ANALYSIS[init] = None
    while not q.empty():	
        state = q.get()
        moves = sim.get_moves()
        for m in moves:
            next_state = sim.get_next_state(state, m)
            if next_state not in disc and next_state is not None and next_state not in ANALYSIS:
                ANALYSIS[next_state] = state
                disc[next_state] = True
                q.put(next_state)

def inspect((i,j), draw_line):
    for key, value in ANALYSIS.iteritems():
        if key[0] == (i,j):
            initialPoint = key
            curr_pnt = key
            prev_pnt = ANALYSIS[curr_pnt]
            while prev_pnt != None:
                draw_line(prev_pnt[0], curr_pnt[0], initialPoint[1], curr_pnt[1])
                curr_pnt = prev_pnt
                prev_pnt = ANALYSIS[prev_pnt]
 		
	#Test line- draw_line((3, 4),(i,j)) 