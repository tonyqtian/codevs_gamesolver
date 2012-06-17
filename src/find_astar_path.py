# A* Shortest Path Algorithm
# http://en.wikipedia.org/wiki/A*
# FB - 201012256
from heapq import heappush, heappop # for priority queue
import math
import time
import random

class node:
    xPos = 0 # x position
    yPos = 0 # y position
    distance = 0 # total distance already travelled to reach the node
    priority = 0 # priority = distance + remaining distance estimate
    def __init__(self, xPos, yPos, distance, priority):
        self.xPos = xPos
        self.yPos = yPos
        self.distance = distance
        self.priority = priority
    def __lt__(self, other): # comparison method for priority queue
        return self.priority < other.priority
    def updatePriority(self, xDest, yDest):
        self.priority = self.distance + self.estimate(xDest, yDest) * 10 # A*
    # give higher priority to going straight instead of diagonally
    def nextMove(self, dirs, d): # d: direction to move
        if dirs == 8 and d % 2 != 0:
            self.distance += 14
        else:
            self.distance += 10
    # Estimation function for the remaining distance to the goal.
    def estimate(self, xDest, yDest):
        xd = xDest - self.xPos
        yd = yDest - self.yPos
        # Euclidian Distance
        d = math.sqrt(xd * xd + yd * yd)
        # Manhattan distance
        # d = abs(xd) + abs(yd)
        # Chebyshev distance
        # d = max(abs(xd), abs(yd))
        return(d)

# A-star algorithm.
# The path returned will be a string of digits of directions.
def pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB):
    closed_nodes_map = [] # map of closed (tried-out) nodes
    open_nodes_map = [] # map of open (not-yet-tried) nodes
    dir_map = [] # map of dirs
    row = [0] * n
    for i in range(m): # create 2d arrays
        closed_nodes_map.append(list(row))
        open_nodes_map.append(list(row))
        dir_map.append(list(row))

    pq = [[], []] # priority queues of open (not-yet-tried) nodes
    pqi = 0 # priority queue index
    # create the start node and push into list of open nodes
    n0 = node(xA, yA, 0, 0)
    n0.updatePriority(xB, yB)
    heappush(pq[pqi], n0)
    open_nodes_map[yA][xA] = n0.priority # mark it on the open nodes map

    # A* search
    while len(pq[pqi]) > 0:
        # get the current node w/ the highest priority
        # from the list of open nodes
        n1 = pq[pqi][0] # top node
        n0 = node(n1.xPos, n1.yPos, n1.distance, n1.priority)
        x = n0.xPos
        y = n0.yPos
        heappop(pq[pqi]) # remove the node from the open list
        open_nodes_map[y][x] = 0
        closed_nodes_map[y][x] = 1 # mark it on the closed nodes map

        # quit searching when the goal is reached
        # if n0.estimate(xB, yB) == 0:
        if x == xB and y == yB:
            # generate the path from finish to start
            # by following the dirs
            path = ''
            while not (x == xA and y == yA):
                j = dir_map[y][x]
                c = str((j + dirs / 2) % dirs)
                path = c + path
                x += dx[j]
                y += dy[j]
            return path

        # generate moves (child nodes) in all possible dirs
        for i in range(dirs):
            xdx = x + dx[i]
            ydy = y + dy[i]
            if not (xdx < 0 or xdx > n-1 or ydy < 0 or ydy > m - 1
                    or the_map[ydy][xdx] == '1' 
                    or the_map[ydy][xdx] == '*' 
                    or closed_nodes_map[ydy][xdx] == 1):
                
                # TO-DO
                # Add diagonal rule for code vs.....
                if dirs == 8:
                    if abs(dx[i]) == abs(dy[i]):
                        #print "Try diagonal move..."
                        if the_map[ydy][x] == '1' or the_map[ydy][x] == '*':
                            #print "Skip ", xdx, ydy, " from ", x, y, "when obstacle ", x, ydy
                            continue
                        if the_map[y][xdx] == '1' or the_map[y][xdx] == '*':
                            #print "Skip ", xdx, ydy, " from ", x, y, "when obstacle ", xdx, y
                            continue
                    
                # generate a child node
                m0 = node(xdx, ydy, n0.distance, n0.priority)
                m0.nextMove(dirs, i)
                m0.updatePriority(xB, yB)
                # if it is not in the open list then add into that
                if open_nodes_map[ydy][xdx] == 0:
                    open_nodes_map[ydy][xdx] = m0.priority
                    heappush(pq[pqi], m0)
                    # mark its parent node direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                elif open_nodes_map[ydy][xdx] > m0.priority:
                    # update the priority
                    open_nodes_map[ydy][xdx] = m0.priority
                    # update the parent direction
                    dir_map[ydy][xdx] = (i + dirs / 2) % dirs
                    # replace the node
                    # by emptying one pq to the other one
                    # except the node to be replaced will be ignored
                    # and the new node will be pushed in instead
                    while not (pq[pqi][0].xPos == xdx and pq[pqi][0].yPos == ydy):
                        heappush(pq[1 - pqi], pq[pqi][0])
                        heappop(pq[pqi])
                    heappop(pq[pqi]) # remove the target node
                    # empty the larger size priority queue to the smaller one
                    if len(pq[pqi]) > len(pq[1 - pqi]):
                        pqi = 1 - pqi
                    while len(pq[pqi]) > 0:
                        heappush(pq[1-pqi], pq[pqi][0])
                        heappop(pq[pqi])       
                    pqi = 1 - pqi
                    heappush(pq[pqi], m0) # add the better node instead
    return '' # if no route found

