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

import pigpio

class COMMS:
    """ r = method is recieving something
        s = method is sending something
    """

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
        Recieves request for data, calls methods to get requested data, and calls method to transmit data

        Args: None

        Returns: None

        """

        COMM_R_TS = 1   # read signal from request line (1 is a placeholder here)

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
<<<<<<< HEAD

=======
        if clear_to_send:
            
        
>>>>>>> 431f39b99414718c743879ef11eac43508de49d6
        pass

    def r_receive_data(self) -> None:
        """
        1. Gets data from COMMS COMM_T_XD line

        2. If it's telemetry, check for microSD space, then store on microSD

        3. If not telem, then it's a command, so call eventmanager (?)
        
        """
        pass


if __name__ == "__main__":

    # runs in the raspberry pi :)

    pi = pigpio.pi()
    h = pi.i2c_open(1, 0x0C) # handle = (bus_no, target_address)

    # throws an error (because we weren't connected) :(

    (count, data) = pi.i2c_read_block_data(h, 10)   # (handle, register)
    pi.i2c_write_block_data(h, 5, b'hi')   # (handle, register, bytes to write)

    # pi.read()
    # pi.write(4, 0)  # 4 = address/pin no, 0 = state written


