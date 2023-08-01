
import requests


def apiCall(self, callRequest, param, query):
    id = "_fvemG26dSGe9Qc55qqFCWU5CErYb6E8Bu9LmgGHJSBI"
    header = {"zsessionid": id}
    param = {
        "workspace": "https://rally1.rallydev.com/slm/webservice/v2.0/workspace/123",
        "start":  1,
        "pagesize": 5000,
        "query": query
    }
    if param == 1:
        return requests.get(callRequest, headers=header).text
    return requests.get(callRequest, headers=header, params=param).text
