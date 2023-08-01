import { useEffect, useState } from "react";
import { breakdownInterface } from "../../interfaces/interface";
import { getBreakdownData, getRecentIteration } from "../../api/api";
import { HistoricalWorkBreakdown } from "../HistoricalWorkBreakdown";
import { WorkBreakdownByIteration } from "../WorkBreakdown";
import { useNavigate, useParams } from "react-router-dom";


export function BreakdownData() {

    const navigate = useNavigate();
    const [recentIteration, setRecentIteration] = useState<string>('')
    const id = useParams().id;
    const g: breakdownInterface = {
        storyType: 'string',
        totalStories: 0,
        totalPoints: 0,
        iterationName:'',
      }

    const [data2, setData2] = useState<breakdownInterface[]>([g]);
    const [x, setX] = useState<string[]>([])
    const [y, setY] = useState<number[]>([])
    const [y1, setY1] = useState<number[]>([])
    const [iterationName, setIterationName] = useState<string>('Getting iteration data...')

  
    let arr1: number[] = [];
    let arr3: number[] = [];
    let arr2: string[] = [];
  
    function handleHistory() {
        getBreakdownData(id).then(json => setData2(json));
      }
    function handleRecentIteration() {
      getRecentIteration().then(json => setRecentIteration(json));
    }

    useEffect(() => {
        handleHistory()
        handleRecentIteration()
    }, [])  
  
    useEffect(() => {
      data2.map(d => {
        arr1.push(d.totalStories);
        arr3.push(d.totalPoints);
        arr2.push(d.storyType)
      })
      setY(arr1);
      setX(arr2);
      setY1(arr3);
      setIterationName("Iteration data for "+data2[0].iterationName)
    }, [data2])

    const handleVelocityClick = () => {
        navigate("/velocity");
      }
    
     const handleBreakdownClick = () => {
        navigate("/history");
    }

    return (
      <div className="App">
        <div>
          <button onClick={ handleVelocityClick }>Get Velocity Data</button>
          <button onClick={ handleBreakdownClick }>Get History Data</button>
        </div>  
          
        <div>
          {iterationName}
        </div>

        <div className="screenFiller">
          <WorkBreakdownByIteration
            storyType={x}
            totalPoints={y1}
            totalStories={y} />
       </div>

      </div>
    )

}