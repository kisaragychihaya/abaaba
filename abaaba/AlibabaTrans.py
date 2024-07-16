import os
import sys

from typing import List

from alibabacloud_alimt20181012.client import Client as alimt20181012Client
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_alimt20181012 import models as alimt_20181012_models
from alibabacloud_tea_util import models as util_models
from alibabacloud_tea_util.client import Client as UtilClient

class AliTrans:
    def __init__(self):
        pass

    @staticmethod
    def create_client() -> alimt20181012Client:
        """
        使用AK&SK初始化账号Client
        @return: Client
        @throws Exception
        """
        # 工程代码泄露可能会导致 AccessKey 泄露，并威胁账号下所有资源的安全性。以下代码示例仅供参考。
        # 建议使用更安全的 STS 方式，更多鉴权访问方式请参见：https://help.aliyun.com/document_detail/378659.html。
        config = open_api_models.Config(
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_ID。,
            access_key_id=os.environ['AK_ABA'],
            # 必填，请确保代码运行环境设置了环境变量 ALIBABA_CLOUD_ACCESS_KEY_SECRET。,
            access_key_secret=os.environ['SK_ABA']
        )
        # Endpoint 请参考 https://api.aliyun.com/product/alimt
        config.endpoint = f'mt.cn-hangzhou.aliyuncs.com'
        return alimt20181012Client(config)

    @staticmethod
    def main(
        txt,sl="zh",tl="en"
    ) -> None:
        client = AliTrans.create_client()
        translate_general_request = alimt_20181012_models.TranslateGeneralRequest(
            format_type='text',
            source_language=sl,
            target_language=tl,
            source_text=txt,
            scene='general'
        )
        runtime = util_models.RuntimeOptions()
            # 复制代码运行请自行打印 API 的返回值
        resp=client.translate_general_with_options(translate_general_request, runtime).body
        if resp.code=="200":
            return resp.data.translated