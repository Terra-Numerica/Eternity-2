from board import Board
import tkinter
from PIL import ImageTk
import PIL.Image

path_pieces = "pieces.png"

"""
	Represents each actual Board
"""

class BoardGUI(tkinter.Canvas):
	"""
		the images are stored using a dictionnary, whose key is the code of the piece
	"""
	def __init__(self,parent,text="hello world", **kwargs):
		tkinter.Canvas.__init__(self, parent, **kwargs)
		self.configure(bg="Black")

		self.labels = [ [None for x in range(16)] for y in range(16)]

		
		self.sizePiece = self.winfo_reqwidth()//16
		#print("reqwidth="+str(self.winfo_reqwidth()))		
		#print("sizePiece="+str(self.sizePiece))

	def initializePieces(self, listPieces):
		self.listImgPieces = {}
		for piece in listPieces:
			self.listImgPieces[piece] = self.__getImg(piece)

	

	def putPiece(self, x, y, piece, rotation):		
		xboard = y*self.sizePiece
		yboard = x*self.sizePiece		

		img = ImageTk.PhotoImage(self.listImgPieces[piece].rotate(rotation*90))

		if not self.labels[x][y]:
			self.labels[x][y] = tkinter.Label(self, image=img, bg="Black")
			self.labels[x][y].image = img			
			self.labels[x][y].place(x=xboard+3, y=yboard)
		else:	
			self.labels[x][y].configure(image=img)
			self.labels[x][y].image = img
		#self.update()
  
	

	def removePiece(self, x, y):
		if self.labels[x][y]:
			self.labels[x][y].configure(image=None)
			self.labels[x][y].image = None		
		self.update()
   

	def update(self) -> None:
		tkinter.Tk.update(self)
		

	def __getImg(self, pieceCode):
		pos = [self.__position(pieceCode[i]) for i in range(4)]
		im = PIL.Image.open(path_pieces, 'r')
		
		new = PIL.Image.new("RGB", (256,256))
		rotate = 0
		regionx = 0
		regiony = 0

		pw = 256
		ph = 128

		for i in range(4) :
			(x, y) = pos[i]	
			regionx = 128 if i==1 else 0
			regiony = 128 if i==2 else 0
			region = im.crop((x*pw, y*ph, (x+1)*pw, (y+1)*ph))	
			region = region.rotate(-rotate, expand=1)		
			new.paste(region, (regionx, regiony, regionx+region.width, regiony+region.height), mask=region.split()[3]) 	
			rotate += 90
	
		new = new.resize((self.sizePiece, self.sizePiece), PIL.Image.ANTIALIAS)
		return new

	def __position(self, char):
		if char=='X' :
			return (0,0)

		num =  ord(char) - 64
		x = num % 4
		y = num // 4 
		return (x, y)

