from operator import length_hint
import tkinter
from tkinter import ttk
from boardGUI import BoardGUI
from tkinter import HORIZONTAL, Button, Scale
from tkinter import Label
from tkinter import filedialog
from algo import Algo
import time
from datetime import datetime, timedelta
from PIL import ImageTk, Image
from TIpWindow import *


class GUI(tkinter.Tk):

    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.configure(background="#e3d5ca")
        
        self.protocol("WM_DELETE_WINDOW", self.onClosing)

        self.title("Eternity II backtracking visualization")

        self.appHeight = int(0.75 * self.winfo_screenheight())
        self.appWidth = int(0.75 * self.winfo_screenwidth())
        self.minsize(self.appWidth+170, self.appHeight+50)

        self.geometry(str(self.appWidth) + "x" + str(self.appHeight))

        # ----- #
        # speedslider to slow down the update of the gui
        self.speedSlider = Scale(self,
                                 from_=0.0,
                                 to=20.0,
                                 length=400,
                                 cursor="hand1",
                                 orient=HORIZONTAL,
                                 activebackground="blue"
                                 )
        self.speedSlider.grid(row=5, column=0)
        self.speedSlider.configure(bg="#e3d5ca", fg= "#000000")
        CreateToolTip(self.speedSlider, text="Use the slider to reduce execution speed")
        
        # ----- #

        titleCurrBoard = Label(self, text="Current board")
        titleCurrBoard.configure(bg="#e3d5ca", fg= "#000000")
        titleCurrBoard.grid(row=1, column=0)

        titleBest = Label(self, text="Best solution found")
        titleBest.configure(bg="#e3d5ca", fg= "#000000")
        titleBest.grid(row=1, column=2)

        self.boardSize = int(0.8 * self.appHeight)

        self.currBoard = BoardGUI(self, width=self.boardSize + 8, height=self.boardSize + 1)
        self.currBoard.grid(row=3, column=0)
        
        self.recordBoard = BoardGUI(self, width=self.boardSize + 8, height=self.boardSize + 1)
        self.recordBoard.grid(row=3, column=2)
        #CreateToolTip(self.recordBoard, text="This is showing")

        self.startButton = Button(self, text="Start", command=self.__startClick)
        self.startButton.grid(row=0, column=1)
        
        self.progressiveStartButton = Button(self, text="Progressive Start", command=self.__progressiveStartClick)
        self.progressiveStartButton.grid(row=2, column=1)

        # button to stop the algorythm and timer
        self.stopButton = Button(self, text="Stop", command=self.__stopClick)
        self.stopButton.grid(row=1, column=1)
        
        self.__configureButtonStyle()

        self.timerIsRunning = False

        self.elapsedTime = timedelta()
        self.timer = Label(self, text="Elapsed time: " + str(self.elapsedTime))
        self.timer.configure(bg="#e3d5ca", fg= "#000000")
        self.timer.grid(row=2, column=0)
        
        self.recordTimer = Label(self, text="Elapsed time since last solution: " + str(self.elapsedTime))
        self.recordTimer.configure(bg="#e3d5ca", fg= "#000000")
        self.recordTimer.grid(row = 2, column= 2)

        self.numberPieces = Label(self, text="Number of pieces: 0/256")
        self.numberPieces.configure(bg="#e3d5ca", fg= "#000000")
        self.numberPieces.grid(row=4, column=2)

        self.movesPerSec = Label(self, text="Number of moves per second: 0")
        self.movesPerSec.configure(bg="#e3d5ca", fg= "#000000")
        self.movesPerSec.grid(row=4, column=0)

        self.algo = Algo(self, self.currBoard, self.recordBoard, self.speedSlider)

        # open a save file to load previous state
        fileName = filedialog.askopenfilename()
        self.algo.initialize(fileName)
        
        
    def startRecordTimer(self):
        now = datetime.now()
        self.virtualStartDateForRecordTimer = now - timedelta()
        self.updateRecordTimer()
    

    def updateRecordTimer(self):
        
        if self.timerIsRunning:
            now = datetime.today()
            #print((now - self.virtualStartDateForRecordTimer).total_seconds())
            time = str(now - self.virtualStartDateForRecordTimer).split(".")[0]
            #print(type(time))
            self.recordTimer.configure(text="Elapsed time since last solution: "+time)
            self.after(1000, self.updateRecordTimer)
         

    def setPreviousElapsedTime(self, totalSeconds):
        self.elapsedTime = timedelta(seconds=int(totalSeconds))
        self.timer.configure(text="Elapsed time: " + str(self.elapsedTime))

    def __startTimer(self):
        self.timerIsRunning = True
        now = datetime.today()
        self.virtualStartDate = now - self.elapsedTime
        self.__updateTimer()
        self.__updateMovesPerSec()

    def __stopTimer(self):
        self.timerIsRunning = False

    def __updateTimer(self):
        if self.timerIsRunning:
            now = datetime.today()
            self.elapsedTime = now - self.virtualStartDate
            self.timer.configure(text="Elapsed time: " + str(self.elapsedTime).split(".")[0])
            self.after(1000, self.__updateTimer)

    def updateNumberOfPieces(self, nb):
        self.numberPieces.configure(text="Number of pieces: " + str(nb) + "/256")

    def __startClick(self):
        self.timerIsRunning = True
        self.startButton['state'] = "disabled"
        self.progressiveStartButton['state'] = "disabled"
        self.stopButton['state'] = "normal"
        self.__startTimer()
        self.algo.runStack()

    def __progressiveStartClick(self):
        self.timerIsRunning = True
        self.startButton['state'] = "disabled"
        self.progressiveStartButton['state'] = "disabled"
        self.stopButton['state'] = "normal"
        self.__startTimer()
        self.speedSlider.set(20.00);
        self.algo.progressive = True
        self.algo.runStack()
    
    def __stopClick(self):
        self.timerIsRunning = False
        self.algo.progressive = False
        self.stopButton['state'] = "disabled"
        self.startButton['state'] = "normal"
        self.progressiveStartButton['state'] = "normal"
        self.__stopTimer()
        self.algo.stopAlgorithm()
        self.algo.save()

    def __updateMovesPerSec(self):
        intervalSec = 3
        numMoves = self.algo.getNumMoves()
        res = numMoves / intervalSec
        self.movesPerSec.configure(text="Number of moves per second: " + "{:.2f}".format(res))
        self.after(intervalSec * 1000, self.__updateMovesPerSec)
        
    def __configureButtonStyle(self):
        # higlightbackround is for Macos
        
        self.stopButton.configure(bg="#e3d5ca",
                                  fg= "#bc6c25",
                                  highlightbackground="#e3d5ca",
                                  disabledforeground="#bc6c25")
        
        self.startButton.configure(bg="#e3d5ca",
                                   fg= "#bc6c25",
                                   highlightbackground="#e3d5ca",
                                   disabledforeground="#bc6c25")
        self.progressiveStartButton.configure(bg="#e3d5ca",
                                              fg= "#bc6c25",
                                              highlightbackground="#e3d5ca",
                                              disabledforeground="#bc6c25")
           

    def onClosing(self):
        self.algo.stopAlgorithm()
        self.after(500, self.saveAndQuit)

    def saveAndQuit(self):
        self.algo.save()
        self.destroy()
