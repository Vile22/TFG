#!/usr/bin/env python3

from pypozyx import (POZYX_POS_ALG_UWB_ONLY, POZYX_2D, POZYX_3D, Coordinates, POZYX_SUCCESS, PozyxConstants, version,
                     DeviceCoordinates, PozyxSerial, get_first_pozyx_serial_port, SingleRegister, DeviceList, PozyxRegisters)

data = [0,0,0,0,0]
remote_id = 0x6833
serial_port = get_first_pozyx_serial_port()
pozyx = PozyxSerial(serial_port)

pozyx.getRead(PozyxRegisters.WHO_AM_I, data, remote_id=remote_id)
print('who am i: 0x%0.2x' % data[0])
print('firmware version: 0x%0.2x' % data[1])
print('hardware version: 0x%0.2x' % data[2])
print('self test result: %s' % bin(data[3]))
print('error: 0x%0.2x' % data[4])