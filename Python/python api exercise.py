from User import User
from UserDAO import UserDAO
from Iteration import Iteration
from IterationDAO import IterationDAO

it = Iteration(-1, "name", "2023-01-01", "2023-02-01", False)
itdao = IterationDAO()
itdao.insert(it)
user = User(-1, "test", -1, 0, 6, 1, 2, 3, 5, 8, 13)
userdao = UserDAO()
userdao.insert(user)
print(userdao.selectAll())
