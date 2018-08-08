from flask import request, jsonify, current_app
from . import api
import datetime
from app.models.design_record import DesignRecord
from app.models.design_company import DesignCompany
from app.helpers.pager import Pager
from app.helpers.common import force_int, filter_key
from bson import ObjectId

## 列表
@api.route('/design_record/list')
def design_record_list():

    query = {}
    meta = {}
    ids = request.args.get('ids', '')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    status = int(request.args.get('status', 1))
    deleted = force_int(request.args.get('deleted', 0))
    sort = force_int(request.args.get('sort', 0))
    mark = request.args.get('mark', '')
    no = int(request.args.get('no', 0))

    if ids:
      # query['_id__in'] = list(map(lambda x: ObjectId(x), ids.split(',')))
      isArr = []
      for d in ids.split(','):
          try:
              id = ObjectId(d)
              isArr.append(id)
          except(Exception) as e:
              pass
      query['_id__in'] = isArr
    else:
        if status == -1:
            query['status'] = 0
        if status == 1:
            query['status'] = 1
        else:
            pass

        if not mark or not no:
            return jsonify(code=3001, message='缺少请求参数！')

        query['mark'] = mark
        query['no'] = no

    query['deleted'] = deleted

    #current_app.logger.debug(query)

    # 排序
    sortVal = '-ave_score'
    nSortVal = '-ave_score'
    if sort:
        if sort == 1:
            sortVal = '-base_average'
        elif sort == 2:
            sortVal = '-business_average'
        elif sort == 3:
            sortVal = '-innovate_average'
        elif sort == 4:
            sortVal = '-design_average'
        elif sort == 5:
            sortVal = '-effect_average'
        elif sort == 6:
            sortVal = '-credit_average'

    if sortVal == nSortVal:
        nSortVal = '-base_average'

    try:
        fields = ['_id', 'mark', 'no', 'ave_score', 'base_average', 'business_average', 'credit_average', 'design_average', 'effect_average', 'innovate_average', 'ave_score', 'type', 'number', 'rank', 'deleted', 'status']
        cFields = ['_id', 'name', 'logo_url', 'd3ing_id', 'province', 'city', 'description', 'scope_business']
        data = DesignRecord.objects(**query).order_by(sortVal, nSortVal).paginate(page=page, per_page=per_page)
        total_count = DesignRecord.objects(**query).count()

        # 过滤数据
        rows = []
        for i, d in enumerate(data.items):
            row = filter_key(fields, d)
            row['_id'] = str(row['_id'])
            row['design_company'] = {}
            row['evaluates'] = []
            designCompany = DesignCompany.objects(number=int(d.number)).first()
            if designCompany:
                # 系统自动生成评价
                row['evaluates'] = auto_evaluate(d, designCompany)
                designCompany['_id'] = str(designCompany['_id'])
                newCompany = filter_key(cFields, designCompany)
                row['design_company'] = newCompany
            rows.append(row)

        meta['rows'] = rows
    except(Exception) as e:
        current_app.logger.debug(str(e))
        meta['rows'] = []
        total_count = 0

    meta['total_count'] = total_count
    meta['page'] = page
    meta['per_page'] = per_page

    return jsonify(code=0, message='success!', data=meta)


