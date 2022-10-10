import numpy as np
import re
import warnings
import re
import csv
warnings.filterwarnings('ignore')


def get_word_vector(s1, s2):
    """
    :param s1: 句子1
    :param s2: 句子2
    :return: 返回中英文句子切分后的向量
    """

    # 把句子按字分开，中文按字分，英文按单词，数字按空格
    regEx = re.compile('[\\W]*')
    res = re.compile(r"([\u4e00-\u9fa5])")

    p1 = regEx.split(s1.lower())
    str1_list = []
    for str in p1:
        if res.split(str) == None:
            str1_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str1_list.append(ch)
    # print(str1_list)

    p2 = regEx.split(s2.lower())
    str2_list = []
    for str in p2:
        if res.split(str) == None:
            str2_list.append(str)
        else:
            ret = res.split(str)
            for ch in ret:
                str2_list.append(ch)
    # print(str2_list)

    list_word1 = [w for w in str1_list if len(w.strip()) > 0]  # 去掉为空的字符
    list_word2 = [w for w in str2_list if len(w.strip()) > 0]  # 去掉为空的字符
    #print(list_word1, list_word2)

    # 列出所有的词,取并集
    key_word = list(set(list_word1 + list_word2))
    #print(key_word)
    # 给定形状和类型的用0填充的矩阵存储向量
    word_vector1 = np.zeros(len(key_word))
    word_vector2 = np.zeros(len(key_word))

    # 计算词频
    # 依次确定向量的每个位置的值
    for i in range(len(key_word)):
        # 遍历key_word中每个词在句子中的出现次数
        for j in range(len(list_word1)):
            if key_word[i] == list_word1[j]:
                word_vector1[i] += 1
        for k in range(len(list_word2)):
            if key_word[i] == list_word2[k]:
                word_vector2[i] += 1

    # 输出向量
    #print(word_vector1)
    #print(word_vector2)
    return word_vector1, word_vector2


def cos_dist(vec1, vec2):
    """
    :param vec1: 向量1
    :param vec2: 向量2
    :return: 返回两个向量的余弦相似度
    """
    dist1 = float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))
    return dist1


if __name__ == '__main__':
    with open('./train.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile)
        column_1 = [row[1] for row in reader]
    with open('./train.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile)
        column_2 = [row[2] for row in reader]
    #print(column_1)
    #print(column_2)

    # pattern = r',|\.|/|;|\'|`|\[|\]|<|>|\?|:|"|\{|\}|\~|!|@|#|\$|%|\^|&|\(|\)|-|=|\_|\+|，|。|、|；|‘|’|【|】|·|！| |…|（|）'
    pattern = r',|，|、'
    for target,i in zip(column_1,column_2):

        #for i in column_2:
        i = i.replace(" ", "")
        result_list = re.split(pattern, i)

        for test_text in result_list:
            vec1, vec2 = get_word_vector(target, test_text)
            dist1 = cos_dist(vec1, vec2)
            fp = open("./output.txt", "a+")  # a+ 如果文件不存在就创建。存在就在文件内容的后面继续追加
            print(target,test_text,dist1,'\n', file=fp)
            fp.close()
    target = '供应商基本情况表'

    test_text = '投标人基本情况表'

    vec1, vec2 = get_word_vector(target, test_text)
    dist1 = cos_dist(vec1, vec2)
    print(dist1)