from neo4j import GraphDatabase

class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    def createNode(self, nodeID, nodeText, entityID, nodeType):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(self._create_node, nodeID, nodeText, entityID, nodeType)
            print("SUCCESSFULLY CREATED NODE", nodeText)

    @staticmethod
    def _create_node(tx, nodeID, nodeText, entityID, nodeType):
        query = (
            f"CREATE (e1:{nodeType}"" { ID: $node_ID, Text: $node_Text, EntityID: $node_entID }) "
            "RETURN e1 "
        )
        result = tx.run(query, node_ID=nodeID, node_Text=nodeText, node_entID=entityID)
        return result

    def createNodesFromList(self, nodes):
        #build query
        query = ""
        for node in nodes:
            query += node.getCypherCreationQuery()

        print("TRYING QUERY", query)
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(self._create_nodes_from_list, query)
            print("SUCCESSFULLY CREATED NODES FROM LIST")

    @staticmethod
    def _create_nodes_from_list(tx, query):
        result = tx.run(query)
        return result

    def createRelationship(self, node1EntID, nodeEnt2ID, relationshipText):
        with self.driver.session(database="neo4j") as session:
            result = session.execute_write(self._create_relationship, node1EntID, nodeEnt2ID, relationshipText)
            print("SUCCESSFULLY CREATED RELATIONSHIP", relationshipText)

    @staticmethod
    def _create_relationship(tx, node1EntID, nodeEnt2ID, relationshipText):
        query = (
            "MATCH (e1), (e2) "
            f"WHERE e1.EntityID=\"{node1EntID}\" AND e2.EntityID=\"{nodeEnt2ID}\" "
            f"CREATE (e1)-[r:{relationshipText}]->(e2); "
        )
        result = tx.run(query)
        return result

    def createRelationshipsFromList(self, relationshipList):

        with self.driver.session(database="neo4j") as session:
            for relationship in relationshipList:
                session.execute_write(self._create_relationship_from_list, relationship.getCypherRelationshipQuery())
            print("SUCCESSFULLY CREATED RELATIONSHIPS FROM LIST")

    @staticmethod
    def _create_relationship_from_list(tx, query):
        result = tx.run(query)
        return result
