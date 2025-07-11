import React from "react";
import "./App.css";
import LiveMetrics from "./components/LiveMetrics";
import LiveChart from "./components/LiveChart";
import RecentAnomalies from "./components/RecentAnomalies";
import DownloadButton from "./components/DownloadButton";
import DownloadAnomalyHistory from "./components/DownloadAnomalyHistory";

function App() {
  return (
    <div className="dashboard">
      <h1>Monitoring Dashboard</h1>
      <div className="main-content">
        <div className="left-panel">
          <LiveMetrics />
          <div className="button-container">
            <DownloadButton />
            <DownloadAnomalyHistory />
          </div>
        </div>
        <div className="center-panel">
          <LiveChart />
        </div>
        <div className="right-panel">
          <RecentAnomalies />
        </div>
      </div>
    </div>
  );
}

export default App;
