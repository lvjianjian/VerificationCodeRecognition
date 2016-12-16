#!/usr/bin/python
#-*- coding:utf-8 -*-

"""
找连通区域进行分割
"""


from PIL import Image
import VerificationCodeSpliter as sp
from collections import deque
import numpy as np
import os
import VerificationCodeSpliter as sp
import VerificationCodeGenerator as gene
import clearpoint as cp
# 周围向量
arround = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]

# 额外边界
EXTRA_ALIGIN=3

isShowSubImage = False;

def cut_dbscan(im, threshold, extra_aligin, width, height):
    """
     通过连通区域切割,返回分割后图像
    :param im: 二值化后的图像
    :param threshold: 阈值
    :param subimage_num: 分割图片数量
    :param width: 重新调整宽度
    :param height: 重新调整高度
    :return: list：[subimages]
    :return:
    """
    count = 0
    pixels = im.load()
    height1 = im.height / 2
    queue = deque()
    visited = np.zeros((im.width+1, im.height+1), dtype=int)
    start = 0
    list=[]
    while start < im.width:
        x_left = im.width
        x_right = -1
        y_top = im.height
        y_bottom = -1
        for i in (range(start, im.width)):
            if(pixels[i, height1] < threshold):
                queue.append((i, height1))
                visited[i][height1] = 1
                break
            start = i
        if start == im.width - 1:
            break
        count = 0
        #从该点开始寻找最大连通区域
        while len(queue) != 0:
            popleft = queue.popleft()
            count += 1
            if(popleft[1] < y_top):
                y_top = popleft[1]
            if(popleft[1] > y_bottom):
                y_bottom = popleft[1]
            if(popleft[0] < x_left):
                x_left = popleft[0]
            if(popleft[0] > x_right):
                x_right = popleft[0]
            __visitArround(popleft[0], popleft[1], pixels, threshold, im.width, im.height, queue, visited)
        region = (x_left-extra_aligin, y_top-extra_aligin, x_right+1+extra_aligin, y_bottom+1+extra_aligin)
        start = x_right+1
        if(count < 30):
            continue
        subimage = im.crop(region)
        subimage = sp.clear_aligin(subimage,EXTRA_ALIGIN)
        subimage = subimage.resize((width, height), Image.ANTIALIAS)
        if(isShowSubImage):
            subimage.show()
        list.append(subimage)
    return list



def __visitArround(i, j, pixels, threshold, width, height, queue, visited):
    for v in arround:
        newi = i + v[0]
        newj = j + v[1]
        if(newi >= 0 and newi < width and newj>=0 and newj<height ):
            if visited[newi][newj] == 0:
                if(pixels[newi, newj] < threshold):
                    queue.append((newi,newj))
                    visited[newi][newj] = 1

def splitOneImage(image,width,height):
    """
    分割图片返回矩阵
    :param image: 处理后图像
    :return: 矩阵list,每个temp对应一个矩阵
    """
    r = []
    submages = cut_dbscan(image,  200, EXTRA_ALIGIN, width, height)
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
        print image_filename
        im = Image.open(imagepath + image_filename)
        im = sp.preprocessImage(im)
        code = dict[image_filename.split(".")[0]] #验证码
        r_list = splitOneImage(im, 28, 28) #验证码对应的矩阵
        if(len(code) != len(r_list)):
            print "drop " + image_filename
        for i in range(min(len(code),len(r_list))):
            if(first):
                first = False
                string = "label"
                for j in range(len(r_list[0])):
                    string += (",pixel" + str(j))
                f_save.write(string+"\n")
            string = code[i]
            for j in range(len(r_list[i])):
                string += ("," + str(r_list[i][j]))
            f_save.write(string + "\n")
    f.flush()
    f.close()

if __name__ == '__main__':
    # im = Image.open("image/95.png")
    im = Image.open("result.png")
    isShowSubImage = True
    im = sp.preprocessImage(im)
    im.show()
    # sp.splitOneImage(im)
    cp.load(im, "./result_after.png")
    im_after = Image.open("result_after.png")
    im_after.show()
    cut_dbscan(im_after, 200, EXTRA_ALIGIN, 28, 28)

# pixel = im.load()
# for x in range(im.height):
#     for y in range(im.width):
#         print "%5d" % pixel[y, x],
#     print