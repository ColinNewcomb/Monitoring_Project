import psutil
import datetime
import time
import platform 


def get_system_metrics():
    """Collects CPU and Memory usage metrics. w/TimeStamp."""
    metrics = {}
    metrics['time_stamp'] = datetime.datetime.now().isoformat() #ISO Formatted TimeStamp
    metrics['cpu_usage'] = psutil.cpu_percent(interval=1) # CPU usage percentage
    metrics['memory_info'] = psutil.virtual_memory().percent # Memory usage percentage
    
    if platform.system() == 'Windows':
        metrics['disk_info'] = psutil.disk_usage('C:\\').percent
    else:
        metrics['disk_info'] = psutil.disk_usage('/').percent
    
    # Uncomment the following lines if you want to collect additional metrics
    #metrics['network_sent'] = psutil.net_io_counters().bytes_sent # Network bytes sent
    #metrics['network_recv'] = psutil.net_io_counters().bytes_recv # Network bytes received
    #metrics['boot_time'] = psutil.boot_time() # System boot time in seconds since epoch
    #metrics['user_info'] = psutil.users() # List of users currently logged in

    return metrics
'''
def get_processes(n=5):
    """Returns the top n CPU and Memory consuming processes."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            if proc.pid == 0:
                continue
            processes.append(proc.info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    # Sort by CPU usage and get the top n processes
    processes.sort(key=lambda x: x['cpu_percent'], reverse=False)
    return processes[:n]
'''