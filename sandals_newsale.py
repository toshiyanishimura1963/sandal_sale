import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service
import configparser


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
price = inifile.get('設定', '価格')
postage = inifile.get('設定', '送料')
description = inifile.get('設定', '商品説明')
USER_ID = inifile.get('設定', 'ユーザーID')
PASSWD = inifile.get('設定', 'パスワード')
folder_name = inifile.get('設定', '画像フォルダ')
total = inifile.get('出品', '出品数')
start_no = inifile.get('出品', '開始番号')
debug_on = inifile.get('設定', 'debug') == "ON"

userdata_dir = 'UserData'  # カレントディレクトリの直下に作る場合
os.makedirs(userdata_dir, exist_ok=True)
cwdpath = os.getcwd()
options = webdriver.chrome.options.Options()
options.add_argument('--user-data-dir=' + cwdpath + "\\" + userdata_dir)
options.add_argument('--profile-directory=Profile 1')
driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome()
# C:\Users\0844278\AppData\Local\Programs\Python\Python38-32\chromedriver.exe
# 一度設定すると find_element 等の処理時に、
# 要素が見つかるまで指定時間繰り返し探索するようになります。
driver.implicitly_wait(20)  # 秒
time.sleep(5)
driver.get("https://auctions.yahoo.co.jp")

input('ログイン後、出品のリンクが表示されるまで進んだあとに、エンターで再開 : ')
click_element("link_text", "出品")

# ダイアログが表示されているかどうか？の判定
time.sleep(4)
if len(driver.find_elements(By.CLASS_NAME, "is-show")) > 0:
    click_element("id", "js-ListingModalClose")

for i in range(int(total)):
    j = i + int(start_no)

    sandal_size = inifile.get('出品', 'サイズ' + str(j))
    sandal_no = inifile.get('出品', '通番' + str(j))
    sandal_price = inifile.get('出品', '価格' + str(j))
    # タイトルのクリア
    time.sleep(3)
    driver.find_element(By.ID,
                        'fleaTitleForm').clear()
    print("タイトルのクリア")
    # タイトルの入力
    sendkeys_element("id",
                     'fleaTitleForm', "西村の布ぞうり %scm (%s)" % (sandal_size, sandal_no))
    print("タイトルの入力 西村の布ぞうり %scm (%s)" % (sandal_size, sandal_no))

    sendkeys_element("id", "selectFile", folder_name + sandal_no + '.jpg')
    time.sleep(3)
    sendkeys_element("id", "selectFile", folder_name + sandal_no + 'a.jpg')
    time.sleep(3)
    click_element("id", "acMdCateChange")  # カテゴリ選択
    click_element("link_text", "リストから選択する")
    click_element("id", "24198")  # 住まい
    click_element("id", "42160")  # 家庭用品
    click_element("id", "2084047779")  # スリッパ
    click_element("id", "updateCategory")  # このカテゴリに決定
    print('カテゴリ選択')

    # 返品を受け付けるにチェックがはいっていない場合は、チェックする
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="js-PCNonPreReutnPolicyArea"]/input')))
    if driver.find_element(By.XPATH, '//*[@id="js-PCNonPreReutnPolicyArea"]/input').get_attribute('value') == "0":
        print('返品可をチェックする')
        click_element(
            "xpath", '//*[@id="js-PCNonPreReutnPolicyArea"]/label/span[1]')

    # # 値下げ交渉はしないので、値下げ交渉のチェックを外す
    # if 'is-check' in driver.find_element(By.XPATH,'//*[@id="price_buynow"]/div[3]/label').get_attribute('class'):
    #     print('値引き交渉するのチェックを外す')
    #     click_element("xpath",
    #                   '//*[@id="price_buynow"]/div[3]/label/span[1]')

    if len(driver.find_elements(By.LINK_TEXT, "HTMLタグ入力")) > 0:
        click_element("link_text", "HTMLタグ入力")
        print('HTMLタグ入力')

    # '出品者が送料負担
    click_element("xpath",
                  '//*[@id="FormReqrd"]/section[2]/div[6]/label[1]')
    print("出品者が送料負担")

    # '1から2日で発送
    click_element("xpath",
                  '//*[@id="standardDeliveryArea"]/div[2]/label[1]')
    print("1から2日で発送")

    # 商品の状態を入力
    Select(driver.find_element(By.NAME, "istatus")).select_by_value('new')
    print("商品の状態を入力")

    # ゆうパケットお手軽版
    click_element("xpath", '//*[@id="yubinForm"]/div[2]/ul/li[1]')
    print("ゆうパケットお手軽版")

    # 終了日を入力
    Select(driver.find_element(By.NAME, "ClosingYMD")).select_by_index(6)
    print("終了日を入力")

    # セールスモード
    click_element(
        "xpath", '//*[@id="FormReqrd"]/section[4]/div[3]/div[2]/label[2]')
    print("セールスモード:フリマ")

    # 価格のクリア
    driver.find_element(By.ID,
                        'auc_BidOrBuyPrice_buynow').clear()
    print("価格のクリア")
    # 価格の入力
    sendkeys_element("id",
                     'auc_BidOrBuyPrice_buynow', sandal_price)
    print("価格の入力")

    # 商品説明のクリア CTRL+A, DELETE
    driver.find_element(By.ID,
                        "rteEditorComposition0").send_keys(Keys.CONTROL, "a")
    driver.find_element(By.ID,
                        "rteEditorComposition0").send_keys(Keys.DELETE)
    for line in description.split('\\n'):
        driver.find_element(By.ID, "rteEditorComposition0").send_keys(line)
        driver.find_element(By.ID,
                            "rteEditorComposition0").send_keys(Keys.ENTER)
    print("商品説明")

    # '出品するボタン
    if debug_on:
        input('入力待ち >>')
    click_element("css_selector", '.Inquiry__button')
    print("確認ボタン")
    click_element("id", 'auc_preview_submit_up')
    print("出品ボタン")

    # 出品後に不要なダイアログが表示されたときは閉じる
    time.sleep(3)
    if driver.find_elements(By.XPATH,'//*[@id = "yaucSellItemCmplt"]/div[10]'):
        # 名前とプロフィール画像を‥
        if "display: block" in driver.find_element(By.XPATH, '//*[@id = "yaucSellItemCmplt"]/div[10]').get_attribute("style"):
            click_element(
                "xpath", '//*[@id = "yaucSellItemCmplt"]/div[10]/div/div/div/a[2]')
    if driver.find_elements(By.XPATH,'//*[@id="yaucSellItemCmplt"]/div[11]'):
        # 支払いを直接‥
        if "display: block" in driver.find_element(By.XPATH, '//*[@id="yaucSellItemCmplt"]/div[11]').get_attribute("style"):
            click_element("link_text", 'とじる')

    click_element("link_text", "出品")

driver.quit()
