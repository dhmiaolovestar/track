import sensor#摄像头
import image#图像传感器
import lcd#屏幕
import time
from fpioa_manager import fm
#调用fm这个类,从 fpioa_manager 包导入fm 对象，主要用于引脚和外设的映射
from Maix import GPIO
#调用GPIO这个类,从包 Maix 导入了 GPIO 这个类， GPIO 外设相关操作

xl_place=7
xr_place=8
yu_place=9
yd_place=10
#定义四个个变量，其中两个值为6，7，即Pin6/IO6，Pin7/IO7，通过这两个引脚分别将色块中心x位置偏离中心发送
fm.register(xl_place,fm.fpioa.GPIO0)
fm.register(xr_place,fm.fpioa.GPIO1)
fm.register(yu_place,fm.fpioa.GPIO2)
fm.register(yd_place,fm.fpioa.GPIO3)
#将前一个值赋予GPIO0，使GPIO0控制一个值对应的引脚
#调用register函数将引脚与具体的硬件功能（GPIO/I2C/UART/SPIU）绑定
#不用时可以用unregister函数进行解绑
'''
使用fm(fpioa manager 的缩写)这个内置的对象来注册芯片的外设和引脚的对应关系，
这里　fm.fpioa.GPIO0 是　K210 的一个 GPIO 外设（注意区分 GPIO（外设） 和引脚（实实在在的硬件引脚）的区别 ），
所以把 fm.fpioa.GPIO0 注册到了 引脚 IO6；
'''

xl_place=GPIO(GPIO.GPIO0,GPIO.OUT)
xr_place=GPIO(GPIO.GPIO1,GPIO.OUT)
yu_place=GPIO(GPIO.GPIO2,GPIO.OUT)
yd_place=GPIO(GPIO.GPIO3,GPIO.OUT)
#实例名=类名（ID, MODE, PULL）省略了PULL这个实例类型
#然后定义一个 GPIO 对象led_r

lcd.init()
'''
lcd.init(type=1, freq=15000000, color=lcd.BLACK, invert = 0, lcd_type = 0)#
初始化 LCD 屏幕显示
1.1.1. 参数#
type： 设备的类型（保留给未来使用）:
0: None
1: lcd shield（默认值）
2: Maix Cube
5: sipeed rgb 屏转接板
type 是键值参数，必须在函数调用中通过写入 type= 来显式地调用
freq： LCD （实际上指 SPI 的通讯速率） 的频率
color： LCD 初始化的颜色， 可以是 16 位的 RGB565 颜色值，比如 0xFFFF；
或者 RGB888 元组， 比如 (236, 36, 36)， 默认 lcd.BLACK
invert: LCD 反色显示
lcd_type: lcd 类型：
0: 默认类型
'''
sensor.reset()
#初始化单目摄像头
sensor.set_pixformat(sensor.RGB565)
#设置帧格式：MaixPy开发板配置的屏幕使用的是RGB565，推荐设置为RGB565格式
sensor.set_framesize(sensor.QVGA)
#设置帧大小：MaixPy开发板配置的屏幕是320*240分辨率，推荐设置为QVGA格式
sensor.run(1)
#摄像头，启动
#初始化

#lcd.rotation(2)# 取值范围 [0,3]， 从0到3依次顺时针旋转

green_threshold   = (0,   80,  -70,   -10,   -0,   30)
yellow_threshold   =   (20,  80,  -40,  40,  15,  100)

'''
定义色块的范围
从图片中查找所有色块对象(image.blob)列表,
传入的颜色阈值参数按照 LAB 格式(l_lo，l_hi，a_lo，a_hi，b_lo，b_hi)
l:light 明度通道，亮度
a:从绿色到红色
b:从蓝色到黄色
理论上说，L*、a*、b*都是实数，不过实际一般限定在一个整数范围内：
- L*越大，亮度越高。L*为0时代表黑色，为100时代表白色。
- a*和b*为0时都代表灰色。
- a*从负数变到正数，对应颜色从绿色变到红色。
- b*从负数变到正数，对应颜色从蓝色变到黄色。
- 我们在实际应用中常常将颜色通道的范围-100~+100或-128~127之间。
'''

