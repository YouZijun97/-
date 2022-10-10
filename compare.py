import json
import os
import acc_func
path1 = "./examplejson"  # 输出的数据
path2 = "./truejson"  # 人工标注的数据
files = os.listdir(path1)
for file in files:
    print("file", file)
    if not os.path.isdir(file):

        name1 = [] # 记录输出的实体归一化名称
        description1 = [] # 描述
        relation1 = [] # 关系
        f = open(path1+"/"+file,'r',encoding="UTF-8",errors='ignore')

        mydict = json.load(f)
        for i in mydict.keys():  # 数字
            j = mydict[i]["结果"]
            # print("j",j)
            name_list = []
            description_list = []
            relation1_list = []
            for k in j.keys(): # 实体i

                l = j[k]
                x = l.get("实体归一化名称")
                name_list.append(x)
                y = l.get("实体描述")
                description_list.append(y)
                z = l.get("实体关系")
                relation1_list.append(z)
                # for n in l.keys():  # 实体描述、实体归一化、实体源文件来源、实体关系
                #     print("n",n)
            name1.append(name_list)
            description1.append(description_list)
            relation1.append(relation1_list)
        # print("name1",name1)
        # print(description1)
        # print(relation1)
        name2 = []  # 记录人工标注的实体归一化名称
        description2 = [] # 描述
        relation2 = [] # 关系
        f = open(path2 + "/" + file, 'r', encoding="UTF-8", errors='ignore')
        mydict = json.load(f)
        for i in mydict.keys():  # 数字
            j = mydict[i]["结果"]
            # print("j",j)
            name_list = []
            description_list = []
            relation1_list = []
            for k in j.keys():  # 实体i

                l = j[k]
                x = l.get("实体归一化名称")
                name_list.append(x)
                y = l.get("实体描述")
                description_list.append(y)
                z = l.get("实体关系")
                relation1_list.append(z)
                # for n in l.keys():  # 实体描述、实体归一化、实体源文件来源、实体关系
                #     print("n",n)
            name2.append(name_list)
            description2.append(description_list)
            relation2.append(relation1_list)
        # print("name2",name2)
        # print(description2)
        # print(relation2)
    print("file", file)
    #判断实体归一化的正确率
    x = acc_func.edit_dist_acc(name1, name2)
    print("该文件实体归一化的正确率为：", x)
    # 判断实体关系的正确率
    z = acc_func.Accuracy(relation1, relation2)
    print("该文件实体关系的正确率为：", z)
