#GroupID-26 (14114009_14114068)
#Date March,15 2018
#main.py File calling all the functions and the GUI

from numpy.random import randint
from easygui import multenterbox
from numpy import lexsort,asarray,append
from matplotlib.pyplot import figure,show
import matplotlib.pyplot as plt
from Colorizer import *
from DCELfile import *
from monotonepart import *
from triangulatemono import *
DEBUG = False

msg = "Enter the value of 'n'"
title = "Polygon with 'n' sides"
fieldNames = ["  n"]
fieldValues = multenterbox(msg,title,fieldNames)
while 1:
    if fieldValues == None: break
    errmsg = ""
    try:
        int(fieldValues[0])
    except:
        errmsg = errmsg + ('%s is a required to be a number.\n\n' % fieldNames[0])
    if fieldValues[0].strip() == "":
        errmsg = errmsg + ('%s is a required field.\n\n' % fieldNames[0])
    if errmsg == "": break
    fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)
    
n = int(fieldValues[0])
from numpy.random import randint
from numpy import lexsort,asarray,append
coords = randint(0,90000, size=(2,n))
x = coords[0] 
y = coords[1]
ind = lexsort((y,x))
coords = [(x[i],y[i]) for i in ind] 
x = asarray([c[0] for c in coords])
y = asarray([c[1] for c in coords])
pivot = coords[0]

y_diff_pivot = y-pivot[1]
x_diff_pivot = x-pivot[0]
tan = (y_diff_pivot[1:]+0.0)/x_diff_pivot[1:]

pairs = zip(tan,coords[1:])
pairs = sorted(pairs, key = lambda (x,y): x)

coords = asarray([pivot])
coords = append(coords, asarray( zip(*pairs)[-1] ), axis=0 )
coords = append(coords, asarray([pivot]), axis=0 )

p=[(c[1],c[0]) for c in coords][::-1][1:]
d = buildSimplePolygon(p)
print("################################ DCEL POLYGON FORMED ###################################")
map_points ={x.coords:x for x in d.getVertices()}
for i in range(1,len(p)-1):
    map_points[p[i]].next = map_points[p[i+1]]
    map_points[p[i+1]].prev = map_points[p[i]]
map_points[p[0]].prev = map_points[p[-1]]
map_points[p[0]].next = map_points[p[1]]
map_points[p[1]].prev = map_points[p[0]]
map_points[p[-1]].next = map_points[p[0]]

d1 = d
def newline(p, q):
    X = np.linspace(p[0], q[0],endpoint=True)
    Y = np.linspace(p[1],q[1],endpoint=True)
    return X,Y

def nowDraw(toDraw):
    for x in toDraw:
        plt.plot(x[0],x[1],x[2])
    plt.show()

toDraw = []
for e in d.getEdges():
    p1,q1 = list(e.origin.coords),list(e.getTwin().origin.coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'r'])

nowDraw(toDraw)
DEBUG = False
ret = getTrapEdges(d)
for r in ret:
    X,Y = newline(r.left,r.right)
    toDraw.append([X,Y,'b'])
    toDraw.append([r.pivot.coords[0],r.pivot.coords[1],'go'])

nowDraw(toDraw)
DEBUG = False
diagnls = monotonePartitioningDgnls(d)
for dg in  diagnls:
    X,Y = newline(dg[0].coords,dg[1].coords)
    toDraw.append([X,Y,'g'])

nowDraw(toDraw)
listOfMonos = insertDgnls(d,[(x[0].coords,x[1].coords) for x in diagnls])
import os
def createMonoPolygon(d,p):
    f = open('cgalinput','w')
    f.write(str(len(p))+"\n")
    for c in p:
        f.write(str(c[0])+" "+str(c[1])+" ")
    f.close()
    os.system("g++ makemonotone.cpp -lCGAL -lgmp")
    os.system("./a.out > cgalout")
    # call(["./a.out","> cgalout"])
    with open('cgalout','r') as f:
        content = f.readlines()
    content = [x.strip() for x in content] 
    result = []
    # print content
    for c in content:
        c = c.split(' ')
        print c
        n = c[0]
        j = 1
        p = []
        for i in range(int(n)):
            p.append((float(c[j]),float(c[j+1])))
            j += 2
        d = buildSimplePolygon(p)
        # print("################################ DCEL POLYGON FORMED ###################################")
        map_points ={x.coords:x for x in d.getVertices()}
        for i in range(1,len(p)-1):
            map_points[p[i]].next = map_points[p[i+1]]
            map_points[p[i+1]].prev = map_points[p[i]]
        map_points[p[0]].prev = map_points[p[-1]]
        map_points[p[0]].next = map_points[p[1]]
        map_points[p[1]].prev = map_points[p[0]]
        map_points[p[-1]].next = map_points[p[0]]
        result.append(d)
    return result

listOfMonos = createMonoPolygon(d,p)

toDraw = []
for m in listOfMonos:
    for e in m.getEdges():
        p1,q1 = list(e.origin.coords),list(e.getTwin().origin.coords)
        X,Y = newline(p1,q1)
        toDraw.append([X,Y,''])
        toDraw.append([e.origin.coords[0],e.origin.coords[1],'o'])
nowDraw(toDraw)

DEBUG = True
toDraw = []
listOfTriangles = []
tmp = -1
# print len(listOfMonos)
for mono in listOfMonos:
    diagnls = triangulateMonotonePolygon(mono)
    vv = [(x[0].coords,x[1].coords) for x in diagnls]
    listOfTriangles += insertDgnls(mono,vv)
#     print listOfTriangles
    tmp+=len(diagnls)+1
# print "\n",tmp
# print len(listOfTriangles)
listOfTriangles = [[t.getFaces()[1].getOuterBoundary()[0].origin,
                    t.getFaces()[1].getOuterBoundary()[1].origin,
                    t.getFaces()[1].getOuterBoundary()[2].origin
                   ] for t in listOfTriangles]
# for i,t in enumerate(listOfTriangles):
#     print i,'[',t.getFaces()[1].getOuterBoundary()[0].origin.coords, \
#            t.getFaces()[1].getOuterBoundary()[1].origin.coords, \
#            t.getFaces()[1].getOuterBoundary()[2].origin.coords,           ']'

# print len(listOfTriangles)
for t in listOfTriangles:
    p1,q1 = list(t[0].coords),list(t[1].coords)
#     print p1,q1,list(t[2].coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'r'])
    p1,q1 = list(t[1].coords),list(t[2].coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'b'])
    p1,q1 = list(t[2].coords),list(t[0].coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'g'])


nowDraw(toDraw)

colorizer = Colorizer(d,listOfTriangles)
x = colorizer.colorize()
# print x
toDraw = []
for e in d1.getEdges():
    p1,q1 = list(e.origin.coords),list(e.getTwin().origin.coords)
    X,Y = newline(p1,q1)
    toDraw.append([X,Y,'r'])
for g in x[0]:
    toDraw.append([g.coords[0],g.coords[1],'bo'])
plt.plot(0,0, label='Gaurds required: '+str(x[1]))
plt.legend()
nowDraw(toDraw)
os.system('rm cgalinput cgalout a.out')
