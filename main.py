# to start web server use: flask --app main run

from flask import Flask, request
from Classes import Document
import requests

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Flask is up and running'


# This route assumes that this is a new uploaded document and has never been processed before
@app.route('/ProcessDocument', methods=['POST'])
def process_document():
    args = request.args
    print(args)
    document_location = args.get('location')
    document_name = args.get('name')

    document = Document.Document(document_name, document_location)
    document.processDocument()

    nodeJson = document.getNodeManager().serialize()


    # Send nodeManager.getGraph() information to Neo4j Here
@app.route('/graphToNeo4j', methods=['GET'])
def graph_to_neo4j():
    authenticate("bolt://localhost:7687", "neo4j", "neo4j")
    neo4jUrl = os.environ.get('NEO4J_URL', "bolt://localhost:7687/db/data/")
    graph = Graph(neo4jUrl, secure=False)
    graph.run("CREATE CONSTRAINT ON (q:Question) ASSERT q.id IS UNIQUE;")
    apiUrl = "/TrainingData/annotations.json"
    json = requests.get(apiUrl, headers={"accept": "application/json"}).json()

    # Send document metaData using /setDocumentMeta API
    url = ''
    metaData = document.getMetaData()
    # requests.put(url, metaData, headers={'content-type': 'text/plain'})

    return nodeJson

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