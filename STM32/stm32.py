import time
from colorama import Fore, Back, Style
import smbus

class STM32:
    defined_bits = {
            'BAD_BYTE' : 0x0,
            'WRITE' : 0x2,
            'READ' : 0x3,
            }

    bus = smbus.SMBus(1)
    timeout_thershold = 3
    
    def __init__(self,slave_address):
        self.slave_address = slave_address

    def transmit(self,data):
        print(f"Transmitting {data} to address " + hex(self.slave_address))
        data[:0] = [self.defined_bits.get('BAD_BYTE')]
        cmd_data = [self.defined_bits.get('WRITE')]
        timeout = 0 
        while True:
            try:
                self.bus.write_i2c_block_data(0x15,0,cmd_data)
            except:
                time.sleep(2)
                timeout += 1
                if timeout > self.timeout_thershold:
                    print(Fore.RED +"WARNING: I2C Bus is likely Bad, Power Cycle to fix")
                    return
            else:
                break
        time.sleep(2)
        data = self.bus.write_i2c_block_data(self.slave_address,0x0,data)

    def receive(self,expected_bytes):
        cmd_data = [self.defined_bits.get('READ')]
        timeout = 0 
        while True:
            try:
                self.bus.write_i2c_block_data(0x15,0,cmd_data)
            except:
                time.sleep(2)
                timeout += 1 
                if timeout > self.timeout_thershold:
                    print(Fore.RED +"WARNING: I2C Bus is likely Bad, Power Cycle to fix")
                    return
            else:
                break
        time.sleep(2)
        data = self.bus.read_i2c_block_data(self.slave_address,0x0,expected_bytes+2)
        return(data[2:])
