from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from UserVelocity import UserVelocity
from TeamVelocity import TeamVelocity
from WorkBreakdown import WorkBreakdown
from IterationData import IterationData

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/users")
async def distinctUsers():
    userVelocity = UserVelocity()
    return {"users": userVelocity.getDistinctUsers()}


@app.get("/velocity/users/{userId}")
async def userVelocity(userId):
    userVelocity = UserVelocity()
    return {"velocity": userVelocity.getUserVelocity(userId)}


@app.get("/velocity/users")
async def allUserVelocities():
    userVelocity = UserVelocity()
    return userVelocity.getAllVelocities()


@app.get("/velocity/user/new")
async def allUserVelocities():
    userVelocity = UserVelocity()
    return userVelocity.getAllNewVelocities()


@app.get("/velocity/team")
async def teamVelocity():
    teamVelocity = TeamVelocity()
    return teamVelocity.getHistoricVelocity()


@app.get("/breakdown/{iterationId}")
async def workBreakdown(iterationId):
    workBreakdown = WorkBreakdown()
    return workBreakdown.getWorkBreakdown(iterationId)


@app.get("/breakdown")
async def getHistoricWorkBreakdown():
    workBreakdown = WorkBreakdown()
    return workBreakdown.getHistoricalWorkBreakdown()


@app.get("/iteration/{iterationId}")
async def getHistoricWorkBreakdown(iterationId):
    iterationData = IterationData()
    return iterationData.getIteration(iterationId)

@app.get("/iteration/recent")
async def getHistoricWorkBreakdown(iterationId):
    iterationData = IterationData()
    return iterationData.getIteration(iterationId)
