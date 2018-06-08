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
        cFields = ['_id', 'name', 'logo_url', 'd3ing_id', 'description', 'scope_business']
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


