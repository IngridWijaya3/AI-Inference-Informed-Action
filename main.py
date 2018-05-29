import numpy as np
import random
import sys
import time
import tkinter as tk


def updateCellInCanvas(canvas, size, value, y, x):
    if value == -5:
        # querying cell
        rect(canvas, size, (x, y), (x+1, y+1),'blue')
        canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='?')
    if value == -4:
        # unknown cells
        rect(canvas, size, (x, y), (x+1, y+1),'grey')
        #canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='?')
    if value == -1:
        # mine (by user)
        rect(canvas, size, (x, y), (x+1, y+1),'red')
        canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='M')
    if value == -2:
        # cell marked as flag (by our program)
        rect(canvas, size, (x, y), (x+1, y+1),'orange')
        canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='M')
    if value == -3:
        # cell marked as cleared (by our program)
        rect(canvas, size, (x, y), (x+1, y+1),'green')
        canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='C')  
    if value >= 0:
        # cell was cleared and displays number of surrounding mines
        rect(canvas, size, (x, y), (x+1, y+1),'white')  
        canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text=str(value))
    canvas.update_idletasks()
    canvas.update()
    time.sleep(0.05)

def drawCanvas(canvas, matrix, size):
    
    for (x,y), value in np.ndenumerate(matrix):
                  
        if value == -4 or value == -5:
            # unknown cells
            rect(canvas, size, (x, y), (x+1, y+1),'grey')
            #canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='?')
        if value == -1:
            # mine (by user)
            rect(canvas, size, (x, y), (x+1, y+1),'red')
            canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='M')
        if value == -2:
            # cell marked as flag (by our program)
            rect(canvas, size, (x, y), (x+1, y+1),'orange')
            canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='M')
        if value == -3:
            # cell marked as cleared (by our program)
            rect(canvas, size, (x, y), (x+1, y+1),'green')
            canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text='C')  
        if value >= 0:
            # cell was cleared and displays number of surrounding mines
            rect(canvas, size, (x, y), (x+1, y+1),'white')  
            canvas.create_text((size*(2*x + 1)/2, size*(2*y + 1)/2), text=str(value))
    #tk.Button(self.root, text="Quit", command=quit).pack()   
    #self.root.protocol("WM_DELETE_WINDOW", self.on_closing)   
    #self.root.mainloop()
   

def rect(canvas, size, a, b, color='black'):
    (x1, y1) = a
    (x2, y2) = b
    x1 *= size
    y1 *= size
    x2 *= size
    y2 *= size
    canvas.create_rectangle((x1, y1, x2, y2), fill=color)
    canvas.update_idletasks()
    
def setProbSurroundingCells(prob, x,y, prob_matrix):
    width, height = np.shape(prob_matrix)
    startRow = 0
    endRow = width - 1
    startCol = 0
    endCol = height - 1
    if x - 1 >= 0:
        startRow = x - 1
    if x + 1 < width:
        endRow = x + 1
    if y - 1 >= 0:
        startCol = y - 1
    if y + 1 < height:
        endCol = y + 1

    for i in range(startRow, endRow + 1):
        for j in range(startCol, endCol + 1):
            if (i == x and j == y):
                continue
            if prob_matrix[i][j] != 0 and prob_matrix[i][j]!= 1:
                if prob_matrix[i][j] == -1:
                    prob_matrix [i][j] = prob     
                else:
                    prob_matrix [i][j]+=prob
                    
def setValueSurroundingCells(val, x,y, grid, canvas, cellsize):
    width, height = np.shape(grid)
    startRow = 0
    endRow = width - 1
    startCol = 0
    endCol = height - 1
    if x - 1 >= 0:
        startRow = x - 1
    if x + 1 < width:
        endRow = x + 1
    if y - 1 >= 0:
        startCol = y - 1
    if y + 1 < height:
        endCol = y + 1

    for i in range(startRow, endRow + 1):
        for j in range(startCol, endCol + 1):
            if (i == x and j == y):
                continue
            if grid[i][j] == -4:
                grid[i][j] = val
                updateCellInCanvas(canvas, cellsize, val, i, j)

