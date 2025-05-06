import random 
import math
from time import sleep
import copy
import os
import csv

# machine learning stuff
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Input
from tensorflow.keras.optimizers import Adam

class Connect4Game:
    
    # --- attributes ---
    board = []
    columnTokenCounter = []
    length = 0
    hight = 0 
    availablePlayers = ["Human", "Random", "Smart", "Min-Max", "Machine Learning"]
    
    # --- methods ---
    
    def __init__(self, length = 7, hight = 6):
        self.length = length
        self.hight = hight
        self.MLModelPath = "Models\\NeuaralNetworkLR_Connect4.h5"
        self.gamesStorePath = "Data\\games.csv"
    # ---file methods---
    def getLastID(self, gamesFilePath):
        if not os.path.exists(gamesFilePath):
            return 0 # so first id is 1  

        with open(gamesFilePath, "r") as f:
            reader = list(csv.reader(f))
            if len(reader) < 2:  # Only header or empty
                return 0 # so first id is 1 
            lastRow = reader[-1]
            return int(lastRow[0])  # gameID
    
    def startGame(self):
        # creating/ resetting board
        self.resetBoard()
        
        # choosing players 
        self.players = [] # used to alternate between players in while loop 
        # choose player 1
        self.player1 = self.choosePlayer(1)
        self.players.append(self.player1)
        # choose player 2 
        self.player1 = self.choosePlayer(2)
        self.players.append(self.player1)
        
        # start the game
        print("---- Connect 4 Game! ----")
        moves = []
        endState = None
        playerWon = False
        round = 1
        while(playerWon != True and round < self.length * self.hight): # second condition is to check is the board is not full
            print(f" ---- Player { 1 if round % 2 == 1 else 2}'s Move ----")
            player = self.players[(round%2)-1]
            self.printBoard()
            chosenCol = player.makeMove()
            moves.append(chosenCol) # not storing player symbol as it can be worked out by move count
            playerWon = self.isWinner(player.symbol)
            round +=1
            
        if(playerWon):
            print(f" ---- Player {(round%2 + 1)} won! ----")
            endState = "win" if round%2 + 1 == 1 else "loss" # endstate in terms of player 1 
        else:
            print("---- No available moves its a Draw! ----")
            endState = "draw"
        
        self.printBoard() # end state 
        # saving the game
        gameID = self.getLastID(self.gamesStorePath)+1
        player1Type = self.players[0].name
        player2Type = self.players[1].name
        gameRecord = [gameID,player1Type,player2Type,moves,endState]

        # storing game to file
        file_exists = os.path.exists(self.gamesStorePath)

        with open(self.gamesStorePath, "a", newline="") as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["gameID", "player1", "player2", "moves", "endState"])
            
            writer.writerow(gameRecord)
        #storing result for agents:
        self.players[0].updateData(endState)
        if (endState == "win"):
            outcome = "loss"
        if (endState == "loss"):
            outcome = "win"
        else:
            outcome = endState
        self.players[1].updateData(outcome)



        print("Would you Like to play Again? (Y/N)")
        
        playAgain = True
        while(playAgain):
            userInput = input(": " )
            match userInput:
                case "Y":
                    playAgain = self.startGame()
                case "N":
                    playAgain = False
                    print("exiting...")
                    return playAgain
                case _:
                    print("invalid input Try again") 

    def startGameForStats(self, players): # for benchmarking hence no output 
        self.players = players
        # creating/ resetting board
        self.resetBoard()
        # start the game
        moves = []
        endState = None
        playerWon = False
        round = 1
        while(playerWon != True and round < self.length * self.hight): # second condition is to check is the board is not full
            player = self.players[(round%2)-1]
            chosenCol = player.makeMove()
            moves.append(chosenCol) # not storing player symbol as it can be worked out by move count
            playerWon = self.isWinner(player.symbol)
            round +=1
            
        if(playerWon):
            endState = "win" if round%2 + 1 == 1 else "loss" # endstate in terms of player 1 
        else:
            endState = "draw"
        
        # saving the game
        gameID = self.getLastID(self.gamesStorePath)+1
        player1Type = self.players[0].name
        player2Type = self.players[1].name
        gameRecord = [gameID,player1Type,player2Type,moves,endState]

        # storing game to file
        file_exists = os.path.exists(self.gamesStorePath)

        with open(self.gamesStorePath, "a", newline="") as file:
            writer = csv.writer(file)
            
            if not file_exists:
                writer.writerow(["gameID", "player1", "player2", "moves", "endState"])
            
            writer.writerow(gameRecord)
        #storing result for agents:
        self.players[0].updateData(endState)
        if (endState == "win"):
            outcome = "loss"
        if (endState == "loss"):
            outcome = "win"
        else:
            outcome = endState
        self.players[1].updateData(outcome)
        
    def resetBoard(self):
        self.board = []
        i = 0
        for i in range(self.hight):
            j = 0
            row = []
            for j in range(self.length):
                row.append(" ")
            self.board.append(row)
        # creating height columnTokenCounter to enable quickly understanding how full a column is
        self.columnTokenCounter  = [0 for _ in range(self.length)]
    
    def choosePlayer(self, playerNum):
        
        print(f"choose from the following Agents for player {playerNum} with win loss and draw rates") 
        i = 1
        for player in self.availablePlayers: # availablePlayers = ["Human", "Random", "Smart", "Min-Max", "Machine Learning"]
            playerAgent = self.getAgent(player, 1)
            agentStats = playerAgent.getAndFormatAgentStats()
            print(f"{i}) " +player+ "Stats:" +agentStats )
            i += 1

        while(True):
            userInput = input(": " )
            playerAgent = self.getAgent(userInput, playerNum)
            if not playerAgent:
                print("invalid input Try again")
            else:
                return playerAgent
            
        
    def getAgent(self, agentChoice, playerNum, addDelay=True ):    
        match agentChoice:
                case "1" | "Human":
                    return HumanPlayer(self, "X" if playerNum ==1 else "O")
                case "2"| "Random":
                    return RandomAgent(self, "X" if playerNum ==1 else "O",addDelay=addDelay)
                case "3" | "Smart":
                    return SmartAgent(self, "X" if playerNum ==1 else "O",addDelay=addDelay)
                case "4"| "Min-Max":
                    return minMaxAgent(self, "X" if playerNum ==1 else "O",addDelay=addDelay)
                case "5"| "Machine Learning":
                    return MachineLearningAgent(self, "X" if playerNum ==1 else "O", self.MLModelPath)
                case _:
                     return False

    
                
    def printBoard(self):
        for row in self.board:
            row = "|" + "|".join(row) + "|"
            print(row)
        print( "|" + "|".join(list(str(num) for num in range(1,self.length + 1))) + "|")
        
        
    
    
    def inBounds(self, row, col):
        if row < 0 or row >= self.hight or col < 0 or col >= self.length:
            return False
        else: 
            return True

    def makeMove(self, column ,symbol): # assuming column is in format from 1 to length 
        if self.columnTokenCounter[column-1] < self.hight:
            self.board[self.hight - (self.columnTokenCounter[column-1] +1)][column-1] = symbol
            self.columnTokenCounter[column-1] += 1 
            return True
        else: 
            return False ## column is full so a token cannot be placed
        
    def isWinner(self, symbol):
        # end to end check checks both ends of a line before working its way in
        FOUR_AWAY_TRANSFORM_FACTORS = [(0,3),(3,3),(3,0),(0,-3),(3,-3),(-3,-3),(-3,0),(-3,3)]
        
        column = 0
        while (column < self.length ):
            row = self.hight - 1 
            while row > (self.hight - (self.columnTokenCounter[column] +1)): ## only checking how high the tokens have reached so far
                if self.board[row][column] == symbol:
                    for ROW_TRANSFORM, COL_TRANSFORM in FOUR_AWAY_TRANSFORM_FACTORS:
                        checkRow = int(row - ROW_TRANSFORM )
                        checkCol = int(column + COL_TRANSFORM) 
                        numChecked = 1
                        while numChecked != 4:
                            # print(f" for space ({checkCol}, {checkRow}): ") # test
                            # print(self.inBounds(checkRow,checkCol)) # test
                            # try:
                            #     print(self.board[checkRow][checkCol] == symbol)# test
                            # except:
                            #     print("error") # test
                            if self.inBounds(checkRow,checkCol) and self.board[checkRow][checkCol] == symbol:
                                checkRow += int(1 * (ROW_TRANSFORM/3)) # will result is + or - 1  if ROW_TRANSFORM > 0 else  will be 0
                                checkCol -= int(1 * (COL_TRANSFORM/3)) # will result is + or - 1  if ROW_TRANSFORM > 0 else  will be 0
                                numChecked += 1 
                            else:
                                break ## line broken therefore not counted: 
                        if numChecked == 4:
                            return True
                row -=1
            column += 1
        return False
    
    def benchMark(self, numGamesPerAgent = 500): # to get win rates of agents 
        agentsToTest = self.availablePlayers
        agentsToTest.remove("Human")
        gamesPerOpponent = numGamesPerAgent // len(agentsToTest)
        for agent1 in agentsToTest:
            for agent2 in agentsToTest:
                if(agent1 != agent2):
                    i = 1
                    for i in range(gamesPerOpponent):
                        players = []
                        players.append(self.getAgent(agent1,1,False))
                        players.append(self.getAgent(agent2,2,False))

                        self.startGameForStats(players)
                
                





