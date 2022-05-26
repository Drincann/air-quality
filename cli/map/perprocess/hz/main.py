import os
import numpy as np
import math
import pandas as pd
import argparse
import matplotlib.pyplot as plt

import WriteCsv as wc

def dist(x1,y1,x2,y2):
    tx = (x1 - x2)
    ty = (y1 - y2)
    return math.sqrt(tx * tx + ty * ty)

def indiv(x):
    for i in range(0,220,12):
        if abs(x - i) < 6:
            return i
    return x

# locapath为记录站点经纬度的文件，datapath为记录站点数据的文件
currDir = os.path.dirname(__file__)
locapath = os.path.join(currDir, "./input/loca.xlsx")
datapath = os.path.join(currDir, "./input/data.xlsx")
outpath = os.path.join(currDir, "./output")

# 需要输入所选的日期、时间。日期只有年月日的日，时间为00-23.
# 例：python main.py -d 25 -t 03
argparser = argparse.ArgumentParser(description='InitHour')
argparser.add_argument('--day', '-d', type=str,
                       required=True, help='Which day(00 - 31/30/28), format1:07, format2:28')
argparser.add_argument('--tim', '-t', type=str,
                       required=True, help='Which time(00 - 23), format1:05, format2:18')
args = argparser.parse_args()

day = int(args.day)
tim = int(args.tim)

df = pd.read_excel(locapath)
loca = df.values

nam = []
lon = {}
lat = {}

for i in range(len(loca)):
    nam.append(loca[i][0])
    lon[loca[i][0]] = loca[i][1]
    lat[loca[i][0]] = loca[i][2]

df = pd.read_excel(datapath)
data = df.values

beg = (day - 1) * 4752 + tim * 198
end = beg + 198
nee = data[beg:end][:]
# print(nee)

dat = {}

for i in range(len(nee)):
    dat[nee[i][1]] = nee[i][3]

# ddata为处理好要利用的数据
ddata = []
for i in nam:
    temp = []

    if i in dat:
        temp.append(lon[i])
        temp.append(lat[i])

        if dat[i] == '--':
            temp.append(0.0)
        else:
            temp.append(float(dat[i]))
    else:
        continue

    ddata.append(temp)

map = np.zeros((800, 1200))

# IDW散点插值
for i in range(1200):
    baifenbi = i / 12
    if(i % 120 == 0):
        print(baifenbi)
    for j in range(800):
        nowlon = i / 400 + 118
        nowlat = j / 400 + 29

        nowdis = []
        nowdat = []

        for k in ddata:
            templon = k[0]
            templat = k[1]
            tempdat = k[2]

            tempdis = dist(nowlon, nowlat, templon, templat)
            nowdis.append(tempdis)
            nowdat.append(tempdat)

        flag = 0
        for k in range(len(nowdat)):
            if nowdis[k] == 0:
                flag = k
                break
        
        if flag != 0:
            map[j][i] = nowdat[flag]
            continue
        
        nowrat = []
        for k in range(len(nowdat)):
            nowrat.append(1 / (nowdis[k] ** 4))
        all = sum(nowrat)

        for k in range(len(nowdat)):
            map[j][i] = map[j][i] + nowrat[k] / all * nowdat[k]
        
        # 模糊处理数据使其变得好看
        map[j][i] = indiv(map[j][i])

# plt.matshow(map)
# plt.show()

reslon = []
reslat = []
resdat = []

for i in range(1200):
    for j in range(800):
        nowlon = i / 400 + 118
        nowlat = j / 400 + 29

        reslon.append(nowlon)
        reslat.append(nowlat)
        resdat.append(map[j][i])

wc.run(reslon, reslat, resdat, outpath, args.day + args.tim + ".csv")