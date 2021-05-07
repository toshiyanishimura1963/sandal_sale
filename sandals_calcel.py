import time
import os
# import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import configparser

def click_element(element_type, element_name):
    if element_type == 'id':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, element_name)))
        driver.find_element_by_id(element_name).click()
    elif element_type == 'link_text':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, element_name)))
        driver.find_element_by_link_text(element_name).click()
    elif element_type == 'xpath':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, element_name)))
        driver.find_element_by_xpath(element_name).click()
    elif element_type == 'name':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, element_name)))
        driver.find_element_by_name(element_name).click()
    elif element_type == 'css_selector':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, element_name)))
        driver.find_element_by_css_selector(element_name).click()
    elif element_type == 'partial_link_text':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, element_name)))
        driver.find_element_by_partial_link_text(element_name).click()
    else:
        print("click_element error")
        exit()

def sendkeys_element(element_type, element_name, send_strings):
    if element_type == 'id':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, element_name)))
        driver.find_element_by_id(element_name).send_keys(send_strings)
    elif element_type == 'link_text':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.LINK_TEXT, element_name)))
        driver.find_element_by_link_text(element_name).send_keys(send_strings)
    elif element_type == 'xpath':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, element_name)))
        driver.find_element_by_xpath(element_name).send_keys(send_strings)
    elif element_type == 'name':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, element_name)))
        driver.find_element_by_name(element_name).send_keys(send_strings)
    elif element_type == 'css_selector':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_name)))
        driver.find_element_by_css_selector(
            element_name).send_keys(send_strings)
    else:
        print("sendkeys_element error")
        exit()


userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
os.makedirs(userdata_dir, exist_ok=True)
cwdpath = os.getcwd()
options = webdriver.ChromeOptions()
options.add_argument('--user-data-dir=' + cwdpath + "/" + userdata_dir)
driver = webdriver.Chrome(options=options)

# 一度設定すると find_element 等の処理時に、
# 要素が見つかるまで指定時間繰り返し探索するようになります。
driver.implicitly_wait(20)  # 秒

driver.get("https://auctions.yahoo.co.jp")
input('ログイン後、マイオクのリンクが表示されるまで進んだあとに、エンターで再開 : ')
click_element('link_text', 'マイオク')
time.sleep(1)
click_element('link_text', '出品中')
time.sleep(1)

# ダイアログの問い合わせステータス
display_dialog1 = "yes"
links = []
links = driver.find_elements_by_partial_link_text("布ぞうり")
print('布ぞうりの数 = ', len(links))
for webitem in links:
    time.sleep(1)
    click_element('partial_link_text', '布ぞうり')
    time.sleep(1)
    click_element('link_text', 'オークションの取り消し')
    time.sleep(1)
    click_element('id', 'confirm')
    time.sleep(1)
    click_element('link_text', 'マイオク')
    click_element('link_text', '出品中')

driver.quit()
