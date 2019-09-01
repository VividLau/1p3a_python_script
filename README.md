# 1p3a_python_script
一亩三分地 Selenium 浏览器自动化脚本

这是一个个人学习项目，使用Selenium的python库实现浏览器的自动化。

# 环境要求

开发环境：macOS Sierra 10.12.6

Python版本：python 3.6

浏览器版本：Chrome 76.0.3809.100

Python依赖库：selenium, pillow, pytesseract

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





