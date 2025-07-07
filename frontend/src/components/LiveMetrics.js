import React, { useState, useEffect } from "react";

function LiveMetrics() {
  // States for metrics
  const [cpuUsage, setCpuUsage] = useState(0);
  const [memoryInfo, setMemoryInfo] = useState(0);
  const [diskInfo, setDiskInfo] = useState(0);

  useEffect(() => {
    // Function to fetch metrics
    const fetchMetrics = () => {
      fetch("http://localhost:8000/metrics")
        .then((response) => response.json())
        .then((data) => {
          console.log("Metrics fetched successfully:", data);
          setCpuUsage(data.cpu_usage);
          setMemoryInfo(data.memory_info);
          setDiskInfo(data.disk_info);
        })
        .catch((error) => console.error("Error fetching metrics:", error));
    };

    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);

    return () => clearInterval(interval); // Cleanup interval on component unmount
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
