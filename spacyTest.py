import spacy
import DocumentReader
from spacy import displacy

nlp = spacy.load("en_core_web_sm")
stopWords = nlp.Defaults.stop_words

#DocText = DocumentReader.Read('ExampleData/USCODE-2020-title1.pdf')
#DocText = DocumentReader.Read('ExampleData/story.txt')
DocText = DocumentReader.Read('ExampleData/example.txt')



doc = nlp(DocText)
#sentences = list(doc.sents)

print("Starting Text\nToken Count: " + str(len(doc)) + "\n\t" + DocText + "\n")

noStopWords = ''
for token in doc:
    if token.is_stop == False:
        noStopWords += token.text + ' '
doc = nlp(noStopWords)
print("Text with no stop words\nToken Count: " + str(len(doc)) + "\n\t" + noStopWords + "\n")

noStopWordsAndLemmatization = ''
for token in doc:
    noStopWordsAndLemmatization += token.lemma_ + ' '
doc = nlp(noStopWordsAndLemmatization)
print("Text with no stop words + lemmatization\nToken Count: " + str(len(doc)) + "\n\t" + noStopWordsAndLemmatization + "\n")

# for sentence in sentences:
#     for token in sentence:
#         print(token.text + ": " + token.ent_type_, token.pos_, token.dep_)
#     print("\n")

print("http://localhost:5000")
#Display styles ['ent', 'dep', 'span']
displacy.serve(doc, style='dep')
