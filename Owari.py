#Natalie Carlson: nfcarlson@alaska.edu
#Linda Lee: ldlee3@alaska.edu
#William de Schweinitz: william.z@ak.net

#AI - #3 Owari
#Due 10/24/19



####Node object####
class Node:
	def __init__(self, board, depth, value = None, pit = None):
		self.board = board
		self.depth = depth
		self.value = value
		self.pit = pit
		self.children = []
		
		
	def createChild(self, pit):
		childBoard = self.board[:]
		childBoard = updateBoard(pit, childBoard)#get child board
		return Node(childBoard, self.depth+1, None, pit) #create child node


###Evaluation Function####
#This function gives a hueristic value to a game state 
def evaluate(node, m):
	
	value = 0
	
	#number of seeds in goal
	value += node.board[6] #computer
	value -= node.board[13] #opponent
	
	#number of seeds captured weighted double
	value += node.board[14]*2 #computer
	value -= node.board[15]*2 #opponent
	
		
	return value


####Search Algrorithms###
#This function gets the optimal move for the computer to make
def alphaBetaSearch(node):
	v = maxValue(node, -100, 100)
	for child in node.children:
		if child.value == v:
			return child.pit
	print("Error: value not found in children")
	exit(1)

#This function finds the maximum value
def maxValue(node, alpha, beta):
	
	if (checkDone(node.board) == True) or (node.depth > maxDepth): #leaf: at end of game or pre-determined cutoff
		return evaluate(node, 'max') 	
	
	v = -100
	for pit in range(0,6): #computer pits
		if node.board[pit] > 0: #pit not empty
			child = node.createChild(pit)
			node.children.append(child)
			
			v = max(v, minValue(child, alpha, beta))
			child.value = v
			if v >= beta:
				return v		
			alpha = max(alpha, v) #update alpha	
	
	return v

#This function finds the minimal value	
def minValue(node, alpha, beta):#(node, alpha, beta):
		
	if (checkDone(node.board) == True) or (node.depth > maxDepth): #leaf: at end of game or pre-determined cutoff
		return evaluate(node, 'min')	
	
	v = 100
	for pit in range(7,13): #opponent pits
		if node.board[pit] > 0: #pit not empty
			child = node.createChild(pit)
			node.children.append(child) 
			v = min(v, maxValue(child, alpha, beta))
			child.value = v
			if v <= alpha:
				return v
			beta = min(beta,v)
	return v


####	Main	####
def main():
	
	global maxDepth
	global sCompCap
	global nOppCap
	
	south = 'sComp' #Computer #sComp pits = board[0-5] #sComp goal = board[6]
	north = 'nOpp'	#opponent #nOpp pits = board[7-12] #nOpp goal = board[13]
	board = [3,3,3,3,3,3,0,3,3,3,3,3,3,0, 0,0] #pit 14 holds computer's captures, pit 15 holds opponents
	
	displayBoard(board)
	maxDepth = int(input("Enter max depth level: "))
	turn = getFirstPlayer()

	#play game
	while turn != 'done':
		
		if turn == 'nOpp':
			move = getNOppMove(board)
		else:
			move = getSCompMove(board)
		
		board = updateBoard(move, board)
		displayBoard(board)
		
		if (checkDone(board) == True):
			turn = 'done'
		else: #switch to next player's turn
			if turn == 'nOpp':
				turn = 'sComp'
			else:
				turn = 'nOpp'
	
	#game over
	board = collectStones(board)	
	displayBoard(board)
	checkWinner(board)	


####	Game Helper functions	####	

# This function requests and then returns who the first player will be
def getFirstPlayer():
	
	first = ''
	while first is not 'y' and first is not 'n':
		first = input("Would you like to go first? (Enter 'y' or 'n'): ")
	if first == 'y':
		return 'nOpp'
	else:
		return 'sComp'
	
# This function requests and then returns the selected move for the opponent
def getNOppMove(board):
		
	pit = -1
	
	#Manually entering "opponents" pits (human or other computer)
	pitList = [7,8,9,10,11,12]
	while pit not in pitList:
		pit = int(input("Enter your selected pit, 7 - 12 with at least one stone in it: "))
		
		#pit += 7 #!!Note: uncomment if opponent is "giving" pit values #0-5 
		if board[pit] == 0:
			print("Error: selected pit is empty.")
			pit = -1

	return pit 
	
