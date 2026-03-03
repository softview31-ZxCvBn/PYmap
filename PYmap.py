# Python-Port-Scanner
import socket
import subprocess
import threading
color = {
"red": "\033[31m",
"green": "\033[32m",
"yellow": "\033[33m",
"blue": "\033[34m",
"magenta": "\033[35m",
"cyan": "\033[36m",
"white": "\033[37m",
"bold": "\033[1m",
"underline": "\033[4m",
"reset": "\033[0m"
}
print(color['cyan'] + color['bold'])
print("=" * 50)
print(f"{'PYmap':^50}")
print("=" * 50 + color['reset'])
print(color['bold'] + color['magenta'] + "made by Softview31" + color['reset'])
print(color['bold'] + color['blue'])
target = input("[*] Target: ")
get_ip = socket.gethostbyname(target)
print("[*] Target's IP " + color['red'], get_ip + color['reset'])
print(color['blue'] + color['bold'])
start_port = int(input("[*]Enter Starting port(default:1): "))
end_port = int(input("[*] Enter Ending port(default: 1024): "))
timeout = float(input("[*] Enter the amount of seconds to scan each ports: "))
print(color['reset'])
open_ports = []
def host_checker(target):
    response = subprocess.call(["ping", "-c", "1", target], stdout = subprocess.DEVNULL,
               stderr = subprocess.DEVNULL)
    if response == 0:
         return True
    else:
         return False
result = host_checker(target)
def scan_port(target, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(timeout)
    connection = sock.connect_ex((target, port))
    sock.close()
    if connection == 0:
        open_ports.append(port)
    else:
        return False

service = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    119: "NNTP",
    123: "NTP",
    135: "RPC",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    194: "IRC",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    587: "SMTP-TLS",
    631: "IPP",
    993: "IMAPS",
    995: "POP3S",
    1080: "SOCKS Proxy",
    1433: "MSSQL",
    1723: "PPTP VPN",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
    9929: "Nping Echo",
    27017: "MongoDB",
    31337: "Elite/Backdoor"
}
threads = []
if result == True:
  print(color['green'] + color['bold'] +  "[*] Host is up, starting scan..." + color['reset'])
  print(color['yellow'] + "_" * 50)
  print(f"  {'PORT':>10} {'SERVICE':>20}")
  print("_" * 50)
  for port in range(start_port, end_port + 1):
    t = threading.Thread(target=scan_port, args=(target, port))
    threads.append(t)
    t.start()
    if len(threads) % 100 == 0:
        for t in threads[-100:]:
            t.join()
  for t in threads:
      t.join()
  for port in sorted(open_ports):
      print(f"  {port:>9} {service.get(port, 'Unknown'):>19}")
else:
    print(color['red'] + "[-] Host is down, exiting scan" + color['reset'])
