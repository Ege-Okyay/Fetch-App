from colorama import init, Fore, Back, Style
from datetime import datetime
from sys import getsizeof
from GPUtil import getGPUs

import psutil
import typer
import time
import socket
import platform

app = typer.Typer()
init(autoreset=True)

# Colors
TITLE = Fore.CYAN
DESC = Fore.GREEN
DETAILS = Fore.WHITE

## Calculations ##
def find_bootime():
    boot_time_timestamp = psutil.boot_time()
    bt = datetime.fromtimestamp(boot_time_timestamp)

    return bt

def byte_calculation(bytes, suffix="B"):
    factor = 1024

    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

## Commands ##
@app.command()
def general():
    uname = platform.uname()
    print(TITLE + f"\nGeneral Details@{socket.gethostname()}\n" + Fore.BLUE + "-"*30)

    print(DESC + "Bootime: " + DETAILS + f"{find_bootime().year}/{find_bootime().month}/{find_bootime().day} {find_bootime().hour}:{find_bootime().minute}:{find_bootime().second}")
    print(DESC + "Local IP: " + DETAILS + f"{socket.gethostbyname(socket.gethostname())}")
    print(DESC + "System: " + DETAILS+ f"{uname.system}")
    print(DESC + "Node Name: " + DETAILS + f"{uname.node}")
    print(DESC + "Release: " + DETAILS + f"{uname.release}")
    print(DESC + "Version: " + DETAILS + f"{uname.version}")
    print(DESC + "Machine: " + DETAILS + f"{uname.machine}")
    print(DESC + "Processor: " + DETAILS + f"{uname.processor}" + "\n")

@app.command()
def cpu():
    cpu_freq = psutil.cpu_freq()
    
    print(TITLE + "\nCPU Details\n" + Fore.BLUE + "-"*30)
    
    print(DESC + "Physical Cores: " + DETAILS + f"{psutil.cpu_count(logical=False)}")
    print(DESC + "Total Cores: " + DETAILS + f"{psutil.cpu_count(logical=True)}")
    print(DESC + "Max Frequency: " + DETAILS + f"{cpu_freq.max:.2f}Mhz")
    print(DESC + "Min Frequency: " + DETAILS + f"{cpu_freq.min:.2f}Mhz")
    print(DESC + "Current Frequency: " + DETAILS + f"{cpu_freq.current:.2f}Mhz")
    
    print(DESC + "CPU Usage Per Core:")
    for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
        print(DETAILS + f"{i}: {percentage}%")

    print(DESC + "Total CPU Usage: " + DETAILS + f"{psutil.cpu_percent()}%")

@app.command()
def memory():
    svmem = psutil.virtual_memory()
    swap = psutil.swap_memory()

    print(TITLE + "\nMemory Details\n" + Fore.BLUE + "-"*30)
    
    print(Fore.YELLOW + "\nVirtual Memory\n" + "-"*13)
    print(DESC + "Total: "+ DETAILS + byte_calculation(svmem.total))
    print(DESC + "Used: " + DETAILS + byte_calculation(svmem.used))
    print(DESC + "Available: " + DETAILS + byte_calculation(svmem.available))
    print(DESC + "Percentage: " + DETAILS + f"{svmem.percent}%")
    
    print(Fore.YELLOW + "\nSwap Memory\n" + "-"*13)
    print(DESC + "Total: " + DETAILS + byte_calculation(swap.total))
    print(DESC + "Used: " + DETAILS + byte_calculation(swap.used))
    print(DESC + "Free: " + DETAILS + byte_calculation(swap.free))
    print(DESC + "Used: " + DETAILS + byte_calculation(swap.used))
    print(DESC + "Percentage: " + DETAILS + f"{swap.percent}%\n")

@app.command()
def disk():
    print(TITLE + "\nDisk Details\n" + Fore.BLUE + "-"*30)
    
    print(Fore.YELLOW + "\nPartitions and Usage\n" + "-"*13)
    
    partitions = psutil.disk_partitions()
    for partition in partitions:
        print(DESC + "Device: " + DETAILS + partition.device)
        print(DESC + "Mountpoint: " + DETAILS + partition.mountpoint)
        print(DESC + "File Type: " + DETAILS + partition.fstype)
        
        try:
            partition_usage = psutil.disk_usage(partition.mountpoint)
        except PermissionError:
            continue

        print(DESC + "Total Size: " + DETAILS + byte_calculation(partition_usage.total))
        print(DESC + "Used: " + DETAILS + byte_calculation(partition_usage.used))
        print(DESC + "Free: " + DETAILS + byte_calculation(partition_usage.free))
        print(DESC + "Percentage: " + DETAILS + f"{byte_calculation(partition_usage.percent)}%" + "\n")

    disk_io = psutil.disk_io_counters()
    print(DESC + "Total Read: " + DETAILS + byte_calculation(disk_io.read_bytes))
    print(DESC + "Total Write: " + DETAILS + byte_calculation(disk_io.write_bytes) + "\n")

@app.command()
def network():
    print(TITLE + "\nNetwork Details\n" + Fore.BLUE + "-"*30)
    
    addrs = psutil.net_if_addrs()
    for i_name, i_addresses in addrs.items():
        print(Fore.YELLOW + f"\nInterface: {i_name}\n" + "-"*13)
        for address in i_addresses:
            if str(address.family) == "AddressFamily.AF_INET":
                print(DESC + "IP Address: " + DETAILS + address.address)
                print(DESC + "Netmask: " + DETAILS + address.netmask)
                print(DESC + "Brodcast IP: " + DETAILS + str(address.broadcast))
            elif str(address.family) == "AddressFamily.AF_PACKET":
                print(DESC + "MAC Address: " + DETAILS + address.address)
                print(DESC + "Netmask: " + DETAILS + address.netmask)
                print(DESC + "Brodcast MAC: " + DETAILS + address.broadcast)

    net_io = psutil.net_io_counters()
    print(DESC + "Total Bytes Sent: " + DETAILS + byte_calculation(net_io.bytes_sent))
    print(DESC + "Total Bytes Received: " + DETAILS + byte_calculation(net_io.bytes_recv) + "\n")

@app.command()
def gpu():
    gpus = getGPUs()

    print(TITLE + "\nGPU Details\n" + Fore.BLUE + "-"*30)

    for gpu in gpus:
        print(Fore.YELLOW + f"\n{gpu.name}\n" + "-"*13)
        print(DESC + "Load Memory: " + DETAILS + f"{gpu.load*100}%")
        print(DESC + "Free Memory: " + DETAILS + f"{gpu.memoryFree}MB")
        print(DESC + "Used Memory: " + DETAILS + f"{gpu.memoryUsed}MB")
        print(DESC + "Total Memory: " + DETAILS + f"{gpu.memoryTotal}MB")
        print(DESC + "Temperature: " + DETAILS + f"{gpu.temperature} °C")
        print(DESC + "UUID: " + DETAILS + gpu.uuid + "\n")

if __name__ == "__main__":
    app()
