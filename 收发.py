from fpioa_manager import fm
from machine import UART
import time

fm.register(7, fm.fpioa.UART1_TX, force=True)
fm.register(10, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1,9600,8,timeout=1000, read_buf_len=4096)

open_str = '1\r\n'
close_str = '2\r\n'
while True:
    read_data = uart_A.read()
    uart_A.write(open_str)
    uart_A.write(close_str)
    if(read_data):
        print(read_data.decode('utf-8'))


