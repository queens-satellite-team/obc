# PI-OBC

This repo is dedicated to python classes utilizing i2c and spi communication in order for a raspberry pi the interact with devices with a higher level of abstraction.

## Usage:

1) Clone repo in home directory
2) Use `python ~/PI-OBC/obc_controller.py init` to initalize hardware.
3) Use the command `crontab -e` and append `* * * * * python ~/PI-OBC/obc_controller.py telemetry >> logs.txt` to the file. This will have telemetry get collected each minute.
4) Enjoy!



## Currently in developement:

- MCP79410 (RTC)
- MCP9808 (Temperature Sensor)
- MCP3008 (ADC)

## Upcomming:

- BNO055 (Orientation Sensor)
