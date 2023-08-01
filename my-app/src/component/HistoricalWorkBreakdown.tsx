import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend,
    Chart,
} from 'chart.js';
import { MouseEventHandler, useEffect, useState } from 'react';
import { Line, Bar } from 'react-chartjs-2';
import { handleBreakdown } from '../App';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

interface handleData {
    setData3(data:any): any,
    setVel(val:boolean):any,
    setHistoric(val:boolean):any,
    setBreakdown(val:boolean):any,
  }


interface graphInterface {
    iteration: string,
    totalStories: number
}
interface allGraphData {
    iteration: string[],
    enhancements: number[],
    security: number[],
    feature: number[],
    defect: number[],
    stabilization: number[],
    setIterationId(val:string): void,
    newData:handleData,
}

export function HistoricalWorkBreakdown(d: allGraphData) {
    console.log(d.iteration);
    const total = d.defect.map((x, index) => {
        return x + d.enhancements[index] + d.feature[index] + d.security[index] + d.stabilization[index];
    })

    const data = {
        labels: d.iteration,
        datasets: [
            {
                stack: "stack1",
                label: 'ENHANCEMENT',
                data: d.enhancements,
                // you can set indiviual colors for each bar
                backgroundColor: [
                    'rgba(201, 203, 207, 0.2)'
                ],
                borderColor: [
                    'rgb(201, 203, 207)'
                ],
                borderWidth: 2,
            },
            {
                stack: "stack1",
                label: 'SECURITY',
                data: d.security,
                backgroundColor: [
                    'rgba(255, 205, 86, 0.2)'
                ],
                borderColor: [
                    'rgb(255, 205, 86)'
                ],
                borderWidth: 2,
            },
            {
                stack: "stack1",
                label: 'STABILIZATION',
                data: d.stabilization,
                // you can set indiviual colors for each bar
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgb(75, 192, 192)'
                ],
                borderWidth: 2,
            },
            {
                stack: "stack1",
                label: 'DEFECT',
                data: d.defect,
                // you can set indiviual colors for each bar
                backgroundColor: [
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgb(54, 162, 235)'
                ],
                borderWidth: 2,
            },
            {
                stack: "stack1",
                label: 'FEATURE',
                data: d.feature,
                // you can set indiviual colors for each bar
                backgroundColor: [
                    'rgba(255, 159, 64, 0.2)'
                ],
                borderColor: [
                    'rgb(255, 159, 64)'
                ],
                borderWidth: 2,
            },
            // {
            //     stack: "stack2",
            //     label: 'TOTAL',
            //     data: total,
            //     // you can set indiviual colors for each bar
            //     backgroundColor: [
            //         'rgba(255, 99, 132, 0.2)'
            //     ],
            //     borderColor: [
            //         'rgb(255, 99, 132)'
            //     ],
            //     borderWidth: 1,
            // }
        ]
    };

    return <Bar 
    data={data} 
    options={{
        onClick: function(evt, element) {
          if(element.length > 0)
          {
            var ind = element[0].index;
            // if(confirm('Do you want to remove this point?')){
            //   data.datasets[0].data.splice(ind, 1);
            //   data.labels.splice(ind, 1);
            //   }
            console.log(d.iteration[ind])
            d.setIterationId(d.iteration[ind])
            handleBreakdown(d.newData, d.iteration[ind])
            }
        }
        }}  />;
};