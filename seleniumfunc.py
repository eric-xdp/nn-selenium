#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : seleniumfunc.py
# @Author: shijiu
# @Date  : 2020/8/7 
# @SoftWare  : PyCharm

import time
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

class WebDriver():

    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('chromedriver.exe')
        self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser.maximize_window()
        self.browser.implicitly_wait(3)
        self.get_iframe()

    # 加载页面
    def get_url(self,url):
        try:self.browser.get(url); return True
        except: return False

    # 隐式等待
    def is_wait(self, xpath):
        WebDriverWait(self.browser, 3000).until(lambda the_driver: the_driver.find_element_by_xpath(xpath).is_displayed())

    def is_sleep(self):
        time.sleep(3)

    # 获取页面iframe ,自定义id,返回ID列表 。存表数据 指定iframe 的id
    def get_iframe(self):
        iframe = """
                    var arr1 = []
                    var iframes1= document.getElementsByTagName("iframe"); 
                    var iframes2= document.getElementsByTagName("frame"); 
                    for(var i=0;i<iframes1.length;i++) { 
                		iframes1[i].style.overflow = "visible";
                		iframes1[i].setAttribute("id", "iframe1"+ i);
                        arr1.push(iframes1[i].id)
                    }
                    for(var i=0;i<iframes2.length;i++) { 
                		iframes2[i].style.overflow = "visible";
                		iframes2[i].setAttribute("id", "iframe2"+ i);
                        arr1.push(iframes2[i].id)
                    }
                    return arr1 
                """
        iframe_id_list = self.browser.execute_script(iframe)
        iframe_id_list.append("主界面")
        return iframe_id_list


    # 检查页面元素id是否存在
    def test_id_Valid(self, name):
        try:self.browser.find_element_by_id(name); self.browser.execute_script("window.stop()"); return True
        except:return False

    # 检查页面元素Class是否存在
    def test_class_Valid(self, name):
        try: e = self.browser.find_elements_by_class_name(name); self.browser.execute_script("window.stop()"); return len(e) > 0
        except: return False

    # 跳转到指定容器，需要参数 容器xpath。 type: jump
    def switch_win(self, frame):
        # 先自定义iframeID,
        # iframe = """
        #                         var arr1 = []
        #                         var iframes1= document.getElementsByTagName("iframe");
        #                         var iframes2= document.getElementsByTagName("frame");
        #                         for(var i=0;i<iframes1.length;i++) {
        #                     		iframes1[i].style.overflow = "visible";
        #                     		iframes1[i].setAttribute("id", "iframe1"+ i);
        #                             arr1.push(iframes1[i].id)
        #                         }
        #                         for(var i=0;i<iframes2.length;i++) {
        #                     		iframes2[i].style.overflow = "visible";
        #                     		iframes2[i].setAttribute("id", "iframe2"+ i);
        #                             arr1.push(iframes2[i].id)
        #                         }
        #                         return arr1
        #                     """
        # try:
        #     self.browser.execute_script(iframe);self.browser.switch_to.frame(frame_id);return True
        # except:
        #     return False
        try:
            iframe = self.browser.find_element_by_xpath(frame)
            self.browser.switch_to.frame(iframe)
            return True
        except: return False

    # 写入数据 find and input
    def input_any(self, xpath, anything):
        try:
            inp = self.browser.find_element_by_xpath(xpath)
            inp.send_keys(anything)
            return True
        except:return False

    # 找到元素,返回元素 find
    def find_ele(self, xpath):
        try:
            ele = self.browser.find_element_by_xpath(xpath)
            return ele
        except: return False

    # 按钮、超链 点击 click
    def click_in(self, xpath):
        try: self.browser.find_element_by_xpath(xpath).click(); return True
        except:return False

        # 通过class 获取元素text
    def judge_text(self, xpath):
        try:
            etext = self.browser.find_element_by_class_name(xpath).text
            return etext
        except: return False

