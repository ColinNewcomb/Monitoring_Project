import collections

from sklearn import metrics
import monitor
import time
from sklearn.ensemble import IsolationForest
import numpy as np

class AnomalyDetector:
    def __init__(self,contaminatin=0.05):
        self.model = IsolationForest(contamination=contaminatin)  # Initialize the Isolation Forest model
        self.trained  = False  # Flag to check if the model is trained
        
    def fit(self, window):
        # This is given a list of metrics and want to split them into vectors
        # Convert the metrics to a 2D arrays for training
        data = []
        for i in window:
            # Extract relevant features from the metrics
            metrics = [i['cpu_usage'], i['memory_info'], i['disk_info']] #i['network_sent'], i['network_recv']]
            data.append(metrics)
        self.model.fit(data)  # Fit the model with the data
        self.trained = True  # Set the trained flag to True after fitting
   
    def predict(self, metrics):
        if not self.trained:
            raise ValueError("Model has not been trained yet. Call fit() before predict().")
        metrics = [[metrics['cpu_usage'], metrics['memory_info'], metrics['disk_info']]] #metrics['network_sent'], metrics['network_recv']]]
        prediction = self.model.predict(metrics)  # Predict anomalies
        if prediction[0] == -1:
            return True  # Anomaly detected
        return False  # No anomaly detected
    
    def anomaly_reason(self, window, latest_metrics):
        metrics = ['cpu_usage', 'memory_info', 'disk_info']
        
        data = []
        for m in window:
            try:
                data.append([float(m[name]) for name in metrics])
            except(KeyError, TypeError, ValueError):
                continue
        if not data or not latest_metrics:
            return None, None
        means = np.mean(data, axis=0)
        try:
            diffs = [abs(float(latest_metrics[name]) - mean) for name, mean in zip(metrics, means)]
        except (KeyError, TypeError, ValueError):
            return None, None
        max_diff_index = diffs.index(max(diffs))
        return metrics[max_diff_index], diffs[max_diff_index]