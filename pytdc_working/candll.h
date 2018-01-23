//==============================================================================
//File name:   "candll.h"
//Purpose:      Header File
//Version:      2.00
//Copyright:    (c) 2013, Akimov Vladimir  E-mail: decoder@rambler.ru		
//==============================================================================
// The following ifdef block is the standard way of creating macros which 
// make exporting from a DLL simpler. All files within this DLL are compiled 
// with the CANDLL_EXPORTS symbol defined on the command line. this symbol 
// should not be defined on any project that uses this DLL. This way any other 
// project whose source files include this file see CANDLL_API functions as 
// being imported from a DLL, whereas this DLL sees symbols defined with this 
// macro as being exported.

#ifndef _CAN_DLL_H_
#define _CAN_DLL_H_

#ifdef CANDLL_EXPORTS
#define CANDLL_API __declspec(dllexport)
#else
#define CANDLL_API __declspec(dllimport)
#endif

//#define  HANDLE unsigned long
#include <windows.h>  

//------------------------------------------------------------------------------
//Adapter control Functions:
//------------------------------------------------------------------------------
CANDLL_API int USBCAN_SetBaudrate( HANDLE lpHandle, unsigned short baudrate);
CANDLL_API int USBCAN_RunSyncTimer( HANDLE lpHandle, int prescaler, int counter);

//------------------------------------------------------------------------------
//API Functions:
//------------------------------------------------------------------------------
CANDLL_API int CAN_GetAdapterList(HANDLE lpComboBox);

CANDLL_API int CAN_ChangeAdapter(HANDLE lpComboBox, HANDLE &lpHandle);

CANDLL_API HANDLE CAN_Open(char const *pCAN_adapter_name, 
						       unsigned short CAN_speed);

CANDLL_API void CAN_Close(HANDLE lpHandle);

CANDLL_API int  CAN_ChannelOpen ( HANDLE lpHandle, 
					         HANDLE event_DataAccepted,
					         unsigned char CAN_DeviceID,
								   unsigned char CAN_ChannelID);

CANDLL_API int  CAN_ChannelClose( HANDLE lpHandle,
							     unsigned char CAN_DeviceID,
								   unsigned char CAN_ChannelID);

CANDLL_API int  CAN_SendCommand( HANDLE lpHandle,
		               unsigned char CAN_device_ID,
								   unsigned char channel_id,
						       unsigned char command,
						       unsigned char param1,
						       unsigned char param2);

CANDLL_API void CAN_SendData( HANDLE lpHandle, 
						       unsigned char  CAN_device_ID,
							     unsigned char  channel_id,
							     unsigned char *pBuffer,
							     unsigned char  size);

CANDLL_API int CAN_ReadData( HANDLE lpHandle,
							    unsigned char *pBuffer,
						      unsigned char  CAN_device_ID,
							    unsigned char  channel_id,
							    unsigned char  Rx_length);	

CANDLL_API int CAN_ReadDevice( HANDLE lpHandle, 
							    unsigned char  device_id,
					        unsigned char  channel_id,
							    unsigned char *pBuffer,
							    unsigned short Rx_length,
					        unsigned char *pTxData,
							    unsigned short Tx_length,
							    int timeout_ms);	

CANDLL_API int CAN_CheckDevice(HANDLE lpHandle, unsigned char CAN_device_ID);

CANDLL_API int CAN_ReturnDeviceID(HANDLE lpHandle, int position);
CANDLL_API int CAN_ReturnDeviceCount(HANDLE lpHandle);

CANDLL_API int CAN_GetDeviceList( HANDLE lpHandle, HANDLE lpListBox,
					        unsigned char device_id_low, 
					        unsigned char device_id_high,
					    		LPVOID pIDs, 	  //CByteArray pointer
	                LPVOID pNames); //CStringArray pointer

//CANDLL_API void CAN_SetRxEvent(HANDLE lpHandle ,CEvent *pEvent);   Old version
CANDLL_API void CAN_SetRxEvent(HANDLE lpHandle, HANDLE *pEvent);

CANDLL_API int CAN_AddPointer( HANDLE lpHandle,
							   unsigned char interface_ID, 
							   unsigned char *pDataBuffer);

CANDLL_API void CAN_ISP_Dialog(HWND hWndParent, HANDLE lpHandle);

//For CAN protocol communication test, Send array + check array
//CANDLL_API void CAN_ProtocolTest(HANDLE lpHandle, unsigned char CAN_device_ID);

//==============================================================================
//Defines:
//==============================================================================
//---------------------------------------
//Virtual CAN channels
//---------------------------------------
#define CAN_CHANNEL7        0x07  //0b111
#define CAN_CHANNEL6        0x06  //0b110
#define CAN_CHANNEL5        0x05  //0b101
#define CAN_CHANNEL4        0x04  //0b101
#define CAN_CHANNEL3        0x03  //0b011
#define CAN_CHANNEL2        0x02  //0b010
#define CAN_CHANNEL1        0x01  //0b001
#define CAN_CMD_CHANNEL     0x00  //0b000

//---------------------------------------
//Cmd for USB-CAN adapter control
//---------------------------------------
#define USBCAN_DATA_EXCHANGE         0xF5
#define USBCAN_STOP_SYNC_TIMER       0x09
#define USBCAN_RUN_SYNC_TIMER        0x08
#define USBCAN_SET_SPEED_1000        0x07
#define USBCAN_SET_SPEED_500         0x06
#define USBCAN_SET_SPEED_250         0x05
#define USBCAN_SET_SPEED_200         0x04
#define USBCAN_SET_SPEED_125         0x03
#define USBCAN_SET_SPEED_100         0x02
#define USBCAN_SET_SPEED_AUTO        0x01
#define USBCAN_ADAPTER_ALREADY_OPEN  2
#define USBCAN_ADAPTER_CONNECTED     1
#define USBCAN_ADAPTER_NOTFOUND      0


#endif
