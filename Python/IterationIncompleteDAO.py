from DatabaseConnection import DatabaseConnection


class IterationIncompleteDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION_INCOMPLETE"
        db.executeSQL(query, None, True)
        db.close()

    def selectIteration(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION_INCOMPLETE WHERE iteration_id = %s"
        data = (iterationId)
        db.executeSQL(query, data, True)
        db.close()

    def insert(self, iterationIncomplete):
        db = DatabaseConnection()
        query = """INSERT INTO ITERATION_INCOMPLETE (iteration_id, defined, in_progress, failed_ac, code_review, pending_environment, ready_for_test, in_test
        total_points, zero_points, one_point, two_points, three_points, five_points, eight_points, thirteen_points, total_stories) 
        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (iterationIncomplete.iterationId, iterationIncomplete.defined, iterationIncomplete.inProgress, iterationIncomplete.failedAc, iterationIncomplete.codeReview,
                iterationIncomplete.pendingEnvironment, iterationIncomplete.readyForTest, iterationIncomplete.inTest, iterationIncomplete.iterationId,
                iterationIncomplete.getTotalEstimate(
                ), iterationIncomplete.iterationStoryCount[0], iterationIncomplete.iterationStoryCount[1], iterationIncomplete.iterationStoryCount[2], iterationIncomplete.iterationStoryCount[3],
                iterationIncomplete.iterationStoryCount[5], iterationIncomplete.iterationStoryCount[8], iterationIncomplete.iterationStoryCount[13], iterationIncomplete.getNumberStories())
        db.executeSQL(query, data, False)
        db.close()
