#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : runmain.py
# @Author: shijiu
# @Date  : 2020/8/28 
# @SoftWare  : PyCharm

"""
    #####################
    执行脚本的GUI
    实现脚本渲染，
"""

import tkinter as tk
from tkinter import ttk
import tkinter.messagebox


class RunMain(tk.Toplevel):

    def __init__(self, parent, script_list):
        super().__init__()
        self.title('脚本坞')
        self.parent = parent
        self.script_list = script_list
        self.mighty = ttk.LabelFrame(self, text=' 脚本列表 ')
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        for i in range(len(self.script_list)):
            ttk.Button(self.mighty, text=self.script_list[i][1], command=lambda aId = self.script_list[i][0]: self.get_script(aId)).grid(column=i, row=1, sticky='W')

    def get_script(self, action_id):
        # msg = self.name_entered.get()
        # 根据 action_id 获取登录网站所需要的动作列表
        self.step_list = []
        sql = "SELECT * FROM [actionList] WHERE actionid = '%s'ORDER BY fatherid ASC ;" % action_id
        info = self.parent.odb.ExecQuery(sql)
        if len(info) > 0:
            # tk.messagebox.showinfo('提示', u_res[0][2])
            for i in info:
                self.step_list.append({'actionId': i[1], 'fatherId': i[2], 'url': i[3], 'actionType': i[4], 'xpath': i[5], 'value': i[6]})
        else:
            tk.messagebox.showinfo('提示', "脚本不存在！")
        print(self.step_list)
        # 检查浏览器是否打开
        self.chrome_is_open()
        self.do_login()

    def chrome_is_open(self):
        try:
            if self.parent.sfc is None:
                self.parent.open_chrome()
                return True
            else:
                return True
        except:
            tk.messagebox.showerror("错误", "请在程序中先开启浏览器。")
            return False

    # 解析登录步骤，登录
    def do_login(self):
        print(self.step_list)
        types = {'wait': self.do_wait, 'find': self.do_find, 'write': self.do_write, 'click': self.do_click, 'jump': self.do_jump, 'get': self.do_get, 'jumpWindow':self.do_jump_window}
        for action in self.step_list:
            method = types.get(action['actionType'])  # type = 0 1 2 ...
            if method:
                isgo = method(action)
                if isgo: continue  # 如果返回True, 表示该步骤执行完毕
                else:tk.messagebox.showerror('错误', '第 %s 步出错。请检查参数。' % (int(action['fatherId'])+1)); break

    def do_wait(self, action):
        print(action)
        self.parent.sfc.is_wait(action['xpath'])
        return True

    def do_find(self, action):
        print(action)
        self.parent.sfc.find_ele(action['xpath'])
        return True

    def do_write(self, action):
        print(action)
        self.parent.sfc.input_any(action['xpath'], action['value'])
        return True

    def do_click(self, action):
        print(action)
        self.parent.sfc.click_in(action['xpath'])
        return True

    def do_jump(self, action):
        print(action)
        self.parent.sfc.switch_win(action['xpath'])
        return True

    def do_get(self, action):
        self.parent.sfc.get_url(action['url'])
        return True

    def do_jump_window(self, action):
        print(action)
        self.parent.sfc.switch_to_window(action['value'])
        return True


