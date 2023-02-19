import time
from   smbus import SMBus

class ADC:

    i2c_bus = SMBus(1)

    stm32_registers = {
        'slave' : 0x6F,
        'current_telemetry': 0x00,
        'target_telemetry': 0x01,
        'status': 0x02,
        'power_controls': 0x03,
    }

    def __init__(self, telemetry, status):
        self.status = status
        self.telemetry = telemetry

    def receive_data(self, slave_address, register):
        #Signal(recieve_pin)
        time.sleep(3)
        try:
            return self.i2c_bus.read_byte_data(slave_address,register)
        except:
            raise RuntimeError(f"Unable to receive data from {register}")

    def transmit_data(self, slave_address, register, data):
        #Signal(transmit_pin)
        time.sleep(3)
        try:
            return self.i2c_bus.write_byte_data(slave_address,register,data)
        except:
            raise RuntimeError(f"Unable to transmit data to register : {register}")

    def get_telemetry(self):
        return self.receive_data(self.stm32_registers['slave'],self.stm32_registers['current_telemetry'])

    @propertry
    def target_telemetry(self):
        return self.receive_data(self.stm32_registers['slave'],self.stm32_registers['target_telemetry'])

    @target_telemetry.setter
    def target_telemetry(self,telemetry):
        self.transmit_data(self.stm32_registers['slave'],self.stm32_registers['targert_telemetry'],telemetry)

    def status(self):
        return self.i2c_bus.read_byte_data(self.stm32_registers['slave'],self.stm32_registers['status'])

    @property
    def power_controls(self):
        return self.receive_data(self.stm32_registers['slave'],self.stm32_registers['power_controls'])

    @power_controls.setter
    def power_controls(self,device_states):
        self.transmit_data(self.stm32_registers['slave'],self.stm32_registers['power_controls'],device_states)

    @property
    def magnatorquer(self):
        return self.power_controls & 0x1

    @magnatorquer.setter
    def magnatorquer(self,state):
        if state == 0:
            modified_power_controls = self.power_controls | 0x1
        if state == 1:
            modified_power_controls = self.power_controls & ~0x1
        else:
            raise ValueError("Value entered must be 0 or 1")
        self.power_controls = modified_power_controls