import os
def loadImages(fileName):
    return os.path.join("content", fileName + ".png")

def mapPath(file_name: str) -> str:
    return os.path.join("content", file_name + ".txt")

def readMap(file_name: str):
    map = []
    file_path = mapPath(file_name)
    with open(file_path, 'r') as f:
        text_line = f.readline().strip("\n")
        while text_line != "":
            row_char_arr = text_line.split(",")
            row_int_arr = []
            for char in row_char_arr:
                row_int_arr.append(int(char))
            map.append(row_int_arr)
            text_line = f.readline().strip("\n")
    return map