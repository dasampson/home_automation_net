#!/usr/bin/python

import time
import smbus
from ctypes import c_short
from ctypes import c_byte
from ctypes import c_ubyte

I2C_ADDRESS = 0x77
bus = smbus.SMBus(1)

def getShort(data, index):
    return c_short((data[index+1] << 8) + data[index]).value

def getUShort(data, index):
    return (data[index+1] << 8) + data[index]

def getChar(data,index):
    result = data[index]
    if result > 127:
        result -= 256
    return result

def getUChar(data,index):
    result =  data[index] & 0xFF
    return result

def readAllSensors(addr=I2C_ADDRESS):
    REGISTER_DATA = 0xF7
    REGISTER_CONTROL = 0xF4
    REGISTER_CONFIG  = 0xF5
    REGISTER_CONTROL_HUM = 0xF2
    REGISTER_HUM_MSB = 0xFD
    REGISTER_HUM_LSB = 0xFE
    OVERSAMPLE_TEMP = 2
    OVERSAMPLE_PRES = 2
    MODE = 1
    OVERSAMPLE_HUM = 2

    bus.write_byte_data(addr, REGISTER_CONTROL_HUM, OVERSAMPLE_HUM)
    control = OVERSAMPLE_TEMP << 5 | OVERSAMPLE_PRES << 2 | MODE
    bus.write_byte_data(addr, REGISTER_CONTROL, control)
  
    cal1 = bus.read_i2c_block_data(addr, 0x88, 24)
    cal2 = bus.read_i2c_block_data(addr, 0xA1, 1)
    cal3 = bus.read_i2c_block_data(addr, 0xE1, 7)
    dig_T1 = getUShort(cal1, 0)
    dig_T2 = getShort(cal1, 2)
    dig_T3 = getShort(cal1, 4)
    dig_P1 = getUShort(cal1, 6)
    dig_P2 = getShort(cal1, 8)
    dig_P3 = getShort(cal1, 10)
    dig_P4 = getShort(cal1, 12)
    dig_P5 = getShort(cal1, 14)
    dig_P6 = getShort(cal1, 16)
    dig_P7 = getShort(cal1, 18)
    dig_P8 = getShort(cal1, 20)
    dig_P9 = getShort(cal1, 22)
    dig_H1 = getUChar(cal2, 0)
    dig_H2 = getShort(cal3, 0)
    dig_H3 = getUChar(cal3, 2)
    dig_H4 = getChar(cal3, 3)
    dig_H4 = (dig_H4 << 24) >> 20
    dig_H4 = dig_H4 | (getChar(cal3, 4) & 0x0F)
    dig_H5 = getChar(cal3, 5)
    dig_H5 = (dig_H5 << 24) >> 20
    dig_H5 = dig_H5 | (getUChar(cal3, 4) >> 4 & 0x0F)
    dig_H6 = getChar(cal3, 6)
  
    wait_time = 1.25 + (2.3 * OVERSAMPLE_TEMP) + ((2.3 * OVERSAMPLE_PRES) + 0.575) + ((2.3 * OVERSAMPLE_HUM)+0.575)
    time.sleep(wait_time/1000) 
  
    data = bus.read_i2c_block_data(addr, REGISTER_DATA, 8)
    raw_pressure = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
    raw_temperature = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
    raw_humidity = (data[6] << 8) | data[7]
  
    var1 = ((((raw_temperature>>3)-(dig_T1<<1)))*(dig_T2)) >> 11
    var2 = (((((raw_temperature>>4) - (dig_T1)) * ((raw_temperature>>4) - (dig_T1))) >> 12) * (dig_T3)) >> 14
    t_fine = var1+var2
    temperature_c = float(((t_fine * 5) + 128) >> 8);
    temperature = ((temperature_c/100.0) * 9/5) + 32
  
    var1 = t_fine / 2.0 - 64000.0
    var2 = var1 * var1 * dig_P6 / 32768.0
    var2 = var2 + var1 * dig_P5 * 2.0
    var2 = var2 / 4.0 + dig_P4 * 65536.0
    var1 = (dig_P3 * var1 * var1 / 524288.0 + dig_P2 * var1) / 524288.0
    var1 = (1.0 + var1 / 32768.0) * dig_P1

    pressure = 1048576.0 - raw_pressure
    pressure = ((pressure - var2 / 4096.0) * 6250.0) / var1
    var1 = dig_P9 * pressure * pressure / 2147483648.0
    var2 = pressure * dig_P8 / 32768.0
    pressure = pressure + (var1 + var2 + dig_P7) / 16.0
    pressure = pressure/100.0
  
    humidity = t_fine - 76800.0
    humidity = (raw_humidity - (dig_H4 * 64.0 + dig_H5 / 16384.0 * humidity)) * (dig_H2 / 65536.0 * (1.0 + dig_H6 / 67108864.0 * humidity * (1.0 + dig_H3 / 67108864.0 * humidity)))
    humidity = humidity * (1.0 - dig_H1 * humidity / 524288.0)
    if humidity > 100:
        humidity = 100
    elif humidity < 0:
        humidity = 0
  
    return temperature, pressure, humidity
  
def main():
    temperature, pressure, humidity = readAllSensors()
    print "Ambient Temperature: ", temperature, u'\N{DEGREE SIGN}' + "F"
    print "Barometric Pressure: ", pressure, "hPa"
    print "Relative Humidity:   ", humidity, "%"

if __name__ == "__main__":
    main()