class AstarSearcher:
    def __init__(self, theMap, this_map, this_level, direc = 4):
        self.dirs = direc # number of possible directions to move on the map
        if self.dirs == 4:
            self.dx = [1, 0, -1, 0]
            self.dy = [0, 1, 0, -1]
        elif self.dirs == 8:
            self.dx = [1, 1, 0, -1, -1, -1, 0, 1]
            self.dy = [0, 1, 1, 1, 0, -1, -1, -1]
        random.seed()
        
        (width, height) = theMap['mapSize']
        self.width = width
        self.height = height
        self.MIN_LEN = max(self.width, self.height) *3 /5
        self.the_map = {}
        for i in range(height): # create empty map
            self.the_map[i] = []
            for j in range(width):
                self.the_map[i].append(theMap['mapLine'][i][j])     
                   
        # get block location: (map scan)
        self.block_loc = set([])
        for y in range(0,height):
            this_map_line = theMap['mapLine'][y]
            #print this_map_line, "this line is ", y
            block_num = this_map_line.count('1')
            for cnt in range(block_num):
                x = this_map_line.find('1')
                if x >= 0:
                    self.block_loc.add((x, y))
                    tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                    #print tmp, " find loc: ", (x, y)
                    this_map_line = tmp
                
        # get target location: (map scan)
        self.target_loc = set([])
        for y in range(1,height-1):
            this_map_line = theMap['mapLine'][y]
            #print this_map_line, "this line is ", y
            target_num = this_map_line.count('g')
            for cnt in range(target_num):
                x = this_map_line.find('g')
                if x >= 0:
                    self.target_loc.add((x, y))
                    tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                    #print tmp, " find loc: ", (x, y)
                    this_map_line = tmp
    
        # get target location: (map scan)
        self.enemy_loc = set([])
        for y in range(1,height-1):
            this_map_line = theMap['mapLine'][y]
            #print this_map_line, "this line is ", y
            enemy_num = this_map_line.count('s')
            for cnt in range(enemy_num):
                x = this_map_line.find('s')
                if x >= 0:
                    self.enemy_loc.add((x, y))
                    tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                    #print tmp, " find loc: ", (x, y)
                    this_map_line = tmp
                
        # get enemy start location:
        self.enemy_show_loc = set([])
        this_enemy_num = theMap['level'][this_level]['enemy_num']
        for cnt in range(this_enemy_num):
            self.enemy_show_loc.add(theMap['level'][this_level]['enemy'][cnt]['position'])
    
        # get built tower location:
        self.tower_loc = set([])
        this_tower_num = theMap['level'][this_level]['tower_num']
        for cnt in range(this_tower_num):
            self.tower_loc.add(theMap['level'][this_level]['tower'][cnt]['position'])
        
        # update map with tower position
        for (x, y) in self.tower_loc:
            self.the_map[y][x] = '*'
        self.tower_added = set([])
        self.tower_delete = set([])
       
    def findMinPathSet(self, the_map = {}, enemy_loc = set([]), target_loc = set([]), verbose = False):
        if the_map == {}:
            the_map = self.the_map
        if enemy_loc == set([]):
            enemy_loc = list(self.enemy_loc)
            random.shuffle(enemy_loc)
        if target_loc == set([]):
            target_loc = list(self.target_loc)
            random.shuffle(target_loc)

        min_enemy_path_set = {}
        for (xA, yA) in enemy_loc:
            this_enemy_route = []
            for (xB, yB) in target_loc:
                if verbose:
                    print 'Start: ', xA, yA
                    print 'Finish: ', xB, yB
                if verbose > 1:
                    t = time.time()
                route = pathFind(the_map, self.width, self.height, \
                                 self.dirs, self.dx, self.dy, xA, yA, xB, yB)
                if verbose > 1:
                    print 'Time to generate the route (seconds): ', time.time() - t
                    print "Route: ", route
                this_enemy_route.append(route)        
            
            pre_distance = 5000
            min_route = ''    
            for route in this_enemy_route:
                this_distance = 0
                for d in route:
                    if self.dirs == 8 and int(d) % 2 != 0:
                        this_distance += 14
                    else:
                        this_distance += 10   
                if verbose > 1:
                    print "This route cost: ", this_distance
                if this_distance < pre_distance: 
                    pre_distance = this_distance
                    min_route = route
            if verbose:
                print "Final route: ", min_route, " cost: ", pre_distance
            # mark the route on the map
            x = xA
            y = yA
            min_enemy_path_set[(xA, yA)] = []
            if len(min_route) > 0:
                for i in range(len(min_route)-1):
                    j = int(min_route[i])
                    x += self.dx[j]
                    y += self.dy[j]
                    min_enemy_path_set[(xA, yA)].append((x, y))
            else:
                if verbose:
                    print "Route searching error: no route found ..."
                    print "Try to reverse tower added..."
                self.reverseTowerAdd()
                break
        return min_enemy_path_set

    def reverseTowerAdd(self):
        try:
            tmp_set = random.sample(self.tower_added, 1)
            for (x, y) in tmp_set:
                if self.the_map[y][x] == '*':
                    self.tower_added.remove((x, y))
                    self.the_map[y][x] = '0'
        except ValueError:
            print "Error: ", ValueError
            #self.formerTowerDeletion()
            
    def getTowerDeletion(self):
        return self.tower_delete
    
    def getTowerAddSet(self):
        return self.tower_added
    
    def formerTowerDeletion(self):
        try:
            ((x,y),) = random.sample(self.tower_loc, 1)
            if self.the_map[y][x] == '*':
                self.tower_loc.remove((x, y))
                self.tower_delete.add((x, y))
                self.the_map[y][x] = '0'
            else:
                self.formerTowerDeletion()
        except ValueError:
            print "Error: ", ValueError
                    
    def addBlockOnPath(self, path_seq):
        path_len = len(path_seq)
        # add at most three position on this path
        # update this map for new added towers
