import re

def remove_lines(line):
    if line == '\n':  # 空行移除
        return False
        # print(line)
    if line.endswith('\n'):  # 移除空行
        t = line[:-1]  # test line
        if t.endswith('要求') or t.endswith('包括') or t.endswith('：') or t.endswith('组成') or t.endswith('内容') or t.endswith('：') or t.endswith('?') or t.endswith('构成'):  # 移除描述行
            return False
    if len(line) > 0 and (is_Chinese(line[0]) or line[0]=="\uFF08"):
        #print("chinese:",line)
        line = remove_chinesenumber(line)
    else:
        line = remove_number(line)
    return line



def get_index(lst=None,item=''): #找到元素的所有索引
    return [i for i in range(len(lst)) if lst[i]==item]


def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False


def remove_chinesenumber(line): #移除诸如一、一.等的标号
    #print("original:",line)
    nline = re.sub(r'（[一|二|三|四|五|六|七|八|九|十|\d]+）', '', line, count=1)
    #print("nline:",nline)
    t = re.split('^.*[一|二|三|四|五|六|七|八|九|十]+[、：]',nline,1)
    if len(t) > 1:
        print(t)
        nline = t[1]
    #print(nline)
    return nline

def remove_number(line): #移除数字标号和字母标号

    #7、供应商同类项目实施情况一览表 (见附件8)；合并处理、）)的话，这一句会被删除掉
    # 顺序也很重要，应该先把复杂的匹配放前面
    nline = re.sub(r'^(\d*\.)+\d*、*|^(\d*\．)\+\d*、*|^\d+[、]|^\(\d+\)|^(\d+)|^\d+[）)]|^\d\-\d|^[a-zA-Z][\.、)）]', '', line, count=1)
    print(nline)
    nline = re.sub(r' ', '', nline)
    s = re.split('^\d+ | ^·', nline, 1)  # 去除序号的最后一个数字 或者 ·
    if len(s) > 1:
        nline = s[1]

    s = re.split('^★|^△|^\* |^□|^●|^·|^◆|^\.', nline, 1)  # 去除句首的特殊符号
    if len(s) > 1:
        nline = s[1]
    t = re.split(
        '^.*[\u2168|^.*\u2167|^.*\u2166|^.*\u2165|^.*\u2164|^.*\u2163|^.*\u2162|^.*\u2161|^.*\u2160|^.*\u215F]+[\.：:]*',
        nline, 1)  #移除罗马数字
    if len(t) > 1:
        nline = t[1]
    s = re.split('①|②|③|③|④|⑤|⑥|⑦|⑧|^I|^\*|^\d', nline, 1)  # 去除句首的特殊符号
    if len(s) > 1:
        nline = s[1]

    #print("nline: ",nline)
    return nline

#remove_number("3.1.1、投标承诺书")