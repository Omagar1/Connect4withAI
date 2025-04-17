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
    def __init__(self, game, symbol, maxDepth = 3):
        self.game = game
        self.symbol = symbol
        self.opponentSymbol = "O" if self.symbol == "X" else "X" 
        self.maxDepth = maxDepth
        self.scoreTree = {}
    
    def minMax(self, copyOfGameForSelf, copyOfGameForOpp, prevCol = "Start", isMaxing = True, currentDepth = 0):
        if(currentDepth != self.maxDepth):
            self.scoreTree.setdefault((prevCol, currentDepth), []) ## initialising so in right order 

        score = 0 
        if(currentDepth > 0 and copyOfGameForSelf.isWinner(self.symbol)):  
            score = 10**(self.maxDepth-currentDepth) * (1 if isMaxing  else -1)  # if self winning move: if my turn: very good if not my turn: bad
            return (prevCol, score) ## return group 1
        elif(currentDepth > 0 and copyOfGameForOpp.isWinner(self.opponentSymbol)):
            score = (10**(self.maxDepth-currentDepth)) * (1 if isMaxing != 0 else -1) # if opponent winning move if my turn: good but not as good as win  if not my turn:very bad
            return (prevCol, score) ## return group 1
        elif(currentDepth == self.maxDepth):
            return (prevCol, 0) # max depth has been reached with no winning move found ## return group 1
        else:
            scores = {}
            availableCols  = list(range(1, self.game.length + 1))

            workingGame = copyOfGameForOpp if isMaxing else copyOfGameForSelf ## i.e. opponent has moved self is yet to move when is maxing = true 

            
            for col in range(1, self.game.length + 1):
                ## make move
                copyOfGameForSelf = copy.deepcopy(workingGame)
                moveValid = copyOfGameForSelf.makeMove(col, self.symbol)
                
                copyOfGameForOpp = copy.deepcopy(workingGame)
                copyOfGameForOpp.makeMove(col, self.opponentSymbol)
                ## evaluate  move
                if(moveValid):
                    if(isMaxing):
                        bestScore = float("-inf"); 
                        colWithBestScore = None; 

                        score = self.minMax(copyOfGameForSelf,copyOfGameForOpp, col, not isMaxing, currentDepth+1)[1] ## where return group 1 returns; should be one score
                        
                        #self.scoreTree[(prevCol, currentDepth)].append((col, currentDepth, scores)) ## adding scores once i have them ## for tree does't effect evaluation 
                        bestScore = max(bestScore, score)
                        
                    else:
                        bestScore = float("inf"); 
                        colWithBestScore = None; 

                        score = self.minMax(copyOfGameForSelf,copyOfGameForOpp, col, not isMaxing, currentDepth+1)[1] ## where return group 1 returns  
                        
                        self.scoreTree[(prevCol, currentDepth)].append((col, currentDepth, scores)) ## adding scores once i have them
                        bestScore = min(bestScore, score)
                        ## but how do I get teh columns? 
        
                else:
                    availableCols.remove(col) ## removing so it isn't used as best col as the move isn't valid 
                col += 1

            if(colWithBestScore == None):
                randomIndex = random.randint(0,len(availableCols)-1)
                colWithBestScore = availableCols[randomIndex] ## adding some random so it wont always play the same game if it thinks moves have equal value 
                bestScore = scores[colWithBestScore]## Randomise

            return (colWithBestScore, bestScore) ## final return 
        
    def printScoreTree(self):
        for prevCol, prevDepth in self.scoreTree:
            print(f"Column {prevCol} at depth {prevDepth}:")
            for colData in self.scoreTree[(prevCol,prevDepth)]:
                print (f"   Column {colData[0]} depth: {colData[1]} Has scores: {colData[2]}")

        
    def makeMove(self):
        result = self.minMax(self.game, self.game)
        bestCol = result[0]
        bestScore = result[1]
        ### making the move ### 
        ##sleep(0.5) # added sleep so that the moves are made at a manageable speed for humans to see
        ## steps away
        ##steps = math.log(abs(bestScore),5)
        


        #self.printScoreTree()
        print(f"best Col:{bestCol} with score: {bestScore}")
      
        moveValid = self.game.makeMove(bestCol, self.symbol)
        
    
            


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