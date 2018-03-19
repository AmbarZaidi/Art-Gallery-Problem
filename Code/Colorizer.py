#GroupID-26 (14114009_14114068)
#Date March,15 2018
# Colorizer.py: Construct dual Graph and obtain 3-coloring

import numpy as np
from DCELfile import *
DEBUG = False

class Colorizer(object):
    def __init__(self,d,listTriangle):
        #Initialize color to -1
        self.colors = {v.coords:-1 for v in d.getVertices()}
        
        #Creating Dual Graph
        self.vdual={i:listTriangle[i] for i in range(0,len(listTriangle))}
        self.edual={}
        for i in range(0,len(listTriangle)):
            j=i+1
            for j in range(0,len(listTriangle)):
                triangle_i = [x.coords for x in listTriangle[i]]
                triangle_j = [x.coords for x in listTriangle[j]]
                if len(list(set(triangle_i)&set(triangle_j))) > 1:
                    if i in self.edual and j not in self.edual[i] and i is not j:
                        self.edual[i].append(j)
                    elif i not in self.edual and i is not j:
                        self.edual[i]=[j]
                    if j in self.edual and i not in self.edual[j] and i is not j:
                        self.edual[j].append(i)
                    elif j not in self.edual and i is not j:
                        self.edual[j]=[i]
    
    def DFS(self,s):
        visited, stack = set(), [s]
        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                colorsum = self.colors[self.vdual[vertex][0].coords]+self.colors[self.vdual[vertex][1].coords]+self.colors[self.vdual[vertex][2].coords]
                if DEBUG:
                    print "Changing Coloring of Triangle#:"+str(vertex)+"  from: ",self.colors[vdual[vertex][0].coords],self.colors[vdual[vertex][1].coords],self.colors[vdual[vertex][2].coords]
                if colorsum<3:
                    if self.colors[self.vdual[vertex][0].coords] is -1:
                        self.colors[self.vdual[vertex][0].coords] = 3-self.colors[self.vdual[vertex][1].coords]-self.colors[self.vdual[vertex][2].coords]
                    elif self.colors[self.vdual[vertex][1].coords] is -1:
                        self.colors[self.vdual[vertex][1].coords] = 3-self.colors[self.vdual[vertex][0].coords]-self.colors[self.vdual[vertex][2].coords]
                    elif self.colors[self.vdual[vertex][2].coords] is -1:
                        self.colors[self.vdual[vertex][2].coords] = 3-self.colors[self.vdual[vertex][1].coords]-self.colors[self.vdual[vertex][0].coords] 
                if DEBUG:
                    print "to: ",self.colors[self.vdual[vertex][0].coords],self.colors[self.vdual[vertex][1].coords],self.colors[self.vdual[vertex][2].coords]
                visited.add(vertex)
                stack.extend(set(self.edual[vertex]) - visited)
    
    def colorize(self):
        #key = first triangle to be 3-colored
        key = 0
        if DEBUG:
            print("############################# INITIAL COLORING OF ONE TRIANGLE ##################################")
            print ("Triangle #"+str(key)+" Vertex #0 colored to 0")
        self.colors[self.vdual[key][0].coords] = 0
        if DEBUG:
            print ("Triangle #"+str(key)+" Vertex #1 colored to 1")
        self.colors[self.vdual[key][1].coords] = 1
        if DEBUG:
            print ("Triangle #"+str(key)+" Vertex #2 colored to 2")
        self.colors[self.vdual[key][2].coords] = 2
        if DEBUG:
            print("############################# GOING TO COLOR REMAINING TRIANGLES ###############################")
        self.DFS(key)
        output,col = self.findMinColor()
        return output,col

    def findMinColor(self):
        rcount,gcount,bcount=0,0,0
        r,g,b=[],[],[]
        out= set()
        for t in self.vdual.values():
            for it in t:
                if it.coords not in out:
                    if self.colors[it.coords] is 0:
                        rcount+=1
                        r.append(it)
                    elif self.colors[it.coords] is 1:
                        gcount+=1
                        g.append(it)
                    elif self.colors[it.coords] is 2:
                        bcount+=1
                        b.append(it)
                    out.add(it.coords)
        if rcount is gcount and rcount is bcount:
            return r,rcount
        if rcount<=gcount and rcount<=bcount:
            return r,rcount
        if gcount<=rcount and gcount<=bcount:
            return g,gcount
        if bcount<=rcount and bcount<=gcount:
            return b,bcount
