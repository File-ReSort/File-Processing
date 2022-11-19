# flask -app main run

from flask import Flask, request
import json
import DocumentParser
import DocumentReader

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask is up and running'

@app.route('/ProcessDocument', methods=['GET'])
def df():
    args = request.args
    print(args)
    document_location = args.get('location')

    document = DocumentReader.Read(document_location)
    nodeManager = DocumentParser.ProcessDocumentText(document)

    fr = nodeManager.serialize()
    return fr