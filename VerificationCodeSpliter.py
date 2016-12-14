#!/usr/bin/python
#-*- coding:utf-8 -*-


from PIL import Image,ImageEnhance,ImageFilter,ImageChops
import os

#是否输出分割子图
isShowSubImage = False

# 额外边界
EXTRA_ALIGIN=3

def cut_width(im, threshold):
    """
    对图像宽度进行分割,把每列映射到x-axis, 存在小于阈值为1, 否则为0
    :param im: 图片
    :param threshold: 阈值
    :return: 分割区间,多个tuple组成的list
    """
    pixelsOfImage = im.load()
    width = mapToAxis("x", 0, im.width, 0, im.height, threshold, pixelsOfImage)
    reslut = []
    start = 0
    end = 0
    i = 0
    while i < len(width):
        tuple = findSplitRegion(i,width)
        if(tuple[0]<=tuple[1]):
            i = tuple[1] + 1
            reslut.append(tuple)
        else:
            return reslut
    return reslut


def findSplitRegion(start, list):
    """
    从list的start开始找到连续1的区间,如果全是0,则返回（len(list),len(list)-1）
    :param start: list中的开始位置
    :param list: 一个含0,1的list
    :return: tuple，（连续1的开始位置，结束位置）
    """
    s = 0;
    e = 0;
    while True:
        if(start >= len(list)):
            return (start,start-1)
        if(list[start] == 1):
            s = start
            break
        start += 1

    while True:
        if(start >= len(list)):
            return (start,start-1)
        if(list[start] == 0):
            e = start - 1
            break
        start += 1
    return (s,e)


def mapToAxis(type ,map_start, map_end, start, end, threshold, pixelsOfImage):
    """
    将像素映射到x或者y轴，若映射到x轴，也就是把像素矩阵中map_start到map_end的所有列的start到end映射到x轴(宽度)
    若映射到y轴，也就是把像素矩阵中map_start到map_end的所有行的start到end映射到y轴(高度)
    :param type: x 或者 y
    :param map_start:
    :param map_end:
    :param start:
    :param end:
    :param threshold:
    :param pixelsOfImage:
    :return:
    """
    value = 0
    if(type == "x"):
        width = []
        for x in range(map_start,map_end):
            for y in range(start,end):
                if (pixelsOfImage[x, y] < threshold):  # 不是白色
                    value = 1
                    break
            width.append(value)
            value = 0
        return width
    elif(type == "y"):
        height = []
        for x in range(map_start,map_end):
            for y in range(start,end):
                if (pixelsOfImage[y, x] < threshold):  # 不是白色
                    value = 1
                    break
            height.append(value)
            value = 0
        return height

    else:
        raise "no this type"
        return None

def cut_height(im,threshold,split_X):
    """
    对图像高度进行分割,需要根据已经给出的宽度分割区域决定
    :param im: 图片
    :param threshold: 阈值
    :param split_X: 宽度分割区域
    :return: 高度分割区域,多个tuple组成的list,长度和split_X一致
    """
    r_list = []
    pixel = im.load()
    for value in split_X:
        x1 = value[0]
        x2 = value[1]
        height = mapToAxis("y", 0, im.height, x1, x2+1, threshold, pixel)
        tuple = findSplitRegion(0,height)
        r_list.append(tuple)
    return r_list

def splitImage(im,split_x,split_y,width,height,extra_aligin):
    """
    根据区域切割图片
    :param im: 原图片
    :param split_x: 宽度划分区域
    :param split_y: 高度划分区域
    :param width: 切割出的图片的宽度
    :param height: 切割出的图片的高度
    :return: 切割图片list
    """
    submages = []
    for i in range(len(split_x)):
        x_region = split_x[i]
        y_region = split_y[i]
        region_ = (x_region[0]-extra_aligin, y_region[0]-extra_aligin, x_region[1]+1+extra_aligin, y_region[1]+1+extra_aligin)
        subimg = im.crop(region_)
        subimg = clear_aligin(subimg,EXTRA_ALIGIN)
        subimg = subimg.resize((width, height), Image.ANTIALIAS)
        submages.append(subimg)
    return submages


def clear_aligin(im,extra_aligin):
    pixel = im.load()
    width = im.width
    height = im.height
    #去除上边界
    for i in range(extra_aligin):
        for j in range(width):
            pixel[j,i] = 255
    #去除下边界
    for i in range(height-extra_aligin,height):
        for j in range(width):
            pixel[j,i] = 255
    # 去除左边界
    for i in range(extra_aligin):
        for j in range(height):
            pixel[i,j] = 255
    # 去除右边界
    for i in range(width - extra_aligin,width):
        for j in range(height):
            pixel[i,j] = 255
    return im


def splitOneImage(image):
    """
    分割图片返回矩阵
    :param image: 处理后图像
    :return: 矩阵list,每个temp对应一个矩阵
    """
    r = []
    split_x = cut_width(image, 200)
    split_y = cut_height(image, 200, split_x)
    submages = splitImage(image, split_x, split_y, 28, 28, EXTRA_ALIGIN)
    for subimg in submages:
        if isShowSubImage:
            subimg.show()
        pixel = subimg.load()
        list = []
        for x in range(subimg.height):
            for y in range(subimg.width):
                list.append(255 - pixel[y, x])
        r.append(list)
    return r

def preprocessImage(image):
    """
    对图像进行预处理
    :param image:
    :return: 处理后图像
    """
    im = image.convert("L")
    return im


def split(imagepath, save_filename):
    """
    对路径下的所有图片进行分割，同时保存相应矩阵到save_filename中
    :param imagepath:
    :param save_filename:
    :return:
    """
    name = imagepath + "name.txt"
    listdir = os.listdir(imagepath)
    listdir.remove("name.txt")
    f = open(name, mode="r")
    #读取所有验证码的值
    dict = {}
    s = f.readline().strip()  #验证码对应的值,去除空格
    while s != "":
        split = s.split(" ")
        dict[split[0]] = split[1]
        s = f.readline().strip()
    f_save = open(save_filename, "w")
    first = True
    for image_filename in listdir:
        im = Image.open(imagepath + image_filename)
        im = preprocessImage(im)
        code = dict[image_filename.split(".")[0]] #验证码
        r_list = splitOneImage(im) #验证码对应的矩阵
        for i in range(len(r_list)):
            if(first):
                first = False
                string = "label"
                for j in range(len(r_list[0])):
                    string += (",pixel" + str(j))
            f_save.write(string+"\n")
            string = code[i]
            for j in range(len(r_list[i])):
                string += ("," + str(r_list[i][j]))
            f_save.write(string+"\n")
    f.flush()
    f.close()



if __name__ == "__main__":
    im = Image.open("image/1.png")
    im = preprocessImage(im)
    isShowSubImage = True
    splitOneImage(im)

