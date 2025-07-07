import React from "react";
import "./App.css";
import AnomalyStatus from "./components/AnomalyStatus";
import LiveMetrics from "./components/LiveMetrics";
import DownloadButton from "./components/DownloadButton";
import DownloadAnomalyHistory from "./components/DownloadAnomalyHistory";
import LiveChart from "./components/LiveChart";
import RecentAnomalies from "./components/RecentAnomalies";

function App() {
  return (
    <div className="App">
      <h1>Monitoring Dashboard</h1>
      <AnomalyStatus />
      <LiveMetrics />
      <DownloadButton />
      <DownloadAnomalyHistory />
      <LiveChart />
      <RecentAnomalies />
      
      {/* DownloadButton component can be added here if needed */}
      {/* <DownloadButton /> */}
      {/* Add more components as needed */}
      {/* You can add more components here as needed */}
      {/* Add more components later */}
      {/* You can add more components here as needed */}
      {/* Add more components later */}
    </div>
  );
}

export default App;