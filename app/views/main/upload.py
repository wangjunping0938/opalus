from flask import render_template, current_app, jsonify, request
import os
from . import main 
from app import redis_store

from app.helpers.asset import handle_file

@main.route('/upload', methods=['POST'])
def upload():
    try:
        f = request.files['file']
        asset_type = request.values.get('asset_type', 1)
        user_id = request.values.get('user_id', 0)
        target_id = request.values.get('target_id', '')
        evt = int(request.values.get('evt', 1))
        callback_type = request.values.get('callback_type', 1)

        param = {
            'asset_type': asset_type,
            'user_id': user_id,
            'target_id': target_id,
            'evt': evt
        }
        handle_result = handle_file(f, **param)

        if not handle_result['success']:
            return jsonify(code=500, message=handle_result['message'])

        handle_result['data']['thumb_url'] = os.path.join(current_app.config['ASSET_URL'], handle_result['data']['path'] + '-sm')
        return jsonify(code=200, message='', data=handle_result['data'])
    except(Exception) as e:
        current_app.logger.debug(str(e))
        return jsonify(code=500, message=str(e))

