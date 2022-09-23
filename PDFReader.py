import PyPDF2

def Read(fileLocation):
    pdfFileObj = open(fileLocation, 'rb')

    # creating a pdf reader object
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj)

    PDFText = ""
    for x in range(pdfReader.numPages):
        PDFText += pdfReader.getPage(x).extractText()

    pdfFileObj.close()
    return PDFText;