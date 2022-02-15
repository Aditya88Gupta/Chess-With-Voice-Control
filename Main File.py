
from Board import ChessBoard
from ChessAI import ChessAI_random, ChessAI_defense, ChessAI_offense
from GUI_text import ChessGUI_text
from GUI_pygame import ChessGUI_pygame
from Rules import ChessRules
from optparse import OptionParser
import time
import pygame
import sys
from Tkinter import *


class Game_Setup:

	def __init__(self):
		self.root = Tk()
		self.root.title("Welcome to Voice Chess")
		self.frame = Frame(self.root)
		self.frame.pack()

		self.inst_mess = StringVar()
		Label(self.frame, textvariable=self.inst_mess).grid(row=0)
		self.inst_mess.set("Please enter game options:")

		Label(self.frame, text="Name").grid(row=1, column=1)
		Label(self.frame, text="Type").grid(row=1, column=2)

		Label(self.frame, text="Player 1 (White)").grid(row=2, column=0)
		self.entry_player1Name = Entry(self.frame)
		self.entry_player1Name.grid(row=2, column=1)
		self.entry_player1Name.insert(ANCHOR, "Vishrut")

		self.tk_player1Type = StringVar()
		Radiobutton(self.frame, text="User", variable=self.tk_player1Type, value="human").grid(row=2, column=2)
		Radiobutton(self.frame, text="Computer", variable=self.tk_player1Type, value="randomAI").grid(row=2, column=3)
		self.tk_player1Type.set("human")

		Label(self.frame, text="Player 2 (Black)").grid(row=3, column=0)
		self.entry_player2Name = Entry(self.frame)
		self.entry_player2Name.grid(row=3, column=1)
		self.entry_player2Name.insert(ANCHOR, "Aryan")

		self.tk_player2Type = StringVar()
		Radiobutton(self.frame, text="User", variable=self.tk_player2Type, value="human").grid(row=3, column=2)
		Radiobutton(self.frame, text="Computer", variable=self.tk_player2Type, value="randomAI").grid(row=3, column=3)
		self.tk_player2Type.set("defenseAI")

		button = Button(self.frame, text="Start the Game!", command=self.ok)
		button.grid(row=4, column=1)

	def ok(self):
		self.player1Name = self.entry_player1Name.get()

		self.player1Color = "white"
		self.player1Type = self.tk_player1Type.get()
		self.player2Name = self.entry_player2Name.get()
		self.player2Color = "black"
		self.player2Type = self.tk_player2Type.get()

		if self.player1Name != "" and self.player2Name != "":
			self.frame.destroy()
		else:

			if self.player1Name == "":
				self.entry_player1Name.insert(ANCHOR, "Vishrut")
			if self.player2Name == "":
				self.entry_player2Name.insert(ANCHOR, "Aryan")

	def GetGameSetupParams(self):
		self.root.wait_window(self.frame)
		self.root.destroy()
		return (self.player1Name, self.player1Color, self.player1Type,
				self.player2Name, self.player2Color, self.player2Type)


if __name__ == "__main__":
	demo = Game_Setup()
	x = demo.GetGameSetupParams()


class ChessPlayer:
	def __init__(self, name, color):
		self.name = name
		self.color = color
		self.type = 'human'

	def GetName(self):
		return self.name

	def GetColor(self):
		global temp_Color
		temp_Color = self.color
		return self.color

	def GetType(self):
		return self.type


if __name__ == "__main__":
	p = ChessPlayer("Anuj", "black")




