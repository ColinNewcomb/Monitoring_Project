import time
import collections
from data_collector import get_system_metrics
import anomaly_detector

window_size = 60 # Default Window Size
class Monitor:
    def __init__(self):
        self.metrics = collections.deque(maxlen=window_size) # Deque to store metrics with a fixed size
        self.start_time = time.time() # Record the start time of the monitor

    def collect_metrics(self):
        current_metrics = get_system_metrics() # Collect current metrics
        self.metrics.append(current_metrics) # Append to the deque, automatically removing oldest metrics if window size exceeded
        print(f"[{len(self.metrics)}/{window_size}] Latest: {self.metrics[-1]}")


    def get_metrics(self):
        return list(self.metrics) #Returns the collected metrics as a list
    
    def get_latest_metrics(self): 
        return self.metrics[-1] if self.metrics else None #Returns latest Metrics
    #outline this with Prometheus later
    def run(self, interval=1):
        while True:
            self.collect_metrics()
            timer = time.time()
            last_train_time = 0
            if len(self.metrics) >= window_size:
                if anaomaly_detector.trained and timer - last_train_time >= 30:
                    anaomaly_detector.fit(self.metrics)
                    print(f"Timer: {timer} seconds. Model Trained")
                    timer = time.time()  # Reset timer after training
                    last_train_time = timer

                
                if not anaomaly_detector.trained:
                    anaomaly_detector.fit(self.metrics)  # Train the anomaly detector with the current metrics
                    print(f"Timer: {timer} seconds. Model Trained")
                    timer = time.time()  # Reset timer after training
                    last_train_time = timer  # Record the time when the model was last trained
                    
                latest_metrics = self.get_latest_metrics()
                
                if anaomaly_detector.predict(latest_metrics):
                    print(f"Anomaly detected at {latest_metrics['time_stamp']}! Metrics: {latest_metrics}")
            time.sleep(interval)  # Collect metrics every 'interval' seconds
          
          
  
if __name__ == "__main__":
    monitor = Monitor()
    anaomaly_detector = anomaly_detector.AnomalyDetector(0.05)
    print(f"Starting system monitoring with a {window_size}-second rolling window...\n")

    try:
        monitor.run()
    except KeyboardInterrupt:
        print("\nStopped monitoring.")
        print(f"Collected {len(monitor.get_metrics())} data points.")
        latest = monitor.get_latest_metrics()
        if latest:
            print("Last collected metrics:")
            print(latest)

