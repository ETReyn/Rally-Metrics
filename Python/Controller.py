# from TeamVelocity import getHistoricVelocity
from UserVelocity import UserVelocity

from flask import Flask


app = Flask(__name__)


@app.route('/')
def hello():
    return 'Hello, World again!'


@app.route('/velocity/team')
def teamVelocity():
    userVelocity = UserVelocity()
    return userVelocity.getUserVelocity("Ethan Reynolds")


userVelocity = UserVelocity()
print(userVelocity.getDistinctUsers())
