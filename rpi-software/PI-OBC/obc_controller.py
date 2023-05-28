import yaml
from Real_Time_Clock.rtc import RTC 
from Temperature_Sensor.temperature_sensor import Temperature_Sensor
#from Adafruit_ADC.Adafruit_MCP3008.MCP3008 import MCP3008
from Adafruit_ADC.examples.mcp3008 import chan1 
from Adafruit_ADC.examples.mcp3008 import chan2 
import argparse
import csv
from csv import writer

class OBC_Controller:
    """This is a class to contain various fucntions and operations of the on board controller. This class is meant to be used through a CLI.
        
        Functionality:
            1) Yaml file configurability 
            2) Aquire telemetry from multiple devices
    """
    config_path =  "controller_config.yml"

    @staticmethod
    def get_config():
        try:
            with open(OBC_Controller.config_path, 'r') as file:
                return yaml.safe_load(file)
        except:
            Exception(f"Unable to open {OBC_Controller.config_path}")

    @staticmethod
    def init_rtc(config):
        rtc_config = config["rtc"]
        return RTC(rtc_config['battery_state'],None,rtc_config['i2c_status'],rtc_config['datetime'])

    @staticmethod
    def init_temp(config):
        temp_config = config["temperature_sensor"]
        return Temperature_Sensor(temp_config["i2c_status"],temp_config["critical_temperature"],temp_config["upper_temperature"],temp_config["lower_temperature"])

    @staticmethod
    def init_csv(config):
        with open('telemetry_log.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Time", "Temperature", "Current", "Voltage"])


#I don't know if this is needed for SPI device
    @staticmethod
    def init_ADC(config):
        ADC_config = config["ADC"]
        return Temperature_Sensor(temp_config["i2c_status"],temp_config["critical_temperature"],temp_config["upper_temperature"],temp_config["lower_temperature"])

    @staticmethod
    def init_hardware():
        config = OBC_Controller.get_config()
        OBC_Controller.init_rtc(config)
        OBC_Controller.init_temp(config)
        OBC_Controller.init_csv(config)
    

    @staticmethod
    def get_telemetry():
        temp_interface = Temperature_Sensor()
        rtc_interface = RTC() 
        current = chan1.voltage*10;

        print(f"Time: {rtc_interface.datetime}")
        print(f"OBC Ambient Temperature: {temp_interface.ambient} °C")
        print(f"Current Monitor: {current} A")
        print(f"Voltage Monitor: {chan2.voltage} V")
        
        with open('telemetry_log.csv', 'a') as f_object:
            writer_object = writer(f_object)
            writer_object.writerow([rtc_interface.datetime, temp_interface.ambient, current, chan2.voltage])
            f_object.close()

if __name__  == '__main__':
    FUNCTION_MAP =  {
        'telemetry': OBC_Controller.get_telemetry,
        'init': OBC_Controller.init_hardware,
        }
    parser = argparse.ArgumentParser()
    parser.add_argument('cmd', choices=FUNCTION_MAP.keys())
    args = parser.parse_args()

    func = FUNCTION_MAP[args.cmd]
    func()
