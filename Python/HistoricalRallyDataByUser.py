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
from UserMining import UserMining
from Mining import Mining
from datetime import datetime


class Main:
    def apiCall(self, callRequest, param, start, pageSize):
        id = "_fvemG26dSGe9Qc55qqFCWU5CErYb6E8Bu9LmgGHJSBI"
        header = {"zsessionid": id}
        param = {
            "start": start,
            "pagesize": pageSize,
        }
        if param == 1:
            return requests.get(callRequest, headers=header).text
        return requests.get(callRequest, headers=header, params=param).text

    def getIterationData(self, iterationDict, story):
        if "Feature" in story:
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

            if story["Iteration"]["_refObjectName"] not in iterationDict:
                iterationDict[story["Iteration"]["_refObjectName"]] = {
                    "iteration": story["Iteration"]["_refObjectName"],
                    "DEFECT": [],
                    "FEATURE": [],
                    "STABILIZATION": [],
                    "ENHANCEMENT": [],
                    "SECURITY": [],
                }

            iterationDict[story["Iteration"]["_refObjectName"]][storyType].append(
                story["PlanEstimate"]
            )
            return iterationDict

    def getTeamMemberData(self, teamMember, iterations, userId, owner, iterationData):
        count = 1
        totalResultCount = 1001
        userIterations = {}
        storiesWithoutIterations = []
        while totalResultCount > 100 * count:
            path = teamMember["_ref"] + "/ArtifactsOwned"
            teamMemberResponse = self.apiCall(path, 1, 1 + (100 * (count - 1)), 100)
            teamMemberData = json.loads(teamMemberResponse)["QueryResult"]["Results"]
            for story in teamMemberData:
                if "task" in story["_ref"]:
                    continue
                if "PlanEstimate" not in story:
                    continue
                if story["PlanEstimate"] == None:
                    continue
                if "Iteration" not in story:
                    continue
                if story["Iteration"] == None:
                    if "AcceptedDate" in story:
                        if story["AcceptedDate"] == None:
                            continue
                        else:
                            storiesWithoutIterations.append(story)
                    continue
                storyIteration = story["Iteration"]["_refObjectName"]
                if storyIteration in userIterations:
                    userIterations[storyIteration]["points"].append(
                        story["PlanEstimate"]
                    )
                else:
                    path = story["Iteration"]["_ref"]
                    iteration = self.apiCall(path, 0, 0, 0)
                    iterationData = json.loads(iteration)["Iteration"]
                    iterations[iterationData["ObjectID"]] = {
                        "startDate": datetime.strptime(
                            iterationData["StartDate"][0:10], "%Y-%m-%d"
                        ),
                        "endDate": datetime.strptime(
                            iterationData["EndDate"][0:10], "%Y-%m-%d"
                        ),
                        "id": iterationData["ObjectID"],
                        "key": iterationData["_refObjectName"],
                    }
                    userIterations[storyIteration] = {
                        "points": [story["PlanEstimate"]],
                        "endDate": datetime.strptime(
                            iterationData["EndDate"][0:10], "%Y-%m-%d"
                        ),
                    }
                self.getIterationData(iterationData, story)

            count += 1
            totalResultCount = json.loads(teamMemberResponse)["QueryResult"][
                "TotalResultCount"
            ]
        for story in storiesWithoutIterations:
            for iteration in iterations:
                if (
                    iterations[iteration]["startDate"]
                    <= datetime.strptime(story["AcceptedDate"][0:10], "%Y-%m-%d")
                    <= iterations[iteration]["endDate"]
                ):
                    if iterations[iteration]["key"] not in userIterations:
                        userIterations[iterations[iteration]["key"]] = []
                    userIterations[iterations[iteration]["key"]].append(
                        story["PlanEstimate"]
                    )
        # print(userIterations)
        # userMining = UserMining()
        # for iteration in userIterations:
        #     user = userId
        #     name = owner
        #     iterationId = iteration
        #     totalPoints = sum(userIterations[iteration]["points"])
        #     totalStories = len(userIterations[iteration]["points"])
        #     endDate = userIterations[iteration]["endDate"]
        #     mining = Mining(user, iterationId, totalPoints, totalStories, name)
        #     userMining.insert(mining)

    def getAllUsers(self):
        path = "https://rally1.rallydev.com/slm/webservice/v2.0/Project/128415043464/TeamMembers"
        allTeamMembersResponse = self.apiCall(path, 1, 1, 1000)
        allTeamMembersData = json.loads(allTeamMembersResponse)["QueryResult"][
            "Results"
        ]
        iterations = {}
        iterationData = {}
        for teamMember in allTeamMembersData:
            self.getTeamMemberData(
                teamMember,
                iterations,
                teamMember["ObjectID"],
                teamMember["_refObjectName"],
                iterationData,
            )
            print(iterationData)


main = Main()
main.getAllUsers()
