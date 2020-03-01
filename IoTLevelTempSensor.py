import glob
import os
import urllib2
import json
import calendar
import Hologram
import spidev
import time
from Hologram.HologramCloud import HologramCloud

# connect to 3G network
hologram = HologramCloud(dict(), network='cellular')
hologram.network.connect(timeout=7)

# print connection status; 1 = Connected
print 'CONNECTION STATUS: ' + str(hologram.network.getConnectionStatus())

# initialize temperature sensor
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

# define variables
delay = 0.5
levelsensor_channel = 0

# create SPI
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1250000

# define methods for reading temperature/level sensor values
def readadc(adcnum):
    # read SPI data from the MCP3008, 8 channels in total
    if adcnum > 7 or adcnum < 0:
        return -1
    r = spi.xfer2([1, 8 + adcnum << 4, 0])
    data = ((r[1] & 3) << 8) + r[2]
    return data

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_c


# loop to read values from the 24V hydrostatic pressure sensor(level sensor) and the DS18B20 temperature sensor
while True:
        levelsensor_value = readadc(levelsensor_channel)
        print "---------------------------------------"
        print "Level sensor value: %d" % levelsensor_value
        print "Temperature value: %s" % (read_temp())
        print "Sending values to Firebase"





        #firebase url for client was entered here = ''

        postdata = {
                'datetime': str(calendar.timegm(time.gmtime())),        
                'temperature': str(read_temp()),
                'level': str(levelsensor_value)
        }
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        data = json.dumps(postdata)
        

        response = urllib2.urlopen(req,data)

        

        time.sleep(5)

