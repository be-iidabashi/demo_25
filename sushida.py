"""
教材「タイピング自動化」で使用する、寿司打自動化（OCR なし）のコードです。
"""
import time

import chromedriver_binary
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()

# ウィンドウサイズを固定し、画面中央に配置
# +123 としているのは、「自動テストソフトウェアによって制御されています。」という部分を考慮している
window_width = 730
window_height = 630 + 123
driver.set_window_size(window_width, window_height)
driver.set_window_position(200, 200)  # 画面の中央に配置

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
