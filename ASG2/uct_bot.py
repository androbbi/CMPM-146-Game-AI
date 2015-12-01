from math import *
import random
import time
THINK_DURATION = 1

class Node:
    ''' A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    '''
    def __init__(self, move = None, parent = None, state = None):
        self.move = move # the move that got us to this node - "None" for the root node
        self.parentNode = parent # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.untriedMoves = state.get_moves() # future child nodes
        self.playerJustMoved = state.get_whos_turn() # the only part of the state that the Node needs later
        
    def UCTSelectChild(self):
        ''' Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        '''
        s = sorted(self.childNodes, key = lambda c: float(c.wins)/c.visits + sqrt(2*log(self.visits)/c.visits))[-1]
        return s
    
    def AddChild(self, m, s, p):
        ''' Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        '''
        n = Node(move = m, parent = self, state = s)
        n.playerJustMoved = p
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n

    def returnVisits(self):
        return self.visits
    
    
    def Update(self, result):
        ''' Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        '''
        self.visits += 1
        self.wins += result

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
             s += c.TreeToString(indent+1)
        return s

    def IndentString(self,indent):
        s = "\n"
        for i in range (1,indent+1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
             s += str(c) + "\n"
        return s

def think(rootstate, quip):

    moves = rootstate.get_moves()
    
    best_move = moves[0]
    best_expectation = float('inf')

    me = rootstate.get_whos_turn()
    
    t_start = time.time()
    t_deadline = t_start + THINK_DURATION

    iterations = 0

    def outcome(score, player):
        if player == 'red':
            return score['red'] #- score['blue']
        else:
            return score['blue'] #- score['red']

    rootnode = Node(state = rootstate)

    while True:
        
        total_score = 0.0
        iterations += 1
        t_now = time.time()
        if t_now > t_deadline:
            break

        node = rootnode
        state = rootstate.copy()
        
        while node.untriedMoves == [] and node.childNodes != []:
            node = node.UCTSelectChild()
            state.apply_move(node.move)
            
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves) 
            play = state.get_whos_turn()
            state.apply_move(m)
            node = node.AddChild(m, state, play)

        while state.get_moves() != []:
            state.apply_move(random.choice(state.get_moves()))
        
        iter = 0
        while node != None:
            player = node.playerJustMoved
            result = state.get_score()
            #print outcome(result)
            #total_score += (outcome(result))
            node.Update(outcome(result, player))
            node = node.parentNode
            iter += 1
            
        #epectation = float(total_score)/iter

    print iterations
    #print player
    #var = sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
    #print "picking %s %f" % (str(var), epectation)
    return sorted(rootnode.childNodes, key = lambda c: c.visits)[-1].move
