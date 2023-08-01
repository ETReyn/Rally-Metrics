class User:
    def __init__(self, iterationId, name, userId):
        self.iterationId = iterationId
        self.userStoryCount = [0] * 14
        self.name = name
        self.userId = userId

    def addToStoryCount(self, index):
        self.userStoryCount[index] += 1

    def getTotalEstimate(self) -> int:
        totalEstimate = 0
        for i in range(len(self.userStoryCount)):
            totalEstimate += (i * self.userStoryCount[i])
        return totalEstimate

    def getNumberStorues(self) -> int:
        numStories = 0
        for i in range(len(self.userStoryCount)):
            numStories += self.userStoryCount[i]
        return numStories

    def __str__(self) -> str:
        return f"""User Id:{self.userId}\nName:{self.name}\nIterationId:{self.iterationId}\nTotal Points:{self.getTotalEstimate()}\nTotal Stories:{self.getNumberStorues()}\nZero Points:{self.userStoryCount[0]}One Points:{self.userStoryCount[1]}\nTwo Points{self.userStoryCount[2]}\nThree Points:{self.userStoryCount[3]}\nFive Points:{self.userStoryCount[5]}\nEight Points:{self.userStoryCount[8]}\nThirteen Points:{self.userStoryCount[13]}"""
