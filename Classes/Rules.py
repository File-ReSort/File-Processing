import requests

class RuleManager:
    def __init__(self, api_url):
        self.ruleDict = self.pull_rules(api_url)

    def get_rules(self):
        return self.ruleDict

    def pull_rules(self, api_url):
        dict = {}
        result = requests.get(url=api_url).json()

        for rule in result:
            temp_rule = Rule(rule["Rule"], rule["ruleID"], rule["Relationship"], rule["Word"])

            # if key already exists, then append to existing key
            if dict.get(temp_rule.word) is not None:
                print(f"On Rule {temp_rule.word}, Appending", temp_rule)
                rule_list = dict.get(temp_rule.word)
                rule_list.append(temp_rule)
                dict[temp_rule.word] = rule_list
            # else create a new key
            elif dict.get(temp_rule.word) is None:
                print(f"Creating New Rule {temp_rule.word}")
                dict[temp_rule.word] = [temp_rule]

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