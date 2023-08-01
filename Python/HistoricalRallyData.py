import json
from enum import Enum
from User import User
from UserDAO import UserDAO
from Iteration import Iteration
from IterationDAO import IterationDAO
from IterationComplete import IterationComplete
from IterationCompleteDAO import IterationCompleteDAO
from IterationIncomplete import IterationIncomplete
from IterationIncompleteDAO import IterationIncompleteDAO
from StoryType import StoryType
from CheckFlowState import checkFlowState
from ApiCall import apiCall
import requests
from UserCapacity import UserCapacity


class Main:
    def convertOwnerToUser(self, owner, iterations) -> User:
        zero = owner.storyCount[0]
        one = owner.storyCount[1]
        two = owner.storyCount[2]
        three = owner.storyCount[3]
        five = owner.storyCount[5]
        eight = owner.storyCount[8]
        thirteen = owner.storyCount[13]
        total = owner.getTotalEstimate()

        user = User(
            iterations.iterationId,
            owner.name,
            owner.id,
            total,
            zero,
            one,
            two,
            three,
            five,
            eight,
            thirteen,
        )
        return user

    def convertIterations(self, iterations) -> Iteration:
        it = Iteration(
            iterations.iterationId,
            iterations.iterationName,
            iterations.startDate,
            iterations.endDate,
            iterations.plan,
        )
        return it

    def convertCompleteIterations(self, iterations) -> IterationComplete:
        zero = iterations.iterationStoryCount[0]
        one = iterations.iterationStoryCount[1]
        two = iterations.iterationStoryCount[2]
        three = iterations.iterationStoryCount[3]
        five = iterations.iterationStoryCount[5]
        eight = iterations.iterationStoryCount[8]
        thirteen = iterations.iterationStoryCount[13]
        numStories = iterations.getNumberOfStories()

        total = (
            one + (2 * two) + (3 * three) + (5 * five) + (8 * eight) + (13 * thirteen)
        )

        ic = IterationComplete(
            iterations.iterationId,
            total,
            zero,
            one,
            two,
            three,
            five,
            eight,
            thirteen,
            numStories,
        )
        return ic

    def checkFlowState(self, story) -> int:
        complete = ["Complete", "Accepted"]
        mostlyComplete = ["Pending Environment", "Ready for Testing", "In Test"]
        if story["FlowState"]["_refObjectName"] in complete:
            return 1
        if story["FlowState"]["_refObjectName"] in mostlyComplete:
            return 2
        return 3

    def apiCall(self, callRequest, param, query):
        id = "_fvemG26dSGe9Qc55qqFCWU5CErYb6E8Bu9LmgGHJSBI"
        header = {"zsessionid": id}
        param = {
            "workspace": "https://rally1.rallydev.com/slm/webservice/v2.0/workspace/123",
            "start": 1,
            "pagesize": 5000,
            "query": query,
        }
        if param == 1:
            return requests.get(callRequest, headers=header).text
        return requests.get(callRequest, headers=header, params=param).text

    #   Limit calls to this method
    def callUser(self, user) -> int:
        nameResponse = self.apiCall(user["_ref"], 0, "")
        user = json.loads(nameResponse)["User"]
        # if user["Disabled"] == True:
        #     return -1
        return user["ObjectID"]

    def addFlowState(self, incompleteDictionary, flowState):
        if flowState == "In Test":
            incompleteDictionary.addInTest()
            return
        if flowState == "Defined":
            incompleteDictionary.addDefined()
            return
        if "Progress" in flowState:
            incompleteDictionary.addInProgress()
            return
        if "Failed" in flowState:
            incompleteDictionary.addFailedAc()
            return
        if "Pending" in flowState:
            incompleteDictionary.addPendingEnvironment()
            return
        if "Code" in flowState:
            incompleteDictionary.addCodeReview()
            return
        if "Test" in flowState:
            incompleteDictionary.addReadyForTest()
            return

    def getUserInfo(self, ignoreNamesList, name, user, activeUsers) -> User:
        # if name in ignoreNamesList:
        #     return None
        if name in activeUsers:
            return activeUsers[name]
        userId = self.callUser(user)
        # if userId == -1:
        #     ignoreNamesList.append(name)
        #     return None
        return userId

    def addToIterationDictionary(
        self, iterationDictionary, planEstimate, storyType, iterationId
    ):
        if storyType in iterationDictionary:
            iterationDictionary[storyType].addToStoryCount(planEstimate)
        else:
            iterationDictionary[storyType] = IterationComplete(iterationId, storyType)
            iterationDictionary[storyType].addToStoryCount(planEstimate)

    def callIndividualStory(
        self,
        story,
        userDictionary,
        completeDictionary,
        incompleteDictionary,
        ignoreNamesList,
        iterationId,
        activeUsers,
    ):
        try:
            user = story["Owner"]
            name = user["_refObjectName"]
            planEstimate = int(story["PlanEstimate"] or 0)
            userInfo = self.getUserInfo(ignoreNamesList, name, user, activeUsers)
            if userInfo != None:
                # print(planEstimate)
                try:
                    # print(planEstimate)
                    if name not in userDictionary:
                        userDictionary[name] = User(iterationId, name, userInfo)
                    storyType = ""
                    if "defect" in story["_ref"]:
                        storyType = "DEFECT"
                    elif "Vulnerabilities" in story["Feature"]["_refObjectName"]:
                        storyType = "SECURITY"
                    elif "Enhancements" in story["Feature"]["_refObjectName"]:
                        storyType = "ENHANCEMENT"
                    elif "Stabilization" in story["Feature"]["_refObjectName"]:
                        storyType = "STABILIZATION"
                    else:
                        storyType = "FEATURE"

                    flowState = self.checkFlowState(story)

                    if flowState < 3:
                        if storyType in completeDictionary:
                            completeDictionary[storyType].addToStoryCount(planEstimate)
                        else:
                            completeDictionary[storyType] = IterationComplete(
                                iterationId, storyType
                            )
                            completeDictionary[storyType].addToStoryCount(planEstimate)
                    if flowState > 1:
                        if storyType in incompleteDictionary:
                            incompleteDictionary[storyType].addToStoryCount(
                                planEstimate
                            )
                        else:
                            incompleteDictionary[storyType] = IterationIncomplete(
                                iterationId, storyType
                            )
                            incompleteDictionary[storyType].addToStoryCount(
                                planEstimate
                            )
                        self.addFlowState(
                            incompleteDictionary, story["FlowState"]["_refObjectName"]
                        )

                    userDictionary[name].addToStoryCount(planEstimate)
                    # print(planEstimate)
                except:
                    None
        except:
            print("No story owner")
        return userDictionary

    def callStoryCurrentIteration(self, story, iterationId, userDictionary):
        try:
            user = story["Owner"]
            name = user["_refObjectName"]
            planEstimate = int(story["PlanEstimate"] or 0)
            userInfo = self.getUserInfo([], name, user, [])
            if userInfo != None:
                try:
                    # print(planEstimate)
                    if name not in userDictionary:
                        userDictionary[name] = User(iterationId, name, userInfo)

                    userDictionary[name].addToStoryCount(planEstimate)
                    # print(planEstimate)
                except:
                    None
        except:
            print("No story owner")
        return userDictionary

    def persistIterationData(self, iteration, completeDictionary, incompleteDictionary):
        iterationDAO = IterationDAO()
        iterationCompleteDAO = IterationCompleteDAO()
        iterationIncompleteDAO = IterationIncompleteDAO()
        try:
            iterationDAO.insert(iteration)
            try:
                for story in completeDictionary:
                    # print(story)
                    iterationCompleteDAO.insert(completeDictionary[story])
            except:
                print("Iteration story type not added to complete")
                print(completeDictionary[story])
            try:
                for story in incompleteDictionary:
                    iterationIncompleteDAO.insert(incompleteDictionary[story])
            except:
                print("Iteration story type not added to incomplete")
                print(incompleteDictionary[story])
        except:
            print("Iteration not added to db")
            print(iteration)

    def callCurrentIteration(self, currentIteration):
        print(currentIteration)
        iterationResponse = self.apiCall(currentIteration["_ref"], 0, "")
        iterationData = json.loads(iterationResponse)["Iteration"]
        iterationName = iterationData["_refObjectName"]
        iterationId = iterationData["ObjectID"]
        workProductsResponse = self.apiCall(
            iterationData["WorkProducts"]["_ref"], 1, ""
        )
        workProductsData = json.loads(workProductsResponse)["QueryResult"]["Results"]
        userDictionary = {}
        plan = "PLAN" in iterationName
        if plan:
            return
        for work in workProductsData:
            self.callStoryCurrentIteration(work, iterationId, userDictionary)
        for user in userDictionary:
            userCapacity = UserCapacity(
                iterationId,
                userDictionary[user].getTotalEstimate(),
                userDictionary[user].userId,
            )
            userDAO = UserDAO()
            userDAO.insertCapacity(userCapacity)
            print(userDictionary[user].userId)
            print(userDictionary[user].name)
            print(userDictionary[user].getTotalEstimate())
            print("")

    def callSingleIteration(self, currentIteration, ignoreNames, activeUsers):
        iterationResponse = self.apiCall(currentIteration["_ref"], 0, "")
        iterationData = json.loads(iterationResponse)["Iteration"]
        iterationName = iterationData["_refObjectName"]
        iterationId = iterationData["ObjectID"]
        workProductsResponse = self.apiCall(
            iterationData["WorkProducts"]["_ref"], 1, ""
        )
        workProductsData = json.loads(workProductsResponse)["QueryResult"]["Results"]
        userDictionary = {}
        completeDictionary = {}
        incompleteDictionary = {}
        start = iterationData["StartDate"]
        end = iterationData["EndDate"]
        plan = "PLAN" in iterationName
        iteration = Iteration(iterationId, iterationName, start, end, plan)
        print(iterationName)

        for work in workProductsData:
            userDictionary = self.callIndividualStory(
                work,
                userDictionary,
                completeDictionary,
                incompleteDictionary,
                ignoreNames,
                iterationId,
                activeUsers,
            )
            # print(userDictionary)

        self.persistIterationData(iteration, completeDictionary, incompleteDictionary)

        return userDictionary

    def callAllIterations(self):
        allIterationRequest = (
            "https://rally1.rallydev.com/slm/webservice/v2.0/iteration"
        )
        allIterationResponse = self.apiCall(
            allIterationRequest, 1, "(StartDate <= today)"
        )
        allIterationData = json.loads(allIterationResponse)["QueryResult"]["Results"]
        ignoreName = []
        iterationList = []
        activeUsers = {}
        userDAO = UserDAO()
        iterationDAO = IterationDAO()
        savedIterations = iterationDAO.selectAll()
        iterationNames = []
        for iteration in savedIterations:
            iterationNames.append(iteration[1])
            # print(iteration[1])
        for i in range(len(allIterationData)):
            if allIterationData[i]["_refObjectName"] not in iterationNames:
                userDictionary = self.callSingleIteration(
                    allIterationData[i], ignoreName, activeUsers
                )
                iterationList.append(userDictionary)
                for i in range(len(iterationList)):
                    usersNotPersisted = {}
                    for user in iterationList[i]:
                        try:
                            userDAO.insert(iterationList[i][user])
                        except:
                            usersNotPersisted[user] = iterationList[i][user]
                    if len(usersNotPersisted) > 0:
                        iterationList[i] = usersNotPersisted
                # Take the userDictionary that is returned, and add the names and ids to a list. Before callSingleIteration calls calluser
                # Prepoulate the userDictionary, this should remove some inneficency and make this run a little faster
                for user in userDictionary:
                    if user not in activeUsers:
                        activeUsers[user] = userDictionary[user].userId
        self.callCurrentIteration(allIterationData[-1])


main = Main()
iterationSet = main.callAllIterations()
