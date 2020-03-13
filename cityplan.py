"""
Couse: Artificial Intelligence EIC0029
Authors: Fátima Barros up201608444 and Miguel Ferreira up201606158
Created on 13/03/2020
"""




class CityInfo:
    def __init__(self,r,c,dist,bplans): 
        #r=rows, c=columns, dist=maximum walking distance, bplans=building plans
        self.r=r
        self.c=c
        self.dist=dist
        self.bplans=bplans
        
    @classmethod
    def specs(cls,data):
        data=data.split(' ') #returns elements in the first line of the file
        r,c,dist,bplans=[int(i) for i in data]
        return cls(r,c,dist,bplans)
    

        





class ProjectType:
    @staticmethod
    def specs(data,index):
        t,r,c,i=data.split(' ')
        #t=type (R or U)
        #r=rows, c=columns
        #i=information, capacity if t=R or utility type if t=U
        if t=='R':
            return Residential(r,c,i,index)
        elif t=='U':
            return Utility(r,c,i,index)
        else:
            raise Exception('Unknown Type of Building Project')

class Residential(ProjectType):
    def __init__(self, r,c,capacity,idx):
        super(Residential,self).__init__(r,c,idx)
        self.capacity=int(capacity)
        
 
class Utility(ProjectType):
    def __init__(self, r,c,service,idx):
        super(Residential,self).__init__(r,c,idx)
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
                
                
                





if __name__ == '__main__':
    input_parser=InputParser()
    city_plan=input_parser("data/a_example.in")

    

    
        # Possible cases
    # ("data/b_short_walk.in")
    # ("data/c_going_green.in")
    # ("data/d_wide_selection.in")
    # ("data/e_precise_fit.in")
    # ("data/f_different_footprints.in")

