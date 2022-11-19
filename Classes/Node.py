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

    def serialize(self):
        nodesSerialized = []
        for node in self.nodeList:
            nodesSerialized.append(node.serialize())
            print("Node Serialized", node.serialize())

        newObj = {"nodeList": nodesSerialized}
        print("Return Obj", newObj)
        return newObj


class Node:
    def __init__(self, span):
        self.id = str(uuid.uuid4())
        self.nodeEdgeOrigins = []
        self.text = [t.text for t in span]
        self.entityID = int(span[0].i)

    def __repr__(self):
        return f"NODE - ID: {self.id}, Text: {self.text}, NodeEdges: {self.nodeEdgeOrigins},  TokenID: {self.entityID}"

    def addEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.append(edge)

    def removeEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.remove(edge)

    def serialize(self):
        nodeEdges = []
        for nodeEdge in self.nodeEdgeOrigins:
            nodeEdges.append(nodeEdge.serialize())

        return {
            "id": self.id,
            "nodeEdgeOrigins": nodeEdges,
            "text": self.text,
            "entityID": self.entityID
        }


class NodeEdge:
    def __init__(self, edgeText, pointsToNodeTokenId):
        self.edgeText = str(edgeText)
        self.pointsTo = pointsToNodeTokenId

    def __repr__(self):
        return f"EdgeText: {self.edgeText} ----> NodeTokenID: {self.pointsTo}"

    def serialize(self):
        return {
            "edgeText": self.edgeText,
            "pointsTo": self.pointsTo
        }