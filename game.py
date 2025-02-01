class Connect4Game:
    
    def __init__(self, lenght = 7, hight = 6):
        # creating the board 
        i = 0
        for i in range(hight):
            j = 0
            row = []
            for j in range(lenght):
                row.append(" ")
            self.board.append(row)
        
    def printBoard(self):
        i = 0
        for row in self.board:
            row +=  str(i)
            row = "|".join(row)
            print(row)
            i += 1
    # --- atributes ---
    board =[[]]

    def makeMove(self,row,column,symbol):
        self.board[row][column] = symbol
        
g1 = Connect4Game()
g1.printBoard()
g1.makeMove(0,0,"X")
g1.printBoard()