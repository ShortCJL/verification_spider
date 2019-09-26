import time
import base64
from io import BytesIO
from PIL import Image
from selenium import webdriver
# from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from zheye import zheye
from mouse import move,click


# 填写知乎的账号与密码
account = '123456'
password = '123456'

class CrackZhiHu():
    def __init__(self):
        self.url = 'https://www.zhihu.com/'
        # self.browser = webdriver.Chrome()
        options = webdriver.ChromeOptions()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36")
        options.add_experimental_option('excludeSwitches', ['enable-automation'])

        self.browser = webdriver.Chrome(
            executable_path="chromedriver2.exe",
            chrome_options=options)

        self.wait = WebDriverWait(self.browser, 3)

    # 程序完成，自动结束程序
    def __del__(self):
        self.browser.close()
    def get_title_height(self):
        """
                打开网页
                获取标题栏高度
                :return: None
                """
        try:
            self.browser.maximize_window()
        except:
            pass
            #  获取标题栏的高度
        js = 'var allH= window.screen.height;var winH = document.body.clientHeight ;alert(allH+","+winH)'
        self.browser.execute_script(js)
        allH, winH = map(lambda x: int(x) - 10, self.browser.switch_to_alert().text.split(","))
        self.browser.switch_to_alert().accept()
        self.titleH = allH - winH

    def open(self):
        """
        打开网页
        :return: None
        """
        self.browser.get(self.url)


    def login(self):
        '''
        网站登录
        :return:
        '''
        self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            Keys.CONTROL + "a")
        self.browser.find_element_by_css_selector(".SignFlow-accountInput.Input-wrapper input").send_keys(
            account)
        self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(Keys.CONTROL + "a")
        self.browser.find_element_by_css_selector(".SignFlow-password input").send_keys(password)

    def need_login(self):
        """
        是否需要登录
        :return:
        """
        try:
            self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'AppHeader-menu')))
            return False
        except:
            self.browser.find_element_by_css_selector(".SignFlow-tabs .SignFlow-tab:nth-child(2)").click()
            return True

    def whether_verify(self):
        """
        判断是否需要输入验证码
        :return: boolearn：true:需要；false:不需要

        """
        imgStyle = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'SignFlow-captchaContainer'))).get_attribute("style")
        if imgStyle:
            return False
        return True
    def input_verify_code(self):
        """
        输入验证码
        :return: none

        """
        try:
            englishImg = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Captcha-englishImg')))
        except:
            englishImg = None
        try:
            chinaImg =self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'Captcha-chineseImg')))
        except:
            chinaImg = None
        # 如果英文验证码
        if englishImg:
            img = englishImg.get_attribute("src").replace("data:image/jpg;base64,", "").replace("%0A", "")
            if img and img != 'null':
                with open("englishImg.jpeg", "wb") as f:
                    f.write(base64.b64decode(img))
            print("英文的图片验证码")
            #传递给识别函数
            # pass
            #目前就是想进行中文验证码测试
            self.crack()

        # 如果中文验证码
        elif chinaImg:
            print("中文验证码")
            x = chinaImg.location["x"]
            y = chinaImg.location["y"]
            img = chinaImg.get_attribute("src").replace("data:image/jpg;base64,", "").replace("%0A", "")
            if img and img != 'null':
                with open("chinaImg.jpeg", "wb") as f:
                    f.write(base64.b64decode(img))
                z = zheye()
                positions = z.Recognize(BytesIO(base64.b64decode(img)))
                for each in positions:
                    move(each[1] / 2 + x, each[0] / 2 + self.titleH + y-30 )
                    click()
                    time.sleep(3)
    def login_button(self):
        submit_button = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.Button.SignFlow-submitButton')))
        submit_button.click()

    def crack(self):
        """'运行'"""
        try:
            self.open()
            if self.need_login():
                self.login()
                # 判断是否需要输入验证码
                if self.whether_verify():
                    # 需要验证码
                    self.input_verify_code()
                self.login_button()
                time.sleep(3)
                self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'AppHeader-menu')))
                print('验证成功')
        except:
            print('失败，再来一次')
            self.crack()


if __name__ == '__main__':

    crack = CrackZhiHu()
    crack.get_title_height()
    crack.crack()
