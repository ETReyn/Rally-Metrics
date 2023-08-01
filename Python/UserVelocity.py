from UserDAO import UserDAO
from IterationDAO import IterationDAO
from UserMining import UserMining


class UserVelocity:
    def getUserVelocity(self, user):
        iterationDAO = IterationDAO()
        iterationList = list(zip(*iterationDAO.selectAllIgnorePlanning()))[0]
        userDAO = UserDAO()
        iterationsByUser = userDAO.selectAllById(user, iterationList)
        totalPoints = 0
        totalIterations = 1
        for iteration in iterationsByUser:
            totalPoints += iteration[2]
            if iteration[2] > 0:
                totalIterations += 1
        velocity = totalPoints / totalIterations
        return velocity

    def getDistinctUsers(self):
        userDAO = UserDAO()
        allUsers = userDAO.getDistinctUsers()
        userDictionaryList = []
        for user in allUsers:
            dict = {"name": user[0], "id": user[1]}
            userDictionaryList.append(dict)
        return userDictionaryList

    def getAllVelocities(self):
        userDAO = UserDAO()
        allUsers = userDAO.getDistinctUsers()
        userDictionaryList = []
        for user in allUsers:
            userData = self.getUserVelocity(user[1])
            userCapacity = userDAO.selectCapacityById(user[1])
            capacity = 0
            if userCapacity:
                capacity = userCapacity[0][1]
            dict = {
                "id": user[1],
                "name": user[0],
                "velocity": userData,
                "capacity": capacity,
            }
            userDictionaryList.append(dict)
        return userDictionaryList

    def getAllNewVelocities(self):
        userMining = UserMining()
        userDAO = UserDAO()
        allUsers = userDAO.getDistinctUsers()
        userDictionaryList = []
        for user in allUsers:
            userIterations = userMining.selectAllByUser(user[0])
            velocity = 0
            numPlanningSprints = 0
            for iteration in userIterations:
                if "PLAN" in iteration[2]:
                    numPlanningSprints += 1
                else:
                    velocity += iteration[4]
            if len(userIterations) > 0:
                velocity = velocity / (len(userIterations) - numPlanningSprints)
            dict = {"id": user[1], "name": user[0], "velocity": velocity}
            userDictionaryList.append(dict)
        return userDictionaryList


userVelocity = UserVelocity()
userVelocity.getAllVelocities()
