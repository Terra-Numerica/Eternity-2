import re
from board import Board
import random
import xml.etree.ElementTree as ET
import time
import tkinter
from datetime import datetime

path_piecesDescriptions = "piecesDescriptions.txt"
#29, 30
seed = random.randint(0, 100)  # the random seed (when shuffling pieces)


class Algo:

    def __init__(self, gui, currBoardGUI, recordBoardGUI, speedSLider):
        print("Initialization...")

        self.gui = gui
        self.speedSlider = speedSLider;
        self.progressive = False
        self.nb_of_loop = 0
        
        # init pieces
        file = open(path_piecesDescriptions, 'r')
        lines = file.readlines()
        file.close()
        self.listPieces = []
        
        self.path_save = ""

        
        id = 0
        for line in lines:
            id += 1
            self.listPieces.append(line.strip())

        # shuffling pieces (random seed)
        # we need to use version 2 of the Mersenne Twister algorithm
        
        # we also need to add a way to keep the best seed somewhere
        # not implemented yet
        random.seed(seed, version=2)
        random.shuffle(self.listPieces)

        self.remainingPieces = self.listPieces.copy()

        self.currBoardGUI = currBoardGUI
        self.recordBoardGUI = recordBoardGUI

        self.initBoards()

        print("done!")

    def initBoards(self):
        self.currentBoard = Board(self, self.currBoardGUI)
        self.recordBoard = Board(self, self.recordBoardGUI)

    def initialize(self, fileName=None):
        if fileName:
            # loading save file
            tree = ET.parse(fileName)
            root = tree.getroot()
            for elem in root.findall("boards"):
                self.currentBoard.fillFromString(elem.find('currentBoard').text)
                self.recordBoard.fillFromString(elem.find('recordBoard').text)
            for elem in root.findall("algo"):
                self.constructStackFromString(elem.find('stack').text)
            for elem in root.findall("stats"):
                self.maxNumCases = int(elem.find('maxNumCases').text)
                self.lastPlacedPiece = int(elem.find('lastPlacedPiece').text)
                self.gui.setPreviousElapsedTime(elem.find('time').text)
            self.numMoves = 0
            listPieces = self.currentBoard.getListPieces()
            for piece in listPieces:
                self.remainingPieces.remove(piece)

            self.gui.updateNumberOfPieces(self.maxNumCases)
            
        else:
            # initializing a fresh board
            self.numMoves = 0
            self.maxNumCases = 0

            firstMoves = self.lookForAvailablePieces(0)

            self.lastPlacedPiece = -1

            self.stack = []
            for (p, r) in firstMoves:
                self.stack.append((p, r, 0))

    def constructStackFromString(self, string):
        # reconstructing the stack from a string in the save file
        self.stack = []
        listStr = string.split(';')
        for elt in listStr:
            eltList = elt.split(",")
            if len(eltList) == 3:
                (p, r, case) = (eltList[0], int(eltList[1]), int(eltList[2]))
                self.stack.append((p, r, case))

    def runStack(self):
        """
			stack stores the last piece found that we need to place. Namely it stores tuples containing:
				- a piece
				- a rotation
				- a case number
		"""
        self.stop = False
        print("starting algo")
        while not self.stop and len(self.stack) > 0:

            self.numMoves += 1
            # getting the last piece found that can be placed
            (piece, rotation, case) = self.stack.pop()
            
            for caseToRemove in range(self.lastPlacedPiece, case - 1, -1):
                # this is the backtracking part
                # removing all the pieces beetwen the last placed piece and the position of the new one
                removedPiece = self.currentBoard.removePiece(caseToRemove)
                self.remainingPieces.append(removedPiece)

            # placing the piece on the board and updating the remaining pieces
            # update the gui
            self.currentBoard.putPiece(case, piece, rotation)    
            self.remainingPieces.remove(piece)
            self.lastPlacedPiece = case
            if case > self.maxNumCases:
                # we have a new record
                self.gui.startRecordTimer();
                self.gui.updateNumberOfPieces(case)
                self.maxNumCases = case
                self.recordBoard.updateEverything(self.currentBoard)

            if case == 255:
                # wow :-) Eternity has passed
                self.currentBoard.print()
                return
            else:
                # looking for the next piece and pushing them on the stack
                case += 1
                listMoves = self.lookForAvailablePieces(case)
                for (p, r) in listMoves:
                    self.stack.append((p, r, case))
                    
                    
            if self.progressive:
                # progressive mode
                val = self.equalToOneEveryTenLoop()
                self.speedSlider.set(self.speedSlider.get()-val)
            
            if (self.speedSlider.get() > 0):
                self.gui.after(self.speedSlider.get()*10, self.currBoardGUI.update())    
            
    def save(self):
        # create the file structure
        
        print("Saving...")
        root = ET.Element('root')

        boards = ET.SubElement(root, "boards")

        currB = ET.SubElement(boards, "currentBoard")
        currB.text = self.currentBoard.toString()
