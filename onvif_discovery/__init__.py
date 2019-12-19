import socket

DOMAIN = 'onvif_discovery'

#PLATFORM_SCHEMA = {"onvif_discovery":}

#DOMAIN = 'hello_service'

ATTR_NAME = 'name'
DEFAULT_NAME = 'World'


def setup(hass, config):
    """Set up is called when Home Assistant is loading our component."""

    def handle_hello(call):

        msgh = """<?xml version="1.0" encoding="utf-8" ?>
        <soap:Envelope
            xmlns:soap="https://www.w3.org/2003/05/soap-envelope"
            xmlns:wsa="https://schemas.xmlsoap.org/ws/2004/08/addressing"
            xmlns:wsd="https://schemas.xmlsoap.org/ws/2005/04/discovery"
            xmlns:wsdp="https://schemas.xmlsoap.org/ws/2006/02/devprof">
        <soap:Header>
            <wsa:To>
                urn:schemas-xmlsoap-org:ws:2005:04:discovery
            </wsa:To>
            <wsa:Action>
                https://schemas.xmlsoap.org/ws/2005/04/discovery/Hello
            </wsa:Action>
            <wsa:MessageID>
                urn:uuid:0f5d604c-81ac-4abc-8010-51dbffad55f2
            </wsa:MessageID>
            <wsd:AppSequence InstanceId="2" SequenceId="urn:uuid:369a7d7b-5f87-48a4-aa9a-189edf2a8772" MessageNumber="14">
            </wsd:AppSequence>
        </soap:Header>
        <soap:Body>
            <wsd:Hello>
                <wsa:EndpointReference>
                    <wsa:Address>
                        urn:uuid:37f86d35-e6ac-4241-964f-1d9ae46fb366
                    </wsa:Address>
                </wsa:EndpointReference>
                <wsd:Types>wsdp:Device</wsd:Types>
            </wsd:Hello>
        </soap:Body>
        </soap:Envelope>"""

        msg = """<?xml version="1.0" encoding="UTF-8" ?>
        <e:Envelope xmlns:e="http://www.w3.org/2003/05/soap-envelope" 
            xmlns:w="http://schemas.xmlsoap.org/ws/2004/08/addressing" 
            xmlns:d="http://schemas.xmlsoap.org/ws/2005/04/discovery" 
            xmlns:dn="http://www.onvif.org/ver10/network/wsdl">
            <e:Header>
                <w:MessageID>uuid:76779Fu4-7018-4974-A88B-BF29651E6E3u</w:MessageID>
                <w:To e:mustUnderstand="true">urn:schemas-xmlsoap-org:ws:2005:04:discovery</w:To>
                <w:Action a:mustUnderstand="true">http://schemas.xmlsoap.org/ws/2005/04/discovery/Probe</w:Action>
            </e:Header>
            <e:Body>
                <d:Probe>
                    <d:Types>dn:NetworkVideoTransmitter</d:Types>
                </d:Probe>
            </e:Body>
        </e:Envelope>"""

        # Set up UDP socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(3)
        s.sendto(msg.encode(), ('239.255.255.250', 3702))
        
        try:
            while True:
                data, addr = s.recvfrom(65507)
                DEFAULT_NAME=addr[0]
#                self.log("Hello from AppDaemon")
        except socket.timeout:
#            self.log("Hello solo")
            pass

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        s.settimeout(2)
        s.sendto(msgh.encode(), ('239.255.255.250', 3702) )

        try:
            while True:
                data, addr = s.recvfrom(65507)
                DEFAULT_NAME += '\n'
                DEFAULT_NAME += addr[0]
#                self.log("Hello from AppDaemon")
        except socket.timeout:
#            self.log("Hello solo")
            pass
        
            """Handle the service call."""
            name = call.data.get(ATTR_NAME, DEFAULT_NAME)

        hass.states.set('onvif_discovery.discover', name)

    hass.services.register(DOMAIN, 'discover', handle_hello)

    # Return boolean to indicate that initialization was successfully.
    return True