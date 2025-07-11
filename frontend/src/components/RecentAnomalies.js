import React, { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./RecentAnomalies.css";

function RecentAnomalies() {
  const [anomalies, setAnomalies] = useState([]);

  useEffect(() => {
    const fetchAnomalies = () => {
      fetch("http://localhost:8000/recent_anomalies")
        .then((response) => response.json())
        .then((data) => {
          const anomaliesArray = data.anomaly || [];
          setAnomalies(anomaliesArray);
        })
        .catch((error) => console.error("Error fetching anomalies:", error));
    };

    fetchAnomalies();
    const interval = setInterval(fetchAnomalies, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="recent-anomalies">
      <h3>Recent Anomalies</h3>
      <AnimatePresence>
        {anomalies.length > 0 ? (
          <ul>
            {anomalies.map((anomaly, index) => (
              <motion.li
                key={index}
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: 10 }}
              >
                Time: {new Date(anomaly.time_stamp).toLocaleTimeString()} — CPU: {anomaly.cpu_usage}% — Memory: {anomaly.memory_info}% — Disk: {anomaly.disk_info}%
              </motion.li>
            ))}
          </ul>
        ) : (
          <p>No recent anomalies found.</p>
        )}
      </AnimatePresence>
    </div>
  );
}

export default RecentAnomalies;
