import uuid


def get_mac_address():
    mac = uuid.getnode()
    mac_address = ':'.join([hex(mac)[i:i+2] for i in range(0, 11, 2)])
    return mac_address