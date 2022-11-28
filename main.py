# to start web server use: flask --app main run

from flask import Flask, request
from Classes import Document
import requests

app = Flask(__name__)

@app.route('/')
def hello_world():
    # neo4j = Neo4j.App(url, username, password)
    # neo4j.createNode(432, 'Duck', 1, "Bird")
    # neo4j.createNode(433, 'Dog', 2, "Mammal")
    #
    # # Node 1 --> Node 2
    # neo4j.createRelationship(432, 433, "Dislikes")
    # neo4j.close()

    return 'Flask is up and running'

url = 'neo4j+s://515235ac.databases.neo4j.io'
username = 'neo4j'
password = 'LYa5ggSL44lY23MF0A2RgRn6cCuo976Pes1OAVGw1dw'

# This route assumes that this is a new uploaded document and has never been processed before
@app.route('/processDocument', methods=['POST'])
def process_document():
    args = request.args
    document_location = args.get('location')
    document_name = args.get('name')
    n4jUrl = args.get('url')
    n4jUsername = args.get('username')
    n4jPassword = args.get('password')

    document = Document.Document(document_name, document_location)
    document.processDocument()

    nodeManager = document.getNodeManager()
    # send node manager data to neo4j
    nodeManager.toNeo4j(n4jUrl, n4jUsername, n4jPassword)

    nodeJson = nodeManager.serialize()
    annotations = document.getAnnotationJson()

    tempObj = {
        "NodeJson": nodeJson,
        "Annotations": annotations
    }

    return tempObj

@app.route('/getAnnotations', methods=['GET'])
def get_annotations():
    args = request.args
    print(args)
    document_location = args.get('location')
    document_name = args.get('name')

    document = Document.Document(document_name, document_location)
    document.processDocument()

    annotationJson = document.getAnnotationJson()

    return annotationJson