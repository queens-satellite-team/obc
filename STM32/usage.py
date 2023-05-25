from stm32 import STM32

expected_bytes = 4 
stm32 = STM32(0x15)

print(stm32.receive(expected_bytes))

data = [0x5,0x7,0x15,0x8]
stm32.transmit(data)

print(stm32.receive(expected_bytes))
