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
import serial
from time import sleep
from events import eventmanager

import pigpio

class COMMS:
    """ r = method is recieving something
        s = method is sending something
    """

    clear_to_send = None    # True if comms is ready to recieve, false otherwise

    # Dummy methods - will either be written in or imported from another file
    def get_telemetry(): pass
    def get_photo(): pass
    def get_shutdown_command(): pass
    def is_msd_space(): pass

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
        Recieves request for data, calls methods to get requested data, and calls method to transmit data

        Args: None

        Returns: None

        """

        COMM_R_TS = 1   # read signal from request line: placeholder ** need to fill in with actual line reading **

        # receive request from comms
        if COMM_R_TS != None:
            data = self.get_data[COMM_R_TS] # get the data
            self.s_transmit_data(data)      # send back the requested data

    def s_transmit_data(self, data=None) -> None:
        """
        1. check clear_to_send
        
        2. Send that data to COMMS over the COMM_R_XD line through **serial communcation**

        Use case: (called in a fault ISR to send fault info to comms)

        Serial communication arduino video:
        https://www.youtube.com/watch?v=6IAkYpmA1DQ
        
        Args:
            data: the data to be transmitted to comms
        """

        self.r_get_clearTS  # get current clear to send status

        if self.clear_to_send:  # while we are clear to send data to COMMs
            # transmit data over COMM_R_XD line through ~serial communication~
            pass

        
        pass

    def r_receive_data(self) -> None:
        """
        1. Gets data from COMMS COMM_T_XD line

        2. If it's telemetry, check for microSD space, then store on microSD

        3. If not telem, then it's a command, so call eventmanager (?)
        
        """

        COMM_T_XD = 111   # placeholder for data ** need to fill in with actual line reading **

        # assumes a convention that the first bit will be an indicator of the type of data (telem = 0, command = 1)

        if COMM_T_XD[0] == '0' and self.is_msd_space():     # if the data is telemetry and we have space, store it
            # store on the microSD
            pass

        if COMM_T_XD[0] == '1':
            eventmanager.dispatch_table[COMM_T_XD]          # if the data is a command, call corresponding process from eventmanager

        pass


if __name__ == "__main__":

    # runs in the raspberry pi :)

    pi = pigpio.pi()

    # ------------------- I2C communication code --------------------
    try:
        h = pi.i2c_open(1, 0x0C) # handle = (bus_no, target_address)
    except:
        print("Handle opening failed")

    try:
        pi.i2c_write_block_data(h, 2, '3')
    except:
        print("Register write failed")

    try:
        (count, data) = pi.i2c_read_block_data(h, 10)
    except:
        print("Register read failed")

    # pi.read()
    # pi.write(4, 0)  # 4 = address/pin no, 0 = state written

    # ----------------- SERIAL TTL communication code -----------------

