import time
import chromedriver_binary
from selenium import webdriver

USER_ID  = "qmcb40im"
PASSWD  = "KANRIKA5433"
MAILADDRESS = "asakura-a@asahi.com"
driver = webdriver.Chrome()
# driver = webdriver.Chrome(executable_path='c:\\Users\\0844278\\AppData\\Local\\SeleniumBasic\\chromedriver.exe')
driver.get('https://www.keicho.net/custom_login.php')
driver.find_element_by_id('id').send_keys(USER_ID)
driver.find_element_by_id("pass").send_keys(PASSWD)
driver.find_element_by_css_selector('p.loginBtn > input[type="image"]').click() # ログインボタン
#member > form > p.loginBtn > input[type="image"]
time.sleep(10)
driver.quit()

# search_box = driver.find_element_by_name("q")
# search_box.send_keys('ChromeDriver')
# search_box.submit()


