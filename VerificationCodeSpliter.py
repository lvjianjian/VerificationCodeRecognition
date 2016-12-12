#!/usr/bin/python
#-*- coding:utf-8 -*-


from PIL import Image,ImageEnhance,ImageFilter,ImageChops



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

def splitImage(im,split_x,split_y,width,height):
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
        region_ = (x_region[0], y_region[0], x_region[1], y_region[1])
        subimg = im.crop(region_)
        subimg = subimg.resize((28, 28), Image.ANTIALIAS)
        submages.append(subimg)
    return submages


def split(images, name, save_filename):
    for image in images:
        pass

#im = Image.open('genimage.png')
im = Image.open("/home/zhongjianlv/ML/VerificationCodeRecognition/image/3.png")
# im = Image.open('1.jpg')
# im.thumbnail((100,100), Image.ANTIALIAS)
# im.show()
#找出划分区域
im = im.convert("L")
# im.show()
# exit()
split_x = cut_width(im, 200)
split_y = cut_height(im, 200, split_x)

#分割
submages = splitImage(im,split_x,split_y,28,28)

for subimg in submages:
    subimg.show()
    pixel = subimg.load()
    list = []
    for x in range(subimg.height):
        for y in range(subimg.width):
            list.append(pixel[y,x])
    print list




#  convert to binary image by the table
# cropped = autoCrop(im)
# cropped.show()

# #纵向切割，依据X轴的投影，将图片切割为4张图片，并返回切割点的坐标
# def Cut_X(im):
#     Image_Value = Caculate_X(im)
#     X_value=[]
#     List0=[]
#     List1=[]
#     ListRow0=[]
#     ListRow1=[]
#     for i in range(len(Image_Value)):
#         if Image_Value[i] ==0 and len(ListRow1)==0: #数字左侧的空白列
#             ListRow0.append(i)
#         elif Image_Value[i] ==0 and len(ListRow1)>0: #数字右侧的空白列
#             List1.append(ListRow1)
#             ListRow1=[]
#             ListRow0.append(i)
#         elif Image_Value[i] >0 and len(ListRow0)>0 : #数字列
#             List0.append(ListRow0)
#             ListRow0=[]
#             ListRow1.append(i)
#         elif Image_Value[i] >0 and len(ListRow0)==0: #数字列
#             ListRow1.append(i)
#     if len(List1)==1 : #如果只有1个数字右侧的空白列，放弃切割
#         for i in range(4):
#             X_value.append(1 12*i)#
#             X_value.append(12*i 12)
#         elif len(List1)==2 :    #如果只有2个数字右侧的空白列，放弃切割
#         for i in range(4):
#             X_value.append(1 12*i)#
#             X_value.append(12*i 12)
#         elif len(List1)==3 : #如果有3个数字右侧的空白列，将数字列中最长的那段值进行拆分，拆分点在X轴投影的大于第五位后的第一个最低点。
#         Max_index = Max_Index(List1)
#         for i in range(len(List1)):
#             if i == Max_index:
#                 #
#                 index = Cut_Two(List1[i],Image_Value)
#                 X_value.append(List1[i][0])
#                 X_value.append(List1[i][index])
#                 X_value.append(List1[i][(index 1)])
#                 X_value.append(List1[i][(len(List1[i])-1)])
#             else:
#                 X_value.append(List1[i][0])
#                 X_value.append(List1[i][(len(List1[i])-1)])
#     elif len(List1)==4 :#4个空白列
#         for i in range(len(List1)):
#             X_value.append(List1[i][0])
#             X_value.append(List1[i][(len(List1[i])-1)])
#     elif len(List1)==5 :#如果有5个数字右侧的空白列，取长度最长的4段。
#         Min_index = Min_Index(List1)
#         for i in range(len(List1)):
#             if i <> Min_index:
#                 X_value.append(List1[i][0])
#                 X_value.append(List1[i][(len(List1[i])-1)])
#     elif len(List1)>5 :#大于5个直接放弃切割
#         for i in range(4):
#             X_value.append(1 12*i)#############
#             X_value.append(12*i 12)
#         return X_value
#
#     #返回矩阵各行最大值位置的函数，以便找到有颜色的列中X轴投影最大的地方
#     def Max_Index(List1):
#         Max = 0
#         Max_index=0
#         for i in range(len(List1)):
#             if len(List1[i])>Max:
#                 Max=len(List1[i])
#                 Max_index=i
#         return Max_index
#
#     #返回矩阵各行最小值位置的函数，以便找到有颜色的列中X轴投影最小的地方
#     def Min_Index(List1):
#         Min = 50
#         Min_index=0
#         for i in range(len(List1)):
#             if len(List1[i])            Min=len(List1[i])
#             Min_index=i
#     return Min_index
#
# #分割两个紧挨的数字
# def Cut_Two(ListRow,Image_Value):
#     index = 0
#     start = 0
#     if len(ListRow)>=15:
#         start = 3
#     for i in range((1 start),(len(ListRow)-1)):
#         if Image_Value[ListRow[i]]<= Image_Value[ListRow[(i 1)]] and Image_Value[ListRow[i]]<=2:#
#             index = i
#             break
#
#     return index
#
# #横向切割 4张图片，4次投影，并返回切割点的坐标
# def Cut_Y(im):
#     Y_value=[]
#     Image_Value=[]
#     Cut_Xs=Cut_X(im)
#     for k in range(4):
#         Image_Value=[]
#         for j in range(im.size[1]):
#             X_pixel=0
#             for i in range(Cut_Xs[(2*k)],(Cut_Xs[(2*k 1)] 1)):
#                 if im.getpixel((i,j))==0:
#                     X_pixel = X_pixel 1
#             Image_Value.append(X_pixel)
#         for i in range(len(Image_Value)):
#             if Image_Value[i]>0:
#                 Y_value.append(i)
#                 break
#         for i in range((len(Image_Value)-1),0,(-1)):
#             if Image_Value[i]>0:
#                 Y_value.append(i)
#                 break
#
#     return Y_value

