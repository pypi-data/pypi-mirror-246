import socket
from scapy.all import IP, TCP, sr1

def single_tcp_scan(target, port):
    try:
        target_ip = socket.gethostbyname(target)
        packet = IP(dst=target_ip) / TCP(dport=port, flags='S')
        response = sr1(packet, timeout=1, verbose=0)
        if response is None:
            return 'Filtered'
        elif response.haslayer(TCP) and response[TCP].flags == 'SA':
            return 'Open'
        else:
            return 'Closed'
    except Exception as e:
        return f"Error: {str(e)}"