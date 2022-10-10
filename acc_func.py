

def Accuracy(data1, data2):
    """
    计算两个列表的列表的相同部分所占的比例

    :param data1: 列表一
    :param data2: 列表二
    :return:
    """
    num, acc_num = 0, 0
    for i in range(len(data1)):
        for j in range(len(data1[i])):
            if data1[i][j] == data2[i][j]:
                acc_num+=1
            num +=1
        acc = acc_num/num
    return acc


# 编辑距离
def Edit_Dist(a, b):
    """
    计算两字符串之间的编辑距离

    :param a: 字符串1
    :param b: 字符串2
    :return: 两个字符串之间的编辑距离
    """
    m, n = len(a) + 1, len(b) + 1
    d = [[0] * n for i in range(m)]
    d[0][0] = 0
    for i in range(1, m):
        d[i][0] = d[i - 1][0] + 1

    for j in range(1, n):
        d[0][j] = d[0][j - 1] + 1
    temp = 0
    for i in range(1, m):
        for j in range(1, n):
            if a[i - 1] == b[j - 1]:
                temp = 0
            else:
                temp = 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + temp)
    # 输出d[i][j]矩阵
    # for i in range(m):
        # print(d[i])
    return d[m - 1][n - 1]


def edit_dist_acc(data1, data2):
    """
    通过计算编辑距离比较两个列表的列表的相似程度

    :param data1: 列表一
    :param data2: 列表二
    :return:
    """
    num, acc_num = 0, 0
    for i in range(len(data1)):
        for j in range(len(data1[i])):
            distance = Edit_Dist(data1[i][j],data2[i][j])
            sum_len = len(data1[i][j])+len(data2[i][j])
            # print("字符串1:",data1[i][j],"字符串2:",data2[i][j],"编辑距离:",distance)
            if distance/sum_len < 0.3:
                acc_num += 1
                # print("相似，判定为一个实体")
            else:
                # print("不相似")
                pass
            num += 1
        acc = acc_num / num
    return acc
# ed = Edit_Dist("江苏苏州", "江苏省苏州市")
# print('编辑距离为：', ed)

