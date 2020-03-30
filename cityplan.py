"""
Couse: Artificial Intelligence EIC0029
Authors: Fátima Barros up201608444 and Miguel Ferreira up201606158
Created on 13/03/2020
Updated until 18/03/2020
"""
import math
import copy
from random import shuffle
from random import seed
import random
import time


###############################################################################
###############################################################################
#empty_matrix(i,j) returns an empty matrix of size (i,j) - list type: of points '.'
def empty_matrix(i,j):
    matrix=[]
    for x in range(i):
        matrix.append(['.' for y in range(j)])
    return matrix

#manhattan_distance
def manhattan_distance(x,y):
    return (math.fabs(x[0]-y[0])+math.fabs(x[1]-y[1]))

###############################################################################
###############################################################################
#class used in final plan of the city
class CityPlan:
    def __init__(self,H,W,dist):
        self.H=H #rows
        self.W=W #columns
        self.dist=dist
        self.resi_building=[] #list of building projects that are residental
        self.util_building=[] #list of building projects that are utilities
        
        self.plan=empty_matrix(self.H,self.W)
        
        self.value=0
        
        
    #to preform submission file    
    def get_building_numbers(self): 
        return (len(self.resi_building)+len(self.util_building))



        
    #calculate final value (optimization process)    
    def calculate_value(self):
        value=0
        utility_services=[]
     
        
        #change filtered_cell according to coordinates - necessary for optimization processes
        #this works fast and smoothly
        for util in self.util_building:
            util.filtered_cell=[]
            for x in range(util.h):
                for y in range(util.w):
                    if util.plan[x][y]=='#':
                        util.filtered_cell.append((util.coordinates[(util.w*x)+y])) 
    
    
    #THIS IS VERY SLOW - main reason: while in the subcity, maximum distance was ~20, here, maximum distance is
    #too high, we need to optimize this in order to only calculate between buildings in a certain area
                            
        
        for resi_building in self.resi_building:   
            for util_building in self.util_building:
                if abs(resi_building.coordinates[0][0]-util_building.coordinates[0][0])<5 and abs(resi_building.coordinates[0][1]-util_building.coordinates[0][1])<5:
                    if self.verify_distance(util_building,resi_building):
                        if util_building.service not in utility_services:
                            utility_services.append(util_building.service)                  
                else:
                    pass
            value += resi_building.capacity * len(utility_services)
            utility_services=[]
        
        self.value=value
        return value
        
    def verify_distance(self,proj_A,proj_B):
        distance=None
        for point_1 in proj_A.filtered_cell:
            for point_2 in proj_B.filtered_cell:
                distance=manhattan_distance(point_1, point_2)
                if distance <= self.dist: 
                    return True
        return False
        
   
    
    
    
###############################################################################
###############################################################################
class SubCity:
    def __init__(self,H,W,residental_projects,utility_projects,dist):
        self.H=H
        self.W=W
        self.residental_projects=residental_projects
        self.utility_projects=utility_projects
        self.dist=dist
        #initialize variables
        self.resi_building=[]
        self.util_building=[]
        
        self.sub_cities=[]
        
        #construct empty plan
        self.plan=empty_matrix(self.H,self.W)
        
    
    #find free cells in the city - all of them
    def get_free_cells(self):
        free_cell=[]
        for i in range(self.H):
            for j in range(self.W):
                if self.plan[i][j]=='.':
                    free_cell.append((i,j))
        return free_cell
    
    
#The distance between two buildings A and B on the city plan is defined as the minimum Manhattan distance
#between any cell a occupied by the building A and any cell b occupied by the building B (regardless of
#whether other cells between a and b are occupied and by which building(s)).    
    
    #verify if distance between two projects is smaller/equal to maximum walking distance
    def verify_distance(self,proj_A,proj_B):
        distance=None
        for point_1 in proj_A.filtered_cell:
            for point_2 in proj_B.filtered_cell:
                distance=manhattan_distance(point_1, point_2)
                if distance <= self.dist:#if any of the points are in less distance than self.dist, then true
                    return True
        return False
        
                
    #returns last free cell in city plan (matrix)
    def get_last_free_cell(self):
        for i in range(self.H):
            for j in range(self.W):
                if self.plan[self.H-1-i][self.W-1-j]=='.':
                    return (self.H-1-i, self.W-1-j)
        return False #if there's no free cell
    
    
    def build_scenario(self):
        city_plan=CityPlan(self.H,self.W,self.dist) #create cityplan of size H and W
        #copy residental and utility projects to new variables (same names)
        residental_projects=copy.copy(self.residental_projects) 
        utility_projects=copy.copy(self.utility_projects)

        finish=False #flag 
        
        while not finish:
            free_cell=self.get_free_cells() #gets all free cells in the city
            empty_cell=False
            
            
            #resi
            if residental_projects: #are there any residental_projects?
                residental_project=copy.copy(residental_projects.pop())                 
                #takes 1 project from residental_projects and copies it to residental_project, 
                #eliminating it from the list of projects
                
                residental_projects_not_construct=True
                
                while residental_projects_not_construct and free_cell:
                    #see construct_building for more information
                    updated_cells,filtered_cell=self.construct_building(free_cell.pop(0),residental_project)
                    if updated_cells: #if cells are updared
                        residental_project.coordinates=updated_cells #add them to residental_projects.coordinates
                        residental_project.filtered_cell=filtered_cell #add filtered_cell (occupied cell) to residental_project.filtered_cell
                        city_plan.resi_building.append(residental_project) #append the project to city_plan.resi_building
                        city_plan.plan=self.plan #update city map
                        residental_projects_not_construct=False
                       
                        break
            else: #if there aren't residental_projects
                empty_cell=True
                
                #if there aren't residental_projects, and there is free cells, and the first free cell isn't the last one, copy residental_projects
            if not residental_projects and free_cell and not free_cell[0]==self.get_last_free_cell():
                residental_projects=copy.copy(self.residental_projects)
            
            #util
                #same structure as residental, see comments above
            free_cell=self.get_free_cells()
            if utility_projects:
                utility_project=copy.copy(utility_projects.pop())
                
                utility_projects_not_construct=True
                
                while utility_projects_not_construct and free_cell:
                    updated_cells,filtered_cell=self.construct_building(free_cell.pop(0),utility_project)
                    if updated_cells:
                        utility_project.coordinates=updated_cells
                        utility_project.filtered_cell=filtered_cell
                        city_plan.util_building.append(utility_project)
                        city_plan.plan=self.plan
                        utility_projects_not_construct=False
                        
                        break
                else:
                    empty_cell=True
                        
            if not utility_projects and free_cell and not free_cell[0]==self.get_last_free_cell():
                utility_projects=copy.copy(self.utility_projects)

            if empty_cell:
                finish=True
                break
        return city_plan                    
            
        
    def get_utility_building(self):
        pass
    
#For every residential building with a capacity r placed on the map, the submission will earn r points for
#every type of utility service accessible to the residents of that building. (If there are two or more utility
#buildings providing the same type of service, the residential building still earns only r points for this type of
#service.)   
    #this function builds the scenario of the city and then calculates it's value through the description above
    def construct(self):
        city_plan=self.build_scenario()
        value=0
        utility_services=[]
        for resi_building in city_plan.resi_building:   
            for util_building in city_plan.util_building:
                if self.verify_distance(util_building,resi_building):
                    if util_building.service not in utility_services:
                        utility_services.append(util_building.service)
            value += resi_building.capacity * len(utility_services)
            resi_building.utility_services=utility_services
            utility_services=[]
        city_plan.value=value
        
        return city_plan
    
    
#consctructs building if it can fit the plan: receives self,startpoint and the project
    def construct_building(self,startpoint,project): 
        updated_cell=[]
        filtered_cell=[]
        
        def undolog_plan(): #functions that solves the plan if project doens't fit: turns updated cells into free cells
            for x_cell,y_cell in updated_cell:
                self.plan[x_cell][y_cell]='.'
                
        for x,y in project.coordinates:
            _x,_y=(x+startpoint[0],y+startpoint[1])
            
            try:
                if not self.plan[_x][_y]=='.': #if the cell _x,_y is not free, undolog_plan()
                    undolog_plan()
                    return False, False
                else:
                    updated_cell.append((_x,_y)) #else, append updated_cell _x,_y
                    self.plan[_x][_y]=project.plan[x][y] #update city plan cells
                    if project.plan[x][y]=='#':
                        filtered_cell.append((_x,_y)) #if project cell is occupied, then added to ffiltered_cell
            except IndexError as e: #errors in index do undolog_plan()
                undolog_plan()
                return False, False
            
        return updated_cell,filtered_cell
                    

###############################################################################
###############################################################################
#most important class where city is created with the help of class subcity
class CityInfo:
    def __init__(self,H,W,dist,bplans): 
        #H=rows, W=columns, dist=maximum walking distance, bplans=building plans
        self.H=H
        self.W=W
        self.dist=dist
        self.bplans=bplans
        #initialize some variables
        self.projects=[]
        self.residental_projects=[]
        self.utility_projects=[]
        
        self.resi_building=[]
        self.util_building=[]
        self.plan=empty_matrix(self.H,self.W)
        self.value=0
        
    @classmethod #splits data from the file and gives attributes to class
    def specs(cls,data):
        data=data.split(' ') #returns elements in the first line of the file
        H,W,dist,bplans=[int(i) for i in data]
        return cls(H,W,dist,bplans)
    
    
    #adds project to specific project list, being aware of project type
    def add_project(self,project):
        self.projects.append(project)
        
        if isinstance(project,Residental_Project):
            self.residental_projects.append(project)

            
        elif isinstance(project,Utility_Project):
            self.utility_projects.append(project)

    #find free cells in the city
    def get_free_cells(self):
        free_cell=[]
        for i in range(self.H):
            for j in range(self.W):
                if self.plan[i][j]=='.':
                    free_cell.append((i,j))
        return free_cell
    

    #verify if distance between two projects is smaller/equal to maximum walking distance
    def verify_distance(self,proj_A,proj_B):
        distance=None
        for point_1 in proj_A.filtered_cell:
            for point_2 in proj_B.filtered_cell:
                distance=math.fabs(point_1[0]-point_2[0])+math.fabs(point_1[1]-point_2[1])
                if distance <= self.dist:
                    return True
        return False
                
    #returns last free cell in city
    def get_last_free_cell(self):
        for i in range(self.H):
            for j in range(self.W):
                if self.plan[self.H-1-i][self.W-1-j]=='.':
                    return (self.H-1-1, self.W-1-j)
        return False #if there's no free cell
    
    
    #for more information on this, see build_scenario in class SubCity
    #consctruct a scenario for building the city, copies information and goes from that
    def build_scenario(self):
        city_plan=CityPlan(self.H,self.W,self.dist)
        residental_projects=copy.copy(self.residental_projects)
        utility_projects=copy.copy(self.utility_projects)

        finish=False #flag
        
        while not finish:
            free_cell=self.get_free_cells()
            empty_cell=False
            
            if residental_projects:
               
                residental_project=residental_projects.pop() #takes argument, updates lisst
              
                residental_projects_not_construct=True
                
                while residental_projects_not_construct and free_cell:
                    updated_cells,filtered_cell=self.construct_building(free_cell.pop(0),residental_project)
                    if updated_cells:
                        residental_project.coordinates=updated_cells
                        residental_project.filtered_cell=filtered_cell
                        city_plan.resi_building.append(residental_project)
                        city_plan.plan=self.plan
                        residental_projects_not_construct=False
                        break
            else:
                empty_cell=True
                
            if not residental_projects and free_cell and not free_cell[0]==self.get_last_free_cell():
                residental_projects=copy.copy(self.residental_projects)
                
            free_cell=self.get_free_cells()
            
            if utility_projects:

                utility_project=utility_projects.pop()
                
                utility_projects_not_construct=True
                
                while utility_projects_not_construct and free_cell:
                    updated_cells, filtered_cell=self.construct_building(free_cell.pop(0),utility_project)
                    if updated_cells:
                        utility_project.coordinates=updated_cells
                        utility_project.filtered_cell=filtered_cell
                        city_plan.util_building.append(utility_project)
                        city_plan.plan=self.plan
                        utility_projects_not_construct=False
                        break
                else:
                    empty_cell=True
                
            
            if empty_cell:
                finish=True
                break
        return city_plan
                                               
            
     
    def get_utility_building(self):
        pass
        
    #receives self and _list of SubCity type args   -- see function construct  
    def unit_city(self,_list):
        city_plan= CityPlan(self.H,self.W,self.dist) #create cityplan through self size
        city_plan.sub_cities=_list
        startpoint=(0,0)
        
        #lets go through all sub_city from _list and add them to the city_plan
        for sub_city in _list:
            self.construct_building(startpoint,sub_city) #consctruct the project: sub_city
            #for each resi_building and util_building in sub_city: cells are updates in the residental_project and utility_project coordinates argument
            #city_plan is also updated with the buildings it possesses 
            
            
            for residental_project in sub_city.resi_building:
                updated_cell=[]
                for x,y in residental_project.coordinates:
                    _x,_y=(x+startpoint[0],y+startpoint[1])
                    updated_cell.append((_x,_y))
                
                residental_project.coordinates=updated_cell
                city_plan.resi_building.append(residental_project)
                
            for utility_project in sub_city.util_building:
                updated_cell=[]
                for x,y in utility_project.coordinates:
                   _x,_y=(x+startpoint[0],y+startpoint[1])
                   updated_cell.append((_x,_y))
                   
                utility_project.coordinates=updated_cell
                city_plan.util_building.append(utility_project)
            city_plan.plan=self.plan
           
            if startpoint[1]+sub_city.W*2 <= self.W:
                startpoint=(startpoint[0],startpoint[1]+sub_city.W)
            else:
                startpoint=(startpoint[0]+sub_city.H,0)
        return city_plan
    
    
    
    
    #most important function that retrieves to others for the construction of the buildings
    def construct(self):
        _list=[]
        #hyper-parameter: beaware of city size for these parameters
        #a sub_city is created bellow with this hyper-paramentes

        sub_city_h=20
        sub_city_w=20
        count=int((self.H * self.W) / (sub_city_h * sub_city_w)) #how many sub_city(s) fit in the city? -> count type int
        
        residental_projects=copy.copy(self.residental_projects)
        utility_projects=copy.copy(self.utility_projects)
        
        for i in range(count): #iterate over the times a sub_city fits the city
            if not residental_projects:
                residental_projects = copy.copy(self.residental_projects)
            if not utility_projects:
                utility_projects = copy.copy(self.utility_projects)
            #create the subcity
            sub_city=SubCity(sub_city_h,sub_city_w,residental_projects=[residental_projects.pop()],utility_projects=[utility_projects.pop()],dist=self.dist)
            #create the city_plan (sub_city.construct() method)
            city_plan=sub_city.construct()
            #append this city_plan to _list
            _list.append(city_plan)
            #calculate the value of self according to the value of the city_plan
            self.value+=city_plan.value
        
        city_plan=self.unit_city(_list)
        city_plan.value=self.value
        return city_plan
            
            
    #updates self.plan to project.plan cells (receives self, startpoint and project)
    def construct_building(self,startpoint,project):
        for x in range(len(project.plan)):
            for y in range(len(project.plan)):
                _x,_y=(x+startpoint[0],y+startpoint[1])
                self.plan[_x][_y]=project.plan[x][y]
        
   
    
###############################################################################
###############################################################################
#Select project type of Building Plan
class ProjectType: 
    @staticmethod
    def specs(data,index):
        t,h,w,i=data.split(' ')
        #t=type (R or U)
        #h=rows, w=columns
        #i=information, capacity if t=R or utility type if t=U
        if t=='R':
            return Residental_Project(h,w,i,index)
        elif t=='U':
           
            return Utility_Project(h,w,i,index)
        else:
            raise Exception('Unknown Type of Building Project')

###############################################################################
###############################################################################
#Create and validate Building Plan           
class BuildingPlan: 
    def __init__(self, h, w, idx):
        self.h=int(h) #string is passed, return int
        self.w=int(w)
        self.plan=empty_matrix(self.h,self.w)
        self.coordinates=[]
        self.idx=idx
        self.filtered_cell=[]
     
    
    #returns coordinates of free cells
    def find_dots(self):
        for i in range(self.h):
            for j in range(self.w):
                if self.plan[i][j]=='.' and not (i==0 or j==0) and not (i==self.h -1 or j == self.w-1):
                    return i,j
        return None, None #return nothing if free cell not found
        
    #gets hole    
    def get_hole(self,x,y):
        right=None
        down=None
        free_cell=[]
        
        if x+1 < self.h-1:
            down=self.plan[x+1][y]
            
        if y+1 < self.w-1:
            right=self.plan[x][y+1]
            
        if right and right == '.':
            free_cell=free_cell+[(x,y+1)]+self.get_hole(x,y+1)
            
        if down and down == '.':
            free_cell=free_cell+[(x+1,y)]+self.get_hole(x+1,y)
            
        return free_cell
    
    #verifies if hole is inside - using previous functions
    def is_hole_inside(self):
        i,j=self.find_dots()
        
        if i is None and j is None:
            return False #if there's no dots, there's no holes
        
        
        free_cell=set([(i,j)]+self.get_hole(i,j))
        
        verifications=[]
        
        for cell in free_cell:
            i,j=cell
            
            neigh=[]
            
            #right
            if j+1 < self.w and (i,j+1) not in free_cell:
                neigh.append(self.plan[i][j+1])
            
            #left
            if j-1 >=0 and (i,j-1) not in free_cell:
                neigh.append(self.plan[i][j-1])
                
            #down
            if i+1 < self.h and (i+1,j) not in free_cell:
                neigh.append(self.plan[i+1][j])
                
            #up
            if i-1 >= 0 and (i-1,j) not in free_cell:
                neigh.append(self.plan[i-1][j])
                
            verification=[True if item == '#' else False for item in neigh]
            
            verifications.append(all(verification))
            
            return all(verifications) if verifications else False
    
    

    #is the building connected
    def is_connected(self):
        for row in self.plan:
            horizontal_hole=[True if item == '.' else False for item in row]
            if all(horizontal_hole):
                return False
        for i in range(self.w):
            vertical_hole=[True if self.plan[j][i]=='.' else False for j in range(self.h)]
            if all(vertical_hole):
                return False
            
        if self.h==1 or self.w==1:
            return True
        
        for i in range(self.h):
            for j in range(self.w):
                if self.plan[i][j] != '#':
                    continue
                if j+1 < self.w:
                    horizontal=self.plan[i][j+1]
                else:
                    horizontal=self.plan[i][j-1]
                    
                if i+1 < self.h:
                    vertical=self.plan[i+1][j]
                else:
                    vertical=self.plan[i-1][j]
                    
                if vertical=='.' and horizontal=='.':
                    return False
            return True

    #edges 
    def edgeoccupied (self):
        edge1= self.plan[0]
        edge2= self.plan[self.h-1]
        edge3= self.plan[0][0]
        edge4= self.plan[0][self.w-1]
        for x in range(1,self.h):
            edge3= edge3 + self.plan[x][0]
            edge4= edge4 + self.plan[x][self.w-1]
        if ('#' in edge1 and '#' in edge2 and '#' in edge3 and '#' in edge4):
            return True
        return False    
        
    #validates building project
    def validate(self):
        if not self.is_connected():
             return False
        if not self.edgeoccupied():
            return False
        if self.is_hole_inside(): 
            return False
        
        return True

        
###############################################################################
###############################################################################
#define type of building plan: residence     
class Residental_Project(BuildingPlan): #super   
    def __init__(self, h,w,capacity,idx):
        super(Residental_Project,self).__init__(h,w,idx)
        self.capacity=int(capacity)
        self.utility_services=[]
 
###############################################################################
###############################################################################      
#define type of building plan: utility     
class Utility_Project(BuildingPlan): #super 
    def __init__(self, h,w,service,idx):
        super(Utility_Project,self).__init__(h,w,idx)
        self.service=int(service)   




###############################################################################
###############################################################################
#class for input parser
class InputParser: 
    def __call__ (self, data_path, *args, **kwargs):
        with open(data_path) as file:
            
            city_type=file.readline() #read first line with city information
            city=CityInfo.specs(city_type)
            #knowing now the first city specs, we can now learn it's buildings
            
            for building in range(0,city.bplans):
                read_project_info=file.readline()               
                building_project=ProjectType.specs(read_project_info,building)
                
                for i in range(building_project.h):
                    row=file.readline().strip()
                    j=0
                    for item in row:
                        
                        building_project.plan[i][j]=item
                        building_project.coordinates.append((i,j))
                        
                        j=j+1
                        
                if building_project.validate():
                    city.add_project(building_project)
        #shuffle to obtain diffent solutions
        shuffle(city.residental_projects)
        shuffle(city.utility_projects)
                    
        return city
                        
   

             
###############################################################################
############################################################################### 
#create submission file as requested              
def result(file_path, city_plan, *args, **kwargs):
    with open(file_path, 'w+') as file:
        result=""
        
        building=city_plan.get_building_numbers()
        result+="{}\n".format(building)
        
        for residental_building in city_plan.resi_building:
            first_coord=residental_building.coordinates[0]
            result+="{} {} {}\n".format(residental_building.idx,first_coord[0],first_coord[1])
            
        for utility_building in city_plan.util_building:
           first_coord=utility_building.coordinates[0]
           result+="{} {} {}\n".format(utility_building.idx,first_coord[0],first_coord[1])
        
        file.write(result)


###############################################################################
############################################################################### 
#when switching between projects in the city plan, we need to change the fitlered cells 
#these corresponde to the ones that are occupied (#) showing their coordinates in the plan
def switch_projects(projA,projB): #projA - original; projB - to exchange
    projB.coordinates=projA.coordinates
    projB.utility_services=projA.utility_services

    
    for x in range(projB.h):
        for y in range(projB.w):           
            if projB.plan[x][y]=="#":
                projB.filtered_cell.append((projB.coordinates[(projB.w*x)+y]))
     
          
    

###############################################################################
###############################################################################
def verify_distance(proj_A,proj_B, dist):
    distance=None
    for point_1 in proj_A.filtered_cell:
        for point_2 in proj_B.filtered_cell:
            distance=math.fabs(point_1[0]-point_2[0])+math.fabs(point_1[1]-point_2[1])
            if distance <= dist:
                return True
    return False 




###############################################################################
###############################################################################
#receives list (projects) and returns the one with higher capacity
def best_choice(list):
    capacities=[]
    for i in range (len(list)):
        capacities.append(list[i].capacity)
        
    best=capacities.index(max(capacities)) 

    return best    


###############################################################################
###############################################################################
def energy(state_value):
    return 1/state_value


         
###############################################################################
###############################################################################
#returns #number of initial solutions
def generate_initial_solutions(number,save_result):
   
    if (number==1):
        input_parser=InputParser()
    
           # Possible cases - unmark wanted
        #city=input_parser("data/example.in")
        city=input_parser("data/b_short_walk.in")
        #city=input_parser("data/c_going_green.in")
        #city=input_parser("data/d_wide_selection.in")
        #city=input_parser("data/e_precise_fit.in")
        #city=input_parser("data/f_different_footprints.in")
    
    
        city_plan=city.construct()
        
        #print city value
        print("Initial solution score: {}".format(city_plan.value))        
        #save results
        if save_result==True:
            result('Result_Initial_Solution.txt',city_plan)
        
        return city,city_plan
        
    elif (number>1):
        city_plans=[]
        cities=[]
        count=0
        while (count<number): 
            #create input parser 
            input_parser=InputParser()
    
               # Possible cases - unmark wanted
            #city=input_parser("data/example.in")
            city=input_parser("data/b_short_walk.in")
            #city=input_parser("data/c_going_green.in")
            #city=input_parser("data/d_wide_selection.in")
            #city=input_parser("data/e_precise_fit.in")
            #city=input_parser("data/f_different_footprints.in")
    
            city_plan=city.construct()
            #print city value
            print("Initial solution score: {}".format(city_plan.value))       
            #save results
            if save_result==True:
                result('Result_Initial_Solution_'+count+'.txt',city_plan)
            
            cities.append(city)
            city_plans.append(city_plan)
            
            del city,city_plan, input_parser
            count=count+1

    return cities,city_plans
   
# if __name__ == '__main__':
#     cities,city_plans=generate_initial_solutions(5)


# ###############################################################################
#     ###                        OPITMIZATION PROCESS                    ###
# ###############################################################################


###############################################################################
    ###                       Hill-Climbing                            ###
    # Start from initial solution (valid) search for the best neighbour
    # Changes all projects that are residental to a project with same dimensions
    # but bigger capacity, resulting in a better final project
