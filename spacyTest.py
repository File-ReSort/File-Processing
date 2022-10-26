import spacy
import coreferee
import DocumentReader
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
nlp.add_pipe('coreferee')
# stopWords = nlp.Defaults.stop_words

#DocText = DocumentReader.Read('ExampleData/USCODE-2020-title1.pdf')
DocText = DocumentReader.Read('ExampleData/story.txt')
#DocText = DocumentReader.Read('ExampleData/example.txt')
#DocText = DocumentReader.Read('ExampleData/test.txt')

doc = nlp(DocText)
doc._.coref_chains.print()
print(doc._.coref_chains.resolve(doc[27]))

for chain in doc._.coref_chains:
    print(chain)
    #print(doc._.coref_chains.resolve(chain))

sentences = list(doc.sents)

print("Starting Text\nToken Count: " + str(len(doc)) + "\n\t" + DocText + "\n")

# noStopWords = ''
# for token in doc:
#     if token.is_stop == False and token.text not in ['"', ',', '.', '!', '?']:
#         noStopWords += ' ' + token.text
#     elif token.is_stop == False:
#         noStopWords += token.text
# doc = nlp(noStopWords)
# print("Text with no stop words\nToken Count: " + str(len(doc)) + "\n\t" + noStopWords + "\n")
#
# noStopWordsAndLemmatization = ''
# for token in doc:
#     noStopWordsAndLemmatization += token.lemma_ + ' '
# doc = nlp(noStopWordsAndLemmatization)
# print("Text with no stop words + lemmatization\nToken Count: " + str(len(doc)) + "\n\t" + noStopWordsAndLemmatization + "\n")

# for sentence in sentences:
#     for token in sentence:
#         print(token.text + ": " + token.ent_type_, token.pos_, token.dep_)
#     print("\n")

#Display styles ['ent', 'dep', 'span']
p = displacy.render(doc, style='ent')
displacy.serve(doc, style='ent')
print(p)

