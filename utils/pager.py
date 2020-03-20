class PageInfo(object):
    def __init__(self, current_page, all_count, per_page, base_url, show_page=11):
        try:
            self.current_page = int(current_page)
        except Exception as e:
            self.current_page = 1
        self.per_page = per_page
        self.all_count = all_count
        a, b = divmod(all_count, per_page)
        if b:
            a += 1
        self.all_pager = a
        self.show_page = show_page
        self.base_url = base_url

    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

    def pager(self):
        page_list = []
        half = int((self.show_page - 1) / 2)

        # 如果数据总页数<11
        if self.all_pager < self.show_page:
            begin = 1
            stop = self.all_pager + 1
        # 如果总页数>11
        else:
            if self.current_page <= half:
                begin = 1
                stop = self.show_page
            else:
                if self.current_page + half >= self.all_pager:
                    begin = self.all_pager - self.show_page + 1
                    stop = self.all_pager + 1
                else:
                    begin = self.current_page - 5
                    stop = self.current_page + 5 + 1
        if self.current_page <= 1:
            pre = """<li class='disabled'><a href="#" aria-label="Previous"><span aria-hidden="true">上一页</span></a></li>"""
        else:
            pre = """<li><a href="%s?page=%s" aria-label="Previous"><span aria-hidden="true">上一页</span></a></li>""" % (self.base_url,self.current_page - 1)
        page_list.append(pre)
        for i in range(begin, stop):
            if i == self.current_page:
                temp = "<li class='active'><a href='%s?page=%s'>%s</a></li>" % (self.base_url, i, i)
            else:
                temp = "<li><a href='%s?page=%s'>%s</a></li>" % (self.base_url, i, i)
            page_list.append(temp)

        if self.current_page >= self.all_pager:
            next = """<li class='disabled'><a href="#" aria-label="Next"><span aria-hidden="true">下一页</span></a></li>"""
        else:
            next = """<li><a href="%s?page=%s" aria-label="Next"><span aria-hidden="true">下一页</span></a></li>"""% (
                self.base_url, self.current_page + 1)
        page_list.append(next)

        return "".join(page_list)