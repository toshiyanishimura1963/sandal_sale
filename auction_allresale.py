import time
import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
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


inifile = configparser.ConfigParser()
inifile.read('./sandals.ini', 'UTF-8')
price = inifile.get('設定', '価格')
postage = inifile.get('設定', '送料')
description = inifile.get('設定', '商品説明')
USER_ID = inifile.get('設定', 'ユーザーID')
PASSWD = inifile.get('設定', 'パスワード')
debug_on = inifile.get('設定', 'debug') == "ON"

# Shohin = input('再出品する商品タイトルの一部を入力してください: ')

driver = webdriver.Chrome()
# 一度設定すると find_element 等の処理時に、
# 要素が見つかるまで指定時間繰り返し探索するようになります。
driver.implicitly_wait(20)  # 秒
driver.get("https://auctions.yahoo.co.jp")

# # 不要なダイアログが表示されたときは閉じる
# if driver.find_elements_by_id('js-prMdl-sbym'):
#     if "display: block" in driver.find_element_by_id('js-prMdl-sbym').get_attribute("style"):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         driver.find_element_by_class_name('prMdl__close').click()

# if len(driver.find_elements_by_link_text("ログイン")) > 0:
#     click_element("link_text", "ログイン")
#     sendkeys_element("id", "username", USER_ID)
#     click_element("id", "btnNext")
#     sendkeys_element("id", "passwd", PASSWD)
# if not driver.find_element_by_id("persistent").is_selected():
#     click_element("id", "persistent")
# click_element("id", "btnSubmit")
# if len(driver.find_elements_by_link_text("ご利用中のサービスに戻る")) > 0:
#     click_element("link_text", "ご利用中のサービスに戻る")

# # 不要なダイアログが表示されたときは閉じる
# if driver.find_elements_by_id('js-prMdl'):
#     if "display: block" in driver.find_element_by_id('js-prMdl').get_attribute("style"):
#         driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#         driver.find_element_by_id('js-prMdl-close').click()

input('ログイン後、マイオクのリンクが表示されるまで進んだあとに、エンターで再開 : ')
click_element('link_text', 'マイオク')
click_element('link_text', '出品終了分')
click_element('link_text', '落札者なし')

# ダイアログの問い合わせステータス
display_dialog1 = "yes"
WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, '落札者あり')))
while len(driver.find_elements_by_xpath("//img[@alt='再出品']")) > 0:
    print("再出品する商品の数: " + str(len(driver.find_elements_by_xpath("//img[@alt='再出品']"))))
    # 不要なダイアログの対応 落札者なしのリスト
    if len(driver.find_elements_by_class_name('closeBtn')) > 0:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")  # スクロールして、ダイアログを表示
        # ダイアログの表示で変更になる部分 ダイアログは最初だけ表示されるので、それ以降は処理しない
        if display_dialog1 == "yes" and input('ダイアログは表示されていますか？ y/n? >> ') == 'y':
            display_dialog1 = "no"
            driver.find_element_by_class_name('closeBtn').click()
    click_element('xpath', "//img[@alt='再出品']")

    # 値下げ交渉はしないので、値下げ交渉のチェックを外す
    if 'is-check' in driver.find_element_by_xpath('//*[@id="price_buynow"]/div[3]/label').get_attribute('class'):
        print('値引き交渉するのチェックを外す')
        click_element("xpath",
                      '//*[@id="price_buynow"]/div[3]/label/span[1]')

    # 終了日を入力
    Select(driver.find_element_by_name("ClosingYMD")).select_by_index(6)
    print("終了日を入力")

    # '出品するボタン
    if debug_on:
        input('入力待ち >>')
    click_element("css_selector", '.Inquiry__button')
    print("確認ボタン")
    click_element("id", 'auc_preview_submit_up')
    print("出品ボタン")

    # 出品後に不要なダイアログが表示されたときは閉じる
    time.sleep(10)
    # 名前とプロフィール画像を‥
    if driver.find_elements_by_xpath('//*[@id = "yaucSellItemCmplt"]/div[10]'):
        if "display: block" in driver.find_element_by_xpath('//*[@id = "yaucSellItemCmplt"]/div[10]').get_attribute("style"):
            click_element(
                "xpath", '//*[@id = "yaucSellItemCmplt"]/div[10]/div/div/div/a[2]')
    # 支払いを直接‥
    if driver.find_elements_by_xpath('//*[@id="yaucSellItemCmplt"]/div[11]'):
        if "display: block" in driver.find_element_by_xpath('//*[@id="yaucSellItemCmplt"]/div[11]').get_attribute("style"):
            click_element("link_text", 'とじる')

    click_element('link_text', 'マイオク')
    click_element('link_text', '出品終了分')
    click_element('link_text', '落札者なし')
    WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.LINK_TEXT, '落札者あり')))

driver.quit()
exit
