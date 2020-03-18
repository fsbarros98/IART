"""
Couse: Artificial Intelligence EIC0029
Authors: Fátima Barros up201608444 and Miguel Ferreira up201606158
Created on 13/03/2020
"""
import math
import copy


#empty_matrix(i,j) returns an empty matrix of size (i,j) - list type
def empty_matrix(i,j):
    matrix=[]
    for x in range(i):
        matrix.append(['.' for y in range(j)])
    return matrix


class CityPlan:
    def __init__(self,H,W):
        self.H=H
        self.W=W
        
        self.resi_building=[]
        self.util_building=[]
        self.plan=empty_matrix(self.H,self.W)
        self.value=0
        
    def get_building_numbers(self):
        return len(self.resi_building)+len(self.util_building)


class SubCity:
    def __init__(self,H,W,residential_projects,utility_projets,dist):
        self.H=H
        self.W=W
        self.residential_projects=residential_projects
        self.utility_projets=utility_projets
        self.dist=dist
        
        self.resi_building=[]
        self.util_building=[]
        self.plan=empty_matrix(self.h,self.w)
        
    
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
    
    
    def build_scenario(self):
        city_plan=CityPlan(self.H,self.W)
        residential_projects=copy.copy(self.residential_projects)
        utility_projects=copy.copy(self.utility_projects)
        
        finish=False #flag
        
        while not finish:
            free_cell=self.get_free_cells()
            empty_cell=False
            #resi
            if residential_projects:
                residential_project=copy.copy(residential_projects.pop())
                
                residential_projects_not_construct=True
                
                while residential_projects_not_construct and free_cell:
                    updated_cells,filtered_cell=self.construct_building(free_cell.pop(0),residential_project)
                    if updated_cells:
                        residential_project.coordinates=updated_cells
                        residential_project.filtered_cell=filtered_cell
                        city_plan.resi_building.append(residential_project)
                        city_plan.plan=self.plan
                        residential_projects_not_construct=False
                        break
            else:
                empty_cell=True
                
            if not residential_projects and free_cell and not free_cell[0]==self.get_last_free_cell():
                residential_projects=copy.copy(self.residential_projects)
            
            #util
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
    
    def construct(self):
        city_plan=self.build_scenario()
        value=0
        utility_services={}
        

        
        for util_building in city_plan.util_building:
            utility_services[util_building.service]=[]
            i=0
            for resi_building in city_plan.resi_building:
                if i in utility_services[util_building.service]:
                    i+=1
                    continue
                if self.verify_distance(resi_building, util_building):
                    utility_services[util_building.service].append(i)
                    value += resi_building.capacity
                i+=1
            
        city_plan.value=value
        return city_plan
            
            
    def construct_building(self,startpoint,project):
        updated_cell=[]
        filtered_cell=[]
        
        def undolog_plan():
            for x_cell,y_cell in updated_cell:
                self.plan[x_cell][y_cell]='.'
                
        for x,y in project.coordinates:
            _x,_y=(x+startpoint[0],y+startpoint[1])
            
            try:
                if not self.plan[_x][_y]=='.':
                    undolog_plan()
                    return False, False
                else:
                    updated_cell.append((_x,_y))
                    self.plan[_x][_y]=project.plan[x][y]
                    if project.plan[x][y]=='#':
                        filtered_cell.append((_x,_y))
            except IndexError as e:
                undolog_plan()
                return False, False
            
        return updated_cell,filtered_cell
                    

class CityInfo:
    def __init__(self,H,W,dist,bplans): 
        #H=rows, W=columns, dist=maximum walking distance, bplans=building plans
        self.H=H
        self.W=W
        self.dist=dist
        self.bplans=bplans
        #initialize some variables
        self.projects=[]
        self.projects_resi=[]
        self.projects_util=[]
        
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
        
        if isinstance(project,Residential_Project):
            self.projects_resi.append(project)
            
        elif isinstance(project,Utility_Project):
            self.projects_util.append(project)

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
    
    #consctruct a scenario for building the city, copies information and goes from that
    def build_scenario(self):
        city_plan=CityPlan(self.H,self.W)
        residential_projects=copy.copy(self.projects_resi)
        utility_projects=copy.copy(self.projects_util)
        
        finish=False #flag
        
        while not finish:
            free_cells=self.get_free_cells()
            empty_cell=False
            
            if residential_projects:
                residential_project=residential_projects.pop() #takes argument, updates lisst
              
                residential_projects_not_construct=True
                
                while residential_projects_not_construct and free_cells:
                    updated_cells,filtered_cell=self.construct_building(free_cells.pop(0),residential_project)
                    if updated_cells:
                        residential_project.coordinates=updated_cells
                        residential_project.filtered_cell=filtered_cell
                        city_plan.resi_building.append(residential_project)
                        city_plan.plan=self.plan
                        residential_projects_not_construct=False
                        break
            else:
                empty_cell=True
                
            if not residential_projects and free_cells and not free_cells[0]==self.get_last_free_cell():
                residential_projects=copy.copy(self.residential_projects)
                
            free_cells=self.get_free_cells()
            if utility_projects:
                utility_project=utility_projects.pop()
                
                utility_projects_not_construct=True
                
                while utility_projects_not_construct and free_cells:
                    updated_cells, filtered_cell=self.construct_building(free_cells.pop(0),utility_project)
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
        
        
    def unit_city(self,_list):
        city_plan= CityPlan(self.H,self.W)
        
        startpoint=(0,0)
        
        for sub_city in _list:
            self.construct_building(startpoint,sub_city)
            for residential_project in sub_city.resi_building:
                updated_cell=[]
                for x,y in residential_project.coordinates:
                    _x,_y=(x+startpoint[0],y+startpoint[1])
                    updated_cell.append((_x,_y))
                
                residential_project.coordinates=updated_cell
                city_plan.resi_building.append(residential_project)
                
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
                startpoint=(startpoint[0]+sub_city.h,0)
        return city_plan
    
    
    
    
    
    def construct(self):
        _list=[]
        sub_city_h=10
        sub_city_w=10
        
        count=int((self.H*self.W)/(sub_city_h*sub_city_w))
        
        residential_projects=copy.copy(self.projects_resi)
        utility_projects=copy.copy(self.projects_util)
        
        for i in range(count):
            if not residential_projects:
                residential_projects = copy.copy(self.projects_resi)
            if not utility_projects:
                utility_projects = copy.copy(self.projects_util)
                
            sub_city=SubCity(sub_city_h,sub_city_w,residential_projects=[residential_projects.pop()],utility_projects=[utility_projects.pop()],dist=self.dist)
            city_plan=sub_city.construct()
            _list.append(city_plan)
            self.value+=city_plan.value
        city_plan=self.unit_city(_list)
        city_plan.value=self.value
        return city_plan
            
            
    
    def construct_building(self,startpoint,project):
        for x in range(len(project.plan)):
            for y in range(len(project.plan)):
                _x,_y=(x+startpoint[0],y+startpoint[1])
                self.plan[_x][_y]=project.plan[x][y]
        
        
        
        


#Select project type of Building Plan
class ProjectType: 
    @staticmethod
    def specs(data,index):
        t,h,w,i=data.split(' ')
        #t=type (R or U)
        #h=rows, w=columns
        #i=information, capacity if t=R or utility type if t=U
        if t=='R':
            return Residential_Project(h,w,i,index)
        elif t=='U':
            return Utility_Project(h,w,i,index)
        else:
            raise Exception('Unknown Type of Building Project')


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
        free_cells=[]
        
        if x+1 < self.h-1:
            down=self.plan[x+1][y]
            
        if y+1 < self.w-1:
            right=self.plan[x][y+1]
            
        if right and right == '.':
            free_cells=free_cells+[(x,y+1)]+self.get_hole(x,y+1)
            
        if down and down == '.':
            free_cells=free_cells+[(x+1,y)]+self.get_hole(x+1,y)
            
        return free_cells
    
    #verifies if hole is inside
    def is_hole_inside(self):
        i,j=self.find_dots()
        
        if i is None and j is None:
            return False #if there's no dots, there's no holes
        
        
        free_cells=set([(i,j)]+self.get_hole(i,j))
        
        verifications=[]
        
        for cell in free_cells:
            i,j=cell
            
            neigh=[]
            
            #right
            if j+1 < self.w and (i,j+1) not in free_cells:
                neigh.append(self.plan[i][j+1])
            
            #left
            if j-1 >=0 and (i,j-1) not in free_cells:
                neigh.append(self.plan[i][j-1])
                
            #down
            if i+1 < self.h and (i+1,j) not in free_cells:
                neigh.append(self.plan[i+1][j])
                
            #up
            if i-1 >= 0 and (i-1,j) not in free_cells:
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

      
class Residential_Project(BuildingPlan): #super   
    def __init__(self, h,w,capacity,idx):
        super(Residential_Project,self).__init__(h,w,idx)
        self.capacity=int(capacity)      
 
class Utility_Project(BuildingPlan): #super 
    def __init__(self, h,w,service,idx):
        super(Utility_Project,self).__init__(h,w,idx)
        self.service=int(service)   


class InputParser: 
    def __call__ (self, data_path, *args, **kwargs):
        with open(data_path) as file:
            city_type=file.readline()
            
            city=CityInfo.specs(city_type)
            #knowing now the first city specs, we can now learn it's buildings
            
            for building in range(city.bplans):
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
                    
        return city
                        
                
                
def result(file_path, city_plan, *args, **kwargs):
    with open(file_path, 'w+') as file:
        result=""
        
        building=city_plan.get_building_numbers()
        result+="{}\n".format(building)
        
        for residential_building in city_plan.resi_building:
            first_coord=residential_building.coordinates[0]
            result+="{} {} {}\n".format(residential_building.idx,first_coord[0],first_coord[1])
            
        for utility_building in city_plan.util_building:
           first_coord=utility_building.coordinates[0]
           result+="{} {} {}\n".format(utility_building.idx,first_coord[0],first_coord[1])
        
        file.write(result)



if __name__ == '__main__':
    input_parser=InputParser()
    city=input_parser("data/a_example.in")
    for project in city.projects:
        print(project.plan)
    city_plan=city.construct()
    print("city value {}".format(city_plan.value))
    result('res.txt',city_plan)

    

    
        # Possible cases
    # ("data/b_short_walk.in")
    # ("data/c_going_green.in")
    # ("data/d_wide_selection.in")
    # ("data/e_precise_fit.in")
    # ("data/f_different_footprints.in")

