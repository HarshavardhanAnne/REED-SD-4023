#Version 0.2
#Author: Harshavardhan Anne

import serial

class SD_4023(object):
    _baudrate = 9600
    _port = '/dev/ttyUSB0'
    _serialObj = serial.Serial()
    _print_option = 0   #0 = No printing, 1 = console printing
    _data_buffer = [''] * 16
    _buffer_idx = 15
    _status_flag = 1    # 0 = Good, 1 = Bad

    #constructor
    def __init__(self,port,print_opt=None):
        self._port = port
        if print_opt is None:
            self._print_option = 0
        elif int(print_opt) >= 0 and int(print_opt) < 3:
             self._print_option = print_opt
        else:
            print "(SD_4023): Error: print_opt invalid"

    def open(self):
        if (self._print_option): print "(SD_4023): Initializing device"
        self._serialObj.baudrate = self._baudrate
        self._serialObj.port = self._port
        self._serialObj.bytesize = serial.EIGHTBITS
        self._serialObj.parity = serial.PARITY_NONE
        self._serialObj.stopbits = serial.STOPBITS_ONE
        self._serialObj.timeout = 0.3
        #self._serialObj.write_timeout = 0.3

        try:
            self._serialObj.open()
            self._status_flag = 0
            if (self._print_option): print ("(SD_4023): Serial connection established")
        except serial.serialutil.SerialException:
            #logsd.ERROR('Could not open serial port %s' % self._port)
            if (self._print_option): print ("(SD_4023): Could not open serial port %s" % self._port)
            self._status_flag = 1



    def close(self):
        try:
            self._serialObj.close()
            if (self._print_option): print ("(SD_4023): Successfully closed serial port")
        except:
            if (self._print_option): print ("(SD_4023): Could not close port.")

    def read(self):
        if self._serialObj.is_open == True:
            if self._status_flag == 0:
                try:
                    start = False
                    #for i in range(0,16):
                    #    self._data_buffer[i] = ''
                    while (self._buffer_idx >= 0):
                        byte_in = self._serialObj.read()
                        if (byte_in == '\x02'): start = True
                        if start == True:
                            self._data_buffer[self._buffer_idx] = byte_in
                            self._buffer_idx = self._buffer_idx - 1
                    self._buffer_idx = 15
                    return self._data_buffer
                except serial.serialutil.SerialException:
                    if (self._print_option): print "(SD_4023): SERIAL EXCEPTION! Could not read data. Close and reopen the serial connection."
                    self._status_flag = 1

            else:
                if (self._print_option): print "(SD_4023): Status flag == 1: Cannot perform read. Close and open serial port again."
        else:
            if (self._print_option): print "(SD_4023): Serial port not open. Call method open()"
            return None

    def read_decibel(self):
        if self._serialObj.is_open == True:
            if self._status_flag == 0:
                try:
                    self.read()
                    #for i in range(0,16):
                    #    if self._data_buffer[i] == '':
                    #        return None
                    temp_str = self._data_buffer[4] + self._data_buffer[3] + self._data_buffer[2] + '.' + self._data_buffer[1]
                    return float(temp_str)
                except serial.serialutil.SerialException:
                    if (self._print_option): print "(SD_4023): Could not read data. Close and reopen the serial connection."
                    self._status_flag = 1
            else:
                if (self._print_option): print "(SD_4023): Status flag = 1: Cannot perform read. Close and open serial port again."
        else:
            if (self._print_option): print "(SD_4023): Serial port not open. Call method open()"
            return None

    def get_status(self):
        return self._status_flag
