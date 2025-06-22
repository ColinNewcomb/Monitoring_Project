import psutil
import datetime
import time


def get_system_metrics():
    """Collects CPU and Memory usage metrics. w/TimeStamp."""
    metrics = {}
    metrics['time_stamp'] = datetime.datetime.now().isoformat() #ISO Formatted TimeStamp
    metrics['cpu_usage'] = psutil.cpu_percent(interval=1) # CPU usage percentage
    metrics['memory_info'] = psutil.virtual_memory().percent # Memory usage percentage
    metrics['disk_info'] = psutil.disk_usage('C:\\').percent # Disk usage percentage
    metrics['network_sent'] = psutil.net_io_counters().bytes_sent # Network bytes sent
    metrics['network_recv'] = psutil.net_io_counters().bytes_recv # Network bytes received
    #metrics['boot_time'] = psutil.boot_time() # System boot time in seconds since epoch
    #metrics['user_info'] = psutil.users() # List of users currently logged in

    return metrics
    
    