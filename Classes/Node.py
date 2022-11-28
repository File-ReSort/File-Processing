import uuid
from Classes import Neo4j


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

    def toNeo4j(self, url, username, password):
        neo4j = Neo4j.App(url, username, password)
        relationships = []

        # create all nodes
        for node in self.nodeList:
            neo4j.createNode(node.id, node.text[0], node.entityID, node.label)
            # if node has relationships add to list
            if len(node.nodeEdgeOrigins) > 0:
                for edge in node.nodeEdgeOrigins:
                    relationships.append({
                        "node1EntID": node.entityID,
                        "node2EntID": edge.pointsTo,
                        "relationshipText": edge.edgeText
                    })

        print('RELATIONSHIPS ------------------', relationships)
        # create relationships between nodes
        for relationship in relationships:
            neo4j.createRelationship(
                relationship["node1EntID"],
                relationship["node2EntID"],
                relationship["relationshipText"])

        neo4j.close()


class Node:
    def __init__(self, span, start, end, label):
        self.id = str(uuid.uuid4())
        self.nodeEdgeOrigins = []
        self.text = [t.text for t in span]
        self.entityID = int(span[0].i)
        self.start = start
        self.end = end
        self.label = label

    def __repr__(self):
        return f"NODE - ID: {self.id}, Text: {self.text}, NodeEdges: {self.nodeEdgeOrigins},  TokenID: {self.entityID}, Label {self.label}"

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
            "entityID": self.entityID,
            "label": self.label,
            "start": self.start,
            "end": self.end
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