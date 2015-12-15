from math import *
class Node:
    def __init__(self, examples):
        self.attribute = ''
        self.examples = examples
        self.positive = 0
        self.negative = 0
        self.label = 100
        self.child = {}
        for example in Examples:
            if example['Decide'] == 'Yes':
                self.positive += 1
            else:
                self.negative += 1

def Entropy(Examples):
    if len(Examples) == 0:
        return 0
    positive = 0.0
    negative = 0.0
    for example in Examples:
        if example['Decide'] == 'Yes':
            positive += 1
        else:
            negative += 1
    p_Positive = float(positive / len(Examples))
    p_Negative = float(negative / len(Examples))
    if p_Positive == 0 or p_Negative == 0:
        return 0
    entropy = -1 * (p_Positive * log(p_Positive, 2) + p_Negative * log(p_Negative, 2))
    return entropy

def Gain(Examples, attribute):
    # values is a list of values. Like ['Weak', 'Strong'] of Wind
    values = wordValue[attribute]
    valueCount = {}
    # values is a dictionary. Like {'Weak' : 8, 'Strong' : 6}
    for i in range(len(values)):
        valueCount[values[i]] = 0
    for example in Examples:
        valueCount[example[attribute]] += 1
    gain = Entropy(Examples)
    for i in range(len(values)):
        valueExamples = []
        for example in Examples:
            if example[attribute] == values[i]:
                valueExamples.append(example)
        gain -= (valueCount[values[i]] * Entropy(valueExamples))/ len(Examples)
    return gain

def getExamples():
    examples = open('Examples.txt')
    Examples = []
    for example in examples:
        example = example[:-1]
        eList = example.split(' ')
        eDic = {}
        for i in range(len(eList)):
            eDic[keyWord[i]] = eList[i]
        Examples.append(eDic)
    return Examples

def ID3(Examples, Attributes):
    positive = 0
    for example in Examples:
        if example[Target_attribute] == 'Yes':
            positive += 1
    if positive == len(Examples) or positive == 0:
        root = Node([])
        if positive == 0:
            root.label = 0
        else:
            root.label = 1
        return root
    if len(Attributes) == 0:
        negative = len(Examples) - positive
        root = Node([])
        if positive > negative:
            root.label = 1
        else:
            root.label = 0
        return root
    root = Node(Examples)
    maxGain = 0
    maxGainAttribute = ''
    for attribute in Attributes:
        gain = Gain(Examples, attribute)
        if gain > maxGain:
            maxGain = gain
            maxGainAttribute = attribute
    root.attribute = maxGainAttribute
    for value in wordValue[root.attribute]:
        examplesOfValue = []
        for example in Examples:
            if example[root.attribute] == value:
                examplesOfValue.append(example)
        if len(examplesOfValue) == 0:
            valueNode = Node(examplesOfValue)
            if root.positive > root.negative:
                valueNode.label = 1
            else:
                valueNode.label = 0
            root.child[value] = valueNode
        else:
            newAttributes = Attributes[:]
            newAttributes.remove(root.attribute)
            root.child[value] = ID3(examplesOfValue, newAttributes)
    return root

def judge(root, condition):
    if root.label != 100:
        return root.label
    nextRoot = root.child[condition[root.attribute]]
    return judge(nextRoot, condition)

keyWord = ['Outlook', 'Temperature', 'Humidity', 'Wind', 'Decide']
wordValue = {'Outlook':['Sunny', 'Rain', 'Overcast'],
        'Temperature':['Hot', 'Mild', 'Cool'],
        'Humidity':['High', 'Normal'],
        'Wind':['Weak', 'Strong']}

global Target_attribute
Target_attribute = 'Decide'
Examples = getExamples()
Attributes = keyWord[:]
Attributes.remove(Target_attribute)
root = ID3(Examples, Attributes)
while True:
    condition = {}
    for attribute in Attributes:
        condition[attribute] = raw_input(attribute + ' : ')
    if judge(root, condition):
        print 'Yes!'
    else:
        print 'No!'
    print ''
