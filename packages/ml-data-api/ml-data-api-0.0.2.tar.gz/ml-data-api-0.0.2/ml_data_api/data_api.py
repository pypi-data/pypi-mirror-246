
import datetime
import hashlib
import json
import requests
import pandas as pd

# def print_test(str):
#     print('----:{}'.format(str))

class DataApi(object):

    def __init__(self):
        # 测试环境自己手动重置下
        self.base_url = 'https://dataapi.susallwave.com/booya-api/'
        self.access_key = ''
        self.access_secret = ''

    def set_base_url(self, base_url):
        self.base_url = base_url

    def set_access_key(self, access_key):
        self.access_key = access_key

    def set_access_secret(self, access_secret):
        self.access_secret = access_secret

    def api_post(self, module: str, method: str, params: dict, return_obj='str'):
        """
        :param module:
        :param method:
        :param params:
        :param return_obj: str/df
        :return:
        """
        timestamp_num = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        access_signature = self.access_key + self.access_secret + timestamp_num
        smd5sign = hashlib.md5(access_signature.encode()).hexdigest()

        url = "{base_url}/{module}/{method}".format(module=module, method=method, base_url=self.base_url)
        # print(url)

        headers = {'accessKey': self.access_key,
                   'accessTimestamp': timestamp_num,
                   'accessSignature': smd5sign,
                   "content-type": "application/json;charset=UTF-8"}
        # print(headers)
        # print()
        # print(combine_params)

        response = requests.post(url, headers=headers, data=json.dumps(params))
        content_str = response.content.decode('utf-8')
        # print(content_str)
        if return_obj == 'df':
            content_dict = json.loads(content_str)
            if content_dict['code'] in ['0', '200']:
                if content_dict['message'] is not None and content_dict['message'] != 'success' and len(content_dict['message']) > 0:
                    print(content_dict['message'])
                return pd.DataFrame(content_dict['data'])
            else:
                raise Exception(content_dict['message'])
        # 默认返回str
        return content_str