###############################################################################
def Hill_Climbing():    
    city,city_plan=generate_initial_solutions(1,save_result=False)
    start_time = time.time()   
    print("Start Hill Climbing Search... ")

    better_projects=[]
    citycopy=copy.copy(city_plan)    

    
    for project in city_plan.resi_building: #resi_building in city_plan are the projects placed in the city 
        for residential in city.residental_projects: #residental_projects in city are the projects available
            
            if (project.h == residential.h) and (project.w == residential.w) and (not(residential.capacity <= project.capacity)):              
                #add better projects than project in city_plan to better projects
                better_projects.append(residential)
        
        if better_projects:                   
            #find best one
            id=best_choice(better_projects)
            #create winner project (best one) copy
            winner=better_projects[id]
            
            #get what value contributed to city_plan.value and subtract it
            project_value= project.capacity * len(project.utility_services)                
            citycopy.value = citycopy.value - project_value         
            
            #switch coordinates of the projects to the original ones
            switch_projects(project,winner)
            #change the plan in citycopy
            citycopy.resi_building[city_plan.resi_building.index(project)].plan=winner.plan
            #change the capacity in citycopy
            citycopy.resi_building[city_plan.resi_building.index(project)].capacity=winner.capacity
            #change filtered_cells
            citycopy.resi_building[city_plan.resi_building.index(project)].filtered_cell=winner.filtered_cell
            #change project index
            citycopy.resi_building[city_plan.resi_building.index(project)].idx=winner.idx
            #empty better_projects
            
            #calculate the new value according to the value that the new project gives 
            winner_value= winner.capacity * len(winner.utility_services)                
            citycopy.value = citycopy.value + winner_value     
            

            #clear better_projects
            better_projects=[]
       
    hill_time = time.time() - start_time 
    
    print("Solution Found!")        
    best_solution=copy.copy(citycopy)
    print("Hill Climbing solution score: {}".format(best_solution.value))
    result('Result_Hill_Climbing.txt',best_solution)
    return best_solution,hill_time

###############################################################################
    ###                       Simulated Annealing                       ###
    # Start from initial solution (valid)
    # While temperature does not change to 0, search for neighbour solution
    # The variable energy is inversely proportional to the score, so the 
    # state with the least energy is the most optimal
    # Hyper-parameters: alpha - decay rate of temperature
###############################################################################
    
def Simulated_Annealing(temperature,alpha):
    city,city_plan=generate_initial_solutions(1,save_result=False)
    start_time = time.time()  
    print("Start Simulated Annealing Search...")
    
    random_solution=copy.copy(city_plan)
    current_state=random_solution
    
    
    #Define temperature
    
    t=temperature #entrance parameter
    
    #alpha
    alpha=alpha #entrance parameter
    
    final_states=[]
    
    for i in range(0,len(alpha)):
        while(t>0.0000000001):
            
            #DECAY RATE
            t=t*alpha[i]
            
            
            #DEFINE NEIGHBOUR: RANDOMLY ALTER RESI_BUILDING
            #define next state: can be done be exchange residental or utility buildings of same dimensions
            #firstly, lets keep it simple and exchange for resi_building only
            #select random project to exchange
            seed(1)
            index_old=random.randrange(0,len(current_state.resi_building))
            project_to_exchange=copy.copy(current_state.resi_building[index_old])
            
            
            #select random neighbour
            
            #colect projects that have the same dimensions
            residental_projects_same_dim=[]
            for residential in city.residental_projects:
                if (project_to_exchange.h == residential.h) and (project_to_exchange.w == residential.w):
                    residental_projects_same_dim.append(residential)
                    
            #select one randomly
            index_new=random.randrange(0,len(residental_projects_same_dim))
            project_new=copy.copy(residental_projects_same_dim[index_new])
            
            #define new state - same as previous - changes next
            next_state=copy.copy(current_state)
            
            #get what value contributed to city_plan.value and subtract it
            old_project_value= project_to_exchange.capacity * len(project_to_exchange.utility_services)                
            next_state.value = current_state.value - old_project_value  
            
            #switch coordinates of the projects to the original ones
            switch_projects(project_to_exchange,project_new)
            #change the plan in next_state
            next_state.resi_building[index_old].plan=project_new.plan
            #change the capacity in next_state
            next_state.resi_building[index_old].capacity=project_new.capacity
            #change filtered_cells
            next_state.resi_building[index_old].filtered_cell=project_new.filtered_cell
            #change project index
            next_state.resi_building[index_old].idx=project_new.idx

            #calculate the new value according to the value that the new project gives 
            new_project_value= project_new.capacity * len(project_new.utility_services)                
            next_state.value = next_state.value + new_project_value     
            
            
            #ENERGY
            energy_delta=energy(next_state.value)-energy(current_state.value)
            
            if ((energy_delta<0) or (math.exp((-energy_delta)/t)>=random.randrange(0,10))):
                current_state=next_state
        
        
        print("Solution Found!")            
        final_state=next_state
        final_states.append(final_state)
        print("Alpha = {}".format(alpha[i]))
        print("Simulated Annealing solution score: {}".format(final_state.value))
        result('Result_Simulated_Annealing.txt',city_plan)

    simu_time = time.time() - start_time 
    return final_states,simu_time

###############################################################################
    ###                       Tabu Search                             ###
    # Start from initial solution (valid), search for neighbours and update
    # tabu list, return best candidate
    # Hyper-parameters: n_iter, tabu_list_max_size
###############################################################################
    
