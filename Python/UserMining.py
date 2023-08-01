from DatabaseConnection import DatabaseConnection
from datetime import datetime, timedelta


class UserMining:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM USER_MINING"
        return db.executeSQL(query, None, True)

    def selectAllByUser(self, user):
        db = DatabaseConnection()
        query = "SELECT * FROM USER_MINING WHERE name = %s"
        data = (user,)
        return db.executeSQL(query, data, True)

    def insert(self, userMining):
        db = DatabaseConnection()
        query = """INSERT INTO USER_MINING (iteration_id, user_id, total_stories, total_points, name) 
        Values(%s, %s, %s, %s, %s)"""
        data = (
            userMining.iterationId,
            userMining.userId,
            userMining.totalStories,
            userMining.totalPoints,
            userMining.name,
        )
        db.executeSQL(query, data, False)
