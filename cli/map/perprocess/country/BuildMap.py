# 建立二维地图，用作插值的参考数据
# 参数：csv文件，数据名
# 返回：二维地图，最小数据值

def run(file, data):
    map = []
    for i in range(400):
        row = []
        for j in range(700):
            row.append(0)
        map.append(row)

    mi = 9999
    line = 1
    for row in file:
        if(line == 1):
            line = -1

            for i in range(len(row)):
                if row[i] == data:
                    tag = i

            continue

        map[int(float(row[2])*10) - 150][int(float(row[1])*10) - 700] = float(row[tag])
        mi = min(mi, float(row[tag]))
    
    return map, mi