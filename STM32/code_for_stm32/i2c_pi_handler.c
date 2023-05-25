#include "i2c_pi_handler.h"


void bad_transfer_handle()
{
	//Your Code here
}

void i2c_pi_handler(I2C_HandleTypeDef* hi2c, uint8_t* txBuffer,unsigned int txBufferSize, uint8_t* rxBuffer,unsigned int rxBufferSize)
{
	  while (HAL_I2C_GetState(hi2c) != HAL_I2C_STATE_READY)
	  {
	  }

	  if (HAL_I2C_Slave_Receive_DMA(hi2c, (uint8_t *)rxBuffer, rxBufferSize) != HAL_OK)
	  {
		  bad_transfer_handle();

	  }

	  while (HAL_I2C_GetState(hi2c) != HAL_I2C_STATE_READY)
	  {
	  }

	  if(rxBuffer[1] == RECEIVE)
	  {
		 if(HAL_I2C_Slave_Receive_DMA(hi2c, (uint8_t *)rxBuffer, rxBufferSize) != HAL_OK)
		 {
			 bad_transfer_handle();
		 }
	  }
	  else if(rxBuffer[1] == TRANSMISSION)
	  {
		 if( HAL_I2C_Slave_Transmit_DMA(hi2c, (uint8_t *)txBuffer, txBufferSize) !=HAL_OK){
			 bad_transfer_handle();
		 }
	  }
}
