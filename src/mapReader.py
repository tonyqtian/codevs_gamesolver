'''
Created on May 25, 2012

@author: Tony
'''

class MapReader(object):
    
    def __init__(self, filename = '../data/input001.in'):
        self.level_ready = False
        if filename == 'std':
            line = raw_input()
            self.mapNumber = int(line)
            if self.mapNumber > 0:
                self.map = {}
                self.State = 'readMapInfo'
                self.nextMap = 1
                # start map info reading
                self.readMap()

        else:
            file_handle = open(filename, 'r')
            # read map number
            line = file_handle.readline()
            line = line.strip()
            self.mapNumber = int(line)
            if self.mapNumber > 0:
                self.map = {}
                #State = 'readMap_widthHight'
                # start map info reading
                for i in range(1, self.mapNumber+1):
                    self.nextMap = i-1
                    self.map[i] = {}
                    line = file_handle.readline()
                    line = line.strip()
                    try:
                        (width, height) = line.split()
                    except ValueError:
                        break
                    width = int(width)
                    height = int(height)
                    self.map[i]['mapSize'] = (width, height)
                    self.map[i]['mapLine'] = {}
                    #State = 'readMap_maplines'
                    for this_map_hight in range(0, height):
                        line = file_handle.readline()
                        line = line.strip()
                        self.map[i]['mapLine'][this_map_hight] = line
                    # read level number
                    line = file_handle.readline()
                    line = line.strip()
                    level = int(line)
                    self.map[i]['levelNum'] = level
                    self.map[i]['level'] = {}
                    # expecting an end
                    line = file_handle.readline()
                    if line.strip() == 'END':
                        pass
                    else:
                        print "Reading file error... expecting END, but get ", line
                    #State = 'readLevelInfo'
                    for level_num in range(1, level+1):
                        line = file_handle.readline()
                        line = line.strip()
                        
                        try:
                            (life, money, tower_num, enemy_num) = line.split()
                        except ValueError:
                            break
                        tower_num = int(tower_num)
                        enemy_num = int(enemy_num)
                        self.map[i]['level'][level_num] = {}
                        self.map[i]['level'][level_num]['life'] = int(life)
                        self.map[i]['level'][level_num]['money'] = int(money)
                        self.map[i]['level'][level_num]['tower_num'] = tower_num
                        self.map[i]['level'][level_num]['enemy_num'] = enemy_num
                        
                        self.map[i]['level'][level_num]['tower'] = {}
                        for tower in range(0, tower_num):
                            line = file_handle.readline()
                            line = line.strip()
                            
                            (x, y, strengthen, twr_type) = line.split()
                            self.map[i]['level'][level_num]['tower'][tower] = {}
                            self.map[i]['level'][level_num]['tower'][tower]['position'] = (int(x), int(y))
                            self.map[i]['level'][level_num]['tower'][tower]['strengthen'] = int(strengthen)
                            self.map[i]['level'][level_num]['tower'][tower]['type'] = int(twr_type)
                        
                        self.map[i]['level'][level_num]['enemy'] = {}    
                        for enemy in range(0, enemy_num):
                            line = file_handle.readline()
                            line = line.strip()
                            
                            (x, y, appear_time, enemy_life, mov_time) = line.split()
                            self.map[i]['level'][level_num]['enemy'][enemy] = {}
                            self.map[i]['level'][level_num]['enemy'][enemy]['position'] = (int(x), int(y))
                            self.map[i]['level'][level_num]['enemy'][enemy]['appear_time'] = int(appear_time)
                            self.map[i]['level'][level_num]['enemy'][enemy]['enemy_life'] = int(enemy_life)
                            self.map[i]['level'][level_num]['enemy'][enemy]['mov_time'] = int(mov_time)
                        # expecting an end
                        line = file_handle.readline()
                        if line.strip() == 'END':
                            pass
                        else:
                            print "Reading file error... expecting END, but get ", line
        
    def getMapNumber(self):
        return self.nextMap

    def getNextLevelNumber(self):
        return self.this_level_num
        
    def getMap(self, i):
        return self.map[i]

    def getReaderState(self):
        return self.level_ready
        
    def readMap(self):
        self.level_ready = False
        if self.nextMap <= self.mapNumber:
            i = self.nextMap
            line = raw_input()
            line = line.strip()
            if self.State == 'readMapInfo':
                self.map[i] = {}
                (width, height) = line.split()
                width = int(width)
                height = int(height)
                self.map[i]['mapSize'] = (width, height)
                self.map[i]['mapLine'] = {}
                #self.State = 'readMap_maplines'
                for this_map_hight in range(0, height):
                    line = raw_input()
                    line = line.strip()
                    self.map[i]['mapLine'][this_map_hight] = line
                # read level number
                line = raw_input()
                line = line.strip()
                level = int(line)
                self.map[i]['levelNum'] = level
                self.map[i]['level'] = {}
                # expecting an end
                line = raw_input()
                if line.strip() == 'END':
                    self.State = 'readLevelInfo'
                else:
                    print "Reading file error... expecting END, but get ", line
                self.this_level_num = 1
                
            if self.State == 'readLevelInfo':
            #for level_num in range(1, level+1):
                level_num = self.this_level_num
                line = raw_input()
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
                    line = raw_input()
                    line = line.strip()
                    
                    (x, y, strengthen, twr_type) = line.split()
                    self.map[i]['level'][level_num]['tower'][tower] = {}
                    self.map[i]['level'][level_num]['tower'][tower]['position'] = (int(x), int(y))
                    self.map[i]['level'][level_num]['tower'][tower]['strengthen'] = int(strengthen)
                    self.map[i]['level'][level_num]['tower'][tower]['type'] = int(twr_type)
                
                self.map[i]['level'][level_num]['enemy'] = {}    
                for enemy in range(0, enemy_num):
                    line = raw_input()
                    line = line.strip()
                    
                    (x, y, appear_time, enemy_life, mov_time) = line.split()
                    self.map[i]['level'][level_num]['enemy'][enemy] = {}
                    self.map[i]['level'][level_num]['enemy'][enemy]['position'] = (int(x), int(y))
                    self.map[i]['level'][level_num]['enemy'][enemy]['appear_time'] = int(appear_time)
                    self.map[i]['level'][level_num]['enemy'][enemy]['enemy_life'] = int(enemy_life)
                    self.map[i]['level'][level_num]['enemy'][enemy]['mov_time'] = int(mov_time)
                # expecting an end
                line = raw_input()
                if line.strip() == 'END':
                    self.level_ready = True
                else:
                    print "Reading file error... expecting END, but get ", line
                self.this_level_num += 1
                if self.this_level_num > self.map[i]['levelNum']:
                    # Level cleared, prepare to read next map
                    self.State = 'readMapInfo' 
                    self.nextMap += 1
    
    def printMap(self, this_map):
        (width, height) = self.map[this_map]['mapSize']
        for y in range(0,height):
            this_map_line = self.map[this_map]['mapLine'][y]
            print this_map_line, "     >>this line is ", y

    def readOutput(self, this_map, filename = '../data/sample_output.out'):
        file_handle = open(filename, 'r')
        line = file_handle.readline()
        line = line.strip()
        towerNum = int(line)
        self.tower_loc = set([])
        for cnt in range(towerNum):
            line = file_handle.readline()
            line = line.strip()
            token = line.split()
            x = int(token[0])
            y = int(token[1])
            self.tower_loc.add((x, y))
        print ' '
        (width, height) = self.map[this_map]['mapSize']
        for y in range(0,height):
            this_map_line = self.map[this_map]['mapLine'][y]
            for x in range(len(this_map_line)):
                if (x, y) in self.tower_loc:
                    tmp = this_map_line[0:x]+ 'x' + this_map_line[x+1:]
                    this_map_line = tmp
            print this_map_line, "     >>this line is ", y
        
def main():
    mymaps = MapReader()
    this_map = mymaps.getMapNumber()
    print this_map, "maps loaded."
    print "Map load ready..."
    mymaps.printMap(42)
    mymaps.readOutput(42)
                    
if __name__ == '__main__':
    main()