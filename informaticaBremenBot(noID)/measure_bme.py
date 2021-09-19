from os import path, listdir, system
from time import sleep
import sensor_bme280

bme280 = sensor_bme280.BME280()

while True:
    data = {}
    try:
        data = bme280.measure()
    except:
        print("Could not read sensor bme")

    print("Temperature: " + str(data["Temperature"]))
    print("Humidity: " + str(data["RelHumidity"]))
    print("Pressure: " + str(data["Pressure"]))
    print("--------------------------------")

    sleep(5)
