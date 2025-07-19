import { useState, useEffect, useRef } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler } from "chart.js";
import "./LiveChart.css";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend, Filler);

function LiveChart() {
  const [chartData, setChartData] = useState({
    labels: [],
    datasets: [
      { label: "CPU Usage", data: [], borderColor: "rgba(75,192,192,1)", backgroundColor: "rgba(75,192,192,0.2)", fill: true },
      { label: "Memory Usage", data: [], borderColor: "rgba(153,102,255,1)", backgroundColor: "rgba(153,102,255,0.2)", fill: true },
      { label: "Disk Usage", data: [], borderColor: "rgba(255,159,64,1)", backgroundColor: "rgba(255,159,64,0.2)", fill: true },
    ],
  });

  const intervalRef = useRef(null);

  useEffect(() => {
    intervalRef.current = setInterval(() => {
      fetch("http://localhost:8000/metrics")
        .then((response) => response.json())
        .then((data) => {
          const currentTime = new Date().toLocaleTimeString();
          setChartData((prevData) => ({
            labels: [...prevData.labels, currentTime].slice(-10),
            datasets: prevData.datasets.map((dataset, index) => ({
              ...dataset,
              data: [...dataset.data, data[Object.keys(data)[index]]].slice(-10),
            })),
          }));
        })
        .catch((error) => console.error("Error fetching metrics:", error));
    }, 5000);

    return () => clearInterval(intervalRef.current);
  }, []);

  return (
    <div className="chart-container">
      <h3>System Metrics Over Time</h3>
      <Line data={chartData} options={{ responsive: true, plugins: { legend: { position: "top" }, title: { display: false } } }} />
    </div>
  );
}

export default LiveChart;
