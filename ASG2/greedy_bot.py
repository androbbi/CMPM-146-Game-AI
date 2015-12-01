'''Implement greedy_bot.py that chooses a legal move that maximizes
the immediate score gain (it looks 1 move into the future and chooses
the one that increases its score the most)'''
def think(state, quip):

	moves = state.get_moves()

	best_move = moves[0]
	best_expectation = float('-inf')

	me = state.get_whos_turn()
	
	def outcome(score):
		if me == 'red':
			return score['red'] - score['blue']
		else:
			return score['blue'] - score['red']
			
	for move in moves:
		total_score = 0.0
		
		depth_state = state.copy()
		depth_state.apply_move(move)
		
		total_score = outcome(depth_state.get_score())
		expectation = float(total_score)
		
		if expectation > best_expectation:
			best_expectation = expectation
			best_move = move
			
	print "Picking %s with expected score %f" % (str(best_move), best_expectation)
	return best_move		