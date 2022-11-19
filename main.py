# flask -app main run

from flask import Flask, request
from Classes import Document

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask is up and running'

# This route assumes that this is a new uploaded document and has never been processed before
@app.route('/ProcessDocument', methods=['GET'])
def df():
    args = request.args
    print(args)
    document_location = args.get('location')

    document = Document.Document(document_location)
    nodeManager = document.getNodeManager()

    result = nodeManager.serialize()
    return result
