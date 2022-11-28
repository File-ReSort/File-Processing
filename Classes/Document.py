from datetime import datetime
import os
import uuid
import time
from Classes import DocumentParser, DocumentReader


class Document:

    def __init__(self, name, documentPath):
        self.id = str(uuid.uuid4())
        self.localDocumentPath = documentPath
        self.name = name
        self.fileName = os.path.basename(documentPath)
        self.uploadDate = str(datetime.now().ctime())
        self.lastEditDate = str(time.ctime(os.path.getmtime(documentPath)))
        self.bucketFileLocation = ''
        self.bucketJsonLocation = ''
        self.documentParser = DocumentParser.DocumentParser((DocumentReader.Read(self.localDocumentPath)))

    def processDocument(self):
        self.documentParser.ProcessDocument()

    def setBucketLocations(self, bucketFileLocation, bucketJsonLocation):
        self.bucketFileLocation = bucketFileLocation
        self.bucketJsonLocation = bucketJsonLocation

    def readDocument(self):
        return DocumentReader.Read(self.localDocumentPath)

    def getNodeManager(self):
        return self.documentParser.getNodeManager()

    def getMetaData(self):
        return {
            'ID': self.id,
            'Name': self.name,
            'FileName': self.fileName,
            'UploadDate': self.uploadDate,
            'LastEditDate': self.lastEditDate,
            'BucketFileLocation': self.bucketFileLocation,
            'BucketJsonLocation': self.bucketJsonLocation
        }

    def getAnnotationJson(self):
        return self.documentParser.getEntCharSpanJson()