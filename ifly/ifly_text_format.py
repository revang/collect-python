#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re


def ifly_text_format(filepath):
    """
    讯飞听见导出文本格式化
    """
    with open(filepath, mode="r", encoding="utf-8") as f:
        text = f.read()
        items = re.findall("说话人[^(说话人)]*", text, flags=re.M)
        for item in items:
            block1, block2 = item.split("\n", maxsplit=1)  # 字符串分割成两部分
            speaker, begin_time = block1.split(" ")
            content = block2.replace("\n", "")
            print("{} {}: {}".format(begin_time, speaker, content))


def main():
    filepath = sys.argv[1]
    ifly_text_format(filepath)


if __name__ == "__main__":
    main()
