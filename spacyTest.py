import spacy
import coreferee
import DocumentReader
from spacy import displacy
from spacy.matcher import DependencyMatcher

nlp = spacy.load('en_core_web_trf')
nlp.add_pipe('coreferee')

#DocText = DocumentReader.Read('ExampleData/USCODE-2020-title1.pdf')
#DocText = DocumentReader.Read('ExampleData/story.txt')
DocText = DocumentReader.Read('ExampleData/example.txt')
#DocText = DocumentReader.Read('ExampleData/test.txt')

doc = nlp(DocText)

#Rule based matching, Matcher and DependencyMatcher
# matcher = DependencyMatcher(nlp.vocab)
#
# patterns = [
#    [{"POS": "PROPN"}, {"POS": "VERB"}, {"POS": "PROPN"}],
#    [{"POS": "NOUN"}, {"POS": "VERB"}, {"POS": "NOUN"}]
# ]
#
# matcher.add("uniqueID", patterns, on_match=newFunc)
#
# matches = matcher(doc)
#
# print("Matches:", [doc[start:end].text for match_id, start, end in matches])

doc._.coref_chains.print()

chainDict = {}

for chain in doc._.coref_chains:
    mentionIndexList = []
    for mention in chain:
        mentionIndexList.append(mention.token_indexes[0])
    chainDict[chain.index] = mentionIndexList

mentionDict = {}

for key in chainDict.keys():
    parentIndex = chainDict[key][0]
    for x in range(1, len(chainDict[key])):
        mentionDict[chainDict[key][x]] = parentIndex

del chainDict

print(mentionDict)

#Display styles ['ent', 'dep', 'span']
#p = displacy.render(doc, style='ent')
displacy.serve(doc, style='dep')


