import uuid

class NodeManager:
    def __init__(self):
        self.nodeList = []

    def add(self, Node):
        self.nodeList.append(Node)

    def remove(self, nodeTokenID):
        for x in range(len(self.nodeList)):
            if self.nodeList[x].entityID == nodeTokenID:
                self.nodeList.remove(self.nodeList[x])

    def addEdge(self, node1TokenID, edge):
        #find node 1
        for x in range(len(self.nodeList)):
            if self.nodeList[x].entityID == node1TokenID:
                self.nodeList[x].addEdgeOrigin(edge)

    def getGraph(self):
        return self.nodeList

class Node:
    def __init__(self, span):
        self.id = uuid.uuid4()
        self.nodeEdgeOrigins = []
        self.text = [t.text for t in span]
        self.entityID = span[0].i

    def __repr__(self):
        return f'NODE - ID: {self.id}, Text: {self.text}, NodeEdges: {self.nodeEdgeOrigins},  TokenID: {self.entityID}'

    def addEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.append(edge)

    def removeEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.remove(edge)

class NodeEdge:
    def __init__(self, edgeText, pointsToNodeTokenId):
        self.edgeText = edgeText
        self.pointsTo = pointsToNodeTokenId

    def __repr__(self):
        return f'EdgeText: {self.edgeText} ----> NodeTokenID: {self.pointsTo}'