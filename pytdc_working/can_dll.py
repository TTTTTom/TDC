__author__ = 'cqt'

from ctypes import *
import time

class can():

    CMD_CAN_SET_DAC0 = 0xC4
    CMD_CAN_SET_DAC1 = 0xC5
    CMD_CAN_SET_DAC2 = 0xC6
    CMD_CAN_SET_DAC3 = 0xC7

    CAN_PID_device_ID = 0x91 #PID controller 1

    def __init__(self):
        try:
#            self.candll = cdll.candll
            self.candll = CDLL("candll.dll")
        except:
            print "Can not load candll"
            self.candll = None

        self.handle = None

    def open(self, adapter_name, can_speed):
        f = self.candll.CAN_Open
        f.argtypes = [c_char_p, c_ushort]
        f.restype  = c_void_p

        self.handle = f(c_char_p(adapter_name), c_ushort(can_speed))

        print "handle", self.handle


    def close(self):
        f = self.candll.CAN_Close
        f.argtypes = [c_void_p]
        f.restype  = None

        f(self.handle)
        self.handle = None

    def send_command(self, can_device_id, channel_id, command, param1, param2):

        f = self.candll.CAN_SendCommand
        f.argtypes = [c_void_p, c_ubyte, c_ubyte, c_ubyte, c_ubyte, c_ubyte]
        f.restype  = c_int

        res = c_int(0)
        res = f(self.handle, c_ubyte(can_device_id), c_ubyte(channel_id), c_ubyte(command), c_ubyte(param1), c_ubyte(param2))

        return res

# Not tested yet.
    def send_data(self,  can_device_id, channel_id, buffer):

        f = self.candll.CAN_SendData
        f.argtypes = [c_void_p, c_ubyte, c_ubyte, POINTER(c_ubyte), c_ubyte]
        f.restype  = c_int
        res = c_int(0)

        bufsize  = sizeof(c_ubyte) * len(buffer)
        p_buffer = POINTER(c_ubyte(buffer))
        res = f(self.handle, c_ubyte(can_device_id), c_ubyte(channel_id), c_ubyte(command), c_ubyte(bufsize))

        return res

# Not tested
    def read_data(self, buf, can_device_id, channel_id):

        f = self.candll.CAN_ReadData
        f.argtypes = [c_void_p, POINTER(c_ubyte), c_ubyte, c_ubyte, c_ubyte]
        f.restype  = c_int
        res = c_int(0)

        rx_length  = sizeof(c_ubyte) * len(buf)
        p_buf      = POINTER(c_ubyte(buf))
        res = f(self.handle, p_buf, c_ubyte(can_device_id), c_ubyte(channel_id), c_ubyte(bufsize))


if __name__ == '__main__':
    c = can()
    print c.candll

    c.open("CAN1", 500)

    for dac_value in range (-33000, 34000, 3000):
        lbyte =  dac_value & 0xFF
        hbyte = (dac_value >> 8) & 0xFF;
        c.send_command(c.CAN_PID_device_ID, 0, c.CMD_CAN_SET_DAC0, lbyte, hbyte)
        print "DAC value is", dac_value
        time.sleep(1.0)

    c.close()