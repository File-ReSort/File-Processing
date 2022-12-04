import uuid
from Classes import Neo4j, Rules


class NodeManager:
    def __init__(self):
        self.nodeList = []
        # Key is node.text
        self.nodeDict = {}

    def add(self, node):
        self.nodeList.append(node)

    def remove(self, node_token_ID):
        for x in range(len(self.nodeList)):
            if self.nodeList[x].EntityID == node_token_ID:
                self.nodeList.remove(self.nodeList[x])

    def addEdge(self, node1_token_ID, edge):
        #find node 1
        for x in range(len(self.nodeList)):
            if self.nodeList[x].EntityID == node1_token_ID:
                self.nodeList[x].addEdgeOrigin(edge)

    def getGraph(self):
        return self.nodeList

    def serialize(self):
        nodes_serialized = []
        for node in self.nodeList:
            nodes_serialized.append(node.serialize())
            print("Node Serialized", node.serialize())

        new_obj = {"nodeList": nodes_serialized}
        print("Return Obj", new_obj)
        return new_obj

    def toNeo4j(self, url, username, password):
        neo4j = Neo4j.App(url, username, password)
        relationships = []

        # create all nodes
        for node in self.nodeList:
            # if node has relationships add to list
            if len(node.nodeEdgeOrigins) > 0:
                for edge in node.nodeEdgeOrigins:
                    relationships.append(Relationship(node.EntityID, edge.pointsTo, edge.edgeText))

        # Create Nodes
        neo4j.createNodesFromList(self.nodeList)

        print('CREATING RELATIONSHIPS')
        # create relationships between nodes
        neo4j.createRelationshipsFromList(relationships)

        neo4j.close()
        return 'success'

    def applyRules(self, dbUrl):
        rule_manager = Rules.RuleManager(dbUrl)
        for node in self.nodeList:
            # If node text matches with a rule(s) "Word", apply all rules to the node
            if rule_manager.get_rules().get(node.text[0]) is not None:
                print("FOUND MATCHING NODE TEXT WITH A RULE'S WORD", node.text[0])
                for rule in rule_manager.get_rules().get(node.text[0]):
                    print("ON RULE,", rule)
                    temp_rule_node = RuleNode(rule.relationship)

                    # SEE IF THE RULE'S RELATIONSHIP NODE EXISTS, if not create relationship node and add to dict
                    if self.nodeDict.get(rule.relationship) is None:
                        self.nodeDict[rule.relationship] = temp_rule_node
                        self.nodeList.append(temp_rule_node)
                        print("CREATED RELATIONSHIP NODE", temp_rule_node)

                    # ELSE GET THE RELATIONSHIP NODES ENTITYID AND CONTINUE
                    elif self.nodeDict.get(rule.relationship) is not None:
                        chosenNode = self.nodeDict.get(rule.relationship)
                        print("FOUND EXISTING RELATIONSHIP NODE", chosenNode)
                        temp_rule_node = chosenNode

                    # CREATE EDGE TO THE RELATIONSHIP NODE
                    node.addEdgeOrigin(NodeEdge(rule.rule, temp_rule_node.EntityID))

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
        node_edges = []
        for nodeEdge in self.nodeEdgeOrigins:
            node_edges.append(nodeEdge.serialize())

        return {
            "id": self.id,
            "nodeEdgeOrigins": node_edges,
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
        node_edges = []
        for nodeEdge in self.nodeEdgeOrigins:
            node_edges.append(nodeEdge.serialize())

        return {
            "id": self.EntityID,
            "nodeEdgeOrigins": node_edges,
            "text": self.text
        }

    def getCypherCreationQuery(self):
        return "CREATE (:Rule {"f" ID: -1, Text: \"{self.text}\", EntityID: \"{self.EntityID}\""" }) "


class NodeEdge:
    def __init__(self, edge_text, points_to_node_token_ID):
        self.edgeText = str(edge_text)
        self.pointsTo = points_to_node_token_ID

    def __repr__(self):
        return f"EdgeText: {self.edgeText} ----> NodeTokenID: {self.pointsTo}"

    def serialize(self):
        return {
            "edgeText": self.edgeText,
            "pointsTo": self.pointsTo
        }

class Relationship:
    def __init__(self, node1_ent_ID, node2_ent_ID, relationship_text):
        self.node1EntID = node1_ent_ID
        self.node2EntID = node2_ent_ID
        self.relationshipText = relationship_text


    def getCypherRelationshipQuery(self):
        e1 = "e" + str(uuid.uuid4()).replace('-', '')
        e2 = "e" + str(uuid.uuid4()).replace('-', '')
        return f"MATCH ({e1}), ({e2}) "f"WHERE {e1}.EntityID=\"{self.node1EntID}\" AND {e2}.EntityID=\"{self.node2EntID}\" "f"CREATE ({e1})-[:{self.relationshipText}]->({e2}) "