# 自动生成评价内容
def auto_evaluate(record, company):
    arr = []
    content = '该机构'
    content1 = ''
    content2 = ''
    content3 = ''
    content4 = ''
    if record.ave_score > 70:
        content += '是我国工业设计行业的领先机构，其超强的整体商业逻辑与专业设计表现让其成为这份榜单中的佼佼者。'

    # 基础运作力
    if record.base_average > 71 and record.base_average <= 80:
        content += '具有相对完善的基础运作力，为其后续服务的顺利展开打下基础。'
    elif record.base_average > 81 and record.base_average <= 90:
        content += '基础实力抢眼，基本完备的企业结构能够保证项目顺利进行。'
    elif record.base_average > 90:
        content += '基础构建趋近完善，为上层设计提供了强劲储备力。'

    # 商业决策力
    if record.business_average > 71 and record.business_average <= 80:
        content += '商业表现较同行突出，商业，是实力的一部分。'
    elif record.business_average > 81 and record.business_average <= 90:
        content += '在商业层面的决策力抢眼，侧面反映了其在其他几个维度上的综合掌控力。'
    elif record.business_average > 90:
        content += '在商业层面的表现格外突出，是值得关注的目标。'

    # 创新交付力
    if record.innovate_average > 71 and record.innovate_average <= 80:
        content += '创新有可能成为这间公司的杀手锏。'
    elif record.innovate_average > 81 and record.innovate_average <= 90:
        content += '注重创新才能有长足的发展，做得不错，继续加油。'
    elif record.innovate_average > 90:
        content += '超强的创新实力让人眼前一亮！在当今强调创新设计的年代，这家公司可为不可多得。'

    # 品牌溢价力
    if record.design_average > 71 and record.design_average <= 80:
        content += '正在学习如何发挥品牌溢价力在现代的商业环境中的杀手锏作用。'
    elif record.design_average > 81 and record.design_average <= 90:
        content += '品牌驱动的年代里，Brand的溢价能力不言而喻。'
    elif record.design_average > 90:
        content += '十分注重品牌建设，在不远的将来会有意想不到的收获。'

    # 客观公信力
    if record.effect_average > 71 and record.effect_average <= 80:
        content += '致力于打磨与客户之间的默契。'
    elif record.effect_average > 81 and record.effect_average <= 90:
        content += '是可靠的合作伙伴。'
    elif record.effect_average > 90:
        content += '是值得信赖与托付的设计公司。'

    # 风险应激力
    if record.credit_average > 71 and record.credit_average <= 80:
        content += '面对风险，可以收放自如。'
    elif record.credit_average > 81 and record.credit_average <= 90:
        content += '专长在于机智应对风险。'
    elif record.credit_average > 90:
        content += '再大的风险都能巧妙化解。'

    # 是否高新企业
    if company.is_high_tech:
        content1 += '该机构为国家高新技术企业。'

    # 省、国家级设计中心
    if company.is_design_center:
        if company.is_design_center == 1:
            content2 += '该机构为省级工业设计中心，组织体系完善，有一定的从业经验与行业地位，在创新、研发实力和知识产权保护等方面表现优秀。'
        elif company.is_design_center == 2:
            content2 += '该机构为国家级工业设计中心，创新设计理念居国家领先地位，组织架构完善，整体经营状况良好，专业表现优异，行业贡献突出。'

    # 国内奖
    inside_awards = company.red_star_award_count + company.innovative_design_award_count + company.china_design_award_count + company.dia_award_count
    if inside_awards:
        inside_award_arr = []
        if company.red_star_award_count:
            inside_award_arr.append('红星奖')
        if company.innovative_design_award_count:
            inside_award_arr.append('红棉奖')
        if company.china_design_award_count:
            inside_award_arr.append('中国好设计奖')
        if company.dia_award_count:
            inside_award_arr.append('中国设计智造大奖')

        inside_award_list = '、'.join(inside_award_arr)
        if inside_awards < 20:
            content3 += "该机构设计作品获得国内工业设计大奖，包括%s，设计创新潜力无限。" % inside_award_list
        elif inside_awards >= 20 and inside_awards < 50:
            content3 += "该机构设计作品屡次获得国内工业设计大奖，包括%s，设计创新竞争力处于国内领先水平。" % inside_award_list
        elif inside_awards >= 50:
            content3 += "该机构设计作品屡次获得国内工业设计大奖，包括%s，设计创新竞争力在内的综合实力领先同行业其他机构。" % inside_award_list

    # 国外奖
    outside_awards = company.if_award_count + company.red_dot_award_count + company.idea_award_count + company.gmark_award_count
    if outside_awards:
        outside_award_arr = []
        if company.if_award_count:
            outside_award_arr.append('IF奖')
        if company.red_dot_award_count:
            outside_award_arr.append('红点奖')
        if company.idea_award_count:
            outside_award_arr.append('IDEA工业设计奖')
        if company.gmark_award_count:
            outside_award_arr.append('G-Mark设计奖')

        outside_award_list = '、'.join(outside_award_arr)
        if outside_awards < 20:
            content4 += "该机构设计作品获得国际工业设计大奖，包括%s，设计创新实力在国际上得到认可。" % outside_award_list
        elif outside_awards >= 20 and outside_awards < 50:
            content4 += "该机构设计作品多次获得国际工业设计大奖，包括%s，设计创新实力多次在国际上得到认可。" % outside_award_list
        elif outside_awards > 50:
            content4 += "该机构设计作品屡次获得国际工业设计大奖，包括%s，具有十分抢眼的国际级竞争力，提升了我国设计创新综合实力。" % outside_award_list

    arr.append(content)
    if content1:
        arr.append(content1)
    if content2:
        arr.append(content2)
    if content3:
        arr.append(content3)
    if content4:
        arr.append(content4)

    return arr

