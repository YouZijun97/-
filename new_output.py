import re


def norm_output(original, name, description, relation="null"):
    """
    :param original: 实体源文件来源
    :param name: 实体归一化名称
    :param description: 实体描述(list)
    :param relation: 实体关系
    :return:
    """
    str = ""
    str += "实体源文件来源：" + original + "\n"

    str += "实体描述："
    if description == []:
        description = ["NULL"]
    for i in range(len(description)):
        str += description[i]
        if i != (len(description) - 1):
            str += "、"
        else:
            str += "\n"
    str += "实体归一化名称：" + name + "\n"
    str += "实体关系：" + relation + "\n"
    return str

def source_output(original):
    str = "实体源文件来源：" + original + "\n"
    return str

def sub_output(description, name, source, relation,space="    "):
    """
        :param description: 实体描述(list)
        :param name: 实体归一化名称
        :param original: 实体源文件来源
        :param relation: 实体关系
        :return:
        """
    #print("description ",description)
    #space = "    "
    str = ""
    str += space + "实体描述："
    if description == []:
        description = ["NULL"]
    print(description)
    for i in range(len(description)):
        str += description[i]
        if i != (len(description) - 1):
            str += "、"
        else:
            str += "\n"

    str += space + "实体归一化名称：" + name + "\n"
    str += space + "实体文件来源：" + source + "\n"

    if relation == "":
        relation = "NULL"
    str += space + "实体关系：" + relation + "\n"

    return str