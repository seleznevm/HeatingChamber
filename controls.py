import modbus_tk
from modbus_tk import modbus_tcp
from modbus_tk import utils
import modbus_tk.defines as cst

PET7017 = modbus_tcp.TcpMaster('10.0.1.217')
PET7017.set_timeout(5)
PET7215 = modbus_tcp.TcpMaster('10.0.1.96')
PET7215.set_timeout(5)

def turnHeaterOn():
    PET7017.execute(1,cst.WRITE_SINGLE_COIL,1,1,1)

def turnHeaterOff():
    PET7017.execute(1,cst.WRITE_SINGLE_COIL,1,1,0)

def turnFanOn():
    PET7017.execute(1,cst.WRITE_SINGLE_COIL,0,1,1)

def turnFanOff():
    PET7017.execute(1,cst.WRITE_SINGLE_COIL,0,1,0)

def getTemp():
    a = PET7215.execute(1,cst.READ_INPUT_REGISTERS,0,1,0)
    return a
