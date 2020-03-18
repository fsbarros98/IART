"""
Couse: Artificial Intelligence EIC0029
Authors: Fátima Barros up201608444 and Miguel Ferreira up201606158
Created on 13/03/2020
"""




    
with open("example.txt") as file:
    data=file.readlines()


# =============================================================================
def edgeoccupied (data, r, c):
    edge1= data[0]
    edge2= data[r-1]
    edge3= data[0][0]
    edge4= data[0][c-1]
    for x in range(1,r):
        edge3= edge3 + data[x][0]
        edge4= edge4 + data[x][c-1]
    if ('#' in edge1 and '#' in edge2 and '#' in edge3 and '#' in edge4):
        return True
    return False

def is_connected (data, r,c):
    for y in range (c):
        if (data[0][y] == '#'):
            if y == 0:
                if (data[1][0]== '.' and data[0][1]== '.'):
                    return False  
            if y == c-1:
                if (data[1][c-1]== '.' and data[0][c-2]== '.'):
                    return False  
            if (data[0][y-1]== '.' and data[0][y+1]=='.' and data[1][y]=='.'):
                return False
        if (data[r-1][y] == '#'):
            if y == 0:
                if (data[r-2][0]== '.' and data[r-1][1]== '.'):
                    return False
            if y == c-1:
                if (data[r-2][c-1]== '.' and data[r-1][c-2]== '.'):
                    return False
            if (data[r-1][y-1]== '.' and data[r-1][y+1]=='.' and data[r-2][y]=='.'):
                return False
    for x in range (1,r-1):
        if (data[x][0] == '#'):
            if (data[x-1][0] == '.' and data[x+1][0] == '.' and data[x][1] == '.'):
                return False
        if (data[x][c-1] == '#'): 
            if (data[x-1][c-1] == '.' and data[x+1][c-1] == '.' and data[x][c-2] == '.'):
                return False 
    for x in range(1,r-1):
        for y in range(1,c-1):
            if (data[x][y]== '#'):
                if (data[x-1][y] == '.' and data[x+1][y] == '.' and data[x][y-1] == '.' and data[x][y+1] == '.'):
                    return False
    return True

def has_hole (data, r,c):
    for x in range(1,r-1):
        for y in range (1,c-1):
            if (data[x][y] == '.'):
                if (data[x-1][y] == '#' and data[x+1][y] == '#' and data[x][y-1] == '#' and data[x][y+1] == '#'):
                    return True
    return False
# =============================================================================


a=edgeoccupied(data,3,3)
print(is_connected(data,3,3))
