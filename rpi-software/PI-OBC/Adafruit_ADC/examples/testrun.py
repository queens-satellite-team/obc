import board
import digitalio
tester = digitalio.DigitalInOut(board.D8)
tester.direction = digitalio.Direction.OUTPUT
tester.value =  False
