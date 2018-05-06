#encoding: utf-8
import sys
import json
from datetime import datetime
from scrapy import DetectionInfoScrapy as DIS
from crawler import DectectionInfo, FieldsInfoMapper, DBSession


reload(sys)
sys.setdefaultencoding('utf-8')
# url = 'http://www.ngstc.cn/MC/'
# params = {
#     'M': 'C',
#     'SN': 'P1801017626',
#     'QO': '4363'
# }

url = 'http://so.gdtc.cc:88/Certificate/DiamondGrading.aspx'
params = {
    'SampleNumber': '66170118083'       # 证书编号
}

if __name__ == '__main__':

    dis = DIS(url=url, params=params)
    detection_infos = dis.scrapy()

    # 创建session对象:
    session = DBSession()


    dectectionInfos = session.query(DectectionInfo)

    for dectectionInfo in dectectionInfos:


        print dectectionInfo.__dict__

    dict = {}
    dict.update(dectectionInfo.__dict__)
    print dict

    sys.exit(0)

    dectection_info = {}

    for detection_info in detection_infos:

        # 取得该检测项目在表中对应的字段名
        rec = session.query(FieldsInfoMapper).filter(FieldsInfoMapper.item_name==detection_info["item_name"],
                                         FieldsInfoMapper.source_url==url).one()

        dectection_info[rec.field_name] = detection_info["item_content"]

    # DectectionInfo的来源链接字段
    dectection_info['source_url'] = url
    # DectectionInfo的参数字段
    dectection_info['url_para'] = '&'.join([k + '=' + v for k,v in params.iteritems()])
    #

    rec = session.query(DectectionInfo).filter(DectectionInfo.detection_number==dectection_info['detection_number'],
                                               DectectionInfo.source_url==url).all()
    # 判断库里有无此证书编号的记录，不存在则插入，存在则更新。
    if len(rec) == 0:
        # 插入该记录
        session.add(DectectionInfo(**dectection_info))
    else:
        # 更新时间
        dectection_info['update_time'] = datetime.now()

        session.query(DectectionInfo).filter(DectectionInfo.detection_number == dectection_info['detection_number'],
                                             DectectionInfo.source_url == url).update(dectection_info)

    # 提交即保存到数据库:
    session.commit()
    # 关闭session:
    session.close()