<<<<<<< Updated upstream

        recordB = ET.SubElement(boards, "recordBoard")
        recordB.text = self.recordBoard.toString()

        algo = ET.SubElement(root, "algo")

        stack = ET.SubElement(algo, "stack")
        stack.text = ';'.join([','.join([str(y) for y in x]) for x in self.stack])

        stats = ET.SubElement(root, "stats")

        saveMaxNumCases = ET.SubElement(stats, "maxNumCases")
        saveMaxNumCases.text = str(self.maxNumCases)

        saveLastPlacedPiece = ET.SubElement(stats, "lastPlacedPiece")
        saveLastPlacedPiece.text = str(self.lastPlacedPiece)

        time = ET.SubElement(stats, "time")
        time.text = str(int(self.gui.elapsedTime.total_seconds()))

        # create a new XML file with the results
        mydata = ET.tostring(root)

        if (len(self.path_save) == 0):
            self.path_save = "save-" + datetime.now().strftime("%b-%d-%Y %H:%M:%S") + ".xml"
        myfile = open(self.path_save, "w")
        myfile.write(str(mydata).strip('b\'\''))
=======
>>>>>>> Stashed changes
        
        if (len(currB.text) != 0):
            recordB = ET.SubElement(boards, "recordBoard")
            recordB.text = self.recordBoard.toString()

            algo = ET.SubElement(root, "algo")

            stack = ET.SubElement(algo, "stack")
            stack.text = ';'.join([','.join([str(y) for y in x]) for x in self.stack])

            stats = ET.SubElement(root, "stats")

            saveMaxNumCases = ET.SubElement(stats, "maxNumCases")
            saveMaxNumCases.text = str(self.maxNumCases)

            saveLastPlacedPiece = ET.SubElement(stats, "lastPlacedPiece")
            saveLastPlacedPiece.text = str(self.lastPlacedPiece)

            time = ET.SubElement(stats, "time")
            time.text = str(int(self.gui.elapsedTime.total_seconds()))

            # create a new XML file with the results
            mydata = ET.tostring(root)

            if (len(self.path_save) == 0):
                self.path_save = "Saved-Grids/save-" + datetime.now().strftime("%b-%d-%Y %H:%M:%S") + ".xml"
            myfile = open(self.path_save, "w")
            myfile.write(str(mydata).strip('b\'\''))
            
            print("Progression saved !")
            return

        print("Nothing to Save..")

    def stopAlgorithm(self):
        self.stop = True

    def lookForAvailablePieces(self, caseId):
        # returns a list of tuples (piece, rotation) that can be placed on the given case
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

    def getNumMoves(self):
        # returns the number of moves made since the last call to this function
        saveNum = self.numMoves
        self.numMoves = 0
        return saveNum

    def getCoordinates(self, caseId):
        return (caseId // 16, caseId % 16)
    
    def equalToOneEveryTenLoop(self):
        # to update the speed slider progressively
        self.nb_of_loop += 1
        val = 0 if self.nb_of_loop%10 != 0 else 1
        return val
