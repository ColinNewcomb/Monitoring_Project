from monitor import Monitor
from datetime import datetime
from anomaly_detector import AnomalyDetector
import time
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from database.database import init_database
from fastapi import Depends
from database.database import SessionLocal, SystemMetrics
from fastapi.middleware.cors import CORSMiddleware
import numpy as np
import json

init_database()  # Initialize the database
app = FastAPI() # Create FastAPI app instance
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to ["http://localhost:3000"] if you want
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
monitor = Monitor() # Initialize the Monitor instance
anomaly_detector = AnomalyDetector() # Initialize the AnomalyDetector instance
last_train_time = 0 # Last time the model was trained
current_anomaly_state = False # Current anomaly state

# Dependency to get a DB session
def get_database(): 
    database = SessionLocal() # Create a new database session
    try:
        yield database # Yield the database session for use in the route
    finally:
        database.close() # Close the database session after use
 
@app.get("/metrics")
def metrics():
    global last_train_time # Last time the model was trained
    global current_anomaly_state # Current anomaly state
    database = SessionLocal() # Get a new database session
    monitor.collect_metrics() # Collect system metrics
    current_time = time.time() # Get the current time
    
    if len(monitor.metrics) >= monitor.window_size: # If enough data is collected
        if not anomaly_detector.trained: # If the model is not trained yet
            anomaly_detector.fit(monitor.metrics) # Train the model with the collected metrics
            last_train_time = current_time # Update the last training time
        elif current_time - last_train_time >= 30: # If enough time has passed since the last training
            anomaly_detector.fit(monitor.metrics) # Re-train the model with the collected metrics
            last_train_time = current_time # Update the last training time
        
        latest_metrics = monitor.get_latest_metrics() # Get the latest metrics
        is_anomaly = anomaly_detector.predict(latest_metrics) # Predict if the latest metrics are an anomaly
        current_anomaly_state = is_anomaly # Update the current anomaly state
        
        anomaly_cause = None
        anomaly_deviation = None
        
        if is_anomaly: # If an anomaly is detected
            cause, deviation = anomaly_detector.anomaly_reason(monitor.metrics, latest_metrics)
            anomaly_cause = cause # Get the cause of the anomaly
            anomaly_deviation = deviation # Get the deviation of the anomaly
    else:
        latest_metrics = monitor.get_latest_metrics() # Get the latest metrics without prediction
        current_anomaly_state = False # Update the current anomaly state
        anomaly_cause = None
        anomaly_deviation = None
         
    
    if latest_metrics is None: # If no metrics are collected yet
        latest_metrics = { # Default metrics if none are collected
            "cpu_usage": 0,
            "memory_info": 0,
            "disk_info": 0,
            "time_stamp": "N/A"
            
        }
    if latest_metrics['time_stamp'] != "N/A": # If a timestamp is available
        timestamp_value = datetime.fromisoformat(latest_metrics['time_stamp']) # Convert the timestamp to a datetime object
    else:
        timestamp_value = None # If no timestamp is available, set it to None
    
    metric_record = SystemMetrics( # Create a new SystemMetrics record
        cpu_usage = latest_metrics['cpu_usage'],
        memory_info = latest_metrics['memory_info'],
        disk_info = latest_metrics['disk_info'],
        anomaly = int(current_anomaly_state),
        time_stamp = timestamp_value,
        anomaly_cause = anomaly_cause,
        anomaly_deviation = anomaly_deviation
    )
    
    database.add(metric_record) # Add the record to the database session
    database.commit() # Commit the changes to the database
    database.close() # Close the database session

    if len(monitor.metrics) > 0:
        data = [[m['cpu_usage'], m['memory_info'], m['disk_info']] for m in monitor.metrics]
        means = np.mean(data, axis=0)
        mean_cpu = means[0]
        mean_memory = means[1]
        mean_disk = means[2]
    else:
        mean_cpu = mean_memory = mean_disk = 0 


    return JSONResponse(content={ # Return the latest metrics and anomaly state
        "cpu_usage": latest_metrics['cpu_usage'],
        "memory_info": latest_metrics['memory_info'],
        "disk_info": latest_metrics['disk_info'],
        "time_stamp": latest_metrics['time_stamp'],
        "anomaly": current_anomaly_state,
        "anomaly_cause": anomaly_cause,
        "anomaly_deviation": anomaly_deviation,
        "mean_cpu_usage": mean_cpu,
        "mean_memory_info": mean_memory,
        "mean_disk_info": mean_disk
    })
    

