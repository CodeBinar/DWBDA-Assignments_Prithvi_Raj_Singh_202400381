"""
Data source for the streaming job.
Every 3 seconds it writes one small JSON-lines file of fake sensor readings
into the 'input_stream' folder. Spark watches that folder for new files.
"""
import json
import os
import random
import time
from datetime import datetime

STREAM_DIR = "input_stream"   # folder Spark reads from
TEMP_DIR = "tmp_stream"       # files are first written here

os.makedirs(STREAM_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

file_no = 0
print("Generating data... press Ctrl+C to stop")

while True:
    file_no += 1
    name = f"readings_{file_no}_{int(time.time())}.json"
    temp_path = os.path.join(TEMP_DIR, name)

    with open(temp_path, "w") as f:
        for _ in range(5):
            record = {
                "sensor_id": random.choice(["S1", "S2", "S3"]),
                "temperature": round(random.uniform(20, 40), 2),
                "event_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            f.write(json.dumps(record) + "\n")

    # Move the finished file in one step so Spark never reads a half-written file
    os.replace(temp_path, os.path.join(STREAM_DIR, name))
    print("Wrote", name)
    time.sleep(3)
