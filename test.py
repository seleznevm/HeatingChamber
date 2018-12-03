from statistics import mode

import modbus_tk
from modbus_tk import modbus_tcp
from modbus_tk import utils
import modbus_tk.defines as cst
import sys
import threading
import time

class TChamber_controls:
    def __init__(self):
        self.setpoint = setpoint
        self.mode = mode
        self.operate = operate

chamber = (TChamber_controls)
chamber.setpoint = 50
chamber.mode = 0
chamber.operate = 0

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
    a = a[0]/100
    return a

def temperature_control():
    while True:
        # print(chamber.mode)       #debug
        # print(chamber.operate)    #debug
        chamber.mode = slave.get_values('2', 2, 1)
        chamber.mode = int(chamber.mode[0])
        chamber.operate = slave.get_values('1', 1, 1)
        chamber.operate = int(chamber.operate[0])
        if chamber.mode == 1 and chamber.operate == 1:
            temperature = getTemp()
            chamber.setpoint = slave.get_values('2', 1, 1)
            chamber.setpoint = int(chamber.setpoint[0])
            if temperature > chamber.setpoint:
                turnFanOn()
                turnHeaterOff()
                time.sleep(1)
            elif temperature < chamber.setpoint:
                turnHeaterOn()
                turnFanOff()
                time.sleep(1)
        elif chamber.operate == 0:
            turnHeaterOff()
            turnFanOff()

def main():
    logger = modbus_tk.utils.create_logger(name='console')
    try:
        server = modbus_tcp.TcpServer()
        logger.info('Modbus server is running...')
        server.start()
        global slave
        slave = server.add_slave(1)
        slave.add_block('1', cst.COILS, 0, 10)              #add COILS
        slave.add_block('2', cst.HOLDING_REGISTERS,0,10)    #add HOLDING REGISTERS
    except:
        logger.info("Can't start modbus server")

    t1 = threading.Thread(target=temperature_control)
    t1.start()

if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

################################
#  Modbus Slave registers map  #
#______________________________#
#
#       Coils (0-100)
#   №  |   Description
#   1   |
#   2   | operate
#   3   |
#   4   |
#
#
#
#
#
#
#       | Standard mode on/off
#
#       Holding registers       #
#   №  |   Description
#   1   |
#   2   | setpoint
#   3   | mode
#
