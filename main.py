# to start web server use: flask --app main run

from flask import Flask, request
from Classes import Document
import requests
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Flask is up and running'

@app.route('/test', methods=['POST'])
def test_func():
    file = request.files['file']
    file.stream.seek(0)
    file.save(f'TempUploads/{file.filename}')
    return 'Success'

# This route assumes that this is a new uploaded document and has never been processed before
@app.route('/processDocument', methods=['POST'])
def process_document():
    # check dynamo db to see if document exists and implement logic TODO

    # save file locally
    args = request.args
    file = request.files['file']
    file.stream.seek(0)
    saveLocation = f'TempUploads/{file.filename}'

    file.save(saveLocation)
    n4jUrl = args.get('url')
    n4jUsername = args.get('username')
    n4jPassword = args.get('password')

    document = Document.Document(file.filename, saveLocation)
    document.processDocument()

    # upload file to bucket here
    bucketUrl = f"https://file-resort-storage.s3.amazonaws.com/{document.id}-{file.filename}"
    response = requests.put(bucketUrl, data=open(saveLocation, 'rb'))
    print("RESPONSE:", response.headers, response.text)
    document.setBucketFileLocation(bucketUrl)

    nodeManager = document.getNodeManager()
    nodeManager.applyRules()
    # send node manager data to neo4j
    nodeManager.toNeo4j(n4jUrl, n4jUsername, n4jPassword)

    # nodeJson = nodeManager.serialize()
    annotations = document.getAnnotationJson()
    metaData = document.getMetaData()

    print("META DATA:\n", metaData)

    tempObj = {
        "BucketFileLocation": metaData['BucketFileLocation'],
        "FileName": metaData['FileName'],
        "ID": metaData['ID'],
        "LastEditDate": metaData['LastEditDate'],
        "Name": metaData['Name'],
        "UploadDate": metaData['UploadDate'],
        "Annotations": annotations["annotations"]
    }

    url = "https://cr8qhi8bu6.execute-api.us-east-1.amazonaws.com/prod/document"
    response = requests.post(url, data=json.dumps(tempObj), headers={"content-type": "application/json"})
    print("RESPONSE:", response.headers, response.text)

    # delete local file
    document.deleteFile()

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