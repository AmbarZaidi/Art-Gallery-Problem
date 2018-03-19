#GroupID-26 (14114009_14114068)
#Date March,15 2018
#triangulatemono.py: triangulate Monotone Polygon // get list of diagonals

import numpy as np
from DCELfile import *
DEBUG = False

def Orientation(p,q,r):
    p=p.coords
    q=q.coords
    r=r.coords
    val = ( q[1] - p[1] )*( r[0] - q[0] ) - ( q[0] - p[0] )* ( r[1] - q[1] )
    return -val

def reflex(p,q,r,chain = 'l'):
    if(chain == 'r'):
        if Orientation(p,q,r)>=0:
            return True
        else:
            return False
    elif(chain == 'l'):
        if Orientation(p,q,r)>0:
            return False
        else:
            return True
    

def triangulateMonotonePolygon(d):
    pts = [x.origin for x in d.getFaces()[1].getOuterBoundary()]
    if DEBUG:
        print "Polygon Boundary:",[x.coords for x in pts]
    min_index = min(enumerate(pts), key=lambda x:x[1].coords[1])[0]
    max_index = max(enumerate(pts), key=lambda x:x[1].coords[1])[0]
    tmp1 = min(min_index,max_index)
    tmp2 = max(min_index,max_index)
    chain1 = pts[tmp1:(tmp2+1)] 
    chain2 = pts[tmp2:]+pts[:(tmp1+1)] 
    
    if(min(chain1, key=lambda x:x.coords[0]).coords[0] >min(chain2, key=lambda x:x.coords[0]).coords[0]):    # ensuring chain1 is left chain
        if DEBUG:
            print "Monotone chains swapped"
        tmp = list(chain1)
        chain1 = chain2
        chain2 = tmp
    if DEBUG:
        print "Left Chain     : ",[x.coords for x in chain1]
        print "Right Chain    : ",[x.coords for x in chain2]
    pts = sorted(pts, key = lambda x:-x.coords[1])
    if DEBUG:
        print "\nSorted pts     : ",[x.coords for x in pts]
        print
    
    queue = []
    diagonals = []
    
    queue.append(pts[0])
    queue.append(pts[1])
    
    i = 2
    while i < (len(pts)-1):
        if DEBUG:
            print "\ni =",i,";",pts[i].coords
        #process(pts[i])
        tmp1 = queue[-1] in chain1
        tmp2 = pts[i] in chain1 
        if (tmp1 and not tmp2) or (tmp2 and not tmp1):
            for qpt in queue[1:]:
                diagonals.append((pts[i], qpt))
                if DEBUG:
                    print "Case: a;  \nDiagonals:", [(x[0].coords,x[1].coords) for x in diagonals]
            queue = [queue[-1],pts[i]]
            if DEBUG:
                print "Queue: ",[x.coords for x in queue]
        else:
            if DEBUG:
                print "||||||",queue[-2],queue[-1],pts[i],"chain =", ('l' if tmp1 else 'r'),"|||||"
                print reflex(queue[-2],queue[-1],pts[i],chain = ('l' if tmp1 else 'r') )
                print Orientation(queue[-2],queue[-1],pts[i] )
            if reflex(queue[-2],queue[-1],pts[i],chain = ('l' if tmp1 else 'r') ):
                queue.append(pts[i])
                if DEBUG:
                    print "Case: b;  \nDiagonals:",# reflex
                    print [(x[0].coords,x[1].coords) for x in diagonals]
                    print "Queue: ",[x.coords for x in queue]
            else:
                diagonals.append((pts[i], queue[-2]))
                if DEBUG:
                    print "Case: c;  \nDiagonals:", # convex
                    print [(x[0].coords,x[1].coords) for x in diagonals]
                    print "Queue: ",[x.coords for x in queue]
                queue.pop(-1)
                if len(queue) == 1:
                    queue.append(pts[i])
                else:
                    i-=1
        i+=1
    
    if len(queue)>2:
        for qpt in queue[1:-1]:
                diagonals.append((pts[i], qpt))
                if DEBUG:
                    print "Case: a;  \nDiagonals:", [(x[0].coords,x[1].coords) for x in diagonals]
    
    if DEBUG:
        print "Queue: ",[x.coords for x in queue]
    return diagonals
            
        
# triangulateMonotonePolygon(d)
# listOfTriangles = insertDgnls(d,triangulateMonotonePolygon(d))
