
 
from Rules import ChessRules

class ChessGUI_text:
	def __init__(self):
		self.Rules = ChessRules()
	def Draw(self,board):
		print "    c0   c1   c2   c3   c4   c5   c6   c7 "
		print "  ----------------------------------------"
		for r in range(8):
			print "r"+str(r)+"|",
			for c in range(8):
				if board[r][c] != 'e':
					print  str(board[r][c]), "|",
				else:
					print "   |",
				if c == 7:
					print #to get a new line
			print "  ----------------------------------------"

	def EndGame(self,board):
		self.Draw(board)
	
	def GetPlayerInput(self,board,color):
		fromTuple = self.GetPlayerInput_SquareFrom(board,color)
		toTuple = self.GetPlayerInput_SquareTo(board,color,fromTuple)
		return (fromTuple,toTuple)


	def GetPlayerInput_SquareFrom(self,board,color):
		ch = "?"
		cmd_r = 0
		cmd_c = 0
		while (ch not in board[cmd_r][cmd_c] or self.Rules.GetListOfValidMoves(board,color,(cmd_r,cmd_c))==[]):
			print "Player", color
			cmd_r = int(raw_input("  From row: "))
			cmd_c = int(raw_input("  From col: "))
			if color == "black":
				ch = "b"
			else:
				ch = "w"
			if (board[cmd_r][cmd_c] == 'e'):
				print "  Nothing there!"
			elif (ch not in board[cmd_r][cmd_c]):
				print "  That's not your piece!"
			elif self.Rules.GetListOfValidMoves(board,color,(cmd_r,cmd_c)) == []:
				print "  No valid moves for that piece!"

		return (cmd_r,cmd_c)


	def GetPlayerInput_SquareTo(self,board,color,fromTuple):
		toTuple = ('x','x')
		validMoveList = self.Rules.GetListOfValidMoves(board,color,fromTuple)
		print "List of valid moves for piece at",fromTuple,": ", validMoveList

		while (not toTuple in validMoveList):
			cmd_r = int(raw_input("  To row: "))
			cmd_c = int(raw_input("  To col: "))
			toTuple = (cmd_r,cmd_c)
			if not toTuple in validMoveList:
				print "  Invalid move!"

		return toTuple


	def PrintMessage(self,message):
		print message
		
if __name__ == "__main__":
	from Board import ChessBoard
	
	cb = ChessBoard(0)
	
	gui = ChessGUI_text()
	gui.Draw(cb.GetState())