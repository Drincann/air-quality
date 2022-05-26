from sqlite3 import Time
from time import time
import pandas as pd

def run(beg, end, name):
    time = []
    res = []

    if beg[4] != '-' or beg[7] != '-' or end[4] != '-' or end[7] != '-':
        print("需求日期的格式有误")
        return res

    df = pd.date_range(beg,end)
    for i in range(len(df)):
        time.append(str(df[i]).split()[0])
    
    for loop in time:
        loopnow = loop[0:4] + loop[5:7] + loop[8:10]

        flag = 0
        for exi in name:
            exinow = exi[0:8]
            if loopnow == exinow:
                res.append(exi)
                flag = 1
                break
        if flag == 0:
            print("需要处理" + loop + "的数据，但数据文件未找到")
    return res




