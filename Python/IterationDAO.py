from DatabaseConnection import DatabaseConnection
from datetime import datetime, timedelta


class IterationDAO:
    def selectAll(self):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION"
        return db.executeSQL(query, None, True)

    def selectAllIgnorePlanning(self):
        db = DatabaseConnection()
        query = "SELECT iteration_id FROM ITERATION WHERE NOT planning"
        return db.executeSQL(query, None, True)

    def selectIterationById(self, iterationId):
        db = DatabaseConnection()
        query = "SELECT * FROM ITERATION WHERE iteration_id = %s"
        data = (iterationId, )
        return db.executeSQL(query, data, True)

    def selectIterationByDate(self, day, month, year):
        db = DatabaseConnection()
        queryDate = (datetime(year, month, day),)
        day += 1
        queryDate1 = (datetime(year, month, day),)
        query = "SELECT * FROM ITERATION WHERE start_date <= %s AND end_date >= %s"
        data = (queryDate, queryDate1)
        return db.executeSQL(query, data, True)

    def insert(self, iteration):
        db = DatabaseConnection()
        query = """INSERT INTO ITERATION (iteration_id, start_date, end_date, planning, iteration_name) 
        Values(%s, %s, %s, %s, %s)"""
        data = (iteration.iterationId, iteration.startDate, iteration.endDate,
                iteration.planning, iteration.iterationName)
        db.executeSQL(query, data, False)
