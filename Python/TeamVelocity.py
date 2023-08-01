from IterationCompleteDAO import IterationCompleteDAO
from IterationDAO import IterationDAO


class TeamVelocity:
    def getHistoricVelocity(self):
        iterationDAO = IterationDAO()
        iterationCompleteDAO = IterationCompleteDAO()
        iterationList = list(zip(*iterationDAO.selectAllIgnorePlanning()))[0]
        allIterationData = iterationCompleteDAO.selectIterations(
            (iterationList,))
        totalPoints = 0
        for data in allIterationData:
            totalPoints += data[2]
        return totalPoints/len(iterationList)
