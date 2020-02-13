import serial
import asyncio
import pynmea2
from collections import deque


def qGPS(s):
    try:
        msg = pynmea2.parse(s)
        q.append(s)
        return s
    except:
        pass

async def showmeGPS():
    while True:
        try:
            s = q.pop() if len(q) > 0 else await asyncio.sleep(1)
            msg = pynmea2.parse(s)
            if msg.sentence_type == 'GGA':
                print("Timestamp: %s -- Lat: %s %s -- Lon: %s %s -- Altitude: %s %s" %
                  (msg.timestamp, msg.lat, msg.lat_dir, msg.lon, msg.lon_dir, msg.altitude, msg.altitude_units))
            else:
                print(f'({msg.sentence_type}...)')
        except:
            pass


async def readGPS():
    with serial.Serial('/dev/ttyUSB0', 9600, timeout=1.0) as sp:
        while True:
            try:
                s = qGPS(sp.readline().decode('utf-8'))

            except:
                print(f'error in decoding {s}')

            await asyncio.sleep(1)


if __name__ == '__main__':
    QMAX = 10
    q = deque(maxlen=QMAX)
    try:
        loop = asyncio.get_event_loop()
        loop.create_task(readGPS())
        loop.run_until_complete(showmeGPS())

    except KeyboardInterrupt:
        print('^C pressed -- exiting script')
