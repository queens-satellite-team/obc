from temperature_sensor import Temperature_Sensor
import time

temp_sensor = Temperature_Sensor(0)

while 1:
    time.sleep(1)
    temperature = temp_sensor.ambient
    print(f"Current Temperature is :{temp_sensor.ambient}") 
