from preprocess import *

from ddparser import DDParser
ddp = DDParser(use_pos=True)

def is_Chinese(word):
    for ch in word:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

def check_paren(line): #
    #print(line)
    index_right = line.find("）")
    index_left = line.find("（")
    #print(index_right,index_left)
    if index_right == -1: #右侧没有发现右括号，说明不在括号内；返回True意味着这个关键字应该被记录；否则忽略
        return True
    else: #存在右括号，检测左括号
        if index_left != -1 and (index_right > index_left): #如果没有左括号，肯定在括号内
            return True
        else:
            return False


def find_all_keywords(line): # 找到所有括号外的连接词并返回索引值；括号内的暂不处理
    """
    :param line: 某一行句子
    :return: 如果出现keyword，返回出现的keyword的索引列表和对应的keyword列表，否则返回-1，-1
    """
    keywords = ["、","和", "或", '/','及']
    index_list = []
    keyword_list = []
    #print("line to be checked: ", line)
    for keyword in keywords:

        #print(line)
        index = line.find(keyword)
        #print(index)
        while index != -1:   #每一个位置
            record = check_paren((line[index+1:])) #查询句子的后部，是否先找到右括号；为什么不用左部，因为find只能发现第一个;补充可以用rfind，找到最后一个位置

            if record:
                if keyword != "及":
                    index_list.append(index)
                    keyword_list.append(keyword)
                else:
                    if line[index-1]=="以":
                        index_list.append(index-1)
                        keyword_list.append("以及")
                    else:
                        index_list.append(index)
                        keyword_list.append(keyword)
            index = line.find(keyword,index+1)

    if len(index_list) > 0:
        index_list, keyword_list = (list(t) for t in zip(*sorted(zip(index_list, keyword_list))))
        return index_list, keyword_list
    else:
        return -1, -1

def check_entity(frag1,frag2):   #检查按照关键字切分的frag的最后一个重点词汇是不是名词，如果不是，那么就不要切分，仍然合起来；防止误切分；还有括号里仅有一个字的情况如（三）、（四）；http://的情况

    #print("frag1, frag2",frag1, frag2)
    if len(frag1) == 0: #http://的情况
        print("不满足切分条件:", frag1, frag2)
        return False

    #要能够处理“简历（加盖公章）、身份证复印件（加盖公章）”

    if frag1[-1] == '）':  #如果关键字前面是括号，那么不处理括号里的内容；如果全部内容本身就是括号，那么拿掉括号就是空了
        index = frag1.find('（')
        #frag = frag1[:index] #这个代码不好，很容易出问题
        frag1 = re.sub('（.*?）','',frag1)  #处理类似“咨询项目经理（必须为项目全职并常驻现场代表）的简历（加盖公章）” 必须要用惰性匹配
        print(frag1)

    if len(frag1)==0 or len(frag2)==0: #各种意外情况
        print("不满足切分条件:", frag1, frag2)
        return False  #如果只有括号，那么不处理；

    #if is_Chinese(frag1[-1])==False:
    #    return False

    if frag1[-1] == '，' or frag1[-1] == '等':
        frag1 = frag1[:-1]
    #print("what frag is:", frag)

    result1 = ddp.parse(frag1)
    result2 = ddp.parse(frag2)

    if (result1[0]['postag'][-1] != 'n' and result1[0]['postag'][-1] != 'nz') or result2[0]['word'][0] == '格式' or (len(result2[0])==1 and result2[0]['postag'][0]=='vn'):
        print("不满足切分条件:",frag1,frag2)
        return False
    else:
        return True

def remove_all_elements(list,element): #移除列表中的某一个元素

    while(element in list):
        list.remove(element)
    if len(list)>0: #考虑到list被删除空了的情况
        return list
    else:
        return -1

