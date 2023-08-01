

class IterationComplete:
    def __init__(self, iterationId, storyType):
        self.iterationId = iterationId
        self.iterationStoryCount = [0] * 14
        self.storyType = storyType

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

    def __str__(self) -> str:
        return f"""IterationId:{self.iterationId}\nStory Type:{self.storyType}Total Points:{self.getTotalEstimate()}\n
Total Stories:{self.getNumberStorues()}\nZero Points:{self.iterationStoryCount[0]}\nOne Points:{self.iterationStoryCount[1]}\n
Two Points{self.iterationStoryCount[2]}\nThree Points:{self.iterationStoryCount[3]}\nFive Points:{self.iterationStoryCount[5]}\n
Eight Points:{self.iterationStoryCount[8]}\nThirteen Points:{self.iterationStoryCount[13]}"""
