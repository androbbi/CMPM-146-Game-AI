import random

def think(state, quip):
    
    moves = state.get_moves()
    
    move = random.choice(moves)
    
    return move
