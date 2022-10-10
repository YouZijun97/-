import os

from preprocess import *
from output import *
from cut_line import *
from extract_entity import *

path = "./tagged_texts"
path1 = "./cut/"
#path = "D:/game/NER/example"
#path1 = "D:/game/NER/examplecut/"
files = os.listdir(path)


for file in files:
    print(file)
    if not os.path.isdir(file):
        f = open(path+"/"+file,'r',encoding="UTF-8",errors='ignore')
        iter_f = iter(f)
        fcut = open(path1+file,'w',encoding="UTF-8")
        for line in iter_f:  #每个line是文件中的每一行；可能包括多个句子，有可能就是一个名词短语
            if line=='\n':
                continue
            nline = remove_lines(line)  #判断是否不需要处理；这一步可以进一步增强，把一些句子描述型的句子给丢掉【待做】
            if nline == False:
                continue
            #print(3, nline)
            if (nline[-2:-1])=='。' or (nline[-2:-1])=='；' : #出现分号或者句号之后，说明有多个句子；把最后的标点符号去掉
                nline=nline[:-2]+nline[-1]
            if nline =='':
                continue

            frag_list = cut_lines(nline) #返回一个列表；按照关键字进行切分；在cut_line中，按照句号进行了切分
            #print(line)
            if frag_list == False:
                #print(frag_list)
                continue
            entity_list = entity_extract(line,frag_list) #line是原始句子，要作为数据来源保存；line_list是切分之后的结果
            fcut.write(entity_list + "\n")

