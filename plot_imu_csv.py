import pandas as pd
import matplotlib.pyplot as plt

def plot_imu_csv(csv_path):
    # CSV laden
    df = pd.read_csv(csv_path)

    # Zeit relativ machen (Start = 0)
    t0 = df["timestamp"].iloc[0]
    df["t"] = df["timestamp"] - t0

    # ACC, GYR, MAG extrahieren
    acc = df[["v1", "v2", "v3"]]
    gyr = df[["v4", "v5", "v6"]]
    mag = df[["v7", "v8", "v9"]]

    # Plot erstellen
    fig, axs = plt.subplots(3, 1, figsize=(12, 10), sharex=True)

    # ACC
    axs[0].plot(df["t"], acc["v1"], label="Acc X")
    axs[0].plot(df["t"], acc["v2"], label="Acc Y")
    axs[0].plot(df["t"], acc["v3"], label="Acc Z")
    axs[0].set_title("Accelerometer")
    axs[0].set_ylabel("Raw Value")
    axs[0].legend()
    axs[0].grid(True)

    # GYR
    axs[1].plot(df["t"], gyr["v4"], label="Gyr X")
    axs[1].plot(df["t"], gyr["v5"], label="Gyr Y")
    axs[1].plot(df["t"], gyr["v6"], label="Gyr Z")
    axs[1].set_title("Gyroscope")
    axs[1].set_ylabel("Raw Value")
    axs[1].legend()
    axs[1].grid(True)

    # MAG
    axs[2].plot(df["t"], mag["v7"], label="Mag X")
    axs[2].plot(df["t"], mag["v8"], label="Mag Y")
    axs[2].plot(df["t"], mag["v9"], label="Mag Z")
    axs[2].set_title("Magnetometer")
    axs[2].set_ylabel("Raw Value")
    axs[2].set_xlabel("Time (s)")
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Beispiel: Datei eines Sensors plotten
    plot_imu_csv("Unterschenkel_links.csv")
