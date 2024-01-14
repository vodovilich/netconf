""" Add a loopback interface to a device with NETCONF """

from ncclient import manager

IOS_HOST = '192.168.100.16'
NETCONF_PORT = '830'
USERNAME = "gandalf"
PASSWORD = "grey"

LOOPBACK_ID = '192'
LOOPBACK_IP = '192.192.192.192'
MASK = '255.255.255.255'
TYPE = 'ianaift:softwareLoopback'
DESC = 'New Loopback added by Python'
STATUS = "true"
#create add_loopback() method
def add_loopback():
    tpl_add_loop_interface = f"""
    <config>
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>Loopback{LOOPBACK_ID}</name>
                <description>{DESC}</description>
                <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                    {TYPE}
                </type>
                <enabled>{STATUS}</enabled>
                <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                    <address>
                        <ip>{LOOPBACK_IP}</ip>
                        <netmask>{MASK}</netmask>
                    </address>
                </ipv4>
            </interface>
        </interfaces>
    </config>"""
    
    with manager.connect(
        host = IOS_HOST,
        port = NETCONF_PORT,
        username = USERNAME,
        password = PASSWORD,
        hostkey_verify = False
    ) as device:
    
        # Add loopback interface
        print(f"\n Adding Loopback {LOOPBACK_ID} with IP address {LOOPBACK_IP} to device {IOS_HOST}...\n")
        netconf_response = device.edit_config(target = 'running', config = tpl_add_loop_interface)
        
        # Print the XML response
        print(netconf_response)
        
if __name__ == '__main__':
    add_loopback()
    
"""
Q: Why <interface xlmns="urn:ietf:params:xml:ns:yang:ietf-interfaces"> ?
A:
    0)
    (venv-netconf) gandalf@debian11:~/Python/netconf$ head -3  ../../yang/standard/ietf/RFC/ietf-interfaces.yang 
    
    module ietf-interfaces {
    yang-version 1.1;
    namespace "urn:ietf:params:xml:ns:yang:ietf-interfaces"; <---------- NAMESPACE
    
    0.5)
    (venv-netconf) gandalf@debian11:~/Python/netconf$ grep -H 'urn:ietf:params:xml:ns:yang:ietf-interfaces' ../../yang/standard/ietf/RFC/*

    ../../yang/standard/ietf/RFC/ietf-interfaces@2014-05-08.yang:  namespace "urn:ietf:params:xml:ns:yang:ietf-interfaces";
    ../../yang/standard/ietf/RFC/ietf-interfaces@2018-02-20.yang:  namespace "urn:ietf:params:xml:ns:yang:ietf-interfaces";
    ../../yang/standard/ietf/RFC/ietf-interfaces.yang:  namespace "urn:ietf:params:xml:ns:yang:ietf-interfaces";        <--------MODEL
    
    1) What model is it?:
    (venv-netconf) gandalf@debian11:~/Python/netconf$ grep "urn:ietf:params:xml:ns:yang:ietf-interfaces" 25.4_capabilities.txt
     
    urn:ietf:params:xml:ns:yang:ietf-interfaces?module=ietf-interfaces&revision=2014-05-08&features=pre-provisioning,if-mib,arbitrary-names
    urn:ietf:params:xml:ns:yang:ietf-interfaces-ext?module=ietf-interfaces-ext
    
Q: Why line_24: <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type"> , line_28: <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">?
A:
    1)
    +--rw interfaces
    |  +--rw interface* [name]
    |     +--rw name                        string
    |     +--rw description?                string
    |     +--rw type                        identityref
    
    2) From get-config command:
<interface>
        <name>Loopback0</name>
        <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:softwareLoopback</type> <-----
        <enabled>true</enabled>
        <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">  <-----
                <address>
                        <ip>192.168.255.30</ip>
                        <netmask>255.255.255.255</netmask>
                </address>
        </ipv4>
        <ipv6 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip"/>
    
Q: Why does get list return ipv4 section if it is not present in the ietf-nterfaces.yang model ?
A: did not find

Q:How does  urn:ietf:params:xml:ns:yang:ietf-interfaces model look?
A:
    (venv-netconf) gandalf@debian11:~/Python/netconf$ pyang -f tree ../../yang/standard/ietf/RFC/ietf-interfaces.yang 
    
    ../../yang/standard/ietf/RFC/ietf-interfaces.yang:6: error: module "ietf-yang-types" not found in search path
    module: ietf-interfaces
    +--rw interfaces
    |  +--rw interface* [name]
    |     +--rw name                        string
    |     +--rw description?                string
    |     +--rw type                        identityref
    |     +--rw enabled?                    boolean
    |     +--rw link-up-down-trap-enable?   enumeration {if-mib}?
    |     +--ro admin-status                enumeration {if-mib}?
    |     +--ro oper-status                 enumeration
    |     +--ro last-change?                yang:date-and-time
    |     +--ro if-index                    int32 {if-mib}?
    |     +--ro phys-address?               yang:phys-address
    |     +--ro higher-layer-if*            interface-ref
    |     +--ro lower-layer-if*             interface-ref
    |     +--ro speed?                      yang:gauge64
    |     +--ro statistics
    |        +--ro discontinuity-time    yang:date-and-time
    |        +--ro in-octets?            yang:counter64
    |        +--ro in-unicast-pkts?      yang:counter64
    |        +--ro in-broadcast-pkts?    yang:counter64
    |        +--ro in-multicast-pkts?    yang:counter64
    |        +--ro in-discards?          yang:counter32
    |        +--ro in-errors?            yang:counter32
    |        +--ro in-unknown-protos?    yang:counter32
    |        +--ro out-octets?           yang:counter64
    |        +--ro out-unicast-pkts?     yang:counter64
    |        +--ro out-broadcast-pkts?   yang:counter64
    |        +--ro out-multicast-pkts?   yang:counter64
    |        +--ro out-discards?         yang:counter32
    |        +--ro out-errors?           yang:counter32
    x--ro interfaces-state
        x--ro interface* [name]
            x--ro name               string
            x--ro type               identityref
            x--ro admin-status       enumeration {if-mib}?
            x--ro oper-status        enumeration
            x--ro last-change?       yang:date-and-time
            x--ro if-index           int32 {if-mib}?
            x--ro phys-address?      yang:phys-address
            x--ro higher-layer-if*   interface-state-ref
            x--ro lower-layer-if*    interface-state-ref
            x--ro speed?             yang:gauge64
            x--ro statistics
            x--ro discontinuity-time    yang:date-and-time
            x--ro in-octets?            yang:counter64
            x--ro in-unicast-pkts?      yang:counter64
            x--ro in-broadcast-pkts?    yang:counter64
            x--ro in-multicast-pkts?    yang:counter64
            x--ro in-discards?          yang:counter32
            x--ro in-errors?            yang:counter32
            x--ro in-unknown-protos?    yang:counter32
            x--ro out-octets?           yang:counter64
            x--ro out-unicast-pkts?     yang:counter64
            x--ro out-broadcast-pkts?   yang:counter64
            x--ro out-multicast-pkts?   yang:counter64
            x--ro out-discards?         yang:counter32
            x--ro out-errors?           yang:counter32
    
"""