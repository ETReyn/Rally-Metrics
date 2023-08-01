from DatabaseConnection import DatabaseConnection


class UserDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM USERS"
        ret = db.executeSQL(query, None, True)
        db.close()
        return ret

    def selectAllById(self, id, iterations):
        db = DatabaseConnection()
        query = "SELECT * FROM USERS WHERE user_id = %s AND iteration_id in %s"
        data = (id, iterations)
        output = db.executeSQL(query, data, True)
        db.close()
        return output

    def selectCapacityById(self, id):
        db = DatabaseConnection()
        query = "SELECT * FROM USER_CAPACITY WHERE user_id = %s"
        data = (id, )
        output = db.executeSQL(query, data, True)
        db.close()
        return output

    def getDistinctUsers(self):
        db = DatabaseConnection()
        query = "SELECT DISTINCT name, user_id FROM USERS"
        output = db.executeSQL(query, None, True)
        db.close()
        return output

    def insert(self, user):
        db = DatabaseConnection()
        query = """INSERT INTO USERS (iteration_id, total_points, zero_points, one_point, two_points, three_points, five_points, eight_points, thirteen_points, name, user_id)
        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (user.iterationId, user.getTotalEstimate(), user.userStoryCount[0], user.userStoryCount[1], user.userStoryCount[2],
                user.userStoryCount[3], user.userStoryCount[5], user.userStoryCount[8], user.userStoryCount[13], user.name, user.userId)
        db.executeSQL(query, data, False)
        db.close()

    def insertCapacity(self, user):
        db = DatabaseConnection()
        query = "DELETE FROM USER_CAPACITY WHERE USER_ID=%s"
        data = (user.userId, )
        db.executeSQL(query, data, False)
        query = "INSERT INTO USER_CAPACITY(USER_ID, CAPACITY, ITERATION_ID) VALUES(%s, %s, %s)"
        data = (user.userId, user.capacity, user.iterationId)
        db.executeSQL(query, data, False)
