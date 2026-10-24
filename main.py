
import time
import asyncio
import random
import matplotlib.pyplot as plt

# Simulated IoT sensor configuration
SENSORS = {
    "Temperature (°C)": (20, 40),
    "Humidity (%)": (30, 90),
    "Pressure (hPa)": (980, 1050),
    "Light (lux)": (100, 1000)
}


def generate_value(sensor_name, limits):
    """Generate a simulated sensor reading."""
    value = round(random.uniform(*limits), 2)
    return sensor_name, value


# --------------------------------
# 1. Synchronous sensor collection
# --------------------------------
def read_sensor_sync(sensor_name, limits):
    # Simulate sensor response delay
    time.sleep(random.uniform(1, 2))
    return generate_value(sensor_name, limits)


def synchronous_collection():
    print("\n=== SYNCHRONOUS EXECUTION ===")
    readings = {}
    start = time.perf_counter()

    for name, limits in SENSORS.items():
        sensor, value = read_sensor_sync(name, limits)
        readings[sensor] = value
        print(f"{sensor}: {value}")

    elapsed = time.perf_counter() - start
    print(f"Total execution time: {elapsed:.2f} seconds")

    return readings, elapsed


# ---------------------------------
# 2. Asynchronous sensor collection
# ---------------------------------
async def read_sensor_async(sensor_name, limits):
    # Simulate non-blocking sensor response delay
    await asyncio.sleep(random.uniform(1, 2))
    return generate_value(sensor_name, limits)


async def asynchronous_collection():
    print("\n=== ASYNCHRONOUS EXECUTION ===")
    start = time.perf_counter()

    tasks = [
        read_sensor_async(name, limits)
        for name, limits in SENSORS.items()
    ]

    results = await asyncio.gather(*tasks)

    readings = {}
    for sensor, value in results:
        readings[sensor] = value
        print(f"{sensor}: {value}")

    elapsed = time.perf_counter() - start
    print(f"Total execution time: {elapsed:.2f} seconds")

    return readings, elapsed


# -------------------------------
# 3. Performance comparison graph
# -------------------------------
def show_comparison(sync_time, async_time):
    methods = ["Synchronous", "Asynchronous"]
    times = [sync_time, async_time]

    plt.figure(figsize=(8, 5))
    bars = plt.bar(methods, times)

    plt.title("IoT Sensor Data Collection Performance")
    plt.ylabel("Execution Time (seconds)")
    plt.xlabel("Execution Method")

    for bar, value in zip(bars, times):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height(),
            f"{value:.2f}s",
            ha="center",
            va="bottom"
        )

    plt.tight_layout()
    plt.show()


# -------------------------------
# 4. Main program
# -------------------------------
async def main():
    print("=" * 45)
    print(" MULTI-SENSOR IoT DATA COLLECTION SYSTEM")
    print("=" * 45)

    sync_data, sync_time = synchronous_collection()

    async_data, async_time = await asynchronous_collection()

    print("\n=== PERFORMANCE ANALYSIS ===")
    print(f"Synchronous time : {sync_time:.2f} seconds")
    print(f"Asynchronous time: {async_time:.2f} seconds")

    if async_time < sync_time:
        improvement = (sync_time - async_time) / sync_time * 100
        print(f"Asynchronous execution was faster by {improvement:.1f}%.")
    else:
        print("Asynchronous execution was not faster in this run.")

    print("\n=== SENSOR DATA SUMMARY ===")
    print("\nSynchronous readings:")
    for sensor, value in sync_data.items():
        print(f"{sensor}: {value}")

    print("\nAsynchronous readings:")
    for sensor, value in async_data.items():
        print(f"{sensor}: {value}")

    show_comparison(sync_time, async_time)


if __name__ == "__main__":
    asyncio.run(main())
