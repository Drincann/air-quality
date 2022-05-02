import os
import math
import csv
import numpy as np
import matplotlib.pyplot as pyplot
import argparse

import CalculateWeight as cw
import TestWork as tw
import BuildMap as bm
import MainCalculatePart as mcp
import WriteCsv as wc
import FindDate as fd
pwd = os.path.dirname(__file__)
O3inpath = os.path.join(pwd, "./input/O3")
O3outpath = os.path.join(pwd, "./output/O3")
SPinpath = os.path.join(pwd, "./input/SP")
SPoutpath = os.path.join(pwd, "./output/SP")

#用于插值的总程序

# 需填写起止日期，例：python main.py -b 2022-02-23 -e 2022-02-24

argparser = argparse.ArgumentParser(description='InitDate')
argparser.add_argument('--beg', '-b', type = str, 
                       required = True, help = 'Begin date, format:XXXX-XX-XX')
argparser.add_argument('--end', '-e', type = str, 
                       required = True, help = 'End date, format:XXXX-XX-XX')
args = argparser.parse_args()

# 建立10倍权值表
w = cw.run()

# 处理O3
print("开始处理O3")

#查找日期
file_name = os.listdir(O3inpath)
needfile_name = fd.run(args.beg, args.end, file_name)

#主体
for loop in range(len(needfile_name)):
    print("处理日期为" + needfile_name[loop][0:8] + "的O3数据")

    # 读取文件
    file = csv.reader(open(O3inpath + "/" + needfile_name[loop]))

    # 将值映射到二维数组地图上
    map, mi = bm.run(file, "M8H_O3")

    # 检查图像
    # pyplot.imshow(map)
    # pyplot.show()

    # 利用权值表、地图进行插值（mi的目的是防止边缘过度模糊）
    reslat, reslon, resdata = mcp.run(w, map, mi)

    # 检查结果图像
    # tw.run(reslat,reslon,resdata)

    # 创建csv
    wc.run(reslon, reslat, resdata, O3outpath, needfile_name[loop])

# 处理组分
print("开始处理组分")

# 查找日期
file_name = os.listdir(SPinpath)
needfile_name = fd.run(args.beg, args.end, file_name)

# 主体
SP_name = ["SO4", "NO3", "NH4", "OM", "BC"]

for loop in range(len(needfile_name)):
    print("处理日期为" + needfile_name[loop][0:8] + "的SP文件")

    for i in range(len(SP_name)):
        print("处理" + SP_name[i])

        # 读取文件
        file = csv.reader(open(SPinpath + "/" + needfile_name[loop]))

        # 将值映射到二维数组地图上
        map, mi = bm.run(file, SP_name[i])

        # 检查图像
        # pyplot.imshow(map)
        # pyplot.show()

        # 利用权值表、地图进行插值（mi的目的是防止边缘过度模糊）
        reslat, reslon, resdata = mcp.run(w, map, mi)

        # 检查结果图像
        # tw.run(reslat,reslon,resdata)

        # 创建csv
        wc.run(reslon, reslat, resdata, SPoutpath +
               "/" + SP_name[i], needfile_name[loop])
