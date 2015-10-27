#!/usr/bin/env python
# encoding: utf-8

"""MPC04 Python driver by ctypes
"""

import ctypes
from ctypes import byref

import sys

mpc04 = ctypes.CDLL('./Mpc04Api.dll')


def Init():
    mpc04.MPC_Initialize()

    i = ctypes.c_int8(0)
    mpc04.MPC_GetNumberOfDevices(byref(i))
    device_num = i.value
    print device_num

    if (device_num > 0):
        arr = ctypes.c_int * device_num
        device_arr = arr()

        mpc04.MPC_GetDeviceSerialNumList(byref(device_arr))

        for device_sn in device_arr:
            print device_sn
            device_handle = ctypes.c_int(0)
            mpc04.MPC_GetMpcDeviceHandle(device_sn, byref(device_handle))
            print device_handle.value
            mpc04.MPC_Connect(device_handle)
            print mpc04.MPC_IsConnected(device_handle)
        return device_handle
    return None


def PowerOn(handle):

    vdd_mV = 1800
    vio_mV = 1800
    vled_mV = 3300
    vddh_mV = 3300
    delay = 2000
    result = mpc04.MPC_SetVoltages(handle, vdd_mV, vio_mV, vled_mV, vddh_mV, delay)
    print result


def PowerOff(handle):

    delay = 2000
    result = mpc04.MPC_SetVoltages(handle, 0, 0, 0, 0, delay)
    print result


if __name__ == "__main__":

    device_handle = Init()
    PowerOn(device_handle)
