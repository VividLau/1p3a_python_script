from time import sleep
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common import exceptions as selexception
from PIL import Image
import captcha

def login(browser, wait):

    print("从配置文件中获取用户名和密码...")
    usr_pwd = {}

    with open("usrname") as config:
        for line in config:
            key, val = line.rstrip().split(":")
            usr_pwd[key] = val 
    
    usr_name = usr_pwd["username"]
    password = usr_pwd["password"]

    print("开始登录一亩三分地")

    # 登录
    wait.until(ec.presence_of_element_located((By.XPATH, "//em[text()='登录']")))
    usr_name_element = browser.find_element_by_css_selector("input[id='ls_username']")
    usr_name_element.send_keys(usr_name)

    pwd_element = browser.find_element_by_css_selector("input[id='ls_password']")
    pwd_element.send_keys(password)

    login_btn_element = browser.find_element_by_xpath("//em[text()='登录']")
    login_btn_element.click()
    wait.until(ec.presence_of_element_located((By.XPATH, '//a[text()="退出"]')))

    print("登录成功！\n=========================")

def daily_check_in(browser, wait):

    print("开始每日签到")

    try:
        # 每日签到
        check_element = browser.find_element_by_xpath("//font[text()='签到领奖!']")
        check_element.click()

        # 自动选择表情：“开心”
        wait.until(ec.presence_of_element_located((By.XPATH, '//li[@id="kx"]')))
        happy_element = browser.find_element_by_css_selector("li[id='kx']")
        happy_element.click()

        # 使用快速选择留言
        say_element = browser.find_element_by_xpath("//input[@name='qdmode'][@value='2']")
        say_element.click()

        # 点击签到
        check_btn_element = browser.find_element_by_xpath("//strong[text()='点我签到!']/..")
        check_btn_element.click()

        # 等待签到框消失
        wait.until(ec.invisibility_of_element_located((By.XPATH, "//div[@id='fwin_dsu_paulsign']")))

        # 等待 “签到领奖！” 链接消失
        wait.until(ec.invisibility_of_element_located((By.XPATH, "//font[text()='签到领奖!']")))

        print("签到完成，大米+1 \n=========================")
        return 1

    except selexception.NoSuchElementException:
        print("今天已经签过啦！！\n=========================")
        return 0

def get_answer(question):

    # 检查题库
    print(f"开始检索题库, 题目: {question}")
    answer = ""
    with open("question_list") as q_list:
        for line in q_list:
            q, answer = line.rstrip().split(":")
            if q == question:
                print(f"答案: {answer}")
                break
    return answer

def daily_question(browser, wait):

    print("开始每日答题")

    try:
        browser.find_element_by_xpath("//img[@src='source/plugin/ahome_dayquestion/images/end.gif']")
        print("今天已经回答过啦！!\n=========================")
        return 
    except selexception.NoSuchElementException:
        pass
    
    # 等待 “开始答题” 或者 ”答题中“ 图标
    two_icons = "img[src='source/plugin/ahome_dayquestion/images/ing.gif'], img[src='source/plugin/ahome_dayquestion/images/begin.gif']"
    wait.until(ec.visibility_of_element_located((By.CSS_SELECTOR, two_icons)))

    # 每日答题
    daily_q_element = browser.find_element_by_xpath("//img[@src='source/plugin/ahome_dayquestion/images/ing.gif']/..")
    daily_q_element.click()

    # 填写验证码
    fill_captcha(browser, wait)

    # 获取问题和答案
    question = browser.find_element_by_xpath("//b[text()='【题目】']/..").text[5:]
    answer = get_answer(question)

    if answer == "":
        print("今日问题未被收录入题库，跳过每日问答")
        return

    # 提交答案
    choose_btn = browser.find_element_by_xpath(f"//div[text()='  {answer}']/input")
    choose_btn.click()

    ans_btn = browser.find_element_by_xpath("//button[@name='submit'][@type='submit']")
    ans_btn.click()
    print("完成每日问答，大米+1\n=========================")

