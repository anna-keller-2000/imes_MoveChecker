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

1. **Scannen nach verfügbaren Bluetooth Devices (`scanner.py`):**  
Diese Datei ist ein kleines Diagnose‑Tool: Sie verbindet sich mit einem einzelnen Sensor, listet alle verfügbaren BLE‑Services und Characteristics auf und testet anschließend jede Notify‑Characteristic, um herauszufinden, welche Daten der Sensor tatsächlich sendet. Damit eignet sich das Skript perfekt, um die Struktur eines Sensors zu verstehen und zu prüfen, welche UUIDs IMU‑ oder Quaternion‑Daten liefern.

