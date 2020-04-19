import time
import chromedriver_binary
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
click_element('link_text', 'マイオク')
click_element('link_text', '出品終了分')
click_element('link_text', '落札者なし')

# get all the href attributes
# ダイアログの問い合わせステータス
display_dialog1 = "yes"
while len(driver.find_elements_by_partial_link_text("布ぞうり")):
    print(len(driver.find_elements_by_partial_link_text("布ぞうり")))
    # 不要なダイアログの対応 落札者なしのリスト
    if len(driver.find_elements_by_class_name('closeBtn')) > 0:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")  # スクロールして、ダイアログを表示
        # ダイアログの表示で変更になる部分 ダイアログは最初だけ表示されるので、それ以降は処理しない
        if display_dialog1 == "yes" and input('ダイアログは表示されていますか？ y/n? >> ') == 'y':
            display_dialog1 = "no"
            driver.find_element_by_class_name('closeBtn').click()
    click_element('partial_link_text', '布ぞうり')
    click_element('link_text', '再出品')

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
    click_element('xpath', '//*[@id="FormReqrd"]/section[2]/div[6]/label[2]')
    # '1から2日で発送
    click_element('xpath', '//*[@id="standardDeliveryArea"]/div[2]/label[1]')
    # 'その他の配送方法
    if 'is-close' in driver.find_element_by_xpath('//*[@id="standardDeliveryArea"]/section/div/div/dl').get_attribute('class'):
        driver.find_element_by_xpath(
            '//*[@id="standardDeliveryArea"]/section/div/div/dl').click()
    # 'クリックポスト
    click_element(
        'xpath', '//*[@id="standardDeliveryArea"]/section/div/div/dl/dd/div/ul[1]/li[1]/label')
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

    # 出品
    click_element('xpath', '//*[@id="FormReqrd"]/ul/ul/li/input')
    click_element('xpath', '//*[@id="auc_preview_submit"]')

    # 出品後に不要なダイアログが表示されたときは閉じる
    if "display: block" in driver.find_element_by_xpath('//*[@id="yaucSellItemCmplt"]/div[10]').get_attribute("style"):
        driver.find_element_by_xpath(
            '//*[@id="yaucSellItemCmplt"]/div[10]/div/div/div/a[2]').click()
    click_element('link_text', 'マイオク')
    click_element('link_text', '出品終了分')
    click_element('link_text', '落札者なし')

driver.quit()
exit