def fill_captcha(browser, wait):

    res_text = ""
    correct_res = "https://www.1point3acres.com/bbs/static/image/common/check_right.gif"
    wrong_res = "https://www.1point3acres.com/bbs/static/image/common/check_error.gif"

    wait.until(ec.visibility_of_element_located((By.XPATH, "//input[@name='seccodeverify']")))
    cap_input_element = browser.find_element_by_xpath("//input[@name='seccodeverify']")
    trial = 1

    while res_text == "" or res_text == wrong_res: # 验证码解码错误

        print(f"开始破解图形验证码，第次{trial}尝试...")
        # 重新获取验证码
        wait.until(ec.visibility_of_element_located((By.XPATH, "//a[text()='换一个']")))
        get_new_captcha = browser.find_element_by_xpath("//a[text()='换一个']")
        get_new_captcha.click()
        wait.until(ec.visibility_of_element_located((By.XPATH, "//span[text()='输入下图中的字符']//img")))
        sleep(1)

        captcha_img_element = browser.find_element_by_xpath("//span[text()='输入下图中的字符']//img")

        loc = captcha_img_element.location
        size = captcha_img_element.size

        left, right = loc['x'], loc['x'] + size['width']
        top, bottom = loc['y'], loc['y'] + size['height']

        browser.save_screenshot('screenshot.png')
        scrsht = Image.open("screenshot.png")
        captcha_img = scrsht.crop((left, top, right, bottom))
        captcha_img.save("catpcha.png")

        # 解码验证码，转化为字符串
        captcha_text = captcha.captcha_to_string(Image.open("catpcha.png"))
        print(f"图形验证码破解结果: {captcha_text}")

        cap_input_element.send_keys(captcha_text)

        # 选择答案以激活正确或错误图标
        answer_element = browser.find_element_by_xpath("//input[@name='answer'][@value='1']")
        answer_element.click()

        # 等待错误或正确图标出现，为的是检验刚才输入的验证码是否正确
        wait.until(
            ec.presence_of_element_located((By.CSS_SELECTOR, "img[src='static/image/common/check_right.gif'], img[src='static/image/common/check_error.gif']")) 
        )

        check_image_element = browser.find_element_by_xpath("//span[@id='checkseccodeverify_SA00']//img")
        res_text = check_image_element.get_attribute("src")

        if res_text == correct_res:
            print("验证码输入正确 ^_^ ")
        else:
            print("验证码输入错误！")
            trial += 1


"""
========================= START =============================
"""

print("""
 __      __   _                  
 \ \    / /__| |__ ___ _ __  ___ 
  \ \/\/ / -_) / _/ _ \ '  \/ -_)
   \_/\_/\___|_\__\___/_|_|_\___|
        """
)

# 初始化 webdriver, 使用chrome浏览器
# 设置为执行操作时，不需要等待页面完全加载
caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"
browser = Chrome(desired_capabilities=caps)
browser.get("https://www.1point3acres.com/bbs/")
wait = WebDriverWait(browser, 10)

# 执行登录，在做任何其他操作前必须先登录
login(browser, wait)

# 每日签到
daily_check_in(browser, wait)

# 每日答题
daily_question(browser, wait)

# # 测试: 每日回答错误
# test_bro = Chrome()
# test_bro.get("https://www.1point3acres.com/bbs/plugin.php?id=ahome_dayquestion:pop")
# wait = WebDriverWait(test_bro, 10)
# login(test_bro, wait)
# text = test_bro.find_element_by_xpath("//body[@id='nv_plugin']/div[@id='wp']/div[@id='ct']/div[@class='nfl']/div/div/p[not(@class)]")
# print(text.text)

print(
"""
  ___       _          
 | __|_ _  (_)___ _  _ 
 | _|| ' \ | / _ \ || |
 |___|_||_|/ \___/\_, |
         |__/     |__/ 
"""
)
