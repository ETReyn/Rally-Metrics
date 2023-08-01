from IterationDAO import IterationDAO


class IterationData:
    def getIteration(self, iterationId):
        iterationDAO = IterationDAO()
        return iterationDAO.selectAll()[-1][0];
