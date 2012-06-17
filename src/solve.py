'''
Created on May 25, 2012

@author: Tony
'''
import sys
#import time

class MapReader(object):
    
    def __init__(self):
        self.level_ready = False
        self.handle = sys.stdin
        line = self.handle.readline()
        self.mapNumber = int(line)
        if self.mapNumber > 0:
            self.map = {}
            self.State = 'readMapInfo'
            self.thisMap = 0
            # start map info reading
            self.readMap()
        
    def getMapNumber(self):
        return self.thisMap

    def getNextLevelNumber(self):
        return self.this_level_num
        
    def getMap(self, i):
        return self.map[i]

    def getReaderState(self):
        return self.level_ready
        
    def readMap(self):
        self.level_ready = False
        if self.thisMap < self.mapNumber:
            if self.State == 'readMapInfo':
                self.thisMap += 1
                i = self.thisMap
                self.map[i] = {}
                
                line = self.handle.readline()
                line = line.strip() 
                (width, height) = line.split()
                width = int(width)
                height = int(height)
                self.map[i]['mapSize'] = (width, height)
                self.map[i]['mapLine'] = {}
                #self.State = 'readMap_maplines'
                for this_map_height in range(0, height):
                    line = self.handle.readline()
                    line = line.strip()
                    self.map[i]['mapLine'][this_map_height] = line
                # read level number
                line = self.handle.readline()
                line = line.strip()
                level = int(line)
                self.map[i]['levelNum'] = level
                self.map[i]['level'] = {}
                # expecting an end
                line = self.handle.readline()
                if line.strip() == 'END':
                    self.State = 'readLevelInfo'
                else:
                    print "Read map error... expecting END, but get ", line
                    sys.stdout.flush()
                    raise RuntimeError
                self.this_level_num = 0
                
            if self.State == 'readLevelInfo':
            #for level_num in range(1, level+1):
                i = self.thisMap
                self.this_level_num += 1
                level_num = self.this_level_num
                
                line = self.handle.readline()
                line = line.strip()
                (life, money, tower_num, enemy_num) = line.split()
                tower_num = int(tower_num)
                enemy_num = int(enemy_num)
                self.map[i]['level'][level_num] = {}
                self.map[i]['level'][level_num]['life'] = int(life)
                self.map[i]['level'][level_num]['money'] = int(money)
                self.map[i]['level'][level_num]['tower_num'] = tower_num
                self.map[i]['level'][level_num]['enemy_num'] = enemy_num
                
                self.map[i]['level'][level_num]['tower'] = {}
                for tower in range(0, tower_num):
                    line = self.handle.readline()
                    line = line.strip()
                    
                    (x, y, strengthen, twr_type) = line.split()
                    self.map[i]['level'][level_num]['tower'][tower] = {}
                    self.map[i]['level'][level_num]['tower'][tower]['position'] = (int(x), int(y))
                    self.map[i]['level'][level_num]['tower'][tower]['strengthen'] = int(strengthen)
                    self.map[i]['level'][level_num]['tower'][tower]['type'] = int(twr_type)
                
                self.map[i]['level'][level_num]['enemy'] = {}    
                for enemy in range(0, enemy_num):
                    line = self.handle.readline()
                    line = line.strip()
                    
                    (x, y, appear_time, enemy_life, mov_time) = line.split()
                    self.map[i]['level'][level_num]['enemy'][enemy] = {}
                    self.map[i]['level'][level_num]['enemy'][enemy]['position'] = (int(x), int(y))
                    self.map[i]['level'][level_num]['enemy'][enemy]['appear_time'] = int(appear_time)
                    self.map[i]['level'][level_num]['enemy'][enemy]['enemy_life'] = int(enemy_life)
                    self.map[i]['level'][level_num]['enemy'][enemy]['mov_time'] = int(mov_time)
                # expecting an end
                line = self.handle.readline()
                if line.strip() == 'END':
                    self.level_ready = True
                else:
                    print "Read level error... expecting END, but get ", line
                    sys.stdout.flush()
                    raise RuntimeError
                
                if self.this_level_num >= self.map[i]['levelNum']:
                    # Level cleared, prepare to read next map
                    #print "this level num: ", self.this_level_num
                    #print "map i levelNum: ", self.map[i]['levelNum']
                    self.State = 'readMapInfo' 

