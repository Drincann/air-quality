# 检测插值后的图像的正确性
# 参数：纬度数组，经度数组，数据数组
# 返回：无

import matplotlib.pyplot as pyplot

def run(lat, lon, data):
    print("开始测试有无错误")

    mapp = []
    for i in range(4000):
        row = []
        for j in range(7000):
            row.append(0)
        mapp.append(row)

    error = 0
    for i in range(len(data)):
        if(mapp[round(lat[i]*100) - 1500][round(lon[i]*100) - 7000] != 0):
            error += 1
        mapp[round(lat[i]*100) - 1500][round(lon[i]*100) - 7000] = round(data[i], 2)

    print("重复赋值的错误个数为：" + str(error))

    print("开始画图")
    pyplot.imshow(mapp)
    pyplot.show()