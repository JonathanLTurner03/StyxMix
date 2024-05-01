from zeroconf import ServiceListener, Zeroconf, ServiceInfo
import socket

class ServicesRegistry(ServiceListener):

    def update_service(self, zc: 'Zeroconf', type_: str, name: str) -> None:
        info = zc.get_service_info(type_, name)
        if info:
            print("Service %s updated, service info: %s" % (name, info))

    def remove_service(self, zc: Zeroconf, type_: str, name: str) -> None:
        print(f"Service {name} removed")

    def register(self, zc: Zeroconf, name: str) -> None:
        info = ServiceInfo(
            "_styxmix._tcp.local.",
            "StyxMix Audio Control._styxmix._tcp.local.",
            addresses=[socket.inet_aton("127.0.0.1")],
            port=18200,
            properties={'version': '0.0', 'a': 'test value', 'b': 'another value'},
        )

        Zeroconf().register_service(info)
        print('Service registered')
