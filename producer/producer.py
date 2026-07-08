import json
import random
import time
import math
from datetime import datetime, timezone
from azure.eventhub import EventHubProducerClient, EventData

EVENTHUB_CONNECTION_STR = "Endpoint=sb://energysentinel.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=NE6EQCWRqydBHQXx/oPDrnjIPEtbD8Toi+AEhG/pKhU="
EVENTHUB_NAME = "energy-sensors"

SENSORS = {
    "SENSOR_A01": {"plant": "PLANT_A", "base_power": 500, "base_temp": 70},
    "SENSOR_A02": {"plant": "PLANT_A", "base_power": 480, "base_temp": 68},
    "SENSOR_A03": {"plant": "PLANT_A", "base_power": 520, "base_temp": 72},
    "SENSOR_A04": {"plant": "PLANT_A", "base_power": 460, "base_temp": 65},
    "SENSOR_A05": {"plant": "PLANT_A", "base_power": 510, "base_temp": 71},
    "SENSOR_B01": {"plant": "PLANT_B", "base_power": 250, "base_temp": 60},
    "SENSOR_B02": {"plant": "PLANT_B", "base_power": 230, "base_temp": 58},
    "SENSOR_B03": {"plant": "PLANT_B", "base_power": 270, "base_temp": 62},
    "SENSOR_C01": {"plant": "PLANT_C", "base_power": 120, "base_temp": 50},
    "SENSOR_C02": {"plant": "PLANT_C", "base_power": 110, "base_temp": 48},
}


def generate_reading(sensor_id: str, timestamp: str, force_anomaly: bool = False) -> dict:
    config = SENSORS[sensor_id]
    base_power = config["base_power"]
    base_temp = config["base_temp"]

    hour = datetime.fromisoformat(timestamp.replace("Z", "+00:00")).hour
    time_factor = 1 + 0.1 * math.sin(2 * math.pi * hour / 24)

    power = base_power * time_factor + random.uniform(-10, 10)
    voltage = 220 + random.uniform(-2, 2)
    current = (power / voltage) + random.uniform(-0.5, 0.5)
    temperature = base_temp * time_factor + random.uniform(-2, 2)
    power_factor = 0.87 + random.uniform(-0.02, 0.02)
    frequency = 50 + random.uniform(-0.1, 0.1)

    is_anomaly = 0
    if force_anomaly:
        anomaly_type = random.choice(["power_spike", "voltage_drop", "overheating", "frequency_fault"])
        if anomaly_type == "power_spike":
            power *= random.uniform(1.8, 2.5)
            current *= random.uniform(1.8, 2.5)
        elif anomaly_type == "voltage_drop":
            voltage *= random.uniform(0.6, 0.75)
            current *= random.uniform(1.5, 2.0)
        elif anomaly_type == "overheating":
            temperature *= random.uniform(1.6, 2.0)
            power *= random.uniform(1.3, 1.5)
        elif anomaly_type == "frequency_fault":
            frequency += random.uniform(3, 5)
            power_factor *= random.uniform(0.5, 0.7)
        is_anomaly = 1

    return {
        "sensor_id": sensor_id,
        "plant_id": config["plant"],
        "timestamp": timestamp,
        "power_consumption": round(power, 2),
        "voltage": round(voltage, 2),
        "current": round(current, 2),
        "temperature": round(temperature, 2),
        "power_factor": round(power_factor, 3),
        "frequency": round(frequency, 2),
        "is_anomaly": is_anomaly,
    }


def main():
    producer = EventHubProducerClient.from_connection_string(
        conn_str=EVENTHUB_CONNECTION_STR,
        eventhub_name=EVENTHUB_NAME,
    )

    print(f"EnergySentinel Producer started → Event Hub: {EVENTHUB_NAME}")
    print("Press Ctrl+C to stop\n")

    batch_count = 0
    try:
        while True:
            timestamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
            event_batch = producer.create_batch()

            for sensor_id in SENSORS:
                is_anomaly = random.random() < 0.05
                reading = generate_reading(sensor_id, timestamp, force_anomaly=is_anomaly)
                event_batch.add(EventData(json.dumps(reading)))

            producer.send_batch(event_batch)

            batch_count += 1
            if batch_count % 10 == 0:
                print(f"[{timestamp}] Sent {batch_count} batches ({batch_count * len(SENSORS)} readings)")

            time.sleep(1)

    except KeyboardInterrupt:
        print(f"\nStopped. Total: {batch_count} batches sent.")
    finally:
        producer.close()


if __name__ == "__main__":
    main()