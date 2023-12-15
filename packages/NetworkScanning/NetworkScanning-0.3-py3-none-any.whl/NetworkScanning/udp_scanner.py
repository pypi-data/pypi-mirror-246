import socket
from scapy.all import IP, UDP, ICMP, RandShort, sr1

def single_udp_scan(target, port):
    try:
        target_ip = socket.gethostbyname(target)
        payload = b"\x00" * 10
        packet = IP(dst=target_ip) / UDP(dport=port, sport=RandShort()) / payload
        response = sr1(packet, timeout=3, verbose=0)

        if response is None:
            return 'Open|Filtered'
        elif response.haslayer(ICMP):
            if int(response[ICMP].type) == 3 and int(response[ICMP].code) in [1, 2, 3, 9, 10, 13]:
                return 'Closed'
            else:
                return 'Filtered'
        else:
            return 'Open'
    except Exception as e:
        return f"Error: {str(e)}"