from os import path, listdir, system
from time import sleep
from influxdb import InfluxDBClient
import sensor_bme280

client = InfluxDBClient(host='localhost', port=8086, username='honig', password='waffel', database='home')

bme280 = sensor_bme280.BME280()

url = 'http://localhost:8086/write?db=home'
metrics = {}
metrics['measurement'] = "sensors"
metrics['tags'] = {}
metrics['tags']['key'] = 'test'

while True:
    metrics['fields'] = {}
    data = {}
    try:
        data = bme280.measure()
    except:
        print("Could not read sensor bme")

    metrics['fields']["Temperature"] = data["Temperature"]
    metrics['fields']["Humidity"] = data["RelHumidity"]
    metrics['fields']["Pressure"] = data["Pressure"]

    client.write_points([metrics])

    sleep(20)
