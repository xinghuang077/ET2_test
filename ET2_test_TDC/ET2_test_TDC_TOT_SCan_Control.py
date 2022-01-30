#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys
import copy
import time
import visa
import datetime
import struct
import socket
import winsound
import heartrate
from command_interpret import *
from ET2_test_comReg_defs import *
import numpy as np
from command_interpret import *
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.inset_locator import zoomed_inset_axes
from mpl_toolkits.axes_grid1.inset_locator import mark_inset
from usb_iss import UsbIss, defs
import ET2_test_functions
'''
@author: Wei Zhang
@date: 2018-03-20
This script is used for testing ETROC1 TDC chip. The mianly function of this script is I2C write and read, Ethernet communication, instrument control and so on.
'''
hostname = '192.168.2.3'					#FPGA IP address
port = 1024									#port number
#--------------------------------------------------------------------------#
## DDR3 write data to external device
# @param[in] wr_wrap: wrap address
# @param[in] wr_begin_addr: write data begin address
# @param[in] post_trigger_addr: post trigger address
def write_data_into_ddr3(wr_wrap, wr_begin_addr, post_trigger_addr):
    # writing begin address and wrap_around
    val = (wr_wrap << 28) + wr_begin_addr
    cmd_interpret.write_config_reg(8, 0xffff & val)
    cmd_interpret.write_config_reg(9, 0xffff & (val >> 16))
    # post trigger address
    cmd_interpret.write_config_reg(10, 0xffff & post_trigger_addr)
    cmd_interpret.write_config_reg(11, 0xffff & (post_trigger_addr >> 16))
#--------------------------------------------------------------------------#
## DDR3 read data from fifo to ethernet
# @param[in] rd_stop_addr: read data start address
def read_data_from_ddr3(rd_stop_addr):
    cmd_interpret.write_config_reg(12, 0xffff & rd_stop_addr)
    cmd_interpret.write_config_reg(13, 0xffff & (rd_stop_addr >> 16))
    cmd_interpret.write_pulse_reg(0x0020)           # reading start
#--------------------------------------------------------------------------#
## test ddr3
def test_ddr3(data_num):
    cmd_interpret.write_config_reg(0, 0x0000)       # written disable
    cmd_interpret.write_pulse_reg(0x0040)           # reset ddr3 control logic
    time.sleep(0.01)
    print("sent pulse!")

    write_data_into_ddr3(1, 0x0000000, 0x0100000)   # set write begin address and post trigger address and wrap around
    cmd_interpret.write_pulse_reg(0x0008)           # writing start
    time.sleep(0.1)
    cmd_interpret.write_config_reg(0, 0x0001)       # written enable fifo32to256
    time.sleep(0.1)
    cmd_interpret.write_pulse_reg(0x0010)           # writing stop

    time.sleep(0.5)
    cmd_interpret.write_config_reg(0, 0x0000)       # write enable fifo32to256
    time.sleep(0.5)
    read_data_from_ddr3(0x0100000)                  # set read begin address

    data_out = []
    ## memoryview usage
    for i in range(data_num):
        data_out += cmd_interpret.read_data_fifo(50000)           # reading start
    return data_out
#--------------------------------------------------------------------------#
## Enable FPGA Descrambler
def Enable_FPGA_Descrablber(val):
    print("val: %d"%val)
    cmd_interpret.write_config_reg(14, 0x0001 & val)       # write enable
