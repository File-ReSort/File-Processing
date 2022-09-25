import spacy
import DocumentReader
from spacy import displacy


nlp = spacy.load("en_core_web_sm");

#DocumentText = PDFReader.Read('ExampleData/USCODE-2020-title1.pdf')
DocText = DocumentReader.Read('ExampleData/story.txt')

doc = nlp(DocText)

# for token in doc:
#     print(token)

# for sent in doc.sents:
#     print(sent)

sentences = list(doc.sents)

for sentence in sentences:
    for token in sentence:
        print(token.text + ": " + token.ent_type_, token.pos_, token.dep_)

    print("\n")

print("http://localhost:5000")
displacy.serve(sentences[0], style="dep")
