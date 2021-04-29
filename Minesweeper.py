import random
import re

#board to represent the game
class Board:
    def __init__(self, dim_size, num_bombs):
        #track these param
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        #create the board
        self.board = self.make_new_board() #plant the bombs
        self.assign_values_to_board()
        #initialize a set to keep track of which locations we've uncovered
        #we'll save (row,col) tuples into this set
        self.dug = set() #if we dig at 0,0 then self.dug = {(0,0)}

    def make_new_board(self):
        #construct a new board based on the dimsizze and numbombs
        #construct lost of lists for 2-D representation


        #generate a new board
        board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        #this creates a 2-D array of None
        #of size dimsize x dimsize

        #plant bombs
        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            #returns a random int N such that a <= N <= b
            loc = random.randint(0, self.dim_size**2 - 1)
            row = loc // self.dim_size #want to know how many times dim_size goes into loc and that number denotes the row we are in
            col = loc % self.dim_size # remainder shows the column we are at
            if board[row][col] == '*':
                #this means we have actually planted a bomb there 
                #so keep going
                continue
            board[row][col] = '*' #plant the bomb
            bombs_planted += 1

        return board

    def assign_values_to_board(self):
        #after planting bombs we will assign a number from 1 - 8 for all empty spaces
        #which will represent how many neighbouring bombs there are. We can precompute
        #these and it will save us some effort checking what's around the board latrer.
        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == '*':
                    #if this is already a bomb no need to calculate
                    continue
                self.board[r][c] = self.get_num_neighbouring_bombs(r, c)



    def get_num_neighbouring_bombs(self, row, col):
        #iterate through each of the neighbouring positions and sum number of bombs
        #top-left: (row-1,col-1)
        #top-middle: (row-1,col)
        #top-right: (row-1, col+1)
        #left: (row, col-1)
        #right: (row,col+1)
        #bottom left: (row+1,col-1)
        #bottom middle: (row+1,col)
        #bottom right: (row+1,col+1)


        #don't go out of bounds
        num_neighbouring_bombs = 0
        #max in min to make sure that we don't go out of bounds
        #max so that we don't go in -ve and min so that we don't go above the dim size
        for r in range(max(0,row - 1), min(self.dim_size - 1,row + 1)+1): #above and below
            for c in range(max(0,col - 1), min(self.dim_size - 1,col + 1)+1): #left and right
                if r == row and c == col:
                    #original location don't check
                    continue
                if self.board[r][c] == '*':
                    #bomb as neighbour
                    num_neighbouring_bombs += 1
        
        return num_neighbouring_bombs

    def dig(self, row, col):
        #dig at location
        #true if successful, False if bomb


        #cases:
        #hit a bomb->game over
        #dig at place with neighbouring bombs -> finish dig
        #dig at location with no neighbouring bombs -> recursively dif neighbours

        self.dug.add((row, col)) #tuple to keep track of location where we have dug
        
        if self.board[row][col] == '*':
            return False
        elif self.board[row][col] > 0:
            return True
        
        #self.board[row][col] == 0
        for r in range(max(0,row - 1), min(self.dim_size - 1,row + 1)+1): #above and below
            for c in range(max(0,col - 1), min(self.dim_size - 1,col + 1)+1): #left and right
                if (r,c) in self.dug:
                    continue #don't dig where already dug
                self.dig(r,c)

        #if our intial dig sisn't hit a bomb, we should not hit a bomb here
        return True

    def __str__(self):
        #magic function where if you call print on this object,
        #it will print out what this function returns
        #return the string that shows the board to the player

        #array to represent what the user will see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for row in range(self.dim_size):
            for col in range(self.dim_size):
                if (row,col) in self.dug:
                    visible_board[row][col] = str(self.board[row][col])
                else:
                    #the user has not dug here show empty space
                    visible_board[row][col] = ' '
        
        #put this in a string
        string_rep =''
        #get max column width for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx],visible_board)
            widths.append(len(max(columns,key = len)))

        #print csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format='%-'+str(widths[idx])+"s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'

        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-'+str(widths[idx])+"s"
                cells.append(format % col)
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'
        
        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len+'\n'+string_rep+'-'*str_len

        return string_rep



#play the game
def play(dim_size = 10, num_bombs = 10):
    #step 1: create the board and plant the bombs
    board = Board(dim_size, num_bombs)
    #Step 2: show the user the board and ask for where thhey want to dig

    #Step 3a: if location is a bomb, show game over message
    #Step 3b: if location is not a bomb, dig recursively until each 
    #         sqaure is at least next to a bomb
    #Step 4: repeat 2 and 3a/b until there are no more places to dig -> WIN

    while len(board.dug) < board.dim_size ** 2 - num_bombs:
        print(board)
        user_input = re.split(',(\\s)*', input("Where would you like yo dig? Input as row, col: ")) #'0, 4' ,(\\s)* handles the , and any amount of space
        row, col = int(user_input[0]),int(user_input[-1])
        if row < 0 or row >= board.dim_size or col < 0 or col >= dim_size:
            print("Inalid location. Try again.")
            continue

        #if it is valid, we dig
        safe = board.dig(row, col)
        if not safe:
            #dug a bomb
            break #(game over)

    # 2 ways to end loop, check which one
    if safe:
        print("Congratulations, YOU WON!!!")
    else:
        print("Sorry , GAME OVER!!")
        #let's reveal the whole board
        board.dug = [(r,c) for r in range(board.dim_size) for c in range(board.dim_size)]
        print(board)



if __name__ == '__main__':
    play()
    