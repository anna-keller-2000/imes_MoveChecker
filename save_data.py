import asyncio
import struct
import csv
import time
from bleak import BleakClient

# Deine Sensoren
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

# Alle Notify-Characteristics der GAIA/BNO055-Sensoren
NOTIFY_CHARS = [
    "00000000-0000-1000-8000-00805f9b34fc",
    "00000000-0000-1000-8000-00805f9b34fa",
    "00000000-0000-1000-8000-00805f9b34ff",
    "00000000-0000-1000-8000-00805f9b34f1",
    "00000000-0000-1000-8000-00805f9b34f4",
]

# CSV Speicher
csv_files = {}

def decode_frame(data: bytearray):
    """Dekodiert BNO055-Frames automatisch."""
    length = len(data)

    # 6 Bytes → ACC/GYR/MAG
    if length == 6:
        x, y, z = struct.unpack("<hhh", data)
        return ("vec3", (x, y, z))

    # 8 Bytes → Quaternion
    if length == 8:
        w, x, y, z = struct.unpack("<hhhh", data)
        return ("quat", (w/16384.0, x/16384.0, y/16384.0, z/16384.0))

    # 20 Bytes → Full IMU frame (manchmal kombiniert)
    if length == 20:
        vals = struct.unpack("<hhhhhhhhhh", data)
        return ("imu20", vals)

    return ("raw", data.hex(" "))


def make_handler(sensor_label):
    def handler(sender, data):
        ts = time.time()
        dtype, values = decode_frame(data)

        writer = csv_files[sensor_label]

        if dtype == "vec3":
            writer.writerow([ts, dtype, *values])

        elif dtype == "quat":
            writer.writerow([ts, dtype, *values])

        elif dtype == "imu20":
            writer.writerow([ts, dtype, *values])

        else:
            writer.writerow([ts, dtype, values])
    return handler


async def connect_sensor(label, mac):
    print(f"Verbinde mit {label} ({mac}) ...")

    client = BleakClient(mac, timeout=10.0)

    try:
        await client.connect()
        if not client.is_connected:
            print(f"  FEHLER: {label} konnte nicht verbunden werden.")
            return

        print(f"  Verbunden mit {label}")

        # CSV Datei öffnen
        f = open(f"{label}.csv", "w", newline="")
        writer = csv.writer(f)
        csv_files[label] = writer
        writer.writerow(["timestamp", "type", "v1", "v2", "v3", "v4", "v5", "v6", "v7", "v8", "v9", "v10"])

        # Notify abonnieren
        for char in NOTIFY_CHARS:
            try:
                await client.start_notify(char, make_handler(label))
            except Exception as e:
                print(f"  Konnte {char} nicht abonnieren: {e}")

        print(f"  {label} streamt Daten...")

        while True:
            await asyncio.sleep(0.1)

    except Exception as e:
        print(f"  Fehler bei {label}: {e}")

    finally:
        try:
            await client.disconnect()
        except:
            pass


async def main():
    tasks = []
    for label, mac in SENSORS.items():
        tasks.append(asyncio.create_task(connect_sensor(label, mac)))

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
