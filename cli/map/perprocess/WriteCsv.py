import csv

# 创建csv文件
# 参数：经度数组，纬度数组，数据数组，输出路径，输出文件名
# 返回：无


def run(lon, lat, data, outpath, name):
    print("开始写入文件" + name)

    csvfile = open(outpath + "/" + name, 'w', newline="")
    writer = csv.writer(csvfile)
    writer.writerow(['lon', 'lat', 'data'])
    for i in range(len(data)):
        writer.writerow(
            [round(lon[i], 2), round(lat[i], 2), round(data[i], 2)])

    print("文件" + name + "写入完成")