def GetWarningsSurrounding(row, col, grid):
    rows, cols = np.shape(grid)
    startRow = 0
    endRow = rows - 1
    startCol = 0
    endCol = cols - 1
    warningCells = []
    if row - 1 >= 0:
        startRow = row - 1
    if row + 1 < rows:
        endRow = row + 1
    if col - 1 >= 0:
        startCol = col - 1
    if col + 1 < cols:
        endCol = col + 1

    for i in range(startRow, endRow + 1):
        for j in range(startCol, endCol + 1):
            if ((i == row and j == col)):
                continue
            if (grid[i][j] > 0 and grid[i][j] <= 8):
                warningCells.append((i, j))
    return warningCells

def GetSurroundingBasedOnType(row, col, grid, typeofcell):
    # -1 mine
    # -2 flag
    # -3 safe cell
    # -4 unknown
    rows, cols = np.shape(grid)
    startRow = 0
    endRow = rows - 1
    startCol = 0
    endCol = cols - 1
    warningCells = []
    if row - 1 >= 0:
        startRow = row - 1
    if row + 1 < rows:
        endRow = row + 1
    if col - 1 >= 0:
        startCol = col - 1
    if col + 1 < cols:
        endCol = col + 1

    for i in range(startRow, endRow + 1):
        for j in range(startCol, endCol + 1):
            if ((i == row and j == col)):
                continue
            if (grid[i][j] == typeofcell):
                warningCells.append((i, j))
    return warningCells

def flagUnknownSurrounding(row, col, grid, prob_matrix, canvas, cellsize):
    # -1 mine
    # -2 flag
    # -3 safe cell
    # -4 unknown
    rows, cols = np.shape(grid)
    startRow = 0
    endRow = rows - 1
    startCol = 0
    endCol = cols - 1
    if row - 1 >= 0:
        startRow = row - 1
    if row + 1 < rows:
        endRow = row + 1
    if col - 1 >= 0:
        startCol = col - 1
    if col + 1 < cols:
        endCol = col + 1

    for i in range(startRow, endRow + 1):
        for j in range(startCol, endCol + 1):
            if ((i == row and j == col)):
                continue
            if (grid[i][j] == -4):
                grid[i][j] = -2
                prob_matrix[i][j] = 1
                updateCellInCanvas(canvas, cellsize, -2, i, j)
                
def clearUnknownSurrounding(row, col, grid, prob_matrix, canvas, cellsize):
    # -1 mine
    # -2 flag
    # -3 safe cell
    # -4 unknown
    rows, cols = np.shape(grid)
    startRow = 0
    endRow = rows - 1
    startCol = 0
    endCol = cols - 1
    if row - 1 >= 0:
        startRow = row - 1
    if row + 1 < rows:
        endRow = row + 1
    if col - 1 >= 0:
        startCol = col - 1
    if col + 1 < cols:
        endCol = col + 1

    for i in range(startRow, endRow + 1):
        for j in range(startCol, endCol + 1):
            if ((i == row and j == col)):
                continue
            if (grid[i][j] == -4):
                grid[i][j] = -3
                prob_matrix[i][j] = 0  
                updateCellInCanvas(canvas, cellsize, -3, i, j)              
   

def updateMinesAndClear(prob_matrix, grid, canvas, cellsize):
    for (x,y), value in np.ndenumerate(grid):
        if value > 0:            
            # get surrounding (already) marked mines
            mines = GetSurroundingBasedOnType(x, y, grid, -2)
            unknown = GetSurroundingBasedOnType(x, y, grid, -4)
            unknown_c = GetSurroundingBasedOnType(x, y, grid, -3)
            if (len(unknown) + len(unknown_c))==(value - len(mines)):
                # mark unknown surrounding as mines
                flagUnknownSurrounding(x, y, grid, prob_matrix, canvas, cellsize)
            elif (len(mines)==value):
                clearUnknownSurrounding(x, y, grid, prob_matrix, canvas, cellsize)      

def updateProbabilityMatrix(prob_matrix, grid, canvas, cellsize):
    #-1 mine
    #-2 flag
    #-3 safe cell
    #-4 unknown
    for (x,y), value in np.ndenumerate(grid):
        if value == 0:
            setProbSurroundingCells(0, x,y, prob_matrix)
            setValueSurroundingCells(-3, x, y, grid, canvas, cellsize)
        elif value == 8:
            setProbSurroundingCells(1, x, y, prob_matrix)
            setValueSurroundingCells(-2, x, y, grid, canvas, cellsize)
        elif value == -3:
            continue
        else:
            setProbSurroundingCells(value/64, x, y, prob_matrix)
    
