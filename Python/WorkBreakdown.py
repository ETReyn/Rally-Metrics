from IterationCompleteDAO import IterationCompleteDAO
from IterationDAO import IterationDAO
from datetime import datetime


class WorkBreakdown:

    def getWorkBreakdown(self, iterationId):
        iterationCompleteDAO = IterationCompleteDAO()
        iteration = IterationDAO()
        iterationData = iterationCompleteDAO.selectIterationById(
            iterationId)
        workBreakdown = []
        iterationName = iteration.selectIterationById(iterationData[0][0])
        print(iterationName[0][1]);
        for work in iterationData:

            workBreakdown.append(
                {
                    "iterationId": work[0],
                    "storyType": work[10],
                    "totalStories": work[1],
                    "totalPoints": work[2],
                    "zero": work[3],
                    "one": work[4],
                    "two": work[5],
                    "three": work[6],
                    "five": work[7],
                    "eight": work[8],
                    "thirteen": work[9],
                    "iterationName": iterationName[0][1]
                })
        return workBreakdown

    def getHistoricalWorkBreakdown(self):
        iterationCompleteDAO = IterationCompleteDAO()
        iterationDAO = IterationDAO()
        allIterationsByStoryType = iterationCompleteDAO.selectAllIterations()
        allIterations = iterationDAO.selectAll()
        historicalBreakdown = {}
        iterations = {}
        iterationCompleteList = []

        for iteration in allIterations:
            iterations[iteration[0]] = {}
            iterations[iteration[0]]["iterationId"] = iteration[0]
            iterations[iteration[0]]["iterationName"] = iteration[1]
            iterations[iteration[0]]["iterationStartDate"] = iteration[2]

        for iteration in allIterationsByStoryType:
            iterationCompleteList.append(
                {
                    "iterationId": iterations[iteration[0]]["iterationId"],
                    "iterationStartDate": iterations[iteration[0]]["iterationStartDate"],
                    "iteration": iterations[iteration[0]]["iterationName"],
                    "storyType": iteration[10],
                    "totalStories": iteration[1],
                    "totalPoints": iteration[2],
                    "zero": iteration[3],
                    "one": iteration[4],
                    "two": iteration[5],
                    "three": iteration[6],
                    "five": iteration[7],
                    "eight": iteration[8],
                    "thirteen": iteration[9],
                })
            print(iteration)
            # if (iteration[0] not in iterationCompleteMap):
            #     iterationCompleteMap[iteration[0]] = {}
            # stories = []
            # for x in range(1, 10):
            #     stories.append(iteration[x])
            # iterationCompleteMap[iteration[0]][iteration[-1]] = stories
            # iterationCompleteMap[iteration[0]
            #                      ]['name'] = iterations[iteration[0]]

        return sorted(iterationCompleteList, key=lambda d: d['iterationStartDate'])


wb = WorkBreakdown()
wb.getHistoricalWorkBreakdown()
