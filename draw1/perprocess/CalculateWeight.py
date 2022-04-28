import math

# 计算权重，用作插值的参考数据
# 参数：无
# 返回：四点权值表

def dist(x1,y1,x2,y2):
    tx = (x1 - x2)
    ty = (y1 - y2)
    return math.sqrt(tx * tx + ty * ty)

def run():
    w = []
    for i in range(10):
        temp1 = []
        for j in range(10):
            temp2 = []
            for k in range(4):
                temp2.append(0)
            temp1.append(temp2)
        w.append(temp1)

    for i in range(10):
        for j in range(10):
            ltww = 10 - dist(0, 0, i, j)
            if ltww < 0:
                ltww = 0
            rtww = 10 - dist(0, 10, i, j)
            if rtww < 0:
                rtww = 0
            lbww = 10 - dist(10, 0, i, j)
            if lbww < 0:
                lbww = 0
            rbww = 10 - dist(10, 10, i, j)
            if rbww < 0:
                rbww = 0

            tot = ltww + rtww + lbww + rbww

            w[i][j][0] = ltww / tot
            w[i][j][1] = rtww / tot
            w[i][j][2] = lbww / tot
            w[i][j][3] = rbww / tot
    return w