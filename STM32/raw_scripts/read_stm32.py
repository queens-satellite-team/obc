import time
import smbus
from colorama import Fore, Back, Style

defined_bits = {
        'BAD_BYTE' : 0x0,
        'WRITE' : 0x2,
        'READ' : 0x3,
        }

bus = smbus.SMBus(1)
slave_address = 0x15
expected_bytes = 5
timeout = 0 

prep_data = [defined_bits.get('READ')]
while True:
    try:
        bus.write_i2c_block_data(0x15,0,prep_data)
    except:
        time.sleep(2)
        timeout += 1
        if timeout > 1:
            print(Fore.RED +"WARNING: I2C Bus is likely Bad, Power Cycle to fix")
            break
    else:
        break

time.sleep(2)

data = bus.read_i2c_block_data(slave_address,0x0,expected_bytes+2)
bus.close()

print(data[2:])
