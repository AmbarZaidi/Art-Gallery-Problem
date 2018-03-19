#GroupID-26 (14114009_14114068)
#Date March,15 2018
#DCELfile.py : File containing DCEL struct and buildSimplePloygon() function

import numpy as np
DEBUG = False

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
    def getOuterBoundaryCoords(self):
        original_pts = self.getOuterBoundary()
        return [x.origin.coords for x in original_pts]
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