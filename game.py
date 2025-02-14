class Connect4Game:
    
    def __init__(self, length = 7, hight = 6):
        self.length = length
        self.hight = hight
        
        # creating the board 
        i = 0
        for i in range(hight):
            j = 0
            row = []
            for j in range(length):
                row.append(" ")
            self.board.append(row)
        # creating height columnTokenCounter to enable quickly understanding how full a column is
        self.columnTokenCounter  = [0 for _ in range(length)]
                
    def printBoard(self):
        for row in self.board:
            row = "|" + "|".join(row) + "|"
            print(row)
        print( "|" + "|".join(list(str(num) for num in range(1,self.length + 1))) + "|")
    # --- atributes ---
    board = []
    columnTokenCounter = []
    length = 0
    hight = 0 
    
    def inBounds(self, row, col):
        if row < self.hight or row > self.hight or col < self.length or col > self.length:
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
        row = self.hight -1 
        column = 0
        while row > (self.hight - (self.columnTokenCounter[column] +1)): ## only checking how high the tokens have reached so far
            if self.board[row][column] == symbol:
                for ROW_TRANSFORM, COL_TRANSFORM in FOUR_AWAY_TRANSFORM_FACTORS:
                    checkRow = row + ROW_TRANSFORM
                    checkCol = column + COL_TRANSFORM
                    numChecked = 1
                    while numChecked != 4:
                        if self.inBounds(checkCol,checkRow) and self.board[checkRow][checkCol] == symbol:
                            checkRow -= (1 * (ROW_TRANSFORM/3)) # will result is + or - 1  if ROW_TRANSFORM > 0 else  will be 0
                            checkCol -= (1 * (COL_TRANSFORM/3)) # will result is + or - 1  if ROW_TRANSFORM > 0 else  will be 0
                            numChecked += 1 
                        else:
                            break ## line broken therefore not counted: 
                    if numChecked == 4:
                        return True
            row-=1
        return False
        
            
        
    
    
# test 
g1 = Connect4Game()
g1.printBoard()
print("") # spacing 
g1.makeMove(1,"X")
g1.makeMove(1,"X")
g1.makeMove(1,"X")
g1.makeMove(1,"X")
# g1.makeMove(1,"X")
# g1.makeMove(2,"O")
# g1.makeMove(2,"X")
# g1.makeMove(3,"O")
# g1.makeMove(3,"O")
# g1.makeMove(3,"O")
# g1.makeMove(4,"O")
# g1.makeMove(4,"O")
# g1.makeMove(4,"O")
# g1.makeMove(4,"X")
g1.printBoard()
print(g1.isWinner("X"))