# Bluetooth LE Scanning Module
# 3C:A3:08:AD:F3:BA Beacon 1
# 3C:A3:08:AD:EC:98 Beacon 2
# 3C:A3:08:AD:EC:BE Beacon 3

from bluepy.btle import Scanner, DefaultDelegate
from numpy import array, empty, savetxt, dtype, str_, sort

# Initialise Delegate Object
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)
    
    # Handle discovery of devices
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print("Discovered device", dev.addr)
        elif isNewData:
            print("Received new data from", dev.addr)

# Setup some default values
count = 0
arrCount = 0
prevArrCount = 0

# Prompt user input for number of scans, delay and writing to file
numScan = input("Enter number of scans (default = 10) : ")
numDelay = input("Enter scanning timeout (default = 5.0s) : ")

if numScan == "": numScan = 10 
if numDelay == "": numDelay = 5.0 

arrtype = dtype([('number', int), ('mac', str_, 20), ('rssi', str_, 16)])
deviceArray = empty([int(numScan)*3], dtype=arrtype)

while count < int(numScan):

    print("\n==================== Scan [%d] ====================" % (count+1))
    # Setup scanner and scanning timeout
    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(float(numDelay))
    print("")

    prevArrCount = arrCount
    # Printing into human readable output
    for dev in devices:
        print("Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi))
        
        # Input Values
        addr = dev.addr.upper()
        rssi = str(dev.rssi)

        if addr == "3C:A3:08:AD:F3:BA":
            deviceArray['number'][arrCount] = 1
            deviceArray['mac'][arrCount] = addr
            deviceArray['rssi'][arrCount] = rssi
            arrCount += 1
        elif addr == "3C:A3:08:AD:EC:98":        
            deviceArray['number'][arrCount] = 2
            deviceArray['mac'][arrCount] = addr
            deviceArray['rssi'][arrCount] = rssi
            arrCount += 1
        elif addr == "3C:A3:08:AD:EC:BE":
            deviceArray['number'][arrCount]= 3
            deviceArray['mac'][arrCount] = addr
            deviceArray['rssi'][arrCount] = rssi
            arrCount += 1
    
    rem = arrCount - prevArrCount
    if rem != 3:
        print("\nFailed to obtain 3 readings... Repeating iteration : %d " % (count+1))

        deviceArray[arrCount - rem:arrCount] = [(0, "", "")]
        #deviceArray['number'][arrCount - rem:arrCount] = 0
        #deviceArray['mac'][arrCount - rem:arrCount] = ""
        #deviceArray['rssi'][arrCount - rem:arrCount] = ""
        arrCount = arrCount - rem
        count -= 1

    count += 1
    
# Attempt at sorting the nodes 

for i in range(0,int(len(deviceArray)) - 1,3):
    deviceArray[i:i+3] = sort(deviceArray[i:i+3], order='number')

savetxt("devices.csv",deviceArray,delimiter=",", fmt="%s")

