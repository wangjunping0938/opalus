#encoding: utf-8

def t_color_list(data):
    if not data:
        return []
    rows = []
    # 过滤数据
    for i, d in enumerate(data.items):
        row = {
            '_id': str(d._id),
            'rgb': d.rgb,
            'hex': d.hex,
            'pantone': d.pantone,
            'cmyk': d.cmyk,
            'user_id': d.user_id,
            'deleted': d.deleted,
            'status': d.status,
            'created_at': d.created_at,
            'updated_at': d.updated_at,
        }
        rows.append(row)
    return rows

