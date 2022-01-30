#!/usr/bin/env python
# -*- coding: utf-8 -*-
import copy
'''
@author: Xing Huang
@date: Jan. 26, 2022
ET2_test common circuit register definition class
'''
#--------------------------------------------------------------------------#
## Manage ET2_test TDC chip's internal registers map
# Allow combining and disassembling individual registers
class ET2_test_comReg_defs(object):
    ## @var _defaultRegMap default register values
    # https://docs.python.org/3/library/stdtypes.html#dict
    # Dictionaries can be created by placing a comma-separated list of key: value pairs within braces.
    _defaultRegMapDict = {
        'Clk1G28_enableRx'          : 0b1       ,
        'Clk1G28_setCM'             : 0b1       ,
        'Clk1G28_enableTerm'        : 0b1       ,
        'Clk1G28_invertData'        : 0b0       , 
        'Clk1G28_equalizer[1:0]'    : 0b00      , 
        'Pulse_enableRx'            : 0b1       ,
        'Pulse_setCM'               : 0b1       ,
        'Pulse_enableTerm'          : 0b1       ,
        'Pulse_invertData'          : 0b0       ,
        'Pulse_equalizer[1:0]'      : 0b00      ,   
        'StrobePulse[7:0]'          : 0b0000_0011,
        'TDC_enable'                : 0b1       ,
        'TDC_resetn'                : 0b1       ,
        'TDC_autoReset'             : 0b0       ,
        'TDC_testMode'              : 0b0       ,
        'TDC_polaritySel'           : 0b1       ,
        'TDC_timeStampMode'         : 0b0       ,
        'TDC_selRawCode'            : 0b0       ,
        'TDC_enableMon'             : 0b0       ,
        'TDC_offset[6:0]'           : 0b000_0000 ,
        'TDC_level[2:0]'            : 0b001     ,
        'DMRO_EnScr'                : 0b1       ,
        'DMRO_REVCLK'               : 0b0       ,
        'DMRO_REVData'              : 0b0       ,
        'DMRO_RSTn'                 : 0b1       ,
        'DMRO_TestMode'             : 0b0       ,
        'DataOut_Sel'               : 0b1       ,
        'DataOut_Ampsel[2:0]'       : 0b111     ,
        'DataOut_disBIAS'           : 0b0       ,
        'TS_PD'                     : 0b0       ,
        'EF_mode[1:0]'              : 0b00      ,
        # 'EF_rstn'                   : 0b1       ,
        # 'EF_en_clk'                 : 0b0       ,
        # 'EF_sel_clk'                : 0b1       ,
        # 'EF_start'                  : 0b0       ,
        # 'EF_TCKHP[3:0]'             : 0b0100    ,
        # 'EF_prog[7:0]'              : 0b0000_0000,
        # 'EF_prog[15:8]'             : 0b0000_0000,
        # 'EF_prog[23:16]'            : 0b0000_0000,
        # 'EF_prog[31:24]'            : 0b0000_0000
    }                                          
    ## @var register map local to the class     

    '''
    https://thispointer.com/python-how-to-copy-a-dictionary-shallow-copy-vs-deep-copy/
    '''

    _regMapDict = {}
    _regMapDict = copy.deepcopy(_defaultRegMapDict)

    def __init__(self):
        self._regMapDict = copy.deepcopy(self._defaultRegMapDict)

    #1 Clk1G28_enableRx     1/0: enable/disable 1.28 GHz clock input eRx
    def set_Clk1G28_enableRx(self, Clk1G28_enableRx_Val):
        self._regMapDict['Clk1G28_enableRx'] = 0x1 & Clk1G28_enableRx_Val

    #2 Clk1G28_setCM    1/0: enable/disable 1.28 GHz clock input eRx common mode voltage
    def set_Clk1G28_setCM(self, Clk1G28_setCM_Val):
        self._regMapDict['Clk1G28_setCM'] = 0x1 & Clk1G28_setCM_Val

    #3 Clk1G28_enableTerm   1/0: enable/disable 1.28 GHz clock input eRx termination.
    def set_Clk1G28_enableTerm(self, Clk1G28_enableTerm_Val):
        self._regMapDict['Clk1G28_enableTerm'] = 0x1 & Clk1G28_enableTerm_Val

    #4 Clk1G28_invertData   1.28 GHz clock input eRx data invert
    def set_Clk1G28_invertData(self, Clk1G28_invertData_Val):
        self._regMapDict['Clk1G28_invertData'] = 0x1 & Clk1G28_invertData_Val

    #5 Clk1G28_equalizer[1:0]   Equalization strength of the 1.28 GHz clock input eRx
    def set_Clk1G28_equalizer(self, Clk1G28_equalizer_Val):
        self._regMapDict['Clk1G28_equalizer[1:0]'] = 0x3 & Clk1G28_equalizer_Val

    #6 Pulse_enableRx   1/0: enable/disable Pulse input eRx
    def set_Pulse_enableRx(self, Pulse_enableRx_Val):
        self._regMapDict['Pulse_enableRx'] = 0x1 & Pulse_enableRx_Val

    #7 Pulse_setCM   1/0: enable/disable Pulse input eRx common mode voltage
    def set_Pulse_setCM(self, Pulse_setCM_Val):
        self._regMapDict['Pulse_setCM'] = 0x1 & Pulse_setCM_Val

    #8 Pulse_enableTerm     1/0: enable/disable Pulse input eRx termination.
    def set_Pulse_enableTerm(self, Pulse_enableTerm_Val):
        self._regMapDict['Pulse_enableTerm'] = 0x1 & Pulse_enableTerm_Val

    #9 Pulse_invertData     Pulse input eRx data invert
    def set_Pulse_invertData(self, Pulse_invertData_Val):
        self._regMapDict['Pulse_invertData'] = 0x1 & Pulse_invertData_Val

    #10 Pulse_equalizer[1:0]    Equalization strength of the Pulse input eRx
    def set_Pulse_equalizer(self, Pulse_equalizer_Val):
        self._regMapDict['Pulse_equalizer[1:0]'] = 0x3 & Pulse_equalizer_Val

    #11 StrobePulse[7:0]    320 MHz clock strobe pulse selection, default calibration width 3.125 ns
    def set_StrobePulse(self, StrobePulse_Val):
        self._regMapDict['StrobePulse[7:0]'] = 0xFF & StrobePulse_Val

    #12 TDC_enable      1/0: enable/disable TDC
    def set_TDC_enable(self, TDC_enable_Val):
        self._regMapDict['TDC_enable'] = 0x1 & TDC_enable_Val

    #13 TDC_resetn      0: external reset TDC
    def set_TDC_resetn(self, TDC_resetn_Val):
        self._regMapDict['TDC_resetn'] = 0x1 & TDC_resetn_Val

    #14 TDC_autoReset   1: auto reset TDC
    def set_TDC_autoReset(self, TDC_autoReset_Val):
        self._regMapDict['TDC_autoReset'] = 0x1 & TDC_autoReset_Val

    #15 TDC_testMode    1: TDC work on test mode (TOA=12.5 ns, TOT=12.5 ns）, 0: TDC work on normal mode.
    def set_TDC_testMode(self, TDC_testMode_Val):
        self._regMapDict['TDC_testMode'] = 0x1 & TDC_testMode_Val

    #16 TDC_polaritySel     TDC controller output signal polarity selection, keep default value 1’b1
    def set_TDC_polaritySel(self, TDC_polaritySel_Val):
        self._regMapDict['TDC_polaritySel'] = 0x1 & TDC_polaritySel_Val

    #17 TDC_timeStampMode   TDC CAL Code output mode, keep default value 1’b0
    def set_TDC_timeStampMode(self, TDC_timeStampMode_Val):
        self._regMapDict['TDC_timeStampMode'] = 0x1 & TDC_timeStampMode_Val

    #18 TDC_selRawCode  TDC Raw code selection, keep default value 1’b0
    def set_TDC_selRawCode(self, TDC_selRawCode_Val):
        self._regMapDict['TDC_selRawCode'] = 0x1 & TDC_selRawCode_Val

    #19 TDC_enableMon   enable/disable TDC raw data output, keep default value 1’b0
    def set_TDC_enableMon(self, TDC_enableMon_Val):
        self._regMapDict['TDC_enableMon'] = 0x1 & TDC_enableMon_Val

    #20 TDC_offset[6:0] TDC metastability window offset, keep default value 7’b0000000
    def set_TDC_offset(self, TDC_offset_Val):
        self._regMapDict['TDC_offset[6:0]'] = 0x7F & TDC_offset_Val

    #21 TDC_level[2:0]  TDC Encoder bubble tolerance level, keep default 3’b001
    def set_TDC_level(self, TDC_level_Val):
        self._regMapDict['TDC_level[2:0]'] = 0x7 & TDC_level_Val

    #22 DMRO_EnScr      1/0: enable/disable DMRO scrambler
    def set_DMRO_EnScr(self, DMRO_EnScr_Val):
        self._regMapDict['DMRO_EnScr'] = 0x1 & DMRO_EnScr_Val

    #23 DMRO_REVCLK     1: revert DMRO 40 MHz clock polarity
    def set_DMRO_REVCLK(self, DMRO_REVCLK_Val):
        self._regMapDict['DMRO_REVCLK'] = 0x1 & DMRO_REVCLK_Val

    #24 DMRO_REVData    1: DMRO output data revert
    def set_DMRO_REVData(self, DMRO_REVData_Val):
        self._regMapDict['DMRO_REVData'] = 0x1 & DMRO_REVData_Val

    #25 DMRO_RSTn       1: DMRO reset, low active
    def set_DMRO_RSTn(self, DMRO_RSTn_Val):
        self._regMapDict['DMRO_RSTn'] = 0x1 & DMRO_RSTn_Val

    #26 DMRO_TestMode   1: DMRO work on test mode （output PRBS7 signal
    def set_DMRO_TestMode(self, DMRO_TestMode_Val):
        self._regMapDict['DMRO_TestMode'] = 0x1 & DMRO_TestMode_Val     
    
    #27 DataOut_Sel     1: eTx output DMRO 1.28 GHz serial data, 0: eTx output 320 MHz strobe pulse
    def set_DataOut_Sel(self, DataOut_Sel_Val):
        self._regMapDict['DataOut_Sel'] = 0x1 & DataOut_Sel_Val

    #28 DataOut_Ampsel[2:0] eTx output amplitude selection
    def set_DataOut_Ampsel(self, DataOut_Ampsel_Val):
        self._regMapDict['DataOut_Ampsel'] = 0x1 & DataOut_Ampsel_Val

    #29 DataOut_disBIAS     1/0：disable/enable eTx current bias
    def set_DataOut_disBIAS(self, DataOut_disBIAS_Val):
        self._regMapDict['DataOut_disBIAS'] = 0x1 & DataOut_disBIAS_Val

    #30 TS_PD   1/0: Temperature sensor power down/up
    def set_TS_PD(self, TS_PD_Val):
        self._regMapDict['TS_PD'] = 0x1 & TS_PD_Val

    #31 EF_mode[1:0]    EFuse mode selection, 0x01: write mode, 0x10: read mode
    def set_EF_mode(self, EF_mode_Val):
        self._regMapDict['EF_mode[1:0]'] = 0x3 & EF_mode_Val

    # #32 EF_rstn	    EFuse reset, low active
    # def set_EF_rstn(self, EF_rstn_Val):
    #     self._regMapDict['EF_rstn'] = 0x1 & EF_rstn_Val

    # #33 EF_en_clk   1/0: enable/disable EFuse input 8 MHz clock
    # def set_EF_en_clk(self, EF_en_clk_Val):
    #     self._regMapDict['EF_en_clk'] = 0x1 & EF_en_clk_Val

    # #34 EF_sel_clk	1/0: select internal 40 MHz divided by 5 or external input 8 MHz clock
    # def set_EF_sel_clk(self, EF_sel_clk_Val):
    #     self._regMapDict['EF_sel_clk'] = 0x1 & EF_sel_clk_Val

    # #35 EF_start	Efuse write/read start signal, high active
    # def set_EF_start(self, EF_start_Val):
    #     self._regMapDict['EF_start'] = 0x1 & EF_start_Val

    # #36 EF_TCKHP[3:0]	EFuse program time setting, EF_TCKHP*0.5 us + 3 us
    # def set_EF_TCKHP(self, EF_TCKHP_Val):
    #     self._regMapDict['EF_TCKHP[3:0]'] = 0xF & EF_TCKHP_Val
    
    # #37 EF_prog[7:0]	EFuse pre-defined program data
    # def set_EF_prog0(self, EF_prog0_Val):
    #     self._regMapDict['EF_prog[7:0]'] = 0xFF & EF_prog0_Val   

    # #38 EF_prog[15:8]	EFuse pre-defined program data
    # def set_EF_prog1(self, EF_prog1_Val):
    #     self._regMapDict['EF_prog[15:8]'] = 0xFF & EF_prog1_Val

    # #39 EF_prog[23:16]	EFuse pre-defined program data
    # def set_EF_prog2(self, EF_prog2_Val):
    #     self._regMapDict['EF_prog[23:16]'] = 0xFF & EF_prog2_Val

    # #40 EF_prog[31:24]	EFuse pre-defined program data
    # def set_EF_prog3(self, EF_prog3_Val):
    #     self._regMapDict['EF_prog[31:24]'] = 0xFF & EF_prog3_Val

    ### get I2C register value
    def get_config_vector(self):
        reg_Val = []
        # 0x0000
        reg_Val += [(self._regMapDict['Clk1G28_equalizer[1:0]'] << 4)   | (self._regMapDict['Clk1G28_invertData'] << 3) | (self._regMapDict['Clk1G28_enableTerm'] << 2) | (self._regMapDict['Clk1G28_setCM'] << 1) | self._regMapDict['Clk1G28_enableRx']]
        # 0x0001
        reg_Val += [(self._regMapDict['Pulse_equalizer[1:0]'] << 4)     | (self._regMapDict['Pulse_invertData'] << 3)   | (self._regMapDict['Pulse_enableTerm'] << 2) | (self._regMapDict['Pulse_setCM'] << 1) | self._regMapDict['Pulse_enableRx']] 
        # 0x0002
        reg_Val += [self._regMapDict['StrobePulse[7:0]']]
        # 0x0003
        reg_Val += [(self._regMapDict['TDC_enableMon'] << 7) | (self._regMapDict['TDC_selRawCode'] << 6) | (self._regMapDict['TDC_timeStampMode'] << 5) | (self._regMapDict['TDC_polaritySel'] << 4) | (self._regMapDict['TDC_testMode'] << 3) | (self._regMapDict['TDC_autoReset'] << 2) | (self._regMapDict['TDC_resetn'] << 1) | self._regMapDict['TDC_enable']]
        # 0x0004
        reg_Val += [self._regMapDict['TDC_offset[6:0]']]
        # 0x0005
        reg_Val += [(self._regMapDict['DMRO_TestMode'] << 7) | (self._regMapDict['DMRO_RSTn'] << 6) | (self._regMapDict['DMRO_REVData'] << 5) | (self._regMapDict['DMRO_REVCLK'] << 4) | (self._regMapDict['DMRO_EnScr'] << 3) | self._regMapDict['TDC_level[2:0]']]
        # 0x0006
        reg_Val += [(self._regMapDict['EF_mode[1:0]'] << 6) | (self._regMapDict['TS_PD'] << 5) | (self._regMapDict['DataOut_disBIAS'] << 4) | (self._regMapDict['DataOut_Ampsel[2:0]'] << 1) | self._regMapDict['DataOut_Sel']]
        # # 0x0007
        # reg_Val += [(self._regMapDict['EF_TCKHP[3:0]'] << 4) | (self._regMapDict['EF_start'] << 3) | (self._regMapDict['EF_sel_clk'] << 2) | (self._regMapDict['EF_en_clk'] << 1) | self._regMapDict['EF_rstn']]
        # # 0x0008
        # reg_Val += [self._regMapDict['EF_prog[7:0]']]
        # # 0x0009
        # reg_Val += [self._regMapDict['EF_prog[15:8]']]        
        # # 0x000A
        # reg_Val += [self._regMapDict['EF_prog[23:16]']]        
        # # 0x000B
        # reg_Val += [self._regMapDict['EF_prog[31:24]']]
        return reg_Val
