from smbus import SMBus

slaveAddress = 0x8 # slave address for test purpose, the real implmentation will be conducted via passing address by functions
bus = SMBus(1) # indicates /dev/ic2-1
data_received_from_device = "" # empty variable with no defined type to accomodate various types of input
bus.write_byte(slaveAddress, 0x1) # switch LED on
input("Press return to exit")
bus.write_byte(slaveAddress, 0x0) # switch LED off



#Writing character to I2C bus @ specific address
def writeNumber(address, value):
    try:
        bus.write_byte(address, ord(value)) # ord(value) returns the ASCII code of a given character
    except:
        print("Device with address:", address, "is not connected!")
        pass
    return -1


#Writing string to I2C bus @ specific address
def writeString(address, word):
    try:
        for character in word:
            bus.write_byte(address, ord(character))
    except:
        print("STM Not Connected!")
        pass
    return -1


# Read number from I2C bus @ specific address
def readNumber(address):
    try:
        x = bus.read_byte(address)
        print(x) # check if bus has something to be fetched? if so x == 1
        data_received_from_Arduino = bus.read_i2c_block_data(address, 0,15) # not sure how that works!! what is 8 means as third input in bus.read_i2c_block_data
        print(data_received_from_device)
    except:
        print("Device with address:", address, "is not connected!")
        pass
    return -1

# Read 


# main 
writeNumber(slaveAddress, 'a')
writeString(slaveAddress, "Hello World")
