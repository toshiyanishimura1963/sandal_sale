import time
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service
import configparser
import warnings
warnings.filterwarnings('ignore')


def click_element(element_type, element_name):
    if element_type == 'id':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.ID, element_name)))
        driver.find_element(By.ID, element_name).click()
    elif element_type == 'link_text':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, element_name)))
        driver.find_element(By.LINK_TEXT, element_name).click()
    elif element_type == 'xpath':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, element_name)))
        driver.find_element(By.XPATH, element_name).click()
    elif element_type == 'name':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.NAME, element_name)))
        driver.find_element(By.NAME, element_name).click()
    elif element_type == 'css_selector':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, element_name)))
        driver.find_element(By.CSS_SELECTOR, element_name).click()
    elif element_type == 'partial_link_text':
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, element_name)))
        driver.find_element(By.PARTIAL_LINK_TEXT, element_name).click()
    else:
        print("click_element error")
        exit()


def sendkeys_element(element_type, element_name, send_strings):
    if element_type == 'id':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, element_name)))
        driver.find_element(By.ID, element_name).send_keys(send_strings)
    elif element_type == 'link_text':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.LINK_TEXT, element_name)))
        driver.find_element(By.LINK_TEXT, element_name).send_keys(send_strings)
    elif element_type == 'xpath':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, element_name)))
        driver.find_element(By.XPATH, element_name).send_keys(send_strings)
    elif element_type == 'name':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, element_name)))
        driver.find_element(By.NAME, element_name).send_keys(send_strings)
    elif element_type == 'css_selector':
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, element_name)))
        driver.find_element(By.CSS_SELECTOR, 
            element_name).send_keys(send_strings)
    else:
        print("sendkeys_element error")
        exit()


inifile = configparser.ConfigParser()
inifile.read('./sandals.ini', 'UTF-8')
postage = inifile.get('設定', '送料')
endday = inifile.get('設定', '終了日')
description = inifile.get('設定', '商品説明')
USER_ID = inifile.get('設定', 'ユーザーID')
PASSWD = inifile.get('設定', 'パスワード')
debug_on = inifile.get('設定', 'debug') == "ON"

userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
os.makedirs(userdata_dir, exist_ok=True)
cwdpath = os.getcwd()
options = webdriver.chrome.options.Options()
options.add_argument('--user-data-dir=' + cwdpath + "\\" + userdata_dir)
options.add_argument('--profile-directory=Profile 1')
# driver = webdriver.Chrome(options=options)
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

# driver = webdriver.Chrome()
# 一度設定すると find_element 等の処理時に、
# 要素が見つかるまで指定時間繰り返し探索するようになります。
driver.implicitly_wait(20)  # 秒
time.sleep(7)
driver.get("https://auctions.yahoo.co.jp/")

input('ログイン後、マイオクのリンクが表示されるまで進んだあとに、エンターで再開 : ')
click_element('link_text', 'マイオク')
click_element('link_text', '出品終了分')
click_element('link_text', '落札者なし')

# ダイアログの問い合わせステータス
display_dialog1 = "yes"
WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, '落札者あり')))
while len(driver.find_elements(By.XPATH, "//img[@alt='再出品']")) > 0:
    print("再出品する商品の数: " + str(len(driver.find_elements(By.XPATH, "//img[@alt='再出品']"))))
    # 不要なダイアログの対応 落札者なしのリスト
    if len(driver.find_elements(By.CLASS_NAME, 'closeBtn')) > 0:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")  # スクロールして、ダイアログを表示
        # ダイアログの表示で変更になる部分 ダイアログは最初だけ表示されるので、それ以降は処理しない
        if display_dialog1 == "yes" and input('ダイアログは表示されていますか？ y/n? >> ') == 'y':
            display_dialog1 = "no"
            driver.find_element(By.CLASS_NAME,'closeBtn').click()
    click_element('xpath', "//img[@alt='再出品']")

    time.sleep(1)
    if len(driver.find_elements(By.XPATH, '//*[@id="js-ListingModal"]')):
        if 'is-show' in driver.find_element(By.XPATH, '//*[@id="js-ListingModal"]').get_attribute('class'):
            print('ヤフネコダイアログのクローズ')
            click_element("css_selector",
                          '.CrossListingModal__exhibitButton')

    # 終了日を入力
    Select(driver.find_element(By.NAME, "ClosingYMD")).select_by_index(endday)
    print("終了日を入力")

    # '出品するボタン
    if debug_on:
        input('入力待ち >>')
    click_element("css_selector", '.Inquiry__button')
    print("確認ボタン")
    click_element("id", 'auc_preview_submit_up')
    print("出品ボタン")

    # 出品後に不要なダイアログが表示されたときは閉じる
    time.sleep(2)
    # 名前とプロフィール画像を‥
    if len(driver.find_elements(By.XPATH ,'//*[@id = "yaucSellItemCmplt"]/div[10]')):
        if "display: block" in driver.find_element(By.XPATH, '//*[@id = "yaucSellItemCmplt"]/div[10]').get_attribute("style"):
            click_element(
                "xpath", '//*[@id = "yaucSellItemCmplt"]/div[10]/div/div/div/a[2]')
    # 支払いを直接‥
    if len(driver.find_elements(By.XPATH, '//*[@id="yaucSellItemCmplt"]/div[11]')):
        if "display: block" in driver.find_element(By.XPATH, '//*[@id="yaucSellItemCmplt"]/div[11]').get_attribute("style"):
            click_element("link_text", 'とじる')

    click_element('link_text', '落札されなかったオークション')

driver.quit()
exit
