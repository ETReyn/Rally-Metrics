import psycopg2
from enum import Enum


class StoryType(Enum):
    FEATURE = 1
    DEFECT = 2
    SECURITY = 3
    STABILIZATION = 4
    ENHANCEMENT = 5


class Iteration:
    def __init__(self, iterationId, iterationName, startDate, endDate, planning):
        self.iterationId = iterationId
        self.iterationName = iterationName
        self.startDate = startDate
        self.endDate = endDate
        self.planning = planning


class IterationIncomplete:
    def __init__(self, storyType, iterationId, defined, inProgress, failedAc, codeReview, pendingEnvironment, readyForTest, inTest):
        self.iterationId = iterationId
        self.storyType = storyType
        self.defined = defined
        self.inProgress = inProgress
        self.failedAc = failedAc
        self.codeReview = codeReview
        self.pendingEnvironment = pendingEnvironment
        self.readyForTest = readyForTest
        self.inTest = inTest

    def insert(self, storyType):
        db = DatabaseConnection()
        query = """INSERT INTO %s (iteration_id, defined, in_progress, failed_ac, code_review, pending_environment, ready_for_test, in_test) 
        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = ""
        if storyType == StoryType.DEFECT:
            data = ("ITERATIONINCOMPLETEDEFECTS", self.iterationId, self.defined, self.inProgress, self.failedAc, self.codeReview,
                    self.pendingEnvironment, self.readyForTest, self.inTest)
        else:
            data = ("ITERATIONINCOMPLETEFEATURES", self.iterationId, self.defined, self.inProgress, self.failedAc, self.codeReview,
                    self.pendingEnvironment, self.readyForTest, self.inTest)
        db.executeSQL(query, data, False)


class UserDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM USER"
        db.executeSQL(query, None, True)

    def selectAllByName(self, name):
        db = DatabaseConnection()
        query = "SELECT * FROM USER where USER.name = %s"
        data = (name)
        db.executeSQL(query, data, True)


class IterationCompleteDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATIONCOMPLETE"
        db.executeSQL(query, None, True)

    def selectIteration(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATIONCOMPLETE WHERE iteration_id = %s"
        data = (iterationId)
        db.executeSQL(query, data, True)


class IterationIncompleteFeatureDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATIONINCOMPLETEFEATURE"
        db.executeSQL(query, None, True)

    def selectIteration(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATIONINCOMPLETEFEATURE WHERE iteration_id = %s"
        data = (iterationId)
        db.executeSQL(query, data, True)


class IterationIncompleteDefectDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATIONINCOMPLETEDEFECT"
        db.executeSQL(query, None, True)

    def selectIteration(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATIONINCOMPLETEDEFECT WHERE iteration_id = %s"
        data = (iterationId)
        db.executeSQL(query, data, True)


class IterationDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION"
        db.executeSQL(query, None, True)

    def selectIteration(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION WHERE iteration_id = %s"
        data = (iterationId)
        db.executeSQL(query, data, True)


class IterationComplete:
    def __init__(self, iterationId, totalPoints, zeroPoints, onePoint, twoPoints, threePoints, fivePoints, eightPoints, thirteenPoints, totalStories):
        self.iterationId = iterationId
        self.totalPoints = totalPoints
        self.zeroPoints = zeroPoints
        self.onePoint = onePoint
        self.twoPoints = twoPoints
        self.threePoints = threePoints
        self.fivePoints = fivePoints
        self.eightPoints = eightPoints
        self.thirteenPoints = thirteenPoints
        self.totalStories = totalStories

    def insert(self):
        db = DatabaseConnection()
        query = """INSERT INTO ITERATIONCOMPLETE (iteration_id, total_points, zero_points, one_point, two_points, three_points, five_points, eight_points, thirteen_points, total_stories) 
        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (self.iterationId, self.totalPoints, self.zeroPoints, self.onePoint, self.twoPoints,
                self.threePoints, self.fivePoints, self.eightPoints, self.thirteenPoints, self.totalStories)
        db.executeSQL(query, data, False)


class User:
    def __init__(self, iterationId, name, totalPoints, zeroPoints, onePoint, twoPoints, threePoints, fivePoints, eightPoints, thirteenPoints):
        self.iterationId = iterationId
        self.totalPoints = totalPoints
        self.zeroPoints = zeroPoints
        self.onePoint = onePoint
        self.twoPoints = twoPoints
        self.threePoints = threePoints
        self.fivePoints = fivePoints
        self.eightPoints = eightPoints
        self.thirteenPoints = thirteenPoints
        self.name = name

    def insert(self):
        db = DatabaseConnection()
        query = """INSERT INTO USER (iteration_id, total_points, zero_points, one_point, two_points, three_points, five_points, eight_points, thirteen_points, name) 
        Values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        data = (self.iterationId, self.totalPoints, self.zeroPoints, self.onePoint, self.twoPoints,
                self.threePoints, self.fivePoints, self.eightPoints, self.thirteenPoints, self.name)
        db.executeSQL(query, data, False)

    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM USER"
        db.executeSQL(query, None, True)

    def selectAllByName(self, name):
        db = DatabaseConnection()
        query = "SELECT * FROM USER where USER.name = %s"
        data = (name)
        db.executeSQL(query, data, True)


class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="postgres",
            user="postgres",
            password="pgpassword",
            host="database-1.cz6gplhyvfbz.us-east-2.rds.amazonaws.com",
            port='5432'
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.cursor.close()
        self.conn.close()

    def executeSQL(self, query, data, select):
        if data is None:
            self.cursor.execute(query)
        else:
            self.cursor.execute(query, data)
        if select:
            output = self.cursor.fetchall()
            self.close()
            return output
        self.close()


# db = DatabaseConnection()
# print(db.executeSQL("SELECT * FROM test;", True))
# db.close()

# conn = psycopg2.connect(
#     database="postgres",
#     user="postgres",
#     password="pgpassword",
#     host="database-1.cz6gplhyvfbz.us-east-2.rds.amazonaws.com",
#     port='5432'
# )

# # Open a cursor to perform database operations
# cur = conn.cursor()

# # cur.execute(
# #     "CREATE TABLE FY2023-Q2-I2-1/18-2/7 (id serial PRIMARY KEY, num integer, data varchar);")
# cur.execute(
#     "INSERT INTO test  (num, data) VALUES (%s, %s)", (100, "abc'def"))
# cur.execute("SELECT * FROM test;")
# print(cur.fetchone())

# conn.commit()

# cur.close()
# conn.close()
