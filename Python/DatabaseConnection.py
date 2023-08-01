import psycopg2


class DatabaseConnection:
    def __init__(self):
        self.conn = psycopg2.connect(
            database="postgres",
            user="myuser",
            password="",
            host="localhost",
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
            return output
        self.conn.commit()

    def setUp(self):
        query = """
            DROP TABLE IF EXISTS iteration_incomplete;
            DROP TABLE IF EXISTS iteration_complete;
            DROP TABLE IF EXISTS users;
            DROP TABLE IF EXISTS iteration;
        """
        self.executeSQL(query, None, False)
        query = """CREATE TABLE iteration (
            iteration_id BIGINT PRIMARY KEY,
            iteration_name VARCHAR ( 50 ) UNIQUE NOT NULL,
            start_date DATE NOT NULL,
            end_date DATE NOT NULL,
            planning BOOLEAN NOT NULL
            );
            """
        self.executeSQL(query, None, False)
        query = """CREATE TABLE users (
                user_id BIGINT NOT NULL,
                iteration_id BIGINT NOT NULL,
                total_points INTEGER NOT NULL,
                zero_points INTEGER NOT NULL,
                one_point INTEGER NOT NULL,
                two_points INTEGER NOT NULL,
                three_points INTEGER NOT NULL,
                five_points INTEGER NOT NULL,
                eight_points INTEGER NOT NULL,
                thirteen_points INTEGER NOT NULL,
                name VARCHAR(50) NOT NULL,

                PRIMARY KEY (user_id, iteration_id),
                FOREIGN KEY (iteration_id)
                REFERENCES iteration (iteration_id)
            );"""
        self.executeSQL(query, None, False)
        query = """
            CREATE TABLE iteration_complete (
                iteration_id BIGINT NOT NULL,
                total_stories INTEGER NOT NULL,
                total_points INTEGER NOT NULL,
                zero_points INTEGER NOT NULL,
                one_point INTEGER NOT NULL,
                two_points INTEGER NOT NULL,
                three_points INTEGER NOT NULL,
                five_points INTEGER NOT NULL,
                eight_points INTEGER NOT NULL,
                thirteen_points INTEGER NOT NULL,
                story_type VARCHAR(50) NOT NULL,

                PRIMARY KEY (iteration_id, story_type),
                FOREIGN KEY (iteration_id)
                REFERENCES iteration (iteration_id)
            );"""
        self.executeSQL(query, None, False)
        query = """
            CREATE TABLE iteration_incomplete (
                iteration_id BIGINT NOT NULL,
                defined INTEGER NOT NULL,
                in_progress INTEGER NOT NULL,
                failed_ac INTEGER NOT NULL,
                in_test INTEGER NOT NULL,
                code_review INTEGER NOT NULL,
                pending_environment INTEGER NOT NULL,
                ready_for_test INTEGER NOT NULL,
                story_type VARCHAR(50) NOT NULL,
                total_stories INTEGER NOT NULL,
                total_points INTEGER NOT NULL,
                zero_points INTEGER NOT NULL,
                one_point INTEGER NOT NULL,
                two_points INTEGER NOT NULL,
                three_points INTEGER NOT NULL,
                five_points INTEGER NOT NULL,
                eight_points INTEGER NOT NULL,
                thirteen_points INTEGER NOT NULL,

                PRIMARY KEY (iteration_id, story_type),
                FOREIGN KEY (iteration_id)
                REFERENCES iteration (iteration_id)
            );"""
        self.executeSQL(query, None, False)


# DB = DatabaseConnection()
# DB.setUp()
# DB.close()
# query = "Select * from Iteration_Complete"

# allData = DB.executeSQL(query, None, True)
# for data in allData:
#     print(data)
