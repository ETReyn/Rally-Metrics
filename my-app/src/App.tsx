import React, { useRef } from 'react';
import { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip,
} from 'chart.js/auto';
import './App.css';
import { UserVelocity } from './component/Bar';
import { WorkBreakdownByIteration } from './component/WorkBreakdown';
import { HistoricalWorkBreakdown } from './component/HistoricalWorkBreakdown';
import { velocity } from './interfaces/interface';
import { ArrayDestructuringAssignment } from 'typescript';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip
);

interface breakdownInterface {
  storyType: string,
  totalStories: number,
  totalPoints: number
}

interface graphInterface {
  iteration: string,
  totalStories: number
}



interface dataInterface {
  storyType: string,
  totalStories: number,
  totalPoints: number,
  iteration: string
}

interface handleData {
  setData3(data:any): any,
  setVel(val:boolean):any,
  setHistoric(val:boolean):any,
  setBreakdown(val:boolean):any,
}



function App() {

  const [iterationId, setIterationId] = useState<string>('499934827772')

  const c: dataInterface = {
    iteration: '',
    storyType: '',
    totalStories: 0,
    totalPoints: 0,
  }
  const g: breakdownInterface = {
    storyType: 'string',
    totalStories: 0,
    totalPoints: 0
  }

  const v: velocity = {
    id: 0,
    velocity: 0,
    capacity: 0
  }

  // USER VELOCITY
  const [data, setData] = useState<velocity[]>([v])
  const [vel, setVel] = useState<boolean>(true)
  const [historic, setHistoric] = useState<boolean>(true)
  const [breakdown, setBreakdown] = useState<boolean>(true)

  // const [x, setX] = useState<number[]>(data.map(d => d.id))
  // const [y, setY] = useState<number[]>(data.map(d => d.velocity))
  // const [y1, setY1] = useState<number[]>(data.map(d => d.capacity))



  // useEffect(() => {
  //   setX(data.map(d => d.id))
  //   setY(data.map(d => d.velocity))
  //   setY1(data.map(d => d.capacity))
  // }, [data])

  // WORK BREAKDOWN BY ITERATION
  const [data2, setData2] = useState<breakdownInterface[]>([g]);
  const [x, setX] = useState<string[]>([])
  const [y, setY] = useState<number[]>([])
  const [y1, setY1] = useState<number[]>([])

  let arr1: number[] = [];
  let arr3: number[] = [];
  let arr2: string[] = [];


  useEffect(() => {

    data2.map(d => {
      arr1.push(d.totalStories);
      arr3.push(d.totalPoints);
      arr2.push(d.storyType)
    })
    setY(arr1);
    setX(arr2);
    setY1(arr3);
  }, [data2])

  // WORK BREAKDOWN BY ITERATION
  const [data1, setData1] = useState<dataInterface[]>([c]);
  const [enhancement, setEnhancement] = useState<number[]>([])
  const [security, setSecurity] = useState<number[]>([])
  const [stabilization, setStabilization] = useState<number[]>([])
  const [feature, setFeature] = useState<number[]>([])
  const [defect, setDefect] = useState<number[]>([])
  const [iteration, setIteration] = useState<string[]>([])
  const velocityData: handleData = {
    setData3: setData,
    setHistoric: setHistoric,
    setVel:setVel,
    setBreakdown:setBreakdown,
  }

  const breakdownData: handleData = {
    setData3: setData2,
    setHistoric: setHistoric,
    setVel:setVel,
    setBreakdown:setBreakdown,
  }

  const historicData: handleData = {
    setData3: setData1,
    setHistoric: setHistoric,
    setVel:setVel,
    setBreakdown:setBreakdown,
  }

  function uniq(a: string[]) {
    return Array.from(new Set(a));
  }


  useEffect(() => {
    let enh: number[] = [];
    let sec: number[] = [];
    let sta: number[] = [];
    let fea: number[] = [];
    let def: number[] = [];
    let iter: string[] = [];
    const map1 = new Map();
    data1.filter(d => {
      return !(d.iteration.includes("PLAN"))
    })
      // .filter(d => {
      //   return d.iteration.includes("2022") || d.iteration.includes("2023")
      // })
      .map(d => {
        if (d.storyType === "DEFECT") {
          def.push(d.totalStories)
        }
        if (d.storyType === "STABILIZATION") {
          sta.push(d.totalStories)
        }
        if (d.storyType === "ENHANCEMENT") {
          enh.push(d.totalStories)
        }
        if (d.storyType === "FEATURE") {
          fea.push(d.totalStories)
        }
        if (d.storyType === "SECURITY") {
          sec.push(d.totalStories)
        }
        iter.push(d.iteration)
        if (!map1.has(d.iteration)) {
          map1.set(d.iteration, 0)
        }
        const newValue = d.totalStories + map1.get(d.iteration)
        map1.set(d.iteration, newValue);
      })
    setEnhancement(enh);
    setStabilization(sta);
    setSecurity(sec);
    setDefect(def);
    setFeature(fea);
    setIteration(uniq(iter));

  }, [data1])

  return (
    <div className="App">
      Iteration Data
      <div>
        <button onClick={() => handleVelocity(velocityData)}>Get Velocity Data</button>
        <button onClick={() => handleHistoricClick(historicData)}>Get Historic Data</button>
        <button onClick={() => handleBreakdown(breakdownData, iterationId)}>Get Breakdown Data</button>
      </div>
      <div hidden={historic}>
        <HistoricalWorkBreakdown
          enhancements={enhancement}
          security={security}
          stabilization={stabilization}
          defect={defect}
          feature={feature}
          iteration={iteration}
          setIterationId={setIterationId}
          newData={breakdownData}
        />
      </div>
      <div hidden={vel}>
        <UserVelocity
          id={data.map(d => d.id)}
          velocity={data.map(d => d.velocity)}
          capacity={data.map(d => d.capacity)}
        />
      </div>
      <div hidden={breakdown}>
        <WorkBreakdownByIteration
          storyType={x}
          totalPoints={y1}
          totalStories={y} />
      </div>
    </div>
  );
}

export function handleBreakdown({setData3, setVel, setHistoric, setBreakdown}:handleData, iterationId:string) {
  fetch(`http://127.0.0.1:8000/breakdown/${iterationId}`, {
    method: 'GET',
    headers: {
      accept: 'application/json',
    },
  }).then(resp => resp.json()).then(json => setData3(json));
  setVel(true)
  setHistoric(true)
  setBreakdown(false)
}

export function handleHistoricClick({setData3, setVel, setHistoric, setBreakdown}:handleData) {
  fetch('http://127.0.0.1:8000/breakdown', {
    method: 'GET',
    headers: {
      accept: 'application/json',
    },
  }).then(resp => resp.json()).then(json => setData3(json));
  setVel(true);
  setBreakdown(true)
  setHistoric(false);
}

function handleVelocity({setData3, setVel, setHistoric, setBreakdown}:handleData) {
  fetch('http://127.0.0.1:8000/velocity/users', {
    method: 'GET',
    headers: {
      accept: 'application/json',
    },
  }).then(resp => resp.json()).then(json => setData3(json.filter((d: { velocity: number, capacity: number, id: string }) => {
    return d.capacity > 0
  })));
  setHistoric(true);
  setBreakdown(true);
  setVel(false);
}

export default App;
