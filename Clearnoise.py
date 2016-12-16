import os
from PIL import *
from PIL import Image
import clearpoint as point

def RGB2BlackWhite(filename,basepath,name):
    im=Image.open(filename)
    (w,h)=im.size
    R=0
    G=0
    B=0

    for x in xrange(w):
        for y in xrange(h):
            pos=(x,y)
            rgb=im.getpixel( pos )
            (r,g,b)=rgb
            R=R+r
            G=G+g
            B=B+b

    rate1=R*1000/(R+G+B)
    rate2=G*1000/(R+G+B)
    rate3=B*1000/(R+G+B)



    for x in xrange(w):
        for y in xrange(h):
            pos=(x,y)
            rgb=im.getpixel( pos )
            (r,g,b)=rgb
            n= r*rate1/1000 + g*rate2/1000 + b*rate3/1000
            #print "n:",n  
            if n>=60:
                im.putpixel( pos,(255,255,255))
            else:
                im.putpixel( pos,(0,0,0))

    point.load(im, basepath+name)

def saveAsBmp(imagepath,bathpath):
    listdir = os.listdir(imagepath)
    listdir.remove("name.txt")
    for image_filename in listdir:

        im = imagepath + image_filename
        pos1=im.rfind('.')
        fname1=im[0:pos1]
        fname1=fname1+'_1.png'
        Im = Image.open(im)
        new_im = Image.new("RGB", Im.size)
        new_im.paste(Im)
        new_im.save(fname1)
        RGB2BlackWhite(fname1,bathpath,image_filename)

if __name__=="__main__":
    filename=saveAsBmp("image/1.png")
    RGB2BlackWhite(filename)
