from elasticsearch import Elasticsearch
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.image import Image
from app.extensions import celery
from manage import create_app

app = create_app()

@celery.task()
def rename():
    query = {}
    query['evt'] = 3
    page = 1
    per_page = 100
    is_end = False
    total = 1
    while not is_end:
        # 倒序
        data = Image.objects(**query).order_by('created_at').paginate(page=page, per_page=per_page)
        if not len(data.items):
            print("get data is empty! \n")
            break
        for i, image in enumerate(data.items):
            if image.channel == '51design':
                image.update(channel='www.51design.com')
            elif image.channel == '333cn':
                image.update(channel='www.333cn.com')
            elif image.channel == 'a-four':
                image.update(channel='www.a-fourdesign.com')
            elif image.channel == 'adesign':
                image.update(channel='www.awardeddesigns.com')
            elif image.channel == 'artop':
                image.update(channel='www.artop-sh.com')
            elif image.channel == 'beetlecn':
                image.update(channel='www.beetlecn.com')
            elif image.channel == 'bfit':
                image.update(channel='www.bfitdesign.com')
            elif image.channel == 'blogdeco':
                image.update(channel='www.blogdecodesign.fr')
            elif image.channel == 'thecool' and image.prize_id == 15:
                image.update(channel='www.chinagooddesignaward.com')
            elif image.channel == 'ctdesign':
                image.update(channel='www.ctdesign.cn')
            elif image.channel == 'daetu':
                image.update(channel='www.daetumdesign.com')
            elif image.channel == 'daye':
                image.update(channel='www.daye.hk')
            elif image.channel == 'milk':
                image.update(channel='design-milk.comm')
            elif image.channel == 'effec':
                image.update(channel='www.effectivedesign.org.uk')
            elif image.channel == 'deboom':
                image.update(channel='www.designboom.com')
            elif image.channel == 'designdo':
                image.update(channel='www.designdo.cn')
            elif image.channel == 'di-award':
                image.update(channel='www.di-award.org')
            elif image.channel == 'dgawards':
                image.update(channel='www.dgawards.com')
            elif image.channel == 'gzid':
                image.update(channel='www.gzid.con')
            elif image.channel == 'redstar':
                image.update(channel='www.redstaraward.org')
            elif image.channel == 'hx-design':
                image.update(channel='www.hx-design.com')
            elif image.channel == 'ico-id':
                image.update(channel='www.ico-id.com')
            elif image.channel == 'idform':
                image.update(channel='www.idform.cn')
            elif image.channel == 'gd-design':
                image.update(channel='good-design.org')
            elif image.channel == 'imaydesign':
                image.update(channel='www.imaydesign.com')
            elif image.channel == 'innozen':
                image.update(channel='www.innozendesign.com')
            elif image.channel == 'jiagle':
                image.update(channel='gida.jiagle.com')
            elif image.channel == 'kangyuan':
                image.update(channel='www.yu-kangyuan.com')
            elif image.channel == 'kickstar':
                image.update(channel='www.kickstarter.com')
            elif image.channel == 'laisj':
                image.update(channel='www.laisj.com')
            elif image.channel == 'lkk':
                image.update(channel='www.lkkdesign.com')
            elif image.channel == 'matomeno':
                image.update(channel='matomeno.in')
            elif image.channel == 'mike':
                image.update(channel='www.mkdesign.cn')
            elif image.channel == 'muma':
                image.update(channel='www.designmoma.com')
            elif image.channel == 'newplan':
                image.update(channel='www.newplan.com.cn')
            elif image.channel == 'perdesign':
                image.update(channel='www.perdesigncn.com')
            elif image.channel == 'pplock':
                image.update(channel='www.pplock.com')
            elif image.channel == 'ruiguan':
                image.update(channel='www.kcandesign.com')
            elif image.channel == 'samdesign':
                image.update(channel='www.sam-id.com')
            elif image.channel == 'seeya':
                image.update(channel='www.seeyadesign.com', company='上海希雅设计有限公司')
            elif image.channel == 'sicheng':
                image.update(channel='www.thinkpower.cc')
            elif image.channel == 'siwei':
                image.update(channel='www.siwei-id.com')
            elif image.channel == 'sj33':
                image.update(channel='www.sj33.cn')
            elif image.channel == 'spark':
                image.update(channel='www.spark-design.cn')
            elif image.channel == 'sz-nd':
                image.update(channel='www.sz-nd.com')
            elif image.channel == 'topgaze':
                image.update(channel='www.topgaze.net')
            elif image.channel == 'vim':
                image.update(channel='www.vimdesign.com')
            elif image.channel == 'warting':
                image.update(channel='www.warting.com')
            elif image.channel == 'wisdbank':
                image.update(channel='www.wisdbank.com')
            elif image.channel == 'wuyi':
                image.update(channel='www.woodesigncn.com')
            elif image.channel == 'yankodesi':
                image.update(channel='www.yankodesign.com')
            elif image.channel == 'yinheid':
                image.update(channel='www.yinheid.com')
            elif image.channel == 'yxidea':
                image.update(channel='www.yxidea.com.cn')
        total += 1
        print("current page %s: \n" % page)
        page += 1
        if len(data.items) < per_page:
            is_end = True
    print("is over execute count %s\n" % total)

