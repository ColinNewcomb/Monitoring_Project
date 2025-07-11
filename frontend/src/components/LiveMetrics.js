import React, { useState, useEffect } from "react";
import "./LiveMetrics.css";

function LiveMetrics() {
  const [cpuUsage, setCpuUsage] = useState(0);
  const [memoryInfo, setMemoryInfo] = useState(0);
  const [diskInfo, setDiskInfo] = useState(0);
  const [Anomaly, setAnomaly] = useState(false);
  const [anomaly_cause, setAnomalyCause] = useState(null);
  const [anomaly_deviation, setAnomalyDeviation] = useState(null);
  const [meanCpu, setMeanCpu] = useState(0);
  const [meanMemory, setMeanMemory] = useState(0);
  const [meanDisk, setMeanDisk] = useState(0);

  useEffect(() => {
    const fetchMetrics = () => {
      fetch("http://localhost:8000/metrics")
        .then((response) => response.json())
        .then((data) => {
          setCpuUsage(data.cpu_usage);
          setMemoryInfo(data.memory_info);
          setDiskInfo(data.disk_info);
          setAnomaly(data.anomaly);
          setAnomalyCause(data.anomaly_cause);
          setAnomalyDeviation(data.anomaly_deviation);
          setMeanCpu(data.mean_cpu_usage);
          setMeanMemory(data.mean_memory_info);
          setMeanDisk(data.mean_disk_info);
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
    <h3 className="live-metrics-header">Live System Metrics</h3>
    <div className="metrics-columns">
      <div className="metrics-left">
        <p className={Anomaly && anomaly_cause === "cpu_usage" ? "anomaly-highlight" : ""}>
          CPU Usage: {cpuUsage.toFixed(2)}%
        </p>
        <p className={Anomaly && anomaly_cause === "memory_info" ? "anomaly-highlight" : ""}>
          Memory Usage: {memoryInfo.toFixed(2)}%
        </p>
        <p className={Anomaly && anomaly_cause === "disk_info" ? "anomaly-highlight" : ""}>
          Disk Usage: {diskInfo.toFixed(2)}%
        </p>
      </div>
      <div className="metrics-right">
        <p>CPU Mean: {meanCpu.toFixed(2)}%</p>
        <p>Memory Mean: {meanMemory.toFixed(2)}%</p>
        <p>Disk Mean: {meanDisk.toFixed(2)}%</p>
      </div>
    </div>
    <p className={`anomaly-status ${Anomaly ? "anomaly-detected" : ""}`}>
      {Anomaly ? "Anomaly Detected!" : "Everything is normal."}
    </p>
  </div>
);
}

export default LiveMetrics;