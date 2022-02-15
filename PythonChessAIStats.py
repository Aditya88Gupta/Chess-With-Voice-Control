
from __future__ import division # For Conversion of integral divison to float
from Board import ChessBoard
from ChessAI import ChessAI_random, ChessAI_defense, ChessAI_offense
from Rules import ChessRules
import datetime
from optparse import OptionParser
import random

class PythonChessAIStats:
	def __init__(self):
		self.Rules = ChessRules()
		
	def SetUp(self,whiteType,blackType):
		self.player = [0,0]
		if whiteType == "defense":
			self.player[0] = ChessAI_defense("Defense AI - white","white")
		elif whiteType == "offense":
			self.player[0] = ChessAI_offense("Offense AI - white","white")
		else:
			self.player[0] = ChessAI_random("Random AI - white","white")
			
		if blackType == "defense":
			self.player[1] = ChessAI_defense("Defense AI - black","black")
		elif blackType == "offense":
			self.player[1] = ChessAI_offense("Offense AI - black","black")
		else:
			self.player[1] = ChessAI_random("Random AI - black","black")
			
	def Run(self,numRuns,useExternalSeed,seedFileName):
		self.seeds = []
		if useExternalSeed:

			seedFile = open(seedFileName)
			for line in seedFile:
				if line != "":
					self.seeds.append(int(line))
	
		self.results = []
		for r in range(numRuns):
			print ""
			#load seed
			if r < len(self.seeds):
				random.seed(self.seeds[r])
				print "Using seed %d" % self.seeds[r]
			else:
				random.seed()
			
			print "Playing Match #%d" % (r+1),
			self.results.append(self.PlaySingleMatch())
	
	def PlaySingleMatch(self):
		self.Board = ChessBoard(0)
		currentPlayerIndex = 0
		turnCount = 0
		
		while not self.Rules.IsCheckmate(self.Board.GetState(),self.player[currentPlayerIndex].color):
			board = self.Board.GetState()
			currentColor = self.player[currentPlayerIndex].GetColor()

			if currentColor == 'white':
				turnCount = turnCount + 1
				if turnCount % 10 == 0:
					print " %d" %turnCount,
				if turnCount > 200:
					return (turnCount,-1)
			moveTuple = self.player[currentPlayerIndex].GetMove(self.Board.GetState(), currentColor) 
			moveReport = self.Board.MovePiece(moveTuple)

			currentPlayerIndex = (currentPlayerIndex+1)%2
		
		winnerIndex = (currentPlayerIndex+1)%2
			
		return (turnCount,winnerIndex)
		
	def PrintResults(self,writeToFile,outFileName,useExternalSeed,seedFileName):
		numRuns = len(self.results)
		whiteWins = 0
		whiteLosses = 0
		whiteTurnsToWin = 0
		whiteTurnsToLoss = 0
		blackWins = 0
		blackLosses = 0
		blackTurnsToWin = 0
		blackTurnsToLoss = 0
		draws = 0
		

		for m in self.results:
			turns = m[0]
			winner = m[1]
			if winner == 0:
				whiteWins = whiteWins + 1
				blackLosses = blackLosses + 1
				whiteTurnsToWin = whiteTurnsToWin + turns
				blackTurnsToLoss = blackTurnsToLoss + turns
			elif winner == 1:
				blackWins = blackWins + 1
				whiteLosses = whiteLosses + 1
				blackTurnsToWin = blackTurnsToWin + turns
				whiteTurnsToLoss = whiteTurnsToLoss + turns
			else:
				draws = draws + 1
		
		whiteWinPct = 100 * whiteWins / numRuns
		whiteAveTurnsToWin = whiteTurnsToWin / numRuns
		blackWinPct = 100 * blackWins / numRuns
		blackAveTurnsToWin = blackTurnsToWin / numRuns
		drawPct = 100 * draws / numRuns
		time = str(datetime.datetime.now())
		print ""
		print "Final results: "
		print "  "+time
		print "  %d runs" % numRuns
		if useExternalSeed:
			print "  %d random seeds used from %s" % (len(self.seeds),seedFileName)
		print "  %s win pct = %0.2f" %(self.player[0].GetName(),whiteWinPct)
		print "  %s average number of turns to win = %0.2f" %(self.player[0].GetName(),whiteAveTurnsToWin)
		print "  %s win pct = %0.2f" %(self.player[1].GetName(),blackWinPct)
		print "  %s average number of turns to win = %0.2f" %(self.player[1].GetName(),blackAveTurnsToWin)
		print "  Draw pct = %0.2f" % drawPct
		
		if writeToFile:
			f = open(outFileName,'a')
			f.write("\n")
			f.write(time+"\n")
			f.write(str("%d runs" % numRuns)+"\n")
			if useExternalSeed:
				f.write(str("%d random seeds used from %s" % (len(self.seeds),seedFileName))+"\n")
			f.write(str("%s win pct = %0.2f" %(self.player[0].GetName(),whiteWinPct))+"\n")
			f.write(str("%s average number of turns to win = %0.2f" %(self.player[0].GetName(),whiteAveTurnsToWin))+"\n")
			f.write(str("%s win pct = %0.2f" %(self.player[1].GetName(),blackWinPct))+"\n")
			f.write(str("%s average number of turns to win = %0.2f" %(self.player[1].GetName(),blackAveTurnsToWin))+"\n")
			f.write(str("Draw pct = %0.2f" % drawPct)+"\n")
			

parser = OptionParser()
parser.add_option("-w", "--white", dest="whiteType",
				  help="Set white player AI('random','defense')", metavar="AITYPE")
parser.add_option("-b", "--black", dest="blackType",
				  help="Set black player AI('random','defense')", metavar="AITYPE")
parser.add_option("-r", "--runs", dest="numRuns",
				  help="Set number of runs", metavar="NUMRUNS")
parser.add_option("-s", "--seed", dest="seedFileName",
				  help="Optional seed input file", metavar="SEEDFILE")
parser.add_option("-o", "--out", dest="outFileName",
				  help="Optional results output file", metavar="OUTFILE")
(options,args) = parser.parse_args()

if options.whiteType:
	whiteType = options.whiteType
else:
	whiteType = "defense"
	
if options.blackType:
	blackType = options.blackType
else:
	blackType = "random"
	
if options.numRuns:
	numRuns = int(options.numRuns)
else:
	numRuns = 5
	
if options.seedFileName:
	useExternalSeed = True
	seedFileName = options.seedFileName
else:
	useExternalSeed = False
	seedFileName = ""
	
if options.outFileName:
	writeToFile = True
	outFileName = options.outFileName
else:
	writeToFile = False
	outFileName = ""


stats = PythonChessAIStats()
stats.SetUp(whiteType,blackType)
stats.Run(numRuns,useExternalSeed,seedFileName)
stats.PrintResults(writeToFile,outFileName,useExternalSeed,seedFileName)


	