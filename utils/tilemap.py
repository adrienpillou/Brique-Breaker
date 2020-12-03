import csv
from os import path

# Tilemap class used to load .csv file

class Tilemap():
    def __init__(self, file_path=""):
        self.file_path = file_path
        self.map = []
        self.cols = 0
        self.rows = 0
        if(self.file_path != "" and not self.file_path is None):
            self.read_map()
    
    # Set .csv asset file
    def set_file(self, file_path):
        self.file_path = file_path
        self.read_map()

    # Read .csv file
    def read_map(self):
        self.map = []
        self.rows = 0
        self.cols = 0
        if(self.file_path == '' or self.file_path is None):
            return
        if not path.exists(self.file_path):
            return
        with open(self.file_path, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter = ',', quotechar = '|')
            self.cols = len(next(reader))
            csvfile.seek(0)
            for row in reader:
                self.rows+=1
                self.map.append(row)
            csvfile.close()
    
    # Return tile key at a given position
    def get_tile_key(self, position):
        if(len(self.map)==0):
            return -1
        (c,r) = position
        return self.map[r][c]

    # Return tilemap grid based content
    def get_tile_map(self):
        return self.map
