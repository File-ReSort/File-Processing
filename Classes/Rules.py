import requests

class RuleManager:
    def __init__(self, api_url):
        self.ruleDict = self.pullRules(api_url)

    def addRule(self, rule):
        self.ruleList.append(rule)

    def removeRule(self, rule):
        self.ruleList.remove(rule)

    def getRules(self):
        return self.ruleDict

    def pullRules(self, api_url):
        dict = {}
        result = requests.get(url=api_url).json()

        for rule in result:
            tempRule = Rule(rule["Rule"], rule["ruleID"], rule["Relationship"], rule["Word"])

            # if key already exists, then append to existing key
            if dict.get(tempRule.word) is not None:
                print(f"On Rule {tempRule.word}, Appending", tempRule)
                ruleList = dict.get(tempRule.word)
                ruleList.append(tempRule)
                dict[tempRule.word] = ruleList
            # else create a new key
            elif dict.get(tempRule.word) is None:
                print(f"Creating New Rule {tempRule.word}")
                dict[tempRule.word] = [tempRule]

        print("PULLED RULES", dict)
        return dict

class Rule:
    def __init__(self, rule, ruleID, relationship, word):
        self.rule = rule
        self.ruleID = ruleID
        self.relationship = relationship
        self.word = word

    def __repr__(self):
        return "{"f"Rule: {self.rule}, RuleID: {self.ruleID}, Relationship: {self.relationship}, Word: {self.word}""}"