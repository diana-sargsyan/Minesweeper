from itertools import permutations 
import matplotlib.pyplot as plt
from time import sleep
from sys import platform
import random
import os

from tqdm import tqdm

subsets = []

 
def print_map(mine_values, n):
    """Prints the map to the screen"""
 
    print()
    print("Mineswooper by Mher Movsisyan, Diana Sargsyan, and Lilit Beglaryan")
    print()
 
    st = "   "
    for i in range(n):
        st = st + str(i + 1).rjust(6)
    print(st)   
 
    for r in range(n):
        st = "     "
        if r == 0:
            for col in range(n):
                st = st + "______" 
            print(st)
 
        st = "     "
        for col in range(n):
            st = st + "|     "
        print(st + "|")
         
        st = str(r + 1).ljust(5)
        for col in range(n):
            st = st + "|  " + str(mine_values[r][col]) + "  "
        print(st + "|") 
 
        st = "     "
        for col in range(n):
            st = st + "|_____"
        print(st + '|')
 
    print()
  
# Function for setting up Mines
def set_mines(numbers, n_mines, n):
    # Track of number of mines already set up
    count = 0
    while count < n_mines:
 
        # Random number from all possible grid positions 
        val = random.randint(0, n*n-1)
 
        # Generating row and column from the number
        r = val // n
        col = val % n
 
        # Place the mine, if it doesn't already have one
        if numbers[r][col] != -1:
            count = count + 1
            numbers[r][col] = -1
            
    return numbers
 
