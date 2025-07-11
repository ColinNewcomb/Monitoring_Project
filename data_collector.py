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
    
    # Uncomment the following lines if you want to collect additional metrics
    #metrics['network_sent'] = psutil.net_io_counters().bytes_sent # Network bytes sent
    #metrics['network_recv'] = psutil.net_io_counters().bytes_recv # Network bytes received
    #metrics['boot_time'] = psutil.boot_time() # System boot time in seconds since epoch
    #metrics['user_info'] = psutil.users() # List of users currently logged in

    return metrics


def get_top_processes(n=5):
    """Get the top N resource-consuming processes."""
    
    # Get processes sorted by CPU usage
    processes_by_cpu = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            proc_info = proc.info
            processes_by_cpu.append(proc_info)
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    
    # Sort by CPU usage
    top_cpu_processes = sorted(processes_by_cpu, key=lambda p: p['cpu_percent'], reverse=True)[:n]
    
    # Sort by memory usage
    top_mem_processes = sorted(processes_by_cpu, key=lambda p: p.get('memory_percent', 0), reverse=True)[:n]
    
    return {
        'top_cpu_processes': [{'pid': p['pid'], 'name': p['name'], 'cpu_percent': p['cpu_percent']} 
                             for p in top_cpu_processes],
        'top_memory_processes': [{'pid': p['pid'], 'name': p['name'], 'memory_percent': p.get('memory_percent', 0)} 
                                for p in top_mem_processes]
    }

