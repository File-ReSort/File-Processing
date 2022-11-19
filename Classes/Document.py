from datetime import datetime
import os
import uuid
from Classes import DocumentParser, DocumentReader


class Document:

    def __init__(self, documentPath):
        self.id = str(uuid.uuid4())
        self.localDocumentPath = documentPath
        self.FileName = os.path.basename(documentPath)
        self.uploadDate = str(datetime.now())
        self.lastEditDate = str(os.path.getmtime(documentPath))
        self.bucketFileLocation = ''
        self.bucketJsonLocation = ''

    def setBucketLocations(self, bucketFileLocation, bucketJsonLocation):
        self.bucketFileLocation = bucketFileLocation
        self.bucketJsonLocation = bucketJsonLocation

    def readDocument(self):
        return DocumentReader.Read(self.localDocumentPath)

    def getNodeManager(self):
        return DocumentParser.ProcessDocumentText(DocumentReader.Read(self.localDocumentPath))