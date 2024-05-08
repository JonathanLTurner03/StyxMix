from zeroconf import Zeroconf, ServiceInfo
from src.handlers import ServicesMonitor

myInfo = None


def register(zc: Zeroconf, name: str, desc: str, props: dict, port: int) -> None:
    global myInfo
    monitor = ServicesMonitor()
    address = monitor.get_local_ipv4()
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
        f'Service registered under name: _{name.lower()}.tcp.local., description: {desc}._{name.lower()}._tcp.local., '
        f'port: {port}',
        f' and properties: {props}')


def unregister(zc: Zeroconf) -> None:
    global myInfo
    if myInfo is not None:
        zc.unregister_service(myInfo)
        print(f"Service removed")
    else:
        print(f"Service not found")
