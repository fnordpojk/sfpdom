#! /usr/bin/python
from __future__ import absolute_import
from six.moves import range
try:
	import pprint
	import smbus
	from sff8472 import sff8472Dom
	from sff8472 import sff8472InterfaceId

except ImportError as e:
    raise ImportError (str(e) + "- required module not found")



if_address = 0x50
dom_address = 0x51
bus = smbus.SMBus(5)

def read_eeprom(address,len=256,offset=0):
	ret = []
	for i in range(0,len):
		byte = bus.read_byte_data(address, i+offset)
		ret.append(hex(byte)[2:].zfill(2))
	return ret

eeprom_if = read_eeprom(if_address)
eeprom_dom = read_eeprom(dom_address)

sfp_data = {}

sfpi_obj = sff8472InterfaceId(eeprom_if)
if sfpi_obj != None:
  sfp_data['interface'] = sfpi_obj.get_data_pretty()
  cal_type = sfpi_obj.get_calibration_type()

sfpd_obj = sff8472Dom(eeprom_dom, cal_type)
if sfpd_obj != None:
  sfp_data['dom'] = sfpd_obj.get_data_pretty()

pp = pprint.PrettyPrinter(indent=4)
pp.pprint(sfp_data)