def check_all_entities(sentence): #思路是判断每个小分片的最后一个词是否是名词；如果是名词，则认为可能是实体，需要切分，否则不需要切分，则删除此index
    index_list, keyword_list = find_all_keywords(sentence)
    #original_index_list,original_keyword_list = find_all_keywords(sentence)  #如果直接把index_list复制给original，那么它们两个指向的是同一个List；所以是白费力气
    if index_list == -1:
        original_index_list = -1
        original_keyword_list = -1
    else:
        # 存在连词,两个连词会将句子分成三段，所以添加最后的索引，并重复最后一个连词，方便调用
        index_list.append(len(sentence))
        keyword_list.append(keyword_list[-1])
        original_index_list = index_list.copy()
        original_keyword_list = keyword_list.copy()

    #新增两个变量，用来存放当前片段和下一片段的位置

    if index_list != -1:  # nline出现了keyword
        # 对出现keyword的句子进行分段处理
        # print(index_list)
        for i in range(len(index_list)-1):  # 用于处理每一个小分片
            index1 = original_index_list[i]
            index2 = original_index_list[i+1]
            key2_len = len(original_keyword_list[i])

            # print("i is:",i)
            if i > 0:
                index0 = original_index_list[i - 1]
                key1_len = len(original_keyword_list[i-1])
                #result = check_entity( sentence[original_index_list[i - 1] + len(original_keyword_list[i]):original_index_list[i]])
                result = check_entity(sentence[index0 + key1_len:index1],sentence[index1+key2_len:index2])  #传递关键字前后两个片段，判断效果更好
                if result == False:
                    index_list[i] = -1
                    keyword_list[i] = -1

            else:
                # 第一个分段是从0位置一直到index_list[i];i==0
                #result = check_entity(sentence[0: original_index_list[i]],sentence[original_index_list[i]+ len(original_keyword_list[i]):original_index_list[i+1]]) #参数太长了
                result = check_entity(sentence[0 : index1], sentence[index1 + key2_len:index2])
                if result == False:
                    index_list[i] = -1
                    keyword_list[i] = -1

        index_list = remove_all_elements(index_list, -1)
        keyword_list = remove_all_elements(keyword_list, -1)
        # print("index_list:",index_list)
    return index_list, keyword_list


def cut_frag(sentence): #基于找到的关键字，将句子切分成片段
    flag = 1
    #index_list, keyword_list = find_all_keywords(sentence)
    print("sentence is:",sentence)
    sentence = pre_check_entity(sentence) #进行简单处理，如果有修饰性的名词，则对句子进行扩展 如把 商务和技术偏差表，变换成 商务偏差表和技术偏差表
    index_list, keyword_list = check_all_entities(sentence)
    #check_all_entities(sentence)
    frag = []
    frag_list = []
    #print(sentence)
    if index_list != -1:  # nline出现了keyword
        flag = 0
        # 对出现keyword的句子进行分段处理
        for i in range(len(index_list)):
            frag = []
            #print("is i:",i)
            if i > 0:
                frag.append(sentence[index_list[i - 1]+len(keyword_list[i]):index_list[i]])
                frag.append(keyword_list[i])
                frag_list.append(frag)

            else:
                # 第一个分段是从0位置一直到index_list[i]
                frag.append(sentence[0: index_list[i]])
                frag.append(keyword_list[i])
                frag_list.append(frag)

        #frag = []

        #print("last i :",i , "last frag:",sentence[index_list[i] + len(keyword_list[i]):] )
        #frag.append(sentence[index_list[i] + len(keyword_list[i]):])
        #frag.append(keyword_list[len(index_list) - 1] ) #最后一项
        #frag_list.append(frag)

    if flag == 1:  # 所有的关键字都不存在，不存在分段问题
        frag.append(sentence)
        frag.append('')
        frag_list.append(frag)
    #print(frag_list)
    return frag_list


