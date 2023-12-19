import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.chrome import service
import configparser
import warnings

warnings.filterwarnings("ignore")


def click_element(element_type, element_name):
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((element_type, element_name))
    )
    driver.find_element(element_type, element_name).click()


inifile = configparser.ConfigParser()
inifile.read("./sandals.ini", "UTF-8")
endday = inifile.get("設定", "終了日")

userdata_dir = "UserData"  # カレントディレクトリの直下に作る場合
os.makedirs(userdata_dir, exist_ok=True)
cwdpath = os.getcwd()

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_argument("--user-data-dir=" + cwdpath + "/" + userdata_dir)
options.add_argument("--log-level=3")
driver = webdriver.Chrome(service=service, options=options)

# 一度設定すると find_element 等の処理時に、
# 要素が見つかるまで指定時間繰り返し探索するようになります。
driver.implicitly_wait(10)  # 秒
time.sleep(3)
driver.get("https://auctions.yahoo.co.jp/")

input("ログイン後、マイオクのリンクが表示されるまで進んだあとに、エンターで再開 : ")
click_element(By.LINK_TEXT, "マイオク")
click_element(By.LINK_TEXT, "出品終了分")
click_element(By.LINK_TEXT, "落札者なし")

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "落札者あり")))
while len(driver.find_elements(By.XPATH, "//img[@alt='再出品']")) > 0:
    print("再出品する商品の数: " + str(len(driver.find_elements(By.XPATH, "//img[@alt='再出品']"))))

    click_element(By.XPATH, "//img[@alt='再出品']")
    time.sleep(1)

    # 不要なダイアログが表示されていた場合のクローズ処理
    if len(driver.find_elements(By.XPATH, '//*[@id="js-ListingModal"]')):
        if "is-show" in driver.find_element(
            By.XPATH, '//*[@id="js-ListingModal"]'
        ).get_attribute("class"):
            print("ヤフネコダイアログのクローズ")
            click_element(By.CSS_SELECTOR, ".CrossListingModal__exhibitButton")

    # 終了日を入力
    Select(driver.find_element(By.NAME, "ClosingYMD")).select_by_index(endday)
    print("終了日を入力")

    # '出品するボタン
    click_element(By.CSS_SELECTOR, ".Inquiry__button")
    print("確認ボタン")
    click_element(By.ID, "auc_preview_submit_up")
    print("出品ボタン")

    # 出品後に不要なダイアログが表示されたときは閉じる
    time.sleep(1)
    # 名前とプロフィール画像を‥
    if len(driver.find_elements(By.XPATH, '//*[@id = "yaucSellItemCmplt"]/div[10]')):
        if "display: block" in driver.find_element(
            By.XPATH, '//*[@id = "yaucSellItemCmplt"]/div[10]'
        ).get_attribute("style"):
            click_element(
                By.XPATH, '//*[@id = "yaucSellItemCmplt"]/div[10]/div/div/div/a[2]'
            )
    # 支払いを直接‥
    if len(driver.find_elements(By.XPATH, '//*[@id="yaucSellItemCmplt"]/div[11]')):
        if "display: block" in driver.find_element(
            By.XPATH, '//*[@id="yaucSellItemCmplt"]/div[11]'
        ).get_attribute("style"):
            click_element(By.LINK_TEXT, "とじる")

    click_element(By.LINK_TEXT, "落札されなかったオークション")

driver.quit()
exit
