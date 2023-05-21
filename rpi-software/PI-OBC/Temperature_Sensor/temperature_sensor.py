from smbus import SMBus

class Temperature_Sensor:
    '''
    TEMP class
    I2C interface class written for MCP9808
    Data Sheet: https://ww1.microchip.com/downloads/en/DeviceDoc/25095A.pdf

    Functionality:
    - Get Ambient Temperature
    - Set/Get Critical Temperature
    - Set/Get Upper Temperature
    - Set/Get Lower Temperature
    '''
    i2c_bus = SMBus(1)

    registers = {
        'slave' : 0x18,
        'config' : 0x01,
        't_upper' : 0x02,
        't_lower' : 0x03,
        't_crit' : 0x04,
        't_ambient' : 0x05,
        'manufacture_id' : 0x06,
        'device_id' : 0x07,
        'resolution' : 0x08
    }

    def __init__(self, i2c_status = None, critical_value = None, upper_value = None, lower_value = None):
        '''
        Initialization of Temperature_Sensor class
        '''
        if i2c_status:
            self.i2c_status = i2c_status

        if critical_value:
            self.critical_temp = critical_value

        if upper_value:
            self.upper_temp = upper_value 

        if lower_value:
            self.lower_temp = lower_value 


    def reset(self):
        '''
        Reset the temperature sensor's critical upper and lower temperatures to 0

        '''
        self.critical_temp = 0 
        self.upper_temp = 0 
        self.lower_temp = 0 

    @staticmethod
    def bit_inverse(bit,binary):
        tmp = binary >> bit
        replacement = 1 << bit 

        if tmp & 0x1: #bit to replace is a 1
            replacement = ~replacement
            binary &= replacement
                
        else: #bit to replace is a 0
            binary |= replacement

        return binary 

    def set_temperature(self, register, value):
        '''
        Return the decoded value of a temperature from a given register. Supported for values up until 256 
        '''
        if value < 0:

            value = int(value * -16)
            upper_byte = value >> 8 #isolate Upper bits
            lower_byte = value & 0xFF

            for i in range(4):
                upper_byte = self.bit_inverse(i,upper_byte)
            for i in range(8):
                lower_byte = self.bit_inverse(i,lower_byte)

            upper_byte |= 0x10 # add sign bit

        else:
            value = int(value * 16)
            upper_byte = value >> 8 #isolate upper bits
            lower_byte = value & 0xFF

        self.i2c_bus.write_i2c_block_data(self.registers['slave'],register, [upper_byte,lower_byte])

    def get_temperature(self, register):
        '''
        Return the decoded value of a temperature from a given register
        '''
        temp_reg_data = self.i2c_bus.read_i2c_block_data(self.registers['slave'],register, 2)
        upper_byte =  temp_reg_data[0] & 0x1F
        lower_byte = (temp_reg_data[1]) / 16
        if upper_byte & 0x10:
            upper_byte = (upper_byte & 0xF) * 16
            return -255.75 + (upper_byte + lower_byte)
        else: 
            upper_byte = upper_byte * 16
            return upper_byte + lower_byte

    @property
    def critical_temp(self):
        return self.get_temperature(self.registers['t_crit'])

    @critical_temp.setter
    def critical_temp(self,value):
        self.set_temperature(self.registers['t_crit'],value)

    @property
    def upper_temp(self):
        return self.get_temperature(self.registers['t_upper'])

    @upper_temp.setter
    def upper_temp(self,value):
        self.set_temperature(self.registers['t_upper'],value)

    @property
    def lower_temp(self):
        return self.get_temperature(self.registers['t_lower'])

    @lower_temp.setter
    def lower_temp(self,value):
        self.set_temperature(self.registers['t_lower'],value)

    @property
    def ambient(self):
        return self.get_temperature(self.registers['t_ambient'])
