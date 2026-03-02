# Python-Port-Scanner-
import socket                                 import subprocess                            color = {                                            "red": "\033[31m",
"green": "\033[32m",                         "yellow": "\033[33m",                  "blue": "\033[34m",                     "magenta": "\033[35m",
"cyan": "\033[36m",                   "white": "\033[37m",
"bold": "\033[1m",                 "underline": "\033[4m",
"reset": "\033[0m"
}

print(color['cyan'], color['bold'])
print("=" * 50)
print(f"{'PYTHON NMAP':^50}")
print("=" * 50, color['reset'])
print(color['blue'], "made by Softview31", color['reset'])
print(color['bold'], color['magenta'])
target = input("[*] Target: ")
get_ip = socket.gethostbyname(target)
print(f"[*] Target's IP {get_ip}", color['reset'])

def host_checker(target):
    response = subprocess.call(["ping", "-c", "1", target], stdout = subprocess.DEVNULL,
               stderr = subprocess.DEVNULL)
    if response == 0:
         return True
    else:
         return False
result = host_checker(target)
if result == True:
    print("")

def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    connection = sock.connect_ex((target, port))
    sock.close()
    if connection == 0:
        return True
    else:
        return False

service = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    3306: "MySQL",
    5432: "PostgreSQL",
    1433: "MSSQL",
    3389: "RDP",
    5900: "VNC",
    27017: "MongoDB"
}

if result == True:
  print(color['green'] + color['bold'] +  "[*] Host is up, starting scan...", color['reset'])
  print(color['yellow'], "_" * 50)
  print(f"  {'PORT':>10} {'SERVICE':>20}")
  print("_" * 50)
  for port in range(1, 65535):
       mainfunc = scan_port(target, port)
       if mainfunc == True:
           print(f"  {port:>10} {service.get(port, 'Unknown'):>20}")
else:
    print(color['red'], "[-] Host is down, exiting scan", color['reset'])
