import os
import sys
import re

sys.path.append(os.path.abspath(os.path.dirname("__file__")))
from app.models.produce import Produce
from app.extensions import celery
import functools
from bson import ObjectId
from manage import create_app

app = create_app()


def decorate(func):
    @functools.wraps(func)
    def loop(*args, **kwargs):
        page = 1
        per_page = 100
        is_end = False
        total = 0
        query = {}
        while not is_end:
            data = Produce.objects(**query).paginate(page=page, per_page=per_page)
            if not len(data.items):
                print("get data is empty! \n")
                break
            func(data)
            print("current page %s: \n" % page)
            page += 1
            total += 1
            if len(data.items) < per_page:
                is_end = True
        print("is over execute count %s\n" % total)

    return loop


@decorate
def delete_design(data):
    for i, image in enumerate(data.items):
        rex = re.compile(r'design', re.IGNORECASE)
        result = [i for i in image.tags if not rex.search(i)]
        if result == image.tags:
            print('此产品无design标签',str(image._id))
            continue
        ok = image.update(tags=result)
        if ok:
            print('去除成功',str(image._id))
        else:
            print('去除失败', str(image._id))


delete_design()
