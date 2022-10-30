import uuid

class Node:
    def __init__(self, span):
        self.id = uuid.uuid4()
        self.nodeEdgeOrigins = []
        self.text = [t.text for t in span]

    def addEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.append(edge)

    def removeEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.remove(edge)

class NodeEdge:
    def __init__(self, edgeText, pointsToNodeId):
        self.edgeText = edgeText
        self.pointsTo = pointsToNodeId