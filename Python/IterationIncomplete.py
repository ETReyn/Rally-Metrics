from DatabaseConnection import DatabaseConnection
from StoryType import StoryType


class IterationIncomplete:
    def __init__(self, storyType, iterationId):
        self.iterationId = iterationId
        self.storyType = storyType
        self.defined = 0
        self.inProgress = 0
        self.failedAc = 0
        self.codeReview = 0
        self.pendingEnvironment = 0
        self.readyForTest = 0
        self.inTest = 0
        self.iterationStoryCount[0] * 14

    def addToStoryCount(self, index):
        self.iterationStoryCount[index] += 1

    def getTotalEstimate(self) -> int:
        totalEstimate = 0
        for i in range(len(self.iterationStoryCount)):
            totalEstimate += (i * self.iterationStoryCount[i])
        return totalEstimate

    def getNumberStories(self) -> int:
        numStories = 0
        for i in range(len(self.iterationStoryCount)):
            numStories += self.iterationStoryCount[i]
        return numStories

    def addDefined(self):
        self.defined += 1

    def addInProgress(self):
        self.inProgress += 1

    def addFailedAc(self):
        self.failedAc += 1

    def addCodeReview(self):
        self.codeReview += 1

    def addPendingEnvironment(self):
        self.pendingEnvironment += 1

    def addReadyForTest(self):
        self.readyForTest += 1

    def addInTest(self):
        self.inTest += 1
