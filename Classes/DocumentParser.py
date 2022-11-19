import spacy, coreferee
from Classes import log, Node
from spacy.matcher import DependencyMatcher


def ProcessDocumentText(DocText):

    nlp = spacy.load('en_core_web_trf')
    # Disable default NER so we can add custom, manual NER for now
    nlp.disable_pipes('ner')
    entityRuler = nlp.add_pipe('entity_ruler')
    nlp.add_pipe('merge_entities')
    nlp.add_pipe('coreferee')

    print(nlp.pipe_names)

    # NER Start
    entList = ['LEGAL ORGANIZATION', 'PERSON']
    entityRulerPatterns = [
        {"label": entList[0], "pattern": "Office of the Comptroller of the Currency"},
        {"label": entList[0], "pattern": "Department of the Treasury"},
        {"label": entList[1], "pattern": "Secretary of the Treasury"},
        {"label": entList[1], "pattern": "Comptroller of the Currency"},
    ]
    entityRuler.add_patterns(entityRulerPatterns)


    # DependencyMatcher Start (This essentially finds all node edges)
    depMatcher = DependencyMatcher(nlp.vocab)

    # https://spacy.io/api/dependencymatcher
    # https://spacy.io/api/matcher

    matcherPatternNames = ["CHARGED", "PERFORM", "ADVISED"]
    matcherPatterns = [
        # Charged Pattern
        [
            {
                'RIGHT_ID': 'anchor_charged',
                'RIGHT_ATTRS': {'ORTH': 'charged'}
            },
            {
                'LEFT_ID': 'anchor_charged',
                'REL_OP': '<',
                "RIGHT_ID": 'charged_subject',
                'RIGHT_ATTRS': {'POS': 'NOUN'}
            },
            {
                'LEFT_ID': 'anchor_charged',
                'REL_OP': '>>',
                "RIGHT_ID": 'charged_verb',
                'RIGHT_ATTRS': {'DEP': 'pcomp', 'POS': 'VERB'}
            },
            {
                'LEFT_ID': 'charged_verb',
                'REL_OP': '>>',
                "RIGHT_ID": 'charged_verb_dobj',
                'RIGHT_ATTRS': {'DEP': 'dobj'}
            }
        ],
        #Perform Pattern
        [
            {
                'RIGHT_ID': 'anchor_perform',
                'RIGHT_ATTRS': {'ORTH': 'perform'}
            },
            {
                'LEFT_ID': 'anchor_perform',
                'REL_OP': '>',
                "RIGHT_ID": 'perform_subject',
                'RIGHT_ATTRS': {'DEP': 'nsubj'}
            },
            {
                'LEFT_ID': 'anchor_perform',
                'REL_OP': '>',
                "RIGHT_ID": 'perform_what',
                'RIGHT_ATTRS': {'DEP': 'dobj'}
            },
            {
                'LEFT_ID': 'perform_what',
                'REL_OP': '>>',
                "RIGHT_ID": 'duties_dobj',
                'RIGHT_ATTRS': {'DEP': 'pobj'}
            }
        ],
        [
            {
                'RIGHT_ID': 'anchor_advised',
                'RIGHT_ATTRS': {'ORTH': 'advised'}
            },
            {
                'LEFT_ID': 'anchor_advised',
                'REL_OP': '>',
                "RIGHT_ID": 'advised_propn',
                'RIGHT_ATTRS': {'DEP': 'nsubjpass'}
            },
            {
                'LEFT_ID': 'anchor_advised',
                'REL_OP': '>>',
                "RIGHT_ID": 'advised_who',
                'RIGHT_ATTRS': {'DEP': 'pobj'}
            }
        ]
    ]

    for x in range(len(matcherPatternNames)):
        asdf = depMatcher.add(matcherPatternNames[x], [matcherPatterns[x]])
        print(asdf)

    doc = nlp(DocText)

    matches = depMatcher(doc)

    log.printSection(f'Found {len(matches)} matching dep patterns')
    print(matches)
    for match in matches:
        match_id, token_ids = match
        print('DEP Match', depMatcher.get(match_id))
        for token in token_ids:
            print(f'TOKEN MATCH:{doc[token]}')

    log.printSection(f'Document contains {len(doc.ents)} entities')
    for ent in doc.ents:
        print('ent:', ent.label_, ent)

    log.printSection(f'Document contains {len(doc)} tokens')
    for token in doc:
        tokenText = token.text.replace('\n','\\n').replace('\t','\\t')
        print('token:', token.i, tokenText)

    log.printSection(f'Coreferee chains')
    doc._.coref_chains.print()

    # [parentDocIndex: [childDocIndex,childDocIndex,...]]
    chainDict = {}

    for chain in doc._.coref_chains:
        mentionIndexList = []
        for mention in chain:
            mentionIndexList.append(mention.token_indexes[0])
        chainDict[chain.index] = mentionIndexList

    # [childDocIndex: parentDocIndex]
    mentionDict = {}
    nodes = []

    nm = Node.NodeManager()


    for key in chainDict.keys():
        parentIndex = chainDict[key][0]
        # nodes.append(doc[parentIndex])

        for x in range(1, len(chainDict[key])):
            mentionDict[chainDict[key][x]] = parentIndex

    del chainDict

    # mention dict is in format of [childDocIndex: parentDocIndex]. This will help to reduce duplicate nodes in our graph
    # when we actually start creating nodes.
    print(mentionDict)
    mentionDictKeys = sorted(mentionDict)
    print(f'Child Keys:{mentionDictKeys}')

    log.printSection(f'Entity parent-child relations')
    # Check all doc entities
    for e in doc.ents:
        print(f'Entity:', e.text, e.label_, e.start, e.end)

        for x in range(e.start, e.end):
            # If current token is a child of a token
            if(x in mentionDict.keys()):
                print('\tHas parent token:', doc[x], mentionDict[x])
            # else create a new node
            else:
                # THIS ASSUMES THAT NER IS 100% accurate
                tempNode = Node.Node(e)
                nm.add(tempNode)

    log.printSection(f'Created Nodes')
    for node in nm.getGraph():
        print('NODE:', node.id, node.text, node.nodeEdgeOrigins, node.entityID)

    log.printSection(f'Created Edges')
    print(matches)

    for match in matches:
        patternMatchName = nlp.vocab.strings[match[0]]
        tokenIDs = match[1]

        print(f'Match: {match}, Pattern: {patternMatchName}')

        #Check to see if any tokens are a child of a parent entity.
        for tokenID in tokenIDs:
            print(f'{doc[tokenID]} ID: {tokenID}')
            if tokenID in mentionDictKeys:
                print(f'\tis child of \"{doc[mentionDict[tokenID]]}\", Parent ID:{mentionDict[tokenID]}')

        if patternMatchName == 'ADVISED':
            edgeText = doc[tokenIDs[0]]
            node1TokenID = mentionDict[tokenIDs[1]]
            node2TokenID = mentionDict[tokenIDs[2]]

            print(f'ET: {edgeText}, N1TID: {node1TokenID}, N2TID: {node2TokenID}')

            tempEdge = Node.NodeEdge(edgeText, node2TokenID)

            nm.addEdge(node1TokenID, tempEdge)

    log.printSection('PROCESSED NODE LIST')
    for node in nm.getGraph():
        print(node)

    return nm

# Displacy styles ['ent', 'dep', 'span']

# f = open('displacyOutput.html', 'w')
# f.write(displacy.render(doc, style='ent'))
# f.close()
#
# displacy.serve(doc, style='ent')