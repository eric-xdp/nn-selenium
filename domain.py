#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : domain.py
# @Author: shijiu
# @Date  : 2020/8/7 
# @SoftWare  : PyCharm

import seleniumfunc as sfunc
import sqlserver as sqls
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
#  GUI 界面
class MyBox():
    def __init__(self) -> None:
        # 初始化自动化方法
        self.sfc = ''
        # 初始化数据库
        self.odb = sqls.ODBC(server='120.79.208.121,1433', uid='auto', pwd='autogxpwd', db="auto")
        # GUI
        self.win = tk.Tk()
        self.win.title('My MagicBox')
        self.mighty = ttk.LabelFrame(self.win, text=' 用户操作 ')
        # self.a_label = ttk.Label(self.mighty, text="用户名:")
        # self.name = tk.StringVar()
        self.open = ttk.Button(self.mighty, text="打开浏览器", command=self.open_chrome, width=10)
        # self.name_entered = ttk.Entry(self.mighty, width=30, textvariable=self.name)
        self.put_js = ttk.Button(self.mighty, text="录制当前页面", command=lambda: self.get_step(action_id=1), width=10)
        self.action = ttk.Button(self.mighty, text="录制当前页面", command=lambda: self.get_step(action_id=1), width=10)
        self.step_list = []

    def layout_grid(self):
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        # self.a_label.grid(column=0, row=0, sticky='W')
        # self.name_entered.grid(column=0, row=1, sticky='W')
        self.open.grid(column=0, row=1, sticky='W')
        self.put_js.grid(column=1, row=1, sticky='W')

    def start(self):
        self.layout_grid()
        self.win.mainloop()

    def open_chrome(self):
        print('打开浏览器')
        self.sfc = sfunc.WebDriver()

    def get_step(self, action_id):
        # msg = self.name_entered.get()
        # 根据 action_id 获取登录网站所需要的动作列表
        self.step_list = []
        sql = "SELECT * FROM [actionList] WHERE actionid = '%s';" % action_id
        info = self.odb.ExecQuery(sql)
        if len(info) > 0:
            # tk.messagebox.showinfo('提示', u_res[0][2])
            for i in info:
                self.step_list.append({'actionId': i[1], 'fatherId': i[2], 'url': i[3], 'actionType': i[4], 'xpath': i[5], 'value': i[6]})
        else:
            tk.messagebox.showinfo('提示', "用户不存在")
        print(self.step_list)
        self.do_login()

    # 解析登录步骤，登录
    def do_login(self):
        types = {'wait': self.do_wait, 'find': self.do_find, 'write': self.do_write, 'click': self.do_click, 'jump': self.do_jump, 'get': self.do_get}
        for action in self.step_list:
            method = types.get(action['actionType'])  # type = 0 1 2 ...
            if method:
                isgo = method(action)
                if isgo: continue  # 如果返回True, 表示该步骤执行完毕
                else:tk.messagebox.showerror('错误', '第 %s 步出错。请检查参数。' % (int(action['fatherId'])+1)); break

    def do_wait(self, action):
        print(action)
        print("这是等待步骤")
        self.sfc.is_wait(action['xpath'])
        return True

    def do_find(self, action):
        print(action)
        print("这是查找元素")
        self.sfc.find_ele(action['xpath'])
        return True

    def do_write(self, action):
        print(action)
        print("这是写入数据")
        self.sfc.input_any(action['xpath'], action['value'])
        return True

    def do_click(self, action):
        print(action)
        print("这是点击步骤")
        self.sfc.click_in(action['xpath'])
        return True

    def do_jump(self, action):
        print(action)
        print("这是iframe窗口切换")
        self.sfc.switch_win(action['xpath'])
        return True

    def do_get(self, action):
        print("这是登录")
        self.sfc.get_url(action['url'])
        return True

if __name__ == '__main__':
    mybox = MyBox()
    mybox.start()