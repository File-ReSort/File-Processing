import PyPDF2

def Read(fileLocation):
    #Parse fileLocation to determine extension
    extension = fileLocation.split('.')[-1]

    docText = ""
    match extension:

        case 'txt':
            with open(fileLocation) as f:
                docText = f.read()
            return docText

        case 'pdf':
            pdfFileObj = open(fileLocation, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

            for x in range(pdfReader.numPages):
                docText += pdfReader.getPage(x).extractText()

            pdfFileObj.close()
            return docText

    return None