from machine import UART
#调用UART类uart 模块主要用于驱动开发板上的异步串口，发送方发出数据后，不等接收方发回响应，接着发送下个数据包的通讯方式。
from board import board_info
#这是一个 MaixPy 板级配置模块，它可以在用户层统一 Python 代码，从而屏蔽许多硬件的引脚差异（不同单片机引脚对应不同）
#他们通过该函数分别进行定义，以找到硬件所对应的引脚
from fpioa_manager import fm
#调用fm这个类,从 fpioa_manager 包导入fm 对象，主要用于引脚和外设的映射

UART1_T=7
UART1_R=8
UART2_T=9
UART2_R=10

# maixduino board_info PIN10/PIN11/PIN12/PIN13 or other hardware IO 10/11/4/3
fm.register(UART1_T, fm.fpioa.UART1_TX, force=True)
fm.register(UART1_R, fm.fpioa.UART1_RX, force=True)
fm.register(UART2_T, fm.fpioa.UART2_TX, force=True)
fm.register(UART2_R, fm.fpioa.UART2_RX, force=True)
'''
register(pin, func, force=True)
pin: 功能映射引脚
function : 芯片功能
force: 强制分配，如果为True，则可以多次对同一个引脚注册;False则不允许同一引脚多次注册。
默认为True是为了方便IDE多次运行程序使用
使用fm(fpioa manager 的缩写)这个内置的对象来注册芯片的外设和引脚的对应关系，
这里　fm.fpioa.GPIO0 是　K210 的一个 GPIO 外设（注意区分 GPIO（外设） 和引脚（实实在在的硬件引脚）的区别 ），
所以把 fm.fpioa.GPIO0 注册到了 引脚 IO6；
'''

uart_A = UART(UART.UART1, 115200, timeout=1000, read_buf_len=4096)
uart_B = UART(UART.UART2, 115200, timeout=1000, read_buf_len=4096)

'''
uart = machine.UART(uart,baudrate,bits,parity,stop,timeout, read_buf_len)
uart UART 号，使用指定的 UART，可以通过 machine.UART. 按tab键来补全
k210 一共有3个 uart，每个 uart 可以进行自由的引脚映射。
baudrate: UART 波特率
bits: UART 数据宽度，支持 5/6/7/8 (默认的 REPL 使用的串口（UARTHS）只支持 8 位模式)， 默认 8
parity: 奇偶校验位，支持 None, machine.UART.PARITY_ODD, machine.UART.PARITY_EVEN
（默认的 REPL 使用的串口（UARTHS）只支持 None）， 默认 None
stop: 停止位， 支持 1， 1.5, 2， 默认 1
timeout: 串口接收超时时间
read_buf_len： 串口接收缓冲，串口通过中断来接收数据，如果缓冲满了，将自动停止数据接收
'''

write_str = 'hello world'
for i in range(20):##当range函数中只有一个数字时，则默认该数字为终止数字，默认起始数字为0，步距为1
    uart_A.write(write_str)#write#用于使用串口发送数据
    read_data = uart_B.read()#read#用于读取串口缓冲中的数据
    if read_data:
        read_str = read_data.decode('utf-8')
        '''
        decode()函数
        描述：以 encoding 指定的编码格式解码字符串，默认编码为字符串编码。
        encoding ——要使用的编码，如：utf-8,gb2312,cp936,gbk等。
        errors ——设置不同解码错误的处理方案。默认为 'strict',意为编码错误引起一个 UnicodeDecodeError。
        其它可能得值有 'ignore', 'replace'以及通过 codecs.register_error() 注册的1其它值。
        语法：str.decode(encoding='utf-8', errors='strict')
        '''

        print("string = ", read_str)
        if read_str == write_str:
            print("baudrate:115200 bits:8 parity:0 stop:0 ---check Successfully")


uart_A.deinit()
uart_B.deinit()

'''
注销 UART 硬件，释放占用的资源
'''
del uart_A
del uart_B
'''
删除变量uart_A，解除uart_A对UART的引用
'''