if __name__ == '__main__':
    debug = input('Use default grid (Y or N)? ')
    if (debug == 'Y' or debug=='y'):
        inputFile = 'in.txt'
    else:
        inputFile = input('Enter input file name (grid must be square): ')
    inputGrid = np.loadtxt(inputFile, dtype='i', delimiter=' ')
    print(inputGrid)
    height, width = np.shape(inputGrid)
    if (height != width):
        sys.exit('The grid must be square.')
    cellsize = (int) (500/max((height, width)));
    master = tk.Tk();               
    master.title("Solution")  
    canvasGenerated = tk.Canvas(master, width=width*cellsize, height=height*cellsize)
    canvasGenerated.grid(row=0, column=0)
    grid = np.ones((width, height))*-4
    prob_matrix = np.ones((width, height))*-1
    drawCanvas(canvasGenerated, np.transpose(grid), cellsize)
    first = True;
    start = time.time()
    while True:
        # First query
        if first:
            x = random.sample(range(width), 1).pop()
            y = random.sample(range(height), 1).pop()
            grid[x][y] = -5 # mark for current query
            updateCellInCanvas(canvasGenerated, cellsize, -5, x, y)            
            grid[x][y] = inputGrid[x][y]
            updateCellInCanvas(canvasGenerated, cellsize, grid[x][y], x, y)
            prob_matrix[x][y] = 0
            first = False
        if grid[x][y] == -1:
            updateCellInCanvas(canvasGenerated, cellsize, -1, x, y)
            end = time.time() - start
            ret = input('Oops! Touched a mine. Press Enter for final output.')
            break
        if (grid == -4).sum()==0:
            drawCanvas(canvasGenerated, np.transpose(grid), cellsize)
            canvasGenerated.update_idletasks()
            canvasGenerated.update()
            end = time.time() - start
            ret = input('Grid cleared! Press Enter for final output.')
            break
        # Attempt to solve...
        # update matrix probability
        updateProbabilityMatrix(prob_matrix, grid, canvasGenerated, cellsize)
        
        updateMinesAndClear(prob_matrix, grid, canvasGenerated, cellsize)
        # -1 mine
        # -2 flag
        # -3 safe cell
        # -4 unknown
        if (grid == -3).sum()>0:
            # We have some "safe-to-ask" cells
            for (x,y), value in np.ndenumerate(grid):
                if grid[x][y]==-3: 
                    updateCellInCanvas(canvasGenerated, cellsize, -5, x, y) # mark for current query
                    grid[x][y] = inputGrid[x][y]
                    updateCellInCanvas(canvasGenerated, cellsize, grid[x][y], x, y)
                    prob_matrix[x][y] = 0
        elif (grid == -4).sum()>0:
            # We still have unknown cells but no more "safe-to-ask" cells
            probp = np.copy(prob_matrix)
            probp[grid > -2] = 1 # for the sake of selection: we don't want to select mines that we already know (i.e. -2(marked as mine), >=0(known cells); set their probability to 1
            probp[prob_matrix == -4] = 0 # for the sake of selection: set to 0 unknown probability cells
            xrange,yrange = np.where(probp == probp.min()) # select cells with minimum probability
            idx = random.sample(range(xrange.size), 1).pop() # select one of the minimum probability cells at random
            x = xrange[idx]
            y = yrange[idx]
            updateCellInCanvas(canvasGenerated, cellsize, -5, x, y) # mark for current query
            grid[x][y] = inputGrid[x][y]
            updateCellInCanvas(canvasGenerated, cellsize, grid[x][y], x, y)
    print("------FINAL OUTPUT------")
    rows, cols = np.shape(grid)
    
    print("Number of mines in original grid: " + str((inputGrid == -1).sum()))
    
    print("Number of flags: " + str((grid == -2).sum()))
    print("Original number of squares: " + str(height*width))
    
    print("Number of uncovered squares: " + str((grid == -4).sum()))
    print("Time taken: " + str(end) + " seconds")
    end = input("Exit program by pressing Enter.")
    master.destroy()