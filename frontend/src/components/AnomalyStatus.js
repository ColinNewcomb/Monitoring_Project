import react, {useState, useEffect } from "react";

function AnomalyStatus() {
    const [anomaly, setAnomaly] = useState(false);

    useEffect(() => {
        fetch("http://localhost:8000/anomaly")
        .then((response) => response.json())
        .then((data) => {
            setAnomaly(data.is_anomaly);
        })
        .catch((error) => {
            console.error("Error fetching anomaly status:", error);
        });
    }, []);

    return (
        <div>
            {anomaly ? (
        <h2 style={{ color: "red" }}>🚨 Anomaly Detected!</h2>
      ) : (
        <h2 style={{ color: "green" }}>✅ System Normal</h2>
      )}
          
        </div>
    );
}
export default AnomalyStatus;