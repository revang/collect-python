#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
讯飞-语音转写 接口调用流程 参考文档: https://www.xfyun.cn/doc/asr/lfasr/API.html#%E6%8E%A5%E5%8F%A3%E8%B0%83%E7%94%A8%E6%B5%81%E7%A8%8B
    1. 预处理 prepare
    2. 文件分片上传 upload
    3. 合并文件 merge
    4. 查询进度处理 get_progress
    5. 获取结果 get_result
"""

import json
import os
import sys
import time
import math
import requests
import hashlib
import hmac
import base64


class SpeectToTextApi(object):
    def __init__(self, appid, secret_key, upload_file_path):
        self.appid = appid
        self.secret_key = secret_key
        self.upload_file_path = upload_file_path
        self.file_piece_sice = 10485760  # 文件分片大小10M

    def get_params(self, apiname, taskid=None, sliceid=None):
        ts = str(int(time.time()))  # 当前时间时间戳
        # 哈希算法 通过一个函数，把任意长度的数据转换为一个长度固定的数据串（通常用16进制的字符串表示）
        md5 = hashlib.md5()
        md5.update((self.appid + ts).encode('utf-8'))
        digest = md5.hexdigest()
        digest = bytes(digest, encoding='utf-8')

        # 通过哈希算法，我们可以验证一段数据是否有效，方法就是对比该数据的哈希值，例如，判断用户口令是否正确，我们用保存在数据库中的password_md5对比计算md5(password)的结果，如果一致，用户输入的口令就是正确的。
        signa = hmac.new(self.secret_key.encode('utf-8'), digest, hashlib.sha1).digest()  # 以secret_key为key, 上面的digest为msg， 使用hashlib.sha1加密结果为signa
        signa = base64.b64encode(signa)
        signa = str(signa, 'utf-8')

        file_size = os.path.getsize(self.upload_file_path)
        file_name = os.path.basename(self.upload_file_path)

        param_dict = {}
        if apiname == "api_prepare":
            slice_num = math.ceil(file_size/self.file_piece_sice)
            param_dict['app_id'] = self.appid
            param_dict['ts'] = ts
            param_dict['signa'] = signa
            param_dict['file_len'] = str(file_size)
            param_dict['file_name'] = file_name
            param_dict['slice_num'] = str(slice_num)
        elif apiname == "api_upload":
            param_dict['app_id'] = self.appid
            param_dict['ts'] = ts
            param_dict['signa'] = signa
            param_dict['task_id'] = taskid
            param_dict['slice_id'] = sliceid
        elif apiname == "api_merge":
            param_dict['app_id'] = self.appid
            param_dict['ts'] = ts
            param_dict['signa'] = signa
            param_dict['task_id'] = taskid
            param_dict['file_name'] = file_name
        elif apiname == "api_get_progress" or apiname == "api_get_result":
            param_dict['app_id'] = self.appid
            param_dict['ts'] = ts
            param_dict['signa'] = signa
            param_dict['task_id'] = taskid
        return param_dict

    def prepare_request(self):
        """ 预处理 """
        res = requests.post("http://raasr.xfyun.cn/api/prepare", data=self.get_params("api_prepare"))
        res = json.loads(res.text)
        print("prepare: {}...".format(str(res)[:100]))
        return res

    def upload_request(self, taskid):
        """ 文件分片上传 """
        sig = SliceIdGenerator()
        with open(self.upload_file_path, 'rb') as f:
            while True:
                content = f.read(self.file_piece_sice)
                if len(content) == 0:
                    break
                params = self.get_params("api_upload", taskid=taskid, sliceid=sig.getNextSliceId())
                files = {"filename": params["slice_id"], "content": content}
                res = requests.post("http://raasr.xfyun.cn/api/upload", data=params, files=files)
                print("upload: {}...".format(str(res.text)[:100]))

    def merge_request(self, taskid):
        """ 合并文件 """
        res = requests.post("http://raasr.xfyun.cn/api/merge", data=self.get_params("api_merge", taskid=taskid))
        print("merge: {}...".format(str(res.text)[:100]))

    def get_progress_request(self, taskid):
        """ 查询进度处理 """
        while True:
            res = requests.post("http://raasr.xfyun.cn/api/getProgress", data=self.get_params("api_get_progress", taskid=taskid))
            res = json.loads(res.text)
            res = json.loads(res["data"])
            print("get progress: {}...".format(str(res)[:100]))
            if res["status"] == 9:
                break
            else:
                time.sleep(3)

    def get_result_request(self, taskid):
        """ 获取结果 """
        res = requests.post("http://raasr.xfyun.cn/api/getResult", data=self.get_params("api_get_result", taskid=taskid))
        res = json.loads(res.text)
        dic = json.loads(res["data"])
        print("get result content")
        for item in dic:
            print("{}-{} {}: {}".format(time.strftime("%H:%M:%S", time.gmtime(int(int(item["bg"])/1000))), time.strftime("%H:%M:%S", time.gmtime(int(int(item["ed"])/1000))), "说话人"+str(int(item["speaker"])+1), item["onebest"]))


class SliceIdGenerator:
    """slice id生成器"""

    def __init__(self):
        self.__ch = 'aaaaaaaaa`'

    def getNextSliceId(self):
        ch = self.__ch
        j = len(ch) - 1
        while j >= 0:
            cj = ch[j]
            if cj != 'z':
                ch = ch[:j] + chr(ord(cj) + 1) + ch[j + 1:]
                break
            else:
                ch = ch[:j] + 'a' + ch[j + 1:]
                j = j - 1
        self.__ch = ch
        return self.__ch


def main():
    print(sys.argv[1])
    api = SpeectToTextApi("[AppId]", "[SecretKey]", sys.argv[1])  # 需要修改AppId, SecretKey
    taskid = api.prepare_request()["data"]
    api.upload_request(taskid)
    api.merge_request(taskid)
    api.get_progress_request(taskid)
    api.get_result_request(taskid)


if __name__ == "__main__":
    main()