while True:
    img = sensor.snapshot()
    #img=摄像头获取的图像对象
    blobs = img.find_blobs([yellow_threshold],x_stride=100,y_stride=100)
    '''
    Blob 类 – 色块对象#
    色块对象是由 image.find_blobs 返回的。
    image.find_blobs(thresholds, roi=Auto, x_stride=2, y_stride=1, invert=False, area_threshold=10,
                     pixels_threshold=10, merge=False, margin=0, threshold_cb=None, merge_cb=None)

    thresholds是颜色的阈值，注意：这个参数是一个列表，可以包含多个颜色。如果你只需要一个颜色，
    那么在这个列表中只需要有一个颜色值，如果你想要多个颜色阈值，那这个列表就需要多个颜色阈值。
    注意：在返回的色块对象blob可以调用code方法，来判断是什么颜色的色块。
    示例
    red    = (xxx,xxx,xxx,xxx,xxx,xxx)
    blue   = (xxx,xxx,xxx,xxx,xxx,xxx)
    yellow = (xxx,xxx,xxx,xxx,xxx,xxx)
    img=sensor.snapshot()
    red_blobs = img.find_blobs([red])
    color_blobs = img.find_blobs([red,blue, yellow])

    roi是“感兴趣区”。示例：
    left_roi = [0,0,160,240]
    blobs = img.find_blobs([red],roi=left_roi)

    x_stride 就是查找的色块的x方向上最小宽度的像素，默认为2，如果你只想查找宽度10个像素以上的色块，
    那么就设置这个参数为10：
    blobs = img.find_blobs([red],x_stride=10)

    y_stride 就是查找的色块的y方向上最小宽度的像素，默认为1，如果你只想查找宽度5个像素以上的色块，
    那么就设置这个参数为5：
    blobs = img.find_blobs([red],y_stride=5)

    invert 反转阈值，把阈值以外的颜色作为阈值进行查找

    area_threshold 面积阈值，如果色块被框起来的面积小于这个值，会被过滤掉

    pixels_threshold 像素个数阈值，如果色块像素数量小于这个值，会被过滤掉

    merge 合并，如果设置为True，那么合并所有重叠的blob为一个。
    注意：这会合并所有的blob，无论是什么颜色的。如果你想混淆多种颜色的blob，只需要分别调用不同颜色阈值的find_blobs。
·

    find_blobs对象返回的是多个blob的列表。（注意区分blobs和blob，这只是一个名字，用来区分多个色块，和一个色块）。
    一个blobs列表里包含很多blob对象，blobs对象就是色块，每个blobs对象包含一个色块的信息。
    9.1. 构造函数#
    class image.blob
    请调用 image.find_blobs() 函数来创建此对象。
    '''


    if blobs:   #如果找到了目标颜色
        for b in blobs:#迭代找到的目标颜色区域
            tmp=img.draw_rectangle(b[0:4])
            tmp=img.draw_cross(b[5], b[6])
            c=img.get_pixel(b[5], b[6])
            print(b.cx(),b.cy())#返回色块中心的坐标到终端
            if(b.cx()>170):
                xl_place.value(0)#如果在屏幕右边，则xl_place(8pin)输出低电平
                xr_place.value(1)#中心点为（160，60）如果在屏幕右边，则xr_place(7pin)输出高电平
            elif(b.cx()<150):
                xl_place.value(1)#如果在屏幕左边，则xl_place(8pin)输出高电平
                xr_place.value(0)
            else:
                xr_place.value(0)
                xl_place.value(0)#在中间就都低电平
            if(b.cy()>70):
                yu_place.value(1)#如果在屏幕上边，则yo_place(9pin)输出高电平
                yd_place.value(0)#中心点为（160，60）如果在屏幕上边，则yd_place(10pin)输出低电平
            elif(b.cy()<50):
                yu_place.value(0)#如果在屏幕下边，则yo_place(9pin)输出低电平
                yd_place.value(1)#yd_place(10pin)输出高电平
            else:
                yu_place.value(0)
                yd_place.value(0)#在中间就都低电平


    '''
    9.2.1. blob.rect()#
    返回一个矩形元组(x, y, w, h) ，用于如色块边界框的 image.draw_rectangle 等 其他的 image 方法。

    9.2.2. blob.x()#
    返回色块的边界框的x坐标(int)。

    您也可以通过索引 [0] 取得这个值。

    9.2.3. blob.y()#
    返回色块的边界框的y坐标(int)。

    您也可以通过索引 [1] 取得这个值。

    9.2.4. blob.w()#
    返回色块的边界框的w坐标(int)。

    您也可以通过索引 [2] 取得这个值。

    9.2.5. blob.h()#
    返回色块的边界框的h坐标(int)。

    您也可以通过索引 [3] 取得这个值。

    9.2.6. blob.pixels()#
    返回从属于色块(int)一部分的像素数量。

    您也可以通过索引 [4] 取得这个值。

    9.2.7. blob.cx()#
    返回色块(int)的中心x位置。

    您也可以通过索引 [5] 取得这个值。

    9.2.8. blob.cy()#
    返回色块(int)的中心x位置。

    您也可以通过索引 [6] 取得这个值。

    9.2.9. blob.rotation()#
    返回色块的旋转（单位：弧度）。如果色块类似铅笔或钢笔，那么这个值就是介于0-180之间的唯一值。
    如果这个色块圆的，那么这个值就没有效用。如果这个色块完全不具有对称性，您只能由此得到0-360度的旋转。

    您也可以通过索引 [7] 取得这个值。

    9.2.10. blob.code()#
    返回一个16位的二进制数字，其中为每个颜色阈值设置一个位，这是色块的一部分。
    例如，如果您通过 image.find_blobs 来寻找三个颜色阈值，这个色块可以设置为0/1/2位。
    注意：除非以 merge=True 调用 image.find_blobs ，否则每个色块只能设置一位。
    那么颜色阈值不同的多个色块就可以合并在一起了。 您也可以用这个方法以及多个阈值来实现颜色代码跟踪。

    您也可以通过索引 [8] 取得这个值。

    9.2.11. blob.count()#
    返回合并为这一色块的多个色块的数量。只有您以 merge=True 调用 image.find_blobs 时，这个数字才不是1。

    您也可以通过索引 [9] 取得这个值。

    9.2.12. blob.area()#
    返回色块周围的边框面积(w * h)

    9.2.13. blob.density()#
    返回这个色块的密度比。这是在色块边界框区域内的像素点的数量。 总的来说，较低的密度比意味着这个对象的锁定得不是很好。
    '''


    lcd.display(img)
    #屏幕展示返回的图像
    '''
    image.draw_rectangle(x, y, w, h[, color[, thickness=1[, fill=False]]])#
    在图像上绘制一个矩形。 您可以单独传递x，y，w，h或作为元组(x，y，w，h)传递。

    color 是用于灰度或RGB565图像的RGB888元组。默认为白色。
    但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。

    thickness 控制线的粗细像素。

    将 fill 设置为True以填充矩形。

    返回图像对象，以便您可以使用 . 表示法调用另一个方法。

    不支持压缩图像和bayer图像。

    image.draw_cross(x, y[, color[, size=5[, thickness=1]]])#
    在图像上绘制一个十字。 您可以单独传递x，y或作为元组(x，y)传递。

    color 是用于灰度或RGB565图像的RGB888元组。默认为白色。
    但是，您也可以传递灰度图像的基础像素值(0-255)或RGB565图像的字节反转RGB565值。

    size 控制十字线的延伸长度。

    thickness 控制边缘的像素厚度。

    image.get_pixel(x, y[, rgbtuple])#
    灰度图：返回(x, y)位置的灰度像素值。

    RGB565l：返回(x, y)位置的RGB888像素元组(r, g, b)。

    Bayer图像: 返回(x, y)位置的像素值。
    '''
