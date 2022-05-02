import io
import sys
import time
import numpy as np
import pandas
import requests
import os
import pickle
import zipfile
import WriteCsv as wc


def saveFromUrls(urls: list, outputPath: str, filename: str) -> None:
    lons = []
    lats = []
    data = []
    grid2Data = {}
    print('正在下载数据... ', end='')
    for url in urls:
        out = f'{(urls.index(url)/(len(urls) - 1))*100:6.2f}%'
        print(out + '\b'*len(out), end='')
        sys.stdout.flush()

        # down to memory
        res = requests.get(url)
        # 重试
        while res.status_code != 200:
            res = requests.get(url)
            time.sleep(1)

        # unzip in memory
        with zipfile.ZipFile(io.BytesIO(res.content)) as z:
            for name in z.namelist():
                csvData = pandas.read_csv(io.BytesIO(z.read(name)))
                if 'Longitude' in csvData:
                    # position file
                    lons.extend(csvData['Longitude'].values)
                    lats.extend(csvData['Latitude'].values)
                    data.extend(csvData['GridID'].values)
                else:
                    # datafile
                    for grid, pm25 in csvData.values:
                        grid2Data.setdefault(grid, pm25)
    print('\n处理数据...')

    data = np.vectorize(lambda grid: grid2Data.get(grid, np.nan))(data)
    # remove
    removedIdx = np.where(np.isnan(data) == True)[0]
    lons = np.delete(lons, removedIdx)
    lats = np.delete(lats, removedIdx)
    data = np.delete(data, removedIdx)

    wc.run(lons, lats, data, outputPath, filename)
