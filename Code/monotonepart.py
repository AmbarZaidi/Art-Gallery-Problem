#GroupID-26 (14114009_14114068)
#Date March,15 2018
# monotonepart.py: divide polygon in monotone partitions

import numpy as np
from DCELfile import *
DEBUG = False

def insertDgnl(d, p1, p2):
    if DEBUG:
        print "Inserting diagonal: ",p1,p2
    pointlist1 = []
    pointlist2 = []
    original_pts = d.getFaces()[1].getOuterBoundaryCoords()
    if (p1 in original_pts and p2 in original_pts) and p1!=p2:
        tmp1 = min(original_pts.index(p1), original_pts.index(p2))
        tmp2 = max(original_pts.index(p1), original_pts.index(p2))
        pointlist1 = original_pts[tmp1:(tmp2+1)]
        pointlist2 = original_pts[tmp2:]+original_pts[:(tmp1+1)]
        d1 = buildSimplePolygon(pointlist1)
        d2 = buildSimplePolygon(pointlist2)
        return [d1,d2]
    return [d]

# divide polygon in many // insert list of diagonals
def insertDgnls(d, dgnls):
    ngons = [d]
    while dgnls != []:
        nxt = dgnls.pop(0)
        print "Current dgnl:",nxt
        ngons = [insertDgnl(x, nxt[0], nxt[1]) for x in ngons]
        ngons = [ngon for lngon in ngons for ngon in lngon]
        print len(ngons)
    return ngons

class trapEdge(object):
    def __init__(self,a,b,s,l,r):
        self.left = a
        self.right = b
        self.pivot = s
        self.le = l
        self.re = r

class point(object):
    def __init__(self, a, b):
        self.x = a
        self.y = b
        
def onSegment(p,q,r):
    if (q.x <= max(p.x, r.x) and q.x >= min(p.x, r.x) and q.y <= max(p.y, r.y) and q.y >= min(p.y, r.y)):
        return True
    return False
def orientation(p,q,r):
    val = (q.y - p.y) * (r.x - q.x) -(q.x - p.x) * (r.y - q.y)
    if (val == 0):
        return 0
    if(val>0):
        return 1
    return 2
def doIntersect(p1,q1,p2,q2):
    o1 = orientation(p1, q1, p2);
    o2 = orientation(p1, q1, q2);
    o3 = orientation(p2, q2, p1);
    o4 = orientation(p2, q2, q1);
    A,B,C,D = p1,q1,p2,q2
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1*(A.x) + b1*(A.y)
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2*(C.x)+ b2*(C.y)
    determinant = a1*b2 - a2*b1
    if(determinant == 0):
        return False
    if (o1 != o2 and o3 != o4):
        return True
    if (o1 == 0 and onSegment(p1, p2, q1)):
        return True
    if (o2 == 0 and onSegment(p1, q2, q1)):
        return True
    if (o3 == 0 and onSegment(p2, p1, q2)):
        return True
    if (o4 == 0 and onSegment(p2, q1, q2)):
        return True
    return False

def findIt(A,B,C,D):
    a1 = B.y - A.y
    b1 = A.x - B.x
    c1 = a1*(A.x) + b1*(A.y)
    a2 = D.y - C.y
    b2 = C.x - D.x
    c2 = a2*(C.x)+ b2*(C.y)
    determinant = a1*b2 - a2*b1
    x = (b2*c1 - b1*c2)/determinant
    y = (a1*c2 - a2*c1)/determinant
    return (x, y)

def findIntersections(lines, hlines):
    res = {}
    for hline in hlines:
        p1 = point(hline[0],hline[1])
        q1 = point(hline[2],hline[3])
        for line in lines:
            p2 = point(line[0][0],line[0][1])
            q2 = point(line[0][2],line[0][3])
            if(doIntersect(p1,q1,p2,q2)):
                res[findIt(p1,q1,p2,q2)] = line[1]
    return res

def getTrapEdges(d):
    N = len(d.getVertices())
    verts = [ list(d.getVertices())[i].coords for i in range(N) ]
    verts = zip(verts, [i for i in list(d.getVertices())])
    edges = [(verts[i][1].next.coords,verts[i][1].coords) for i in range(N) ]
    edges = zip(edges, [v[1].getOutgoingEdges()[0] for v in verts])
    verts.sort(key=lambda x: -x[0][0])
    lines = []
    temp = []
    for e in edges:
        temp = [e[0][0][0],e[0][0][1],e[0][1][0],e[0][1][1]],e[1]
        lines.append(temp)
    lines2 = []
    temp = []
    for v in verts:
        temp = verts[0][0][0],v[0][1],verts[-1][0][0],v[0][1]
        lines2.append(temp)
    res = findIntersections(lines,lines2)

    res = [[x,y,res[(x,y)]] for (x,y) in res]
    res.sort(key = lambda x: -x[1])
    ret = []
    
    for v in verts:
        templ = [(x[0],x[1],x[2]) for x in res if (x[0]<v[0][0] and x[1]==v[0][1])]
        tempr = [(x[0],x[1],x[2]) for x in res if (x[0]>v[0][0] and x[1]==v[0][1])]
        templ.sort(key = lambda x: x[0])
        tempr.sort(key = lambda x: x[0])
        if( len(templ)%2==0 and len(tempr)%2==0 ):
            if v[1].getOutgoingEdges()[0].getTwin().origin.coords[1] < v[1].coords[1] :
                tr = trapEdge(v[0],v[0],v[1],v[1].getOutgoingEdges()[0],v[1].getOutgoingEdges()[1].getTwin())
            else:
                tr = trapEdge(v[0],v[0],v[1],v[1].getOutgoingEdges()[1],v[1].getOutgoingEdges()[0])
