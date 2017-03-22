# -*- coding:utf-8 -*-

import math
import urllib.parse

class Pager:

    PER_PRE_NUM = 6  
    PER_NUMBER_MAX = 10

    #page
    #per_page
    #total_count
    #page_url

    def __init__(self, page, per_page, total_count, page_url):
        self.page = int(page)
        self.per_page = int(per_page)
        self.total_count = int(total_count)
        self.page_url = page_url
        self.cur_page =  math.ceil(self.total_count / self.per_page); #总页数，ceil()函数用于求大于数字的最小整数
  
    # 分页数组  
    def get_page(self):

        if self.cur_page > self.PER_NUMBER_MAX:  
            limit_start = 1 if self.page <= self.PER_PRE_NUM else self.page - (self.PER_PRE_NUM - 1)  
      
            if self.cur_page >= self.page+(self.PER_PRE_NUM-2):  
                if self.page >= self.PER_PRE_NUM:  
                    limit_end = self.cur_page - limit_start if self.page < self.PER_PRE_NUM else self.page + (self.PER_PRE_NUM - 2)  
                else:  
                    limit_end = self.PER_NUMBER_MAX  
            else:  
                limit_end = self.cur_page
                if self.page >= self.PER_NUMBER_MAX or ((limit_end - limit_start) < self.PER_NUMBER_MAX):  
                    limit_start = limit_end - (self.PER_NUMBER_MAX - 1)  
      
        else:  
            limit_start, limit_end = 1, self.cur_page
      
        return [i for i in range(limit_start, limit_end + 1)]


    # 组织页面
    def render_view(self):
        previous = 1 if self.page==1 else self.page - 1
        is_disabled_pre = 'disabled' if previous == 1 else ''
        nexts = self.page if self.cur_page==self.page else self.page + 1
        is_disabled_nex = 'disabled' if nexts == self.page else ''
        temp = '<nav aria-label="Page navigation">'
        temp += '<ul class="pagination">'
        temp += '<li class="%s"><a href="%s" aria-label="Previous"><span aria-hidden="true">&laquo;</span></a></li>' % (is_disabled_pre, self.page_url.replace(urllib.parse.quote('#p#'), str(previous)))
        for i in self.get_page():
            is_current_page = 'active' if self.page == i else ''
            temp += '<li class="%s"><a href="%s">%d</a></li>' % (is_current_page, self.page_url.replace(urllib.parse.quote('#p#'), str(i)), i)

        temp += '<li class="%s"><a href="%s" aria-label="Next"><span aria-hidden="true">&raquo;</span></a><li>' % (is_disabled_nex, self.page_url.replace(urllib.parse.quote('#p#'), str(nexts)))
        temp += '</ul>'
        temp += '</nav>'

        return temp
