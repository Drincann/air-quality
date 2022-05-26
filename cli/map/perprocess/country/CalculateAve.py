import os
import math
import csv
import numpy as np
import matplotlib.pyplot as pyplot
import argparse
import matplotlib.pyplot as pyplot

import FindDate as fd
import WriteCsv as wc
import TestWork as tw

pwd = os.path.dirname(__file__)

# 用于求平均数据的程序

# 需填写求平均的数据类型和起止日期，例：python CalculateAve.py -t O3 -b 2022-02-23 -e 2022-02-24

argparser = argparse.ArgumentParser(description='InitDate')
argparser.add_argument('--type', '-t', type = str, 
                       required = True, help = 'Type, PM25, O3, SO4, NO3, NH4, OM, BC')
argparser.add_argument('--beg', '-b', type = str, 
                       required = True, help = 'Begin date, format:XXXX-XX-XX')
argparser.add_argument('--end', '-e', type = str, 
                       required = True, help = 'End date, format:XXXX-XX-XX')
args = argparser.parse_args()

if args.type == "PM25" or args.type == "O3":
    inpath = os.path.join(pwd, "./output/" + args.type)
    outpath = os.path.join(pwd, "./output/Ave/" + args.type)
else:
    inpath = os.path.join(pwd, "./output/SP/" + args.type)
    outpath = os.path.join(pwd, "./output/Ave/SP/" + args.type)


file_name = os.listdir(inpath)
needfile_name = fd.run(args.beg, args.end, file_name)

map = []
for i in range(4000):
    row = []
    for j in range(7000):
        row.append(0)
    map.append(row)

for loop in range(len(needfile_name)):
    print("加平均处理日期为" + needfile_name[loop][0:8] + "的数据")

    # 读取文件
    file = csv.reader(open(inpath + "/" + needfile_name[loop]))

    line = 1
    for row in file:
        if(line == 1):
            line = -1
            continue

        map[int((float(row[1]) - 0.049)*100) - 1500][int((float(row[0]) - 0.049)*100) - 7000] += float(row[2])
    
    # pyplot.imshow(map)
    # pyplot.show()

reslon = []
reslat = []
resdata = []

error = 0
for i in range(4000):
    for j in range(7000):

        nowlat = float(i + 1500) / 100 + 0.05
        nowlon = float(j + 7000) / 100 + 0.05
        nowdata = map[i][j] / len(needfile_name)

        if nowdata > 0:
            reslat.append(nowlat)
            reslon.append(nowlon)
            resdata.append(nowdata)

# tw.run(reslat,reslon,resdata)

wc.run(reslon, reslat, resdata, outpath,
 needfile_name[0][0:8] + "_" + needfile_name[len(needfile_name)-1][0:8] + "_" + args.type + "csv")