#--------------------------------------------------------------------------#
## main functionl
def main():

    userdefinedir = "TDC_TOT_Scan_Step=2ps_PulseStrobe_0x03"

    ##  Creat a directory named path with date of today
    today = datetime.date.today()
    todaystr = today.isoformat() + "_Standalone_TDC_Test_Results"
    try:
        os.mkdir(todaystr)
        print("Directory %s was created!"%todaystr)
    except FileExistsError:
        print("Directory %s already exists!"%todaystr)
    userdefine_dir = todaystr + "./%s"%userdefinedir
    try:
        os.mkdir(userdefine_dir)
    except FileExistsError:
        print("User define directories already created!!!")

    rm = visa.ResourceManager()
    print(rm.list_resources())
    inst = rm.open_resource('GPIB0::10::INSTR')                 # connect to SOC
    print(inst.query("*IDN?"))                                  # Instrument ID

    inst.write(":OUTPut1:STATE ON")                             # Enable CH1 output
    inst.write(":SOURce:FUNCtion1:SHAPe PULSe")                 # Pulse mode

    ## setting parameters
    Pulse_Strobe = 0x03                 # 0x03: 3.125 ns Cal Code
    Board_Num = 1                       # Board Number
    testMode = 0                        # 0: nromal mode 1: test mode
    polaritySel = 1                     # 0: high power mode, 1: low power mode
    Total_point = 2                   # total fetch data = Total_point * 50000
    fetch_data = 1

    reg_Val = []
    ET2_test_comReg = ET2_test_comReg_defs()

    ## Clock 40MHz TX output setting
    ET2_test_comReg.set_Pulse_enableRx(1)

    ## Data output setting
    ET2_test_comReg.set_DataOut_Ampsel(7)
    ET2_test_comReg.set_DataOut_Sel(1)

    ## Strobe pulse setting
    ET2_test_comReg.set_StrobePulse(Pulse_Strobe)

    ## DMRO setting
    ET2_test_comReg.set_DMRO_TestMode(0)
    ET2_test_comReg.set_DMRO_EnScr(1)           ## enable Scrambler
    Enable_FPGA_Descrablber(1)                  ## Enable FPGA Firmware Descrambler

    ET2_test_comReg.set_DMRO_RSTn(1)
    ET2_test_comReg.set_DMRO_REVCLK(0)

    ## TDC setting
    ET2_test_comReg.set_TDC_resetn(1)
    ET2_test_comReg.set_TDC_testMode(testMode)
    ET2_test_comReg.set_TDC_autoReset(0)
    ET2_test_comReg.set_TDC_enable(1)
    ET2_test_comReg.set_TDC_level(1)

    ET2_test_comReg.set_TDC_polaritySel(polaritySel)       ## 1: low power mode 0: high power mode
    ET2_test_comReg.set_TDC_timeStampMode(0)

    reg_Val = ET2_test_comReg.get_config_vector()

    I2C_Addr = 0x05                                       # I2C slave address
    COM_Port = "COM10"
    Reg_Addr = [0x0000, 0x0001, 0x0002, 0x0003, 0x0004, 0x0005, 0x0006]

    # set usb-iss iic master device
    iss = UsbIss()
    iss.open(COM_Port)
    iss.setup_i2c(clock_khz=100)

    # Check whether a device responds at the specified I2C address.
    if(iss.i2c.test(I2C_Addr)):
        # print("Successful communication with the target via I2C!")
        winsound.PlaySound("SystemExit", winsound.MB_OK)
        print('-------------------------I2C Successful Communication---------------------------')

        #Swap all register addresses in ET2_test chip.
        Reg_Addr_new = ET2_test_functions.regAddrSwap(Reg_Addr)
        iss.i2c.write_ad2(I2C_Addr, Reg_Addr_new[0], reg_Val)
        iic_read_val = iss.i2c.read_ad2(I2C_Addr, Reg_Addr_new[0], len(Reg_Addr))
        if (ET2_test_functions.valueCompare(Reg_Addr, reg_Val, iic_read_val) == 1):
            print('Common-circuit I2C write/read Passed!')
        else:
            print('Common-circuit I2C write/read Failed!')

    else:
        print("Unsuccessful communication with the target via I2C!")
        for i in range(4):                                 
            winsound.Beep(freqency = 1000, duration = 200)
            time.sleep(0.01)


    for m in range(4741,5225):
        width = 0.002 * m             # step = 2 ps.
        print("TOT width: %.3f"%width)
        inst.write(":SOURce:PULSe:WIDTh1 %sns"%width)
        time.sleep(0.01)

        if fetch_data == 1:                 # fetch data switch
            time_stamp = time.strftime('%m-%d_%H-%M-%S',time.localtime(time.time()))
            filename = "TDC_Data_TOT_Width=%.3fns_TestMode=%d_polaritySel=%d_PulseStrobe=%s_B%d_%s_%s.dat"%(width, testMode, polaritySel, hex(Pulse_Strobe), Board_Num, Total_point*50000, time_stamp)
            print(filename)
            with open("./%s/%s/%s"%(todaystr, userdefinedir, filename), 'w') as infile:

                data_out = [0]
                data_out = test_ddr3(Total_point)      # num: The total fetch data num * 50000
                print("Start store data......")

                for i in range(len(data_out)):
                    TDC_data = []
                    for j in range(30):
                        TDC_data += [((data_out[i] >> j) & 0x1)]
                    hitFlag = TDC_data[29]
                    TOT_Code1 = TDC_data[0] << 8 | TDC_data[1] << 7 | TDC_data[2] << 6 | TDC_data[3] << 5 | TDC_data[4] << 4 | TDC_data[5] << 3 | TDC_data[6] << 2 | TDC_data[7] << 1 | TDC_data[8]
                    TOA_Code1 = TDC_data[9] << 9 | TDC_data[10] << 8 | TDC_data[11] << 7 | TDC_data[12] << 6 | TDC_data[13] << 5 | TDC_data[14] << 4 | TDC_data[15] << 3 | TDC_data[16] << 2 | TDC_data[17] << 1 | TDC_data[18]
                    Cal_Code1 = TDC_data[19] << 9 | TDC_data[20] << 8 | TDC_data[21] << 7 | TDC_data[22] << 6 | TDC_data[23] << 5 | TDC_data[24] << 4 | TDC_data[25] << 3 | TDC_data[26] << 2 | TDC_data[27] << 1 | TDC_data[28]
                    infile.write("%3d %3d %3d %d\n"%(TOA_Code1, TOT_Code1, Cal_Code1, hitFlag))

if __name__ == "__main__":
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)	#initial socket
	s.connect((hostname, port))								#connect socket
	cmd_interpret = command_interpret(s)					#Class instance
	main()													#execute main function
	s.close()												#close socket