def cut_lines(line):
    # 首先对句子按照句号进行切分；目前看起来太长的句子，基本都不需要处理；暂时先按照这个思路处理
    # 单句中比较复杂的情况是句子中包括连接词，也即包括多个实体，需要进行正确的切分和提取
    #print(line)
    if line =='\n':
        return False
    if line.endswith('\n') or line.endswith('。'):
        #print(line)
        sentence_list = line[:-1].split('。', -1)
    else:
        sentence_list = line.split('。', -1)
    #print(sentence_list)

    while '' in sentence_list: #循环删除''
        sentence_list.remove('')
    for sentence in sentence_list:
        frag_list = cut_frag(sentence)
        #print(frag_list)
    return frag_list


def pre_check_entity(sentence): #主要用于对句子片段进行修改，扩展实体词或者修饰语
    ddp_list = ddp.parse(sentence)
    ddpzero = ddp_list[0]
    #print(ddp_list)
    try:
        count_list = get_index(ddpzero['postag'], 'c') #可能有多个连接词，每一个都需要处理
    except ValueError:
        nline = sentence

    #print("old count list:",count_list)

    cl = get_index(ddpzero['word'],'/')  # '/'也是连接词
    if cl != []:
        count_list += cl
    #print("new count list:",count_list)

    tline = ''  # temporary line
    if (count_list):  #对每个连接词进行处理
        #print("count list:", count_list)
        x = 0;
        z = len(ddpzero['word'])

        for i in range(len(count_list)): #
            if count_list[i] == 0 or count_list[i]== z-1: #出现“若应征人” 中把 “若”当成 'c'的情况，而且位于句首，报错；如果出现count_list中0的情况，直接不处理 #一种特殊情况 http://xwqy.gsxt.gov.cn/  导致j+2会溢出
                continue
            y = count_list[i]
            j = count_list[i] - 1  #找出连接词前的一个词，判断它是不是单独的实体；可以处理如“质量控制和质量保证方案”，将方案扩展到质量控制

            #print("i is",i,ddpzero['word'][j+2],ddpzero['head'][j])
            #print(ddpzero['head'][ddpzero['head'][j]-1])
            if ddpzero['deprel'][j] == 'ATT' and (ddpzero['deprel'][j + 2] == 'COO' or ddpzero['deprel'][j + 2] == 'ATT') and (ddpzero['deprel'][ddpzero['head'][j] - 1] == 'HED' or ddpzero['deprel'][ddpzero['head'][ddpzero['head'][j]-1]-1]=='HED'): #如果j是修饰词，那么对句子进行扩展；
            #print(ddpzero['head'][i] - 1,ddpzero['deprel'][ddpzero['head'][i] - 1])
            #if ddpzero['deprel'][j] == 'ATT' and ddpzero['deprel'][j + 2] == 'COO' and ddpzero['deprel'][ddpzero['head'][j] - 1] == 'HED':
                print("满足条件的：", sentence)
                for k in range(x, count_list[i]):
                    tline += ddpzero['word'][k]
                #tline = sentence[0:j+2]
                #print("j is",j,"first part:",tline)

                for w in range(j + 3, ddpzero['head'].index(0)+1): #把实体部分拷贝一份，从COO拷贝到HED
                    tline += ddpzero['word'][w]
                    #print(tline)
                tline += ddpzero['word'][j+1]  #把连接词拷贝上

                #判断j之前有没有修饰，如果有的话，拷贝到后面的实体;思路就是找到连接词前的实体的修饰词
                for k in range(0,j):
                    #print(ddpzero['deprel'][k],ddpzero['head'][k])
                    if ddpzero['deprel'][k] == "ATT" and ddpzero['head'][k]==j+1: #j+1是因为HED总是0，占了一个数字
                        #print("word is:",ddpzero['word'][k])
                        tline += ddpzero['word'][k]
                    #print(tline)

                for k in range(j + 2, len(ddpzero['word'])):  # 把剩下的句子原封不动地拷贝一遍
                    tline += ddpzero['word'][k]

                #print(tline) #形成新的句子
    if tline != '':
        print("new sentence is: ",tline)
        tline = tline
    else:
        tline = sentence
    return tline

    #接下来考虑处理描述扩展，如“经营场地租赁合同/自有产权证”