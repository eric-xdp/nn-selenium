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
import runmain
import execute

# 新增脚本
class NewScript(tk.Toplevel):

    def __init__(self, parent):
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


# 新增步骤
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
        self.check = tk.Button(self.commitFrame, text="演示校验", command=self.check_ele)
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
        # self.parent.is_cancel = False
        self.destroy()

    def check_ele(self):
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


# 编辑脚本> 修改脚本
class MakeStep(tk.Toplevel):

    def __init__(self, parent, info):
        super().__init__()
        self.title('编辑脚本')
        self.parent = parent
        self.step_info = info
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
        self.value.set(self.step_info['value'])
        self.value_entered = ttk.Entry(self.valueFrame, width=80, textvariable=self.value)
        self.valueFrame.grid(column=0, row=1, padx=8, pady=4)
        self.value_entered.grid(column=0, row=0, sticky='W')
        # 步骤类型
        self.stepTypeFrame = ttk.LabelFrame(self, text=' 步骤类型: ')
        self.stepType = tk.StringVar()
        self.stepType.set(self.step_info['actionType'])
        # self.stepType_entered = ttk.Entry(self.stepTypeFrame, width=80, textvariable=self.stepType)
        self.stepType_box = ttk.Combobox(self.stepTypeFrame, width=77, textvariable=self.stepType)
        self.stepType_box["values"] = ("find", "write", "click")
        self.stepType_box.bind("<<ComboboxSelected>>", self.stepType_set)
        # self.stepType_box.set(self.step_info['actionType'])
        self.stepTypeFrame.grid(column=0, row=2, padx=8, pady=4)
        self.stepType_box.grid(column=0, row=0, padx=8, pady=4)
        # self.stepType_box.grid(column=0, row=0, sticky='W')
        # 步骤说明
        self.remarkFrame = ttk.LabelFrame(self, text=' 步骤说明: ')
        self.remark = tk.StringVar()
        self.remark.set(self.step_info['remark'])
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
        self.parent.is_cancel = True
        self.destroy()  # 销毁窗口

    def cancel(self):
        self.parent.is_cancel = False
        self.destroy()

    def check(self):
        info = {'xpath':self.xpath.get(), 'name':'id', 'value':self.xpath.get()}
        # find ,click
        setp_type = self.stepType.get()
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


# 插入步骤
class InsertStep(tk.Toplevel):
    def __init__(self, parent, front_list, back_list):
        super().__init__()
        self.title('插入步骤')
        self.parent = parent
        self.step_info = {}
        self.step_list = []
        self.back_list = back_list
        self.front_list = front_list
        self.is_jump = False
        self.jump_step = {'stepNumber': None, 'actionType': 'jump', 'url': '', 'xpath': '', 'value': '', 'remark': '插入了其他容器数据，需要跳转会原容器。'}
        # xpath
        self.xpathFrame = ttk.LabelFrame(self, text=' xpath: ')
        self.xpath = tk.StringVar()
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
        self.catch = tk.Button(self.commitFrame, text="采集元素", command=self.catch_ele)
        self.catch.grid(column=0, row=0, sticky='W')
        self.check = tk.Button(self.commitFrame, text="演示校验", command=self.check_ele)
        self.check.grid(column=1, row=0, sticky='W')
        self.commit = tk.Button(self.commitFrame, text="确认提交", command=self.ok)
        self.commit.grid(column=2, row=0, sticky='W', padx=30)
        self.backBtn = tk.Button(self.commitFrame, text="取消/返回", command=self.cancel)
        self.backBtn.grid(column=3, row=0, sticky='W')

    def stepType_set(self, *args):
        self.step_info['actionType'] = self.stepType_box.get()

    def ok(self):
        self.step_info['remark'] = self.remark.get()
        self.step_info['value'] = self.value.get()
        # 显式地更改父窗口参数
        # 不取消,添加进步骤内，并且更新所在的frame
        if len(self.parent.refresh_frame) > 0:
            self.current_frame = self.parent.refresh_frame[-1]
            # 添加步骤刷新表格
            # 9.5 将采集到的插入数据list与传入的数据做处理，生成完成插入的list，并刷新表格。
        for step in self.step_list:
            if step['actionType'] == 'jump':
                self.is_jump = True
                break
        if self.is_jump:
            for s in reversed(self.front_list):
                if s['actionType'] == 'jump':
                    self.jump_step['stepNumber'] = self.step_list[-1]['stepNumber'] + 1
                    self.jump_step['xpath'] = s['xpath']
                    self.step_list.append(self.jump_step)
                    break

        self.front_list.extend(self.step_list)  # 前段直接整合
        self.front_list.extend(self.back_list)
        self.parent.step_list = self.front_list
        self.parent.refresh_table()
        self.destroy()  # 销毁窗口

    def cancel(self):
        # self.parent.is_cancel = False
        # 取消 则获取后半段，执行到最后一步，销毁窗口
        # 合并前后两段
        self.front_list.extend(self.back_list)
        execute.ExecuteClass(self.parent, self.front_list).execute_core()
        self.destroy()

    def check_ele(self):
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

    def catch_ele(self):
        if self.parent.url_is_change():return
        self.parent.sfc.clear_list()
        step_list = self.parent.sfc.catch_xpath()  # [当前抓取的步骤] 抓取步骤最多一个 actionType 为空
        if len(step_list) < 1 or step_list[-1]['actionType'] == 'jump':
            tk.messagebox.showerror('错误', '请先选取目标元素！')
            # 跳转到之前的页面
            self.parent.sfc.switch_win(self.parent.current_frame)
            return
        for step in step_list:
            self.parent.step_number += 1
            step['stepNumber'] = self.parent.step_number  # 给步骤排序完成
            # 如果不是跳转的动作，则映射抓取到的xpath
            if step['actionType'] == '':
                self.xpath.set(step['xpath'])
                self.step_info = step
            else:
                self.parent.refresh_frame.append(step['xpath'])
        self.step_list.extend(step_list)

