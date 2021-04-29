def find_next_empty(puzzle):
    #finds the next row, col on the puzzle that is not filled yer -->rep with -1
    #return row, col tuple (None, None) is there is none

    #we are using 0 - 8 indices
    for r in range(9):
        for c in range(9): #range(9) is 0,1,..8
            if puzzle[r][c] == -1:
                return r,c
    return None,None #if no spaces in the puzzle are empty


def is_valid(puzzle, guess, row, col):
    #find out if guess at (row, col) is valid or not
    #return True if it is valid else False

    #row
    row_val = puzzle[row]
    if guess in row_val:
        return False

    #col
    col_vals = []
    # for i in range(9):
    #     col_vals.append(puzzle[i][col])
    #or using list comprehension
    col_vals = [puzzle[i][col] for i in range(9)]
    if guess in col_vals:
        return False

    #in sqaures
    #get where the 3x3 starts and iterate over  the 3 values in the square
    row_start = (row // 3) * 3  #don't take remainder , * 3 to get the actual index
    # 1 // 3 = 0, 5 // 3 = 1 ...
    col_start = (col // 3) * 3
    for r in range(row_start, row_start + 3):
        for c in range(col_start, col_start + 3):
            if puzzle[r][c] == guess:
                return False
    #all checks pass
    return True

def solve_sudoku(puzzle):
    #solves using backtracking
    #puzzle is a list of list, where each inner list is a row 
    #returns whether a solution exists
    #mutates puzzle to the solution when it exists

    #step 1:choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    #Step1.1 if there is nowhere left, then we are done because we only allowed valid input
    if row is None:
        return True

    #Step 2: if there is a place to put a number, then make a guess 1 to 9
    for guess in range(1,10): #range(1,10) is 1,2..9
        #step 3: chec if this is a valid guess
        if is_valid(puzzle, guess, row, col):
            #step 3.1 if this is valid, then place that guess on the puzzle:
            puzzle[row][col] = guess
            #Step 4: recursively call our function
            if solve_sudoku(puzzle):
                return True
        #step 5: if not valid OR if our guess does not solve the puzzle we need to backtrack
        #and try another number
        puzzle[row][col] = -1 #reset the guess

    #step 6: if none of the numbers that we try work, then this puzzle is unsolvable.
    return False

if __name__ == '__main__':
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(solve_sudoku(example_board))
    print(example_board)