# #定义图像预处理的整体函数
# def Change_Image(Docu_Name,Dist):
#     im = Handle_Image(Docu_Name,Dist)
#     X_Value=Cut_X(im)
#     Y_Value=Cut_Y(im)
#
#     ims = []
#     Image_Value=[]
#     Image_Values=[]
#     Image_Value_Row=[]
#     for k in range(4):
#         im1= im.crop((X_Value[(2*k)],Y_Value[(2*k)],(X_Value[(2*k+1)]+1),(Y_Value[(2*k+1)]+1))) #切割图像为4个子图像
#         ims.append(im1)
#         for j in range(Y_Value[(2*k)],(Y_Value[(2*k+1)]+1)):
#             for i in range(X_Value[(2*k)],(X_Value[(2*k+1)]+1)):
#                 if im.getpixel((i,j))==0:#黑色像素的值是0
#                     Image_Value_Row.append(1)
#                 else:
#                     Image_Value_Row.append(0)
#             Image_Value.append(Image_Value_Row)#
#             Image_Value_Row=[]#
#
#         Image_Values.append(Image_Value)
#         Image_Value=[]
#
#     return Image_Values #返回切割后各个图像对应的黑白像素的0-1值所存储在其中的三维数组。
#
# #处理图片以便后续的0-1二值化
# def Handle_Image(Docu_Name,Dist):
#     im = Image.open('%s'%(Dist+Docu_Name) + '.png') #打开对应目录的png格式的验证码图片
#     im=im.convert('RGB')
#     for j in range(im.size[1]):
#         for i in range(im.size[0]):
#             Gray = Change_Gray(im.getpixel((i,j)))  #灰度化
#             im.putpixel([i,j],(Gray,Gray,Gray))
#             if i==0 or i==(im.size[0]-1): #将图片的第一行和最后一行设为白色。
#                 im.putpixel([i,j],(255,255,255))
#             if j==0 or j==(im.size[1]-1):#将图片的第一列和最后一列设为白色。
#                 im.putpixel([i,j],(255,255,255))
#     enhancer = ImageEnhance.Contrast(im) #增加对比对
#     im = enhancer.enhance(2)
#     enhancer = ImageEnhance.Sharpness(im) #锐化
#     im = enhancer.enhance(2)
#     enhancer = ImageEnhance.Brightness(im) #增加亮度
#     im = enhancer.enhance(2)
#     #im=im.convert('L').filter(ImageFilter.DETAIL) #滤镜效果
#     im = im.convert('1') #转为黑白图片
#
#     im = Clear_Point(im) #清除周围8个像素都是白色的孤立噪点
#     im = Clear_Point_Twice(im) #清除两个孤立的噪点：周围8个像素中有7个是白色，而唯一的黑色像素对应的他的邻域（他周围的8个像素）中唯一的黑色像素是自身。
#     im = Clear_Point_Third(im) #清除第三种噪点：左右都是3个（含）以上的空白列，自身相邻的3个列上的X值投影不大于3.
#
#     return im
#
# #改变灰度，查文献后发现据说按照下面的R，G，B数值的比例进行调整，图像的灰度最合适。
# def Change_Gray(RGB_Value):
#     Gray = int((RGB_Value[0]*299+RGB_Value[1]*587+RGB_Value[2]*114)/1000)
#     return Gray
#
# #图像处理的关键是后续的清楚噪点，也就是所谓的孤立点
#
# #清除单个孤立点
# def Clear_Point(im):
#     for j in range(1,(im.size[1]-1)):
#         for i in range(1,(im.size[0]-1)):
#             if im.getpixel((i,j))==0 and im.getpixel(((i-1),(j-1)))==255  and im.getpixel((i,(j-1)))==255  and im.getpixel(((i 1),(j-1)))==255  and im.getpixel(((i-1),j))==255  and im.getpixel(((i 1),j))==255  and im.getpixel(((i-1),(j 1)))==255  and im.getpixel((i,(j 1)))==255  and im.getpixel(((i 1),(j 1)))==255:
#                 im.putpixel([i,j],255)
#     return im
#
# #清除只有2个的孤立点
# def Clear_Point_Twice(im):
#     for j in range(1,(im.size[1]-1)):
#         for i in range(1,(im.size[0]-1)):
#             if im.getpixel((i,j))==0 and ( im.getpixel(((i-1),(j-1)))+im.getpixel((i,(j-1)))+im.getpixel(((i+1),(j-1)))+im.getpixel(((i-1),j))+im.getpixel(((i+1),j)) im.getpixel(((i-1),(j 1))) im.getpixel((i,(j 1))) im.getpixel(((i 1),(j 1)))) == 255*7:
#                 if im.getpixel(((i 1),j))==0: #因为扫描的顺序是从上到下，从左到右，噪点只能是在自身像素的后面和下面，也就是只有4个可能性而已，而不是8个，可以减少一半的代码。
#                     m=i 1
#                     n=j
#                     if ( im.getpixel(((m-1),(n-1))) im.getpixel((m,(n-1))) im.getpixel(((m 1),(n-1))) im.getpixel(((m-1),n))   im.getpixel(((m 1),n)) im.getpixel(((m-1),(n 1))) im.getpixel((m,(n 1))) im.getpixel(((m 1),(n 1)))) == 255*7:
#                         im.putpixel([i,j],255)
#                         im.putpixel([m,n],255)
#                 elif im.getpixel(((i-1),(j 1)))==0:
#                     m=i-1
#                     n=j 1
#                     if ( im.getpixel(((m-1),(n-1))) im.getpixel((m,(n-1))) im.getpixel(((m 1),(n-1))) im.getpixel(((m-1),n))    im.getpixel(((m 1),n)) im.getpixel(((m-1),(n 1))) im.getpixel((m,(n 1))) im.getpixel(((m 1),(n 1)))) == 255*7:
#                         im.putpixel([i,j],255)
#                         im.putpixel([m,n],255)
#                 elif im.getpixel((i,(j 1)))==0:
#                     m=i
#                     n=j 1
#                     if ( im.getpixel(((m-1),(n-1))) im.getpixel((m,(n-1))) im.getpixel(((m 1),(n-1))) im.getpixel(((m-1),n))    im.getpixel(((m 1),n)) im.getpixel(((m-1),(n 1))) im.getpixel((m,(n 1))) im.getpixel(((m 1),(n 1)))) == 255*7:
#                         im.putpixel([i,j],255)
#                         im.putpixel([m,n],255)
#                 elif im.getpixel(((i 1),(j 1)))==0:
#                     m=i 1
#                     n=j 1
#                     if ( im.getpixel(((m-1),(n-1))) im.getpixel((m,(n-1))) im.getpixel(((m 1),(n-1))) im.getpixel(((m-1),n))    im.getpixel(((m 1),n)) im.getpixel(((m-1),(n 1))) im.getpixel((m,(n 1))) im.getpixel(((m 1),(n 1)))) == 255*7:
#                         im.putpixel([i,j],255)
#                         im.putpixel([m,n],255)
#     return im
#
# #清楚第三种噪点比较麻烦，需要计算图像的0-1值在X轴的投影后，才能判断。
# #依据图片像素颜色计算X轴投影
# def Caculate_X(im):
#     Image_Value=[]
#     for i in range(im.size[0]):
#         Y_pixel=0
#         for j in range(im.size[1]):
#             if im.getpixel((i,j))==0:
#                 temp_value=1
#             else:
#                 temp_value=0
#             Y_pixel = Y_pixel temp_value
#         Image_Value.append(Y_pixel)
#     return Image_Value
#
# #逐次将多列设为全白
# def Set_White_Y(im,List_Black):
#     for j in range(im.size[1]):
#         for i in range(List_Black[0],(List_Black[(len(List_Black)-1)] 1)):
#             im.putpixel([i,j],255)
#     return im
#
# #清除第三种残余的孤立点
# def Clear_Point_Third(im):
#     Image_Value = Caculate_X(im)
#     List01=[]
#     List_Black=[]
#     List03=[]
#     for i in range(len(Image_Value)): #从左到右扫描
#         if Image_Value[i] ==0 and len(List_Black) == 0 : #X轴投影是0，说明是空白列，黑色列的列表是空值，说明当前列是黑色列的左侧
#             List01.append(i)
#         elif  Image_Value[i] >0 : #X周投影大于0的列，即扫描到了黑色列
#             List_Black.append(i)
#         elif Image_Value[i] ==0 and len(List_Black)>0 and len(List_Black)<=3:# 黑色列的列表的长度大于0，不大于3个空白字符，现在的X轴投影为0，说明现在扫描到了孤立噪点所在的黑色列右侧的空白列
#             List03.append(i)
#             if len(List03)==3:#空白列为3列
#                 im = Set_White_Y(im,List_Black) #逐次将多列设为全白
#                 List01=[]
#                 List_Black=[]
#                 List03=[]
#         elif Image_Value[i] ==0 and len(List_Black)>3: #当前是空白列，黑色列的数量大于3，说明扫描到了数字所在部分（不是噪点）的右侧空白列。
#             List01=[]
#             List_Black=[]
#             List03=[]
#             List01.append(i)
#     return im