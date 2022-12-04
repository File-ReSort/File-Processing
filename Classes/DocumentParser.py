import spacy
import coreferee
from Classes import log, Node
from spacy.matcher import DependencyMatcher

class DocumentParser:
    def __init__(self, text):
        self.docText = text
        self.doc = None
        self.entityCharSpans = None
        self.nodeManager = None

    def ProcessDocument(self):
        nlp = spacy.load('en_core_web_trf')
        # Disable default NER, so we can add a custom, manual NER for now
        nlp.disable_pipes('ner')
        entity_ruler = nlp.add_pipe('entity_ruler')
        nlp.add_pipe('merge_entities')
        nlp.add_pipe('coreferee')

        print(nlp.pipe_names)

        # NER Start
        ent_list = ['LEGAL_ORGANIZATION', 'PERSON', 'CONCEPT']
        entity_ruler_patterns = [
            {"label": ent_list[0], "pattern": "Office of the Comptroller of the Currency"},
            {"label": ent_list[0], "pattern": "Department of the Treasury"},
            {"label": ent_list[0], "pattern": "federal"},
            {"label": ent_list[1], "pattern": "Secretary of the Treasury"},
            {"label": ent_list[1], "pattern": "Comptroller of the Currency"},
            {"label": ent_list[2], "pattern": "commerce"}
        ]
        entity_ruler.add_patterns(entity_ruler_patterns)

        # DependencyMatcher Start (This essentially finds all node edges)
        dep_matcher = DependencyMatcher(nlp.vocab)

        # https://spacy.io/api/dependencymatcher
        # https://spacy.io/api/matcher

        matcher_pattern_names = ["CHARGED", "PERFORM", "ADVISED"]
        matcher_patterns = [
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
            # Perform Pattern
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
            # Advised Pattern
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

        for x in range(len(matcher_pattern_names)):
            dep_matcher.add(matcher_pattern_names[x], [matcher_patterns[x]])

        self.doc = nlp(self.docText)

        matches = dep_matcher(self.doc)

        log.printSection(f'Found {len(matches)} matching dep patterns')
        print(matches)
        for match in matches:
            match_id, token_ids = match
            print('DEP Match', dep_matcher.get(match_id))
            for token in token_ids:
                print(f'TOKEN MATCH:{self.doc[token]}')

        log.printSection(f'Document contains {len(self.doc.ents)} entities')
        # Start finding start char and end char for entities. Will later send to front end to be displayed.
        ent_char_spans = []
        for ent in self.doc.ents:
            print('ent:', ent.label_, ent, ent.start_char, ent.end_char, ent.label_)
            ent_char_spans.append([
                ent.start_char,
                ent.end_char,
                ent.label_
            ])

        log.printSection(f'Document contains {len(self.doc)} tokens')
        for token in self.doc:
            token_text = token.text.replace('\n', '\\n').replace('\t', '\\t')
            print('token:', token.i, token_text)

        log.printSection(f'Coreferee chains')
        self.doc._.coref_chains.print()

        # [parentDocIndex: [childDocIndex,childDocIndex,...]]
        chain_dict = {}

        for chain in self.doc._.coref_chains:
            mentionIndexList = []
            for mention in chain:
                mentionIndexList.append(mention.token_indexes[0])
            chain_dict[chain.index] = mentionIndexList

        # [childDocIndex: parentDocIndex]
        mention_dict = {}

        nm = Node.NodeManager()

        for key in chain_dict.keys():
            parent_index = chain_dict[key][0]

            for x in range(1, len(chain_dict[key])):
                mention_dict[chain_dict[key][x]] = parent_index

        del chain_dict

        # mention dict is in format of [childDocIndex: parentDocIndex]. This will help to reduce duplicate nodes in our graph
        # when we actually start creating nodes.
        print(mention_dict)
        mention_dict_keys = sorted(mention_dict)
        print(f'Child Keys:{mention_dict_keys}')

        log.printSection(f'Entity parent-child relations')
        # Check all doc entities
        for e in self.doc.ents:
            print(e)
            print(f'Entity:', e.text, e.label_, e.start, e.end)

            for x in range(e.start, e.end):
                # If current token is a child of a token
                if(x in mention_dict.keys()):
                    print('\tHas parent token:', self.doc[x], mention_dict[x])
                # else create a new node
                else:
                    # THIS ASSUMES THAT NER IS 100% accurate
                    tempNode = Node.Node(e, e.start, e.end, e.label_)
                    nm.add(tempNode)

        log.printSection(f'Created Nodes')
        for node in nm.getGraph():
            print('NODE:', node.id, node.text, node.nodeEdgeOrigins, node.EntityID)

        log.printSection(f'Created Edges')
        print(matches)

        for match in matches:
            pattern_match_name = nlp.vocab.strings[match[0]]
            tokenIDs = match[1]

            print(f'Match: {match}, Pattern: {pattern_match_name}')

            #Check to see if any tokens are a child of a parent entity.
            for tokenID in tokenIDs:
                print(f'{self.doc[tokenID]} ID: {tokenID}')
                if tokenID in mention_dict_keys:
                    print(f'\tis child of \"{self.doc[mention_dict[tokenID]]}\", Parent ID:{mention_dict[tokenID]}')

            if pattern_match_name == 'ADVISED':
                edge_text = self.doc[tokenIDs[0]]
                node1_token_id = mention_dict[tokenIDs[1]]
                node2_token_id = mention_dict[tokenIDs[2]]

                print(f'ET: {edge_text}, N1TID: {node1_token_id}, N2TID: {node2_token_id}')

                temp_edge = Node.NodeEdge(edge_text, node2_token_id)

                nm.addEdge(node1_token_id, temp_edge)

        log.printSection('PROCESSED NODE LIST')
        for node in nm.getGraph():
            print(node)

        nm.nodeListToDict()

        self.entityCharSpans = ent_char_spans
        self.nodeManager = nm

    def processForAnnotations(self):
        nlp = spacy.load('en_core_web_trf')
        # Disable default NER, so we can add a custom, manual NER for now
        nlp.disable_pipes('ner')
        entity_ruler = nlp.add_pipe('entity_ruler')
        nlp.add_pipe('merge_entities')

        # NER Start
        ent_list = ['LEGAL_ORGANIZATION', 'PERSON', 'CONCEPT']
        entity_ruler_patterns = [
            {"label": ent_list[0], "pattern": "Office of the Comptroller of the Currency"},
            {"label": ent_list[0], "pattern": "Department of the Treasury"},
            {"label": ent_list[0], "pattern": "federal"},
            {"label": ent_list[1], "pattern": "Secretary of the Treasury"},
            {"label": ent_list[1], "pattern": "Comptroller of the Currency"},
            {"label": ent_list[2], "pattern": "commerce"}
        ]
        entity_ruler.add_patterns(entity_ruler_patterns)

        self.doc = nlp(self.docText)

        log.printSection(f'Document contains {len(self.doc.ents)} entities')
        # Start finding start char and end char for entities. Will later send to front end to be displayed.
        ent_char_spans = []
        for ent in self.doc.ents:
            print('ent:', ent.label_, ent, ent.start_char, ent.end_char, ent.label_)
            ent_char_spans.append([
                ent.start_char,
                ent.end_char,
                ent.label_
            ])

        self.entityCharSpans = ent_char_spans

    def getEntCharSpanJson(self):
        char_span_json = {
            "annotations": [
                [
                    self.doc.__repr__(),
                    {
                        "entities": self.entityCharSpans
                    }
                ]
            ]
        }

        return char_span_json

    def getNodeManager(self):
        return self.nodeManager
