# KEYWORDS = ['存款', '公款', '结算账户', '专户', '存放', '存放银行', '存放定期', '存放资金',
#             '存放公款', '存放定点', '存放账户', '存放金融', '存放养老金',
#             '存放备用金', '存放保证金', '存放公积金', '代理银行', '开户银行',
#             '资金银行', '基本户', '一般户', '账户开户', '基本账户', '一般账户', '银行账户', '开立账户']
KEYWORDS = ['存款', '公款', '结算账户', '专户', '存放', '代理银行', '开户银行',
            '资金银行', '基本户', '一般户', '账户开户', '基本账户', '一般账户', '银行账户', '开立账户']
BLACK_LIST = ['反向竞价', '在线询价', '存放室', '存放楼', '存放堂',
              '纪念堂', '存放架', '存放柜', '废旧物资回收', '反向竞价', '骨灰', '公开出租']
MONGO_URL = 'localhost:17027'
# MONGO_URL = '120.193.61.37:17027'
MONGO_DB = 'czck'
MONGO_TABLE = 'czck'


SEARCH_LINK = 'http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?'
# NOTICE_LINK = 'http://manager.zjzfcg.gov.cn/cms/api/cors/getRemoteResults?'

# 绍兴市公共资源交易网-招标
SX_MAIN_ZB_LINK = 'http://www.sxztb.gov.cn:33660/sxweb/fzxjy/007001/MoreInfo.aspx?CategoryNum=007001'

# 绍兴市公共资源交易网-中标
SX_MAIN_ZB2_LINK = 'http://www.sxztb.gov.cn:33660/sxweb/fzxjy/007002/MoreInfo.aspx?CategoryNum=007002'


SX_MAIN_SEARCH_LINK = [('http://ggb.sx.gov.cn/col/col1518878/index.html',
                        '招标（交易）公告', 1518878),  # 非中心交易（公告代发）项目	> 招标（交易）公告
                       ('http://ggb.sx.gov.cn/col/col1518879/index.html',
                        '中标公示', 1518879),  # 非中心交易（公告代发）项目	> 中标公示
                       ('http://ggb.sx.gov.cn/col/col1518859/index.html',
                        '采购要素公示', 1518859),  # 政府采购	> 采购要素公示
                       ('http://ggb.sx.gov.cn/col/col1518860/index.html',
                        '采购公告', 1518860),  # 政府采购	> 采购公告
                       ('http://ggb.sx.gov.cn/col/col1518861/index.html',
                        '中标（成交）公告', 1518861),  # 政府采购	> 中标（成交）公告
                       ('http://ggb.sx.gov.cn/col/col1518862/index.html',
                        '终止（废标）公告', 1518862)]  # 政府采购	> 终止（废标）公告

SX_MAIN_DATA_PROXY = 'http://ggb.sx.gov.cn/module/jpage/dataproxy.jsp'


# 嘉兴市公共资源交易中心
JX_GGZY_MAIN_LINK = 'http://www.jxzbtb.cn'
JX_GGZY_SEARCH_LINK = 'http://www.jxzbtb.cn/inteligentsearch/rest/inteligentSearch/getFullTextData'

# 湖州公共资源交易中心

HZ_MAIN_SEARCH_LINK = [('http://ggzy.huzhou.gov.cn/HZfront/zfcg/024001/024001001/', ' 集中采购招标公告'),  # 政府采购 > 集中采购 > 集中采购招标公告
                       # 政府采购 > 集中采购 > 集中采购中标公示
                       ('http://ggzy.huzhou.gov.cn/HZfront/zfcg/024001/024001002/', '集中采购中标公示'),
                       # 政府采购 > 分散采购 > 分散采购招标公告
                       ('http://ggzy.huzhou.gov.cn/HZfront/zfcg/024002/024002001/', '分散采购招标公告'),
                       # 政府采购 > 分散采购 > 分散采购中标公示
                       ('http://ggzy.huzhou.gov.cn/HZfront/zfcg/024002/024002002/', '分散采购中标公示')
                       ]

# 丽水市公共资源交易网
LS_MAIN_SEARCH_LINK = [
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001001/', '丽水市本级', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001002/', '莲都区', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001003/', '龙泉市', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001004/', '青田县', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001005/', '云和县', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001006/', '庆元县', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001007/', '缙云县', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001008/', '遂昌县', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001009/', '松阳县', '交易公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005001/071005001010/', '景宁畲族自治县', '交易公告'),

    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002001/', '丽水市本级', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002002/', '莲都区', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002003/', '龙泉市', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002004/', '青田县', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002005/', '云和县', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002006/', '庆元县', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002007/', '缙云县', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002008/', '遂昌县', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002009/', '松阳县', '补充通知'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005002/071005002010/', '景宁畲族自治县', '补充通知'),

    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003001/', '丽水市本级', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003002/', '莲都区', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003003/', '龙泉市', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003004/', '青田县', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003005/', '云和县', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003006/', '庆元县', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003007/', '缙云县', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003008/', '遂昌县', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003009/', '松阳县', '成交公告'),
    ('http://www.lssggzy.com/lsweb/jyxx/071005/071005003/071005003010/', '景宁畲族自治县', '成交公告')
]
# 萧山招投标管理信息网(查看地址)
XS_MAIN_ZTB_LINK = 'http://www.xszbjyw.com/Module/ModuleView.aspx?ModuleID=4&ViewID=6'
# 萧山招投标管理信息网(爬虫所用地址)
XS_MAIN_ZTB_LINK_REAL='http://www.xszbjyw.com//web_news/NewFrom.aspx?news_bigclass=6&ViewID=6'
#开启浏览器渲染
CONFIG_SITE =['sxyc.gov.cn','yuhang.gov.cn', 'hangzhou.gov.cn', 'zjxc.gov.cn', 'ztb.shangyu.gov.cn', 'jiande.gov.cn', 'zhoushan.gov.cn']
FIRE_TIME1 = "10:30"
FIRE_TIME2 = "16:57"
