import numpy as np
import time
import random
import multiprocessing
from multiprocessing import Queue

class CART(object):
    def __init__(self, treeNode = None, maxDepth = 10):
        self.tree = treeNode
        self.maxDepth = maxDepth

    def fit(self, data, depth = 0):
        treeNode = {}
        if depth > self.maxDepth:
            treeNode["type"] = "leaf"
            treeNode["label"] = self.getLabel(data)
            return treeNode
        feature, value = self.chooseFeature(data)
        if not feature:
            # can't split anymore
            treeNode["type"] = "leaf"
            treeNode["label"] = self.getLabel(data)
            return treeNode
        leftData, rightData = self.splitData(data, feature, value)
        treeNode["type"] = "node"
        treeNode["feature"] = feature
        treeNode["splitValue"] = value
        treeNode["leftTree"] = self.fit(data = leftData, depth = depth + 1)
        treeNode["rightTree"] = self.fit(data = rightData, depth = depth + 1)
        if depth == 0:
            self.tree = treeNode
        return treeNode

    def predict(self, data, treeNode = None, isRoot = True):
        if isRoot:
            treeNode = self.tree
        if treeNode["type"] == "leaf":
            return treeNode["label"]
        if data[treeNode["feature"]] < treeNode["splitValue"]:
            return self.predict(data, treeNode["leftTree"], False)
        else:
            return self.predict(data, treeNode["rightTree"], False)

    # get the count of each label, return as a dictionary
    def getCountDic(self, data):
        labels = data[:, -1]
        countDic = {}
        for label in labels:
            try:
                countDic[label] += 1
            except:
                countDic[label] = 1
        return countDic

    # for classify problem
    def getLabel(self, data):
        labels = data[:, -1]
        # get the dictionary as {value : occured time}
        countDic = self.getCountDic(data)
        maxLabel = None
        maxCount = 0
        # find the label which 
        for label in countDic:
            if countDic[label] > maxCount:
                maxLabel = label
                maxCount = countDic[label]
        return maxLabel

    # the bigger GINI means messer data
    def getGINI(self, data):
        m, n = data.shape
        countDic = self.getCountDic(data)
        GINI = 1
        for key in countDic:
            GINI -= (float(countDic[key]) / m) ** 2
        return GINI

    # the smaller GINI_Gain is better
    def getGINIGain(self, data, feature, value):
        m, n = data.shape
        left, right = self.splitData(data, feature, value)
        if len(left.shape) == 1:
            return self.getGINI(right)
        if len(right.shape) == 1:
            return self.getGINI(left)
        ml, nl = left.shape
        mr, nr = right.shape
        GINI_Gain = (float(ml) * self.getGINI(left) + float(mr) * self.getGINI(right)) / m
        return GINI_Gain

    # split the dataset according the value of feature
    def splitData(self, data, feature, value):
        left, right = [], []
        m, n = data.shape
        for i in range(m):
            if data[i][feature] < value:
                left.append(data[i])
            else:
                right.append(data[i])
        # return numpy.array
        return np.array(left), np.array(right)

    def chooseFeature(self, data):
        # well, all the data refer to the same label
        if len(set(data[:, -1])) == 1:
            return None, data[0][-1]
        m, n = data.shape
        if m < 20:
            return None, self.getLabel(data)
        bestFeature = None
        bestValue = None
        minGain = float("inf")
        for feature in range(n - 1):
            values = list(set(data[:, feature]))
            values = sorted(values)
            if len(values) > 30:
                values = values[::len(values) / 30]
            for index in range(1, len(values)):
                value = (values[index] + values[index - 1]) / 2
                GINI_Gain = self.getGINIGain(data, feature, value)
                if GINI_Gain < minGain:
                    bestFeature, bestValue, minGain = feature, value, GINI_Gain
        if not bestFeature:
            return None, self.getLabel(data)
        left, right = self.splitData(data, bestFeature, bestValue)
        try:
            ml, nl = left.shape
            mr, nr = right.shape
        except:
            return None, self.getLabel(data)
        if ml > mr:
            ml, mr = mr, ml
        # whethe is a good split
        '''
        if float(ml) / mr < 0.1:
            return None, getLabel(data)
        '''
        return bestFeature, bestValue

