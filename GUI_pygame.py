import pygame
import os
import sys
from pygame.locals import *
from Rules import ChessRules
from ScrollingTextBox import ScrollingTextBox
from Board import ChessBoard
from VoiceRecognition import SpeechRecognition

class ChessGUI_pygame:
	def __init__(self,graphicStyle=1):
		os.environ['SDL_VIDEO_CENTERED'] = '1' # For centering the pop up window
		self.Rules = ChessRules()
		pygame.init()
		pygame.display.init()
		self.screen = pygame.display.set_mode((850,500))
		self.boardStart_x = 50
		self.boardStart_y = 50
		pygame.display.set_caption('Chess With Voice Control')

		self.textBox = ScrollingTextBox(self.screen,525,825,50,450)
		self.LoadImages(graphicStyle)
		self.fontDefault = pygame.font.Font( None, 20 )
		self.speech =SpeechRecognition()
		
		

	def LoadImages(self,graphicStyle):
		if graphicStyle == 0:
			self.square_size = 50 #Images must be 50 x 50 pixels
			self.white_square = pygame.image.load(os.path.join("images","white_square.png")).convert()
			self.brown_square = pygame.image.load(os.path.join("images","brown_square.png")).convert()
			self.cyan_square = pygame.image.load(os.path.join("images","cyan_square.png")).convert()
			self.black_pawn = pygame.image.load(os.path.join("images","blackPawn.png")) 
			self.black_rook = pygame.image.load(os.path.join("images","blackRook.png"))
			self.black_knight = pygame.image.load(os.path.join("images","blackKnight.png"))
			self.black_bishop = pygame.image.load(os.path.join("images","blackBishop.png"))
			self.black_king = pygame.image.load(os.path.join("images","blackKing.png"))
			self.black_queen = pygame.image.load(os.path.join("images","blackQueen.png"))
			self.white_pawn = pygame.image.load(os.path.join("images","whitePawn.png"))
			self.white_rook = pygame.image.load(os.path.join("images","whiteRook.png"))
			self.white_knight = pygame.image.load(os.path.join("images","whiteKnight.png"))
			self.white_bishop = pygame.image.load(os.path.join("images","whiteBishop.png"))
			self.white_king = pygame.image.load(os.path.join("images","whiteKing.png"))
			self.white_queen = pygame.image.load(os.path.join("images","whiteQueen.png"))
		elif graphicStyle == 1:
			self.square_size = 50
			self.white_square = pygame.image.load(os.path.join("images","white_square.png")).convert()
			self.brown_square = pygame.image.load(os.path.join("images","brown_square.png")).convert()
			self.cyan_square = pygame.image.load(os.path.join("images","cyan_square.png")).convert()
			
			self.black_pawn = pygame.image.load(os.path.join("images","Chess_tile_pd.png")).convert()
			self.black_pawn = pygame.transform.scale(self.black_pawn, (self.square_size,self.square_size))
			self.black_rook = pygame.image.load(os.path.join("images","Chess_tile_rd.png")).convert()
			self.black_rook = pygame.transform.scale(self.black_rook, (self.square_size,self.square_size))
			self.black_knight = pygame.image.load(os.path.join("images","Chess_tile_nd.png")).convert()
			self.black_knight = pygame.transform.scale(self.black_knight, (self.square_size,self.square_size))
			self.black_bishop = pygame.image.load(os.path.join("images","Chess_tile_bd.png")).convert()
			self.black_bishop = pygame.transform.scale(self.black_bishop, (self.square_size,self.square_size))
			self.black_king = pygame.image.load(os.path.join("images","Chess_tile_kd.png")).convert()
			self.black_king = pygame.transform.scale(self.black_king, (self.square_size,self.square_size))
			self.black_queen = pygame.image.load(os.path.join("images","Chess_tile_qd.png")).convert()
			self.black_queen = pygame.transform.scale(self.black_queen, (self.square_size,self.square_size))

			self.white_pawn = pygame.image.load(os.path.join("images","Chess_tile_pl.png")).convert()
			self.white_pawn = pygame.transform.scale(self.white_pawn, (self.square_size,self.square_size))
			self.white_rook = pygame.image.load(os.path.join("images","Chess_tile_rl.png")).convert()
			self.white_rook = pygame.transform.scale(self.white_rook, (self.square_size,self.square_size))
			self.white_knight = pygame.image.load(os.path.join("images","Chess_tile_nl.png")).convert()
			self.white_knight = pygame.transform.scale(self.white_knight, (self.square_size,self.square_size))
			self.white_bishop = pygame.image.load(os.path.join("images","Chess_tile_bl.png")).convert()
			self.white_bishop = pygame.transform.scale(self.white_bishop, (self.square_size,self.square_size))
			self.white_king = pygame.image.load(os.path.join("images","Chess_tile_kl.png")).convert()
			self.white_king = pygame.transform.scale(self.white_king, (self.square_size,self.square_size))
			self.white_queen = pygame.image.load(os.path.join("images","Chess_tile_ql.png")).convert()
			self.white_queen = pygame.transform.scale(self.white_queen, (self.square_size,self.square_size))


	def PrintMessage(self,message):

		self.textBox.Add(message)
		self.textBox.Draw()
		
	def ConvertToScreenCoords(self,chessSquareTuple):

		(row,col) = chessSquareTuple
		screenX = self.boardStart_x + col*self.square_size
		screenY = self.boardStart_y + row*self.square_size
		return (screenX,screenY)
		
	def ConvertToChessCoords(self,screenPositionTuple):
		(X,Y) = screenPositionTuple
		row = (Y-self.boardStart_y) / self.square_size
		col = (X-self.boardStart_x) / self.square_size
		return (row,col)
		
		
	def Draw(self,board,highlightSquares=[]):
		self.screen.fill((0,0,0))
		self.textBox.Draw()
		boardSize = len(board)

		#drawing empty board
		current_square = 0
		for r in range(boardSize):
			for c in range(boardSize):
				(screenX,screenY) = self.ConvertToScreenCoords((r,c))
				if current_square:
					self.screen.blit(self.brown_square,(screenX,screenY))
					current_square = (current_square+1)%2
				else:
					self.screen.blit(self.white_square,(screenX,screenY))
					current_square = (current_square+1)%2

			current_square = (current_square+1)%2


		chessboard_obj = ChessBoard(0)
		color = (255,255,255)#white
		antialias = 1

		# displaying the brown square at the top left corner
		speechSquare = self.screen.blit(self.brown_square, (0, 0))
		

		for c in range(boardSize):
			for r in [-1,boardSize]:
				(screenX,screenY) = self.ConvertToScreenCoords((r,c))
				screenX = screenX + self.square_size/2
				screenY = screenY + self.square_size/2
				notation = chessboard_obj.ConvertToAlgebraicNotation_col(c)
				renderedLine = self.fontDefault.render(notation,antialias,color)
				self.screen.blit(renderedLine,(screenX,screenY))
		

		for r in range(boardSize):
			for c in [-1,boardSize]:
				(screenX,screenY) = self.ConvertToScreenCoords((r,c))
				screenX = screenX + self.square_size/2
				screenY = screenY + self.square_size/2
				notation = chessboard_obj.ConvertToAlgebraicNotation_row(r)
				renderedLine = self.fontDefault.render(notation,antialias,color)
				self.screen.blit(renderedLine,(screenX,screenY))
				
		#highlighting squares
		for square in highlightSquares:
			(screenX,screenY) = self.ConvertToScreenCoords(square)
			self.screen.blit(self.cyan_square,(screenX,screenY))
		
		# Placing Pieces at their respective position
		for r in range(boardSize):
			for c in range(boardSize):
				(screenX,screenY) = self.ConvertToScreenCoords((r,c))
				if board[r][c] == 'bP':
					self.screen.blit(self.black_pawn,(screenX,screenY))
				if board[r][c] == 'bR':
					self.screen.blit(self.black_rook,(screenX,screenY))
				if board[r][c] == 'bT':
					self.screen.blit(self.black_knight,(screenX,screenY))
				if board[r][c] == 'bB':
					self.screen.blit(self.black_bishop,(screenX,screenY))
				if board[r][c] == 'bQ':
					self.screen.blit(self.black_queen,(screenX,screenY))
				if board[r][c] == 'bK':
					self.screen.blit(self.black_king,(screenX,screenY))
				if (board[r][c] == 'wP1') | (board[r][c] == 'wP2') | (board[r][c] == 'wP3') | (board[r][c] == 'wP4') | (board[r][c] == 'wP5') | (board[r][c] == 'wP6') | (board[r][c] == 'wP7') | (board[r][c] == 'wP8'):
					self.screen.blit(self.white_pawn,(screenX,screenY))
				if (board[r][c] == 'wR1') | (board[r][c] == 'wR2'):
					self.screen.blit(self.white_rook,(screenX,screenY))
				if (board[r][c] == 'wT1') | (board[r][c] == 'wT2'):
					self.screen.blit(self.white_knight,(screenX,screenY))
				if (board[r][c] == 'wB1') | (board[r][c] == 'wB2'):
					self.screen.blit(self.white_bishop,(screenX,screenY))
				if board[r][c] == 'wQ':
					self.screen.blit(self.white_queen,(screenX,screenY))
				if board[r][c] == 'wK':
					self.screen.blit(self.white_king,(screenX,screenY))
			
		pygame.display.flip()

	def EndGame(self,board):
		self.PrintMessage("Press any key to exit.")
		self.Draw(board)  # Board after every move
		pygame.event.set_blocked(MOUSEMOTION)
		while 1:
			e = pygame.event.wait()
			if e.type is KEYDOWN:
				pygame.quit()
				sys.exit(0)
			if e.type is QUIT:
				pygame.quit()
				sys.exit(0)

	def GetPlayerInput(self,board,currentColor):

		fromSquareChosen = 0
		toSquareChosen = 0
		while not fromSquareChosen or not toSquareChosen:
			squareClicked = []
			pygame.event.set_blocked(MOUSEMOTION)
			e = pygame.event.wait()
			if e.type is KEYDOWN:
				if e.key is K_ESCAPE:
					fromSquareChosen = 0
					fromTuple = []
			if e.type is MOUSEBUTTONDOWN:
				(mouseX,mouseY) = pygame.mouse.get_pos()
				squareClicked = self.ConvertToChessCoords((mouseX,mouseY))
				print(mouseX,mouseY)
				if (mouseX < 50) & (mouseY < 50):
					speechText = self.speech.Speech()
					self.PrintMessage("You said: " + speechText)
					entityList = self.speech.LUIS_api(speechText)
					if entityList[0] == 'select':
						squareClicked = self.speech.findPieceLocation(entityList, board)
					elif entityList[0] == 'move':
						squareClicked = self.speech.moveToLocation(entityList, board)
				if squareClicked[0]<0 or squareClicked[0]>7 or squareClicked[1]<0 or squareClicked[1]>7:
					squareClicked = []
			if e.type is QUIT:
				pygame.quit()
				sys.exit(0)
			
			if not fromSquareChosen and not toSquareChosen:
				self.Draw(board)
				if squareClicked != []:
					(r,c) = squareClicked
					if currentColor == 'black' and 'b' in board[r][c]:
						if len(self.Rules.GetListOfValidMoves(board,currentColor,squareClicked))>0:
							fromSquareChosen = 1
							fromTuple = squareClicked
					elif currentColor == 'white' and 'w' in board[r][c]:						
						if len(self.Rules.GetListOfValidMoves(board,currentColor,squareClicked))>0:
							fromSquareChosen = 1
							fromTuple = squareClicked
						
			elif fromSquareChosen and not toSquareChosen:
				possibleDestinations = self.Rules.GetListOfValidMoves(board,currentColor,fromTuple)
				self.Draw(board,possibleDestinations)
				if squareClicked != []:
					(r,c) = squareClicked
					if squareClicked in possibleDestinations:
						toSquareChosen = 1
						toTuple = squareClicked
					elif currentColor == 'black' and 'b' in board[r][c]:
						if squareClicked == fromTuple:
							fromSquareChosen = 0
						elif len(self.Rules.GetListOfValidMoves(board,currentColor,squareClicked))>0:
							fromSquareChosen = 1
							fromTuple = squareClicked
						else:
							fromSquareChosen = 0
					elif currentColor == 'white' and 'w' in board[r][c]:
						if squareClicked == fromTuple:
							fromSquareChosen = 0
						elif len(self.Rules.GetListOfValidMoves(board,currentColor,squareClicked))>0:
							fromSquareChosen = 1
							fromTuple = squareClicked
						else:
							fromSquareChosen = 0
					else:
						fromSquareChosen = 0

		return (fromTuple,toTuple)

	def GetClickedSquare(self,mouseX,mouseY):
		# Testing Function
		print "User clicked screen position x =",mouseX,"y =",mouseY
		(row,col) = self.ConvertToChessCoords((mouseX,mouseY))
		if col < 8 and col >= 0 and row < 8 and row >= 0:
			print "  Chess board units row =",row,"col =",col

	def TestRoutine(self):
		pygame.event.set_blocked(MOUSEMOTION)
		while 1:
			e = pygame.event.wait()
			if e.type is QUIT:
				return
			if e.type is KEYDOWN:
				if e.key is K_ESCAPE:
					pygame.quit()
					return
			if e.type is MOUSEBUTTONDOWN:
				(mouseX,mouseY) = pygame.mouse.get_pos()
				self.GetClickedSquare(mouseX,mouseY)
					
			


if __name__ == "__main__":

	testBoard = [['bR','bT','bB','bQ','bK','bB','bT','bR'],\
				 ['bP','bP','bP','bP','bP','bP','bP','bP'],\
				 ['e','e','e','e','e','e','e','e'],\
				 ['e','e','e','e','e','e','e','e'],\
				 ['e','e','e','e','e','e','e','e'],\
				 ['e','e','e','e','e','e','e','e'],\
				 ['wP','wP','wP','wP','wP','wP','wP','wP'],\
				 ['wR','wT','wB','wQ','wK','wB','wT','wR']]
				 
	validSquares = [(5,2),(1,1),(1,5),(7,6)]

	game = ChessGUI_pygame()
	game.Draw(testBoard,validSquares)
	game.TestRoutine()