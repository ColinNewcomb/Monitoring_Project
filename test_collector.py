from data_collector import get_system_metrics
# test_collector.py

"""This script tests the system metrics collector by printing out the collected metrics.
It collects metrics every second for a total of 10 seconds."""

if __name__ == "__main__":
    import time

    print("Starting system monitor test...\n")
    for _ in range(10):  # Collect 10 samples, one per second
        metrics = get_system_metrics()
        print(metrics)
        time.sleep(1)
