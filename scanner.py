import asyncio
from bleak import BleakClient

MAC = "00:A0:50:E0:EA:99"   # <-- eine deiner Sensor-MACs hier eintragen

async def explore_sensor(mac):
    print(f"Verbinde mit Sensor {mac} ...")
    client = BleakClient(mac)

    await client.connect()
    print("Verbunden.\n")

    print("=== SERVICES & CHARACTERISTICS ===")
    for service in client.services:
        print(f"[SERVICE] {service.uuid}")

        for char in service.characteristics:
            print(f"  [CHAR] {char.uuid}  |  Props: {char.properties}")

    print("\n=== TESTE NOTIFY-CHARACTERISTICS ===")

    async def notify_handler(sender, data):
        print(f"\n>>> DATA von {sender}: {data.hex(' ')}")
        print(f"Länge: {len(data)} Bytes")

    # Teste jede Characteristic, die Notify unterstützt
    for service in client.services:
        for char in service.characteristics:
            if "notify" in char.properties:
                print(f"\nTeste Notify auf {char.uuid} ...")
                try:
                    await client.start_notify(char.uuid, notify_handler)
                    await asyncio.sleep(2.0)   # 2 Sekunden zuhören
                    await client.stop_notify(char.uuid)
                except Exception as e:
                    print(f"  Fehler: {e}")

    await client.disconnect()
    print("\nFertig.")

asyncio.run(explore_sensor(MAC))
