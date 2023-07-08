## Untitled - By: User - 周日 4月 23 2023
import time
from machine import UART #串口库函数
from fpioa_manager import fm # GPIO重定向函数

fm.register(18, fm.fpioa.UART1_TX, force=True)
uart_A = UART(UART.UART1, 115200, 8, 0, 1, timeout=1000, read_buf_len=4096)


def sending_data(x,y,z):
    FH = bytearray([0x2C,0x12,x,y,z,0x5B])
    uart_A.write(FH);

Cx = 0
Cy = 0
Cz = 0

while True:

    Cx+=1;
    Cy+=1;
    Cz+=1;
    sending_data(Cx,Cy,Cz)
    print("Cx:",Cx,"Cy",Cy,"Cz:",Cz)
    time.sleep_ms(1000)
