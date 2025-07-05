import React from "react";
import "./App.css";
import AnomalyStatus from "./components/AnomalyStatus";

function App() {
  return (
    <div className="App">
      <h1>Monitoring Dashboard</h1>
      <AnomalyStatus />
      {/* Add more components later */}
    </div>
  );
}

export default App;