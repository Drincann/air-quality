# 插值主要计算部分
# 参数：权值表，二维地图，最小数据值
# 返回：纬度数组，经度数组，数据数组

def run(w, map, mi):
    reslat = []
    reslon = []
    resdata = []

    for i in range(399):
        if (i + 2) % 40 ==0:
            print(str((i + 2) / 4) + "%")
        for j in range(699):
            ltdata = map[i][j]
            rtdata = map[i][j + 1]
            lbdata = map[i + 1][j]
            rbdata = map[i + 1][j + 1]

            bglat = float(i + 150) / 10 + 0.05
            bglon = float(j + 700) / 10 + 0.05

            for nowr in range(10):
                for nowc in range(10):
                    nowdata = w[nowr][nowc][0] * ltdata + w[nowr][nowc][1] * rtdata + w[nowr][nowc][2] * lbdata + w[nowr][nowc][3] * rbdata
                    nowlat = bglat + 0.01 * nowr
                    nowlon = bglon + 0.01 * nowc

                    if nowdata > mi:
                        reslat.append(nowlat)
                        reslon.append(nowlon)
                        resdata.append(nowdata)
                        #float有精度损失
    return reslat, reslon, resdata