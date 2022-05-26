import numpy as np
import time
import os
# 创建csv文件
# 参数：经度数组，纬度数组，数据数组，输出路径，输出文件名
# 返回：无


def run(lon, lat, data, outpath, name):
    print("开始写入文件" + name)

    tic = time.time()

    res = np.array([lon, lat, data])
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    np.savetxt(os.path.join(outpath, name), res.T, delimiter=",", fmt='%.4f')

    # 头插一行
    with open(os.path.join(outpath, name), 'r') as f:
        lines = f.readlines()
    with open(os.path.join(outpath, name), 'w') as f:
        f.write('lon,lat,data\n')
        f.writelines(lines)

    toc = time.time()

    print("文件" + name + "写入完成，用时" + str(int(toc - tic)) + "s")
