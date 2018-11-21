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

chamber = (TChamber_controls)
chamber.setpoint = 50
chamber.mode = 0

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

def debug():
    while True:
        chamber.mode = slave.get_values('1', 3, 1)
        chamber.mode = int(chamber.mode[0])
        chamber.setpoint = slave.get_values('2', 1, 1)
        chamber.setpoint = int(chamber.setpoint[0])
        print(chamber.mode)
        print(chamber.setpoint)
        time.sleep(1)

def main():
    logger = modbus_tk.utils.create_logger(name='console')
    try:
        server = modbus_tcp.TcpServer()
        logger.info('Modbus server is running...')
        server.start()
        global slave
        slave = server.add_slave(1)
        slave.add_block('1', cst.COILS, 0, 10)
        slave.add_block('2', cst.HOLDING_REGISTERS,0,10)
        print(chamber.setpoint) #debug
        print(chamber.mode) #debug
    except:
        logger.info("Can't start modbus server")

    t1 = threading.Thread(target=debug)
    t1.start()


if __name__ == '__main__':  # Если мы запускаем файл напрямую, а не импортируем
    main()  # то запускаем функцию main()

################################
#  Modbus Slave registers map  #
#______________________________#
#
#       Coils (0-100)
#   №  |   Description
#   1   | heater
#   2   | fan
#   3   | mode
#
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
#   1   | setpoint
#   2   |
#
#