class PythonChessMain:
	def __init__(self,options):
		if options.debug:
			self.Board = ChessBoard(2)
			self.debugMode = True
		else:
			self.Board = ChessBoard(0) # Intial Setup of Chess board
			self.debugMode = False

		self.Rules = ChessRules()
		
	def SetUp(self,options):
		# Intial Information required to start the game
		if self.debugMode:
			player1Name = 'Vishrut'
			player1Type = 'User'
			player1Color = 'white'
			player2Name = 'Aryan'
			player2Type = 'randomAI'
			player2Color = 'black'		
		else:
			GameParams = Game_Setup()
			(player1Name, player1Color, player1Type, player2Name, player2Color, player2Type) = GameParams.GetGameSetupParams()

		self.player = [0,0]
		if player1Type == 'human':
			self.player[0] = ChessPlayer(player1Name,player1Color)
		elif player1Type == 'randomAI':
			self.player[0] = ChessAI_random(player1Name,player1Color)
		elif player1Type == 'defenseAI':
			self.player[0] = ChessAI_defense(player1Name,player1Color)
		elif player1Type == 'offenseAI':
			self.player[0] = ChessAI_offense(player1Name,player1Color)
			
		if player2Type == 'human':
			self.player[1] = ChessPlayer(player2Name,player2Color)
		elif player2Type == 'randomAI':
			self.player[1] = ChessAI_random(player2Name,player2Color)
		elif player2Type == 'defenseAI':
			self.player[1] = ChessAI_defense(player2Name,player2Color)
		elif player2Type == 'offenseAI':
			self.player[1] = ChessAI_offense(player2Name,player2Color)
			
		if 'AI' in self.player[0].GetType() and 'AI' in self.player[1].GetType():
			self.AIvsAI = True
		else:
			self.AIvsAI = False
			
		if options.pauseSeconds > 0:
			self.AIpause = True
			self.AIpauseSeconds = int(options.pauseSeconds)
		else:
			self.AIpause = False
			

		if options.text:
			self.guitype = 'text'
			self.Gui = ChessGUI_text()
		else:
			self.guitype = 'pygame'
			if options.old:
				self.Gui = ChessGUI_pygame(0)
			else:
				self.Gui = ChessGUI_pygame(1)
			
	def MainLoop(self):
		currentPlayerIndex = 0
		turnCount = 0

		while not self.Rules.IsCheckmate(self.Board.GetState(),self.player[currentPlayerIndex].color):

			board = self.Board.GetState()
			currentColor = self.player[currentPlayerIndex].GetColor()



			# To make sure that the first chance is given to White
			if currentColor == 'white':
				turnCount = turnCount + 1

			self.Gui.PrintMessage("")
			baseMsg = "TURN %s - %s (%s)" % (str(turnCount),self.player[currentPlayerIndex].GetName(),currentColor)

			self.Gui.PrintMessage("-----%s-----" % baseMsg)
			self.Gui.Draw(board)

			if self.Rules.IsInCheck(board,currentColor):
				self.Gui.PrintMessage("Warning..."+self.player[currentPlayerIndex].GetName()+" ("+self.player[currentPlayerIndex].GetColor()+") is in check!")
			

			if self.player[currentPlayerIndex].GetType() == 'AI':
				moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor) 
			else:
				moveTuple = self.Gui.GetPlayerInput(board,currentColor)

			moveReport = self.Board.MovePiece(moveTuple)
			self.Gui.PrintMessage(moveReport)

			currentPlayerIndex = (currentPlayerIndex+1)%2

			if self.AIvsAI and self.AIpause:
				time.sleep(self.AIpauseSeconds)
		
		self.Gui.PrintMessage("CHECK MATE!")
		winnerIndex = (currentPlayerIndex+1)%2
		self.Gui.PrintMessage(self.player[winnerIndex].GetName()+" ("+self.player[winnerIndex].GetColor()+") won the game!")
		self.Gui.EndGame(board)
		

parser = OptionParser()
parser.add_option("-d", dest="debug",
				  action="store_true", default=False, help="Enable debug mode (different starting board configuration)")
parser.add_option("-t", dest="text",
				  action="store_true", default=False, help="Use text-based GUI")
parser.add_option("-o", dest="old",
				  action="store_true", default=False, help="Use old graphics in pygame GUI")
parser.add_option("-p", dest="pauseSeconds", metavar="SECONDS",
				  action="store", default=0, help="Sets time to pause between moves in AI vs. AI games (default = 0)")


(options,args) = parser.parse_args()

game = PythonChessMain(options)
game.SetUp(options)
game.MainLoop()


	