from zeroconf import Zeroconf, ServiceInfo
import socket


def register(zc: Zeroconf, name: str, desc: str, props: dict, port: int) -> None:
    global myInfo

    local_ip = socket.gethostbyname(socket.gethostname())
    address = socket.inet_aton(local_ip)
    fName = '_' + name.lower() + '._tcp.local.'
    fDesc = desc + '.' + fName

    myInfo = ServiceInfo(
        fName,
        fDesc,
        addresses=[address],
        port=port,
        properties=props,
    )

    Zeroconf().register_service(myInfo)
    print(
        f'Service registered under name: _{name.lower()}.tcp.local., description: {desc}._{name.lower()}._tcp.local., port: {port}',
        f' and properties: {props}')


def unregister(zc: Zeroconf) -> None:
    global myInfo
    if myInfo is not None:
        zc.unregister_service(myInfo)
        print(f"Service removed")
    else:
        print(f"Service not found")


def get_local_ipv4() -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 80))
    my_eip = s.getsockname()[0]
    return my_eip


class ServicesMonitor:
    def update_service(self, zeroconf, type, name):
        print("Service %s updated" % (name,))

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            # print("Service %s added, service info: %s" % (name, info))
            print("Service %s added, IP address: %s" % (name, socket.inet_ntoa(info.addresses[0])))

