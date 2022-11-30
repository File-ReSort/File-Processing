import uuid
from Classes import Neo4j, Rules


class NodeManager:
    def __init__(self):
        self.nodeList = []
        # Key is node.text
        self.nodeDict = {}

    def add(self, Node):
        self.nodeList.append(Node)

    def remove(self, nodeTokenID):
        for x in range(len(self.nodeList)):
            if self.nodeList[x].EntityID == nodeTokenID:
                self.nodeList.remove(self.nodeList[x])

    def addEdge(self, node1TokenID, edge):
        #find node 1
        for x in range(len(self.nodeList)):
            if self.nodeList[x].EntityID == node1TokenID:
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
            # if node has relationships add to list
            if len(node.nodeEdgeOrigins) > 0:
                for edge in node.nodeEdgeOrigins:
                    relationships.append(Relationship(node.EntityID, edge.pointsTo, edge.edgeText))

        #Create Nodes
        neo4j.createNodesFromList(self.nodeList)

        print('CREATING RELATIONSHIPS')
        # create relationships between nodes
        neo4j.createRelationshipsFromList(relationships)

        neo4j.close()
        return 'success'

    def applyRules(self):
        ruleManager = Rules.RuleManager("https://cr8qhi8bu6.execute-api.us-east-1.amazonaws.com/prod/rules")
        for node in self.nodeList:
            # If node text matches with a rule(s) "Word", apply all rules to the node
            if ruleManager.getRules().get(node.text[0]) is not None:
                print("FOUND MATCHING NODE TEXT WITH A RULE'S WORD", node.text[0])
                for rule in ruleManager.getRules().get(node.text[0]):
                    print("ON RULE,", rule)
                    tempRuleNode = RuleNode(rule.relationship)

                    # SEE IF THE RULE'S RELATIONSHIP NODE EXISTS, if not create relationship node and add to dict
                    if self.nodeDict.get(rule.relationship) is None:
                        self.nodeDict[rule.relationship] = tempRuleNode
                        self.nodeList.append(tempRuleNode)
                        print("CREATED RELATIONSHIP NODE", tempRuleNode)

                    #ELSE GET THE RELATIONSHIP NODES ENTITYID AND CONTINUE
                    elif self.nodeDict.get(rule.relationship) is not None:
                        chosenNode = self.nodeDict.get(rule.relationship)
                        print("FOUND EXISTING RELATIONSHIP NODE", chosenNode)
                        tempRuleNode = chosenNode

                    # CREATE EDGE TO THE RELATIONSHIP NODE
                    node.addEdgeOrigin(NodeEdge(rule.rule, tempRuleNode.EntityID))

    def nodeListToDict(self):
        dict = {}
        for node in self.nodeList:
            dict[node.text[0]] = node
        self.nodeDict = dict


class Node:

    def __init__(self, span, start, end, label):
        self.id = str(uuid.uuid4())
        self.nodeEdgeOrigins = []
        self.text = [t.text for t in span]
        self.EntityID = int(span[0].i)
        self.start = start
        self.end = end
        self.label = label

    def __repr__(self):
        return f"NODE - ID: {self.id}, Text: {self.text}, NodeEdges: {self.nodeEdgeOrigins},  TokenID: {self.EntityID}, Label {self.label}"

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
            "entityID": self.EntityID,
            "label": self.label,
            "start": self.start,
            "end": self.end
        }

    def getCypherCreationQuery(self):
        return f"CREATE (:{self.label}"" {"f" ID: \"{self.id}\", Text: \"{self.text}\", EntityID: \"{self.EntityID}\""" }) "


class RuleNode:

    def __init__(self, text):
        self.EntityID = str(uuid.uuid4())
        self.nodeEdgeOrigins = []
        self.text = text

    def __repr__(self):
        return f"NODE - EntityID: {self.EntityID}, Text: {self.text}, NodeEdges: {self.nodeEdgeOrigins}"

    def addEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.append(edge)

    def removeEdgeOrigin(self, edge):
        self.nodeEdgeOrigins.remove(edge)

    def serialize(self):
        nodeEdges = []
        for nodeEdge in self.nodeEdgeOrigins:
            nodeEdges.append(nodeEdge.serialize())

        return {
            "id": self.EntityID,
            "nodeEdgeOrigins": nodeEdges,
            "text": self.text
        }

    def getCypherCreationQuery(self):
        return "CREATE (:Rule {"f" ID: -1, Text: \"{self.text}\", EntityID: \"{self.EntityID}\""" }) "


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

class Relationship:
    def __init__(self, node1EntID, node2EntID, relationshipText):
        self.node1EntID = node1EntID
        self.node2EntID = node2EntID
        self.relationshipText = relationshipText


    def getCypherRelationshipQuery(self):
        e1 = "e" + str(uuid.uuid4()).replace('-', '')
        e2 = "e" + str(uuid.uuid4()).replace('-', '')
        return f"MATCH ({e1}), ({e2}) "f"WHERE {e1}.EntityID=\"{self.node1EntID}\" AND {e2}.EntityID=\"{self.node2EntID}\" "f"CREATE ({e1})-[:{self.relationshipText}]->({e2}) "