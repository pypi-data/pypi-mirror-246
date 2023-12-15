import socket

def grab_banner(target, port, protocol="TCP"):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM if protocol == "TCP" else socket.SOCK_DGRAM)
        s.settimeout(3)

        if protocol == "TCP":
            s.connect((target, port))
            banner = s.recv(1024)
        else:
            s.sendto(b"", (target, port))
            banner, _ = s.recvfrom(1024)
        
        s.close()
        return banner.decode('utf-8').strip() if banner else "No banner received"
    except Exception as e:
        return f"Error: {str(e)}"
