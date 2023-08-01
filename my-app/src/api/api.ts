

export function getVelocityData() {
    return fetch('http://127.0.0.1:8000/velocity/users', {
        method: 'GET',
        headers: {
            accept: 'application/json',
        },
        }).then(resp => resp.json())
}

export function getBreakdownData(id?:string) {
    return fetch(`http://127.0.0.1:8000/breakdown/${id}`, {
        method: 'GET',
        headers: {
          accept: 'application/json',
        },
      }).then(resp => resp.json())
}

export function getHistoricalData() {
    return fetch(`http://127.0.0.1:8000/breakdown`, {
        method: 'GET',
        headers: {
          accept: 'application/json',
        },
      }).then(resp => resp.json())
}

export function getRecentIteration() {
    return fetch(`http://127.0.0.1:8000/iteration/recent`, {
        method: 'GET',
        headers: {
          accept: 'application/json',
        },
      }).then(resp => resp.json())
}