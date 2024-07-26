import subprocess
import time


def adb(command):
    subprocess.run(f"sudo adb {command}", shell=True)

adb("kill-server")
adb("start-server")

click_counter = 0
while True:
    adb("shell input tap 250 1000")
    click_counter += 1

    print(f"Clicks : {click_counter}")
    time.sleep(0.01)