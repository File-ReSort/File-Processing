# to start web server use: flask -app main run

from flask import Flask, request
from Classes import Document
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Flask is up and running'


# This route assumes that this is a new uploaded document and has never been processed before
@app.route('/ProcessDocument', methods=['GET'])
def process_document():
    args = request.args
    print(args)
    document_location = args.get('location')
    document_name = args.get('name')

    document = Document.Document(document_name, document_location)
    nodeManager = document.getNodeManager()

    # Send nodeManager.getGraph() information to Neo4j Here

    # Send document metaData using /setDocumentMeta API
    url = ''
    metaData = document.getMetaData()
    # requests.post(url, json=metaData)


    result = nodeManager.serialize()
    print(metaData)
    return result
