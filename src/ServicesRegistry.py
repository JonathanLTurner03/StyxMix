from zeroconf import ServiceListener, Zeroconf, ServiceInfo
import socket

info = None


class ServicesRegistry(ServiceListener):
    info = None

    def unregister(self, zc: Zeroconf) -> None:
        global info
        if info is not None:
            zc.unregister_service(info)
            print(f"Service removed")
        else:
            print(f"Service not found")

    def register(self, zc: Zeroconf, name: str, desc: str, props: dict, port: int) -> None:
        global info

        local_ip = socket.gethostbyname(socket.gethostname())
        address = socket.inet_aton(local_ip)
        fName = '_' + name.lower() + '._tcp.local.'
        fDesc = desc + '.' + fName

        info = ServiceInfo(
            fName,
            fDesc,
            addresses=[address],
            port=port,
            properties=props,
        )

        Zeroconf().register_service(info)
        print(
            f'Service registered under name: _{name.lower()}.tcp.local., description: {desc}._{name.lower()}._tcp.local., port: {port}',
            f' and properties: {props}')
