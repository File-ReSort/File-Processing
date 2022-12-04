# to start web server use: flask --app main run
# https://nagasudhir.blogspot.com/2022/10/waitress-as-flask-server-wsgi.html

import time
from flask import Flask, request
from Classes import Document, log
from waitress import serve
import requests
import json
import os

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
    print("Received /processDocument request")
    start_time = time.time()
    args = request.args
    n4j_url = args.get('url')
    n4j_username = args.get('username')
    n4j_password = args.get('password')
    friendly_name = args.get('name')
    # check dynamo db to see if document exists and implement logic TODO

    # save file locally
    if not os.path.exists('TempUploads'):
        os.makedirs('TempUploads')
    file = request.files['file']
    file.stream.seek(0)
    save_location = f'TempUploads/{file.filename}'
    file.save(save_location)

    document = Document.Document(friendly_name, save_location)
    document.processDocument()

    # upload file to bucket here
    log.printSection("Uploading File to Bucket")
    bucket_url = f"https://file-resort-storage.s3.amazonaws.com/{document.id}-{file.filename}"
    response = requests.put(bucket_url, data=open(save_location, 'rb'))
    print("RESPONSE:", response.headers, response.text)
    document.setBucketFileLocation(bucket_url)

    # apply rules from ruledb
    rule_db_url = "https://cr8qhi8bu6.execute-api.us-east-1.amazonaws.com/prod/rules"
    node_manager = document.getNodeManager()
    node_manager.applyRules(rule_db_url)

    # send node manager data to neo4j
    log.printSection("Sending Node Data to Neo4j")
    node_manager.toNeo4j(n4j_url, n4j_username, n4j_password)

    annotations = document.getAnnotationJson()
    meta_data = document.getMetaData()

    temp_obj = {
        "BucketFileLocation": meta_data['BucketFileLocation'],
        "FileName": meta_data['FileName'],
        "ID": meta_data['ID'],
        "LastEditDate": meta_data['LastEditDate'],
        "Name": meta_data['Name'],
        "UploadDate": meta_data['UploadDate'],
        "Annotations": annotations["annotations"]
    }

    # send processed document data to Dynamo
    log.printSection("Sending Document Data to Dynamo")
    url = "https://cr8qhi8bu6.execute-api.us-east-1.amazonaws.com/prod/document"
    response = requests.post(url, data=json.dumps(temp_obj), headers={"content-type": "application/json"})
    print("RESPONSE:", response.headers, response.text)

    # delete local file
    document.deleteFile()

    log.printSection("Returning")
    print(temp_obj)

    print("---Time Elapsed: %s seconds ---" % (time.time() - start_time))
    return temp_obj


# this endpoint processes document text and only returns annotation data
@app.route('/getAnnotations', methods=['POST'])
def get_annotations():
    print("Received /getAnnotations request")
    start_time = time.time()

    if not os.path.exists('TempUploads'):
        os.makedirs('TempUploads')

    # save file locally
    file = request.files['file']
    file.stream.seek(0)
    save_location = f'TempUploads/{file.filename}'
    file.save(save_location)

    document = Document.Document("temp", save_location)
    document.processDocumentOnlyAnnotations()

    annotation_json = document.getAnnotationJson()

    # delete local file
    document.deleteFile()

    log.printSection("Returning")
    print(annotation_json)

    print("---Time Elapsed: %s seconds ---" % (time.time() - start_time))
    return annotation_json


if __name__ == '__main__':
    with open('misc/ascii-art.txt') as f:
        print(f.read())
    print("Initiating Flask app...")
    serve(app, host='0.0.0.0', port=50100, threads=1, url_prefix="/processor")