# Function for setting up the other grid values
def set_values(numbers, n):
    # Loop for counting each cell value
    for r in range(n):
        for col in range(n):
 
            # Skip, if it contains a mine
            if numbers[r][col] == -1:
                continue
 
            # Check up  
            if r > 0 and numbers[r-1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check down    
            if r < n-1  and numbers[r+1][col] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check left
            if col > 0 and numbers[r][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check right
            if col < n-1 and numbers[r][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-left    
            if r > 0 and col > 0 and numbers[r-1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check top-right
            if r > 0 and col < n-1 and numbers[r-1][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-left  
            if r < n-1 and col > 0 and numbers[r+1][col-1] == -1:
                numbers[r][col] = numbers[r][col] + 1
            # Check below-right
            if r < n-1 and col < n-1 and numbers[r+1][col+1] == -1:
                numbers[r][col] = numbers[r][col] + 1
                
    return numbers
 
# Function for clearing the terminal
def clear():
    if platform in ["linux", "linux2", "darwin"]:
        os.system("clear")
    elif platform == "win32":
        os.system("cls")   
 
# Function to display the instructions
def instructions():
    print("Instructions:")
    print('1. Enter row and column number to select a cell, Example "2 3"')
    print('2. In order to flag a mine, enter F after row and column numbers, Example "2 3 F"')
 
# Goal check
def check_over():
    global mine_values
    global n
    global n_mines
 
    # Count of all numbered values
    count = 0
 
    # Loop for checking each cell in the grid
    for r in range(n):
        for col in range(n):
 
            # If cell not empty or flagged
            if mine_values[r][col] != ' ' and mine_values[r][col] != 'F':
                count = count + 1
     
    # Count comparison          
    if count == n * n - n_mines:
        return True
    else:
        return False
    
# Display all the mine locations                    
def show_mines(mine_values, numbers, n):
 
    for row in range(n):
        for col in range(n):
            if numbers[row][col] == -1:
                mine_values[row][col] = 'M'
    
    return mine_values
 

def get_adj_coords(row, col, n):
    u_rows = []
    if row != 0:
        u_rows += [row - 1]
    u_rows += [row]
    if row != n - 1:
        u_rows += [row + 1]
    
    u_cols = []
    if col != 0:
        u_cols += [col - 1]
    u_cols += [col]
    if col != n - 1:
        u_cols += [col + 1]
        
    pairs = [(r, c) for r in u_rows for c in u_cols]
    if (row, col) in pairs:
        pairs.remove((row, col))
        
    return pairs


 
def solve(i, n, n_mines, mine_values, flags, unopeneds, vis, tovis):
    global subsets, unopened
    # Opening up corner as first step (childhood habit of Mher)
    if i == 0:
        return "1 1"
    
    # check if all mines are found
    if n_mines == len(flags):
        input("Done artificially intelligencing this game. Press enter to exit")
        

    for row, col in vis:
        if mine_values[row][col] == 0:
            # uncover safe squares
            for pair in unopeneds[row][col]:
                return f"{pair[0] + 1} {pair[1] + 1}"


    for row, col in vis:
        # if unopened squares = indicator, flag as mine
        if (mine_values[row][col] == len(unopeneds[row][col])) and \
                mine_values[row][col] > 0:
            f_row, f_col = unopeneds[row][col][-1]
            return f"{f_row + 1} {f_col + 1} f"
        

    try:
        if len(vis) > 1:
            for row, col in vis:
                # only look at different 2-adjascent pairs
                for row_2, col_2 in set(vis):
                    if row_2 > row + 2 or row_2 < row - 2 or col_2 > col + 2 or col_2 < col - 2:
                        continue 
                    
                    # If unopened squares are subset of another visited numbered square
                    if set(unopeneds[row][col]).intersection(set(unopeneds[row_2][col_2])) == set(unopeneds[row][col]) and \
                            type(mine_values[row_2][col_2]) is int and \
                            type(mine_values[row][col]) is int and \
                            mine_values[row_2][col_2] > 0 and \
                            mine_values[row][col] > 0 and \
                            len(unopeneds[row][col]) < len(unopeneds[row_2][col_2]):

                        # schedule to decrement value
                        subsets.append(((row_2, col_2), mine_values[row][col]))
                        
                        # remove constraints from second square
                        for r, c in unopeneds[row][col]:
                            unopeneds[row_2][col_2].remove((r, c))

                        raise StopIteration()
    except StopIteration as e:
        return "0 0" # Return errant input to update state
                

                    # return f"{f_row + 1} {f_col + 1} f"
        
    # if number of unopened squares matches the number of missing mines, flag em all
    if len(tovis) == (n_mines - len(flags)):
        f_row, f_col = tovis[row][col][-1]
        return f"{f_row + 1} {f_col + 1} f"
    
    # free up corners before brute-forcing, avoids worst case in most cases
    if i <= 12:
        if (n-1, n-1) in tovis:
            return f"{n} {n}"
        elif (0, n-1) in tovis:
            return f"{1} {n}"
        elif (n-1, 0) in tovis:
            return f"{n} {1}"
    
    mines_left = (n_mines - len(flags))
    multiverse = {}
    
    # Brute force through remaining squares
    perms = set(permutations(([-1]*mines_left) + ([0] * (len(tovis) - mines_left))))
    for perm in tqdm(perms):
        # Simulate mine placement
        hypothesis_world = [[0 for c in range(n)] for r in range(n)]
        for sq_id in range(len(tovis)):
            hypothesis_world[tovis[sq_id][0]][tovis[sq_id][1]] = perm[sq_id]
                
        # calculate indicators
        hypothesis_world = set_values(hypothesis_world, n)
        
        try:
            for hypo_row, hypo_col in vis:
                p1 = hypothesis_world[hypo_row][hypo_col]
                p2 = mine_values[hypo_row][hypo_col]
                if type(p2) is int:
                    assert p1 == p2, "Inconsistent universe model"
        except AssertionError as e:
            continue # skip permutation, since we noticed an inconsistency
        
        # increment dangerous block counts of the multiverse
        for sq_id in range(len(tovis)):
            if tovis[sq_id] in multiverse.keys():
                multiverse[tovis[sq_id]] -= perm[sq_id]
            else:
                multiverse[tovis[sq_id]] = -perm[sq_id]
            
    least_dangerous = min(multiverse, key=multiverse.get)
    return f"{least_dangerous[0] + 1} {least_dangerous[1] + 1}"



if __name__ == "__main__":
    
    # region Init
    
    # Size of grid
    seed = random.randint(1, 10000)
    # seed = 4938
    random.seed(seed)
    n = 10
    
    # Number of mines
    n_mines = 10
 
    # The actual values of the grid
    numbers = [[0 for y in range(n)] for x in range(n)] 
    # The apparent values of the grid
    mine_values = [[' ' for y in range(n)] for x in range(n)]
    # The positions that have been flagged
    flags = []
    accounted_flags = []
    accounted_subsets = []
    
    vis = []
    tovis = [(r, c) for r in range(n) for c in range(n)]
    
    # keeping track of unopened neighbors for each block
    _unopeneds = [[[(row-1, col-1), (row-1, col), (row-1, col+1),
                      (row,   col-1),               (row,   col+1),
                      (row+1, col-1), (row+1, col), (row+1, col+1),] 
                    for col in range(n)] for row in range(n)]
    
    unopeneds = [[[]for col in range(n)] for row in range(n)]
    for row in range(n):
        for col in range(n):
            for unopened in _unopeneds[row][col]:
                if (-1 in unopened) or (n in unopened):
                    continue # removing unopened squares outside of border bounds
                unopeneds[row][col].append(unopened)
 
    # Set the mines and values
    numbers = set_mines(numbers, n_mines, n)
    numbers = set_values(numbers, n)
 
    # Display the instructions
    instructions()
    incorrect_msg = "Invalid input"
    
    # endregion Init
         
    # Game loop
    i = 0
    over = False
    while not over:
        for row, col in flags:
            for u_row, u_col in get_adj_coords(row, col, n):
                if ((row, col), (u_row, u_col)) in accounted_flags:
                    continue
                if type(mine_values[u_row][u_col]) is int and mine_values[u_row][u_col] > 0:

                    mine_values[u_row][u_col] -= 1
                    accounted_flags.append(((row, col), (u_row, u_col)))
        
        for coords, dec_num in subsets:
            if coords in accounted_subsets:
                continue
            u_row, u_col = coords
            if type(mine_values[u_row][u_col]) is int and mine_values[u_row][u_col] > 0:
                mine_values[u_row][u_col] -= dec_num
                accounted_subsets.append(coords)
                

            
        print_map(mine_values, n)
 
        # Input from the AI
        inp = solve(i, n, n_mines, mine_values, flags, unopeneds, vis, tovis)
        print()
        print("Got input:" + inp)
        print()
        # sleep(0.1)
        # inp = input("Input your move:")
        i += 1
        if inp == "exit":
            exit()
            
        inp = inp.split() 
         
        # Standard input
        if len(inp) == 2:
 
            # Try block to handle errant input
            try: 
                val = list(map(int, inp))
            except ValueError:
                clear()
                print(incorrect_msg)
                instructions()
                continue
 
        # Flag input
        elif len(inp) == 3:
            if inp[2].lower() != 'f':
                #clear()
                print(incorrect_msg)
                instructions()
                continue
 
            # handle errant input  
            try:
                val = list(map(int, inp[:2]))
            except ValueError:
                #clear()
                print(incorrect_msg)
                instructions()
                continue
 
            # Sanity checks 
            if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
                #clear()
                print(incorrect_msg)
                instructions()
                continue
 
            # Get row and column numbers
            r = val[0] - 1
            col = val[1] - 1 
 
            # If cell already been flagged
            if [r, col] in flags:
                #clear()
                print("Flag already set")
                continue
 
            # If cell already been displayed
            if mine_values[r][col] != ' ':
                #clear()
                print("Value already known")
                continue
 
            # Check the number for flags    
            if len(flags) < n_mines:
                #clear()
                print("Flag set")
 
                # Adding flag to the list
                flags.append([r, col])
                 
                # Set the flag for display
                mine_values[r][col] = 'F'
                
                
                
                if (r, col) not in vis:
                    # adding to visited list
                    vis.append((r, col))
                    # removing from to visit list
                    tovis.remove((r, col))

                # identifying adjascent squares
                u_pairs = get_adj_coords(r, col, n)
                    
                # removing "unopened" status of current square from adjascent squares
                for u_row, u_col in u_pairs:
                    if (r, col) in unopeneds[u_row][u_col]:
                        unopeneds[u_row][u_col].remove((r, col))
                
                continue
            else:
                #clear()
                print("Flags finished")
                continue    
 
        else: 
            #clear()
            print(incorrect_msg)   
            instructions()
            continue
             
 
        # Sanity checks
        if val[0] > n or val[0] < 1 or val[1] > n or val[1] < 1:
            #clear()
            print(incorrect_msg)
            instructions()
            continue
             
        # Get row and column number
        row = val[0]-1
        col = val[1]-1
 
        # Unflag the cell if already flagged
        if [row, col] in flags:
            flags.remove([row, col])
 
        # If landing on a mine, blow up    
        if numbers[row][col] == -1:
            mine_values[row][col] = 'M'
            mine_values = show_mines(mine_values, numbers, n)
            print_map(mine_values, n)
            print(f"Landed on a mine, ended up with an arrow to the knee... better luck next time\nIteration: {i}, seed {seed}")
            over = True
            continue
        # If selecting a cell with atleast 1 mine in neighboring cells  
        else:   
            # registering move by displaying number
            mine_values[row][col] = numbers[row][col]
            if (row, col) not in vis:
                # adding to visited list
                vis.append((row, col))
                # removing from to visit list
                tovis.remove((row, col))
            
                # identifying adjascent squares
                u_pairs = get_adj_coords(row, col, n)
                    
                # removing "unopened" status of current square from adjascent squares
                for u_row, u_col in u_pairs:
                    if (row, col) in unopeneds[u_row][u_col]:
                        unopeneds[u_row][u_col].remove((row, col))
            
            
 
        # Check for game completion 
        if(check_over()):
            mine_values = show_mines(mine_values, numbers, n)
            print_map(mine_values, n)
            print("You win, you deserve cookies!")
            over = True
            continue
 