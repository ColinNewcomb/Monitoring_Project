import React from "react";
import "./App.css";
import AnomalyStatus from "./components/AnomalyStatus";
import LiveMetrics from "./components/LiveMetrics";

function App() {
  return (
    <div className="App">
      <h1>Monitoring Dashboard</h1>
      <AnomalyStatus />
      <LiveMetrics />
      {/* You can add more components here as needed */}
      {/* Add more components later */}
    </div>
  );
}

export default App;