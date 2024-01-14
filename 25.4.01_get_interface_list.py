from ncclient import manager
import xmltodict
import xml.dom.minidom

IOS_HOST = '192.168.100.16'
NETCONF_PORT = '830'
USERNAME = "gandalf"
PASSWORD = "grey"

# Create an XML filter for targeted NETCONF queries
netconf_filter = """
<filter>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface></interface>
    </interfaces>
</filter>"""

print(f"Opening NETCONF Connection to {IOS_HOST}")

# Open a connection to the network device using ncclient
with manager.connect(
    host = IOS_HOST,
    port = NETCONF_PORT,
    username = USERNAME,
    password = PASSWORD,
    hostkey_verify = False
) as device:
    
    print("Sending a <get-config> operation to the device.\n")
    #Make a NETCONF <get-config> query using the filter
    netconf_reply = device.get_config(source = 'running', filter = netconf_filter)

print('*'*50)
print("Here is the raw XML data sent from a device:")
print('*'*50)
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")

# Parse the returned XML to an Ordered Dictionary
netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]

# Create a list if interfaces
interfaces = netconf_data["interfaces"]["interface"]

print('*'*50)
print("Here is the parsed XML data sent from a device:")
print('*'*50)
print(f"The interface status of the {IOS_HOST} device is: ")
for interface in interfaces:
    print("Interface {} enabled status is {}".format(
        interface["name"],
        interface["enabled"]
        )
    )

"""
OUTPUT:

(venv-netconf) gandalf@debian11:~/Python/netconf$ python3 25.4.01_get_interface_list.py 
Opening NETCONF Connection to 192.168.100.16
Sending a <get-config> operation to the device.

**************************************************
Here is the raw XML data sent from a device:
**************************************************
<?xml version="1.0" ?>
<rpc-reply xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" message-id="urn:uuid:35741a46-e38c-4a9a-b3a5-e9764e683857">
        <data>
                <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                        <interface>
                                <name>GigabitEthernet1</name>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>GigabitEthernet2</name>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                                <enabled>false</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>GigabitEthernet3</name>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                                <enabled>false</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>GigabitEthernet4</name>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                                <enabled>false</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>Loopback0</name>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>192.168.255.30</ip>
                                                <netmask>255.255.255.255</netmask>
                                        </address>
                                </ipv4>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                        <interface>
                                <name>Loopback192</name>
                                <description>New Loopback added by Python</description>
                                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type>
                                <enabled>true</enabled>
                                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                                        <address>
                                                <ip>192.192.192.192</ip>
                                                <netmask>255.255.255.255</netmask>
                                        </address>
                                </ipv4>
                                <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
                        </interface>
                </interfaces>
        </data>
</rpc-reply>


**************************************************
Here is the parsed XML data sent from a device:
**************************************************
The interface status of the 192.168.100.16 device is: 
Interface GigabitEthernet1 enabled status is true
Interface GigabitEthernet2 enabled status is false
Interface GigabitEthernet3 enabled status is false
Interface GigabitEthernet4 enabled status is false
Interface Loopback0 enabled status is true
Interface Loopback192 enabled status is true
"""