def Tabu_Search(n_iter,tabu_list_max_size):
    city,city_plan=generate_initial_solutions(1,save_result=False)
    start_time = time.time()

    #set initial solution
    s=copy.copy(city_plan)
    s_best=s
    #set empty tabu list
    tabu_list=[]
    
    #set number of iterations
    n_iter=100
    
    #set tabu list maximum size
    tabu_list_max_size=100
    
    #counter
    counter=0
    
    while (counter<=n_iter):
            
        #generate neighbours - all possible
        neighbours=[]                
        for project in s.resi_building: #resi_building in city_plan are the projects placed in the city 
            for residential in city.residental_projects: #residental_projects in city are the projects available       
                if (project.h == residential.h) and (project.w == residential.w):
                    #define neighbour
                    neighbour=copy.copy(s)
            
                    #get what value contributed to city_plan.value and subtract it
                    old_project_value= project.capacity * len(project.utility_services)                
                    neighbour.value = s.value - old_project_value  
            
                    #switch coordinates of the projects to the original ones
                    switch_projects(residential,project)
                    #change the plan in neighbour
                    neighbour.resi_building[s.resi_building.index(project)].plan=residential.plan
                    #change the capacity in neighbour
                    neighbour.resi_building[s.resi_building.index(project)].capacity=residential.capacity
                    #change filtered_cells
                    neighbour.resi_building[s.resi_building.index(project)].filtered_cell=residential.filtered_cell
                    #change project index
                    neighbour.resi_building[s.resi_building.index(project)].idx=residential.idx

                    #calculate the new value according to the value that the new project gives 
                    new_project_value= residential.capacity * len(residential.utility_services)                
                    neighbour.value = neighbour.value + new_project_value             
                        
                    neighbours.append(neighbour)
            
        for i in range(0,len(neighbours)):
            if neighbours[i] not in tabu_list and neighbours[i]>s.value:
                best_candidate=neighbours[i]
            
        if best_candidate.value > s_best.value:
            s_best=best_candidate
            
        tabu_list.append(best_candidate)
            
        if len(tabu_list)>tabu_list_max_size:
            tabu_list.remove[0]
            
            
        counter=counter+1
     
    tabu_time = time.time() - start_time 
        
    print("Solution Found!")            
    final_state_tabu_search=s_best
    print("Tabu Search solution score: {}".format(final_state_tabu_search.value))
    
    return final_state_tabu_search,tabu_time
    
###############################################################################
    ###                       Genetic Algorithms                       ###
    # Start from initial population of solutions (valid already)
    # Iterate over the initial solution
    # Solutions (City Plan type class) have the sub-cities in their variables
    # These are going to be used as the genes to mutate and reproduce
    # Updates are only done at sub_city level, and not all city (need to add 
    # unit_city method for that, too slow)
###############################################################################
def reproduce(x,y):
    n_sub_cities=len(x.sub_cities)
    amount_x=round(n_sub_cities/2)
    amount_y=n_sub_cities-amount_x
    seed(1)
    if random.randint(0,10)<5:
        child=copy.copy(x)
        value_to_subtract=0
        value_to_add=0
        for i in range(0,len(amount_y)):
            value_to_subtract=value_to_subtract+child.sub_cities[amount_x+1+i].value
            value_to_add=value_to_add+y.sub_cities[amount_x+1+i].value
            child.sub_cities[amount_x+1+i]=y.sub_cities[amount_x+1+i]
        child.value=child.value-value_to_subtract
        child.value=child.value+value_to_add
    else:
        child=copy.copy(y)
        value_to_subtract=0
        value_to_add=0
        for i in range(0,len(amount_x)):
            value_to_subtract=value_to_subtract+child.sub_cities[amount_y+1+i].value
            value_to_add=value_to_add+x.sub_cities[amount_y+1+i].value
            child.sub_cities[amount_y+1+i]=x.sub_cities[amount_y+1+i]
        child.value=child.value-value_to_subtract
        child.value=child.value+value_to_add
        
    return child

def fitness(initial_population, individual,actual_iter,n_iter):
    values_initial_population=[]
    for i in range(0,len(initial_population)):
        values_initial_population.append(initial_population[i].value)
    best_value_initial_population=max(values_initial_population)
    

    if individual.value < best_value_initial_population:
        return False
    
    if (individual.value > best_value_initial_population) and (actual_iter<n_iter*0.75):
        return False
        
    if (individual.value > best_value_initial_population) and (actual_iter>n_iter*0.75):
        return True  
    
def mutate(child):
    seed(1)
    amount_mutate=random.randint(0,len(child.sub_cities))
    
    for i in range (0,len(amount_mutate)):
        value_to_subtract=child.sub_cities[i]
        seed(2)
        new_sub_city_index=random.randint(0,len(child.sub_cities))
        value_to_add=child.sub_cities[new_sub_city_index].value
        child.sub_cities[i]=child.sub_cities[new_sub_city_index]
        
        child.value=child.value-value_to_subtract
        child.value=child.value-value_to_add
    return child

def Genetic_Algorithms(initial_pop_size,n_iter):
    initial_cities,initial_population=generate_initial_solutions(initial_pop_size,save_result=False)
    start_time = time.time()
    actual_iter=0
    population=initial_population
    while (actual_iter<=n_iter):
        new_population=[]    
        for i in range(0,len(population)):
            seed(1)
            index_x=random.randint(0,len(initial_population))
            index_y=random.randint(0,len(initial_population))
            
            x=initial_population[index_x]      
            y=initial_population[index_y]
            
            child=reproduce(x,y)
            
            seed(2)
            if random.randint(0,10)<=2:
                child=mutate(child)
            
            new_population.append(child)
        
            for individual in new_population:       
                if fitness(population,new_population,actual_iter,n_iter):
                    best_solution=individual
    
        population=new_population    
    
    print("Solution Found!")         
    final_state_AG=best_solution
    print("Genetic Algorithm solution score: {}".format(final_state_AG.value))
    AG_time = time.time() - start_time 
    return final_state_AG,AG_time
    

