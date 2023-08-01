import React from 'react';
import {
  BrowserRouter, Routes, Route,
} from 'react-router-dom';
import Data from './Data';
import { Velocity } from './component/Velocity/Velocity';
import { BreakdownData } from './component/Breakdown/Breakdown';
import { HistoricalData } from './component/History/History';

function App() {
  return(
    <div className='App'>
      <h1>
        Rally Metric Tracker
      </h1>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Data />} />
          <Route path="/velocity" element={<Velocity />} />
          <Route path="/breakdown/:id" element={<BreakdownData />} />
          <Route path="/history" element={<HistoricalData />} />
        </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App;
