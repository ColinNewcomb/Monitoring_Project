import React, { useState, useEffect } from "react";
import "./LiveMetrics.css";

function LiveMetrics() {
  const [cpuUsage, setCpuUsage] = useState(0);
  const [memoryInfo, setMemoryInfo] = useState(0);
  const [diskInfo, setDiskInfo] = useState(0);
  const [Anomaly, setAnomaly] = useState(false);

  useEffect(() => {
    const fetchMetrics = () => {
      fetch("http://localhost:8000/metrics")
        .then((response) => response.json())
        .then((data) => {
          setCpuUsage(data.cpu_usage);
          setMemoryInfo(data.memory_info);
          setDiskInfo(data.disk_info);
          setAnomaly(data.anomaly);
          if (data.anomaly) {
            console.warn("Anomaly detected!");
          }
        })
        .catch((error) => console.error("Error fetching metrics:", error));
    };
    fetchMetrics();
    const interval = setInterval(fetchMetrics, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="metrics-box">
      <h3>Live System Metrics</h3>
      <p>CPU Usage: {cpuUsage}%</p>
      <p>Memory Usage: {memoryInfo}%</p>
      <p>Disk Usage: {diskInfo}%</p>
      <p className={`anomaly-status ${Anomaly ? "anomaly-detected" : ""}`}>
        {Anomaly ? "Anomaly Detected!" : "Everything is normal."}
      </p>
    </div>
  );
}

export default LiveMetrics;