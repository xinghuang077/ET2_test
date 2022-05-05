# import pandas as pdc
import os
import sys
import time
from usb_iss import UsbIss, defs
import ET2_test_functions
import numpy as np
import datetime

'''
@author: Xing Huang
@date: Jan. 7, 2021
This script as a generic I2C cofniguration software to configure I2C slave. The I2C reg configuration data is read into a xxx.dat file.
The UsbIss as I2C master deivce is used to write and read I2C slave register.
'''


#-----------------------------------------------------------------------------------#
freqency = 1000
duration = 200
#-----------------------------------------------------------------------------------#
def main():
    user_config_filename = "ET2_Config_SEUTest.txt" 
    COM_Port = "COM4"

    # All of the register addresses, and default values 
    Reg_Addr = []
    Reg_Val_Default = []
    Reg_Val_Write = []
    Reg_Val_Broadcast = []      

    # Read configuraton file, I2C address, 16-bit register addresses, 8-bit register values
    with open(user_config_filename, 'r') as infile:                  # read configuration file
        for line in infile.readlines():
            if len(line.split()) == 1:
                #print(len(line.split()))                          # read I2C address
                I2C_Addr = int(line.split()[0], 16)
            else:                                               # read register address and value
                Reg_Addr += [int(line.split()[0], 16)]
                Reg_Val_Default += [int(line.split()[1], 16)]
                Reg_Val_Write += [int(line.split()[2], 16)]
                Reg_Val_Broadcast += [int(line.split()[3], 16)]
    print('There are', len(Reg_Addr), 'registers in ET2_test chip.')
    
    # Power Supply USB devices
    # VISA_ADDRESS = ET2_test_functions.find('USB?*INSTR')
    ET2_test_functions.find('USB?*INSTR')

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    # Check whether a device responds at the specified I2C address.
    if(not iss.i2c.test(I2C_Addr)):
        print("Unsuccessful communication with the target via I2C!")
        return
    print("Successful communication with the target via I2C!")

    #Swap all register addresses in ET2_test chip.
    Reg_Addr_new = ET2_test_functions.regAddrSwap(Reg_Addr)
    # print("reg addr swapped")

    writeVal = []
    readVal = []
    # for i in range(len(Reg_Addr)):
        # if((0 <= i <=255) | (512 <= i <= 563)):
    for i in list(range(0, 8)) + list(range(120, 128)) + list(range(128, 136)) + list(range(248, 256)) + list(range(512, 524)):
        # print(i, hex(Reg_Addr[i]))
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[i], [Reg_Val_Write[i]])
        writeVal.append(Reg_Val_Write[i])
        readVal += (iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1))
    # print("writing done", readVal)
    # print(writeVal)
    
    if readVal == writeVal :
        lasttime = datetime.datetime.now()
        print("%s I2C Written and Read-back values matched as expected! \n%s" %(lasttime, '[{}]'.format(', '.join(hex(x) for x in readVal))))
    else:
        for i in list(range(0, 8)) + list(range(120, 128)) + list(range(128, 136)) + list(range(248, 256)) + list(range(512, 520)):
            if readVal[i] != writeVal[i]:
                print("%d %x %x %x" %(i, Reg_Addr[i], writeVal[i], readVal[i]))

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()