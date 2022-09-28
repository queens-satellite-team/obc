cmake_minimum_required(VERSION 3.15.3)
project(nucleo-f446re)

enable_language(C ASM)
set(CMAKE_C_STANDARD 99)
set(CMAKE_C_STANDARD_REQUIRED ON)
set(CMAKE_C_EXTENSIONS OFF)

set(STM32CUBEMX_GENERATED_FILES
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_tim_ex.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_uart.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_rcc.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ex.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_flash_ramfunc.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_gpio.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_dma_ex.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pwr_ex.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_cortex.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_exti.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pcd.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_pcd_ex.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_i2c.c
  Drivers/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_i2c_ex.c

  Inc/main.h
  Inc/board_utils.h
  Inc/gpio.h
  Inc/dma.h
  Inc/i2c.h
  Inc/usart.h
  Inc/stm32f4xx_hal_conf.h
  Inc/stm32fxx_it.h


  Src/main.c
  Src/board_utils.c
  Src/gpio.c
  Src/dma.c
  Src/i2c.c
  Src/usart.c
  Src/stm32f4xx_hal_msp.c
  Src/stm32f4xx_it.c
  Src/system_stm32f4xx.c

  Startup/startup_stm32f446xx.s)

set(EXECUTABLE ${PROJECT_NAME}.out)

add_executable(${EXECUTABLE} ${STM32CUBEMX_GENERATED_FILES})

target_compile_definitions(${EXECUTABLE} PRIVATE
  -DUSE_HAL_DRIVER
  -DSTM32F446xx
  )

target_include_directories(${EXECUTABLE} PRIVATE
  Inc
  Drivers/STM32F4xx_HAL_Driver/Inc
  Drivers/CMSIS/Device/ST/STM32F4xx/Include
  Drivers/CMSIS/Include
  )

target_compile_options(${EXECUTABLE} PRIVATE
  -mcpu=cortex-m4
  -mthumb
  -mfpu=fpv4-sp-d16
  -mfloat-abi=soft

  -fdata-sections
  -ffunction-sections
  -Wall
  )

target_link_options(${EXECUTABLE} PRIVATE
  -T${CMAKE_SOURCE_DIR}/STM32F446RE_FLASH.ld
  -mcpu=cortex-m4
  -mthumb
  -mfpu=fpv4-sp-d16
  -specs=nano.specs
  -specs=nosys.specs
  -lc
  -lm
  -lnosys
  -Wl,-Map=${PROJECT_NAME}.map,--cref
  -Wl,--gc-sections
  )

add_custom_command(TARGET ${EXECUTABLE}
  POST_BUILD
  COMMAND arm-none-eabi-size ${EXECUTABLE})

add_custom_command(TARGET ${EXECUTABLE}
  POST_BUILD
  COMMAND arm-none-eabi-objcopy -O ihex ${EXECUTABLE} ${PROJECT_NAME}.hex
  COMMAND arm-none-eabi-objcopy -O binary ${EXECUTABLE} ${PROJECT_NAME}.bin)
