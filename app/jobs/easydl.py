import base64
from io import BytesIO
import json
import requests
from aip import AipImageClassify


# 数据集管理
class DSManger:
    headers = {'Content-Type': 'application/json'}
    host = {
        'ds_add': 'https://aip.baidubce.com/rpc/2.0/easydl/dataset/create',
        'ds_list': 'https://aip.baidubce.com/rpc/2.0/easydl/dataset/list',
        'tag_list': 'https://aip.baidubce.com/rpc/2.0/easydl/label/list',
        'tag_add': 'https://aip.baidubce.com/rpc/2.0/easydl/dataset/addentity',
        'ds_delete': 'https://aip.baidubce.com/rpc/2.0/easydl/dataset/delete',
        'tag_delete': 'https://aip.baidubce.com/rpc/2.0/easydl/label/delete'
    }
    type = 'IMAGE_CLASSIFICATION'

    # 获取access_token
    # client_id 为官网获取的AK， client_secret 为官网获取的SK
    def get_access_token(self, client_id, client_secret):
        acc_host = 'https://aip.baidubce.com/oauth/2.0/token'
        params = {'grant_type': 'client_credentials', 'client_id': client_id, 'client_secret': client_secret}
        response = requests.get(acc_host, headers=self.headers, params=params)
        content = json.loads(response.text)
        if 'error' in content:
            print('获取access_token失败')
            return
        access_token = content['access_token']
        self.params = {'access_token': access_token}

    # 创建数据集
    def ds_add(self, dataset_name):
        data = json.dumps({'type': self.type, 'dataset_name': dataset_name}, ensure_ascii=True)
        response = requests.post(self.host['ds_add'], data=data, headers=self.headers, params=self.params)
        result = json.loads(response.text)
        if 'error_code' in result:
            print('创建数据集失败')
            return
        return result['dataset_id']  # 返回数据集id

    # 数据集列表
    def ds_list(self):
        data = json.dumps({'type': 'IMAGE_CLASSIFICATION'})
        response = requests.post(self.host['ds_list'], data=data, params=self.params, headers=self.headers)
        result = json.loads(response.text)
        if 'error_code' in result:
            print('获取数据集列表失败')
            return
        return result['results']  # 返回数据集列表

    # 删除数据集
    def ds_delete(self, dataset_id):
        data = json.dumps({'type': self.type, 'dataset_id': dataset_id})
        response = requests.post(self.host['ds_delete'], data=data, params=self.params, headers=self.headers)
        result = json.loads(response.text)
        if 'error_code' in result:
            print('删除数据集失败')
            return

    # 添加分类数据
    # appendLabel 确定添加标签/分类的行为：追加(true)、替换(false)。默认为追加(true)。
    # entity_content 图片base64编码，entity_name 文件名
    # labels 标签/分类数据  object  {label_name 标签/分类名称 }
    def tag_add(self, dataset_id, entity_content, entity_name, labels, appendLabel=True):
        data = json.dumps({
            'type': self.type,
            'dataset_id': dataset_id,
            'appendLabel': appendLabel,
            'entity_content': entity_content,
            'entity_name': entity_name,
            'labels': labels,
        })
        response = requests.post(self.host['tag_add'], data=data, params=self.params, headers=self.headers)
        result = json.loads(response.text)
        if 'error_code' in result:
            print('添加分类数据失败')
            return

    # 分类列表
    def tag_list(self, dataset_id):
        data = json.dumps({'type': self.type, 'dataset_id': dataset_id})
        response = requests.post(self.host['tag_list'], data=data, params=self.params, headers=self.headers)
        result = json.loads(response.text)
        if 'error_code' in result:
            print('查看分类列表失败')
            return
        return result['results']

    # 删除分类
    def tag_delete(self, dataset_id, label_name):
        data = json.dumps({'type': self.type, 'dataset_id': dataset_id, 'label_name': label_name})
        response = requests.post(self.host['tag_delete'], data=data, params=self.params, headers=self.headers)
        result = json.loads(response.text)
        if 'error_code' in result:
            print('删除分类失败')
            return


# ds.ds_add('手机')
# ds.ds_list()
# ds.tag_list(21487)
# ds.tag_add(21487, entity_content=img_data, entity_name='111', labels=[{'label_name': 'iphone'}])
# ds.tag_delete(21487,'iphone')
# 模型发布后校验
def check():
    ds = DSManger()
    ds.get_access_token('2GzP6I50zxHOqQ66zyKdRMT3', '5VL8eL2IFKH61CxjSv55CvCWGdcFogr0')
    params = ds.params
    headers = ds.headers
    host = 'https://aip.baidubce.com/rpc/2.0/ai_custom/v1/classification/' + 'category'
    img_response = requests.get(
        'http://laisheji-web.oss-cn-shenzhen.aliyuncs.com/default/20180612/3a3476e67ab5c9c5232985d39620a08cwTtXCW2rSw.jpg')
    img_data = base64.b64encode(BytesIO(img_response.content).read()).decode('utf-8')
    data = json.dumps({'image': img_data})  # top_num 返回分类数量，默认为6个
    response = requests.post(host, params=params, data=data, headers=headers)
    result = json.loads(response.text)
    if 'error_code' in result:
        print('模型检验失败')
        return
    return result['results']


# 标签识别
def tag_recognition(url, APP_ID, API_KEY, SECRET_KEY):
    APP_ID = APP_ID
    API_KEY = API_KEY
    SECRET_KEY = SECRET_KEY
    client = AipImageClassify(APP_ID, API_KEY, SECRET_KEY)
    img_response = requests.get(url)
    response = client.advancedGeneral(img_response.content)
    return response


result = tag_recognition('http://s4.taihuoniao.com/opalus/image/181213/5c127210ce156a5ece3d9508', '15180965',
                         'Gjw3RzhDcMSS8RESUEiVNWkH', 'pZVtDe5Z74cA2ropdsI3s3rGMrFmXH9N')
print(result)
