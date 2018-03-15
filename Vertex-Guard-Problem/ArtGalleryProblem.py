'''
@Author: Pranay Yadav, 12CS30025
@Description: Solving the Art Gallery Problem for N planar points given in CCW ordered (distinct) using the DCEL Data Structure

'''

import tkinter
class Point:
	def __init__(self, coordinates,auxData=None):
		self.data=auxData
		self.coords = coordinates
		self.edge = None
		self.ear = False
		self.next = None
		self.prev = None
		self.color= -1
	def ___str___(self):
		return str(self.ID)
	def __getitem__(self,key):
		return self.coords[key]
	def scale(self, k1, k2):
		self.coords = list(self.coords)
		self.coords[0] = int(self.coords[0] * k1)
		self.coords[1] = int(self.coords[1] * k2)
		self.coords = tuple(self.coords)
	def __hash__(self):
		return hash(id(self))
	def getData(self):
		return self.data
	def setData(self, auxData):
		self.data = auxData
	def getCoords(self):
		return Point(self.coords)
	def setCoords(self):
		self.coords = coordinates
	def getOutgoingEdges(self):
		visited = set()
		out = []
		here = self.edge
		while here and here not in visited:
			out.append(here)
			visited.add(here)
			temp = here.getTwin()
			if temp:
				here = temp.getNext()
			else:
				here = None
		return out
	def getIncidentEdge(self):
		return self.edge
	def setIncidentEdge(self, edge):
		self.edge = edge
	def __repr__(self):
		return 'DCEL.Point with coordnates (' + str(self.coords[0])+','+str(self.coords[1])+')'

class Edge:
	def __init__(self, auxData=None):
		self.data = auxData
		self.twin = None
		self.origin = None
		self.face = None
		self.next = None
		self.prev = None
	def __hash__(self):
		return hash(id(self))
	def getTwin(self):
		return self.twin
	def setTwin(self, twin):
		self.twin = twin
	def getData(self):
		return self.data
	def setData(self, auxData):
		self.data = auxData
	def getNext(self):
		return self.next
	def setNext(self, edge):
		self.next = edge
	def getOrigin(self):
		return self.origin
	def setOrigin(self, v):
		self.origin = v
	def getPrev(self):
		return self.prev
	def setPrev(self, edge):
		self.prev = edge
	def getDest(self):
		return self.twin.origin
	def getFace(self):
		return self.face
	def getFaceBoundary(self):
		visited = set()
		bound = []
		here = self
		while here and here not in visited:
			bound.append(here)
			visited.add(here)
			here = here.getNext()
		return bound
	def setFace(self, face):
		self.face = face
	def clone(self):
		c = Edge()
		c.data,c.twin,c.origin,c.face,c.next,c.prev = self.data,self.twin,self.origin,self.face,self.next,self.prev
	def __repr__(self):
		return 'DCEL.Edge from Origin: DCEL.Point with coordinates (' + str(self.getOrigin().coords[0])+','+str(self.getOrigin().coords[1])+')' + '\nDestination: DCEL.Point with coordinates (' + str(self.getDest().coords[0])+','+str(self.getDest().coords[1])+')'

class Face:
	def __init__(self, auxData=None):
		self.data = auxData
		self.outer = None
		self.inner = set()
		self.isolated = set()
	def __hash__(self):
		return hash(id(self))
	def getOuterComponent(self):
		return self.outer
	def setOuterComponent(self, edge):
		self.outer = edge
	def getData(self):
		return self.data
	def setData(self, auxData):
		self.data = auxData
	def getOuterBoundary(self):
		if self.outer:
			return self.outer.getFaceBoundary()
		else:
			return []
	def getInnerComponents(self):
		return list(self.inner)
	def addInnerComponent(self, edge):
		self.inner.add(edge)
	def removeInnerComponent(self, edge):
		self.inner.discard(edge)
	def removeIsolatedVertex(self,Point):
		self.isolated.discard(Point)
	def getIsolatedVertices(self):
		return list(self.isolated)
	def addIsolatedVertex(self,Point):
		self.isolated.add(Point)
	