#        front = path_len/4
#        try:
#            (x,y) = path_seq[front]
#            if self.the_map[y][x] == '0':
#                self.tower_added.add((x,y))
#                self.the_map[y][x] = '*'
#        except IndexError:
#            pass
           
        try:
            middle = path_len/2
            (x,y) = path_seq[middle]
            if self.the_map[y][x] == '0':
                self.tower_added.add((x,y))
                self.the_map[y][x] = '*'
        except IndexError:
            pass
                    
#        try:
#            back = path_len*3/5
#            (x,y) = path_seq[back]
#            if self.the_map[y][x] == '0':
#                self.tower_added.add((x,y))
#                self.the_map[y][x] = '*'
#        except IndexError:
#            pass
        
    def searchBestTarget(self, exclude_position = set([]), verbose = False):   

        target_loc = self.target_loc.different(exclude_position)
        
        enemy_path_sum_set = {}
        for (xB, yB) in target_loc:
            this_enemy_route = []
            for (xA, yA) in self.enemy_loc:
                if verbose:
                    print 'Start: ', xA, yA
                    print 'Finish: ', xB, yB
                if verbose > 1:
                    t = time.time()
                route = pathFind(self.the_map, self.width, self.height, \
                                 self.dirs, self.dx, self.dy, xA, yA, xB, yB)
                if verbose > 1:
                    print 'Time to generate the route (seconds): ', time.time() - t
                    print "Route: ", route
                this_enemy_route.append(route)        
            
            distance_sum = 0
            for route in this_enemy_route:
                this_distance = 0
                for d in route:
                    if self.dirs == 8 and int(d) % 2 != 0:
                        this_distance += 14
                    else:
                        this_distance += 10   
                if verbose > 1:
                    print "This route cost: ", this_distance
                distance_sum += this_distance
            enemy_path_sum_set[(xB, yB)] = distance_sum
        
        xB = 0
        yB = 0
        max_sum = 0
        for (x, y) in enemy_path_sum_set:
            if enemy_path_sum_set[(x, y)] > max_sum:
                xB = x
                yB = y
                max_sum = enemy_path_sum_set[(x, y)]
        
        if max_sum == 0:
            print "Error in finding best target..."
            return (0, 0)    
        else:
            return (xB, yB)        
                     
    def getEnoughPath(self, verbose = False):
        cur_enemy_path_set = self.findMinPathSet(verbose = verbose)
        for this_pos in cur_enemy_path_set:
            if len(cur_enemy_path_set[this_pos]) < self.MIN_LEN:
                if len(cur_enemy_path_set[this_pos]) > 0:
                    self.addBlockOnPath(cur_enemy_path_set[this_pos])
        cur_enemy_path_set = self.findMinPathSet(verbose = verbose)
        if verbose:
            self.printPathList(cur_enemy_path_set)
        no_enough_path = True
        while(no_enough_path):
            no_enough_path = False
            for this_pos in cur_enemy_path_set:
                if len(cur_enemy_path_set[this_pos]) < self.MIN_LEN:
                    no_enough_path = True
                    if len(cur_enemy_path_set[this_pos]) > 0:
                        self.addBlockOnPath(cur_enemy_path_set[this_pos])
                        cur_enemy_path_set = self.findMinPathSet(verbose = verbose)
                        if verbose:
                            self.printPathList(cur_enemy_path_set)
                    elif len(self.tower_added) > 0:
                        self.MIN_LEN = self.MIN_LEN *3 /4
                        self.reverseTowerAdd()
                        cur_enemy_path_set = self.findMinPathSet(verbose = verbose)
                        if verbose:
                            self.printPathList(cur_enemy_path_set)
                    elif len(self.tower_loc) > 0:
                        self.MIN_LEN = self.MIN_LEN /2
                        self.formerTowerDeletion()
                        cur_enemy_path_set = self.findMinPathSet(verbose = verbose)
                        if verbose:
                            self.printPathList(cur_enemy_path_set)
                    else:
                        if verbose:
                            print "Error in get long enough path."
                            print "Searching terminated..."
                            self.printPathList(cur_enemy_path_set)
                        no_enough_path = False
                    break
        return cur_enemy_path_set

    def printPathList(self, enemy_path_set, holdOn = False):
        for this_pos in enemy_path_set:
            path_list = enemy_path_set[this_pos]
            if len(path_list) > 0:
                for i in range(len(path_list)):
                    (x, y) = path_list[i]
                    self.the_map[y][x] = 3
            else:
                print "Error: no route to print ..."
                return False
                
            # display the map with the route added
            if holdOn == False:
                print "Map for enemy start at: ", this_pos
            else:
                print "Combined map: "
            for y in range(self.height):
                for x in range(self.width):
                    xy = self.the_map[y][x]
                    if xy == '0':
                        print '.', # space
                    elif xy == '1':
                        print '1', # obstacle
                    elif xy == '*':
                        print '*', # tower
                    elif xy == 2 or xy == 's':
                        print 'S', # start
                    elif xy == 3:
                        print '>', # route
                    elif xy == 4 or xy == 'g':
                        print 'G', # finish
                print
            
            #clear
            if holdOn == False:
                for y in range(self.height):
                    for x in range(self.width):
                        if self.the_map[y][x] == 3:
                            self.the_map[y][x] = '0'  
        return True          

    def printTowerMap(self, enemy_path_set, construct_area):
        for this_pos in enemy_path_set:
            path_list = enemy_path_set[this_pos]
            for tmp_pos in path_list:
                (x, y) = tmp_pos
                self.the_map[y][x] = 3
        for tmp_pos in construct_area:
            (x, y) = tmp_pos
            self.the_map[y][x] = '*'
        print "Constructed map: "
        for y in range(self.height):
            for x in range(self.width):
                xy = self.the_map[y][x]
                if xy == '0':
                    print '.', # space
                elif xy == '1':
                    print '1', # obstacle
                elif xy == '*':
                    print '*', # tower
                elif xy == 2 or xy == 's':
                    print 'S', # start
                elif xy == 3:
                    print '>', # route
                elif xy == 4 or xy == 'g':
                    print 'G', # finish
            print
                        
    def getSquareLoc(self, position):
        temp_set = set([])
        (x, y) = position
        temp_set.add((x-1,y))
        temp_set.add((x+1,y))
        temp_set.add((x,y-1))
        temp_set.add((x,y+1))
        temp_set.add((x-1,y+1))
        temp_set.add((x-1,y-1))
        temp_set.add((x+1,y+1))
        temp_set.add((x+1,y-1))
        return temp_set
        
    def towerConstruct(self, enemy_path_set):
        enemy_show_area = set([])
        targer_area = set([])
        intersection_set = set([])
        raw_path_area = set([])
        enemy_path_dict = {}
        
        for this_pos in enemy_path_set:
            path_list = enemy_path_set[this_pos]
            for tmp_pos in path_list:
                for tmp in self.getSquareLoc(tmp_pos):
                    raw_path_area.add(tmp)
                try:
                    enemy_path_dict[tmp_pos] += 1
                except KeyError:
                    enemy_path_dict[tmp_pos] = 1
        
        for tmp_pos in enemy_path_dict:
            if enemy_path_dict[tmp_pos] > 0:
                intersection_set.add(tmp_pos)
                
        raw_path_area = raw_path_area.difference(self.block_loc)
        raw_path_area = raw_path_area.difference(self.target_loc)
        raw_path_area = raw_path_area.difference(self.enemy_loc)
        raw_path_area = raw_path_area.difference(self.tower_loc)
        raw_path_area = raw_path_area.difference(self.tower_added)
        halo_path_area = raw_path_area.difference(set(enemy_path_dict))
        
