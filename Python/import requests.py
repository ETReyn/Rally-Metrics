import requests
import json
from enum import Enum


class StoryType(Enum):
    FEATURE = 1
    DEFECT = 2
    SECURITY = 3
    STABILIZATION = 4
    ENHANCEMENT = 5


class Story:
    def __init__(self, ref, name, storyType, points, status):
        self.ref = ref
        self.name = name
        self.storyType = storyType
        self.point = points
        self.status = status


class StoryTotals:

    def __init__(self):
        self.points = 0
        self.count = 0

    def addToStoryTotals(self, points):
        self.points += points
        self.count += 1


class Iteration:
    iterationId = -1
    iterationName = ""
    iterationStoryCount = [0] * 14
    iterationTotal = 0
    iterationDefect = StoryTotals()
    iterationFeature = StoryTotals()
    iterationEnhancement = StoryTotals()
    iterationSecurity = StoryTotals()
    iterationStabilization = StoryTotals()

    def __init__(self, iterationId, iterationName):
        self.iterationId = iterationId
        self.iterationName = iterationName
        self.iterationStoryCount = [0] * 14

    def addToStoryCount(self, index):
        self.iterationStoryCount[index] += 1

    def addToStoryType(self, givenType, estimate):
        if givenType == StoryType.DEFECT:
            self.iterationDefect.addToStoryTotals(estimate)
        if givenType == StoryType.ENHANCEMENT:
            self.iterationEnhancement.addToStoryTotals(estimate)
        if givenType == StoryType.SECURITY:
            self.iterationSecurity.addToStoryTotals(estimate)
        if givenType == StoryType.STABILIZATION:
            self.iterationStabilization.addToStoryTotals(estimate)
        if givenType == StoryType.FEATURE:
            self.iterationFeature.addToStoryTotals(estimate)

    def addStoryCount(self, index):
        self.iterationStoryCount[index] += 1

    def __str__(self):
        totalEstimate = 0
        numberOfStories = 0
        for i in range(len(self.iterationStoryCount)):
            totalEstimate += (i * self.iterationStoryCount[i])
            numberOfStories += self.iterationStoryCount[i]
        return f"ID:{self.iterationId}\nNAME:{self.iterationName}\nStoryCount:{self.iterationStoryCount}\nTotal Estimate:{totalEstimate}\nStory Count:{numberOfStories}"


class Owner:
    name = ''
    id = -1
    storyCount = [14] * 0

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.storyCount = [0] * 14

    def __str__(self):
        return f"\nName:{self.name} \nID:{self.id} \nIteration:{self.iteration} \nstoryCount:{self.storyCount}"

    def addToStoryCount(self, index):
        self.storyCount[index] += 1


class Main:
    def apiCall(self, callRequest, param, query):
        id = "_fvemG26dSGe9Qc55qqFCWU5CErYb6E8Bu9LmgGHJSBI"
        header = {"zsessionid": id}
        param = {
            "workspace": "https://rally1.rallydev.com/slm/webservice/v2.0/workspace/123",
            "start":  1,
            "pagesize": 5000,
            "query": query
        }
        if param == 1:
            return requests.get(callRequest, headers=header).text
        return requests.get(callRequest, headers=header, params=param).text

    def callUser(self, user):
        nameResponse = self.apiCall(user["_ref"], 0, "")
        user = json.loads(nameResponse)["User"]
        if user["Disabled"] == True:
            return -1
        return user["ObjectID"]

    def callIndividualStory(self, story, userDict, storyDict, ignoreName, iterationData):
        try:
            name = story["Owner"]["_refObjectName"]
            storyName = story["_refObjectName"]
            planEstimate = int(
                story["PlanEstimate"] or 0)
            userId = 1
            if name not in ignoreName:
                if name not in userDict:
                    userId = self.callUser(story["Owner"])
                    if userId > 0:
                        userDict[name] = Owner(
                            name, userId)
                    else:
                        ignoreName.append(name)
                if userId > 0:
                    try:
                        storyType = ""
                        if ("defect" in story["_ref"]):
                            storyType = StoryType.DEFECT
                        elif ("Vulnerabilities" in story["Feature"]["_refObjectName"]):
                            storyType = StoryType.SECURITY
                        elif ("Enhancements" in story["Feature"]["_refObjectName"]):
                            storyType = StoryType.ENHANCEMENT
                        elif ("Stabilization" in story["Feature"]["_refObjectName"]):
                            storyType = StoryType.STABILIZATION
                        else:
                            storyType = StoryType.FEATURE

                        iterationData.addToStoryType(storyType, planEstimate)
                        iterationData.addStoryCount(planEstimate)
                        userDict[name].addToStoryCount(planEstimate)
                        # print(name + " " + str(planEstimate) + " " + storyName)
                        if userDict[name] not in storyDict:
                            storyDict[userDict[name]] = 0
                        storyDict[userDict[name]
                                  ] += planEstimate
                    except:
                        print("An error has occured")
        except:
            print("No story owner")

    def callSingleIteration(self, iteration, ignoreName):
        iterationResponse = self.apiCall(iteration["_ref"], 0, "")
        iterationData = json.loads(iterationResponse)["Iteration"]
        iterationName = iterationData["_refObjectName"]
        iterationId = iterationData["ObjectID"]
        workProductsResponse = self.apiCall(
            iterationData["WorkProducts"]["_ref"], 1, "")
        workProductsData = json.loads(workProductsResponse)[
            "QueryResult"]["Results"]
        userDict = {}
        storyDict = {}
        totalEstimate = 0
        iterationObject = Iteration(iterationId, iterationName)
        for work in workProductsData:
            self.callIndividualStory(
                work, userDict, storyDict, ignoreName, iterationObject)

        return iterationObject

    def callAllIterations(self):
        allIterationRequest = "https://rally1.rallydev.com/slm/webservice/v2.0/iteration"
        allIterationResponse = self.apiCall(
            allIterationRequest, 1, "(EndDate <= today)")
        allIterationData = json.loads(allIterationResponse)[
            "QueryResult"]["Results"]
        ignoreName = []
        iterationDataSet = []
        # iterationDataSet.append(self.callSingleIteration(
        #     allIterationData[102], ignoreName))
        for i in range(106):
            iterationDataSet.append(self.callSingleIteration(
                allIterationData[i], ignoreName))
        return iterationDataSet


main = Main()
iterationSet = main.callAllIterations()
for iteration in iterationSet:
    print(iteration)
# allStoriesList = "https://rally1.rallydev.com/slm/webservice/v2.0/hierarchicalrequirement"
# id = "_fvemG26dSGe9Qc55qqFCWU5CErYb6E8Bu9LmgGHJSBI"
# header = {"zsessionid": id}
# param = {
#     "workspace": "https://rally1.rallydev.com/slm/webservice/v2.0/workspace/123",
#     "query": "((Iteration.StartDate <= today) AND (Iteration.EndDate >= today-70))",
#     "start":  1,
#     "pagesize": 2000
# }
# allStoriesResponse = requests.get(
#     allStoriesList, headers=header, params=param)
# allStoriesData = json.loads(allStoriesResponse.text)[
#     "QueryResult"]["Results"]
# nameIdDict = {}
# userToStoryDict = {}
# main = Main()
# ownerList = []
# storylist = []
# count = 0
# for story in allStoriesData:
#     if count % 50 == 0:
#         print(count)
#     count += 1
#     main.callIndividualStory(story, nameIdDict, userToStoryDict, storylist)

# for owner in userToStoryDict:
#     print(owner)
#     print(userToStoryDict[owner])
