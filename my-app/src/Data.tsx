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
import { NavigateFunction, useNavigate } from 'react-router-dom';

ChartJS.register(
  CategoryScale,
  LinearScale,
  BarElement,
  Title,
  Tooltip
);


function Data() {

    const navigate = useNavigate();


   const handleVelocityClick = () => {
    navigate("/velocity");
  }

 const handleHistoryClick = () => {
    navigate("/history");
  }

 const handleBreakdownClick = () => {
    navigate("/breakdown/499934827772");
 }


  return (
    <div className="App">
        <button onClick={ handleVelocityClick }>Get Velocity Data</button>
        <button onClick={ handleHistoryClick }>Get Historical Data</button>
        <button onClick={ handleBreakdownClick }>Get Most Recent Iteration Data</button>
    </div>
  );
}


export default Data;