#        self.tower_added = self.tower_added.difference(set(enemy_path_dict))
#        tmp_set = self.tower_loc.intersection(set(enemy_path_dict))
#        for elem in tmp_set:
#            self.tower_delete.add(elem)
            
        return halo_path_area
        
def main():
    # MAIN
    dirs = 8 # number of possible directions to move on the map
    if dirs == 4:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
    elif dirs == 8:
        dx = [1, 1, 0, -1, -1, -1, 0, 1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]
    
    n = 30 # horizontal size of the map
    m = 30 # vertical size of the map
    the_map = []
    row = [0] * n
    for i in range(m): # create empty map
        the_map.append(list(row))
    
    # fillout the map with a '+' pattern
    for x in range(n / 8, n * 7 / 8):
        the_map[m / 2][x] = 1
    for y in range(m/8, m * 7 / 8):
        the_map[y][n / 2] = 1
    
    # randomly select start and finish locations from a list
    sf = []
    sf.append((0, 0, n - 1, m - 1))
    sf.append((0, m - 1, n - 1, 0))
    sf.append((n / 2 - 1, m / 2 - 1, n / 2 + 1, m / 2 + 1))
    sf.append((n / 2 - 1, m / 2 + 1, n / 2 + 1, m / 2 - 1))
    sf.append((n / 2 - 1, 0, n / 2 + 1, m - 1))
    sf.append((n / 2 + 1, m - 1, n / 2 - 1, 0))
    sf.append((0, m / 2 - 1, n - 1, m / 2 + 1))
    sf.append((n - 1, m / 2 + 1, 0, m / 2 - 1))
    (xA, yA, xB, yB) = random.choice(sf)
    
    print 'Map size (X,Y): ', n, m
    print 'Start: ', xA, yA
    print 'Finish: ', xB, yB
    t = time.time()
    route = pathFind(the_map, n, m, dirs, dx, dy, xA, yA, xB, yB)
    print 'Time to generate the route (seconds): ', time.time() - t
    print 'Route:'
    print route
    
    # mark the route on the map
    if len(route) > 0:
        x = xA
        y = yA
        the_map[y][x] = 2
        for i in range(len(route)):
            j = int(route[i])
            x += dx[j]
            y += dy[j]
            the_map[y][x] = 3
        the_map[y][x] = 4
    
    # display the map with the route added
    print 'Map:'
    for y in range(m):
        for x in range(n):
            xy = the_map[y][x]
            if xy == 0:
                print '.', # space
            elif xy == 1:
                print '1', # obstacle
            elif xy == 2:
                print 'S', # start
            elif xy == 3:
                print '+', # route
            elif xy == 4:
                print 'G', # finish
        print

