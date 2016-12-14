#coding=utf-8
import random
import string
import sys
import math
from PIL import Image,ImageDraw,ImageFont,ImageFilter

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
def __gene_text(i, save_path):
    source = []
    for j in range(0, number):
        source.append(str(random.choice(range(10))))
    s = "".join(source)
    f = open(save_path+'name.txt', 'a')
    f.write("%d %s" % (i, s))
    f.write('\n')
    f.close()
    return "".join(source)

#生成验证码
def __gene_code(i, save_path, fonts):
    width, height = size #宽和高
    fontid = random.randint(0,len(fonts)-1)
    font_path = fonts[fontid]
    image = Image.new('RGBA', (width,height),bgcolor) #创建图片
    font = ImageFont.truetype(font_path, 25) #验证码的字体
    draw = ImageDraw.Draw(image)  #创建画笔
    text = __gene_text(i, save_path) #生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font, fill=fontcolor) #填充字符串

    # image = image.transform((width+30,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    # image = image.transform((width+20,height+10), Image.AFFINE, (1,-0.3,0,-0.1,1,0),Image.BILINEAR)  #创建扭曲
    image = image.filter(ImageFilter.EDGE_ENHANCE_MORE) #滤镜，边界加强
    image.save(save_path + '%s.png' % i) #保存验证码图片


def gene_easyVerificationCode(num, path, fonts):
    """
    生成简单验证码
    :param num: 生成的验证码数量
    :param path: 存放路径
    :param fonts: 生成验证码的字体
    :return:
    """
    for i in range(1, num + 1):
        __gene_code(i, path, fonts)

if __name__ == "__main__":
    Fonts = ["/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf"
        ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-M.ttf"
        ,"/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf"
        ,"/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf"]

    gene_easyVerificationCode(1, "/home/zhongjianlv/ML/VerificationCodeRecognition/imagetest/",
                          Fonts)
