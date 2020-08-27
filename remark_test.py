#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : remark_test.py
# @Author: shijiu.Xu
# @Date  : 2020/8/27 
# @SoftWare  : PyCharm


class EditScript(tk.Toplevel):
    def __init__(self, parent, step_list):
        super().__init__()
        self.title('编辑脚本')
        self.parent = parent
        self.step_list = step_list
        self.main = ttk.LabelFrame(self, text=' 脚本详情 ')
        column = ("步骤顺序", "URL", "步骤类型", "XPATH", "VALUE", "REMARK")
        self.etable = ttk.Treeview(self.main, show="headings", column=column)
        self.evbar = ttk.Scrollbar(self.main, orient='vertical', command=self.etable.yview)
        self.etable.configure(yscrollcommand=self.evbar.set)
        self.etable.column("步骤顺序", width=50, anchor='center')
        self.etable.column("URL", width=80, anchor='center')
        self.etable.column("步骤类型", width=80, anchor='center')
        self.etable.column("XPATH", width=240, anchor='center')
        self.etable.column("VALUE", width=100, anchor='center')
        self.etable.column("REMARK", width=170, anchor='center')
        self.etable.heading("步骤顺序", text="No", anchor='center')
        self.etable.heading("URL", text="URL", anchor='center')
        self.etable.heading("步骤类型", text="TYPE", anchor='center')
        self.etable.heading("XPATH", text="XPATH", anchor='center')
        self.etable.heading("VALUE", text="VALUE", anchor='center')
        self.etable.heading("REMARK", text="REMARK", anchor='center')
        self.domain = ttk.LabelFrame(self)
        self.insert = tk.Button(self.domain, text="插入上一步(✖)", width=15, command=self.insert_step)
        self.update = tk.Button(self.domain, text="修改步骤", width=15, command=self.update_step)
        self.delete = tk.Button(self.domain, text="删除步骤", width=15, command=self.del_step)
        # self.ok = tk.Button(self.domain, text="保存编辑", width=15, command=self.insert_step)
        # self.cancel = tk.Button(self.domain, text="取消编辑", width=15, command=self.insert_step)
        # grid
        self.main.grid(column=0, row=0, padx=8, pady=4)
        self.etable.grid(column=0, row=1, sticky='W')
        self.evbar.grid(row=1, column=1, sticky='NS')
        self.domain.grid(column=0, row=2, padx=8, pady=4)
        self.insert.grid(column=0, row=3, padx=10)
        self.update.grid(column=1, row=3, padx=10)
        self.delete.grid(column=2, row=3, padx=10)
        # self.ok.grid(column=3, row=3, padx=10)
        # self.cancel.grid(column=4, row=3, padx=10)
        # bind
        self.etable.bind('<ButtonRelease-1>', self.select_row)
        # refresh
        self.reload()
        # status
        self.is_true = False

    # 插入数据
    def insert_step(self):
        tk.messagebox.showerror('错误', '暂不支持插入步骤！')

    def update_step(self):
        step = self.select_step()
        if step:
            index = self.step_list.index(step)
            ms = MakeStep(self, step)

            self.wait_window(ms)
            print(step)
            if self.is_true:
                self.step_list[index] = step
                self.reload()

    def del_step(self):
        step = self.select_step()
        if step:
            self.is_true = tk.messagebox.askyesno("提醒", "确认删除该步骤吗？")
            if self.is_true:
                self.step_list.remove(step)
                self.reload()

    def select_step(self):
        info = self.etable.selection()
        if info:
            for item in info:
                data = self.etable.item(item, "values")
                # 在这个地方插入
                step = {'stepNumber': int(data[0]), 'actionType': data[2], 'url': data[1], 'xpath': data[3],
                        'value': data[4], 'remark': data[5]}
                return step
        else:
            tk.messagebox.showerror('错误', '请先选择插入位置')
            return False
    # 左键选中触发事件
    def select_row(self, *args):
        step = []
        for item in self.etable.selection():
            print(item)
            data = self.etable.item(item, "values")
            step.append({'stepNumber': int(data[0]), 'actionType': data[2], 'url': data[1], 'xpath': data[3], 'value': data[4], 'remark':data[5]})

