#Version 2 is nearly the same as version 1, but all the bugs are gone.  Now a
#clear and readable path is found.
#
#This is an example of the A* pathfinding algorithm I wrote in Python.  This
#program is primarly based on Abraham L. Howell's ER1 Mapper made specifically
#for the ER1 robot.  His program was written in Visual Basic, so I tried to
#"translate" it to Python as best I can.  All credit goes to him for the basic
#code I used as a general guide to create this.  You are free to use, edit and
#distribute this as long as credit is given where appropriate.
#
#The code is very basic right now.  You create a map in the grid below; it can
#be any size as long as if it stays a rectangle or square (it does not have to
#be one, but it is significantly easier if it is).  This grid is basically a
#list within a list: lists a through e are the rows and they are in list "map".
#The bottom-left cell is reached by typing "map[0][0]".  The first x and y
#coordinates are 0 (so if you have 5 rows, the bottom is row 0 and the top is
#row 4).  You enter the x and y coordinates of the start and goal cells to the
#"start" and "target" variables appropriately (see below).  You then run the
#program and it finds a path to the start to goal cell.  It then prints the
#entire map again with the path marked.  That is all it does for now; it finds
#a path.  Other details about this code can be discovered by reading this code
#or Howell's original code/documentation.

a = [0, 0, 0, 0, 0, 0, 0, 0]
b = [1, 1, 1, 1, 1, 1, 1, 0]   #0 means cell is blocked and 1 means cell is
c = [1, 1, 1, 1, 1, 1, 1, 0]   #unblocked.  When accessing a cell, type y-
d = [0, 0, 1, 1, 1, 1, 1, 0]   #coordinate first, then the x-coordinate.  like:
e = [0, 0, 0, 0, 0, 0, 0, 0]   #"map[4][0]" to access the top left cell in a.
map = [e,                   #list 0
       d,                   #list 1
       c,                   #list 2
       b,                   #list 3
       a]                   #list 4

openlist = []                           #open list is empty
closedlist = []                         #closed list is empty
targetX = 6                             #goal cell X coordinate
targetY = 1                             #goal cell Y coordinate
startX = 0                              #start X coordiante
startY = 3                              #start Y coordinate
numpasses = 0           #Used to count how many times the while-loop looped.

#These are the heuristic constants.  If Dg > Dh, more cells are analyzed and a
#more ideal path is found.  If Dh >= Dg, less cells are analyzed and a path is
#found quicker.
Dg = 1
Dh = 1

maxValX = 7                             #x value of a cell cannot be greater
maxValY = 4                             #y value of a cell cannot be greater

#--------------------------------------------------------------------
#This part of the code creates a 2-dimensional array for storing parent cells.
#For example: Pcell[2][3] = [2, 2].  It has the same dimensions and size as the
#above map, so no "cell is out of range" errors can occur.  It works the same as
#the map above; y value first and x second.  Example: Pcell[y][x] = [NewX, NewY]

ap = [0, 0, 0, 0, 0, 0, 0, 0]
bp = [0, 0, 0, 0, 0, 0, 0, 0]
cp = [0, 0, 0, 0, 0, 0, 0, 0]
dp = [0, 0, 0, 0, 0, 0, 0, 0]
ep = [0, 0, 0, 0, 0, 0, 0, 0]
Pcell = [ep, dp, cp, bp, ap]

#--------------------------------------------------------------------
#this part of the code establishes the telnet connection to the RCC and is
#independent and unrelated to the A* algorithm or finding a path (it is only
#used to physically move the robot after the path is found).

import telnetlib
import time
import string

HOST = "localhost"

print "\nOpening Telnet session to ER1 GUI."
tn = telnetlib.Telnet(HOST, 9000)
print "Opened session.\n"

def evocon (cmd, timeout=1):
          a=''
          if cmd=='events':
                 tn.write("%s\n" % cmd)
                 time.sleep(.1)
                 a=tn.read_until("\n", timeout)
                 print a
                 if a != '':
                        while a!= '':
                               a=tn.read_until("\n", timeout)
                               print a
          tn.write("%s\n" % cmd)
          return tn.read_until("\n", timeout)

#---------------------------------------------------------------------
#These are the mathamatical heuristics, used to calculate the so-called G,
#H and F scores of a cell.

def G(a):
    answerG = Dg * (abs(a[0] - startX) + abs(a[1] - startY))
    return answerG

def H(a):
    Hscore = Dh * (abs(a[0] - targetX) + abs(a[1] - targetY))
    return Hscore

def F(a):
    Fscore = G(a) + H(a)
    return Fscore

#----------------------------------------------------------------------
#When the goal cell is found, print map with marked cells.
def ShowPath():
    #Display that a path was found and how many loops were made to find it.
    print "Path found! ", "Number of loops =", numpasses

    map[targetY][targetX] = 5        #mark goal cell with integer 5, so you
                                     #can tell where the path ends.
    curCellX = targetX               #Start with target cell
    curCellY = targetY

    intPathLength = 0           #Path length is 0 (it has not been found yet)

    #Find the parent of the goal cell, then find that cell's parent and so on,
    #until, the current cell is the start cell.  This trail of parent cells is
    #the found path.
    while curCellX != startX or curCellY != startY:
        intPathLength = intPathLength + 1       #Record the length of the path
        P = Pcell[curCellY][curCellX]
        curCellX = P[0]
        curCellY = P[1]
        map[curCellY][curCellX] = 4  #Mark each parent cell with a 4

    print "Path length =", intPathLength

    map.reverse()                    #reverse list "map", so when printed in the
    for i in map:                    #for: loop, it comes out right-side up
        print i