#                 tr = trapEdge(v[0],v[0],v[1],None,None)
            ret.append(tr)
        if( len(templ)%2==1 and len(tempr)%2==1 ):
            tr = trapEdge(templ[-1][:2],tempr[0][:2],v[1],templ[-1][2],tempr[0][2])
            ret.append(tr)
        if( len(templ)%2==0 and len(tempr)%2==1 ):
            tr = trapEdge(v[0],tempr[0][:2],v[1],v[1].getOutgoingEdges()[0], tempr[0][2])
            ret.append(tr)
        if( len(templ)%2==1 and len(tempr)%2==0 ):
            tr = trapEdge(templ[-1][:2],v[0],v[1],templ[-1][2],v[1].getOutgoingEdges()[1].getTwin())
            ret.append(tr)
    
    return ret

# returns list of diagonals for partioning

def monotonePartitioningDgnls(d):
    
    ret = getTrapEdges(d)
    ret = sorted(ret, key=lambda x:-x.pivot.coords[1])

    a = dict()
    b = dict()

    for x in ret:
        x.re = x.re.getTwin()
        if DEBUG:
            print "\n",x.left,x.right
            print "Pivot:",x.pivot.coords
            print "Ledge:",x.le.origin.coords,"-->",x.le.getTwin().origin.coords
            print "Redge:",x.re.origin.coords,"-->",x.re.getTwin().origin.coords


        if x.pivot.coords[1] > x.re.getTwin().origin.coords[1]:
            a[x.pivot] = (x.le,x.re)
            if x.le in b:
                b[x.le].append(x.pivot)
            else:
                b[x.le] = [x.pivot]

            if x.re in b:
                b[x.re].append(x.pivot)
            else:
                b[x.re] = [x.pivot]
                
#             if (x.pivot.getOutgoingEdges()[0].getTwin().origin.coords[1] < x.pivot.coords[1] and
#                 x.pivot.getOutgoingEdges()[1].getTwin().origin.coords[1] < x.pivot.coords[1] and
#                 x.pivot != x.le.origin ): # split vertex
                
#                 lc = x.pivot.getOutgoingEdges()[1]
#                 rc = x.pivot.getOutgoingEdges()[0]
                
#                 a.append((x.le,lc))
#                 a.append((rc,x.re))
                
                
                
# #                 if lc in b:
# #                     b[lc].append(x.pivot)
# #                 else:
# #                     b[lc] = [x.pivot]
                    
# #                 if rc in b:
# #                     b[rc].append(x.pivot)
# #                 else:
# #                     b[rc] = [x.pivot]
                
            

    for e in b:
        b[e].append(e.getTwin().origin)

    if DEBUG:
        print "\n### a"    
        for (i,x) in enumerate(a):
            print
            print i,x.coords
            for e in a[x]:
                print e.origin.coords, e.getTwin().origin.coords

        print "\n### b"
        for (i,x) in enumerate(b):
            print
            print i,x.origin.coords, x.getTwin().origin.coords
            print b[x]

    dgnls = []
    # pt = list(a.keys())[1]

    # print "]]]]",pt.coords
    # print a[pt]
    # print [x.coords for x in b[a[pt][0]] ],b[a[pt][0]].index(pt)
    # print [x.coords for x in b[a[pt][1]] ],b[a[pt][1]].index(pt),"[[[[["

    for pt in sorted(a, key=lambda x:-x.coords[1]):
        if DEBUG:
            print "\n]]]]",pt.coords
            print a[pt][0].origin.coords, a[pt][0].getTwin().origin.coords,
            print len(b[a[pt][0]]),[x.coords for x in b[a[pt][0]] ],b[a[pt][0]].index(pt)
            print a[pt][1].origin.coords, a[pt][1].getTwin().origin.coords,
            print len(b[a[pt][1]]),[x.coords for x in b[a[pt][1]] ],b[a[pt][1]].index(pt),"[[[[["

#         if not a[pt][0].origin == a[pt][1].origin:
#             print "in"
        if pt in ( a[pt][0].origin, a[pt][0].getTwin().origin ):
            dgnls.append((pt, b[a[pt][1]][b[a[pt][1]].index(pt)+1] ))
        elif pt in ( a[pt][1].origin, a[pt][1].getTwin().origin ):
            dgnls.append((pt, b[a[pt][0]][b[a[pt][0]].index(pt)+1] ))
        else:
            dgnls.append((pt,
                          min( b[a[pt][0]][b[a[pt][0]].index(pt)+1], 
                               b[a[pt][1]][b[a[pt][1]].index(pt)+1], 
                               key=lambda x:x.coords[1]
                             )
                         ))
        if DEBUG:
            print "Dgnls:",[(x[0].coords,x[1].coords) for x in dgnls]

    if DEBUG:
        print "ppp",[(x.origin,x.getTwin().origin) for x in d.getEdges()]
        for ww in dgnls:
            print ww in [(x.origin,x.getTwin().origin) for x in d.getEdges()]
    dgnls = list(set(dgnls)-set([(x.origin,x.getTwin().origin) for x in d.getEdges()]))
    return dgnls