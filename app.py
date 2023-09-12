from flask import Flask,request,abort
from events.service import *
from line_bot_api import *
from events.basic import *
from events.admin import *
from extensions import db, migrate
from models.user import User    

import os

app = Flask(__name__)#admin: !QAZ2wsx資料庫的帳號和密碼
#讓程式自己去判斷如果是測試端就會使用APP_SETTINGS
app.config.from_object(os.environ.get('APP_SETTINGS', 'config.DevConfig'))
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://medicine_offer:Vt6RqxnBcXH45JzKvz8wUqVJZi6Vq4Ny@dpg-cjg2jec1ja0c739odo7g-a.singapore-postgres.render.com/medicine_offer'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.app = app
db.init_app(app)
migrate.init_app(app, db)


#callback

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    message_text = str(event.message.text).lower()
    user = User.query.filter(User.line_id == event.source.user_id).first()#取得user的第一筆資料
    #如果沒有user資料時，才會透過api去取得
    if not user:
        profile = line_bot_api.get_profile(event.source.user_id)#Line API 中說明get_profile可以取得的資料
        print(profile.display_name)
        print(profile.user_id)#相同的好以會因為不同的profile 而有不同的user_id

        user = User(profile.user_id, profile.display_name, profile.picture_url)
        db.session.add(user)
        db.session.commit()

    print(user.id)
    print(user.line_id)
    print(user.display_name)


    if message_text == '@關於我們':
        about_us_event(event)

    elif message_text == '@營業據點':
        location_event(event)
    elif message_text =='@預約服務':
        service_category_event(event)

    elif message_text.startswith('*'):
        if event.source.user_id not in ['U135d0047f682b28ef4001bcb47d0d21f']:
            return
        if message_text in ['*data', '*d']:
            list_reservation_event(event)
    elif message_text == '@取消預約':
        pass

        


#接收postback的訊息
#parse_qsl解析data中的資料
@handler.add(PostbackEvent)
def handle_postback(event):
    #把傳進來的event儲存在postback.data中再利用parse_qsl解析data中的資料然漚轉換成dict
    data = dict(parse_qsl(event.postback.data))
    #建立好def service_event(event) function後要來這裡加上判斷式
    #直接呼叫service_event(event)

    if data.get('action') == 'service':
        service_event(event)
    elif data.get('action') == 'select_date':
        service_select_date_event(event)
    elif data.get('action') == 'select_time':
        service_select_time_event(event)
    elif data.get('action') == 'confirm':
        service_confirm_event(event)
    elif data.get('action') == 'confirmed':
        service_confirmed_event(event)
    elif data.get('action') == 'cancel':
        service_cancel_event(event)

    #用get()來取得data中的資料，好處是如果備有data時會顯示None，而不會出線錯物
    

################## 解除封鎖 ####################
@handler.add(FollowEvent)
def handle_follow(event):
    welcome_msg="""Hello! 您好，歡迎您成為 寶石服飾 的好友！

我是寶石服飾的小幫手 

-想預約試穿/現場取貨服務都可以直接跟我互動喔~
-直接點選下方【歡迎光臨專屬您的優惠】選單功能

-期待您的光臨！"""

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=welcome_msg)
    )

################## 顯示封鎖 ####################
@handler.add(UnfollowEvent)
def handle_unfollow(event):
    print(event)





if __name__ == '__main__':
    app.run()