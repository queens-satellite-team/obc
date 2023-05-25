import time
from colorama import Fore, Back, Style
import smbus

defined_bits = {
        'BAD_BYTE' : 0x0,
        'WRITE' : 0x2,
        'READ' : 0x3,
        }

bus = smbus.SMBus(1)
slave_address = 0x15
timeout = 0 
data = [defined_bits.get('BAD_BYTE'),0x5,0x7,0x15,0x8]
actual_data = data[1:]
print(f"Transmitting {actual_data} to address " + hex(slave_address))

prep_data = [defined_bits.get('WRITE')]
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

data = bus.write_i2c_block_data(slave_address,0x0,data)
bus.close()
