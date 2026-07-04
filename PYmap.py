import socket
import subprocess
import threading
import platform  
from concurrent.futures import ThreadPoolExecutor 

color = {
    "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
    "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",
    "white": "\033[37m", "bold": "\033[1m", "underline": "\033[4m",
    "reset": "\033[0m"
}

print(color['cyan'] + color['bold'])
print("=" * 50)
print(f"{'PYmap':^50}")
print("=" * 50 + color['reset'])
print(color['bold'] + color['magenta'] + "made by Softview31" + color['reset'])

print(color['bold'] + color['blue'])
target = input("[*] Target: ")
try:
    get_ip = socket.gethostbyname(target)
except socket.gaierror:
    print(color['red'] + "[-] Could not resolve hostname." + color['reset'])
    exit()

print("[*] Target's IP " + color['red'], get_ip + color['reset'])
print(color['blue'] + color['bold'])
start_port = int(input("[*] Enter Starting port: "))
end_port = int(input("[*] Enter Ending port: "))
timeout = float(input("[*] Enter the amount of seconds to scan each ports: "))
print(color['reset'])

open_ports = []
lock = threading.Lock() 

def host_checker(target_ip):
    ping_flag = "-n" if platform.system().lower() == "windows" else "-c"
    response = subprocess.call(["ping", ping_flag, "1", target_ip], 
                               stdout=subprocess.DEVNULL, 
                               stderr=subprocess.DEVNULL)
    return response == 0

def scan_port(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    connection = sock.connect_ex((get_ip, port)) 
    sock.close()
    if connection == 0:
        with lock:
            open_ports.append(port)

service = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 80: "HTTP",
    110: "POP3", 443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP", 8080: "HTTP-Alt"
}

if host_checker(get_ip):
    print(color['green'] + color['bold'] +  "[*] Host is up, starting scan..." + color['reset'])
    print(color['yellow'] + "_" * 50)
    print(f"  {'PORT':>10} {'SERVICE':>20}")
    print("_" * 50)
    
    ports_to_scan = range(start_port, end_port + 1)
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, ports_to_scan)
        
    for port in sorted(open_ports):
        print(f"  {port:>9} {service.get(port, 'Unknown'):>19}")
else:
    print(color['red'] + "[-] Host is down, exiting scan" + color['reset'])

print(color['reset'])
