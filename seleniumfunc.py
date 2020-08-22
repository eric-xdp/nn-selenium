#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : seleniumfunc.py
# @Author: shijiu
# @Date  : 2020/8/7 
# @SoftWare  : PyCharm

import time
import json
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
        self.step_list = []
    # 加载页面
    def get_url(self,url):
        try:self.browser.get(url); return True
        except: return False

    # 获取当前网址
    def get_current_url(self): return self.browser.current_url

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

    def check_id_exist(self,xpath):
        try:
            element = self.browser.find_element_by_xpath(xpath)
            e_id = element.get_attribute('id')
            return e_id
        except:
            return False

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
            # 将跳转步骤插入入数据库
            # sql = "SELECT * FROM [actionList] WHERE actionid = '%s';" % action_id
            # sql = "INSERT INTO [actionList] (actionid,fatherid,actionType,xpath,remark) VALUES ('%s', '%s', '%s', '%s', '%s')" %()
            # info = self.odb.ExecQuery(sql)
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


    # 初始化iframe id ，并把获取xpath的js注入到每个容器中。
    def init_iframe(self):
        init_iframe = """
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
        iframe_id_list = self.browser.execute_script(init_iframe)
        self.get_xpath()
        for iframe in iframe_id_list:
            self.browser.switch_to.frame(iframe)
            self.get_xpath()
            self.browser.switch_to.default_content()
        # 返回原来的iframe


    # 注入获取目标元素xpath的js
    def get_xpath(self):
        js = """
            var arr = [];
    		var result = []
    		var textarea = document.createElement("textarea");
    		textarea.setAttribute("id", "textarea_result"); 
    		document.body.appendChild(textarea); 
    		var tags = document.getElementsByTagName('*')
    		var text11 = document.getElementById('textarea_result');

    		var tips = document.createElement("p");
    		tips.setAttribute("id", "tips_result"); 
    		tips.setAttribute("title", "tips_result"); 
    		document.body.appendChild(tips); 
    		tips.style.position = "absolute";
    		tips.style.backgroundColor="yellow"
    		tips.style.zIndex = "999"
    		tips.style.display = "none"
    		tips.style.width = "500px"
    		tips.style.height = "50px"
    		tips.style.border = "black 1px solid"

    		console.log(text11)
    		console.log(tags)
    		for (var i = 0; i < tags.length; i++) {
    			if (tags[i].tagName === "HTML" || tags[i].tagName === "SCRIPT" || tags[i].tagName === "SCRIPT" || tags[i].tagName === "STYLE") {
    				continue
    			} else {
    				arr.push(tags[i])
    			}
    		}
    		var elementList = arr
    			// 给元素添加事件
    		var getXpath = function (element) {

    			//这里需要需要主要字符串转译问题，可参考js 动态生成html时字符串和变量转译（注意引号的作用）
    			if (element === document.body) {//递归到body处，结束递归
    				xPath = '/html/' + element.tagName.toLowerCase()
    				return xPath;
    			}
    			let ix = 1;//
    			let siblings = element.parentNode.childNodes;//ͬ
    			for (let i = 0, l = siblings.length; i < l; i++) {
    				let sibling = siblings[i];
    				if (sibling == element) {
    					return getXpath(element.parentNode) + '/' + element.tagName.toLowerCase() + '[' + (ix) + ']';
    				} else if (sibling.nodeType == 1 && sibling.tagName == element.tagName) {
    					ix++;
    				}
    			}
    		}

    		for (var i = 0; i < elementList.length; i++) {
    			let element = elementList[i] 
    			const res = {xPath:"",content:""}
    			elementList[i].onmouseover = function (event) {
    				event.stopPropagation()
    				element.style.border = "1px solid blue"
    				var xPath ;
    				toRun = setTimeout(function () {
    					console.log(element)
    					res.content = ""
    					if (element.tagName == "INPUT" || element.tagName == "TEXTAREA"){
    					    res.content = element.value
    					}else {
    				        res.content = element.innerText
    					}
    					res.xPath = getXpath(element)
    					result.push(res)
    					console.log(JSON.stringify(result))
    					text11.value = JSON.stringify(result);
    					element.title = JSON.stringify(res);
    					tips.innerText = JSON.stringify(res)
    					var x = event.clientX + document.body.scrollLeft + 20;
    					var y = event.clientY + document.body.scrollTop - 5; 
    					tips.style.left = x + "px";
    					tips.style.top = y + "px";
    					tips.style.display = "block";
    					return result
    				}, 3000)
    				element.style.border = "1px solid blue"
    				console.log("移入")
    			}
    			elementList[i].onmouseout = function (event) {
    				clearTime = clearTimeout(toRun)
    				tips.style.display = "none";
    				console.log("移出")
    				element.style.border = "1px solid rgba(0,0,0,0)"
    			}
    		}
    """
        self.browser.execute_script(js)
    # 获取采集到的xpath

    def clear_list(self):
        self.step_list.clear()

    # 每次采集xpath值前进行所在容器判断。判断后生成步骤。
    def catch_xpath(self):
        step_info = {'stepNumber': 1, 'actionType': '', 'url': '', 'xpath': '', 'value': '', 'remark': ''}
        result_js = """
                            var xpathResult = document.getElementById('textarea_result');
                            console.log(xpathResult)
                            var result = xpathResult.value
                            xpathResult.value = ""
                            return result
                        """
        result = self.browser.execute_script(result_js)
        # 如果是空，那么表示采集的数据不在这个容器内(或者用户没有选择目标元素)，先跳转到主界面
        if result == '':
            self.browser.switch_to.default_content()
            step_info['actionType'] = 'jump'
            step_info['xpath'] = '主界面'
            step_info['remark'] = '检测到目标元素不处于当前容器，跳转到目标容器，并新增跳转步骤。'
            self.step_list.append(step_info)
            return self.catch_xpath()

        result = json.loads(result)
        step_info['xpath'] = result[-1]['xPath']
        # 查询xpath是否能找到元素。
        if self.find_ele(result[-1]['xPath']) is False:
            self.browser.switch_to.default_content()

        if 'frame' in result[-1]['xPath']:
            #  如果跳转成功，要将跳转步骤插入数据库中。该步骤会展示给录制用户
            if self.switch_win(result[-1]['xPath']):
                # 插入数据
                # sql = "INSERT INTO [actionList] (actionid,fatherid,actionType,xpath,remark) VALUES ('%s', '%s', '%s', '%s', '%s')" %()
                # info = self.odb.ExecQuery(sql)
                step_info['actionType'] = 'jump'
                step_info['remark'] = '检测到目标元素不处于当前容器，跳转到目标容器，并新增跳转步骤。'
                self.step_list.append(step_info)
                return self.catch_xpath()
        else:
            self.step_list.append(step_info)
            return self.step_list

    # 通过xpath给元素设置属性
    def set_element_attribute(self, info):
        js = """
        var ele = document.evaluate('{}',document).iterateNext();
        console.log(ele);
        if(ele) {{
            ele.setAttribute('{}','{}');
            return true
        }};
        return false
        """.format(info['xpath'], info['name'], info['value'])
        done = self.browser.execute_script(js)
        if done: return info
        else:return done


    # 通过id给标签画框
    def add_style_border(self,id):
        js = """document.getElementById('{}').style.border="3px solid red";""".format(id)
        self.browser.execute_script(js)

    # 通过id移除添加的样式
    def remove_style(self,id):
        js = """document.getElementById('{}').style="";""".format(id)
        self.browser.execute_script(js)
