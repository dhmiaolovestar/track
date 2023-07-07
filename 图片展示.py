import lcd, image

lcd.init()

img = image.Image("/sd/sllh.jpg")
'''
class image.Image(path[, copy_to_fb=False])

从 path 中的文件中创建一个新的图像对象。

支持bmp/pgm/ppm/jpg/jpeg格式的图像文件。

若 copy_to_fb 为True，图像会直接载入帧缓冲区，您就可以加载
大幅图片了。若为False，图像会载入MicroPython的堆中，堆远比帧缓冲区小。
'''
while(True):
    lcd.display(img)

