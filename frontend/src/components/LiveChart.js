import { Line } from "react-chartjs-2";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement,
    Title, Tooltip, Legend } from "chart.js";
import { useState, useEffect } from "react";

ChartJS.register(
    CategoryScale,
    LinearScale,
    PointElement,
    LineElement,
    Title,
    Tooltip,
    Legend
);

function LiveChart() {
    const [chartData, setChartData] = useState({
        labels: [],
        datasets: [
            {
                label: "CPU Usage",
                data: [],
                borderColor: "rgba(75,192,192,1)",
                fill: false,
                pointRadius: 5,
                pointHoverRadius: 7,
            },
            {
                label: "Memory Usage",
                data: [],
                borderColor: "rgba(153,102,255,1)",
                fill: false,
                pointRadius: 5,
                pointHoverRadius: 7,
            },
            {
                label: "Disk Usage",
                data: [],
                borderColor: "rgba(255,159,64,1)",
                fill: false,
                pointRadius: 5,
                pointHoverRadius: 7,
            },
        ],
    });

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response = await fetch("http://localhost:8000/metrics");
                const data = await response.json();
                
                const labels = data.map(item => new Date(item.time_stamp).toLocaleString());
                const cpuData = data.map(item => item.cpu_usage);
                const memoryData = data.map(item => item.memory_info);
                const diskData = data.map(item => item.disk_info);

                    setChartData({
                        labels,
                        datasets: [
                            { ...chartData.datasets[0], 
                                data: cpuData,
                                pointRadius: 5,
                                pointHoverRadius: 7,
                            },
                            { ...chartData.datasets[1], 
                                data: memoryData,
                                pointRadius: 5,
                                pointHoverRadius: 7,
                            },
                            { ...chartData.datasets[2],
                                data: diskData,
                                pointRadius: 5,
                                pointHoverRadius: 7,
                            },
                        ],
                    });
            } catch (error) {
                console.error("Error fetching Live data:", error);
            }
        };

        fetchData();
    }, []);

    return (
    <div>
        <h2>System Metrics</h2>
        <Line
        data={chartData}
        options={{
            elements: {
            point: {
                radius: 5,
                hoverRadius: 7,
            },
            },
            responsive: true,
            plugins: {
                legend: {
                    display: true,
                    position: "top",
                },
                title: {
                    display: true,
                    text: "Live System Metrics",
                },
            },
        }}
        />
    </div>
    );
}

export default LiveChart;