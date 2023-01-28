"""
Interrupt service routines for:
    1. Ground-int
    2. Fault-int
    3. Pass sequences

Call these once an interrupt has occurred (no interrupt checking here)

"""
# import RPi.GPIO as GPIO

def ground_isr():
    # Receive MCC command

    # transmit telemetry - send data from microSD and send to comms - method for this being developed in comms class (just pass it what needs to be sent)

    # execute commands

    # load new schedule

    return

def fault_isr():
    # fault detection

    # switch to fault-safe mode

    return

def pass_isr():
    # roll to pointing angle

    # check memory

    # system health check

    # proceed to pass mode

    return