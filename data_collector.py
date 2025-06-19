import psutil
import datetime
import time


def get_system_metrics():
    """Collects CPU and Memory usage metrics. w/TimeStamp."""
    metrics = {}
    metrics['time_stamp'] = datetime.datetime.now().isoformat()
    metrics['cpu_usage'] = psutil.cpu_percent(interval=1)
    metrics['memory_info'] = psutil.virtual_memory().percent
    metrics['disk_info'] = psutil.disk_usage('C:\\').percent
    metrics['network_sent'] = psutil.net_io_counters().bytes_sent
    metrics['network_recv'] = psutil.net_io_counters().bytes_recv
    metrics['boot_time'] = psutil.boot_time()
    metrics['user_info'] = psutil.users()
    
    return metrics
    
    