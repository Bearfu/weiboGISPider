import math
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.path as mplPath


def GeneratePointInCycle3(point_num, radius):
    for i in range(1, point_num + 1):
        theta = random.random() * 2 * pi
        r = random.uniform(0, radius)
        x = r * math.sin(theta)
        y = r * math.cos(theta)
        plt.plot(x, y, '*', color="black")

    # 博客算法4


def GeneratePointInCycle4(point_num, radius):
    for i in range(1, point_num + 1):
        theta = random.random() * 2 * pi
        r = random.uniform(0, radius)
        x = math.sin(theta) * (r ** 0.5)
        y = math.cos(theta) * (r ** 0.5)
        plt.plot(x, y, '*', color="black")


def GeneratePointInTriangle(point_num, pointA, pointB, pointC):
    for i in range(1, point_num + 1):
        pointP = np.array([random.uniform(pointA[0], pointB[0]), random.uniform(pointA[1], pointC[1])])
        if not IsPointInTriangle(pointA, pointB, pointC, pointP):
            if pointP[0] > pointC[0]:
                pointP = ComputeCentralSymmetryPoint(pointP, np.array(
                    [(pointC[0] + pointB[0]) / 2, (pointC[1] + pointB[1]) / 2]))
            else:
                pointP = ComputeCentralSymmetryPoint(pointP, np.array(
                    [(pointC[0] + pointA[0]) / 2, (pointC[1] + pointA[1]) / 2]))
        plt.plot(pointP[0], pointP[1], '*', color="black")


def OneGeneratePointInTriangle(pointA, pointB, pointC):
    while 1:
        pointP = np.array([random.uniform(pointA[0], pointB[0]), random.uniform(pointA[1], pointC[1])])
        if not IsPointInTriangle(pointA, pointB, pointC, pointP):
            if pointP[0] > pointC[0]:
                pointP = ComputeCentralSymmetryPoint(pointP, np.array(
                    [(pointC[0] + pointB[0]) / 2, (pointC[1] + pointB[1]) / 2]))
            else:
                pointP = ComputeCentralSymmetryPoint(pointP, np.array(
                    [(pointC[0] + pointA[0]) / 2, (pointC[1] + pointA[1]) / 2]))
        return pointP


# 根据向量叉乘计算三角形面积，参考 http://www.cnblogs.com/TenosDoIt/p/4024413.html
def ComputeTriangleArea(pointA, pointB, pointC):
    return math.fabs(np.cross(pointB - pointA, pointB - pointC)) / 2.0


# 判断点P是否在三角形ABC内,参考 http://www.cnblogs.com/TenosDoIt/p/4024413.html
def IsPointInTriangle(pointA, pointB, pointC, pointP):
    area_abc = ComputeTriangleArea(pointA, pointB, pointC)
    area_pab = ComputeTriangleArea(pointA, pointB, pointP)
    area_pbc = ComputeTriangleArea(pointP, pointB, pointC)
    area_pac = ComputeTriangleArea(pointP, pointA, pointC)
    return math.fabs(area_pab + area_pac + area_pbc - area_abc) < 0.000001


# 计算一个点关于某一点的中心对称点
def ComputeCentralSymmetryPoint(point_src, point_center):
    return np.array([point_center[0] * 2 - point_src[0], point_center[1] * 2 - point_src[1]])


'''
@description 判断点point是否在由顶点数组vertices所指定的多边形内部
思想：将点point和多边形所有的顶点链接起来，计算相邻两边的夹角之和，
若和等于360°，那说明该点就在多边形内。
参考链接：http://www.html-js.com/article/1538
@param  point 待判断的点。有两个分量的List。
@param  vertices 多边形顶点数组，其中的前后相邻的元素在多边形上也
是相邻的。3个以上的二分量List(一个二分量List为一个顶点)组成的List。
@return 若在多边形之内或者在多边形的边界上，返回True，否则返回False
'''


def is_in_2d_polygon(point, vertices):
    px = point[0]
    py = point[1]
    angle_sum = 0

    size = len(vertices)
    if size < 3:
        raise ValueError("len of vertices < 3")
    j = size - 1
    for i in range(0, size):
        sx = vertices[i][0]
        sy = vertices[i][1]
        tx = vertices[j][0]
        ty = vertices[j][1]

        # 计算夹角
        angle = math.atan2(sy - py, sx - px) - math.atan2(ty - py, tx - px)
        # angle需要在-π到π之内
        if angle >= math.pi:
            angle = angle - math.pi * 2
        elif angle <= -math.pi:
            angle = angle + math.pi * 2

        # 累积
        angle_sum += angle
        j = i

    # 计算夹角和于2*pi之差，若小于一个非常小的数，就认为相等
    print(math.fabs(angle_sum - math.pi * 2))
    return math.fabs(angle_sum - math.pi * 2) < 10