# 主窗口 main
class MyBox():
    # init
    def __init__(self):
        # 初始化数据库
        self.odb = sqls.ODBC(server='120.79.208.121,1433', uid='auto', pwd='autogxpwd', db="auto")
        # GUI
        self.win = tk.Tk()
        self.win.title('My MagicBox')
        # 设置居中显示
        self.center_window(840, 320)
        # 脚本注册
        self.mighty = ttk.LabelFrame(self.win, text=' 脚本初始化 ')
        self.open = ttk.Button(self.mighty, text="打开浏览器", command=self.open_chrome, width=10)
        self.new_script = ttk.Button(self.mighty, text="新建脚本", command=self.new_script, width=10)
        self.show_dock = ttk.Button(self.mighty, text="脚本坞", command=self.show_script,width=8)

        # 脚本录制
        self.mighty_record = ttk.LabelFrame(self.win, text=' 脚本录制 ')
        self.put_js = ttk.Button(self.mighty_record, text="录制当前页面", command=self.start_record, width=13)
        self.action = ttk.Button(self.mighty_record, text="录制此步骤", command=self.catch_step, width=10)
        self.go_js = ttk.Button(self.mighty_record, text="注入录制功能", command=self.set_js, width=13)

        # 脚本编辑
        self.mighty_edit = ttk.LabelFrame(self.win, text=' 脚本编辑 ')
        self.edit_script = ttk.Button(self.mighty_edit, text="插入步骤", command=self.insert_step, width=8)
        self.update_step = ttk.Button(self.mighty_edit, text="修改步骤", command=self.update_step, width=8)
        self.del_step = ttk.Button(self.mighty_edit, text="删除步骤", command=self.del_step, width=8)
        self.save_script = ttk.Button(self.mighty_edit, text="保存脚本", command=self.save_script, width=8)

        # 初始化步骤列表
        self.mighty1 = ttk.LabelFrame(self.win, text=' 步骤详情 ')
        self.init_table()
        # 初始化变量值
        self.init_all()
        self.window_list = []

    # 步骤列表初始化
    def init_table(self):
        column = ("步骤顺序", "URL", "步骤类型", "XPATH", "VALUE", "REMARK")
        self.table = ttk.Treeview(self.mighty1, show="headings", column=column)
        self.vbar = ttk.Scrollbar(self.mighty1, orient='vertical', command=self.table.yview)
        self.table.configure(yscrollcommand=self.vbar.set)
        self.table.column("步骤顺序", width=50, anchor='center')
        self.table.column("URL", width=80, anchor='center')
        self.table.column("步骤类型", width=80, anchor='center')
        self.table.column("XPATH", width=275, anchor='center')
        self.table.column("VALUE", width=125, anchor='center')
        self.table.column("REMARK", width=175, anchor='center')
        self.table.heading("步骤顺序", text="No", anchor='center')
        self.table.heading("URL", text="URL", anchor='center')
        self.table.heading("步骤类型", text="TYPE", anchor='center')
        self.table.heading("XPATH", text="XPATH", anchor='center')
        self.table.heading("VALUE", text="VALUE", anchor='center')
        self.table.heading("REMARK", text="REMARK", anchor='center')

    # grid
    def layout_grid(self):

        # 脚本注册模块
        self.mighty.grid(column=0, row=0, padx=8, pady=4)
        self.open.grid(column=0, row=1, sticky='W')
        self.new_script.grid(column=3, row=1, sticky='W')
        self.show_dock.grid(column=10, row=1, sticky='W')
        # 脚本录制模块
        self.mighty_record.grid(column=1, row=0, padx=8, pady=4)
        self.put_js.grid(column=1, row=1, sticky='W')
        self.action.grid(column=4, row=1, sticky='W')
        self.go_js.grid(column=9, row=1, sticky='W')
        # 脚本编辑模块
        self.mighty_edit.grid(column=2, row=0, padx=8, pady=4)
        self.edit_script.grid(column=5, row=1, sticky='W')
        self.update_step.grid(column=6, row=1, sticky='W')
        self.del_step.grid(column=7, row=1, sticky='W')
        self.save_script.grid(column=8, row=1, sticky='W')

        # 脚本步骤预览模块
        self.mighty1.grid(column=0, row=1, padx=8, pady=4, columnspan=3)
        self.table.grid(column=0, row=2, sticky='W')
        self.vbar.grid(row=2, column=1, sticky='NS')

    # 设置页面宽高，位置
    def center_window(self, w, h):
        # 获取屏幕 宽、高
        ws = self.win.winfo_screenwidth()
        hs = self.win.winfo_screenheight()
        # 计算 x, y 位置
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)
        self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # 初始化GUI
    def start(self):
        # self.refresh_table()
        self.layout_grid()
        self.win.mainloop()

    # 打开浏览器
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
            self.is_start =True
            # 新增步骤，刷新表格
            self.refresh_table()
            self.window_list.append(self.sfc.get_current_window())
            self.window_jump()
        except:
            tk.messagebox.showerror('错误', '请先打开浏览器')

    # 判断是否要注入录制功能
    def url_is_change(self):
        try:
            self.current_url = self.sfc.get_current_url()
            if self.is_start:
                if self.url != self.current_url:
                    # 如果url改变，表示发生了跳转，需要重新注入JS，则提示用户需要点击注入录制功能，重新采集
                    self.url = self.current_url
                    tk.messagebox.showerror("错误", "页面发生跳转，请先注入录制功能，并重新采集！")
                    return True
                else:
                    # 如果URL没有变，那就直接下一步
                    return False
            else:
                tk.messagebox.showerror("错误", "请先开始录制！")
                return True
        except:
            tk.messagebox.showerror('错误', '请规范操作！')
            return True

    # 新建脚本
    def new_script(self):
        new_win = NewScript(self)
        self.win.wait_window(new_win)
        if self.script_name == '':
            tk.messagebox.showwarning('警告', '请输入有效脚本名')
            return
        else:tk.messagebox.showinfo('成功', '脚本新建成功！')

    # 采集步骤
    def catch_step(self):
        # self.url = self.sfc.get_current_url()
        if self.url_is_change():return
        self.sfc.clear_list()
        step_list = self.sfc.catch_xpath()  # [当前抓取的步骤]
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
                self.new_step(step)
            else:
                self.refresh_frame.append(step['xpath'])
        # 不取消,添加进步骤内，并且更新所在的frame
        if self.is_cancel:
            self.step_list.extend(step_list)
            if len(self.refresh_frame) > 0:
                self.current_frame = self.refresh_frame[-1]
            # 添加步骤刷新表格
            self.refresh_table()
        # 取消
        if self.is_cancel is False:
            self.step_number -= len(step_list)
            # 如果本次采集跳转步骤list长度大于1，那么逆序跳转
            if len(self.refresh_frame) > 1:
                for frame in reversed(self.refresh_frame):
                    self.sfc.switch_win(frame)
            self.sfc.switch_win(self.current_frame)

    # 刷新表格
    def refresh_table(self):
        # 清空表
        for _ in map(self.table.delete, self.table.get_children("")):pass
        # 插入表
        if len(self.step_list) > 0:
            for rw in self.step_list:
                rw['stepNumber'] = self.step_list.index(rw) + 1
                self.table.insert('', rw.get('stepNumber'), values=(
                rw.get('stepNumber'), rw.get('url'), rw.get('actionType'), rw.get('xpath'), rw.get('value'), rw.get('remark')))
        # self.table.after(500, self.refresh_table)
        # 在每次操作后进行刷新。

    # 打开新增步骤的窗口
    def new_step(self, step):
        ns = NewStep(self, step)
        self.win.wait_window(ns)

    # 手动注入js
    def set_js(self):
        try:
            self.sfc.init_iframe()
        except:
            tk.messagebox.showerror('错误', '请规范操作！')

    # 跳转到最新页面（多页面判断）
    def window_jump(self):
        # 获取所有的window
        all_windows = self.sfc.get_all_windows()
        if all_windows:
            for window in all_windows:
                if window not in self.window_list:
                    is_jump = tk.messagebox.askyesno("页面切换", "是否切换到新页面？")
                    if is_jump:
                        # 添加一条切换新页面的步骤。
                        step = {'stepNumber': 1, 'actionType': 'jumpWindow', 'url': '', 'xpath': '', 'value': -1,
                             'remark': '跳转到新页面'}
                        self.step_list.append(step)
                        self.window_list.append(window)
                        # 跳转新页面
                        self.sfc.switch_to_window(step['value'])
        self.win.after(500, self.window_jump)

    # 插入步骤
    def insert_step(self):
        step = self.select_step()
        all_step = self.step_list
        if step:
            # 将self.step_list根据step进行切割
            # if step['']
            index = self.step_list.index(step)
            front_step = all_step[:index]
            back_section_step = all_step[index:]
            # 执行前半段
            execute.ExecuteClass(self, front_step).execute_core()
            # 重新定位到front_step位置。需要调用执行脚本的函数 do_login(front_Step)
            # 9.3继续
            tk.messagebox.showwarning("提醒", "请选择插入的目标元素，并点击采集。")
            # 生成一个空白GUI，有采集按钮，功能和录制此步骤一样 。
            # 9.5继续
            insert_ele = InsertStep(self, front_step, back_section_step)
            self.win.wait_window(insert_ele)

    # 修改更新步骤
    def update_step(self):
        step = self.select_step()
        if step:
            index = self.step_list.index(step)
            ms = MakeStep(self, step)
            self.win.wait_window(ms)
            print(step)
            if self.is_cancel:
                self.step_list[index] = step
                self.refresh_table()

    # 删除步骤
    def del_step(self):
        step = self.select_step()
        if step:
            self.is_cancel = tk.messagebox.askyesno("提醒", "确认删除该步骤吗？")
            if self.is_cancel:
                self.step_list.remove(step)
                self.refresh_table()

    # 选中步骤
    def select_step(self):
        info = self.table.selection()
        if info:
            for item in info:
                data = self.table.item(item, "values")
                # 在这个地方插入
                step = {'stepNumber': int(data[0]), 'actionType': data[2], 'url': data[1], 'xpath': data[3],
                        'value': data[4], 'remark': data[5]}
                return step
        else:
            tk.messagebox.showerror('错误', '请先选择步骤！')
            return False

    # 保存脚本
    def save_script(self):
        if self.script_name is None:
            tk.messagebox.showwarning('警告', '请先新建脚本')
            return
        else:
            try:
                self.insert_script()
                if len(self.step_list) > 0:
                    for step in self.step_list:
                        # 插入数据
                        sql = "INSERT INTO [actionList] (actionid, fatherid, url, actionType, xpath, value, remark) VALUES (" \
                              "'%s', '%s', '%s', '%s', '%s', '%s','%s')" % (self.actionid, step['stepNumber'], step['url'],
                                                                            step['actionType'], step['xpath'], step['value'],
                                                                            step['remark'])
                        self.odb.ExecNonQuery(sql)

                select_sql = "SELECT * FROM [actionList] WHERE actionid = '%s'" % self.actionid
                info = self.odb.ExecQuery(select_sql)
                if info is not None:
                    if len(info) == len(self.step_list):
                        tk.messagebox.showinfo('成功', '脚本保存成功！')
                        # 初始化数据
                        self.init_all()
                        self.refresh_table()
            except:
                tk.messagebox.showerror('失败', '脚本保存失败！')

    # 插入数据表 [action]
    def insert_script(self):

        # 先将脚本插入数据库 action 表内
        sql = "INSERT INTO [action] (ActionName,ActionDesc) VALUES ('%s', '%s')" % (self.script_name, self.script_name)
        self.odb.ExecNonQuery(sql)
        select_sql = "SELECT * FROM [action] WHERE ActionName = '%s'" % self.script_name
        info = self.odb.ExecQuery(select_sql)
        if info is not None:
            self.actionid = info[0][0]
            # tk.messagebox.showinfo('成功', '脚本新建成功，actionid为 %s' % self.actionid)

    def init_all(self):
        # init
        self.script_name = None
        self.step_list = []
        self.url = None
        self.step_number = 0
        self.is_cancel = False
        self.current_frame = '主界面'
        self.refresh_frame = []
        self.actionid = None
        self.current_url = None
        self.is_change = False
        self.is_start = False

    # 脚本坞展示
    def show_script(self):
        select_sql = "SELECT * FROM [action] "
        info = self.odb.ExecQuery(select_sql)
        if info is not None:
            runmain.RunMain(self, info)

if __name__ == '__main__':
    mybox = MyBox()
    mybox.start()