def simpleBuild(theMap, this_map, this_level):
    
    (width, height) = theMap['mapSize']
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
    #print "Target Location: ", target_loc
            
    # get enemy start location:
    enemy_show_loc = set([])
    this_enemy_num = theMap['level'][this_level]['enemy_num']
    for cnt in range(this_enemy_num):
        enemy_show_loc.add(theMap['level'][this_level]['enemy'][cnt]['position'])
    #print "Enemy show up Location: ", enemy_loc

    # get built tower location:
    tower_loc = set([])
    this_tower_num = theMap['level'][this_level]['tower_num']
    for cnt in range(this_tower_num):
        tower_loc.add(theMap['level'][this_level]['tower'][cnt]['position'])
    #print "Built tower Location: ", tower_loc

    # start loc choosing...
    candidate_loc = set([])
    for (x, y) in target_loc:
        candidate_loc.add((x-1, y-1))
        candidate_loc.add((x+1, y-1))
        candidate_loc.add((x-1, y+1))
        candidate_loc.add((x+1, y+1))
        
        if this_map >= 10:
            candidate_loc.add((x-2, y-2))
            candidate_loc.add((x-2, y-1))
            candidate_loc.add((x-1, y-2))
            
            candidate_loc.add((x+2, y-2))
            candidate_loc.add((x+2, y-1))
            candidate_loc.add((x+1, y-2))
            
            candidate_loc.add((x-2, y+2))
            candidate_loc.add((x-2, y+1))
            candidate_loc.add((x-1, y+2))
            
            candidate_loc.add((x+2, y+2))
            candidate_loc.add((x+2, y+1))
            candidate_loc.add((x+1, y+2))  
        
        block_loc.add((x-1, y))
        block_loc.add((x+1, y))
        block_loc.add((x, y-1))
        block_loc.add((x, y+1)) 
         
        block_loc.add((x-2, y))
        block_loc.add((x+2, y))
        block_loc.add((x, y-2))
        block_loc.add((x, y+2))  
        
        block_loc.add((x-3, y))
        block_loc.add((x+3, y))
        block_loc.add((x, y-3))
        block_loc.add((x, y+3))          
    for (x, y) in enemy_show_loc:
        candidate_loc.add((x-1, y-1))
        candidate_loc.add((x+1, y-1))
        candidate_loc.add((x-1, y+1))
        candidate_loc.add((x+1, y+1))
        
        candidate_loc.add((x-2, y-2))
        candidate_loc.add((x-2, y-1))
        candidate_loc.add((x-1, y-2))
        
        candidate_loc.add((x+2, y-2))
        candidate_loc.add((x+2, y-1))
        candidate_loc.add((x+1, y-2))
        
        candidate_loc.add((x-2, y+2))
        candidate_loc.add((x-2, y+1))
        candidate_loc.add((x-1, y+2))
        
        candidate_loc.add((x+2, y+2))
        candidate_loc.add((x+2, y+1))
        candidate_loc.add((x+1, y+2))  
        
        block_loc.add((x-1, y))
        block_loc.add((x+1, y))
        block_loc.add((x, y-1))
        block_loc.add((x, y+1))
        
        block_loc.add((x-2, y))
        block_loc.add((x+2, y))
        block_loc.add((x, y-2))
        block_loc.add((x, y+2)) 
            
        block_loc.add((x-3, y))
        block_loc.add((x+3, y))
        block_loc.add((x, y-3))
        block_loc.add((x, y+3))                
    # range checking:
    for (x, y) in candidate_loc:
        if x < 1:
            block_loc.add((x, y))
        if y < 1:
            block_loc.add((x, y))
        if x > width-1:
            block_loc.add((x, y))
        if y > height-1:
            block_loc.add((x, y))
    #print "Candidate Location: ", candidate_loc
    myLoc = candidate_loc.difference(block_loc)
    
    # Map based modification
    manual_block_list = set([])
    special_tower = {}
    if this_map == 1:
        myLoc.add((14,6))
    if this_map == 10:
        myLoc.add((14,6))
        myLoc.add((14,9))
    if this_map == 15:
        myLoc.add((6,3))
    if this_map == 16:
        myLoc.add((9,1))
        myLoc.add((9,2))
        myLoc.add((9,3))
        myLoc.add((9,4))
        myLoc.add((13,3))
        myLoc.add((14,3))
        myLoc.add((9,6))
        myLoc.add((11,6))
    if this_map == 17:
        myLoc.add((13,13))
        myLoc.add((6,13))
        myLoc.add((9,13))
    if this_map == 19:
        myLoc.add((4,12))
        myLoc.add((11,10))
        myLoc.add((18,7))
        myLoc.add((17,9))
        myLoc.add((17,10))
        manual_block_list.add((5,11))
    if this_map == 20:
        myLoc.add((5,5))
        myLoc.add((6,6))
        myLoc.add((6,9))
    if this_map == 24:
        manual_block_list.add((4,9))
        manual_block_list.add((4,10))
    if this_map == 26:
        myLoc.add((12,14))
        myLoc.add((10,17))
        myLoc.add((13,7))
        myLoc.add((12,6))
        myLoc.add((11,2))
        myLoc.add((12,2))
        myLoc.add((9,3))
        myLoc.add((9,9))
        myLoc.add((11,10))
        myLoc.add((11,20))
        myLoc.add((12,10))
        myLoc.add((10,13))
        myLoc.add((2,13))
    if this_map == 28:
        myLoc.add((6,15))
        myLoc.add((7,15))
        myLoc.add((8,14))
        myLoc.add((3,11))
        myLoc.add((10,11))
        myLoc.add((13,15))
        myLoc.add((13,17))
        manual_block_list.add((6,13))
        manual_block_list.add((6,12))
        manual_block_list.add((5,19))
        manual_block_list.add((6,19))
        manual_block_list.add((8,19))
        manual_block_list.add((10,13))
    if this_map == 29:
        myLoc.add((6,9))
        myLoc.add((7,11))
        myLoc.add((9,6))
        myLoc.add((7,2))
        myLoc.add((7,4))
        myLoc.add((10,4))            
    if this_map == 30:
        myLoc.add((10,2))
        myLoc.add((11,3))
        myLoc.add((7,8))
        myLoc.add((8,9))
        myLoc.add((9,8))
        myLoc.add((14,1))
        myLoc.add((13,5))
    if this_map == 32:
        myLoc.add((3,14))
        myLoc.add((2,17))
        myLoc.add((4,18))
        myLoc.add((7,18))
    if this_map == 34:
        myLoc.add((1,10))
        myLoc.add((1,17))
        myLoc.add((7,13))
        myLoc.add((8,12))  
        myLoc.add((11,2))    
    if this_map == 35:
        myLoc.add((11,1))
        myLoc.add((12,2))
        myLoc.add((4,8))
        myLoc.add((5,9))
        myLoc.add((5,7))
        myLoc.add((14,4))
        myLoc.add((14,5))
        myLoc.add((14,6))
        myLoc.add((14,7))            
    if this_map == 36:
        myLoc.add((12,10))
        myLoc.add((8,13))
        myLoc.add((10,8))
        special_tower[(12,9)] = (3,2)
        special_tower[(12,8)] = (3,1)
        special_tower[(12,11)] = (3,1)
