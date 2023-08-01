import { useEffect, useState } from "react";
import { dataInterface } from "../../interfaces/interface";
import { getHistoricalData, getRecentIteration } from "../../api/api";
import { useNavigate } from "react-router-dom";
import { HistoricalWorkBreakdown } from "../HistoricalWorkBreakdown";

export function HistoricalData() {
    const navigate = useNavigate()
    const c: dataInterface = {
        iteration: '',
        storyType: '',
        totalStories: 0,
        totalPoints: 0,
        iterationId:'',
      }


    const [recentIteration, setRecentIteration] = useState<string>('')
    const [data1, setData1] = useState<dataInterface[]>([c]);
    const [enhancement, setEnhancement] = useState<number[]>([])
    const [security, setSecurity] = useState<number[]>([])
    const [stabilization, setStabilization] = useState<number[]>([])
    const [feature, setFeature] = useState<number[]>([])
    const [defect, setDefect] = useState<number[]>([])
    const [iteration, setIteration] = useState<string[]>([])
    const [iterationId, setIterationId] = useState<string[]>([])


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
        let iterId: string[] = [];
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
            iterId.push(d.iterationId)
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
        setIterationId(uniq(iterId));

        }, [data1])


    function handleHistoricClick() {
        getHistoricalData().then(json => setData1(json));
    }

    function handleRecentIteration() {
        getRecentIteration().then(json => setRecentIteration(json));
      }

    useEffect(() => {
        handleHistoricClick()
        handleRecentIteration()
    }, [])

    const handleVelocityClick = () => {
        navigate("/velocity");
      }
    
     const handleBreakdownClick = () => {
        navigate(`/breakdown/${recentIteration}`);
    }

    return (
        <div className="App">
            <div>
                <button onClick={ handleVelocityClick }>Get Velocity Data</button>
                <button onClick={ handleBreakdownClick }>Get Most Recent Iteration Data</button>
            </div>    
        <div className="screenFiller">
            <HistoricalWorkBreakdown
            enhancements={enhancement}
            security={security}
            stabilization={stabilization}
            defect={defect}
            feature={feature}
            iteration={iteration}
            iterationId={iterationId}
            />
        </div>
      </div>
    )
}