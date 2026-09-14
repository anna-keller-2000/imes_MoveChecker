import asyncio
import struct
import csv
import time
from bleak import BleakClient

# GAIA Sensor MAC-Adressen
SENSORS = {
    "Torso": "00:A0:50:E0:E5:D7",
    "Oberarm_rechts": "00:A0:50:E0:C6:C8",
    "Oberarm_links": "00:A0:50:E0:F4:E6",
    "Unterarm_rechts": "00:A0:50:E0:F6:08",
    "Unterarm_links": "00:A0:50:E0:F9:5C",
    "Oberschenkel_rechts": "00:A0:50:E0:EC:18",
    "Oberschenkel_links": "00:A0:50:E0:F8:A2",
    "Unterschenkel_rechts": "00:A0:50:E0:E8:4A",
    "Unterschenkel_links": "00:A0:50:E0:EA:99",
}

# IMU + Quaternion Characteristics
IMU_CHAR  = "00000000-0000-1000-8000-00805f9b34ff"  # 20-Byte IMU Frame
QUAT_CHAR = "00000000-0000-1000-8000-00805f9b34fc"  # 8-Byte Quaternion

csv_files = {}
quat_files = {}

START_TIME = None  # globaler Zeit-Nullpunkt


# -----------------------------
# Decoder
# -----------------------------
def decode_imu(data: bytearray):
    return struct.unpack("<hhhhhhhhhh", data)

def decode_quat(data: bytearray):
    w, x, y, z = struct.unpack("<hhhh", data)
    return (w/16384.0, x/16384.0, y/16384.0, z/16384.0)


# -----------------------------
# Handler
# -----------------------------
def make_imu_handler(sensor_label):
    def handler(sender, data):
        ts = time.time() - START_TIME
        vals = decode_imu(data)
        csv_files[sensor_label].writerow([ts, *vals])
    return handler

def make_quat_handler(sensor_label):
    def handler(sender, data):
        ts = time.time() - START_TIME
        w, x, y, z = decode_quat(data)
        quat_files[sensor_label].writerow([ts, w, x, y, z])
    return handler


# -----------------------------
# Robuste Verbindung mit Retry
# -----------------------------
async def robust_connect(label, mac, retries=5):
    for attempt in range(1, retries + 1):
        print(f"{label}: Verbindungsversuch {attempt}/{retries} ...")
        client = BleakClient(mac, timeout=10.0)

        try:
            await client.connect()
            if client.is_connected:
                print(f"{label}: Verbunden.")
                return client
        except Exception as e:
            print(f"{label}: Fehler beim Verbinden: {e}")

        await asyncio.sleep(1)

    print(f"{label}: Konnte nach {retries} Versuchen nicht verbunden werden.")
    return None


# -----------------------------
# Main
# -----------------------------
async def main():
    global START_TIME

    # 1) Sensoren seriell verbinden (WICHTIG!)
    clients = {}
    for label, mac in SENSORS.items():
        client = await robust_connect(label, mac)
        if client:
            clients[label] = client

    if not clients:
        print("Keine Sensoren verbunden. Beende.")
        return

    # 2) CSV-Dateien öffnen
    for label in clients.keys():
        f = open(f"{label}.csv", "w", newline="")
        writer = csv.writer(f)
        csv_files[label] = writer
        writer.writerow(["timestamp", "v1","v2","v3","v4","v5","v6","v7","v8","v9","v10"])

        fq = open(f"{label}_quat.csv", "w", newline="")
        wq = csv.writer(fq)
        quat_files[label] = wq
        wq.writerow(["timestamp", "w", "x", "y", "z"])

    # 3) Zeit-Nullpunkt setzen
    START_TIME = time.time()

    # 4) Notify für alle Sensoren parallel starten
    for label, client in clients.items():
        try:
            await client.start_notify(IMU_CHAR, make_imu_handler(label))
            await client.start_notify(QUAT_CHAR, make_quat_handler(label))
            print(f"{label}: Stream gestartet.")
        except Exception as e:
            print(f"{label}: Notify-Fehler: {e}")

    # 5) Aufnahme läuft
    try:
        while True:
            await asyncio.sleep(0.05)
    except KeyboardInterrupt:
        print("Beende Aufnahme...")

    # 6) Sauber trennen
    for label, client in clients.items():
        try:
            await client.disconnect()
            print(f"{label}: getrennt.")
        except:
            pass


# -----------------------------
# Start
# -----------------------------
if __name__ == "__main__":
    asyncio.run(main())