class DCEL:
	def __init__(self):
		self.exterior = Face()
	def getExteriorFace(self):
		return self.exterior
	def getFaces(self):
		result = []
		known = set()
		temp = []
		temp.append(self.exterior)
		known.add(self.exterior)
		while temp:
			f = temp.pop(0)
			result.append(f)
			for e in f.getOuterBoundary():
				nb = e.getTwin().getFace()
				if nb and nb not in known:
					known.add(nb)
					temp.append(nb)
			for inner in f.getInnerComponents():
				for e in inner.getFaceBoundary():
					nb = e.getTwin().getFace()
					if nb and nb not in known:
						known.add(nb)
						temp.append(nb)
		return result
	
	def getEdges(self):
		edges = set()
		for f in self.getFaces():
			edges.update(f.getOuterBoundary())
			for inner in f.getInnerComponents():
				edges.update(inner.getFaceBoundary())
		return edges

	def getVertices(self):
		verts = set()
		for f in self.getFaces():
			verts.update(f.getIsolatedVertices())
			verts.update([e.getOrigin() for e in f.getOuterBoundary()])
			for inner in f.getInnerComponents():
				verts.update([e.getOrigin() for e in inner.getFaceBoundary()])
		return verts

def buildSimplePolygon(points):
	d = DCEL()
	if points:
		exterior = d.getExteriorFace()
		interior = Face()
		verts = []
		for p in points:
			verts.append(Point(p))
		innerEdges = []
		outerEdges = []
		for i in range(len(verts)):
			e = Edge()
			e.setOrigin(verts[i])
			verts[i].setIncidentEdge(e)
			e.setFace(interior)
			t = Edge()
			t.setOrigin(verts[(i+1)%len(verts)])
			t.setFace(exterior)
			t.setTwin(e)
			e.setTwin(t)
			innerEdges.append(e)
			outerEdges.append(t)

		for i in range(len(verts)):
			innerEdges[i].setNext(innerEdges[(i+1)%len(verts)])
			innerEdges[i].setPrev(innerEdges[i-1])
			outerEdges[i].setNext(outerEdges[i-1])
			outerEdges[i].setPrev(outerEdges[(i+1)%len(verts)])
		interior.setOuterComponent(innerEdges[0])
		exterior.addInnerComponent(outerEdges[0])   
	return d


