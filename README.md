# nn-selenium
自动化项目-自动录制脚本、执行脚本
### 8.19
创建一个初步的GUI，生成两个按钮 （打开浏览器、录制当前网页）

打开浏览器： 初始化selenium,打开浏览器并最大化
录制当前网页：（如何跳转到正确的目标容器 iframe。难点）
  1.注入JS:获取当前网页内的所有iframe,并将所有的iframe的id进行重新赋值 ；给每个元素添加onmouseover事件，通过悬停3秒获取自身全局xpath。
  2.用户将鼠标移动到目标元素进行悬停。将获取xpath后，后台将遍历所有的iframe,查找这个xpath.如果不在当前iframe则跳出该iframe,进入下一个iframe.直至找到该xpath。此时将该iframe的id记录到数据库，新增一条跳转iframe的动作 。
