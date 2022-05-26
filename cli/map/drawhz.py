import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import matplotlib as mpl
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import argparse
import matplotlib.patches as mpatches
import shapefile
argparser = argparse.ArgumentParser(description='Draw')
argparser.add_argument('-i', '--input',  type=str,
                       required=True, help='input csv file')
argparser.add_argument('-n', '--lonName', type=str, nargs='+',
                       help='name of longitude col in csv', default='lon')
argparser.add_argument('-t', '--latName',  type=str, nargs='+',
                       help='name of latitude col in csv', default='lat')
argparser.add_argument('-v', '--dataName',  type=str, nargs='+',
                       help='name of data col in csv', default='data')
argparser.add_argument('-u', '--unit', type=str, nargs='+',
                       required=False, help='the unit align to the top right and colorbar', default='μg/m³')
argparser.add_argument('-d', '--dpi', type=int, required=False, default=300,)
argparser.add_argument('-o', '--output', type=str,
                       help='output png file', default='output.png')

pwd = os.getcwd()
currFileDir = os.path.join(os.path.dirname(os.path.realpath(__file__)))


# https://stackoverflow.com/questions/32333870/how-can-i-show-a-km-ruler-on-a-cartopy-matplotlib-plot
def scale_bar(ax, length=None, location=(0.5, 0.05), linewidth=3):
    """
    ax is the axes to draw the scalebar on.
    length is the length of the scalebar in km.
    location is center of the scalebar in axis coordinates.
    (ie. 0.5 is the middle of the plot)
    linewidth is the thickness of the scalebar.
    """
    # Get the limits of the axis in lat long
    llx0, llx1, lly0, lly1 = ax.get_extent(ccrs.PlateCarree())
    # Make tmc horizontally centred on the middle of the map,
    # vertically at scale bar location
    sbllx = (llx1 + llx0) / 2
    sblly = lly0 + (lly1 - lly0) * location[1]
    tmc = ccrs.TransverseMercator(sbllx, sblly)
    # Get the extent of the plotted area in coordinates in metres
    x0, x1, y0, y1 = ax.get_extent(tmc)
    # Turn the specified scalebar location into coordinates in metres
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    # Calculate a scale bar length if none has been given
    # (Theres probably a more pythonic way of rounding the number but this works)
    if not length:
        length = (x1 - x0) / 5000  # in km
        ndim = int(np.floor(np.log10(length)))  # number of digits in number
        length = round(length, -ndim)  # round to 1sf
        # Returns numbers starting with the list

        def scale_number(x):
            if str(x)[0] in ['1', '2', '5']:
                return int(x)
            else:
                return scale_number(x - 10 ** ndim)
        length = scale_number(length)

    # Generate the x coordinate for the ends of the scalebar
    bar_xs = [sbx - length * 500, sbx + length * 500]
    # Plot the scalebar
    ax.plot(bar_xs, [sby, sby], transform=tmc, color='k', linewidth=linewidth)
    # Plot the scalebar label
    ax.text(sbx, sby, str(length) + ' km', transform=tmc,
            horizontalalignment='center', verticalalignment='bottom', )


# https://blog.csdn.net/qq_32832803/article/details/110910540
def add_north(ax1, labelsize=15, loc_x=0.92, loc_y=0.9, width=0.02, height=0.07, pad=0.14):
    """
    画一个比例尺带'N'文字注释
    主要参数如下
    :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
    :param labelsize: 显示'N'文字的大小
    :param loc_x: 以文字下部为中心的占整个ax横向比例
    :param loc_y: 以文字下部为中心的占整个ax纵向比例
    :param width: 指南针占ax比例宽度
    :param height: 指南针占ax比例高度
    :param pad: 文字符号占ax比例间隙
    :return: None
    """
    minx, maxx = ax1.get_xlim()
    miny, maxy = ax1.get_ylim()
    ylen = maxy - miny
    xlen = maxx - minx
    left = [minx + xlen*(loc_x - width*.5), miny + ylen*(loc_y - pad)]
    right = [minx + xlen*(loc_x + width*.5), miny + ylen*(loc_y - pad)]
    top = [minx + xlen*loc_x, miny + ylen*(loc_y - pad + height)]
    center = [minx + xlen*loc_x, left[1] + (top[1] - left[1])*.4]
    triangle = mpatches.Polygon([left, top, right, center], color='k')
    ax1.text(s='N',
             x=minx + xlen*loc_x,
             y=miny + ylen*(loc_y - pad + height),
             fontsize=labelsize,
             horizontalalignment='center',
             verticalalignment='bottom')
    ax1.add_patch(triangle)


