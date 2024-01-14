from ncclient import manager

IOS_HOST = '192.168.100.16'
NETCONF_PORT = '830'
USERNAME = "gandalf"
PASSWORD = "grey"

#create a get_capabilities() method
def get_capabilities():
    """
    Method that prints NETCONF capabilities of a remote device
    """
    with manager.connect(
        host = IOS_HOST,
        port = NETCONF_PORT,
        username = USERNAME,
        password = PASSWORD,
        hostkey_verify = False
    ) as device:
        
        #print all NETCONF capabilities
        #print('\n***NETCONF Capabilities for device {}***\n'.format(IOS_HOST))
        print(f'\n***NETCONF Capabilities for device {IOS_HOST}***\n')
        for capability in device.server_capabilities:
            print(capability)
            
if __name__ == '__main__':
    get_capabilities()