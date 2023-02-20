import linzhutil
import os
import re

file_list = linzhutil.getFileListFromPattern('./', '*.srt')

LANGUAGE = 1  # 1: European, 2: Chinese/Japanese/Korean/etc.
TWO_LINE_MODE = False
KEEP_LINE = 1
SPLIT_CHAR = " " if LANGUAGE == 1 else "。"

if __name__ == '__main__':

    line_index_pattern = re.compile(r'^\d+\n')
    for file in file_list:
        with open(file, 'r', encoding='utf-8-sig') as raw_file:
            text = raw_file.readlines()
        with open(os.path.splitext(file)[0] + '.txt', 'w') as new_file:
            index = 0
            while index < len(text):
                if TWO_LINE_MODE:
                    if line_index_pattern.match(text[index]):
                        index += 2
                        for i in range(KEEP_LINE):
                            new_file.write(text[index][:-1] + SPLIT_CHAR)
                            print(text[index], end='')
                            index += 1
                        continue
                    index += 1
                else:
                    if line_index_pattern.match(text[index]):
                        index += 2
                        new_file.write(text[index][:-1] + SPLIT_CHAR)
                        print(text[index], end='')
                    index += 1
