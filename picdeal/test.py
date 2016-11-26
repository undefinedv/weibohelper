#!/usr/bin/env python
#encoding=utf-8
import sys,os,random

from PIL import Image,ImageEnhance,ImageFilter,ImageDraw
from StringIO import StringIO
import copy
import json,urllib2



def calcThreshold(im):
    L = im.convert('L').histogram()
    sum = 0
    threshold = 0
    for i in xrange(len(L)):
        sum += L[i]
        if sum >= 450:
            threshold = i
            break
    return threshold

def binaryzation(im,threshold = 90):
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    imgry = im.convert('L')
    imout = imgry.point(table,'1')  
    return imout


    '''
抽取出字符矩阵 列表
'''
def extractChar(im):
    OFFSETLIST = [(1,0),(0,1),(-1,0),(0,-1),(1,1),(-1,1),(1,-1),(-1,-1)]
    pixelAccess = im.load()
    num = 1
    queue = []
    ff = [[0]*im.size[1] for i in xrange(im.size[0])]
        
    '''
        floodfill 提出块
    '''
    
    for i in xrange(im.size[0]):
        for j in xrange(im.size[1]):
            '''
                pixelAccess[i,j] == 0 表示是黑点
            '''
            if pixelAccess[i,j] == 0 and ff[i][j] == 0:
                ff[i][j] = num
                queue.append((i,j))
                while len(queue) > 0 :
                    a,b = queue[0]
                    queue = queue[1:]
                    for offset1,offset2 in OFFSETLIST:
                        x,y = a + offset1, b + offset2
                        if x < 0 or x >= im.size[0]:continue
                        if y < 0 or y >= im.size[1]:continue
                        if pixelAccess[x,y] == 0 and ff[x][y] == 0:
                            ff[x][y] = num
                            queue.append((x,y))

                num += 1
    
    '''
        字符点阵的坐标列表，对齐到 (0,0)
        eg: [(1,2),(3,24),(54,23)]
    '''
    #初始化字符数组
    info = {
            "x_min":im.size[0],
            "y_min":im.size[1],
            "x_max":0,
            "y_max":0,
            "width":0,
            "height":0,
            "number":0,
            "points":[]
    }
    charList = [copy.deepcopy(info) for i in xrange(num)]
    #统计
    for i in xrange(im.size[0]):
        for j in xrange(im.size[1]):
            if ff[i][j] == 0:
                continue
            id = ff[i][j]
            if i < charList[id]['x_min']:charList[id]['x_min'] = i
            if j < charList[id]['y_min']:charList[id]['y_min'] = j
            if i > charList[id]['x_max']:charList[id]['x_max'] = i
            if j > charList[id]['y_max']:charList[id]['y_max'] = j
            charList[id]['number'] += 1
            charList[id]['points'].append((i,j))
            
    for i in xrange(num):
        charList[i]['width'] = charList[i]['x_max'] - charList[i]['x_min'] + 1
        charList[i]['height'] = charList[i]['y_max'] - charList[i]['y_min'] + 1
        #修正偏移
        charList[i]['points'] = [(x-charList[i]['x_min'], y-charList[i]['y_min']) for x,y in charList[i]['points'] ]
    #过滤杂点
    ret = [one for one in charList if one['number'] > 6]
    #排序
    ret.sort(lambda a,b:a['x_min'] < b['x_min'])
    return ret

'''
    获取模型
'''
def getCharList():
    arr = {
        'char' : '',
        'data' : ''
    }
    trainfiles = os.listdir('json')
    charList = [copy.deepcopy(arr) for i in xrange(len(trainfiles))]
    i = 0
    for trainfile in trainfiles:
        (filepath,tempfilename) = os.path.split(trainfile);
        (shotname,extension) = os.path.splitext(tempfilename);
        if extension != '.json':
            continue
        f = open('json/'+trainfile, 'r')
        str = f.read()
        ret = json.loads(str.decode("utf8"))
        f.close()
        charList[i]['data'] = ret
        charList[i]['char'] = shotname
        i += 1
    return charList

'''
    识别字符
'''

def charSimilarity(charA,charB):

    s2 = set([(one[0],one[1]) for one in charB['points']])
    sumlen = len(charA['points']) + len(charB['points'])
    max = 0
    # 晃动匹配
    i_adjust = 1 if charB['width'] - charA['width'] >= 0 else -1
    j_adjust = 1 if charB['height'] - charA['height'] >= 0 else -1
    for i in xrange(0,charB['width'] - charA['width'] + i_adjust,i_adjust):
        for j in xrange(0,charB['height'] - charA['height'] + j_adjust,j_adjust):
            s1 = set([(one[0]+i,one[1]+j) for one in charA['points']])
            sim = len(s1&s2) *2.0 / sumlen
            if sim > max:
                max = sim
    return max


def recognise(one):
    trainfiles = os.listdir('json')
    i = 0
    max = 0
    char = None;
    for trainfile in trainfiles:
        (filepath,tempfilename) = os.path.split(trainfile);
        (shotname,extension) = os.path.splitext(tempfilename);
        if extension != '.json':
            continue
        f = open('json/'+trainfile, 'r')
        str = f.read()
        ret = json.loads(str.decode("utf8"))
        f.close()
        s = charSimilarity(one,ret)
        if s > max:
            char = shotname[0]
            max = s
        i += 1
    return char


'''
    训练获取字形模具
'''
def train():
    trainfiles = os.listdir('png')
    for trainfile in trainfiles:
        (filepath,tempfilename) = os.path.split(trainfile);
        (shotname,extension) = os.path.splitext(tempfilename);
        if extension != '.png':
            continue
        im = Image.open('png/'+trainfile)
        threshold = calcThreshold(im)
        imout = binaryzation(im,threshold)
        imout.show()
        ret = extractChar(imout)
        if len(ret) != len(shotname):
            continue
        for i in range(len(ret)):
            dump(shotname[i],ret[i])
'''
    获取字模
'''
def dump(char,dic):
    number = random.randint(0, 100)
    with open('json/'+ char + '_'+bytes(number)+'.json','wb') as f:
        f.write(json.dumps(dic))

'''
    下载图片保存到本地
'''
def downImg(flink):
    number = random.randint(1000, 10000)
    content2 = urllib2.urlopen(flink).read()
    with open(u'imgs'+'/temp_'+bytes(number)+'.png','wb') as code:
        code.write(content2)
    return 'imgs'+'/temp_'+bytes(number)+'.png'

def dowork(image_url):
    image_name = downImg(image_url)
    ans = []
    im = Image.open(image_name)
    threshold = calcThreshold(im)
    imout = binaryzation(im,threshold)
    imout.show()
    rets = extractChar(imout)
    for one in rets:
        ans.append(recognise(one))
    print ans
	
if __name__ == '__main__':
    dowork('http://www.zbjj.gov.cn:5555/imageServlet?0.08824421651661396')
#train()
