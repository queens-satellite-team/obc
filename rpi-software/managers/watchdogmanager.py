"""
Watchdog class
~~~~~~~~~~~~~~~~~~~~~

A class to interface with the software based watchdog provided by signal
Supports multiple separate timers simultaneously
"""

import signal
import time
from os import system
import platform


class Watchdog:
    __active_watchdogs = []
    __alarm_handler_setup = False
    __linux = platform.system() == "Linux"

    def _alarm_handler(signum, frame):
        """
        Action performed when the watchdog alarm is triggerd
        Set to reboot the rpi
        """
        print("Alarm triggerd, rebooting")
        if platform.system() == "Linux":
            system("sudo reboot")

    def __init__(self):
        """
        Constructs a new watchdog
        """
        if Watchdog.__linux:
            signal.signal(signal.SIGALRM, Watchdog._alarm_handler)
        self.timeout = 0
        if not Watchdog.__alarm_handler_setup:
            Watchdog.__active_watchdogs.append([self, 0])
            Watchdog.__alarm_handler_setup = True

    def start(self, timeout):
        """ 
        Start the timer of a watchdog 

        params:
            timeout: Time in seconds before triggering the watchdog alarm
        """
        self.timeout = timeout
        low = int(time.time()) + timeout
        for i in Watchdog.__active_watchdogs:
            if i[0] == self:
                i[1] = int(time.time()) + timeout
            if i[1] < low and i[1] != 0:
                low = i[1]

        print("timing out in", low - int(time.time()))
        if Watchdog.__linux:
            signal.alarm(low-int(time.time()))

    def stroke(self):
        """
        Restarts the timer for a given watchdog
        """
        low = int(time.time()) + self.timeout
        for i in Watchdog.__active_watchdogs:
            if i[0] == self:
                i[1] = int(time.time()) + self.timeout
            if i[1] < low and i[1] != 0:
                low = i[1]

        print("stroked, now timing out in", low - int(time.time()))
        if Watchdog.__linux:
            signal.alarm(low-int(time.time()))

    def stop(self):
        """
        Stops the timer on a given watchdog
        """
        self.timeout = 0
        low = 0
        for i in Watchdog.__active_watchdogs:
            if i[0] == self:
                i[1] = 0

            if (i[1] < low and i[1] != 0) or low == 0:
                low = i[1]
        if low == 0: timeout = 0
        else: timeout = low - int(time.time())
        print("Stopped, now timing out in", timeout)
        if Watchdog.__linux:
            signal.alarm(timeout)


"""
#create the watchdog
sample_watchdog = Watchdog()

#start the timer
sample_watchdog.start(5) #has a 5 second timeout 


#this loop will preform as normal
while(True):
    sample_watchdog.stroke()
    time.sleep(4)


#this cause the rpi to restart due to the watchdog exceding its timeout
while(True):
    sample_watchdog.stroke()
    time.sleep(6)
"""

"""
#create multiple watchdogs
sample_watchdog1 = Watchdog()
sample_watchdog2 = Watchdog()

sample_watchdog1.start(4)
sample_watchdog2.start(20)

while(True):
    continue

This will end due to sample_watchdog1 timer of 4 seconds being reached
"""