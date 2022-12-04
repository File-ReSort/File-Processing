from datetime import datetime
import os
import uuid
import time
from Classes import DocumentParser, DocumentReader


class Document:

    def __init__(self, name, document_path):
        self.id = str(uuid.uuid4())
        self.localDocumentPath = document_path
        self.name = name
        self.fileName = os.path.basename(document_path)
        self.uploadDate = str(datetime.now().ctime())
        self.lastEditDate = str(time.ctime(os.path.getmtime(document_path)))
        self.bucketFileLocation = ''
        self.documentParser = DocumentParser.DocumentParser((DocumentReader.Read(self.localDocumentPath)))

    def processDocument(self):
        self.documentParser.ProcessDocument()

    def processDocumentOnlyAnnotations(self):
        self.documentParser.processForAnnotations()

    def setBucketFileLocation(self, bucket_file_location):
        self.bucketFileLocation = bucket_file_location

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
            'BucketFileLocation': self.bucketFileLocation
        }

    def getAnnotationJson(self):
        return self.documentParser.getEntCharSpanJson()

    def deleteFile(self):
        os.remove(self.localDocumentPath)