def mapTest(input_map = 1, input_level = 1):
    dirs = 8 # number of possible directions to move on the map
    if dirs == 4:
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]
    elif dirs == 8:
        dx = [1, 1, 0, -1, -1, -1, 0, 1]
        dy = [0, 1, 1, 1, 0, -1, -1, -1]
        
    import mapReader
    mymaps = mapReader.MapReader()
    this_map = mymaps.getMapNumber()
    print this_map, "maps loaded."
    print "Map load ready..."
    
    this_map = input_map
    this_level = input_level
    print "Map ", this_map, "   Level ",  this_level
    theMap = mymaps.getMap(this_map)
    (width, height) = theMap['mapSize']
    print 'Map size (X,Y): ', width, height
    
#    n = width # horizontal size of the map
#    m = height # vertical size of the map
    the_map = {}
    for i in range(height): # create empty map
        the_map[i] = []
        for j in range(width):
            the_map[i].append(theMap['mapLine'][i][j])

    # get block location: (map scan)
    block_loc = set([])
    for y in range(0,height):
        this_map_line = theMap['mapLine'][y]
        #print this_map_line, "this line is ", y
        block_num = this_map_line.count('1')
        for cnt in range(block_num):
            x = this_map_line.find('1')
            if x >= 0:
                block_loc.add((x, y))
                tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                #print tmp, " find loc: ", (x, y)
                this_map_line = tmp
    #print "Block Location: ", block_loc
            
    # get target location: (map scan)
    target_loc = set([])
    for y in range(1,height-1):
        this_map_line = theMap['mapLine'][y]
        #print this_map_line, "this line is ", y
        target_num = this_map_line.count('g')
        for cnt in range(target_num):
            x = this_map_line.find('g')
            if x >= 0:
                target_loc.add((x, y))
                tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                #print tmp, " find loc: ", (x, y)
                this_map_line = tmp
    #print "Target Location: ", target_loc

    # get target location: (map scan)
    enemy_loc = set([])
    for y in range(1,height-1):
        this_map_line = theMap['mapLine'][y]
        #print this_map_line, "this line is ", y
        enemy_num = this_map_line.count('s')
        for cnt in range(enemy_num):
            x = this_map_line.find('s')
            if x >= 0:
                enemy_loc.add((x, y))
                tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                #print tmp, " find loc: ", (x, y)
                this_map_line = tmp
                    
    enemy_show_loc = set([])
    this_enemy_num = theMap['level'][this_level]['enemy_num']
    for cnt in range(this_enemy_num):
        enemy_show_loc.add(theMap['level'][this_level]['enemy'][cnt]['position'])
    
    tower_loc = set([])
    this_tower_num = theMap['level'][this_level]['tower_num']
    for cnt in range(this_tower_num):
        tower_loc.add(theMap['level'][this_level]['tower'][cnt]['position'])    
    
    for (x, y) in tower_loc:
        the_map[y][x] = '*'
          
    for (xA, yA) in enemy_show_loc:
        this_enemy_route = []
        for (xB, yB) in target_loc:
            print 'Start: ', xA, yA
            print 'Finish: ', xB, yB
            #t = time.time()
            route = pathFind(the_map, width, height, dirs, dx, dy, xA, yA, xB, yB)
            #print 'Time to generate the route (seconds): ', time.time() - t
            #print "Route: ", route
            this_enemy_route.append(route)
        
        pre_distance = 2000
        min_route = ''    
        for route in this_enemy_route:
            this_distance = 0
            for d in route:
                if dirs == 8 and int(d) % 2 != 0:
                    this_distance += 14
                else:
                    this_distance += 10   
            #print "This route cost: ", this_distance
            if this_distance < pre_distance: 
                pre_distance = this_distance
                min_route = route
        print "Final route: ", min_route, " cost: ", pre_distance
        # mark the route on the map
        if len(min_route) > 0:
            x = xA
            y = yA
            the_map[y][x] = 2
            for i in range(len(min_route)):
                j = int(min_route[i])
                x += dx[j]
                y += dy[j]
                the_map[y][x] = 3
            the_map[y][x] = 4
        else:
            print "Route finding error: no route fund ..."
            
        # display the map with the route added
        print 'Map:'
        for y in range(height):
            for x in range(width):
                xy = the_map[y][x]
                if xy == '0':
                    print '.', # space
                elif xy == '1':
                    print '1', # obstacle
                elif xy == '*':
                    print '*', # tower
                elif xy == 2 or xy == 's':
                    print 'S', # start
                elif xy == 3:
                    print '>', # route
                elif xy == 4 or xy == 'g':
                    print 'G', # finish
            print
        
        #clear
        for y in range(height):
            for x in range(width):
                xy = the_map[y][x]
                if xy == 3:
                    the_map[y][x] = '0'

def pathTest(input_map = 1, input_level = 1):
    import mapReader
    mymaps = mapReader.MapReader()
    this_map = mymaps.getMapNumber()
    print this_map, "maps loaded."
    print "Map load ready..."
    
    this_map = input_map
    this_level = input_level
    print "Map ", this_map, "   Level ",  this_level
    theMap = mymaps.getMap(this_map)
    (width, height) = theMap['mapSize']
    print 'Map size (W,H): ', width, height
    
    print "Start path searcher..."
    mySearcher = AstarSearcher(theMap, this_map, this_level)
    print "Search for long enough path..."
    enemy_path_set = mySearcher.getEnoughPath(verbose = True)
    print "Print found path..."
    mySearcher.printPathList(enemy_path_set)
    #mySearcher.printPathList(enemy_path_set, holdOn = True)
    print "Evaluate tower construction..."
    contruct_area = mySearcher.towerConstruct(enemy_path_set)
    mySearcher.printTowerMap(enemy_path_set, contruct_area)
    
if __name__ == "__main__":
    #main()
    input_map = 2
    input_level = 1
    #mapTest(input_map, input_level)
    pathTest(input_map, input_level)