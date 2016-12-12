#coding=utf-8
import random
import string
import sys
import math
from PIL import Image,ImageDraw,ImageFont,ImageFilter

#字体的位置，不同版本的系统会有不同
font_path = 'C:\Windows\Fonts\Arial.ttf'
#生成几位数的验证码
number = 4
#生成验证码图片的高度和宽度
size = (100,30)
#背景颜色，默认为白色
bgcolor = (255,255,255)
#字体颜色，默认为蓝色
fontcolor = (0,0,255)
#干扰线颜色。默认为红色
linecolor = (255,0,0)

#用来随机生成一个字符串
def gene_text():
    source = []
    for i in range(0,number):
        source.append(str(random.choice(range(10))))
    s = "".join(source)
    f = open('name.txt','a')
    f.write(s)
    f.write('\n')
    f.close()
    return "".join(source)

#生成验证码
def gene_code(i):
    width,height = size #宽和高
    image = Image.new('RGBA',(width,height),bgcolor) #创建图片
    font = ImageFont.truetype(font_path,25) #验证码的字体
    draw = ImageDraw.Draw(image)  #创建画笔
    text = gene_text() #生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number),text,
              font= font,fill=fontcolor) #填充字符串

    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    # image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
    image.save('F:\\python\\test\\image\\%s.png' %i) #保存验证码图片
if __name__ == "__main__":
    for i in range(1,2000):
        gene_code(i)
