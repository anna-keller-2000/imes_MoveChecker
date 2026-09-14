# Datenaufnahme mit MoveChecker-Sensoren

## Datenstruktur

```
imes_MoveChecker/
│
├── scanner.py
├── 
    ├── 
    ├── 
    └── 
└── README.md
```

## Voraussetzungen

- Bluetooth muss aktiviert sein
- Sensoren müssen aufgeladen und bereit zum verbinden sein
- Die MAC-Adressen der einzelnen Sensoren müssen zugeordnet sein (Dafür habe ich mit der App nRF Connect jeden Sensor einzeln verbunden und geschaut, welcher beim Verbinden aufhört zu leuchten und nach Trennen der Verbindung wieder damit anfängt. Die Zuordnung habe ich notiert und weiter verwendet.)
- Folgende Pakete müssen installiert sein:
  - bleak
  - pandas
  - numpy
  - matplotlib


Installiere alle benötigten Pakete mit:
```bash
pip install bleak pandas numpy matplotlib
```

## Nutzung

1. **Verbinden mit einem bestimmten Sensor, um UUID herauszufinden  (`scanner.py`):**  
Diese Datei ist ein kleines Diagnose‑Tool: Sie verbindet sich mit einem einzelnen Sensor, listet alle verfügbaren BLE‑Services und Characteristics auf und testet anschließend jede Notify‑Characteristic, um herauszufinden, welche Daten der Sensor tatsächlich sendet. Damit eignet sich das Skript perfekt, um die Struktur eines Sensors zu verstehen und zu prüfen, welche UUIDs IMU‑ oder Quaternion‑Daten liefern.

IMU‑Daten (20‑Byte‑Frames):  
00000000-0000-1000-8000-00805f9b34ff  
→ enthält ACC, GYR, MAG + Status

Quaternion‑Daten (8‑Byte‑Frames):  
00000000-0000-1000-8000-00805f9b34fc  
→ enthält w, x, y, z (Rotation)

2. **Verbinden mit allen Sensoren und streamen der IMU-Daten (`save_data`):**
Die Datei verbindet sich nacheinander mit den 9 Sensoren, startet anschließend für jeden Sensor zwei Datenstreams (IMU‑Rohdaten und Quaternion‑Daten) und speichert diese Live‑Daten direkt in CSV‑Dateien.
Für jeden Sensor entstehen zwei Dateien:
    <Sensor>.csv → IMU‑Rohdaten (ACC/GYR/MAG)
    <Sensor>_quat.csv → Quaternion‑Rotationen (w,x,y,z)
*PROBLEM*: Mehrere Sensoren können nicht verbunden werden, weil der Windows‑Bluetooth‑Stack überlastet ist, die Sensoren zu nah beieinander liegen, manche im Busy‑State hängen und Advertising‑Pakete kollidieren. Dadurch schlagen die Verbindungsversuche für bestimmte Sensoren wiederholt fehl, und für diese Sensoren wird kein Notify‑Stream gestartet und ihre CSV‑Dateien bleiben leer.

