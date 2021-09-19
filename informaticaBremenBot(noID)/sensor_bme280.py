import smbus2
import bme280

class BME280():

    def __init__(self, port=1, address=0x77):
        self.port = port
        self.address = address
        self.bus = smbus2.SMBus(self.port)

        self.calibration_params = bme280.load_calibration_params(self.bus, self.address)



    def measure(self):
        values = bme280.sample(self.bus, self.address, self.calibration_params)
        data ={}
        data["Temperature"] = values.temperature
        data["Pressure"] = values.pressure
        data["RelHumidity"] = values.humidity
        return data
