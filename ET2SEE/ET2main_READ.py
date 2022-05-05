# import pandas as pdc
import os
import pyvisa as visa
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
    user_config_filename = "ET2_Config_SEUTest.txt" ## ET2_Config_SEUTest modified the line 520, 521 for SEU test based on ET2_Config.txt
    COM_Port = "COM4"
    
    # value = input("Please enter the number of the ET2_test board you are testing:\n")

    ## All of the register addresses, and default values 
    Reg_Addr = []
    Reg_Val_Default = []
    Reg_Val_Write = []
    Reg_Val_Broadcast = []      

    ## Read configuraton file, I2C address, 16-bit register addresses, 8-bit register values
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

    ## Power Supply USB devices
    VISA_ADDRESS = ET2_test_functions.find('USB?*INSTR')

    ## set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    ## Check whether a device responds at the specified I2C address.
    if(not iss.i2c.test(I2C_Addr)):
        print("Unsuccessful communication with the target via I2C!")
        return
    print("Successful communication with the target via I2C!")

    ## Swap all register addresses in ET2_test chip.
    Reg_Addr_new = ET2_test_functions.regAddrSwap(Reg_Addr)
    # print("reg addr swapped") 
     

    while True:
       ###################################################################################################### 
       # Pixel configuration registers write and read back to compare the write-in and read-back values
       ######################################################################################################
        myAddr = []
        myreadVal = []              
        expectedVal = []
        for i in list(range(0, 8)) + list(range(120, 128)) + list(range(128, 136)) + list(range(248, 256)) + list(range(512, 524)):
            myAddr += [Reg_Addr[i]]
            expectedVal += [Reg_Val_Write[i]]
            myreadVal += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1) 
            # print("%d %x %x" %(i, Reg_Addr[i], Reg_Val_Write[i]))
        #end for

       ######################################################################################################
       ## SEU Counter Read
       ######################################################################################################
        seuCntAddr = []
        seuCntVal = []
        for i in list(range(560, 564)):
            seuCntAddr += [Reg_Addr[i]]
            # print(hex(Reg_Addr[i]))
            seuCntVal += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1) 
        # print("%s" %( lasttime), "SEU counter Addresses:", '[{}]'.format(', '.join(hex(x) for x in seuCntAddr)), "Values:", "%s" %( serCntVal))
        # print("%s The SEU counter in ET2_test I2C, address & value %s %s" %(lasttime, seuCntAddr, serCntVal))
        #end for


       ######################################################################################################
       ## Variable Status Read
       ######################################################################################################
        statusVarAddr = []
        statusVarReadVal = []              
        statusVarExpectedVal = []
        for i in list(range(256, 264)) + list(range(376, 392)) +  list(range(504, 512)):
        # for i in list(range(504, 512)):
            # print(hex(Reg_Addr[i]))
            statusVarAddr += [Reg_Addr[i]]
            # statusVarExpectedVal += [Reg_Val_Default[i]]
            statusVarReadVal += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1) 
            # print("%d %x %x" %(i, Reg_Addr[i], Reg_Val_Write[i]))
            
        statusVarExpectedVal = []
        regAddr = []
        regReadVal = []
        for i in list(range(0, 8)) + list(range(120, 128)) + list(range(128, 136)) + list(range(248, 256)) + list(range(512, 520)):
            regAddr += [Reg_Addr[i]]
            regReadVal += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
        # print(regReadVal[0], statusVarReadVal[0])
        statusVarExpectedVal = [regReadVal[0] ^ 0x00,  regReadVal[1] ^ 0xff,  regReadVal[2] ^ 0xff,  regReadVal[3] ^ 0xff, \
                                regReadVal[4] ^ 0xff,  regReadVal[5] ^ 0xff,  regReadVal[6] ^ 0xff,  regReadVal[7] ^ 0xff, \
                                regReadVal[8] ^ 0x0f,  regReadVal[9] ^ 0xff,  regReadVal[10] ^ 0xff, regReadVal[11] ^ 0xff, \
                                regReadVal[12] ^ 0xff, regReadVal[13] ^ 0xff, regReadVal[14] ^ 0xff, regReadVal[15] ^ 0xff, \
                                regReadVal[16] ^ 0xf0, regReadVal[17] ^ 0xff, regReadVal[18] ^ 0xff, regReadVal[19] ^ 0xff, \
                                regReadVal[20] ^ 0xff, regReadVal[21] ^ 0xff, regReadVal[22] ^ 0xff, regReadVal[23] ^ 0xff, \
                                regReadVal[24] ^ 0xff, regReadVal[25] ^ 0xff, regReadVal[26] ^ 0xff, regReadVal[27] ^ 0xff, \
                                regReadVal[28] ^ 0xff, regReadVal[29] ^ 0xff, regReadVal[30] ^ 0xff, regReadVal[31] ^ 0xff]
        # print(statusVarExpectedVal, "\n", statusVarReadVal) 
    

       ######################################################################################################
       ## Stasus Read
       ######################################################################################################
        statusAddr = []
        statusReadVal = []              
        statusExpectedVal = []
        for i in list(range(8, 120)) + list(range(136, 248)) + list(range(264, 376)) +  list(range(392, 504)):
            statusAddr += [Reg_Addr[i]]
            statusExpectedVal += [Reg_Val_Default[i]]
            statusReadVal += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1) 
            # print("%d %x %x" %(i, Reg_Addr[i], Reg_Val_Write[i]))


       ######################################################################################################
       ## E-Fuse Read
       ######################################################################################################
        ## efuse config registers
        efuseConfigAddr = []
        efuseConfigWrite = []
        efuseConfigRead = []
        for i in list(range(518, 520)):
            # print(hex(Reg_Addr[i]))
            efuseConfigAddr += [Reg_Addr_new[i]]
            efuseConfigWrite += [Reg_Val_Default[i]]
            efuseConfigRead += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)  
            
        efMode = 0b10                   # 0b10 read mode, 0b01 write mode
        tsPD = 0b0
        dataOut_disBias = 0b0
        dataOut_AmpSel = 0b111
        dataOut_Sel = 0b1

        efTckhp = 0b0100                # 4'b0100 ~ 5 us
        efStart = 0b0                  # start = 1
        efClkSel = 0b0
        efClkEn = 0b1
        efRstN = 0b1
        # efProg_preDef = 0x0000_0000     #32'h0001
        Reg6 = (efMode << 6) + (tsPD << 5) +(dataOut_disBias << 4) +(dataOut_AmpSel <<1) + (dataOut_Sel)
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
    
        ##0. Write the initialization of eFuse configuration registers.
        # iss.i2c.write_ad2(I2C_Addr, efuseConfigAddr[0], [Reg6, Reg7])
        # print('[{}]'.format(', '.join(hex(x) for x in iss.i2c.read_ad2(I2C_Addr, efuseConfigAddr[0], 2))))
        ##1. Reset the eFuse after the initialization.
        efRstN = 0b0 # reset = 0
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, efuseConfigAddr[1], [Reg7])    
        efRstN = 0b1 # reset = 1
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, efuseConfigAddr[1], [Reg7])
        ##2. Write start a pulse to generate the falling edge.
        efStart = 0b0 # start = 0
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, efuseConfigAddr[1], [Reg7]) 
        efStart = 0b1 # start = 1
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, efuseConfigAddr[1], [Reg7]) 
        efStart = 0b0 # start = 0
        Reg7 = (efTckhp << 4) + (efStart << 3) + (efClkSel << 2) + (efClkEn << 1) + efRstN
        iss.i2c.write_ad2(I2C_Addr, efuseConfigAddr[1], [Reg7])   
        ##3. After writing the eFuse, read back the values of eFuse.
        # Registers' addresses are 0x0100, 0x0101, 0x0102, 0x0103.        
        efuseReadVal = []              
        efuseExpectedVal = []
        ## Registers stored the efule values
        for i in list(range(572, 576)):
            # print(hex(Reg_Addr[i]))
            efuseExpectedVal += [Reg_Val_Write[i]]
            efuseReadVal += iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[i], 1)
        # print('[{}]'.format(', '.join(hex(x) for x in efuseExpectedVal)),\
        #       '[{}]'.format(', '.join(hex(x) for x in efuseReadVal)))
        # print(efuseExpectedVal, efuseReadVal)
        ##Rewrite the Reg6/Reg7 to the write value
        # iss.i2c.write_ad2(I2C_Addr, 0x0600, [0xDC])
        # iss.i2c.write_ad2(I2C_Addr, 0x0700, [0xFE])        


       ######################################################################################################
       ## Power Supply Source Current Read
       ######################################################################################################
        ## Change this variable to the address of your instrument
        # VISA_ADDRESS = 'USB0::0x2A8D::0x1102::MY58041593::INSTR'
                # print(VISA_ADDRESS)
        try:
            ## Create a connection (session) to the instrument
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(VISA_ADDRESS)    # connect to SOC
            # print(session.query("*IDN?"))
        except visa.Error as ex:
            print('Couldn\'t connect to \'%s\', exiting now...' % VISA_ADDRESS)
            sys.exit()
        # session.write("SOURce:VOLTage %.3f,(@1)"%(1.2))                         # Channel One Power Voltage Setting
        current_Ch1 = round(float(session.query("MEAS:CURR? CH1"))*1000000.0, 3)   # Channel One Current Reading
        # ## Close the connection to the instrument
        # session.close()
        # resourceManager.close()
       
       
       ######################################################################################################
       ## Info Printing and Output to txt file
       ######################################################################################################
        with open("./DATA/ET2_I2C_EFUSE_register.TXT", 'a') as infile_iic:  
            lasttime = datetime.datetime.now()
            if expectedVal == myreadVal :
                print("%s \nI2C Written == Read: %s\nSEU counter values:%s\n" % (lasttime, '[{}]'.format(', '.join(hex(x) for x in myreadVal)), '[{}]'.format(', '.join(hex(x) for x in seuCntVal))))
                infile_iic.write("%s \nI2C Written == Read: %s\nSEU counter values:%s\n" % (lasttime, '[{}]'.format(', '.join(hex(x) for x in myreadVal)), '[{}]'.format(', '.join(hex(x) for x in seuCntVal))))
            else:
                print("%s \nI2C Written != Read: %s\nSEU counter values:%s\n" % (lasttime, '[{}]'.format(', '.join(hex(x) for x in myreadVal)), '[{}]'.format(', '.join(hex(x) for x in seuCntVal))))
                infile_iic.write("%s \nI2C Written != Read: %s\nSEU counter values:%s\n" % (lasttime, '[{}]'.format(', '.join(hex(x) for x in myreadVal)), '[{}]'.format(', '.join(hex(x) for x in seuCntVal))))
            # end if mywriteval == myreadval

            if statusVarExpectedVal == statusVarReadVal :
                print("I2C Variable Status Expected == Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusVarReadVal))))
                infile_iic.write("I2C Variable Status Expected == Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusReadVal))))
            else:
                print("I2C Variable Status Expected != Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusVarReadVal))))
                infile_iic.write("I2C Variable Status Default != Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusReadVal))))
            # end if statusVarExpectedVal == statusVarReadVal

            if statusExpectedVal == statusReadVal :
                print("I2C Fixed Status Default == Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusReadVal))))
                infile_iic.write("I2C Fixed Status Default == Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusReadVal))))
            else:
                print("I2C Fixed Status Default != Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusReadVal))))
                infile_iic.write("I2C Fixed Status Default != Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in statusReadVal))))
            # end if statusExpectedVal == statusReadVal
                
            if efuseExpectedVal == efuseReadVal :
                print("E-Fuse values of B1/9 Expected == Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in efuseReadVal))))
                infile_iic.write("E-Fuse values of B1/9 Expected == Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in efuseReadVal))))
            else:
                print("E-Fuse values of B1/9 Expected != Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in efuseReadVal))))
                infile_iic.write("E-Fuse values of B1/9 Expected != Read: %s\n" % ('[{}]'.format(', '.join(hex(x) for x in efuseReadVal))))
            # end if efuseExpectedVal == efuseReadVal
            infile_iic.flush()
        # end with
                      
        with open("./DATA/ET2_I2C_EFUSE_current.TXT", 'a') as infile_current:  
            lasttime = datetime.datetime.now()
            print("%s %d uA\n" % (lasttime, current_Ch1))
            infile_current.write("%s %d uA\n" % (lasttime, current_Ch1) )
        # end with

        time.sleep(15) 
    # end while 
# end def main

#-----------------------------------------------------------------------------------#
if __name__ == '__main__':
    main()