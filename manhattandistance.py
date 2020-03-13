# -*- coding: utf-8 -*-
"""
Couse: Artificial Intelligence EIC0029
Authors: Fátima Barros up201608444 and Miguel Ferreira up201606158
Created on 13/03/2020
"""

class ManhattanD:
    @staticmethod
    def manhattan_d(a1,a2):
        x=abs(a1[0]-a2[0])
        y=abs(a1[1]-a2[1])
        return x+y
    
    