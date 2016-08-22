# coding:utf8
import math
import random


def splitDataset(dataset, ratio):
    '''
    splitDataset takes a full set of data in
    array of arrays format and returns a training
    set and a test set based on the ratio you pass in
    '''

    trainSize = int(len(dataset) * ratio)
    trainSet = []
    testSet = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(testSet))
        trainSet.append(testSet.pop(index))

    return trainSet, testSet


def getLabels(dataset, indexOfLabel=-1):
    labels = []

    for i in range(len(dataset)):
        labels.append(dataset[i].pop(indexOfLabel))

    return labels


def splitDataByLabel(data, labels):
    '''
    groups data by labels
    returns a dict: { 'a': [[...],[...]] }
    '''

    if len(data) != len(labels):
        print "data and labels arrays are different lengths"
        return

    byClass = {}

    for i in range(len(labels)):

        if labels[i] in byClass:
            byClass[labels[i]].append(data[i])
        else:
            byClass[labels[i]] = []
            byClass[labels[i]].append(data[i])

    return byClass


def mean(numbers):
    '''
    numbers: a vector
    returns: a single mean value
    '''

    return sum(numbers) / float(len(numbers))


def variance(numbers):
    '''
    numbers: a vector
    returns: a single variance value
    '''

    _mean = mean(numbers)

    return sum([pow(x - _mean, 2) for x in numbers]) / float(len(numbers) - 1)


def stDev(numbers):
    '''
    numbers: a vector
    returns: a single standard deviation value
    '''

    _variance = variance(numbers)

    return math.sqrt(_variance)


def calcConditionalProbability(x, mean, stDev):
    '''
    x: the data point to test
    mean: mean of dataset
    stDev: standard deviation of dataset
    '''

    exponent = math.exp(-(math.pow(x - mean, 2) / (2 * math.pow(stDev, 2))))

    return (1 / (math.sqrt(2 * math.pi) * stDev)) * exponent


def calcClassProbability(summaries, vector):
    probabilities = {}

    for label, labelSummary in summaries.iteritems():
        probabilities[label] = 1

        for i in range(len(labelSummary)):
            mean, var, stDev = labelSummary[i]
            x = vector[i]
            probabilities[label] *= calcConditionalProbability(x, mean, stDev)

    return probabilities


def summarizeByAttribute(dataset):
    '''
    dataset: array of arrays
    returns: [(mean, var, stDev)...(meanN, varN, stDevN)]
    this function assumes that your label is NOT in the dataset
    '''

    summary = [(mean(attr), variance(attr), stDev(attr))
               for attr in zip(*dataset)]
    return summary


def summarizeByLabel(dataset, labels):
    '''
    dataset: array of arrays
    labels: array of labels
    len(dataset) == len(labels)
    returns dict {label: (mean, var, stDev)}
    '''

    groupByLabel = splitDataByLabel(dataset, labels)

    summaryByLabel = {}

    for label, data in groupByLabel.iteritems():
        summaryByLabel[label] = summarizeByAttribute(data)

    return summaryByLabel


def getAccuracy(labels, predictions):
    '''
    labels: 1-dimensional array of length N
    predictions: 1-dimensional array of length N
    returns: decimal % of correct predictions
    '''

    if len(labels) != len(predictions):
        print "Array lengths do not match"
        return

    correct = 0

    for i in range(len(labels)):
        if labels[i] == predictions[i]:
            correct += 1

    return correct / float(len(predictions))


class NaiveBayesGaussian:
    def fit(self, dataset, labels):
        self.summariesByLabel = summarizeByLabel(dataset, labels)

    def _predict(self, vector):
        probabilities = calcClassProbability(self.summariesByLabel, vector)

        bestLabel, bestProb = None, -1

        for classValue, probability in probabilities.iteritems():
            if bestLabel is None or probability > bestProb:
                bestLabel = classValue
                bestProb = probability

        return bestLabel

    def predict(self, testSet):
        predictions = []

        for i in range(len(testSet)):
            predictions.append(self._predict(testSet[i]))

        return predictions


if __name__ == "__main__":
    NBg = NaiveBayesGaussian()
    dataset = ''
    ratio = 0.67
    trainSet, testSet = splitDataset(dataset, ratio)
    trainLabels = getLabels(trainSet)
    testLabels = getLabels(testSet)
    NBg.fit(trainSet, trainLabels)
    predictions = NBg.predict(testSet)
    accuracy = getAccuracy(testLabels, predictions)
