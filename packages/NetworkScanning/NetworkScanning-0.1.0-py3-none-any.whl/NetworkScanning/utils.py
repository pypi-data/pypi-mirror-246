from scapy.all import get_if_list, conf

def set_default_interface():
    interfaces = get_if_list()
    common_interfaces = ['Ethernet', 'Wi-Fi', 'en0', 'wlan0']
    
    for iface in common_interfaces:
        if iface in interfaces:
            conf.iface = iface
            return iface
    conf.iface = interfaces[0]
    return interfaces[0]