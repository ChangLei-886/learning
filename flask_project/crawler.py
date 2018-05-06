#encoding: utf-8
from sqlalchemy import Column, Integer, String, DateTime, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# 创建对象的基类:
Base = declarative_base()

# 定义检测内容表对象
class DectectionInfo(Base):
    # 表的名字:
    __tablename__ = 'detection_information'

    # 表的结构:
    # 自增ID
    id = Column(Integer, primary_key=True)
    # 检测/证书编号
    detection_number = Column(String(15), unique=True, index=True, nullable=False, default=' ')
    # 查询/识别码
    query_code = Column(String(10), index=True, nullable=False, default=' ')
    # 饰品名称
    jewelry_name = Column(String(50), nullable=False, default=' ')
    # 总质量
    totle_weight = Column(String(10), nullable=False, default=' ')
    # 钻石质量
    carat_weight = Column(String(10), nullable=False, default=' ')
    # 形状
    shape = Column(String(20), nullable=False, default=' ')
    # 颜色
    color = Column(String(10), nullable=False, default=' ')
    # 净度级别
    clarity = Column(String(10), nullable=False, default=' ')
    # 切工
    cut = Column(String(10), nullable=False, default=' ')
    # 镶嵌材料
    material = Column(String(50), nullable=False, default=' ')
    # 货号
    orna_no = Column(String(20), nullable=False, default=' ')
    # 放大检查
    magnification = Column(String(50), nullable=False, default=' ')
    # 贵金属检测
    precious_metal = Column(String(20), nullable=False, default=' ')
    # 检测依据
    test_basis = Column(String(100), nullable=False, default=' ')
    # 备注
    remarks = Column(String(200), nullable=False, default=' ')
    # 创建时间
    create_time = Column(DateTime, nullable=False, default=datetime.now())
    # 更新时间
    update_time = Column(DateTime, nullable=False, default=datetime.now)
    # 来源url
    source_url = Column(String(100), nullable=False, default=' ')
    # 参数
    url_para = Column(String(100), nullable=False, default=' ')

# 定义检测项目字段对应关系对象
class FieldsInfoMapper(Base):

    __tablename__ = 'fields_mapper_info'

    # 表的结构
    # 自增ID
    id = Column(Integer, primary_key=True)
    # 爬取的检测项目
    item_name = Column(String(100))
    # 爬取的检测项目对应的字段
    field_name = Column(String(50))
    # 检测项目显示的内容
    disply_name = Column(String(100))
    # 来源url
    source_url = Column(String(100))

# 初始化数据库连接:
engine = create_engine('mysql+mysqlconnector://root:!QAZ2wsx@localhost:3306/crawler')

# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)