"""Retrieve the last 'limit' system metrics records from the database."""
@app.get("/history")
def get_history(limit: int = 50, database: SessionLocal = Depends(get_database)): # type: ignore

    # Retrieve the last 'limit' system metrics records from the database
    metrics = database.query(SystemMetrics).order_by(SystemMetrics.time_stamp.desc()).limit(limit).all() 
    
    history = [] # Initialize an empty list to store the history of metrics
    for metric in metrics: # Iterate through each metric record
        history.append({ # Create a dictionary for each metric record
            "time_stamp": metric.time_stamp.isoformat(),
            "cpu_usage": metric.cpu_usage,
            "memory_info": metric.memory_info,
            "disk_info": metric.disk_info,
            "anomaly": bool(metric.anomaly),
            "anomaly_cause": metric.anomaly_cause,
            "anomaly_deviation": metric.anomaly_deviation
        })
    return JSONResponse(content=history) # Return the history of metrics as a JSON response

@app.get("/anomaly")
def get_current_anomaly(database: Session = Depends(get_database)):
    global current_anomaly_state
    
    # Retrieve the latest system metrics record from the database
    latest_metric = database.query(SystemMetrics).order_by(SystemMetrics.time_stamp.desc()).first()
    if latest_metric is None:
        return JSONResponse(content={"error": "No metrics found"}, status_code=404)
    # Create a dictionary for the latest metric record
    if latest_metric.anomaly != True:
        current_anomaly_state = False
        return JSONResponse(content={"anomaly": False, "message": "No anomaly detected"})
    else:
        current_anomaly_state = True
        return JSONResponse(content={
            "time_stamp": latest_metric.time_stamp.isoformat(),
            "cpu_usage": latest_metric.cpu_usage,
            "memory_info": latest_metric.memory_info,
            "disk_info": latest_metric.disk_info,
            "anomaly": bool(latest_metric.anomaly),
            "anomaly_cause": latest_metric.anomaly_cause,
            "anomaly_deviation": latest_metric.anomaly_deviation
        })
    
@app.get("/recent_anomalies")
def get_previous_anomalies(limit: int = 8, database: Session = Depends(get_database)):
    
    anomalies = database.query(SystemMetrics).filter(SystemMetrics.anomaly == True).order_by(SystemMetrics.time_stamp.desc()).limit(limit).all()
    
    prev = []
    for anomaly in anomalies: # Iterate through each anomaly record
        prev.append({ # Create a dictionary for each anomaly record
            "time_stamp": anomaly.time_stamp.isoformat(),
            "cpu_usage": anomaly.cpu_usage,
            "memory_info": anomaly.memory_info,
            "disk_info": anomaly.disk_info,
            "anomaly": bool(anomaly.anomaly),
            "anomaly_cause": anomaly.anomaly_cause, 
            "anomaly_deviation": anomaly.anomaly_deviation
        })
        
    return JSONResponse(content={"anomaly": prev}) # Returns the current anomaly state as a JSON response

"""Retrieve the last 'limit' anomaly records from the database."""
@app.get("/anomalies/history")
def get_anomalies_history(limit: int = 50, database: Session = Depends(get_database)):
    
    # Retrieve the last 'limit' anomaly records from the database
    anomalies = database.query(SystemMetrics).filter(SystemMetrics.anomaly == True).order_by(SystemMetrics.time_stamp.desc()).limit(limit).all()
    
    history = [] #Initialize an empty list to store the history of anomalies
    for anomaly in anomalies: # Iterate through each anomaly record
        history.append({ # Create a dictionary for each anomaly record
            "time_stamp": anomaly.time_stamp.isoformat(),
            "cpu_usage": anomaly.cpu_usage,
            "memory_info": anomaly.memory_info,
            "disk_info": anomaly.disk_info,
            "anomaly": bool(anomaly.anomaly),
            "anomaly_cause": anomaly.anomaly_cause,
            "anomaly_deviation": anomaly.anomaly_deviation
        })
    return JSONResponse(content=history) #Return the history of anomalies as a JSON response

"""Download the entire history of system metrics as a JSON file."""
@app.get("/download")

def download_history(database: Session = Depends(get_database)):
    
    metrics = database.query(SystemMetrics).all() # Retrieve all system metrics records from the database
    
    history = [] # Initialize an empty list to store the history of metrics
    for metric in metrics: # Iterate through each metric record
        history.append({ # Create a dictionary for each metric record
            "time_stamp": metric.time_stamp.isoformat(),
            "cpu_usage": metric.cpu_usage,
            "memory_info": metric.memory_info,
            "disk_info": metric.disk_info,
            "anomaly": bool(metric.anomaly),
            "anomaly_cause": metric.anomaly_cause,
            "anomaly_deviation": metric.anomaly_deviation
        })
    return JSONResponse(content=history) # Return the history of metrics as a JSON response

"""Get the current status of the monitoring system."""
@app.get("/status")
def get_status():
    
    global current_anomaly_state
    return JSONResponse(content={
        "monitoring": True,
        "anomaly_detected": current_anomaly_state,
        "last_train_time": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(monitor.start_time))
    })
    
#@app.get("/config")
'''
@app.get("/processes")
def get_processes(n: int = 5, database: Session = Depends(get_database)):
    """Retrieve the top n CPU and Memory consuming processes."""
    processes = monitor.get_processes(n)
    return JSONResponse(content={
        "processes": processes
    })
'''