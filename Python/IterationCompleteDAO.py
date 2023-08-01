from DatabaseConnection import DatabaseConnection
from IterationDAO import IterationDAO
from IterationComplete import IterationComplete


class IterationCompleteDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION_COMPLETE"
        db.executeSQL(query, None, True)
        db.close()

    def selectIterations(self, iterationIds):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION_COMPLETE WHERE iteration_id in %s"
        data = (iterationIds)
        output = db.executeSQL(query, data, True)
        db.close()
        return output

    def selectIterationById(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION_COMPLETE WHERE iteration_id = %s"
        data = (iterationId,)
        output = db.executeSQL(query, data, True)
        db.close()
        return output

    def selectAllIterations(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION_COMPLETE"
        output = db.executeSQL(query, None, True)
        db.close()
        return output

    def insert(self, iterationComplete):
        db = DatabaseConnection()
        query = """INSERT INTO ITERATION_COMPLETE (iteration_id, total_points, zero_points, one_point, two_points, three_points, five_points, eight_points, thirteen_points, total_stories, story_type) 
        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (iterationComplete.iterationId, iterationComplete.getTotalEstimate(), iterationComplete.iterationStoryCount[0],
                iterationComplete.iterationStoryCount[1], iterationComplete.iterationStoryCount[
                    2], iterationComplete.iterationStoryCount[3],
                iterationComplete.iterationStoryCount[5], iterationComplete.iterationStoryCount[
                    8], iterationComplete.iterationStoryCount[13],
                iterationComplete.getNumberStories(), iterationComplete.storyType)
        db.executeSQL(query, data, False)
        db.close()

    def addZeros(self):
        db = DatabaseConnection()
        iterationDAO = IterationDAO()
        iterations = iterationDAO.selectAll()
        allIterations = []
        for iteration in iterations:
            allIterations.append(iteration[0])
        for iteration in allIterations:
            storyTypes = self.selectIterationById(iteration)
            allStories = {
                "DEFECT": 0,
                "FEATURE": 0,
                "STABILIZATION": 0,
                "SECURITY": 0,
                "ENHANCEMENT": 0
            }
            for story in storyTypes:
                if (story[10] == "DEFECT"):
                    allStories["DEFECT"] = 1
                if (story[10] == "FEATURE"):
                    allStories["FEATURE"] = 1
                if (story[10] == "ENHANCEMENT"):
                    allStories["ENHANCEMENT"] = 1
                if (story[10] == "STABILIZATION"):
                    allStories["STABILIZATION"] = 1
                if (story[10] == "SECURITY"):
                    allStories["SECURITY"] = 1
            for story in allStories:
                if (allStories[story] == 0):
                    iterationComplete = IterationComplete(iteration, story)
                    iterationComplete.getNumberStories()
                    iterationComplete.getTotalEstimate()
                    self.insert(iterationComplete)
        db.close()
