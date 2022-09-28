"""
arduino python interface class
~~~~~~~~~~~~

A library to facilitate communication between python scripts
and arduino microcontrollers. Provides basic communication 
methods for UART, I2C, and SPI protocols. For direct implementation,
the matching Arduino is expected to have the firmware file loaded on
to it from: mock-sat/firmware/common/arduino/arduino.ino
"""

import serial
from serial import SerialTimeoutException
from serial.serialutil import SerialException
import smbus
import time

class Arduino:
    """Arduino base class. This class can be inherited by a parent
    classes, i.e. one of the sub-system devices (radio, camera,
    etc.) that utilize an Arduino as its controller. The parent
    will have access to all methods defined here.
    """

    def __init__(self, port='/dev/ttyACM0', baud=115200, start_marker='<', end_marker='>', timeout=10) -> None:
        '''serial parameters'''
        try:
            self.ser = serial.Serial(port=port, baudrate=baud, timeout=timeout, rtscts=True)
        except SerialException as e:
            raise e
        self.ser.reset_input_buffer()
        self._start_marker = start_marker
        self._end_marker = end_marker
        self._data_buffer = ""
        self._data_started = False
        self._message_complete = False

        '''i2c parameters'''
        self.bus = smbus.SMBus(1)
        self.i2c_address = 0x04


    def send_over_serial(self, string:str='hello world'):
        ''' Send a message with serial (UART) communication.

        Params:
            - string (str): the data to send.

        Returns:
            - count (int): the number of bytes written.

        Raises:	
            - SerialTimeoutException: In case a write timeout is configured for the port and the time is exceeded.
        '''

        stringWithMarkers = self._start_marker
        stringWithMarkers += string
        stringWithMarkers += self._end_marker
        count = 0
        self.ser.flushOutput()
        try:
            self.ser.write(stringWithMarkers.encode('utf-8'))
        except SerialTimeoutException as e:
            raise e
        return count

    def receive_over_serial(self):
        '''Read and return data from the USB port.

        Params:
            - None
        
        Returns:
            - line (string): the data received from the USB port
                or "xxx" if no data is available.

        Raises:
            - None
        '''
        while self.ser.inWaiting() > 0 and self._message_complete == False:
            x = self.ser.read().decode('utf-8')  # decode needed for Python3

            if self._data_started == True:
                if x != self._end_marker:
                    self._data_buffer = self._data_buffer + x
                else:
                    self._data_started = False
                    self._message_complete = True
            elif x == self._start_marker:
                self._data_buffer = ''
                self._data_started = True

        if self._message_complete == True:
            self._message_complete = False
            return self._data_buffer
        else:
            return 'xxx'

    def send_over_i2c(self, string:str='hello world'):
        '''Send a message using the I2C bus communication.

        Params:
            - string: the data to send.

        Returns:
            - count (int): the number of bytes written.

        Raises:
            - None
        '''
        count = 0
        for char in string:
            data = int(ord(char))
            try:
                self.bus.write_byte(self.address, data)
            except Exception as e:
                raise e
            count += 1
        return count

    def receive_over_i2c(self):
        '''Receive a message using the I2C bus communication.

        Params:
            - None

        Returns:
            - count (int): the number of bytes written.

        Raises:
            - None

        TODO:
            - include start and stop characters to receive more
            that one value at a time!
        '''
        number = self.bus.read_byte_data(self.i2c_address, 1)
        return number