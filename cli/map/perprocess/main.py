import os
import math
import csv
import numpy as np
import matplotlib.pyplot as pyplot

import CalculateWeight as cw
import TestWork as tw
import BuildMap as bm
import MainCalculatePart as mcp
import WriteCsv as wc
pwd = os.path.dirname(__file__)
O3inpath = os.path.join(pwd, "./input/O3")
O3outpath = os.path.join(pwd, "./output/O3")
SPinpath = os.path.join(pwd, "./input/SP")
SPoutpath = os.path.join(pwd, "./output/SP")

# 建立10倍权值表
w = cw.run()

# 处理O3
file_name = os.listdir(O3inpath)

for loop in range(len(file_name)):
    print("处理O3第" + str(loop+1) + "个文件")

    # 读取文件
    file = csv.reader(open(O3inpath + "/" + file_name[loop]))

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
    wc.run(reslon, reslat, resdata, O3outpath, file_name[loop])

# 处理组分
file_name = os.listdir(SPinpath)
SP_name = ["SO4", "NO3", "NH4", "OM", "BC"]

for loop in range(len(file_name)):
    print("处理SP第" + str(loop+1) + "个文件")

    for i in range(len(SP_name)):
        print("处理" + SP_name[i])

        # 读取文件
        file = csv.reader(open(SPinpath + "/" + file_name[loop]))

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
               "/" + SP_name[i], file_name[loop])
