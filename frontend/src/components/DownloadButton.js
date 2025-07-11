import React from 'react';

function DownloadButton() {
    const handleDownload = async () => {
        try {
            const response = await fetch('http://localhost:8000/download');
            const data = await response.json();
            const jsonStr = JSON.stringify(data, null, 2); 
            const blob = new Blob([jsonStr], { type: 'application/json' });
            const url = URL.createObjectURL(blob);

            const link = document.createElement('a');
            link.href = url;
            link.download = 'system_metrics.json';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            URL.revokeObjectURL(url);
        } catch (error) {
            console.error('Error downloading data:', error);
        }
    };

    return (
        <div className ="button-group">
            <button onClick={handleDownload}>
                Download Metrics History
            </button>
        </div>
    );
}

export default DownloadButton;
