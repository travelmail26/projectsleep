#recording bluetooth polar

import asyncio
from bleak import BleakScanner

async def scan_for_devices():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Device {device.address}: {device.name}")
        for service_uuid in device.service_uuids:
            print(f"  Service UUID: {service_uuid}")

asyncio.run(scan_for_devices())
