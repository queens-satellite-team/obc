#include "stm32l4xx_hal.h"


#define RECEIVE 0x2
#define TRANSMISSION 0x3

void bad_transfer_handle();// for you to initialize

void i2c_pi_handler(I2C_HandleTypeDef* hi2c, uint8_t* txBuffer,unsigned int txBufferSize, uint8_t* rxBuffer,unsigned int rxBufferSize);

void bad_cmd_error();// for you to initialize

void subsystem_task(int task); // for you to initialize
