"""
Event manager class.

Continuously poll for a trigger and call the appropriate ISR when needed.

-likely need to import files such as events/specific_event to use methods written there

"""

from default_ISRs import ground_isr, fault_isr, pass_isr

# dynamic dispatch file

# the key hex numbers are placeholders, NOT accurate
dispatch_table = {
    0x00 : ground_isr,
    0x01 : fault_isr,
    0x02 : pass_isr
}

# we'll grab the interrupt signal from something, store it in a variable
#get_input = rasberripi/comms/bus

# then we'll call the isr associated with it as such:
#dispatch_table[get_input]