class forest(object):
    def __init__(self, treeSize = 26, treeNum = 30, maxDepth = 10):
        print treeSize
        print treeNum
        print maxDepth
        self.treeSize = treeSize
        self.treeNum = treeNum
        self.maxDepth = maxDepth
        self.forest = [None] * self.treeNum
    
    # create a forest with the training data and label
    def fit(self, data, label):
        # randomly split the data by treeSize and treeNum
        # relation marks the feature index
        split_data, relation = self.splitTrainData(data, label)
        process = []
        pos = 0
        q = Queue(self.treeNum + 1)
        for data in split_data:
            # multiprocessing, write the result into tree file
            p = multiprocessing.Process(target = self.multipletrain, args = (data, relation[pos], q))
            p.start()
            process.append(p)
            pos += 1
        print "training..."
        # wait until training over
        for p in process:
            p.join()
        print q.qsize()
        for i in range(self.treeNum):
            self.forest[i] = q.get()
        # load the tree file, create a forest
        # self.loadForestFromTree(self.treeNum)

    # load the tree file, create a forest
    def loadForestFromTree(self, treeNum):
        relation = []
        for i in range(self.treeNum):
            f = open("tree" + str(i) + ".txt", "r")
            tree = eval(f.readline().strip())
            relation.append(eval(f.readline().strip()))
            f.close()
            self.forest.append(tree)
        for i in range(self.treeNum):
            self.forest[i] = self.relativeTree(self.forest[i], relation[i])

    # predict the output of data using the forest
    def predict(self, data):
        output = []
        length = len(self.forest)
        print "in predict"
        print self.forest
        m, n = data.shape
        # predict all input
        for i in range(m):
            # each input was split to several data
            tree_outputs = {}
            for j in range(length):
                # the jth piece, ith row of data
                tree = CART(self.forest[j])
                label = tree.predict(data[i])
                if label not in tree_outputs:
                    tree_outputs[label] = 1
                else:
                    tree_outputs[label] += 1
            maxLabel = None
            maxCount = 0
            for key in tree_outputs:
                if tree_outputs[key] > maxCount:
                    maxLabel, maxCount = key, tree_outputs[key]
            output.append(maxLabel)
        return output

    # get the real tree(with real feature index)
    def relativeTree(self, tree, relation):
        if "feature" in tree:
            tree["feature"] = relation[tree["feature"]]
            self.relativeTree(tree["leftTree"], relation)
            self.relativeTree(tree["rightTree"], relation)
        return tree

    # create random numbers for selecting feature
    def randomNumber(self, n, domain):
        l = []
        for i in range(n):
            l.append(int(random.random() * domain - 1))
        while len(set(l)) < n:
            l.append(int(random.random() * domain - 1))
        return list(set(l))

    # for multipleprocessing, solve the recurse program
    def multipletrain(self, data, relation, q):
        tree = CART(self.maxDepth)
        treeNode = tree.fit(data = data)
        reTree = self.relativeTree(treeNode, relation)
        q.put(reTree)
        '''
        f = open("tree" + str(pos) + ".txt", "w")
        f.write(str(treeDic))
        f.write("\n")
        f.write(str(relation))
        f.close()
        '''

    # load forest from forest file
    def loadForest(self, fileName):
        self.forest = []
        f = open(fileName, "r")
        for line in f:
            tree = eval(line.strip())
            self.forest.append(tree)
        return forest

    # save forest as file
    def saveForest(self):
        f = open("forest.txt", "w")
        for tree in self.forest:
            f.write(str(tree))
            f.write("\n")
        f.close()

    # split training data to several random piece
    def splitTrainData(self, data, label):
        m, n = data.shape
        split_data = []
        relation = []
        for i in range(self.treeNum):
            # get random numbers
            r = self.randomNumber(self.treeSize, n)
            relation.append(r)
            tupleData = []
            for s in r:
                tupleData.append(data[:,s].reshape((m, 1)))
            tupleData.append(label)
            split_data.append(np.hstack(tuple(tupleData)))
        copy = split_data
        split_data = []
        # select samples
        print "begin select sample"
        for data in copy:
            select = []
            m, n = data.shape
            for i in range(m):
                if random.random() < 0.9:
                    select.append(data[i])
            split_data.append(np.array(select))
        print "end select sample"
        return split_data, relation

def getData(filename):
    f = open(filename, "r")
    data = []
    for line in f:
        data.append(line.strip().split("\t")[1:])
    data = np.array(data[1:], dtype=float)
    return data

if __name__ == "__main__":
    t1 = time.time()
    # get the training data
    raw_data = getData("train.txt")
    label = raw_data[:, -1]
    label = label.reshape((len(label), 1))
    data = raw_data[:, :-1]
    # split the training data, crossing validation
    td, tl = data[5600:], label[5600:]
    data, label = data[:5600], label[:5600]
    m, n = data.shape

    rf = forest(26, 4, 2)
    rf.fit(data, label)
    rf.saveForest()

    # forest = loadForest("forest.txt")
    print "\ntrain data accuracy:"
    output = rf.predict(data)
    print "size " + str(len(output)) + " vs " + str(m)
    correct = 0
    for i in range(m):
        if output[i] == label[i]:
            correct += 1
    print "correct " + str(correct) + "/" + str(m)

    print "\ntest data accuracy:"
    m, n = td.shape
    output = rf.predict(td)
    print "size " + str(len(output)) + " vs " + str(m)
    correct = 0
    for i in range(m):
        if output[i] == tl[i]:
            correct += 1
    print "correct " + str(correct) + "/" + str(m)
