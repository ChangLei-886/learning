#encoding: utf-8
import requests
import copy
from bs4 import BeautifulSoup

class DetectionInfoScrapy:
    def __init__(self, url=None, params={}):
        self.url = url
        self.params = params

    def scrapy(self):

        # 红珠宝检测项目爬取
        if self.url == 'http://www.ngstc.cn/MC/':
            detection_infos = []
            detection_info = {'item_name': '', 'item_content': ''}
            res = requests.get(self.url, params=self.params)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')
            for child in soup.body.descendants:
                # 如果不是table标签则跳入下一个循环
                if child.name != 'table':
                    continue
                # 如果不是指定table则跳入下一个循环
                if ' '.join(child.attrs.get('class')) != 'w_100 f16 b-bor f-f-h':
                    continue
                # 循环table的子孙节点
                for td in child.descendants:
                    kv_flg = '1'
                    # 如果不是td标签则跳入下一个循环
                    if td.name != 'td':
                        continue

                    # 如果不是指定td则跳入下一个循环
                    if ' '.join(td.attrs.get('class')) != 't-left c6' and ' '.join(
                            td.attrs.get('class')) != 't-c c-blue':
                        continue

                    # 要爬取的key
                    if ' '.join(td.attrs['class']) == 't-left c6':
                        detection_info['item_name'] = td.string.strip().replace('\r\n', '')
                        kv_flg = '1'
                    # 要爬取的value
                    if ' '.join(td.attrs['class']) == 't-c c-blue':
                        detection_info['item_content'] = td.string.strip().replace('\r\n', '')
                        kv_flg = '2'

                    if kv_flg == '2':
                        detection_infos.append(copy.deepcopy(detection_info))

            return detection_infos

        # 钻石检测项目爬取
        if self.url == 'http://so.gdtc.cc:88/Certificate/DiamondGrading.aspx':
            detection_infos = []
            detection_info = {'item_name': '', 'item_content': ''}
            res = requests.get(self.url, params=self.params)
            res.encoding = 'utf-8'
            soup = BeautifulSoup(res.text, 'html.parser')

            for td in soup.body.descendants:
                # 判断是否指定td标签
                if td.name != 'td' or td.attrs.get('height'):
                    continue

                for tr in td.descendants:
                    # 如果不是table标签则跳入下一个循环
                    if tr.name != 'tr':
                        continue
                    # 如果不是指定table则跳入下一个循环
                    if 'mso-yfti-irow' not in tr.attrs.get('style'):
                        continue

                    kv_flg = '1'
                    for p in tr.descendants:
                        if p.name != 'p' or ' '.join(p.attrs.get('class')) != 'MsoNormal':
                            continue
                        # 要爬取的key
                        if p.b:
                            detection_info['item_name'] = p.text.strip().replace('\r\n', '').replace(' ', '').replace('\n', '')
                            kv_flg = '1'
                        # 要爬取的value
                        if not p.b:
                            detection_info['item_content'] = p.text.strip().replace('\r\n', '').replace(' ', '').replace('\n', '')
                            kv_flg = '2'

                        if kv_flg == '2':
                            detection_infos.append(copy.deepcopy(detection_info))

            return detection_infos




