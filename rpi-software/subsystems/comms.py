"""COMMS class will contain methods to handle r/s from the comms subsystem

Will be fairly hardware involved.

Lines to comms:

COMM_C_TS = clear to send (says whether or not the comms board is ready to receive something)

COMM_R_TS = request to send (requesting info from obc to be send to comms)

COMM_T_XD = COMMS-DB (comms transmiter data line)

COMM_R_XD = COMMS-DB (comms reciever data line)


To do:
-request command code
-tell comms about a fault

Hello Hana

Hi back, testing conflicts


"""

class COMMS:
    """ r = method is recieving something
        s = method is sending something
    """

    clear_to_send = None    # True if comms is ready to recieve, false otherwise

    def __init__(self):
        """not sure if this needs to be a class"""
        pass

    def r_get_clearTS(self) -> None:
        """
        1. Recieves the signal from comms COMM_C_TS line indicating if they are ready for data

        2. Store result in global var.
        
        """
        pass

    def r_get_requestTS(self) -> None:
        """
        1. Recieves request for data from comms on the COMM_R_TS line
        
        2. Get that data

        3. Call s_transmit_data to send back the requested data
        """
        pass

    def s_transmit_data(self, data=None) -> None:
        """
        1. check clear_to_send

        2. If we're clear, get data from microSD (possibly format it)
        
        3. Send that data to COMMS over the COMM_T_XD line

        Use case: (called in a fault ISR to send fault info to comms)
        
        Args:
            data: the data to be transmitted to comms
        """
        pass

    def r_receive_data(self) -> None:
        """
        1. Gets data from COMMS COMM_R_XD line

        2. If it's telemetry, check for microSD space, then store on microSD

        3. If not telem, then it's a command, so call eventmanager (?)
        
        """
        pass