# --- agents --- 
class agent:
    def __init__(self):
        self.agentDataPath = "Data\\agentData"
        self.name = "agent"
    
    def updateData(self, outcome):
        fieldnames = ["agent", "winNum", "lossNum", "drawNum"]
        updated = False
        modifiedRow = {"agent": self.name, "winNum": "0", "lossNum": "0", "drawNum": "0"}
        filePath = "Data\\agentStats.csv"

        if not os.path.exists(filePath): # creating a file if it doesn't exist
            with open(filePath, "w", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()

        with open(filePath, "r+", newline="") as file:
            reader = csv.DictReader(file)
            rows = list(reader)

            # Find and update the row
            for row in rows:
                if row["agent"] == self.name:
                    row[outcome + "Num"] = str(int(row[outcome + "Num"]) + 1)
                    updated = True
                    break

            # If agent not found, add new row
            if not updated:
                modifiedRow[outcome + "Num"] = "1"
                rows.append(modifiedRow)

            # Move to beginning and overwrite file
            file.seek(0)
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
            file.truncate()  # clear remaining old content

    def getAndFormatAgentStats(self):
        filePath = "Data\\agentStats.csv"

        if  os.path.exists(filePath): 
            with open(filePath, "r", newline="") as file:
                reader = csv.DictReader(file)
                rows = list(reader)
                for row in rows:
                    if row["agent"] == self.name:
                        totalGames = int(row["winNum"]) + int(row["lossNum"])  +int(row["drawNum"])
                        winRate = int(row["winNum"])/totalGames *100
                        lossRate = int(row["lossNum"])/totalGames * 100
                        DrawRate = int(row["drawNum"])/totalGames * 100
                        returnStr =   returnStr = (
                                f"Win rate: {winRate:.3f}  "
                                f"Loss rate: {lossRate:.3f}  "
                                f"Draw rate: {DrawRate:.3f}  "
                                f"out of {totalGames} games"
                            )
                        return returnStr

            return "No Data"
        else:
            return "No Data"


class HumanPlayer(agent):
    def __init__(self, game, symbol):
        self.game = game
        self.symbol = symbol
        self.name = "HumanPlayer"
    
    def makeMove(self):
        moveValid = False
        while (moveValid != True):
            chosenCol = input("coloumn: ")
            try: 
                chosenCol = int(chosenCol) 
                if(chosenCol < 1 or chosenCol > self.game.length):
                    print(f"Please input a Number between 1 and {self.game.length}!")
                else:
                    moveValid = self.game.makeMove(chosenCol, self.symbol)
                    if (moveValid == False):
                        print("row is full! ")
                    else:
                        return chosenCol
            except ValueError:
                print(f"Please input a valid Number! ")

class RandomAgent(agent):
    def __init__(self, game, symbol, addDelay=True):
        self.game = game
        self.symbol = symbol
        self.name = "RandomAgent"
        self.addDelay = addDelay
        
    def makeMove(self):
        moveValid = False
        if self.addDelay:
                sleep(1) # added sleep so that the moves are made at a manageable speed for humans to see
        while (moveValid != True):
            chosenCol = random.randint(1,self.game.length)
            moveValid = self.game.makeMove(chosenCol, self.symbol)
        return chosenCol

class SmartAgent(agent):
    def __init__(self, game, symbol, addDelay=True):
        self.game = game
        self.symbol = symbol
        self.opponentSymbol = "O" if self.symbol == "X" else "X"
        self.name = "SmartAgent"
        self.addDelay = addDelay
        
        ### test #### 
        ##self.minMaxAgent = minMaxAgent(self.game, self.symbol, 2)
        
    def checkForWinningMove(self, symbol):
        col = 1
        for col in range(1,self.game.length):
            #check 
            copyOfGame = copy.deepcopy(self.game)
            copyOfGame.makeMove(col,symbol)
            
            if(copyOfGame.isWinner(symbol)):
                # make move
                return col
            col += 1
        return False
        
    def makeMove(self):
         ### test ### 
        ##scores = self.minMaxAgent.calcMovesScores(self.game)
        ##print(scores)
        ##print(type(scores[1]))

        moveValid = False

        if self.addDelay:
            sleep(1) # added sleep so that the moves are made at a manageable speed for humans to see
        
        # 1) check if there is a winning move for self 
        winningMove = self.checkForWinningMove(self.symbol)
        if(winningMove != False):
            moveValid = self.game.makeMove(winningMove, self.symbol)
            return winningMove
        # 2) check if winning move for opponent 
        blockingMove = self.checkForWinningMove(self.opponentSymbol)
        if(blockingMove != False):
            moveValid = self.game.makeMove(blockingMove, self.symbol)
            return blockingMove
        
        # 3) no winning or blocking move found revert to random move
        while (moveValid != True):
            chosenCol = random.randint(1,self.game.length)
            moveValid = self.game.makeMove(chosenCol, self.symbol)
        return chosenCol
    
                
                        
class minMaxAgent(agent):
    def __init__(self, game, symbol, maxDepth = 2, addDelay=True):
        self.game = game
        self.symbol = symbol
        self.opponentSymbol = "O" if self.symbol == "X" else "X" 
        self.maxDepth = maxDepth
        self.name = "minMaxAgent"
        self.addDelay = addDelay
    
    def calcMovesScores(self, game, isSelfTurn = True, currentDepth = 1): ## will return a tree of scores for each possible move
        
        
        if(currentDepth > self.maxDepth):
            return 0; ## no winning move found at maximum depth so position is deemed neutral
        
        scores = {col: 0 for col in range(1, game.length+1)}
        
        col = 1
        for col, score in scores.items():
            copyOfGameForSelf = copy.deepcopy(game)
            moveValid = copyOfGameForSelf.makeMove(col, self.symbol)
            
            copyOfGameForOpp = copy.deepcopy(game)
            copyOfGameForOpp.makeMove(col, self.opponentSymbol)
            if(not moveValid): ## so as not to suggest a move that isn't valid
                scores[col] = None
            elif(copyOfGameForSelf.isWinner(self.symbol)):  
                scores[col] = 10**(self.maxDepth-currentDepth) * (1 if isSelfTurn  else -0.5) # second condition so it will understand what the opponent will do 
            elif(copyOfGameForOpp.isWinner(self.opponentSymbol)):
                scores[col] = (10**(self.maxDepth-currentDepth)) * (0.5 if isSelfTurn != 0 else -1) ## 0.5 in both scores is to represent a blocking move 
            else:
                gameToPass = copyOfGameForSelf if isSelfTurn else copyOfGameForOpp
                scores[col]  = self.calcMovesScores(gameToPass, not isSelfTurn, currentDepth + 1)
            ##print(scores) ## test 
        return scores
        
    def minMax(self, scores, isMaxing, currentDepth = 1):
        
        score = 0 ## remove?
        bestScore = 0; 
        colWithBestScore = None; ##  defaulting to first column to avoid error
        availableCols  = list(range(1, self.game.length + 1))
        ##print(scores.items())
        for col, score in scores.items():
            #print(type(score))
            if (score == None):
                availableCols.remove(col) ## removing so it isn't used as best col as the move isn't valid 
            elif (isinstance(score, dict)):
                scores[col] = self.minMax(score, not isMaxing, currentDepth+1)[1]
                score = scores[col]
                
            
            if(score != None):
                if((isMaxing) and score > bestScore):
                    bestScore = score
                    colWithBestScore = col
                elif((not isMaxing) and score < bestScore):
                    bestScore = score
                    colWithBestScore = col
            if not self.addDelay:
                print(f"scores for col: {col} at depth: {currentDepth} Scores: {scores}")
       

        if(colWithBestScore == None):
            randomIndex = random.randint(0,len(availableCols)-1)
            colWithBestScore = availableCols[randomIndex] ## adding some random so it wont always play the same game if it thinks moves have equal value 
            bestScore = scores[colWithBestScore]## Randomise 

        return (colWithBestScore, bestScore)
        
    def makeMove(self):
        scores = self.calcMovesScores(self.game)
        result = self.minMax(scores, True)
        bestCol = result[0]
        bestScore = result[1]
        ### making the move ### 
        ##sleep(0.5) # added sleep so that the moves are made at a manageable speed for humans to see
        print (scores)
        ## steps away
        ##steps = math.log(abs(bestScore),5)
        



        print(f"best Col:{bestCol} with score: {bestScore}")
      
        moveValid = self.game.makeMove(bestCol, self.symbol)
        return bestCol


class MachineLearningAgent(agent):
    def __init__(self, game, symbol, modelPath, addDelay=True):
        self.game = game
        self.symbol = symbol
        self.opponentSymbol = "O" if self.symbol == "X" else "X"
        #print(os.path.exists(modelPath)) ## test 
        self.model = load_model(modelPath) 
        self.classes = ['draw', 'loss', 'win']
        self.cellMap = {'X': 1, 'O': 2, ' ': 0}
        self.name = "MachineLearningAgent"
        self.addDelay = addDelay

    # def oneHotEncode(label, classes):
    #     oneHot = np.zeros(len(classes))
    #     index = classes.index(label)  # Find the index of the label
    #     oneHot[index] = 1  # Set the corresponding index to 1
    #     return oneHot

    def oneHotDecode(self, oneHot, classes):
        index = np.argmax(oneHot)
        return classes[index]
    
    def formatBoard(self, board):
        # get board as one list in format ML model expects
        encodedBoard = []
        for row in board:
            encodedBoard+=row
        
        # changing cellMap so 1 is always self an 2 is always opponent 
        if self.symbol == 'O':
            self.cellMap = {'X': -1, 'O': 1, ' ': 0}
        else: 
            self.cellMap = {'X': 1, 'O': -1, ' ': 0}

        # changing symbols to numbers so ML model can understand  
        encodedBoard = [self.cellMap.get(x, x) for x in encodedBoard]
        #  reshaping in numpy
        encodedBoard = np.array(encodedBoard).reshape(1, 42)

        return encodedBoard

    def makeMove(self):
        ## evaluated current position
        # formattedCurrentGame = self.formatBoard(self.game.board)
        # result = self.model.predict(formattedCurrentGame)
        # index = np.argmax(result)
        # outcome = self.oneHotDecode(result, self.classes)
        # confidence = round(result[0][index],3) ## sees how good the move is
        # print((outcome, confidence ))


        if self.addDelay:
            sleep(1) # added sleep so that the moves are made at a manageable speed for humans to see

        # finding what move is the best move according to ML agent 
        bestResult = -1
        bestCol = None ## val is None to avoid playing a move that is invalid
        moveResults = []
        col = 1
        for col in range(1,self.game.length+1):
            copyOfGame = copy.deepcopy(self.game) 
            validMove = copyOfGame.makeMove(col, self.symbol) ## makes the move 
            if(validMove != False):
                formattedCopyOfGame = self.formatBoard(copyOfGame.board)

                result = self.model.predict(formattedCopyOfGame)[0]
                moveResults.append((col, result ))
                # deciding best move 
                if(result > bestResult ):
                    bestResult = result
                    bestCol = col
                

        # making the move on the real board 
        if self.addDelay:
            print(moveResults) # test 
            print(f"ML Agent think the best Col is: {bestCol} with confidence of: {result} ")
        self.game.makeMove(bestCol, self.symbol)
        return bestCol
        
    
            


# test 
g1 = Connect4Game()
#g1.benchMark()
g1.startGame()

# p1 = HumanPlayer(g1,"X")
# p1.makeMove()
# g1.printBoard()
# p1.makeMove()
# g1.printBoard()
# - break check
# g1.printBoard()
# print("") # spacing 
# g1.makeMove(1,"X")
# g1.makeMove(2,"O")
# g1.makeMove(3,"X")
# g1.makeMove(4,"X")
# g1.makeMove(5,"X")
# g1.makeMove(6,"X")

# - diagonal check - 
# g1.makeMove(1,"X")
# g1.makeMove(2,"O")
# g1.makeMove(2,"X")
# g1.makeMove(3,"O")
# g1.makeMove(3,"O")
# g1.makeMove(3,"X")
# g1.makeMove(4,"O")
# g1.makeMove(4,"O")
# g1.makeMove(4,"O")
# g1.makeMove(4,"X")
# g1.printBoard()
# print(g1.isWinner("X"))