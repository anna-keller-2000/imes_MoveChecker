import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Zuordnung: Sensor → Segment-Endpunkte im Ruhezustand (lokale Koordinaten)
SEGMENTS = {
    "Torso": ([0.0, 0.0, 0.0], [0.0, 0.3, 0.0]),
    "Oberarm_rechts": ([0.0, 0.3, 0.0], [0.2, 0.45, 0.0]),
    "Unterarm_rechts": ([0.2, 0.45, 0.0], [0.35, 0.55, 0.0]),
    "Oberarm_links": ([0.0, 0.3, 0.0], [-0.2, 0.45, 0.0]),
    "Unterarm_links": ([-0.2, 0.45, 0.0], [-0.35, 0.55, 0.0]),
    "Oberschenkel_rechts": ([0.05, 0.0, 0.0], [0.05, -0.4, 0.0]),
    "Unterschenkel_rechts": ([0.05, -0.4, 0.0], [0.05, -0.8, 0.0]),
    "Oberschenkel_links": ([-0.05, 0.0, 0.0], [-0.05, -0.4, 0.0]),
    "Unterschenkel_links": ([-0.05, -0.4, 0.0], [-0.05, -0.8, 0.0]),
}

def quat_to_rot_matrix(w, x, y, z):
    q = np.array([w, x, y, z], dtype=float)
    n = np.linalg.norm(q)
    if n == 0:
        return np.eye(3)
    q /= n
    w, x, y, z = q
    return np.array([
        [1 - 2*(y*y + z*z), 2*(x*y - w*z),     2*(x*z + w*y)],
        [2*(x*y + w*z),     1 - 2*(x*x + z*z), 2*(y*z - w*x)],
        [2*(x*z - w*y),     2*(y*z + w*x),     1 - 2*(x*x + y*y)]
    ])

def load_quat_csv(label):
    path = f"{label}_quat.csv"
    df = pd.read_csv(path)
    return df

# Alle Quaternion-Daten laden
quat_data = {}
for label in SEGMENTS.keys():
    try:
        quat_data[label] = load_quat_csv(label)
    except FileNotFoundError:
        print(f"Warnung: {label}_quat.csv nicht gefunden – Segment wird ignoriert.")
        quat_data[label] = None

# Minimale gemeinsame Länge bestimmen
lengths = [len(df) for df in quat_data.values() if df is not None]
if not lengths:
    raise RuntimeError("Keine gültigen Quaternion-CSV-Dateien gefunden.")
min_len = min(lengths)

# Plot vorbereiten
fig = plt.figure(figsize=(6, 8))
ax = fig.add_subplot(111, projection="3d")
ax.set_xlim(-0.6, 0.6)
ax.set_ylim(-1.0, 0.8)
ax.set_zlim(-0.6, 0.6)
ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("9-IMU Stick Figure")

lines = {}
for label in SEGMENTS.keys():
    line, = ax.plot([], [], [], "o-", lw=3, label=label)
    lines[label] = line

ax.legend(loc="upper right", fontsize=8)

def update(frame):
    for label, (p0, p1) in SEGMENTS.items():
        df = quat_data[label]
        if df is None or frame >= len(df):
            continue

        w, x, y, z = df.iloc[frame][["w", "x", "y", "z"]]
        R = quat_to_rot_matrix(w, x, y, z)

        p0r = R @ np.array(p0)
        p1r = R @ np.array(p1)

        xs = [p0r[0], p1r[0]]
        ys = [p0r[1], p1r[1]]
        zs = [p0r[2], p1r[2]]

        lines[label].set_data(xs, ys)
        lines[label].set_3d_properties(zs)

    return list(lines.values())

ani = FuncAnimation(fig, update, frames=min_len, interval=30, blit=True)
plt.tight_layout()
plt.show()
