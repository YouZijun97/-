import json
import os


class json_saver:
    def __init__(self, input_dir='./', out_dir='./out_dir/', encoding='utf-8'):
        self.input_dir = input_dir
        self.out_dir = out_dir
        self.encoding = encoding

    def save(self, file):
        data = dict()
        cur_case = dict()
        idx = -1
        path = self.input_dir + file
        with open(path, 'r', encoding=self.encoding) as f:
            lines = f.read().split('\n')
            n = len(lines)
            i = 0
            while i < n:
                line = lines[i]
                i += 1
                if len(line) > 1:
                    if line[2] == '源':
                        cur_case = dict()
                        cur_case['实体源文件来源'] = line.strip().split('：')[-1]
                        cur_case['结果'] = {}
                        entity_idx = -1
                    elif line[2] == '描' or line[2] == '归' or line[2] == '关' or line[2] == '文':
                        cur_case, entity_idx = self.gen_entity_data(cur_case, entity_idx, line)
                        if line[2] == '关':
                            idx += 1
                            data[idx] = cur_case
                            cur_case = dict()
                    else:
                        line = line.strip()
                        if line[2] == '描' or line[2] == '归' or line[2] == '关' or line[2] == '文':
                            cur_case, entity_idx = self.gen_entity_data(cur_case, entity_idx, line)
                            if i >= len(lines) or (len(lines[i + 1]) > 0 and lines[i + 1][0] == '实'):
                                idx += 1
                                data[idx] = cur_case
                                cur_case = dict()
                        elif line[2] == '源':
                            entity = '实体' + str(entity_idx)
                            cur_case['结果'][entity]['实体源文件来源'] = line.strip().split('：')[-1]

        out_path = self.out_dir + file[:-3] + 'json'
        data_jsom = json.dumps(data, ensure_ascii=False, indent=8)
        with open(out_path, 'w', encoding=self.encoding) as f:
            f.write(data_jsom)

    def gen_entity_data(self, cur_case, entity_idx, line):
        entity = '实体' + str(entity_idx)
        if line[2] == '描':
            entity_idx += 1
            entity = '实体' + str(entity_idx)
            cur_case['结果'][entity] = dict()
            cur_case['结果'][entity]['实体描述'] = line.strip().split('：')[-1]
        elif line[2] == '归':
            cur_case['结果'][entity]['实体归一化名称'] = line.strip().split('：')[-1]
        elif line[2] == '文':
            cur_case['结果'][entity]['实体文件来源'] = line.strip().split('：')[-1]
        elif line[2] == '关':
            cur_case['结果'][entity]['实体源文件来源'] = cur_case['实体源文件来源']
            cur_case['结果'][entity]['实体关系'] = line.strip().split('：')[-1]
        return cur_case, entity_idx

    def save_json(self):
        if not os.path.exists(self.out_dir):
            os.mkdir(self.out_dir)
        for file in os.listdir(self.input_dir):
            if file[-3:] != 'txt':
                continue
            self.save(file)


if __name__ == '__main__':
    input_dir = './cut/'
    out_dir = './out_dir/'
    json_saver = json_saver(input_dir=input_dir, out_dir=out_dir)
    json_saver.save_json()
