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
        self.check = tk.Button(self.commitFrame, text="演示校验", command=self.check)
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
        # self.parent.step_list.append(self.step_info)
        self.parent.is_cancel = True
        self.parent.current_window = self.parent.sfc.get_current_window()
        # 显式地更新父窗口界面
        # self.parent.l1.config(text=self.parent.name)
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.parent.is_cancel = False
        self.destroy()

    def check(self):
        info = {'xpath':self.xpath.get(), 'name':'id', 'value':self.xpath.get()}
        # find ,click
        setp_type = self.stepType_box.get()
        if setp_type == 'write':
            self.parent.sfc.input_any(self.xpath.get(), self.value.get())

        # 检测元素是否有id
        is_id = self.parent.sfc.check_id_exist(self.xpath.get())
        if is_id and is_id != '':
            self.parent.sfc.add_style_border(is_id)
        else:
            element = self.parent.sfc.set_element_attribute(info)
            if element:
                self.parent.sfc.add_style_border(info['value'])
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
        self.open = ttk.Button(self.mighty, text="打开浏览器", command=self.open_chrome, width=10)
        self.put_js = ttk.Button(self.mighty, text="录制当前页面", command=self.start_record, width=10)
        self.new_script = ttk.Button(self.mighty, text="新建脚本", command=self.new_script, width=10)
        self.action = ttk.Button(self.mighty, text="录制此步骤", command=self.catch_step, width=10)
        self.edit_script = ttk.Button(self.mighty, text="编辑脚本", command=self.catch_step, width=10)
        self.save_script = ttk.Button(self.mighty, text="保存脚本", command=self.new_step, width=10)
        self.go_js = ttk.Button(self.mighty, text="注入功能", command=self.set_js, width=10)
        # self.action = ttk.Button(self.mighty, text="测试", command=lambda: self.get_step(action_id=1), width=10)
        self.mighty1 = ttk.LabelFrame(self.win, text=' 步骤详情 ')
        column = ("步骤顺序", "URL", "步骤类型", "XPATH", "VALUE", "REMARK")
        self.table = ttk.Treeview(self.mighty1, show="headings", column=column)
        self.vbar = ttk.Scrollbar(self.mighty1, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=self.vbar.set)
        self.table.column("步骤顺序", width=50, anchor='center')
        self.table.column("URL", width=80, anchor='center')
        self.table.column("步骤类型", width=80, anchor='center')
        self.table.column("XPATH", width=240, anchor='center')
        self.table.column("VALUE", width=100, anchor='center')
        self.table.column("REMARK", width=170, anchor='center')
        self.table.heading("步骤顺序", text="No", anchor='center')
        self.table.heading("URL", text="URL", anchor='center')
        self.table.heading("步骤类型", text="TYPE", anchor='center')
        self.table.heading("XPATH", text="XPATH", anchor='center')
        self.table.heading("VALUE", text="VALUE", anchor='center')
        self.table.heading("REMARK", text="REMARK", anchor='center')

        self.script_name = 'a'
        self.step_list = []
        self.url = None
        self.step_number = 0
        self.is_cancel = False
        self.current_frame = '主界面'
        self.refresh_frame = []
    def layout_grid(self):
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        self.open.grid(column=0, row=1, sticky='W')
        self.put_js.grid(column=1, row=1, sticky='W')
        self.new_script.grid(column=3, row=1, sticky='W')
        self.action.grid(column=4, row=1, sticky='W')
        self.edit_script.grid(column=5, row=1, sticky='W')
        self.save_script.grid(column=6, row=1, sticky='W')
        self.go_js.grid(column=7, row=1, sticky='W')
        self.mighty1.grid(column=0, row=1, padx=8, pady=4)
        self.table.grid(column=0, row=2, sticky='W')
        self.vbar.grid(row=2, column=1, sticky='NS')

    def start(self):
        self.refresh_table()
        self.layout_grid()
        self.win.mainloop()

    def open_chrome(self):
        # 初始化自动化方法
        self.sfc = sfunc.WebDriver()
        self.sfc.clear_list()
        self.step_list = []

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
            self.step_list.append({'stepNumber': 1, 'actionType': 'get', 'url': self.url, 'xpath': '', 'value': '', 'remark': '打开目标网址'})
            self.current_frame = '主界面'
        except: tk.messagebox.showerror('错误', '请先打开浏览器')

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
        if info is not None:
            self.actionid = info[0][0]
            tk.messagebox.showinfo('成功', '脚本新建成功，actionid为 %s' % self.actionid)

    # 测试不同容器间步骤切换。
    def catch_step(self):
        # self.url = self.sfc.get_current_url()
        # 添加判断 ，如果
        self.sfc.clear_list()
        step_list = self.sfc.catch_xpath()  # [当前抓取的步骤]
        print('1=====', step_list)
        # 判断step_list中只有主界面一个元素，那么错误（待开发）
        # if step_list is False or len(step_list) < 1:
        if len(step_list) < 1 or step_list[-1]['actionType'] == 'jump':
            tk.messagebox.showerror('错误', '请先选取目标元素！')
            # 跳转到之前的页面
            self.sfc.switch_win(self.current_frame)
            return
        for step in step_list:
            self.step_number += 1
            step['stepNumber'] = self.step_number  # 给步骤排序完成
            # 如果不是跳转的动作，则弹出新增动作的输入框
            if step['actionType'] == '':
                self.new_step(step)  # 将排序好的步骤传入新建页面 ，进行value和type、remark填写。
                # 新增步骤有两种情况，一个是确认，一个是取消 。填写完成后用户点击确定，将修改后的step插入self.step_list
                # self.step_list.remove(step)  # 确认新增，
            else:
                print("进入:", step['xpath'])
                self.refresh_frame.append(step['xpath'])
        # 不取消,添加进步骤内，并且更新所在的frame
        if self.is_cancel:
            self.step_list.extend(step_list)
            self.current_frame = self.refresh_frame[-1]
        # 取消
        if self.is_cancel is False:
            print(step_list)
            self.step_number -= len(step_list)
            # 如果本次采集跳转步骤list长度大于1，那么逆序跳转
            if len(self.refresh_frame) > 1:
                for frame in reversed(self.refresh_frame):
                    self.sfc.switch_win(frame)
                    print("返回：", frame)
            self.sfc.switch_win(self.current_frame)

        print(self.step_list)
        # 刷新步骤

    def refresh_table(self):
        # 清空表
        for _ in map(self.table.delete, self.table.get_children("")):pass
        # 插入表
        if len(self.step_list) > 0:
            for rw in self.step_list:
                self.table.insert('', rw.get('stepNumber'), values=(
                rw.get('stepNumber'), rw.get('url'), rw.get('actionType'), rw.get('xpath'), rw.get('value'), rw.get('remark')))
        self.table.after(500, self.refresh_table)


    # 打开新增步骤的窗口
    def new_step(self, step):
        ns = NewStep(self, step)
        self.win.wait_window(ns)
        # 判断
    # 手动注入js
    def set_js(self):
        self.sfc.init_iframe()
    # 编辑脚本



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