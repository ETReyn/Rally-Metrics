

interface interface1 {
    storyType: string,
    totalStories: number
    totalPoints: number
}

interface interface2 {
    iteration: string,
    totalStories: number
}

export interface velocity {
    id: number,
    velocity: number,
    capacity: number
}


export interface dataInterface {
    storyType: string,
    totalStories: number,
    totalPoints: number,
    iteration: string,
    iterationId:string,
}


export interface breakdownInterface {
    storyType: string,
    totalStories: number,
    totalPoints: number,
    iterationName:string,
  }
  
  export interface graphInterface {
    iteration: string,
    totalStories: number
  }
  
  
  
  export interface dataInterface {
    storyType: string,
    totalStories: number,
    totalPoints: number,
    iteration: string
  }
  
  export interface handleData {
    setData3(data:any): any,
    setVel(val:boolean):any,
    setHistoric(val:boolean):any,
    setBreakdown(val:boolean):any,
  }