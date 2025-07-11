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
      <LiveChart />
      <LiveMetrics />
      <RecentAnomalies />
      <DownloadButton />
      <DownloadAnomalyHistory />
    </div>
  );
}

export default App;
