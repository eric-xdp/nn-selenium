#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : execute.py
# @Author: shijiu
# @Date  : 2020/9/4 
# @SoftWare  : PyCharm


class ExecuteClass():

    def __init__(self, parent, step_list):
        self.parent = parent
        self.step_list = step_list
        self.message = None

    def execute_core(self):
        print(self.step_list)
        types = {'wait': self.do_wait, 'find': self.do_find, 'write': self.do_write, 'click': self.do_click,
                 'jump': self.do_jump, 'get': self.do_get, 'jumpWindow': self.do_jump_window}
        for action in self.step_list:
            method = types.get(action['actionType'])  # type = 0 1 2 ...
            if method:
                isgo = method(action)
                if isgo:
                    continue  # 如果返回True, 表示该步骤执行完毕
                else:
                    self.message = '第 %s 步出错。请检查参数。' % (int(action['fatherId']) + 1)
                    break

    def do_wait(self, action):
        print(action)
        print("这是等待步骤")
        self.parent.sfc.is_wait(action['xpath'])
        return True

    def do_find(self, action):
        print(action)
        print("这是查找元素")
        self.parent.sfc.find_ele(action['xpath'])
        return True

    def do_write(self, action):
        print(action)
        print("这是写入数据")
        self.parent.sfc.input_any(action['xpath'], action['value'])
        return True

    def do_click(self, action):
        print(action)
        print("这是点击步骤")
        self.parent.sfc.click_in(action['xpath'])
        return True

    def do_jump(self, action):
        print(action)
        print("这是iframe窗口切换")
        self.parent.current_frame = action['xpath']
        self.parent.sfc.switch_win(action['xpath'])
        return True

    def do_get(self, action):
        print("这是登录")
        self.parent.sfc.get_url(action['url'])
        self.parent.sfc.init_iframe()
        return True

    def do_jump_window(self, action):
        print(action)
        print("跳转页面")
        self.parent.sfc.switch_to_window(action['value'])
        self.parent.sfc.init_iframe()
        return True

