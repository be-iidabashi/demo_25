"""
教材「タイピング自動化」で使用する、寿司打自動化（OCR なし）のコードです。
"""
import os
import re
import time
import zipfile
import urllib.request
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import SessionNotCreatedException, WebDriverException

# WebDriverのダウンロード関連の定数
LATEST_VERSION_URL = "https://googlechromelabs.github.io/chrome-for-testing/"

# ウィンドウサイズを固定し、画面中央に配置
# +123 としているのは、「自動テストソフトウェアによって制御されています。」という部分を考慮している
window_width = 730
window_height = 630 + 123

def get_latest_webdriver_version():
    response = requests.get(LATEST_VERSION_URL)
    soup = BeautifulSoup(response.content, 'html.parser')
    td_element = soup.find(string="Stable").find_next('td')
    stable_version = td_element.find("code").text
    return stable_version

def download_webdriver_version(version):
    # MacOS用のURLに変更
    file_url = f"https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/{version}/mac-arm64/chromedriver-mac-arm64.zip"
    save_path = "./download_webdriver.zip"
    print(f'{version} のバージョンをダウンロードします。')
    
    with urllib.request.urlopen(file_url) as download_file:
        data = download_file.read()
        with open(save_path, mode='wb') as save_file:
            save_file.write(data)
            
    with zipfile.ZipFile("./download_webdriver.zip") as obj_zip:
        # MacOS用のパスに変更
        with obj_zip.open('chromedriver-mac-arm64/chromedriver') as src, open('./chromedriver', 'wb') as dst:
            dst.write(src.read())
    
    # 実行権限を付与
    os.chmod('./chromedriver', 0o755)
            
    os.remove('./download_webdriver.zip')
    print("ドライバーのダウンロードが完了しました")

def setup_webdriver():
    # カレントディレクトリの絶対パスを取得
    current_dir = os.path.dirname(os.path.abspath(__file__))
    chromedriver_path = os.path.join(current_dir, 'chromedriver')
    
    try:
        service = Service(executable_path=chromedriver_path)
        driver = webdriver.Chrome(service=service)
        return driver
    except (FileNotFoundError, WebDriverException, SessionNotCreatedException) as e:
        print(f"エラーが発生しました: {str(e)}")
        match = re.search(r'(?<=\bchrome=)\d+', str(e))
        if match:
            version = match.group()
        else:
            version = get_latest_webdriver_version()
        
        download_webdriver_version(version)
        service = Service(executable_path=chromedriver_path)
        return webdriver.Chrome(service=service)

# メインの実行コード（if __name__ == "__main__": を削除）
driver = setup_webdriver()  # 最新のドライバーをセットアップ

# ウィンドウサイズを固定し、画面中央に配置
driver.set_window_size(window_width, window_height)
driver.set_window_position(200, 200)

url = "https://sushida.net/play.html"
driver.get(url)
    
# 画面が表示されるまで待つ
time.sleep(8)

# 寿司打のゲーム画面をずらすために書く
target_xpath = '//*[@id="game"]/div'
webgl_element = WebDriverWait(driver, 30).until(
    EC.presence_of_element_located((By.XPATH, target_xpath))
)

actions = ActionChains(driver)
actions.move_to_element(webgl_element)
actions.perform()

# # 要素の位置とサイズを取得
# location = webgl_element.location
# size = webgl_element.size
# print(f"Element location: {location}")
# print(f"Element size: {size}")

# # スタートボタンの座標
# center_x = size['width'] // 2
# center_y = size['height'] // 2
# print(f"Click coordinates: ({center_x}, {center_y})")

# # スタートボタンをクリックする
# print("スタートボタンをクリック")
# actions.move_to_element_with_offset(webgl_element, center_x, center_y).click().perform()

# # ボタンが表示されるまで待つ
# time.sleep(2)

# # お勧めコースをクリックする
# print("お勧めコースをクリック")
# actions.move_to_element_with_offset(webgl_element, center_x, center_y).click().perform()

# time.sleep(1)

# <body> に向かってキーを入力させる
target_xpath = '/html/body'
element = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, target_xpath))
)

element.send_keys(" ")

start = time.time()

while time.time() - start < 90.0:
    # 文字をテキトーに入力
    element.send_keys("abcdefghijklmnopqrstuvwxyz-!?.,")

input("何か入力してください")

# ドライバーを閉じる
driver.quit()