#!/bin/sh
# Start the monitor process in background
python monitor.py &

# Start API server
uvicorn api_metrics:app --host 0.0.0.0 --port 8000