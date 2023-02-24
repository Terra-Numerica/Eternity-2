import xml.etree.ElementTree as ET
from tkinter import filedialog
import b
import random

path_piecesDescriptions = "piecesDescriptions.txt"


class algo:
    def __init__(self):
        
        file = open(path_piecesDescriptions, 'r')
        lines = file.readlines()
        file.close()
        self.listPieces = []        
        self.path_save = ""

        self.numMoves =0

        id = 0
        for line in lines:
            id += 1
            self.listPieces.append(line.strip())

        self.remainingPieces = self.listPieces.copy()
        
        fileName = filedialog.askopenfilename()
        self.currentBoard = b.Board(self)
        self.initialize(fileName)
        
    def getCoordinates(self, caseId):
        return (caseId // 16, caseId % 16)
    
    def initialize(self, fileName):
        # loading save file
        tree = ET.parse(fileName)
        root = tree.getroot()
        for elem in root.findall("boards"):
            self.currentBoard.fillFromString(elem.find('currentBoard').text)
        for elem in root.findall("stats"):
            self.maxNumCases = int(elem.find('maxNumCases').text)
            self.lastPlacedPiece = int(elem.find('lastPlacedPiece').text) 
        
        listPieces = self.currentBoard.getListPieces()
        for piece in listPieces:
            self.remainingPieces.remove(piece)

            
            
    def runAlgo(self):    
        self.listOfBoards = []
        
        for seed in range(3):
            random.seed(seed, version=2)
            random.shuffle(self.remainingPieces)

            caseID = self.lastPlacedPiece + 1
            
            while self.remainingPieces:
                AvailablePieces = self.lookForAvailablePieces(caseID)
                if not AvailablePieces:
                    piece = self.remainingPieces.pop()
                    correct = 1
                    self.currentBoard.putPiece(caseID, piece, 0, correct)
                    self.numMoves += 1
                    caseID += 1
                else:
                    print(AvailablePieces)    
                
                for piece in AvailablePieces:
                    (x, y) = self.getCoordinates(caseID)
                    constraints = self.currentBoard.getConstraints(x, y)
                    correct = 0 if self.match(piece[0], constraints) != -1 else 1
                    if correct == 0:
                        self.currentBoard.putPiece(caseID, piece[0], piece[1], correct)
                        caseID += 1
                        self.remainingPieces.remove(piece[0])
                        self.numMoves +=1
                    
            
            self.listOfBoards.append(self.currentBoard.placedPieces.copy())
            
    
    def lookForAvailablePieces(self, caseId):
        (x, y) = self.getCoordinates(caseId)
        constraints = self.currentBoard.getConstraints(x, y)
        #print("constraints of case "+str(caseId)+" : "+constraints)
        availablePieces = []
        for p in self.remainingPieces:
            #print("pieces -> " + p + " for constraints --> " + constraints)
            if self.numMoves == 0:
                rotation = self.match(p, constraints)
                if rotation > 0:
                    availablePieces.append((p, rotation))
            else:
                # print("pieces -> " + p + " for constraints --> " + constraints)    
                if constraints[0] in p:
                    rotation = self.match(p, constraints)
                    if rotation > 0:
                        availablePieces.append((p, rotation))
        return availablePieces
    
    
    """
	tests whether a given piece matches with some constraints
	outputs the correct rotation if it matches, or -1 otherwise
	piece is a code
	constraints are assumed to be given as a code, starting from the top, a star * meaning there is no constraint
	ex: "B**X" means there is a constraint for the top and the left edges only
	"""        
                 
    def match(self, piece, constraints):   
        for i in range(4):
            firsti = i
            j = 0
            while j < 4 and ((constraints[j] == '*' and piece[i] != 'X') or piece[i] == constraints[j]):
                j += 1
                i = (i + 1) % 4
            if j == 4:
                return firsti
        return -1
    
        
        
algo = algo()

        
# fonction de cout pour renvoyant le nombre d'erreurs de placement dans le plateau
def cost(board):
    errors = 0
    for row in board:
        for (_, _, correct) in row:
            if correct == 1:
                errors += 1
        
    return errors
        
        
algo.runAlgo()
for board in algo.listOfBoards:
     print(cost(board))
