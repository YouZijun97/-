from cut_line import *
from ddparser import DDParser
from new_output import *

ddp = DDParser(use_pos=True)

#实体提取：情况包括 frag_list只有1项；也有可能有多个项；每个项的情况可能包括：  1. 单个的名词短语；2. 单个的名词短语+描述型括号 3. 单个的名词短语+多关键字括号 4. 句子中多个括号
#处理思路：首先检查frag_list的长度，如果只有一项且没有括号或者括号里没有实体，那么line就是数据来源，一共生成四项；如果括号里有实体，那么继续分析
#其次，如果frag_list的长度大于1，那么line就是最外层的数据；每一项再进行如上的分析
#最后，对于多括号的情况，只处理最后一个括号，把其余括号的内容保持不变，也不提取；因为一般中间的括号前一个实体的同义词，没必要提取

def check_description(entity): #用来划分描述和实体；暂时先用de来判断，把接口准备好；后面再改进
    index = entity.find('的')
    print("index is", index)
    if index != -1:
        return entity[:index+1], entity[index+1:]
    else:
        return -1,-1


def parenthesis(line): #提取出括号内容；如果没有括号，返回0；如果有括号，返回
    # 改变思路，改成只提取最后一个括号的内容 中间的括号内容不处理；如果括号是空的，原封不动返回
    i = 0
    x = ''
    paren_frag_list = []
    #print("paren line is:",line)
    p1 = re.compile(r'（.*?）', re.S)
    description = re.findall(p1, line)  # 提取出括号内容；分为中文括号和英文括号
    #print("description is:",description)
    p2 = re.compile(r"\(.*?\)", re.S)
    description2 = re.findall(p2, line) #英文括号；暂时没用上
    length = len(description)
    str = ''
    if length > 0:
       str = description[-1][1:-1] #取最后一项，并去除括号
       if str == "":
           paren_frag_list = []  #需要考虑到括号中为空的情况
           return 0 #print("括号内的：",str)
       else:
           paren_frag_list += cut_frag(str) #此时的str是括号内的内容；括号内的内容可能很复杂，分为多个实体；也有可能是描述；如果能检查出来多个实体，那么要再调用切分
           #print(paren_frag_list)  如果有一个括号，那么r长度为1；如果2个括号，则长度为2；如果括号内容进一步进行了切分，那么列表元素本身为列表

       return paren_frag_list  #可能只有一项，可能有多项
    else:  #没有括号；
        return 0
    #return str


def single_frag(line,frag): #单个frag的检测，首先查看是否有括号；没有括号则是normal_output;有括号则继续区分括号中切分长度为一或为多的情况；
    print("line is",line)
    frag0 = frag[0]
    if line.endswith("\n")==True:
        line = line[:-1]
    x = ""
    y = "实体源文件来源：" + line + '\n' #用来处理括号中多个实体的情况

    #print("frag[0]",frag[0])
    r = parenthesis(frag[0]) #返回的是括号里的内容；如果有一个括号，那么r长度为1；如果2个括号，则长度为2；如果括号内容进一步进行了切分，那么列表元素本身为列表
    print("r is:",r)
    if r == 0:#没有括号，此时应该提取description【待做】
        description,entity = check_description(frag[0])
        if(entity == -1):
            entity = frag[0]
            description = []
        else:
            description = [description]
        x += norm_output(line, entity,description)
        return x
    else:  # 有括号，返回一个frag_list：依然要分两种情况，一种是长度为1的，有可能是描述；一种是长度>1的，有可能是实体
        #index = frag0.rfind('（') #index最右边的（的位置
        #print("index is",index)

        if (len(r) == 1): #括号中的内容只切分为了一项；需要检查一下 这是描述还是实体（好难；待做）；如果是描述，就生成描述；还有个问题是，多个括号实际上应该是多个描述，而不是单独输出
            result = ddp.parse(r[0][0])
            print(r,result)
            description = []
            if('v' in result[0]['postag']):
                description = [r[0][0]]
            #print(description)

            x += source_output(frag[0])
            source = remove_parenthesis(frag[0])
            x += sub_output(description,source,source,r[0][1])  #description是描述；frag[0]是source；r[k][0]是实体；r[k][1]是关系
            return x
        else:  # 括号内又有多个实体，首先要把数据来源写清楚，然后再一项项列出来
            #print("实体时:",line[0:line.find('（')])
            #先取出最后一对括号前的内容
            #index = line.find('（')
            description = []
            source = remove_parenthesis(frag[0])
            y += sub_output(description,source,source,'NULL',"    ")  #是否要加上括号前内容
            for i in range(len(r)):  #如果括号中有多个实体，那么应该首先列出数据来源；然后把多个实体分别打出来；
                #print(r[i])
                y += sub_output(description,r[i][0],r[i][0],'NULL',"     ") #输出括号内实体

        return y