class Triangulation:
	def __init__(self, head = None, size = 0):
		self.HEAD = head
		self.SIZE = size
	def cloneLinkedList(self):
		cursor = self.HEAD
		newHead = Point(cursor)
		newHead.ear = cursor.ear
		cursor = cursor.next
		newCursor = newHead
		while cursor.coords is not self.HEAD.coords:
			newPoint = Point(cursor)
			newPoint.ear = cursor.ear
			newCursor.next = newPoint
			newPoint.prev = newCursor
			cursor = cursor.next
			newCursor = newPoint 
		newHead.prev = newCursor
		newCursor.next = newHead
		return newHead, self.SIZE
	
	def Area(self, a, b, c):
		ap=a.coords
		bp=b.coords
		cp=c.coords
		a1 = (bp[0] - ap[0]) * 1.0 * (cp[1] - ap[1])
		a2 = (cp[0] - ap[0]) * 1.0 * (bp[1] - ap[1])
		area2 = a1 - a2
		if area2 > 0.5:
			return 1
		if area2 < -0.5:
			return -1
		return 0

	
	def AreaDet(self, a, b, c):
		return ((b.coords[0] - a.coords[0]) * (c.coords[1] - a.coords[1])) - ((c.coords[0] - a.coords[0]) * (b.coords[1] - a.coords[1]))

	def boolXOR(self, x, y):
		return x is not y

	def liesLeft(self, a,b,c):
		return self.Area(a,b,c) > 0

	def liesLeftOrOn(self, a,b,c):
		return self.Area(a,b,c) >= 0

	def Collinear(self, a,b,c):
		return self.Area(a,b,c) == 0

	def Between(self, a, b, c):
		if not self.Collinear(a, b, c):
			return False
		if a.coords[0] != b.coords[0]:
			return (a.coords[0] <= c.coords[0] and c.coords[0] <= b.coords[0]) or (a.coords[0] >= c.coords[0] and c.coords[0] >= b.coords[0])
		else:
			return (a.coords[1] <= c.coords[1] and c.coords[1] <= b.coords[1]) or (a.coords[1] >= c.coords[1] and c.coords[1] >= b.coords[1])

	def Intersect(self, a, b, c , d):
		if self.intersectPr(a, b, c, d):
			return True
		elif self.Between(a, b, c) or self.Between(a, b, d) or self.Between(c,d,a) or self.Between(c, d, b):
			return True
		return False

	def Dgnlize(self, a, b, HEAD):
		c = HEAD
		c1 = None
		while True:
			c1 = c.next
			if (c is not a) and (c1 is not a) and (c is not b) and (c1 is not b) and self.Intersect(a, b, c, c1):
				return False
			c = c.next
			if c is HEAD:
				break
		return True

	def EarInit(self, HEAD):
		v0 = None
		v1 = None
		v2 = None
		v1 = HEAD
		while True:
			v2 = v1.next
			v0 = v1.prev
			v1.ear = self.Dgnl(v0, v2, HEAD)
			v1 = v1.next
			if v1 is HEAD:
				break

	def Triangulate(self):
		v0 = None
		v1 = None
		v2 = None
		v3 = None
		v4 = None
		earfound = False
		returnlist = []
		self.EarInit(self.HEAD)
		HEAD, n = self.cloneLinkedList()
		while n > 3:
			v2 = HEAD
			earfound = False
			while True:
				if v2.ear:
					earfound = True
					v3 = v2.next
					v4 = v3.next
					v1 = v2.prev
					v0 = v1.prev
					tri = [v1, v2, v3]
					returnlist.append(tri)
					v1.ear = self.Dgnl(v0, v3, HEAD)
					v3.ear = self.Dgnl(v1, v4, HEAD)
					v1.next = v3
					v3.prev = v1
					HEAD = v3
					n -= 1
					if n == 3:
						v2 = HEAD
						v1 = v2.prev
						v3 = v2.next
						tri = [v1, v2, v3]
						returnlist.append(tri)
						return returnlist
					break
				v2 = v2.next
				if v2 is HEAD:
					break
			if not earfound:
				break
		return returnlist

	def iCON(self, a, b):
		a0 = None
		a1 = None
		a1 = a.next
		a0 = a.prev
		if self.liesLeftOrOn(a, a1, a0):
			return self.liesLeft(a,b,a0) and self.liesLeft(b,a,a1)
		return not (self.liesLeftOrOn(a,b,a1) and self.liesLeft(b,a,a0))

	def intersectPr(self, a, b, c, d):
		if self.Collinear(a,b,c) or self.Collinear(a,b,d) or self.Collinear(c,d,a) or self.Collinear(c,d,b):
			return False
		return self.boolXOR(self.liesLeft(a,b,c), self.liesLeft(a,b,d)) and self.boolXOR(self.liesLeft(c,d,a) , self.liesLeft(c,d,b))

	def Dgnl(self, a, b, HEAD):
		return self.iCON(a,b) and self.iCON(b, a) and self.Dgnlize(a,b, HEAD)

	def drawPolygon(self, canvas):
		cursor = self.HEAD
		while True:
			x1 = cursor.coords[0]
			y1 = cursor.coords[1]
			x2 = cursor.next.coords[0]
			y2 = cursor.next.coords[1]
			#label = tkinter.Label(canvas, text = "("+str(cursor.coords[0])+","+str(cursor.coords[1])+")", font = "Times 6")
			#label.place(x = x1 + 4, y = 700 - (y1 + 4))
			canvas.create_line(x1, 700 - y1, x2, 700 - y2, width = 2.0, fill = 'black')
			canvas.create_oval(x1 - 4, 700 - (y1 - 4), x1 + 4, 700 - (y1 + 4), fill = 'black')
			cursor = cursor.next
			if cursor.coords is self.HEAD.coords:
				break

	def drawTriangles(self, canvas, triangles):
		pointlist = []
		cursor = self.HEAD
		while True:
			pointlist.append(cursor)
			cursor = cursor.next
			if cursor.coords is self.HEAD.coords:
				break
		if len(triangles) > 0:
			for t in triangles:
				canvas.create_line(t[0].coords[0], 700 - t[0].coords[1], t[1].coords[0], 700 - t[1].coords[1],width = 1.0, fill = 'red')
				canvas.create_line(t[0].coords[0], 700 - t[0].coords[1], t[2].coords[0], 700 - t[2].coords[1],width = 1.0, fill = 'red')
				canvas.create_line(t[2].coords[0], 700 - t[2].coords[1], t[1].coords[0], 700 - t[1].coords[1],width = 1.0, fill = 'red')

	def scale(self, uniform = False):
		xmin = 1000000000 # Initialize to some huge numbers
		ymin = 1000000000
		cursor = self.HEAD
		while True:
			if cursor.coords[0] < xmin:
				xmin = cursor.coords[0]
			if cursor.coords[1] < ymin:
				ymin = cursor.coords[1]
			cursor = cursor.next
			if cursor.coords is self.HEAD.coords:
				break
		
		cursor = self.HEAD
		while True:
			cursor.coords = list(cursor.coords)
			cursor.coords[0] = cursor.coords[0] - xmin + 10
			cursor.coords[1] = cursor.coords[1] - ymin + 10
			cursor = cursor.next
			if cursor.coords is self.HEAD.coords:
				break
		
		xmin = 1000000000
		ymin = 1000000000
		xmax = 0
		ymax = 0
		cursor = self.HEAD
		while True:
			if cursor.coords[0] < xmin:
				xmin = cursor.coords[0]
			if cursor.coords[1] < ymin:
				ymin = cursor.coords[1]
			if cursor.coords[0] > xmax:
				xmax = cursor.coords[0]
			if cursor.coords[1] > ymax:
				ymax = cursor.coords[1]
			cursor = cursor.next
			if cursor.coords is self.HEAD.coords:
				break
		
		k1 = 990.0 / xmax
		k2 = 550.0 / ymax
		if uniform:
			if k1 < k2:
				k2 = k1
			else:
				k1 = k2
		cursor = self.HEAD
		while True:
			cursor.scale(k1, k2)
			cursor = cursor.next
			if cursor.coords is self.HEAD.coords:
				break

