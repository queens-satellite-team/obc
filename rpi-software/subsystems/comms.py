"""COMMS class will contain methods to handle r/s from the comms subsystem

Will be fairly hardware involved.

Lines to comms:

COMM_C_TS = clear to send (says whether or not the comms board is ready to receive something)

COMM_R_TS = request to send (comms is requesting info from obc)

COMM_T_XD = COMMS-DB (comms transmiter data line)

COMM_R_XD = COMMS-DB (comms reciever data line)


To do:
-request command code
-tell comms about a fault


"""
# from RPi import GPIO

import serial
from time import sleep

import pigpio
# import gpiozero # this is built on pigpio and RPi.GPIO, useful only if we need their pre-created methods

class COMMS:
    """ r = method is recieving something
        s = method is sending something
    """

    pi = pigpio.pi()
    h = pi.i2c_open(1, 0x53) # handle = (bus_no, target_address)
    clear_to_send = None    # True if comms is ready to recieve, false otherwise

    # These methods will either be written in or imported from another file
    def get_telemetry(): pass
    def get_photo(): pass
    def get_shutdown_command(): pass

    # dictionary which calls commands to get certain data
    # Note: these methods are not the actual methods we will use (placeholders for now)
    get_data = {
        0x0 : get_telemetry(),
        0x1 : get_photo(),
        0x10 : get_shutdown_command()
    }


    def __init__(self):
        """not sure if this needs to be a class"""
        pass

    def r_get_clearTS(self) -> None:
        """
        1. Recieves the signal from comms COMM_C_TS line indicating if they are ready for data
        
        2. Store result in global var.
        
        """
        if COMM_C_TS:
            clear_to_send = True
        
        pass

    def r_get_requestTS(self) -> None:
        """
        1. Recieves request for data from comms on the COMM_R_TS line

        2. Get that data - telemetry, photos*, shutdown/restart command

        3. Call s_transmit_data to send back the requested data
        """
        COMM_R_TS = 1   # read signal from request line (1 is a placeholder here)

        # receive request from comms
        if COMM_R_TS != None:
            data = self.get_data[COMM_R_TS] # get the data
            self.s_transmit_data(data)      # send back the requested data

    def s_transmit_data(self, data=None) -> None:
        """
        1. check clear_to_send

        2. If we're clear, get data from microSD (possibly format it)
        
        3. Send that data to COMMS over the COMM_R_XD line

        Use case: (called in a fault ISR to send fault info to comms)
        
        Args:
            data: the data to be transmitted to comms
        """
        if clear_to_send:
            
        
        pass

    def r_receive_data(self) -> None:
        """
        1. Gets data from COMMS COMM_T_XD line

        2. If it's telemetry, check for microSD space, then store on microSD

        3. If not telem, then it's a command, so call eventmanager (?)
        
        """
        pass

# this site contains info on the pigpio library, seems very useful
# https://abyz.me.uk/rpi/pigpio/python.html#custom_1

# I've written the details of the most useful functions (imo) below w little examples

if __name__ == "__main__":
    pi = pigpio.pi()

    # SMBus is a python module which makes it super easy to write data on the 12C bus
    # h = handle (identifier for the device we are connecting to)

    h = pi.i2c_open(1, 0x53) #(bus_no, target_address)
    
    (count, data) = pi.i2c_read_block_data(h, 10)

    pi.i2c_write_block_data(h, 5, b'hi')   # (handle, register, bytes to write)

    print(data)

    
    # pi.read()
    # pi.write(4, 0)  # 4 = address/pin no, 0 = state written
    
    # """custom_2(arg1, argx, retMax):
    # calls a pigpio function customised by the user

    # arg1 : default 0
    # argx : extra arguments (each 0-255), default empty)
    # retMax : max number of bytes to return, default 8192

    # returns : [num bytes returned, bytearray containing bytes]
    
    # (count, data) = pi.custom_2()
    # """callback(user_gpio, edge, func):
    # calls a user supplied function (a callback) whenever the specified GPIO edge is detected

    # user_gpio: 0-31
    # edge : EITHER_EDGE, RISING_EDGE (default), FALLING_EDGE
    # func : user supplied callback function
    
    # """
    # def cbf(gpio, level, tick):
    #     print(gpio, level, tick)

    # cb1 = pi.callback(22, pigpio.EITHER_EDGE, cbf)

