from monitor import Monitor
from datetime import datetime
from anomaly_detector import AnomalyDetector
import time
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from database import init_database
from fastapi import Depends
from database import SessionLocal, SystemMetrics

init_database()  # Initialize the database
app = FastAPI()
monitor = Monitor()
anomaly_detector = AnomalyDetector()
last_train_time = 0
current_anomaly_state = False

# Dependency to get a DB session
def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()
        
@app.get("/metrics")
def metrics():
    global last_train_time
    global current_anomaly_state

    
    database = SessionLocal()

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
        current_anomaly_state = is_anomaly
        
    else:
        latest_metrics = monitor.get_latest_metrics()
        is_anomaly = current_anomaly_state
    
    if latest_metrics is None:
        latest_metrics = {
            "cpu_usage": 0,
            "memory_info": 0,
            "disk_info": 0,
            "time_stamp": "N/A"
        }
    if latest_metrics['time_stamp'] != "N/A":
        timestamp_value = datetime.fromisoformat(latest_metrics['time_stamp'])
    else:
        timestamp_value = None
    # Initialize the database
    metric_record = SystemMetrics(
        cpu_usage = latest_metrics['cpu_usage'],
        memory_info = latest_metrics['memory_info'],
        disk_info = latest_metrics['disk_info'],
        anomaly = int(current_anomaly_state),
        time_stamp = timestamp_value
    )
    
    database.add(metric_record)
    database.commit()
    database.close()
    return JSONResponse(content={
        "cpu_usage": latest_metrics['cpu_usage'],
        "memory_info": latest_metrics['memory_info'],
        "disk_info": latest_metrics['disk_info'],
        "time_stamp": latest_metrics['time_stamp'],
        "anomaly": current_anomaly_state
    })
    
@app.get("/history")
def get_history(limit: int = 50, database: SessionLocal = Depends(get_database)): # type: ignore
    """
    Retrieve the last 'limit' system metrics records from the database.
    """
    metrics = database.query(SystemMetrics).order_by(SystemMetrics.time_stamp.desc()).limit(limit).all()
    
    history = []
    for metric in metrics:
        history.append({
            "time_stamp": metric.time_stamp.isoformat(),
            "cpu_usage": metric.cpu_usage,
            "memory_info": metric.memory_info,
            "disk_info": metric.disk_info,
            "anomaly": bool(metric.anomaly)
        })
    return JSONResponse(content=history)

@app.get("/anaomaly")
def get_anomaly_state():
    """
    Get the current anomaly state.
    """
    global current_anomaly_state

    return JSONResponse(content={"anomaly": current_anomaly_state})

@app.get("/anomalies/history")
def get_anomalies_history(limit: int = 50, database: SessionLocal = Depends(get_database)):
    """
    Retrieve the last 'limit' anomaly records from the database.
    """
    anomalies = database.query(SystemMetrics).filter(SystemMetrics.anomaly == True).order_by(SystemMetrics.time_stamp.desc()).limit(limit).all()
    
    history = []
    for anomaly in anomalies:
        history.append({
            "time_stamp": anomaly.time_stamp.isoformat(),
            "cpu_usage": anomaly.cpu_usage,
            "memory_info": anomaly.memory_info,
            "disk_info": anomaly.disk_info,
            "anomaly": bool(anomaly.anomaly)
        })
    return JSONResponse(content=history)

@app.get("/download")
def download_history(database: SessionLocal = Depends(get_database)):
    """
    Download the entire history of system metrics as a JSON file.
    """
    metrics = database.query(SystemMetrics).all()
    
    history = []
    for metric in metrics:
        history.append({
            "time_stamp": metric.time_stamp.isoformat(),
            "cpu_usage": metric.cpu_usage,
            "memory_info": metric.memory_info,
            "disk_info": metric.disk_info,
            "anomaly": bool(metric.anomaly)
        })
    
    return JSONResponse(content=history)

@app.get("/status")
def get_status():
    """
    Get the current status of the monitoring system.
    """
    global current_anomaly_state
    return JSONResponse(content={
        "monitoring": True,
        "anomaly_detected": current_anomaly_state,
        "last_train_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(monitor.start_time))
    })
    
#@app.get("/config")
