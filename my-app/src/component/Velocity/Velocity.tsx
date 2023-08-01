import { useEffect, useState } from "react"
import { velocity, handleData } from "../../interfaces/interface"
import { UserVelocity } from "../Bar"
import { getRecentIteration, getVelocityData } from "../../api/api"
import { useNavigate } from "react-router-dom"



export function Velocity() {
    const navigate = useNavigate()
    const v: velocity = {
        id: 0,
        velocity: 0,
        capacity: 0
      }

    const [data, setData] = useState<velocity[]>([v])
    const [recentIteration, setRecentIteration] = useState<string>('')

    function handleVelocity() {
        getVelocityData().then(json => setData(
            json.filter((d: { velocity: number, capacity: number, id: string }) => {
                return d.capacity > 0
        })));
  }
    function handleHistory() {
        navigate("/history");
    }

    function handleBreakdown() {

        navigate(`/breakdown/${recentIteration}`);
    }
    function handleRecentIteration() {
        getRecentIteration().then(json => setRecentIteration(json));
      }

    useEffect(() => {
        handleVelocity()   
        handleRecentIteration()
        }, [])

    return (
        <div className="App ">
            <div>
                <button onClick={ handleHistory }>Get Historic Data</button>
                <button onClick={ handleBreakdown }>Get Most Recent Iteration Dataa</button>
            </div>    
            <div className="screenFiller">
                <UserVelocity 
                id={data.map(d => d.id)}
                velocity={data.map(d => d.velocity)}
                capacity={data.map(d => d.capacity)}
            />
        </div>
      </div>
    )
    
}
