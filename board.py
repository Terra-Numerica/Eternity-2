

class Board():

	def __init__(self, algo, boardGUI, init=True):
		self.algo = algo
		self.placedPieces = [ [None for x in range(16)] for y in range(16)]
		self.boardGUI = boardGUI
		if init:
			self.boardGUI.initializePieces(algo.listPieces)
		
	def copy(self):
		newb = Board(self.algo, self.boardGUI, False)
		for x in range(16):
			for y in range(16):
				newb.placedPieces[x][y] = self.placedPieces[x][y]
		return newb

	def putPiece(self, caseId, piece, rotation):
		(x,y) = self.algo.getCoordinates(caseId)
		self.placedPieces[x][y] = (piece, rotation)
		self.boardGUI.putPiece(x, y, piece, rotation)

	def removePiece(self, caseId):
		(x, y) = self.algo.getCoordinates(caseId)
		prevPiece = self.placedPieces[x][y]
		self.placedPieces[x][y] = None
		self.boardGUI.removePiece(x, y)
		if prevPiece:
			return prevPiece[0]
	
	def updateEverything(self, board):
		case = 0
		stop = False
		while not stop:
			(x, y) = self.algo.getCoordinates(case)
			if board.placedPieces[x][y]:
				self.removePiece(case)
				self.putPiece(case, board.placedPieces[x][y][0], board.placedPieces[x][y][1])
			else:
				stop = True
			case += 1

	def getConstraints(self, x, y):
		top = 'X' if x==0 else self.getEdge(x-1,y, 2)
		right = 'X' if y==15 else self.getEdge(x, y+1, 3)
		bottom = 'X' if x==15 else self.getEdge(x+1, y, 0)
		left = 'X' if y==0 else self.getEdge(x, y-1, 1)
		return top+right+bottom+left

	#sides : 0=top, 1=left, 2=bottom, 3=right
	def getEdge(self, x, y, side):
		if self.placedPieces[x][y]:
			return self.placedPieces[x][y][0][(side+self.placedPieces[x][y][1])%4]
		else:
			return '*'

	def getListPieces(self):
		listPieces = []
		for x in range(16):
			for y in range(16):
				if self.placedPieces[x][y]:
					listPieces.append(self.placedPieces[x][y][0])
		return listPieces

	def fillFromString(self, string):		
		splittedString = list(string.split(" "))		
		for i in range(len(splittedString)):
			placement = list(splittedString[i].split(";"))
			if len(placement) == 2:
				(p, r) = (placement[0], int(placement[1]))
				(x,y) = self.algo.getCoordinates(i)
				self.placedPieces[x][y] = (p, r)
				self.boardGUI.putPiece(x, y, p, r)
			
		

	def toString(self):
		s = ""
		for x in range(16):
			for y in range(16):
				if self.placedPieces[x][y] :
					s += self.placedPieces[x][y][0]+";"+str(self.placedPieces[x][y][1])+" "
		return s

	
	def print(self):
		print(self.toString())


