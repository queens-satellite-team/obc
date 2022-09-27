# OBC0
### Overview
The OBC0 is based on a Arm Cortex M4 and uses a
[STM32 Nucleo-F446RE](https://www.digikey.ca/en/products/detail/stmicroelectronics/NUCLEO-F446RE/5347712)
development board. The documentation for the Nucleo board is [here](). This
Nucleo board wasn't chosen for a specific reason, and it is possible in future
we will switch a different one. The Nucleo development board family was selected
for ease of development and having a built in ST-Link programmer.

### Directory Structure

### Building
The repository is configured to build with the GNU Arm Embedded Toolchain and
CMake. In a Unix-like environment, open a termina, navigate to the root of the
repository and run:
```
mkdir build && cd build
cmake -DCMAKE_TOOLCHAIN_FILE=../arm-none-eabi-gcc.cmake -DCMAKE_BUILD_TYPE=Debug ..
cmake --build . -- -j 4
```
To flash the executable to the Nucleo:
```
sudo st-flash write <name-of-executable>.bin 0x8000000
```
### Notes
To get the `stm32f4xx_hal_i2c` driver to compile, it was necessary to define
a `HAL_I2C_WRONG_START` variable which was set arbitrarily to 0. This seems to
be a known [issue](https://github.com/STMicroelectronics/STM32CubeG4/issues/8)
with the library.

this is a test change!
