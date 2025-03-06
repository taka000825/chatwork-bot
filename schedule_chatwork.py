import schedule
import time
import requests
from datetime import datetime

# Chatwork API情報
API_TOKEN = "ecbfe8cfd91f8f46a2e06cc4174b1e9c"  # あなたのAPIキー
ROOM_ID = "377337322"  # 送信先のルームID

# メッセージ生成関数
def create_message():
    now = datetime.now()
    previous_month = now.month - 1 if now.month > 1 else 12  # 前月
    current_month = now.month  # 今月

    message = f"""[toall]
【精算のお願い】
皆さん、いつもお世話になっております。

{previous_month}月分のお仕事の精算をお願いいたします

提出期限：{current_month}月10日（月）まで
※期限が過ぎてからの提出は一切受け付けておりませんのでご了承ください※

お支払いに関しては末締め、
翌月18～20日に順次お支払いさせていただきます。

不明な点があればお気軽に鈴木との個別チャットでご連絡ください。

※常駐していないため、確認が翌日～翌々日になる場合がございます。
※提出していただいた請求書、または個別チャットからのメッセージに【翌々日までに】鈴木からのアクションまたは返信がない場合、お手数ですが一声おかけください。

請求書に関する問い合わせは鈴木さんまでお願いします。

今後ともよろしくお願いいたします(bow)
"""
    return message

# Chatworkにメッセージを送信
def send_message():
    message = create_message()
    url = f"https://api.chatwork.com/v2/rooms/{ROOM_ID}/messages"
    headers = {"X-ChatWorkToken": API_TOKEN}
    data = {"body": message}
    
    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        print("✅ メッセージ送信成功！")
    else:
        print(f"❌ メッセージ送信失敗: {response.status_code}, {response.text}")

# 1日ならメッセージを送信
def check_and_send_message():
    if datetime.now().day == 1:  # 1日の場合のみ実行
        send_message()

# 毎日13時に実行（1日ならメッセージを送る）
schedule.every().day.at("13:00").do(check_and_send_message)

# スケジュール実行ループ
while True:
    schedule.run_pending()
    time.sleep(60)  # 1分ごとにチェック
