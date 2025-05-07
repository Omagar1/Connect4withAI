import random 
import math
from time import sleep
import copy

class Connect4Game:
    
    # --- attributes ---
    board = []
    columnTokenCounter = []
    length = 0
    hight = 0 
    
    # --- methods ---
    
    def __init__(self, length = 7, hight = 6):
        self.length = length
        self.hight = hight
    
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
        
        playerWon = False
        round = 1
        while(playerWon != True and round < self.length * self.hight): # second condition is to check is the board is not full
            print(f" ---- Player { 1 if round % 2 == 1 else 2}'s Move ----")
            player = self.players[(round%2)-1]
            self.printBoard()
            player.makeMove()
            playerWon = self.isWinner(player.symbol)
            round +=1
            
        #self.printBoard() # why?
        if(playerWon):
            print(f" ---- Player {(round%2 + 1)} won! ----")
        else:
            print("---- No available moves its a Draw! ----")
        
        self.printBoard() # end state 
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
        availablePlayers = ["Human", "Random", "Smart", "Min-Max"]
        print(f"choose from the following Agents for player {playerNum}")
        i = 1
        for player in availablePlayers:
            print(f"{i}) " +player)
            i += 1

        while(True):
            userInput = input(": " )
            match userInput:
                case "1":
                    return HumanPlayer(self, "X" if playerNum ==1 else "O")
                case "2":
                    return RandomAgent(self, "X" if playerNum ==1 else "O")
                case "3":
                    return SmartAgent(self, "X" if playerNum ==1 else "O")
                case "4":
                    return minMaxAgent(self, "X" if playerNum ==1 else "O")
                case _:
                    print("invalid input Try again")     
            
        

    
                
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

# --- agents --- 
class HumanPlayer:
    def __init__(self, game, symbol):
        self.game = game
        self.symbol = symbol
    
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
            except ValueError:
                print(f"Please input a valid  Number! ")

class RandomAgent:
    def __init__(self, game, symbol):
        self.game = game
        self.symbol = symbol
        
    def makeMove(self):
        moveValid = False
        while (moveValid != True):
            chosenCol = random.randint(1,self.game.length)
            sleep(1) # added sleep so that the moves are made at a manageable speed for humans to see
            moveValid = self.game.makeMove(chosenCol, self.symbol)

class SmartAgent:
    def __init__(self, game, symbol):
        self.game = game
        self.symbol = symbol
        self.opponentSymbol = "O" if self.symbol == "X" else "X"
        
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
        sleep(1) # added sleep so that the moves are made at a manageable speed for humans to see
        
        # 1) check if there is a winning move for self 
        winningMove = self.checkForWinningMove(self.symbol)
        if(winningMove != False):
            moveValid = self.game.makeMove(winningMove, self.symbol)
            return False
        # 2) check if winning move for opponent 
        blockingMove = self.checkForWinningMove(self.opponentSymbol)
        if(blockingMove != False):
            moveValid = self.game.makeMove(blockingMove, self.symbol)
            return False
        
        # 3) no winning or blocking move found revert to random move
        while (moveValid != True):
            chosenCol = random.randint(1,self.game.length)
            moveValid = self.game.makeMove(chosenCol, self.symbol)

        
        return False
    
                
                        
class minMaxAgent:
    def __init__(self, game, symbol, maxDepth = 5):
        self.game = game
        self.symbol = symbol
        self.maxDepth = maxDepth
    
    def isMoveWinning(self, game, col, symbol): ## makes moves on board passed through 
        moveValid = game.makeMove(col, symbol)
        result = game.isWinner(symbol)
        return (result , moveValid)
        
        
    def minMax(self, game, currentSymbol, currentDepth = 1):

        scores = []
        # finds all legal moves and creates copy to make move
        for col in range(1, self.game.length + 1):
            # make move
            copyOfGame = copy.deepcopy(game)

            # evaluates the move (recursive )
            isWinning, moveValid = self.isMoveWinning(copyOfGame, col, currentSymbol)
            if not moveValid:
                scores.append( float('-inf') if currentSymbol == self.symbol else float('inf') )# so move is never chosen if not valid 
            elif isWinning:
                scores.append(10**(self.maxDepth-currentDepth) * (1 if currentSymbol == self.symbol else -1)) # second condition so it will understand what the opponent will do 
            ## set up to account for turns to get to that positions so it will prioritise a blocking move in 1 move than an winning move in 5
            elif currentDepth >= self.maxDepth: # exit condition
                scores.append(0); ## might add heuristics later
            else:
                colScore = self.minMax(copyOfGame, "O" if currentSymbol == "X" else "X", currentDepth + 1 )[0]
                scores.append(colScore)

        # finds best move
        if currentDepth == 1:
            print(f"currentDepth: {currentDepth}")#test 
            print(scores) #test

        if currentSymbol == self.symbol:
            bestScore = max(scores)
        else: 
            bestScore = min(scores)

        bestCol = scores.index(bestScore) + 1 

        #print(f"bestCol: {bestCol}")#test 


        return (bestScore, bestCol)

            
 
    def makeMove(self):
        
        result = self.minMax(self.game, self.symbol)
        print(f"Min Max thinks that {result[1]} is the best col with score: {result[0]}")
        self.game.makeMove(result[1], self.symbol)
        
    
            


# test 
g1 = Connect4Game()
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