def isRayIntersectsSegment(poi, s_poi, e_poi):  # [x,y] [lng,lat]
    # 输入：判断点，边起点，边终点，都是[lng,lat]格式数组
    if s_poi[1] == e_poi[1]:  # 排除与射线平行、重合，线段首尾端点重合的情况
        return False
    if s_poi[1] > poi[1] and e_poi[1] > poi[1]:  # 线段在射线上边
        return False
    if s_poi[1] < poi[1] and e_poi[1] < poi[1]:  # 线段在射线下边
        return False
    if s_poi[1] == poi[1] and e_poi[1] > poi[1]:  # 交点为下端点，对应spoint
        return False
    if e_poi[1] == poi[1] and s_poi[1] > poi[1]:  # 交点为下端点，对应epoint
        return False
    if s_poi[0] < poi[0] and e_poi[1] < poi[1]:  # 线段在射线左边
        return False

    xseg = e_poi[0] - (e_poi[0] - s_poi[0]) * (e_poi[1] - poi[1]) / (e_poi[1] - s_poi[1])  # 求交
    if xseg < poi[0]:  # 交点在射线起点的左侧
        return False
    return True  # 排除上述情况之后


def isPoiWithinPoly(poi, poly):
    # 输入：点，多边形三维数组
    # poly=[[[x1,y1],[x2,y2],……,[xn,yn],[x1,y1]],[[w1,t1],……[wk,tk]]] 三维数组

    # 可以先判断点是否在外包矩形内
    # if not isPoiWithinBox(poi,mbr=[[0,0],[180,90]]): return False
    # 但算最小外包矩形本身需要循环边，会造成开销，本处略去
    sinsc = 0  # 交点个数
    for epoly in poly:  # 循环每条边的曲线->each polygon 是二维数组[[x1,y1],…[xn,yn]]
        for i in range(len(epoly) - 1):  # [0,len-1]
            s_poi = epoly[i]
            e_poi = epoly[i + 1]
            if isRayIntersectsSegment(poi, s_poi, e_poi):
                sinsc += 1  # 有交点就加1

    return True if sinsc % 2 == 1 else False


# 返回一个四边形空间坐标内的随机点
# 这里是对信息源数据去取巧了
# 由于给到的都是四边形，且四个点的坐标是知道左上右下关系的
# 所以我们直接将四边形一份为二 然后根据面积来获取一个落点权重，最后依据权重。选择其中一个三角区来获取位置坐标
# def OneGeneratePointInQuadrilateral(pointA, pointB, pointC, pointD):
#     TriangleA = [pointA, pointB, pointC]
#     TriangleB = [pointB, pointC, pointD]
#     AreaA = ComputeTriangleArea(TriangleA[0], TriangleA[1], TriangleA[2])
#     AreaB = ComputeTriangleArea(TriangleB[0], TriangleB[1], TriangleB[2])
#     if random.uniform(0, 1) < (AreaA / (AreaA + AreaB)):
#         print("A")
#         return OneGeneratePointInTriangle(pointA, pointB, pointC)
#     else:
#         print("B")
#         return OneGeneratePointInTriangle(pointB, pointC, pointD)

def OneGeneratePointInQuadrilateral(pointA, pointB, pointC, pointD):
    while 1:
        xMin = min(pointA[0], pointB[0], pointC[0], pointD[0])
        xMax = max(pointA[0], pointB[0], pointC[0], pointD[0])
        yMin = min(pointA[1], pointB[1], pointC[1], pointD[1])
        yMax = max(pointA[1], pointB[1], pointC[1], pointD[1])
        pointP = np.array([random.uniform(xMin, xMax), random.uniform(yMin, yMax)])
        vertices = [pointA, pointB, pointC, pointD]
        # return pointP
        bbPath = mplPath.Path(np.array([pointA,
                                        pointC,
                                        pointD,
                                        pointB]))

        if bbPath.contains_point(pointP):
            return pointP


def GeneratePointInQuadrilateral(point_num, pointA, pointB, pointC, pointD):
    for i in range(1, point_num + 1):
        pointP = OneGeneratePointInQuadrilateral(pointA, pointB, pointC, pointD)
        plt.plot(pointP[0], pointP[1], '*', color="black")


if __name__ == '__main__':
    # 圆形
    # pi = np.pi
    # theta = np.linspace(0, pi * 2, 1000)
    # R = 1
    # x = np.sin(theta) * R
    # y = np.cos(theta) * R
    #
    # plt.figure(figsize=(6, 6))
    # plt.plot(x, y, label="cycle", color="red", linewidth=2)
    # plt.title("cycyle")
    # GeneratePointInCycle3(4000, R)  # 修改此处来显示不同算法的效果
    # plt.legend()
    # plt.show()

    # 三角形

    # 四边形
    pointA = np.array([116.381000, 39.960000])
    pointB = np.array([116.422000, 39.960000])
    pointC = np.array([116.393000, 39.871000])
    pointD = np.array([116.436000, 39.871000])

    plt.plot([pointA[0], pointB[0]], [pointA[1], pointB[1]])
    plt.plot([pointA[0], pointC[0]], [pointA[1], pointC[1]])
    plt.plot([pointC[0], pointD[0]], [pointC[1], pointD[1]])
    plt.plot([pointB[0], pointD[0]], [pointB[1], pointD[1]])

    # GeneratePointInTriangle(1500, pointA, pointB, pointC)

    GeneratePointInQuadrilateral(1500, pointA, pointB, pointC, pointD)  # 修改此处来显示不同算法的效果
    # 画坐标
    plt.ylim(39.871000, 39.960000)
    plt.xlim(116.381000, 116.436000)
    plt.show()

    print(round(OneGeneratePointInQuadrilateral(pointA, pointB, pointC, pointD)[0], 6))
    print(round(OneGeneratePointInQuadrilateral(pointA, pointB, pointC, pointD)[1], 6))
