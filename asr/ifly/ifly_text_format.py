#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys


def ifly_text_format(inpath, outpath="output.txt"):
    """
    讯飞听见导出文本格式化
    """
    res = []
    with open(inpath, mode="r", encoding="utf-8") as f:
        lines = f.readlines()
        idx, size = 1, len(lines)
        while idx < size:
            if lines[idx].find("说话人") >= 0:
                speaker, begin_time = lines[idx].split(" ")
                context = ""
                idx += 1
                while idx < size and lines[idx].find("说话人") < 0:
                    context += lines[idx]
                    idx += 1
                begin_time, speaker,  context = begin_time.strip(), speaker.strip(), context.replace("\n", "").strip()
                res.append("{} {}：{}\n".format(begin_time, speaker, context))
                print("{} {}：{}".format(begin_time, speaker, context))
            else:
                idx += 1

    with open(outpath, mode="w", encoding="utf-8") as f:
        f.writelines(res)


def main():
    filepath = sys.argv[1]
    ifly_text_format(filepath)


if __name__ == "__main__":
    main()
