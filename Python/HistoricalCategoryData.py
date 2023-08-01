from IterationComplete import IterationComplete
from IterationCompleteDAO import IterationCompleteDAO
from IterationDAO import IterationDAO


class HistoricalCategoryData:

    def getAllSprintInfo(self):
        iterationDAO = IterationDAO()
        iterationCompleteDAO = IterationCompleteDAO()
        iterations = iterationDAO.selectAllIgnorePlanning()
        iterationList = list(zip(*iterations))[0]
        iterationDict = {}
        for iteration in iterations:
            iterationDict[iteration[0]] = iteration
        completeIterationData = iterationCompleteDAO.selectIterations(
            (iterationList,))
        completeIterationDict = {}
        for data in completeIterationData:
            if iterationDict[data[0]] not in completeIterationDict:
                completeIterationDict[iterationDict[data[0]]] = []
            completeIterationDict[iterationDict[data[0]]].append(data)

        return completeIterationDict

    def getSpecificCategoryData(self, iterationId):
        iterationDAO = IterationDAO()
        iteration = iterationDAO.selectIterationById((iterationId,))
        print(iteration)
        iteration = list(zip(*iteration))[0]
        iterationCompleteDAO = IterationCompleteDAO()
        completeIterationData = iterationCompleteDAO.selectIterationById(
            (iterationId,))
        completeIterationDict = {}
        completeIterationDict[iteration] = []
        for data in completeIterationData:
            completeIterationDict[iteration].append(data)

        return completeIterationDict


hcd = HistoricalCategoryData()
data = hcd.getSpecificCategoryData(128415043608)

test = True
for d in data:
    if test:
        print(data[d])