#            special_tower[(8,12)] = (3,1)
#            special_tower[(9,12)] = (3,2)
#            special_tower[(8,13)] = (3,1)
    if this_map == 37:
        myLoc.add((1,10))
        myLoc.add((13,15))
        myLoc.add((14,14))
        myLoc.add((19,19))
        myLoc.add((20,19))
        myLoc.add((4,5))
        myLoc.add((4,6))
        myLoc.add((4,7))
        myLoc.add((4,8))
        myLoc.add((4,9))
        myLoc.add((4,10))
        myLoc.add((4,12))
        myLoc.add((7,5))
        myLoc.add((9,5))
        special_tower[(7,3)] = (3,1)
    if this_map == 38:
        myLoc.add((4,16))
        myLoc.add((4,18))
        myLoc.add((5,17))
        myLoc.add((2,10))
        myLoc.add((3,11)) 
        myLoc.add((5,13))
        myLoc.add((6,13))   
        myLoc.add((10,16))
        myLoc.add((12,16))
        myLoc.add((11,15))
        myLoc.add((10,17))
        myLoc.add((12,17))
        special_tower[(10,17)] = (3,1)
        special_tower[(10,19)] = (3,1)
    if this_map == 40:
        myLoc.add((13,11))
        myLoc.add((9,7))
        myLoc.add((10,7))
        myLoc.add((10,8))
        manual_block_list.add((12,6))
    if this_map == 41:
        myLoc.add((5,11))
        myLoc.add((6,11))
    if this_map == 42:
        myLoc.add((5,12))
        myLoc.add((4,20))
        myLoc.add((8,7))
        myLoc.add((11,12))
        myLoc.add((11,13))
        manual_block_list.add((2,11))
        manual_block_list.add((3,11))
    if this_map == 43:
        myLoc.add((1,7))
        myLoc.add((9,6))
        special_tower[(2,9)] = (3,1)
    if this_map == 44:
        myLoc.add((6,10))
        myLoc.add((7,11))
        myLoc.add((4,10))
        myLoc.add((5,7))
        myLoc.add((6,7))
        myLoc.add((6,9))
        special_tower[(17,6)] = (3,1)
    if this_map == 45:
        myLoc.add((11,4))
        myLoc.add((13,4))
        myLoc.add((10,13))
    if this_map == 46:
        myLoc.add((11,13))
        myLoc.add((10,14))
        myLoc.add((11,15))      
        special_tower[(13,15)] = (3,2)
        special_tower[(12,12)] = (3,2)      
    if this_map == 47:
        myLoc.add((17,10))      
        special_tower[(15,10)] = (3,2)  
    if this_map == 48:
        myLoc.add((7,12)) 
        myLoc.add((5,12)) 
        myLoc.add((6,11))   
        special_tower[(7,2)] = (3,2)      
                                      
    myLoc = myLoc.difference(manual_block_list)
    myLoc = myLoc.difference(target_loc)
    myLoc = myLoc.difference(enemy_show_loc)
    myLoc = myLoc.difference(tower_loc)
    #print "My Location choose: ", myLoc
    #print "This map %d, this level %d" % (this_map, this_level)    
    print len(myLoc)
    if len(special_tower):
        for (x, y) in myLoc:
            if special_tower.has_key((x,y)):
                (stren, type_) = special_tower[(x,y)]
                print "%d %d %d %d" % (x, y, stren, type_)
            else:
                print "%d %d 3 0" % (x, y)
    else:
        for (x, y) in myLoc:
            print "%d %d 3 0" % (x, y)
    sys.stdout.flush()
    return True
                    
