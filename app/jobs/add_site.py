import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.site import Site
from app.extensions import celery

site_dict = {
    '51design': {'name': '51design', 'url': 'http://www.51design.com'},
    '333cn': {'name': '333cn', 'url': 'http://www.333cn.com'},
    'a-four': {'name': '岸峰官网', 'url': 'http://www.a-fourdesign.com'},
    'adesign': {'name': 'A 设计大奖官网', 'url': 'http://www.awardeddesigns.com'},
    'artop': {'name': '浪尖官网', 'url': 'http://www.artop-sh.com'},
    'beetlecn': {'name': '百拓官网', 'url': 'http://www.beetlecn.com'},
    'bfit': {'name': '柏菲官网', 'url': 'http://www.bfitdesign.com'},
    'blogdeco': {'name': '装饰设计博客', 'url': 'http://www.blogdecodesign.fr'},
    'chinagood': {'name': '中国好设计官网', 'url': 'http://www.chinagooddesignaward.com'},
    'ctdesign': {'name': '创品官网', 'url': 'http://www.ctdesign.cn'},
    'daetu': {'name': '德腾官网', 'url': 'http://www.daetumdesign.com'},
    'daye': {'name': '大业官网', 'url': 'http://www.daye.hk'},
    'milk': {'name': 'design-milk', 'url': 'http://design-milk.com'},
    'effec': {'name': 'DBA设计效能奖官网', 'url': 'http://www.effectivedesign.org.uk'},
    'deboom': {'name': 'designboom', 'url': 'http://www.designboom.com'},
    'designdo': {'name': '鼎典官网', 'url': 'http://www.designdo.cn'},
    'di-award': {'name': 'DIA中国设计制造大奖官网', 'url': 'http://www.di-award.org'},
    'gzid': {'name': '沅子官网', 'url': 'http://www.gzid.cn'},
    'redstar': {'name': '红星奖官网', 'url': 'http://www.redstaraward.org'},
    'hx-design': {'name': '幻想官网', 'url': 'http://www.hx-design.com'},
    'ico-id': {'name': '日本爱谷官网', 'url': 'http://www.ico-id.com'},
    'idform': {'name': '艾德方官网', 'url': 'http://www.idform.cn'},
    'gd-design': {'name': 'g-mark设计奖官网', 'url': 'http://good-design.org'},
    'imaydesign': {'name': '怡美官网', 'url': 'http://www.imaydesign.com'},
    'innozen': {'name': '意臣官网', 'url': 'http://www.innozendesign.com'},
    'jiagle': {'name': '中国家具金点设计奖官网', 'url': 'http://gida.jiagle.com'},
    'kangyuan': {'name': '康源官网', 'url': 'http://www.yu-kangyuan.com'},
    'kickstar': {'name': 'kickstarter', 'url': 'http://www.kickstarter.com'},
    'laisj': {'name': '来设计平台', 'url': 'http://www.laisj.com'},
    'matomeno': {'name': 'matomeno', 'url': 'http://matomeno.in'},
    'newplan': {'name': '嘉兰图官网', 'url': 'http://www.newplan.com.cn'},
    'perdesign': {'name': '品物官网', 'url': 'http://www.perdesigncn.com'},
    'pplock': {'name': 'pplock', 'url': 'http://www.pplock.com'},
    'ruiguan': {'name': '瑞观官网', 'url': 'www.kcandesign.com'},
    'samdesign': {'name': '迪特格官网', 'url': 'http://www.sam-id.com'},
    'seeya': {'name': '希雅官网', 'url': 'http://www.seeyadesign.com'},
    'sicheng': {'name': '思乘官网', 'url': 'http://www.thinkpower.cc'},
    'siwei': {'name': '思为官网', 'url': 'http://www.siwei-id.com'},
    'sj33': {'name': '设计之家', 'url': 'http://www.sj33.cn'},
    'spark': {'name': '斯帕克官网', 'url': 'http://www.spark-design.cn'},
    'sz-nd': {'name': '无限空间官网', 'url': 'http://www.sz-nd.com'},
    'topgaze': {'name': '上品设计官网', 'url': 'http://www.topgaze.net'},
    'vim': {'name': '威曼官网', 'url': 'http://www.vimdesign.com'},
    'warting': {'name': '设计帝国', 'url': 'http://www.warting.com'},
    'wisdbank': {'name': '大脑很行官网', 'url': 'http://www.wisdbank.com'},
    'wuyi': {'name': '五一设计官网', 'url': 'http://www.woodesigncn.com'},
    'yankodesi': {'name': 'yankodesign', 'url': 'http://www.yankodesign.com'},
    'yinheid': {'name': '银河官网', 'url': 'http://www.yinheid.com'},
    'yxidea': {'name': '易形官网', 'url': 'http://www.yxidea.com.cn'},

}


@celery.task()
def add_site():
    for key, value in site_dict.items():
        site = Site.objects(mark=key).first()
        if site:
            continue
        else:
            date = {'mark': key}
            date.update(value)
            site = Site(**date)
            site.save()
