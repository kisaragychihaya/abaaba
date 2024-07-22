import requests
import json
import os
class BaiduTrans:
    def __init__(self):
        self.__token = None
        self.__sk=os.environ['sK_ABA']
        self.__ak=os.environ['aK_ABA']
        self.__gen_token()
        self._url="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro"

    def __gen_token(self):
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {"grant_type": "client_credentials", "client_id": self.__ak, "client_secret": self.__sk}
        self.__token= str(requests.post(url, params=params).json().get("access_token"))

    def main(self,txt,sl="zh",tl="en"):
        lang_table = {"zh": "中文", "en": "英文", "ja": "日文"}
        sl = lang_table[sl]
        tl = lang_table[tl]
        system = "你是一名语言翻译和交流协调员。我需要你的帮助进行语言翻译和交流。请提供语言翻译服务，并帮助我克服语言障碍。"+\
                  f"你的角色是促进不同语言之间的有效沟通，并确保准确理解和传达信息。你不应该说出翻译结果之外的任何语句,请勿扩写任何内容，请直接告诉我答案，如果遇到{sl}标点符号请翻译为{tl}标点，禁止说多余的话。"

        msg=[{
            "role": "user",  # 用户或功能角色
            "content": "请帮我翻译一下这段{from_lang}：{txt}\n到{to_lang}".format(from_lang=sl,txt=txt,to_lang=tl)
        }]

        _url = self._url+"?access_token=" +self.__token
        payload = json.dumps({"messages": msg,  "system": system,"temperature":0.5})
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.request("POST", _url, headers=headers, data=payload).json()
        return response['result']

class BaiduFreeTrans(BaiduTrans):
    def __init__(self):
        super().__init__()
        self._url="https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/ernie_speed"

class Baidu35Trans(BaiduTrans):
    def __init__(self):
        super().__init__()
        self._url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions"


