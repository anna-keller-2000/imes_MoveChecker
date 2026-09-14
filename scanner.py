import asyncio
from bleak import BleakClient

# sensor MAC-adresses
SENSORS = {
    "Oberarm_rechts": "00:A0:50:E0:C6:C8",
    "Oberarm_links": "00:A0:50:E0:F4:E6",
    "Oberschenkel_rechts": "00:A0:50:E0:EC:18",
    "Unterschenkel_links": "00:A0:50:E0:EA:99",
    "Unterschenkel_rechts": "00:A0:50:E0:E8:4A",
    "Torso": "00:A0:50:E0:E5:D7",
    "Unterarm_rechts": "00:A0:50:E0:F6:08",
    "Oberschenkel_links": "00:A0:50:E0:F8:A2",
    "Unterarm_links": "00:A0:50:E0:F9:5C",
}

MAC = "00:A0:50:E0:EA:99"   # <-- MAC-adress of the sensor you want to explore

async def explore_sensor(mac):
    print(f"Connect to sensor {mac} ...")
    client = BleakClient(mac)

    await client.connect()
    print("Connected.\n")

    print("=== SERVICES & CHARACTERISTICS ===")
    for service in client.services:
        print(f"[SERVICE] {service.uuid}")

        for char in service.characteristics:
            print(f"  [CHAR] {char.uuid}  |  Props: {char.properties}")

    print("\n=== TEST NOTIFY-CHARACTERISTICS ===")

    async def notify_handler(sender, data):
        print(f"\n>>> DATA from {sender}: {data.hex(' ')}")
        print(f"Length: {len(data)} Bytes")

    # Test each characteristic that supports notify
    for service in client.services:
        for char in service.characteristics:
            if "notify" in char.properties:
                print(f"\nTesting Notify on {char.uuid} ...")
                try:
                    await client.start_notify(char.uuid, notify_handler)
                    await asyncio.sleep(2.0)   # 2 seconds to listen
                    await client.stop_notify(char.uuid)
                except Exception as e:
                    print(f"  Error: {e}")

    await client.disconnect()
    print("\nFinished.")

asyncio.run(explore_sensor(MAC))
