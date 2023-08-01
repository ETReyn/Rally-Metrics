class Iteration:
    def __init__(self, iterationId, iterationName, startDate, endDate, planning):
        self.iterationId = iterationId
        self.iterationName = iterationName
        self.startDate = startDate
        self.endDate = endDate
        self.planning = planning

    def __str__(self) -> str:
        return f"Iteration Id:{self.iterationId}Iteration Name:{self.iterationName}"
