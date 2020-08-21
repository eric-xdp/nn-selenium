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
class NewScript(tk.Toplevel):
    def __init__(self,parent):
        super().__init__()
        self.title('新建脚本')
        self.parent = parent
        # 第一行（两列）
        row1 = tk.Frame(self)
        row1.pack(fill="x", ipadx=10, pady=30)
        tk.Label(row1, text='脚本名称：', width=8).pack(side=tk.LEFT)
        self.name = tk.StringVar()
        tk.Entry(row1, textvariable=self.name, width=20).pack(side=tk.LEFT)
        # 第二行
        row2 = tk.Frame(self)
        row2.pack(fill="x",ipadx=10, ipady=10)
        tk.Button(row2, text="取消", command=self.cancel).pack(side=tk.RIGHT,padx=10)
        tk.Button(row2, text="确定", command=self.ok).pack(side=tk.RIGHT,padx=10)

    def ok(self):
        # 显式地更改父窗口参数
        self.parent.script_name = self.name.get()
        # 显式地更新父窗口界面
        # self.parent.l1.config(text=self.parent.name)
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()

class NewStep(tk.Toplevel):
    def __init__(self, parent, stepinfo):
        super().__init__()
        self.title('新增步骤')
        self.parent = parent
        self.step_info = stepinfo
        # xpath
        self.xpathFrame = ttk.LabelFrame(self, text=' xpath: ')
        self.xpath = tk.StringVar()
        self.xpath.set(self.step_info['xpath'])
        self.xpath_entered = ttk.Entry(self.xpathFrame, width=80, textvariable=self.xpath, state='readonly')
        self.xpathFrame.grid(column=0, row=0, padx=8, pady=4)
        self.xpath_entered.grid(column=0, row=0, sticky='W')
        # value
        self.valueFrame = ttk.LabelFrame(self, text=' 传入值: ')
        self.value = tk.StringVar()
        self.value_entered = ttk.Entry(self.valueFrame, width=80, textvariable=self.value)
        self.valueFrame.grid(column=0, row=1, padx=8, pady=4)
        self.value_entered.grid(column=0, row=0, sticky='W')
        # 步骤类型
        self.stepTypeFrame = ttk.LabelFrame(self, text=' 步骤类型: ')
        self.stepType = tk.StringVar()
        self.stepType_box = ttk.Combobox(self.stepTypeFrame, width=77, textvariable=self.stepType, state='readonly')
        self.stepType_box["values"] = ("find", "write", "click")
        self.stepType_box.bind("<<ComboboxSelected>>", self.stepType_set)
        self.stepTypeFrame.grid(column=0, row=2, padx=8, pady=4)
        self.stepType_box.grid(column=0, row=0, sticky='W')
        # 步骤说明
        self.remarkFrame = ttk.LabelFrame(self, text=' 步骤说明: ')
        self.remark = tk.StringVar()
        self.remark_entered = ttk.Entry(self.remarkFrame, width=80, textvariable=self.remark)
        self.remarkFrame.grid(column=0, row=3, padx=8, pady=4)
        self.remark_entered.grid(column=0, row=0, sticky='W')
        # 演示、提交、取消
        self.commitFrame = ttk.LabelFrame(self, text='')
        self.commitFrame.grid(column=0, row=4, padx=8, pady=4)
        self.check = tk.Button(self.commitFrame, text="演示校验", command=self.cancel)
        self.check.grid(column=0, row=0, sticky='W')
        self.commit = tk.Button(self.commitFrame, text="确认提交", command=self.ok)
        self.commit.grid(column=1, row=0, sticky='W', padx=30)
        self.backBtn = tk.Button(self.commitFrame, text="取消/返回", command=self.cancel)
        self.backBtn.grid(column=2, row=0, sticky='W')


    def stepType_set(self, *args):
        self.step_info['actionType'] = self.stepType_box.get()

    def ok(self):
        self.step_info['remark'] = self.remark.get()
        self.step_info['value'] = self.value.get()
        # 显式地更改父窗口参数
        self.parent.step_list.append(self.step_info)
        # 显式地更新父窗口界面
        # self.parent.l1.config(text=self.parent.name)
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.destroy()
# 主窗口
class MyBox():
    def __init__(self):
        # super().__init__()
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
        self.put_js = ttk.Button(self.mighty, text="录制当前页面", command=self.start_record, width=10)
        self.new_script = ttk.Button(self.mighty, text="新建脚本", command=self.new_script, width=10)
        self.edit_script = ttk.Button(self.mighty, text="编辑脚本", command=self.catch_step, width=10)
        self.action = ttk.Button(self.mighty, text="录制此步骤", command=self.catch_step, width=10)
        self.insert_step = ttk.Button(self.mighty, text="ceshi", command=self.new_step, width=10)
        # self.action = ttk.Button(self.mighty, text="测试", command=lambda: self.get_step(action_id=1), width=10)
        self.mighty1 = ttk.LabelFrame(self.win, text=' 步骤详情 ')
        column = ("步骤顺序", "URL", "步骤类型", "XPATH", "VALUE", "REMARK")
        self.table = ttk.Treeview(self.mighty1, show="headings", column=column)
        self.table.column("步骤顺序", width=100)
        self.table.column("URL", width=100)  
        self.table.column("步骤类型", width=100)  
        self.table.column("XPATH", width=100)  
        self.table.column("VALUE", width=100)  
        self.table.column("REMARK", width=100)  
        self.table.heading("步骤顺序", text="步骤顺序")
        self.table.heading("URL", text="URL")  
        self.table.heading("步骤类型", text="步骤类型")  
        self.table.heading("XPATH", text="XPATH")  
        self.table.heading("VALUE", text="VALUE")  
        self.table.heading("REMARK", text="REMARK")

        self.script_name = 'a'
        self.step_list = []
        self.url = None
        self.step_number = 0

    def layout_grid(self):
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        self.open.grid(column=0, row=1, sticky='W')
        self.put_js.grid(column=1, row=1, sticky='W')
        self.new_script.grid(column=3, row=1, sticky='W')
        self.edit_script.grid(column=4, row=1, sticky='W')
        self.action.grid(column=5, row=1, sticky='W')
        self.insert_step.grid(column=6, row=1, sticky='W')
        self.mighty1.grid(column=0, row=1, padx=8, pady=4)
        self.table.grid(column=0, row=2, sticky='W')

    def start(self):
        self.layout_grid()
        self.win.mainloop()

    def open_chrome(self):
        print('打开浏览器')
        # 初始化自动化方法
        self.sfc = sfunc.WebDriver()

    # 开始录制
    def start_record(self):
        try:
            # 初始化iframe并将获取xpath的js注入到每个iframe中。并记录第一步，网址
            if self.script_name is None:
                tk.messagebox.showwarning('警告', '请先新建脚本')
                return
            self.sfc.init_iframe()
            self.url = self.sfc.get_current_url()
            self.step_number = 1
            self.step_list.append({'stepNumber': 1, 'actionType': 'get', 'xpath': None, 'remark': '打开目标网址'})
        except: tk.messagebox.showerror('错误', '请先打开浏览器');

    # 在新建脚本后，需要将脚本信息插入数据库，生成action的信息返回。
    def new_script(self):
        new_win = NewScript(self)
        self.win.wait_window(new_win)
        if self.script_name == '':
            tk.messagebox.showwarning('警告', '请输入有效脚本名')
            return
        # 插入数据
        sql = "INSERT INTO [action] (ActionName,ActionDesc) VALUES ('%s', '%s')" %(self.script_name, self.script_name)
        self.odb.ExecNonQuery(sql)
        select_sql = "SELECT * FROM [action] WHERE ActionName = '%s'" % self.script_name
        info = self.odb.ExecQuery(select_sql)
        print(info)
        if info is not None:
            self.actionid = info[0][0]
            tk.messagebox.showinfo('成功', '脚本新建成功，actionid为 %s' % self.actionid)

    # 测试不同容器间步骤切换。
    def catch_step(self):
        self.sfc.clear_list()
        step_list = self.sfc.catch_xpath()
        for step in step_list:
            self.step_number += 1
            step['stepNumber'] = self.step_number
            # 如果不是跳转的动作，则弹出新增动作的输入框
            if step['actionType'] is None:
                self.new_step()

        self.step_list.extend(step_list)
        print(self.step_list)

    def new_step(self):
        step = {'stepNumber': 1, 'actionType': None, 'xpath': '/html/body/div[1]/div[4]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]', 'value': None, 'remark': '打开目标网址'}
        ns = NewStep(self, step)
        self.win.wait_window(ns)
        print(self.step_list)
        # column = ("步骤顺序", "URL", "步骤类型", "XPATH", "VALUE", "REMARK") {'stepNumber': 1, 'actionType': 'get', 'xpath': None, 'remark': '打开目标网址'}
        # 将步骤插入列表 [{'actionid': None, 'fatherid': None, 'actionType': None, 'xpath': '/html/body/div[1]/div[4]/div[1]/div[1]/div[2]/form[1]/div[2]/div[1]/input[1]', 'remark': ''}]
        # i = 0
        # for step in step_list:
        #     self.table.insert('', i, values=(self.fatherid, step.get("fatherid"), step.get("actionid"), step.get("age")))
        #     i += 1
    # 设置步骤，增删改
    # def set_step(self):
    #     pass
    #
    # def get_step(self, action_id):
    #     # msg = self.name_entered.get()
    #     # 根据 action_id 获取登录网站所需要的动作列表
    #     self.step_list = []
    #     sql = "SELECT * FROM [actionList] WHERE actionid = '%s';" % action_id
    #     info = self.odb.ExecQuery(sql)
    #     if len(info) > 0:
    #         # tk.messagebox.showinfo('提示', u_res[0][2])
    #         for i in info:
    #             self.step_list.append({'actionId': i[1], 'fatherId': i[2], 'url': i[3], 'actionType': i[4], 'xpath': i[5], 'value': i[6]})
    #     else:
    #         tk.messagebox.showinfo('提示', "用户不存在")
    #     print(self.step_list)
    #     self.do_login()
    #
    # # 解析登录步骤，登录
    # def do_login(self):
    #     types = {'wait': self.do_wait, 'find': self.do_find, 'write': self.do_write, 'click': self.do_click, 'jump': self.do_jump, 'get': self.do_get}
    #     for action in self.step_list:
    #         method = types.get(action['actionType'])  # type = 0 1 2 ...
    #         if method:
    #             isgo = method(action)
    #             if isgo: continue  # 如果返回True, 表示该步骤执行完毕
    #             else:tk.messagebox.showerror('错误', '第 %s 步出错。请检查参数。' % (int(action['fatherId'])+1)); break
    #
    # def do_wait(self, action):
    #     print(action)
    #     print("这是等待步骤")
    #     self.sfc.is_wait(action['xpath'])
    #     return True
    #
    # def do_find(self, action):
    #     print(action)
    #     print("这是查找元素")
    #     self.sfc.find_ele(action['xpath'])
    #     return True
    #
    # def do_write(self, action):
    #     print(action)
    #     print("这是写入数据")
    #     self.sfc.input_any(action['xpath'], action['value'])
    #     return True
    #
    # def do_click(self, action):
    #     print(action)
    #     print("这是点击步骤")
    #     self.sfc.click_in(action['xpath'])
    #     return True
    #
    # def do_jump(self, action):
    #     print(action)
    #     print("这是iframe窗口切换")
    #     self.sfc.switch_win(action['xpath'])
    #     return True
    #
    # def do_get(self, action):
    #     print("这是登录")
    #     self.sfc.get_url(action['url'])
    #     return True

if __name__ == '__main__':
    mybox = MyBox()
    mybox.start()