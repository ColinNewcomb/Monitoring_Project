import React, { use, useEffect, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import "./RecentAnomalies.css";


function RecentAnomalies() {
    const [anomalies, setAnomalies] = useState([]);

    useEffect(() => {
        // Function to fetch recent anomalies
        const fetchRecentAnomalies = () => {
            fetch("http://localhost:8000/recent_anomalies")
                .then((response) => response.json())
                .then((data) => {
                    console.log("Recent anomalies fetched successfully:", data);
                    setAnomalies(data);
                })
                .catch((error) => console.error("Error fetching recent anomalies:", error));
        };

        fetchRecentAnomalies();
        const interval = setInterval(fetchRecentAnomalies, 5000); // Fetch every 5 seconds
        return () => clearInterval(interval); // Cleanup interval on component unmount
    }, []);

    return (
        <div className = "recent-anomalies">
            <h3>Recent Anomalies</h3>
        </div>
    );
}

export default RecentAnomalies;