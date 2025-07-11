import React from 'react';

function DownloadAnomalyHistory() {
    const handleDownload = async () => {
        try {
            const response = await fetch('http://localhost:8000/anomalies/history');
            const data = await response.json();
            const jsonStr = JSON.stringify(data, null, 2); // Convert data to JSON string with indentation
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = 'anomaly_history.json'; // Name of the downloaded file
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url); // Clean up the URL object
            } catch (error) {
                console.error('Error downloading anomaly history:', error);
            }
        };

        return (
            <div>
                <button onClick={handleDownload}>
                    Download Anomaly History
                </button>
            </div>
        );
    }

    export default DownloadAnomalyHistory;