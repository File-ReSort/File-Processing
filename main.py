# to start web server use: flask --app main run

from flask import Flask, request
from Classes import Document, Rules

app = Flask(__name__)

@app.route('/')
def hello_world():
    Rules.RuleManager("https://cr8qhi8bu6.execute-api.us-east-1.amazonaws.com/prod/rules")
    return 'Flask is up and running'

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