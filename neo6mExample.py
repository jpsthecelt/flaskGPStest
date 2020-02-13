import serial
import pynmea2

def parseGPS(str):
    if str.find('GGA') > 0:
       msg = pynmea2.parse(str)
       print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" %
            (msg.timestamp,msg.lat,msg.lat_dir,msg.lon,msg.lon_dir,msg.altitude,msg.altitude_units))

if __name__ == '__main__':
    try:
        with serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0) as sp:
#        with serial.Serial('/dev/serial0', 9600, timeout=1.0) as sp:
           while True:
               byteChars = sp.readline()
               parseGPS(byteChars.decode('utf-8'))

    except KeyboardInterrupt:
        print('^C pressed -- exiting script')