# This function returns a selected move for the computer
def getSCompMove(board):
	
	#create current node
	root = Node(board, 0, None, None) #create current node
	pit = alphaBetaSearch(root)
	print("I selected pit #", pit, " (", pit+7, ")")
	return pit

# This function updates the board with the current players selected move
def updateBoard(move, board):
	
	stones = board[move] #number of stones in hand
	board[move] = 0 #empty out pit

	if move < 6:
		turn = 'sComp'
	else:
		turn = 'nOpp'
	
	while stones > 0:
		move += 1
		if (turn == 'nOpp' and move == 6) or (turn == 'sComp' and move == 13): #skip other player's goal
			move += 1 
		if move >= 14: #circle around
			move = 0		
		board[move] += 1 #deposit stone in next pit
		stones -= 1 #reduce stone in hand count
		if stones == 0 and board[move] == 1: #check and adjust for capture
			board = checkCapture(turn, move, board)
		else:
			board[14] = 0 #computer capture count = 0
			board[15] = 0 #opponent capture count = 0		
	return board

# This function checks if a capture is possible and adjusts the board accordingly	
def checkCapture(turn, move, board):

	capture = [12,11,10,9,8,7,None,5,4,3,2,1,0]
	if (turn == 'sComp' and move >=0 and move < 6): #capture
		capturePit = capture[move]
		stones = board[capturePit]
		board[6] += stones
		board[capturePit] = 0
		board[14] = stones #keep record of number of stones captured
		board[15] = 0
	
	if (turn == 'nOpp' and move > 6 and move < 13): #capture
		capturePit = capture[move]
		stones = board[capturePit]
		board[13] += stones
		board[capturePit] = 0
		board[15] = stones #keep record of number of stones captured
		board[14] = 0
	
	return board	

# This function checks to see if the game board is at the end of the game (one player has no more stones)	
def checkDone(board):
	
	sumNOpp = 0
	for i in range(7, 13):
		sumNOpp += board[i]
	sumSComp = 0
	for i in range(0, 6):
		sumSComp += board[i]
	if sumNOpp == 0 or sumSComp == 0: #one of the players has no more stones in their pits
		return True
	return False

# This function collects remaining stones
def collectStones(board):
	print("Game Over.  Collecting remaining stones.")
	for i in range(7, 13):
		board[13] += board[i]
		board[i] = 0
	for i in range(0, 6):
		board[6] += board[i]
		board[i] = 0
	return board

# This function checks to see which player won the game	
def checkWinner(board):
	
	if (board[13] > board[6]):
		print("Opponent won: ", board[13], " to ", board[6])
	elif(board[6] > board[13]):
		print("Computer won: ", board[6], " to ", board[13])
	else:
		print("It was a tie: ", board[13], " to ", board[6])
		
# This function displays the current game board
def displayBoard(board):
	
	print("\n                              Owari                  \n")
	
	#players side
	print("                            Your side")
	print("          Pit #        ", end = "")
	for i in range (12, 9, -1):
		print( i,  end = "  ")
	for i in range (9, 6, -1):
		print( i,  end = "   ")
	print("\n                   ----------------------------")
	print("          Stones       ", end = "")
	for i in range (12, 6, -1):
		stones = board[i]
		if stones < 10:
			print( board[i], end = "   ")
		else:
			print( board[i], end = "  ")
	print("")
	
	#Goals
	print("Your goal         ", board[13], "                         ", board[6], "  My goal")
	
	#computer's side
	print("          Stones       ", end = "")
	for i in range (0, 6):
		stones = board[i]
		if stones < 10:
			print( board[i], end = "   ")
		else:
			print( board[i], end = "  ")	
	print("\n                   ----------------------------")
	print("          Pit #        ", end = "")
	for i in range (0, 6):
		print( i,  end = "   ")
	print("\n                             My side\n")
	
	
####	excute program	####
if __name__ == '__main__':
	main()