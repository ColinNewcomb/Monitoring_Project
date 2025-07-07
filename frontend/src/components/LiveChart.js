import { useState, useRef ,useEffect, use } from "react";
import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement,
    Title, Tooltip, Legend } from "chart.js";
import "./LiveChart.css"; // Import the CSS file for styling

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

const LiveChart = () => {
    const [chartData, setChartData] = useState({
        labels: [],
        datasets: [
            {
                label: "CPU Usage",
                data: [],
                borderColor: "rgba(75,192,192,1)",
                backgroundColor: "rgba(75,192,192,0.2)",
                fill: true,
            },
            {
                label: "Memory Usage",
                data: [],
                borderColor: "rgba(153,102,255,1)",
                backgroundColor: "rgba(153,102,255,0.2)",
                fill: true,
            },
            {
                label: "Disk Usage",
                data: [],
                borderColor: "rgba(255,159,64,1)",
                backgroundColor: "rgba(255,159,64,0.2)",
                fill: true,
            },
        ],
    });
    const chartRef = useRef(null);
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
        }, 5000); // Fetch data every 5 seconds
        
        return () => clearInterval(intervalRef.current); // Cleanup interval on component unmount
    
    }, []);

    return (
        <div className ="chart-container">
            <div className="live-chart-container">
            <h2>Live System Metrics</h2>
            <Line
                ref={chartRef}
                data={chartData}
                options={{
                    responsive: true,
                    plugins: {
                        legend: {
                            position: "top",
                        },
                        title: {
                            display: true,
                            text: "System Metrics Over Time",
                        },
                    },
                    scales: {
                        y : {
                            min: 0,
                            max: 100,
                            ticks: {
                                stepSize: 10,
                            },
                        },
                        x: {
                            min: 0,
                            max: 50,
                            ticks: {
                                autoSkip: true,
                                maxTicksLimit: 10,
                            },
                        }
                    }
                }}
            />
            </div>
        </div>
    );
}
    export default LiveChart;
    