def main():
    simple_map_list = []
    
    import find_astar_path as astar 
    #print "Program start..."
    mymaps = MapReader()
    #print mymaps.getMapNumber()
    while(mymaps.getReaderState()):
        #TO-DO
        this_map = mymaps.getMapNumber()
        this_level = mymaps.getNextLevelNumber()
        print "Map ", this_map, "   Level ",  this_level
        theMap = mymaps.getMap(this_map)
        state = False
        
        if this_map in simple_map_list:
            state = simpleBuild(theMap, this_map, this_level)
        
        if state == False:
            mySearcher = astar.AstarSearcher(theMap, this_map, this_level)
            enemy_path_set = mySearcher.getEnoughPath(verbose = False)
            contruct_area = mySearcher.towerConstruct(enemy_path_set)
            tower_add_set = mySearcher.getTowerAddSet()
            tower_delete_set = mySearcher.getTowerDeletion()
            
            # standard output
            print len(contruct_area)+len(tower_add_set)+len(tower_delete_set)
            for (x, y) in contruct_area:
                print "%d %d 2 0" % (x, y)
            for (x, y) in tower_add_set:
                print "%d %d 0 0" % (x, y)
            for (x, y) in tower_delete_set:
                print "%d %d 0 3" % (x, y)
            sys.stdout.flush()
            state = True
            
        #state = simpleBuild(theMap, this_map, this_level)
        #time.sleep(1)
        #print "Start read next..."
        if state:
            mymaps.readMap()
        else:
            raise RuntimeError
        
    
if __name__ == "__main__":
    main()