def isInPolygon(position, polygons):  # 传参为待测点和多边形,判断该点是否在多边形内部，点为单个数，多边形为数组
    # 从待求点引一条射线，该射线与多边形交点为奇数个则点在多边形内部
    sign = 0  # 标志位
    st = 1
    lon = position[0]
    lat = position[1]
    for polygon in polygons:
        for loop_one in range(len(polygon.points)-1):  # 循环所有的点
            if len(polygon.parts) != 1:  # 跳过每块的结束的点
                if loop_one == polygon.parts[st]-1:
                    if st != len(polygon.parts)-1:
                        st += 1
                    continue
            if (polygon.points[loop_one][1] >= lat and polygon.points[loop_one+1][1] <= lat) or (polygon.points[loop_one][1] <= lat and polygon.points[loop_one+1][1] >= lat):  # 粗判断范围
                # 线段坐标x均小于待求点，线在点的左边
                if polygon.points[loop_one][0] < lon and polygon.points[loop_one+1][0] < lon:
                    continue
                # 线段坐标x均大于待求点，线在点的右边
                elif polygon.points[loop_one][0] > lon and polygon.points[loop_one+1][0] > lon:
                    sign += 1
                else:
                    k = (polygon.points[loop_one][1]-polygon.points[loop_one+1][1])/(
                        polygon.points[loop_one][0]-polygon.points[loop_one+1][0])  # 求斜率
                    x = (lat-polygon.points[loop_one][1])/k + \
                        polygon.points[loop_one][0]  # 使用点斜式求交点的x坐标值
                    if x >= lon:
                        sign += 1
        if sign % 2 != 0:
            return True
    return False


def draw(*, saveto,  lons, lats, values, dpi, unit, HZPolygon,):

    fig = plt.figure(figsize=[15, 10], dpi=150)
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_extent([118, 121, 29, 30.7], crs=ccrs.PlateCarree())
# 框选杭州区域 "./Hangzhou-Shp/HZQX.shp"
    for points in HZPolygon:
        ax.plot(points[0], points[1], color='black', linewidth=1.5,
                transform=ccrs.PlateCarree(), alpha=1, zorder=2)

    cbarticks = [35, 75, 115, 150, 250]
    norm = mpl.colors.Normalize(vmin=cbarticks[0], vmax=cbarticks[-1])
    im = ax.scatter(lons, lats, c=values, s=1, transform=ccrs.PlateCarree(
    ), cmap=cm.Spectral_r, norm=norm, alpha=1, zorder=1)

    fig.subplots_adjust(right=0.93)
    position = fig.add_axes([0.95, 0.22, 0.015, .55])  # 位置[左,下,右,上]
    cb = fig.colorbar(im, cax=position)
    font = {
        'color': 'black',
        'weight': 'normal',
        'size': 20,
    }
    cb.set_label(unit, fontdict=font)
    cb.set_ticks(cbarticks)
    tl = cb.ax.set_yticklabels(cbarticks, fontdict=font)
    cb.ax.tick_params(labelsize=16, direction='out')
    # 经纬度 刻度
    ax.gridlines(draw_labels=False, linewidth=0.6, color='black',
                 alpha=0.5, linestyle='--', crs=ccrs.PlateCarree(),)

    # 右上角绘制指北针
    add_north(ax, loc_x=0.95, loc_y=0.99)
    plt.savefig(saveto, dpi=dpi, bbox_inches='tight')
    # plt.show()


def main():
    args = argparser.parse_args()
    data = pd.read_csv(os.path.join(pwd, args.input))
    lons = data[args.lonName].values.reshape((len(data[args.lonName]),))
    lats = data[args.latName].values.reshape((len(data[args.latName]),))
    __dirname = os.path.dirname(os.path.abspath(__file__))
    with shapefile.Reader(os.path.join(__dirname, './Hangzhou-Shp/HZ.shp'), encoding='GBK') as shapef:
        shapes = shapef.shapes()
        HZPolygon = [*map(lambda shape:np.array(shape.points).T,  shapes)]
    dataDict = {}
    for lon, lat, value in data.values:
        dataDict[(lon, lat)] = value
    HZStartLon = np.min([*map(lambda points:np.min(points[0]), HZPolygon)])
    HZEndLon = np.max([*map(lambda points:np.max(points[0]), HZPolygon)])
    HZStartLat = np.min([*map(lambda points:np.min(points[1]), HZPolygon)])
    HZEndLat = np.max([*map(lambda points:np.max(points[1]), HZPolygon)])
    # 杭州浓度采样点
    HZDataList = []
    HZlons = []
    HZlats = []
    # index = 0

    for lon, lat in zip(lons, lats):
        if lon >= HZStartLon and lon <= HZEndLon and lat >= HZStartLat and lat <= HZEndLat:
            # index += 1
            # if index % 100 != 0:
            #     continue
            if isInPolygon((lon, lat), shapes):
                HZDataList.append(dataDict[(lon, lat)])
                HZlons.append(lon)
                HZlats.append(lat)
    draw(saveto=args.output,
         lons=HZlons, lats=HZlats,
         values=HZDataList,
         unit=args.unit,
         dpi=args.dpi, HZPolygon=HZPolygon)


main()