def dualgraph(map_points,listTriangle):
  	dvert={i:listTriangle[i] for i in range(0,len(listTriangle))}
  	dedge={}
  	for i in range(0,len(listTriangle)):
  		j=i+1
  		for j in range(0,len(listTriangle)):
  			if len(list(set(listTriangle[i])&set(listTriangle[j]))) > 1:
  				if i in dedge and j not in dedge[i] and i is not j:
  					dedge[i].append(j)
  				elif i not in dedge and i is not j:
  					dedge[i]=[j]	
  				if j in dedge and i not in dedge[j] and i is not j:
  					dedge[j].append(i)
  				elif j not in dedge and i is not j:
  					dedge[j]=[i]	
  	return dvert,dedge					

def DFS(s,vdual,edual):
    visited, stack = set(), [s]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            colorsum = vdual[vertex][0].color+vdual[vertex][1].color+vdual[vertex][2].color
            if colorsum<3:
            	print ("Triangle #"+str(vertex)+" has one vertex uncolored!!!")
            	if vdual[vertex][0].color is -1:
            		vdual[vertex][0].color = 3-vdual[vertex][1].color-vdual[vertex][2].color
            		print ("Triangle #"+str(vertex)+" Vertex #0 found uncolored!!! Now colored to "+str(vdual[vertex][0].color))
            	elif vdual[vertex][1].color is -1:
            		vdual[vertex][1].color = 3-vdual[vertex][0].color-vdual[vertex][2].color
            		print ("Triangle #"+str(vertex)+" Vertex #1 found uncolored!!! Now colored to "+str(vdual[vertex][1].color))
            	elif vdual[vertex][2].color is -1:
            		vdual[vertex][2].color = 3-vdual[vertex][1].color-vdual[vertex][0].color		 
            		print ("Triangle #"+str(vertex)+" Vertex #2 found uncolored!!! Now colored to "+str(vdual[vertex][2].color))
            visited.add(vertex)
            stack.extend(set(edual[vertex]) - visited)
    return visited

