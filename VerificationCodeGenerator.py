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

TYPE_EASY = 1
TYPE_WITH_NOISE = 2
TYPE2_NUM_ONLY = 10
TYPE2_ALL = 62
CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
for w in string.lowercase:
    CHARS.append(w)
for w in string.uppercase:
    CHARS.append(w)

# #背景颜色，默认为白色
# bgcolor = (255,255,255)
# #字体颜色，默认为蓝色
# fontcolor = (0,0,255)
# #干扰线颜色。默认为红色
# linecolor = (255,0,0)
# 随机颜色1:
def rndColor():
    return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))

# 随机颜色2:
def rndColor2():
    return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))

#用来随机生成一个字符串
def __gene_text(i, save_path , type):
    source = []
    for j in range(0, number):
        source.append(str(CHARS[random.choice(range(type))]))
    s = "".join(source)
    f = open(save_path+'name.txt', 'a')
    f.write("%d %s" % (i, s))
    f.write('\n')
    f.close()
    return "".join(source)

#生成验证码
def __gene_code(i, save_path, fonts, type, type2): #type : 是否带噪点 type2: 是否只有数字
    width, height = size #宽和高
    fontid = random.randint(0,len(fonts)-1)
    font_path = fonts[fontid]
    image = Image.new('RGBA', (width,height),(255, 255, 255)) #创建图片
    font = ImageFont.truetype(font_path, 25) #验证码的字体
    draw = ImageDraw.Draw(image)  #创建画笔
    if(type == TYPE_WITH_NOISE):
        for x in range(width):
            for y in range(height):
                draw.point((x, y), fill=rndColor())
    text = __gene_text(i, save_path, type2) #生成字符串
    font_width, font_height = font.getsize(text)
    draw.text(((width - font_width) / number, (height - font_height) / number), text,
              font=font, fill=(0, 0, 0)) #填充字符串

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
        __gene_code(i, path, fonts, TYPE_EASY, TYPE2_NUM_ONLY)

def gene_EasyVerificationCodeWithNoise(num, path, fonts):
    """
    生成带噪点的验证码
    :param num:
    :param path:
    :param fonts:
    :return:
    """
    for i in range(1, num + 1):
        __gene_code(i, path, fonts, TYPE_WITH_NOISE, TYPE2_NUM_ONLY)

def gene_ALLVerificationCode(num, path, fonts):
    """
    生成不带噪点的所有字母数字组成的验证码
    :param num:
    :param path:
    :param fonts:
    :return:
    """
    for i in range(1, num + 1):
        __gene_code(i, path, fonts, TYPE_EASY, TYPE2_ALL)

def gene_AllVerificationCodeWithNoise(num, path, fonts):
    """
    生成带噪点的所有字母数字组成的验证码
    :param num:
    :param path:
    :param fonts:
    :return:
    """
    for i in range(1, num + 1):
        __gene_code(i, path, fonts, TYPE_WITH_NOISE, TYPE2_ALL)

if __name__ == "__main__":
    Fonts = ["/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-B.ttf"
        , "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-M.ttf"
        , "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-R.ttf"
        , "/usr/share/fonts/truetype/ubuntu-font-family/UbuntuMono-R.ttf"]

    gene_easyVerificationCode(1, "/home/lee/workplace/VerificationCodeRecognition/imagetest/",
                          Fonts)
