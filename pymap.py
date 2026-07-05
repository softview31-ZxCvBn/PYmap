import socket                                                     import subprocess                                                 import threading
import platform
from concurrent.futures import ThreadPoolExecutor

color = {                                                             "red": "\033[31m", "green": "\033[32m", "yellow": "\033[33m",
    "blue": "\033[34m", "magenta": "\033[35m", "cyan": "\033[36m",    "white": "\033[37m", "bold": "\033[1m", "dim": "\033[2m", "reset": "\033[0m"
}
                                                                  print(f"{color['cyan']}{color['bold']}{'=' * 50}")
print(f"{' PYmap ':^50}")                                         print(f"{'=' * 50}{color['reset']}")
print(f"{color['dim']}{'Developed by Softview31':^50}{color['reset']}\n")

print(f"{color['blue']}{color['bold']} TARGET CONFIGURATION{color['reset']}")
target = input(f"  {color['cyan']}»{color['reset']} Enter Target (IP/Domain): ")
try:                                                                  get_ip = socket.gethostbyname(target)
except socket.gaierror:
    print(f"\n{color['red']}{color['bold']}  [-] Error: Could not resolve hostname.{color['reset']}\n")
    exit()

print(f"  {color['cyan']}»{color['reset']} Resolved Target IP: {color['red']}{get_ip}{color['reset']}\n")

print(f"{color['blue']}{color['bold']} SCAN PARAMETERS{color['reset']}")
start_port = int(input(f"  {color['cyan']}»{color['reset']} Starting Port : "))
end_port = int(input(f"  {color['cyan']}»{color['reset']} Ending Port   : "))
timeout = float(input(f"  {color['cyan']}»{color['reset']} Timeout (sec) : "))
print()

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
    110: "POP3", 443: "HTTPS", 445: "SMB", 1433: "MSSQL", 3306: "MySQL",
    3389: "RDP", 8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}

print(f"{color['yellow']}[*] Checking host status...{color['reset']}", end="\r")

if host_checker(get_ip):
    print(f"{color['green']}{color['bold']}[+] Host is online. Beginning active scan...{color['reset']}\n")

    print(f"{color['cyan']}{'-' * 45}{color['reset']}")
    print(f"  {color['bold']}{'PORT':<12} {'STATUS':<12} {'SERVICE':<15}{color['reset']}")
    print(f"{color['cyan']}{'-' * 45}{color['reset']}")

    ports_to_scan = range(start_port, end_port + 1)
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(scan_port, ports_to_scan)

    if open_ports:
        for port in sorted(open_ports):
            srv_name = service.get(port, 'Unknown')
            print(f"  {color['green']}{port:<12}{color['reset']} {color['bold']}{'OPEN':<12}{color['reset']} {color['dim']}{srv_name:<15}{color['reset']}")
    else:
        print(f"  {color['dim']}No open ports found within the specified range.{color['reset']}")

    print(f"{color['cyan']}{'-' * 45}{color['reset']}")
    print(f"\n{color['green']}{color['bold']} Scan completed successfully.{color['reset']}\n")
else:
    print(f"{color['red']}{color['bold']}[-] Host appears offline. Scan aborted.{color['reset']}\n")