def NoSolutionFound():
    print "No path found, the goal cell is unreachable"

#----------------------------------------------------------------------
#This part of the code is the actual A* algorithm.

curCellX = startX                             #start cell is the current cell
curCellY = startY

closedlist.append([startX, startY])           #add start cell to closed list

rest = 0                              #start search.  I set up a dummy variable,
while not rest:                       #so it would loop.

      numpasses = numpasses + 1       #Counts how many times it has looped.

      NcellX = curCellX
      NcellY = curCellY + 1
      ScellX = curCellX
      ScellY = curCellY - 1
      EcellX = curCellX + 1
      EcellY = curCellY
      WcellX = curCellX -1
      WcellY = curCellY

      #check if north cell is in range, that is, not under 0 or over max value
      if NcellX >= 0 and NcellY >= 0 and NcellX <= maxValX and NcellY <= maxValY:
         #check if it's on the closed list or blocked.  Its blocked if the cell
         #NcellX and NcellY represent is = 0, open is = 1    
         if map[NcellY][NcellX] != 0 and closedlist.count([NcellX, NcellY]) == 0:
             #if it's not on the openlist, add it and set parent.
             if openlist.count([NcellX, NcellY]) == 0:
                 openlist.append([NcellX, NcellY])
                 Pcell[NcellY][NcellX] = [curCellX, curCellY]
             else:
                 #check if path from current cell has a lower G value
                 if G([curCellX, curCellY]) + Dg < G([NcellX, NcellY]):
                     #if it is, set parent to current cell and recalculate G&F scores
                     #for this cell
                     Pcell[NcellY][NcellX] = [curCellX, curCellY]
                     G([NcellX, NcellY]) == G([curCellX, curCellY]) + Dg
                     F([NcellX, NcellY]) == G([NcellX, NcellY]) + H([NcellX, NcellY])

      #repeat above, only for south, east and west cells.
      if ScellX >= 0 and ScellY >= 0 and ScellX <= maxValX and ScellY <= maxValY:
         if map[ScellY][ScellX] != 0 and closedlist.count([ScellX, ScellY]) == 0:
              if openlist.count([ScellX, ScellY]) == 0:
                  openlist.append([ScellX, ScellY])
                  Pcell[ScellY][ScellX] = [curCellX, curCellY]
              else:
                  if G([curCellX, curCellY]) + Dg < G([ScellX, ScellY]):
                      Pcell[ScellY][ScellX] = [curCellX, curCellY]
                      G([ScellX, ScellY]) == G([curCellX, curCellY]) + Dg
                      F([ScellX, ScellY]) == G([ScellX, ScellY]) + H([ScellX, ScellY])

      if EcellX >= 0 and EcellY >= 0 and EcellX <= maxValX and EcellY <= maxValY:
         if map[EcellY][EcellX] != 0 and closedlist.count([EcellX, EcellY]) == 0:
              if openlist.count([EcellX, EcellY]) == 0:
                  openlist.append([EcellX, EcellY])
                  Pcell[EcellY][EcellX] = [curCellX, curCellY]
              else:
                  if G([curCellX, curCellY]) + Dg < G([EcellX, EcellY]):
                      Pcell[EcellY][EcellX] = [curCellX, curCellY]
                      G([EcellX, EcellY]) == G([curCellX, curCellY]) + Dg
                      F([EcellX, EcellY]) == G([EcellX, EcellY]) + H([EcellX, EcellY])

      if WcellX >= 0 and WcellY >= 0 and WcellX <= maxValX and WcellY <= maxValY:
         if map[WcellY][WcellX] != 0 and closedlist.count([WcellX, WcellY]) == 0:
              if openlist.count([WcellX, WcellY]) == 0:
                  openlist.append([WcellX, WcellY])
                  Pcell[WcellY][WcellX] = [curCellX, curCellY]
              else:
                  if G([curCellX, curCellY]) + Dg < G([WcellX, WcellY]):
                      Pcell[WcellY][WcellX] = [curCellX, curCellY]
                      G([WcellX, WcellY]) == G([curCellX, curCellY]) + Dg
                      F([WcellX, WcellY]) == G([WcellX, WcellY]) + H([WcellX, WcellY])

      if len(openlist) == 0:                         #if openlist is empty, exit
          NoSolutionFound()                          #loop; there is no solution.
          break

      #now we find the cell on the openlist with the lowest F score and set it
      #as the current cell.
      smallest = F(openlist[0])         #Assume the first member is the smallest.
      for r in openlist:
          if F(r) <= smallest:          #If an item on the list is smaller than
              smallest = F(r)           #the first item, set it as the new smallest
              NewX = r[0]
              NewY = r[1]           #Keep looping until a smaller value is found

      #add the cell you just selected to the closed list and remove it from the
      #open list.        
      closedlist.append([NewX, NewY])
      openlist.remove([NewX, NewY])

      #Find out if the cell you put in the closed list is the target cell
      #else, mark the current cell, so when you print "map", you can see it
      #was analyzed (analyzed cells are marked with the number 3)
      if NewX == targetX and NewY == targetY:
          ShowPath()
          break

      if NewX > -1 and NewY > -1 and NewX < maxValX and NewY < maxValY:
          map[NewY][NewX] = 3

      curCellX = NewX
      curCellY = NewY
