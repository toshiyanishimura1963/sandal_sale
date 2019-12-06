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
price = inifile.get('設定', '価格')
postage = inifile.get('設定', '送料')
description = inifile.get('設定', '商品説明')
USER_ID = inifile.get('設定', 'ユーザーID')
PASSWD = inifile.get('設定', 'パスワード')
folder_name = inifile.get('設定', '画像フォルダ')
total = inifile.get('出品', '出品数')
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
    driver.find_element_by_id("btnNext").click()
    time.sleep(1)
    driver.find_element_by_id("passwd").send_keys(PASSWD)
if not driver.find_element_by_id("persistent").is_selected():
    driver.find_element_by_id("persistent").click()
driver.find_element_by_id("btnSubmit").click()
time.sleep(1)
# if driver.find_element_by_id("js-close"):
#     driver.find_element_by_id("js-close").click()
if len(driver.find_elements_by_link_text("ご利用中のサービスに戻る")) > 0:
    driver.find_element_by_link_text("ご利用中のサービスに戻る").click()
    time.sleep(1)
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "フリマ出品")))
driver.find_element_by_link_text("フリマ出品").click()

# ダイアログが表示されているかどうか？の判定
if "block" in driver.find_element_by_id("js-exhibitMdl").get_attribute("style"):
    driver.find_elements_by_css_selector("#js-doRefuse").click()

for i in range(total):
    time.sleep(1)
    driver.find_elements_by_id("acMdCateChange").click()  # カテゴリ選択
    time.sleep(1)
    driver.find_elements_by_xpath("//*[@id='CategorySelect']/ul/li[1]/a/div").click() #リストから選択
    time.sleep(1)
    driver.find_elements_by_id("24198").click()   #住まい
    time.sleep(1)
    driver.find_elements_by_id("42160").click()   #家庭用品
    time.sleep(1)
    driver.find_elements_by_id("2084047779").click() #スリッパ
    time.sleep(1)
    driver.find_elements_by_id("updateCategory").click()  # このカテゴリに決定
    time.sleep(1)

    driver.FindElementByXPath("//*[@id='ImageUpArea']/div[5]/a").click() #写真の登録
    time.sleep(1)
    sandal_size = inifile.get('出品', 'サイズ' + str(i))
    sandal_no = inifile.get('出品', '通番' + str(i))
    driver.find_elements_by_name("ImageFile1").send_keys(folder_name + str(i) + '.jpg')
    time.sleep(1)
    driver.find_elements_by_name("ImageFile2").send_keys(folder_name + str(i) + 'a.jpg')
    time.sleep(1)
    driver.find_elements_by_id("cnfm_btn").click()
    time.sleep(1)
    driver.find_elements_by_id("back_btn").click()
    time.sleep(1)

    # paypay のダイアログ表示を消去
    print(driver.find_element_by_id('js-ListingModal').get_attribute('class'))
    if 'is-show' in driver.find_element_by_id('js-ListingModal').get_attribute('class'):
        driver.find_element_by_id("js-ListingModalClose").click()

    # 返品を受け付けるにチェックがはいっていない場合は、チェックする
    WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="FormReqrd"]/div[13]/input')))
    if driver.find_element_by_xpath('//*[@id="FormReqrd"]/div[13]/input').get_attribute('value') == "0":
        print('返品可をチェックする')
        driver.find_element_by_xpath(
            '//*[@id="FormReqrd"]/div[13]/label/span[1]').click()

    # 値下げ交渉はしないので、値下げ交渉のチェックを外す
    if 'is-check' in driver.find_element_by_xpath('//*[@id="price_buynow"]/div[3]/label').get_attribute('class'):
        print('値引き交渉するのチェックを外す')
        driver.find_element_by_xpath(
            '//*[@id="price_buynow"]/div[3]/label/span[1]').click()

    if len(driver.find_elements_by_link_text("HTMLタグ入力")) > 0:
        driver.find_element_by_link_text("HTMLタグ入力").click()

    # '落札者が送料負担
    driver.find_element_by_xpath(
        '//*[@id="FormReqrd"]/section[2]/div[6]/label[2]').click()
    # '1から2日で発送
    driver.find_element_by_xpath(
        '//*[@id="standardDeliveryArea"]/div[2]/label[1]').click()
    # 'その他の配送方法
    if 'is-close' in driver.find_element_by_xpath('//*[@id="standardDeliveryArea"]/section/div/div/dl').get_attribute('class'):
        driver.find_element_by_xpath(
            '//*[@id="standardDeliveryArea"]/section/div/div/dl').click()
    # 'クリックポスト
    driver.find_element_by_xpath(
        '//*[@id="standardDeliveryArea"]/section/div/div/dl/dd/div/ul[1]/li[1]/label').click()
    # '送料のクリア
    driver.find_element_by_xpath(
        '//*[@id="standardDeliveryArea"]/section/div/div/dl/dd/div/ul[1]/li[1]/div/div[2]/input').clear()
    # 送料の入力
    driver.find_element_by_xpath(
        '//*[@id="standardDeliveryArea"]/section/div/div/dl/dd/div/ul[1]/li[1]/div/div[2]/input').send_keys(postage)

    # 商品説明のクリア CTRL+A, DELETE
    driver.find_element_by_id(
        "rteEditorComposition0").send_keys(Keys.CONTROL, "a")
    driver.find_element_by_id(
        "rteEditorComposition0").send_keys(Keys.DELETE)
    for line in description.split('\\n'):
        driver.find_element_by_id("rteEditorComposition0").send_keys(line)
        driver.find_element_by_id(
            "rteEditorComposition0").send_keys(Keys.ENTER)
    if debug_on:
        input('入力待ち >>')

    driver.find_element_by_xpath(
        '//*[@id="auc_BidOrBuyPrice_buynow"]').clear()  # 価格のクリア
    driver.find_element_by_xpath(
        '//*[@id="auc_BidOrBuyPrice_buynow"]').send_keys(price)      # 価格の入力
    time.sleep(1)
    # '出品するボタン
    if debug_on:
        input('入力待ち >>')
    driver.find_element_by_xpath('//*[@id="FormReqrd"]/ul/ul/li/input').click()
    time.sleep(1)
    driver.find_element_by_xpath('//*[@id="auc_preview_submit"]').click()
    time.sleep(1)

    # 出品後に不要なダイアログが表示されたときは閉じる
    if "display: block" in driver.find_element_by_xpath('//*[@id="yaucSellItemCmplt"]/div[10]').get_attribute("style"):
        driver.find_element_by_xpath(
            '//*[@id="yaucSellItemCmplt"]/div[10]/div/div/div/a[2]').click()

    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "マイオク")))
    time.sleep(1)
    driver.find_element_by_link_text("マイオク").click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "フリマ出品")))
    time.sleep(1)
    driver.find_element_by_link_text("フリマ出品").click()

driver.quit()
