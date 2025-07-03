from monitor import Monitor
from anomaly_detector import AnomalyDetector
import time
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

app = FastAPI()
monitor = Monitor()
anomaly_detector = AnomalyDetector()
last_train_time = 0


@app.get("/metrics", response_class=PlainTextResponse)
def metrics():
    global last_train_time
    
    #Current System Metrics
    monitor.collect_metrics()
    current_time = time.time()
    
    #Checks ML Data
    if len(monitor.metrics) >= monitor.window_size:
        if not anomaly_detector.trained:
            anomaly_detector.fit(monitor.metrics)
            last_train_time = current_time
        elif current_time - last_train_time >= 30:
            anomaly_detector.fit(monitor.metrics)
            last_train_time = current_time
        
        latest_metrics = monitor.get_latest_metrics()
        is_anomaly = anomaly_detector.predict(latest_metrics)
    
    else:
        latest_metrics = monitor.get_latest_metrics()
        is_anomaly = False
        
    # Step 3: Return Prometheus-compatible metrics
    if latest_metrics is None:
        latest_metrics = {
            "cpu_usage": 0,
            "memory_info": 0,
            "disk_info": 0,
        }

    return (
        f"cpu_usage {latest_metrics['cpu_usage']}\n"
        f"memory_usage {latest_metrics['memory_info']}\n"
        f"disk_usage {latest_metrics['disk_info']}\n"
        f"anomaly_detected {int(is_anomaly)}\n"
    )

