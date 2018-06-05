# -*- coding:utf-8 -*-

from flask import render_template, request, current_app, url_for, jsonify, g, flash
from . import admin
from app.models.design_record import DesignRecord
from app.models.design_company import DesignCompany
from app.models.design_conf import DesignConf
from app.helpers.pager import Pager
from app.helpers.common import force_int
from app.helpers.constant import design_dimension_options, design_fields_label_options
from app.forms.design_record import SaveForm, setStatus
from bson import ObjectId

## 列表
@admin.route('/design_record/list')
def design_record_list():
    meta = {
        'title': '设计公司统计管理',
        'css_nav_sub_design_record': 'active',
        'css_nav_design': 'active'
    }
    query = {}
    page = force_int(request.args.get('page', 1))
    per_page = force_int(request.args.get('per_page', 100))
    status = force_int(request.args.get('status', 0))
    deleted = force_int(request.args.get('deleted', 0))
    sort = force_int(request.args.get('sort', 0))
    is_d3in = force_int(request.args.get('is_d3in', 0))
    mark = request.args.get('mark', '')
    number = request.args.get('number', '')
    no = request.args.get('no', '')

    if mark:
        query['mark'] = mark
    if no:
        query['no'] = no
    if number:
        query['number'] = number

    if is_d3in:
        if is_d3in == -1:
            query['is_d3in'] = 0
        elif is_d3in == 1:
            query['is_d3in'] = 1

    if status == -1:
        meta['css_disable'] = 'active'
        query['status'] = 0
    if status == 1:
        query['status'] = 1
        meta['css_enable'] = 'active'
    else:
        meta['css_all'] = 'active'

    query['deleted'] = deleted

    # 排序
    sortVal = '-created_at'
    nSortVal = '-base_average'
    if sort:
        if sort == 1:
            sortVal = '-ave_score'
        elif sort == 2:
            sortVal = '-base_average'
        elif sort == 3:
            sortVal = '-business_average'
        elif sort == 4:
            sortVal = '-innovate_average'
        elif sort == 5:
            sortVal = '-design_average'
        elif sort == 6:
            sortVal = '-effect_average'
        elif sort == 7:
            sortVal = '-credit_average'

    if sortVal == nSortVal:
        nSortVal = '-base_average'

    page_url = url_for('admin.design_record_list', page="#p#", mark=mark, no=no, number=number, sort=sort, is_d3in=is_d3in, status=status)

    data = DesignRecord.objects(**query).order_by(sortVal, nSortVal).paginate(page=page, per_page=per_page)
    total_count = DesignRecord.objects(**query).count()

    # 过滤数据
    for i, d in enumerate(data.items):
        data.items[i].design_company = {}
        designCompany = DesignCompany.objects(number=int(d.number)).fields(['_id', 'name', 'logo_url', 'd3ing_id']).first()
        if designCompany:
            data.items[i].design_company = designCompany

    meta['data'] = data.items

    # 获取配置列表
    confArr = DesignConf.objects(status=1).fields(['mark', 'name'])
    meta['design_conf'] = confArr

    pager = Pager(page, per_page, total_count, page_url)
    meta['pager'] = pager.render_view()
    
    meta['design_dimension_options'] = design_dimension_options()
    meta['design_fields_label_options'] = design_fields_label_options()
    #current_app.logger.debug('aaaa')

    return render_template('admin/design_record/list.html', meta=meta)

## 编辑
@admin.route('/design_record/submit')
def design_record_submit():
    meta = {
        'title': '设计公司统计管理',
        'css_nav_sub_design_record': 'active',
        'css_nav_design': 'active'
    }
    id = request.args.get('id', None)
    meta['data'] = None
    if id:
        design_record = DesignRecord.objects(_id=ObjectId(id)).first()
        meta['data'] = design_record

    form = SaveForm()

    meta['referer_url'] = request.environ.get('HTTP_REFERER') if request.environ.get('HTTP_REFERER') else ''
    
    return render_template('admin/design_record/submit.html', meta=meta, form=form)

## 保存
@admin.route('/design_record/save', methods=['POST'])
def design_record_save():
    meta = {
        'title': '设计公司统计管理',
        'css_nav_sub_design_record': 'active',
        'css_nav_design': 'active'
    }

    form = SaveForm()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            if id:
                design_record = form.update()
            else:
                design_record = form.save(user_id=g.user._id)
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if design_record:
            flash('操作成功!', 'success')
            redirect_to = request.form.get('referer_url') if request.form.get('referer_url') else url_for('admin.design_record_list')
            return jsonify(success=True, message='操作成功!', redirect_to = redirect_to)
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))

## 操作状态
@admin.route('/design_record/set_status', methods=['POST'])
def design_record_set_status():
    meta = {}

    form = setStatus()
    if form.validate_on_submit():
        id = request.form.get('id')
        
        try:
            design_record = form.set_status()
        except(Exception) as e:
            return jsonify(success=False, message=str(e))

        if design_record:
            return jsonify(success=True, message='操作成功!')
        else:
            return jsonify(success=False, message='操作失败!')
    else:
        return jsonify(success=False, message=str(form.errors))
    
    
## 删除
@admin.route('/design_record/delete', methods=['POST'])
def design_record_delete():
    meta = {}

    ids = request.values.get('ids', '')
    type = request.values.get('type', 1)
    if not ids:
        return jsonify(success=False, message='缺少请求参数!')
    
    try:
        arr = ids.split(',')
        for d in arr:
            design_record = DesignRecord.objects(_id=ObjectId(d)).first()
            design_record.delete() if design_record else None
    except(Exception) as e:
        return jsonify(success=False, message=str(e))

    return jsonify(success=True, message='操作成功!', data={'ids': ids, 'type':type}, redirect_to=url_for('admin.design_record_list'))


