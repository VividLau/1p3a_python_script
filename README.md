# 1p3a_python_script
一亩三分地 Selenium 浏览器自动化脚本

这是一个个人学习项目，使用Selenium的python库实现浏览器的自动化。









# 环境要求

开发环境：macOS Sierra 10.12.6

Python版本：python 3.6

浏览器版本：Chrome 76.0.3809.100

Python依赖库：selenium, pillow, pytesseract



# 功能
* 自动登录
* 自动签到
* 自动答题



# 使用方法

### 在使用前，确保安装了 Chrome webdriver 并将其添加到系统路径下：

* 前往Chrome浏览器官方驱动下载网址 https://chromedriver.chromium.org/downloads 选择对应版本下载并解压
* 打开 terminal, 前往根目录： `cd ~`
* 编辑 .bash_profile文件，不同操作系统下, 配置环境的文件名可能不同，可能是 `.profile` 或 `.bashrc` 或 `.bash_profile` , 可先分别 `cat 文件名` 来确认正确文件
* 假设chrome driver的安装路径是 `/Users/usrname/Desktop/webauto/driver/` 注意，路径的最后一级仍然是文件夹而不是驱动文件 
* 运行命令：`echo 'export PATH=${PATH}:/Users/usrname/Desktop/webauto/driver/' >> .bash_profile`
* 运行命令 `source .bash_profile`

### 确保安装 tesseract
* 运行 `brew install tesseract`

### 确保安装 python 依赖库
* 使用 `pip` 或者 `pip3`：`pip install pytesseract selenium pillow`

### 修改配置文件
* 在 `usrname` 文件中加入一亩三分地账号名和密码 形式：`username:yourusrname`
* 可以自行扩展题库文件`question_list`，也可以以issue的形式提交到此repo

### 运行脚本
* clone this repo and cd to it
* run `python 1p3.py` or `python3 1p3.py`



# 验证码处理逻辑
### 使用开源OCR库tesseract，将图片验证码转化为字符串
* 图片预处理，将彩色图片转化为黑白，并去除干扰

![Image text](https://github.com/VividLau/1p3a_python_script/blob/master/image/img1.png)
![Image text](https://github.com/VividLau/1p3a_python_script/blob/master/image/phase2_img1.png)

![Image text](https://github.com/VividLau/1p3a_python_script/blob/master/image/img2.png)
![Image text](https://github.com/VividLau/1p3a_python_script/blob/master/image/phase2_img2.png)

![Image text](https://github.com/VividLau/1p3a_python_script/blob/master/image/img3.png)
![Image text](https://github.com/VividLau/1p3a_python_script/blob/master/image/phase2_img3.png)

* 图片切割，将图片按字符切割为四张小图片，使tesseract识别准确度提高
* **仅适用于此种类型的图形验证码！**




# TO DO
* 更新题库
* 添加 遇到新题自动更新题库 功能 
* find better way to wait fully loaded image, instead of using sleep() 



# LICENSE
DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE





