import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import configparser

inifile = configparser.ConfigParser()
inifile.read('./sandals.ini', 'UTF-8')
USER_ID = inifile.get('設定', 'ユーザーID')
PASSWD = inifile.get('設定', 'パスワード')
debug_on = inifile.get('設定', 'debug') == "ON"

driver = webdriver.Chrome()
# 一度設定すると find_element 等の処理時に、
# 要素が見つかるまで指定時間繰り返し探索するようになります。
driver.implicitly_wait(20)  # 秒

driver.get("https://auctions.yahoo.co.jp")

if len(driver.find_elements_by_link_text("ログイン")) > 0:
    driver.find_element_by_link_text("ログイン").click()
    time.sleep(1)
    driver.find_element_by_id('username').send_keys(USER_ID)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.ID, "btnNext")))
    driver.find_element_by_id("btnNext").click()
    time.sleep(1)
    driver.find_element_by_id("passwd").send_keys(PASSWD)
if not driver.find_element_by_id("persistent").is_selected():
        driver.find_element_by_id("persistent").click()
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.ID, "btnSubmit")))
driver.find_element_by_id("btnSubmit").click()
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "マイオク")))
driver.find_element_by_link_text("マイオク").click()
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "出品中")))
driver.find_element_by_link_text("出品中").click()
time.sleep(1)

# ダイアログの問い合わせステータス
display_dialog1 = "yes"
links = []
links = driver.find_elements_by_partial_link_text("布ぞうり")
print('布ぞうりの数 = ', len(links))
for webitem in links:
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "布ぞうり")))
    driver.find_element_by_partial_link_text("布ぞうり").click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "オークションの取り消し")))
    driver.find_element_by_link_text('オークションの取り消し').click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.NAME, "confirm")))
    driver.find_element_by_name('confirm').click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "マイオク")))
    driver.find_element_by_link_text("マイオク").click()
    time.sleep(1)
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "出品中")))
    driver.find_element_by_link_text("出品中").click()

driver.quit()
