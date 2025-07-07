import React, { useState, useEffect } from "react";

function LiveMetrics() {
  // States for metrics
  const [cpuUsage, setCpuUsage] = useState(0);
  const [memoryInfo, setMemoryInfo] = useState(0);
  const [diskInfo, setDiskInfo] = useState(0);

  useEffect(() => {
  const fetchMetrics = () => {
    fetch("http://localhost:8000/metrics")
      .then((response) => response.json())
      .then((data) => {
        setCpuUsage(data.cpu_usage);
        setMemoryInfo(data.memory_info);
        setDiskInfo(data.disk_info);
      })
      .catch((error) => console.error("Error fetching metrics:", error));
  };

  fetchMetrics(); // fetch immediately first

  const interval = setInterval(fetchMetrics, 5000); // fetch every 5 seconds

  return () => clearInterval(interval); // cleanup when component unmounts
}, []);
      

  return (
    <div>
      <h3>Live System Metrics</h3>
      <p>CPU Usage: {cpuUsage}%</p>
      <p>Memory Usage: {memoryInfo}%</p>
      <p>Disk Usage: {diskInfo}%</p>
    </div>
  );
}

export default LiveMetrics;
