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
    EC.element_to_be_clickable((By.LINK_TEXT, "マイオク")))
driver.find_element_by_link_text("マイオク").click()
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "出品終了分")))
time.sleep(1)
driver.find_element_by_link_text("出品終了分").click()
WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "落札者なし")))
time.sleep(1)
driver.find_element_by_link_text("落札者なし").click()
time.sleep(1)

# get all the href attributes
# ダイアログの問い合わせステータス
display_dialog1 = "yes"
links = []
links = driver.find_elements_by_partial_link_text("布ぞうり")
print('布ぞうりの数 = ', len(links))
for webitem in links:
    # 不要なダイアログの対応 落札者なしのリスト
    if len(driver.find_elements_by_class_name('closeBtn')) > 0:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")  # スクロールして、ダイアログを表示
        # ダイアログの表示で変更になる部分 ダイアログは最初だけ表示されるので、それ以降は処理しない
        if display_dialog1 == "yes" and input('ダイアログは表示されていますか？ y/n? >> ') == 'y':
            display_dialog1 = "no"
            driver.find_element_by_class_name('closeBtn').click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.PARTIAL_LINK_TEXT, "布ぞうり")))
    driver.find_element_by_partial_link_text("布ぞうり").click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "再出品")))
    time.sleep(1)
    driver.find_element_by_link_text('再出品').click()
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
    # driver.find_element_by_xpath('//*[@id="FormReqrd"]/ul/ul/li/input').click()
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
        EC.element_to_be_clickable((By.LINK_TEXT, "出品終了分")))
    time.sleep(1)
    driver.find_element_by_link_text("出品終了分").click()
    WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "落札者なし")))
    time.sleep(1)
    driver.find_element_by_link_text("落札者なし").click()
    time.sleep(1)

driver.quit()
