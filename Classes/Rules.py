import requests

class RuleManager:
    def __init__(self, api_url):
        self.ruleList = self.getRules(api_url)

    def addRule(self, rule):
        self.ruleList.append(rule)

    def removeRule(self, rule):
        self.ruleList.remove(rule)

    def getRules(self, api_url):
        list = []
        result = requests.get(url=api_url).json()

        for rule in result:
            list.append(Rule(rule["Rule"], rule["ruleID"], rule["Relationship"], rule["Word"]))

        return list

class Rule:
    def __init__(self, rule, ruleID, relationship, word):
        self.rule = rule
        self.ruleID = ruleID
        self.relationship = relationship
        self.word = word

    def __repr__(self):
        return "{"f"Rule: {self.rule}, RuleID: {self.ruleID}, Relationship: {self.relationship}, Word: {self.word}""}"