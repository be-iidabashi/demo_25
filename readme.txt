[macの場合]
1.仮想環境
python3 -m venv .venv
source .venv/bin/activate

2.パッケージのインストール
pip install -r requirements.txt

3.sushida501.py(chromedriver最新版自動インストール版)の実行

※.もしうまくいかなければ、sushida.pyの実行
→chromedriverエラーが出た場合
https://googlechromelabs.github.io/chrome-for-testing/
以下のサイトのChannel>Stableのverで最新版をインストール
(例)pip install chromedriver-binary==132.0.6834.159