###############################################################################
    ###                             main                              ###
###############################################################################    

    
if __name__ == "__main__":
    
    ###########################################################################
    print("City Plan - Hashcode 2018 - Optimizers")
    
    print("\n")
    
    print("For initial solution, press a:   ")
    print("For Hill Climbing search, press b:   ")
    print("For Simulated Annealing search, press c:   ")
    print("For Tabu Search, press d:   ")
    print("For Genetic Algorithm search, press e:   ")
    print("For all the above, press all:   ")
    print("\n")
    print("To quit, press q:   ")
    
    input_user=input()
    
    
    ###########################################################################
    if input_user=='q':
        raise SystemExit
    
    ###########################################################################    
    if input_user=='a':
        print("Initial Solution - Valid")
        initial_city, initial_solution = generate_initial_solutions(1,save_result=True)
    
    ###########################################################################    
    if input_user=='b':
        print("Hill Climbing")
        solution, time_elapsed = Hill_Climbing()
        result("Result_Hill_Climbing.txt",solution)
        print("Time elapsed: {}".format(time_elapsed))
    
    ###########################################################################
    if input_user=='c':
        print("Simulated Annealing")
        print("Insert Temperature (1000 - default):   ")
        temperature=input()
        if not temperature:
            temperature=1000
        print("Insert alphas (0.1,0.3,0.01,0.03,0.001,0.003 - default):   ")
        alphas=input()
        if not alphas:
            alphas=[0.1,0.3,0.01,0.03,0.001,0.003]
        solution, time_elapsed = Simulated_Annealing(temperature,alphas)
        for sol in range(0,len(solution)):
            result("Result_Simulated_Annealing_"+sol+".txt",sol)
        print("Time elapsed: {}".format(time_elapsed))    
    
    ###########################################################################
    if input_user=='d':
        print("Tabu Search")
        print("Insert Number of Iterations (1000 - default):   ")
        n_iter=input()
        if not n_iter:
            n_iter=1000
        print("Insert Tabu List Max Size (100 - default):   ")
        tabu_list_max_size=input()
        if not tabu_list_max_size:
            tabu_list_max_size=100
        solution, time_elapsed = Tabu_Search(n_iter,tabu_list_max_size) 
        result("Result_Tabu_Seacrh.txt",solution)
        print("Time elapsed: {}".format(time_elapsed))    
    
    ###########################################################################
    if input_user=='e':
        print("Genetic Algorithm")
        print("Insert Number of Iterations (1000 - default):   ")
        n_iter=input()
        if not n_iter:
            n_iter=1000
        print("Insert Initial Population Size (10 - default):   ")
        initial_pop_size=input()
        if not initial_pop_size:
            tabu_list_max_size=10
        solution, time_elapsed = Genetic_Algorithms(initial_pop_size,n_iter) 
        result("Result_Genetic_Algorithm.txt",solution)
        print("Time elapsed: {}".format(time_elapsed))           
    
    if input_user=='all':
        #######################################################################
        print("Initial Solution - Valid")
        initial_city, initial_solution = generate_initial_solutions(1,save_result=True)
        
        #######################################################################
        print("Hill Climbing")
        solution, time_elapsed = Hill_Climbing()
        result("Result_Hill_Climbing.txt",solution)
        print("Time elapsed: {}".format(time_elapsed))
    
        #######################################################################
        print("Simulated Annealing")
        print("Insert Temperature (1000 - default):   ")
        temperature=input()
        if not temperature:
            temperature=1000
        print("Insert alphas (0.1,0.3,0.01,0.03,0.001,0.003 - default):   ")
        alphas=input()
        if not alphas:
            alphas=[0.1,0.3,0.01,0.03,0.001,0.003]
        solution, time_elapsed = Simulated_Annealing(temperature,alphas)
        for sol in range(0,len(solution)):
            result("Result_Simulated_Annealing_"+sol+".txt",sol)
        print("Time elapsed: {}".format(time_elapsed))    
    
        #######################################################################
        print("Tabu Search")
        print("Insert Number of Iterations (1000 - default):   ")
        n_iter=input()
        if not n_iter:
            n_iter=1000
        print("Insert Tabu List Max Size (100 - default):   ")
        tabu_list_max_size=input()
        if not tabu_list_max_size:
            tabu_list_max_size=100
        solution, time_elapsed = Tabu_Search(n_iter,tabu_list_max_size) 
        result("Result_Tabu_Seacrh.txt",solution)
        print("Time elapsed: {}".format(time_elapsed))    
    
        #######################################################################
        print("Genetic Algorithm")
        print("Insert Number of Iterations (1000 - default):   ")
        n_iter=input()
        if not n_iter:
            n_iter=1000
        print("Insert Initial Population Size (10 - default):   ")
        initial_pop_size=input()
        if not initial_pop_size:
            tabu_list_max_size=10
        solution, time_elapsed = Genetic_Algorithms(initial_pop_size,n_iter) 
        result("Result_Genetic_Algorithm.txt",solution)
        print("Time elapsed: {}".format(time_elapsed))           
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    