def remove_parenthesis(line):
    index1 = line.rfind('（')
    index2 = line.rfind('）')
    newline = line[:index1]+line[index2+1:]
    print("newline:",newline)
    return newline

def multi_frag(frag,relation): #用于多个frag的情况，对每个frag进行处理；和上面的single有些不同；
    #这里的Line是每个frag的
    frag0 = frag
    print("frag is",frag)
    x = ""
    y = ""
    #print("frag[0]",frag[0])
    r = parenthesis(frag) #返回的是括号里的内容
    #print("括号内：",r)
    if r == 0:#没有括号
        description,entity = check_description(frag)

        if(entity == -1):
            entity = frag
            description = []
        else:
            description = [description]
        x += sub_output(description,entity,frag0,relation,"    ")
        return x
    else:  # 有括号，返回一个frag_list：依然要分两种情况，一种是长度为1的；一种是长度>1的
        #index = frag0.rfind('（')  # index最右边的（的位置
        if (len(r) == 1):  # 括号中的内容只切分为了一项；需要检查一下 这是描述还是实体（好难；待做）；如果是描述，就生成描述；还有个问题是，多个括号实际上应该是多个描述，而不是单独输出
            result = ddp.parse(r[0][0])
            print(r, result)
            description = []
            if ('v' in result[0]['postag']):
                description = [r[0][0]]
            # print(description)

            #x += source_output(frag)
            source = remove_parenthesis(frag0)
            x += sub_output(description, source, source, r[0][1])  # description是描述；frag[0]是source；r[k][0]是实体；r[k][1]是关系
            return x
        else:  # 括号内又有多个实体，首先要把数据来源写清楚，然后再一项项列出来
            # print("实体时:",line[0:line.find('（')])
            # 先取出最后一对括号前的内容
            # index = line.find('（')
            description = []
            source = remove_parenthesis(frag0)
            y += sub_output(description, source, source, 'NULL', "    ")  # 是否要加上括号前内容
            for i in range(len(r)):  # 如果括号中有多个实体，那么应该首先列出数据来源；然后把多个实体分别打出来；
                # print(r[i])
                y += sub_output(description, r[i][0], r[i][0], 'NULL', "     ")  # 输出括号内实体

        return y

def entity_extract(line,frag_list):  ##已经经过关键字切分；还要区分line_list的长度；如果长度为1，那么数据来源就是整个句子；否则的话，整个句子先写上，后面每个分片还得写出来数据来源
    # 如果有括号，提取出括号内容；括号内容有可能是实体、有可能是描述；单句考虑区分描述和实体；归一化怎么处理呢？
    x = ''
    #print(1,frag_list)
    if(len(frag_list)==1): #句子只有一项
        x += single_frag(line, frag_list[0])

    else: #切分之后的frag有多项，对每一项分别进行处理
        x += source_output(line)      #首先准备好来源
        for frag in frag_list:  #对每一个分片，检查
            x += multi_frag(frag[0],frag[1])

    return x



