import numpy as np
import time

# 创建csv文件
# 参数：经度数组，纬度数组，数据数组，输出路径，输出文件名
# 返回：无

def run(lon, lat, data, outpath, name):
    print("开始写入文件" + name)

    tic = time.time()

    res = np.array([lon, lat, data])
    np.savetxt(outpath + "/" + name, res.T, delimiter=",", fmt='%.2f')
    
    toc = time.time()

    print("文件" + name + "写入完成，用时" + str(int(toc - tic)) + "s")