def colorize(map_points,listTriangle,vdual,edual):
  	ear_vertex=None
  	ear_tri=None
  	key=None
  	for ear_vertex in map_points:
  		if map_points[ear_vertex].ear:
  			break;

  	for ear_tri in listTriangle:
  		if ear_vertex in ear_tri:
  			break

  	for key in vdual:
  		if vdual[key] is ear_vertex:
  			break

  	print("############################# INITIAL COLORING OF ONE TRIANGLE ##################################")
  	print ("Triangle #"+str(key)+" Vertex #0 colored to 0")
  	ear_tri[0].color = 0
  	print ("Triangle #"+str(key)+" Vertex #1 colored to 1")
  	ear_tri[1].color = 1
  	print ("Triangle #"+str(key)+" Vertex #2 colored to 2")
  	ear_tri[2].color = 2
  	print("############################# GOING TO COLOR REMAINING TRIANGLES ###############################")
  	DFS(key,vdual,edual)
  	output,col = findMinColor(vdual.values())
  	print("Guards are colored "+str(col-1))

def findMinColor(triangles):
	rcount,gcount,bcount=0,0,0
	r,g,b=[],[],[]
	out= set()
	for t in triangles:
		for it in t:
			if it not in out:
				if it.color is 0:
					rcount+=1
					r.append(it)
				elif it.color is 1:
					gcount+=1
					g.append(it)
				elif it.color is 2:
					bcount+=1
					b.append(it)	
				out.add(it)	
	if rcount is gcount and rcount is bcount:
		return r,rcount
	if rcount<=gcount and rcount<=bcount:
		return r,rcount
	if gcount<=rcount and gcount<=bcount:
		return g,gcount
	if bcount<=rcount and bcount<=gcount:
		return b,bcount

p=[]
N= int(input())
lines=[input().strip() for i in range(0,N)]
p=[(int(lines[i].split()[0]),int(lines[i].split()[1])) for i in range(0,len(lines))]
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

T = Triangulation(map_points[p[0]],len(map_points))
listTriangle = T.Triangulate()
print("################################# TRIANGULATED REGIONS ####################################")
for i,items in enumerate(listTriangle):
	print("Triangle #"+str(i))
	print(items[0])
	print(items[1])
	print(items[2])

print("################################ GRAPHICAL VIEW #####################################")
canvas_width = 1000
canvas_height = 600
master = tkinter.Tk()
canvas = tkinter.Canvas(master, width=canvas_width, height=canvas_height)
canvas.pack()
T.scale(True)
T.drawTriangles(canvas, listTriangle)
T.drawPolygon(canvas)
tkinter.mainloop()

#for key in map_points:
# 	if map_points[key].ear:
# 		print (map_points[key])
# 		print ("is a ear!!"

print("############################### CONSTRUCTING DUAL GRAPH ############################")
vdual,edual = dualgraph(map_points,listTriangle)
print("############################### COLORIZING BEGINS ##################################")
colorize(map_points,listTriangle,vdual,edual)
