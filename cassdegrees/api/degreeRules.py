class degreeRules:
    JSONString = []

    def getRule(self, ruleType, match):
        rule = {"type": ruleType, "match": match}

        return rule

    """ 
        ["(", A, "OR", "B", ")", "AND", "(", "C", "OR", "D", ")"]
    """
    def buildExpression(self, expressionList):
        tree = {}
        stack = []
        node = tree
        for token in expressionList:
            if token == "(":
                node['left'] = {}
                stack.append(node)
                node = node['left']
            elif token == ")":
                if len(stack) > 0:
                    node = stack.pop()
                else:
                    print("h")
                    parent = {}
                    parent["left"] = node
                    node = parent
                    tree = parent
            elif token in ["AND", "OR"]:
                node['val'] = token
                node['right'] = {}
                stack.append(node)
                node = node['right']
            else:
                node['rule'] = token
                print(stack)
                parent = stack.pop()
                print(stack)
                node = parent
        return tree
        #create rules, return rules. Then take a list of rules in a bool alg expression and build the json

    # Add rule as another AND?



degreeRule = degreeRules()
A = degreeRule.getRule("single course", "COMP1***")
test = ["(", A, "OR", "B", ")", "AND", "(", "C", "OR", "D", ")"]
t = degreeRule.buildExpression(test)
print(t)
