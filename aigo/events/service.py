from line_bot_api import *
from urllib.parse import parse_qsl
import datetime

from extensions import db
from models.user import User
from models.reservation import Reservation



services = {
    1: {
        'category': '上衣',
        'img_url': 'https://imgur.com/J2MyydK',
        'title': '棉麻花方領',
        'duration': '183699170',
        'description': '上衣',
        'price': 882,
        'post_url': 'https://www.jwshop.com.tw/products/47249ba7-955d-42e2-9d22-297114260287'
    },
    2: {
        'category': '上衣',
        'img_url': 'https://imgur.com/45Z9G1P',
        'title': '防曬外套',
        'duration': '18306223',
        'description': '上衣',
        'price': 702,
        'post_url': 'https://www.jwshop.com.tw/products/020f8e72-f629-49fe-a082-a20edf0c5f1c'
    },
    3: {
        'category': '上衣',
        'img_url': 'https://imgur.com/cwNySA8',
        'title': '橫條短polo衫',
        'duration': '187022038',
        'description': '上衣',
        'price': 882,
        'post_url': 'https://www.jwshop.com.tw/products/ff237560-47b9-4c25-ae95-d073daca697e'
    },
}

def service_category_event(event):
    image_carousel_template_message = TemplateSendMessage(
        alt_text='請選擇想服務類別',
        template=ImageCarouselTemplate(
            columns=[
                ImageCarouselColumn(
                    image_url='https://imgur.com/J2MyydK',
                    action=PostbackAction(
                        label='棉麻花方領',
                        display_text='想了解棉麻花方領',
                        data='action=service&category=棉麻花方領'
                    )
                ),
                ImageCarouselColumn(
                    image_url='https://imgur.com/cwNySA8',
                    action=PostbackAction(
                        label='橫條短polo衫',
                        display_text='橫條短polo衫',
                        data='action=service&category=橫條短polo衫'
                    )
                )
            ]
        )
    )
    line_bot_api.reply_message(
        event.reply_token,
        [image_carousel_template_message])


def service_event(event):
    #底下三個要等上面的service建立後才寫,主要是要跑service的服務
    #data = dict(parse_qsl(event.postback.data))
    #bubbles = []
    #for service_id in services:
    data = dict(parse_qsl(event.postback.data))

    bubbles = []

    for service_id in services:
        if services[service_id]['category'] == data['category']:
            service = services[service_id]
            bubble = {
              "type": "bubble",
              "hero": {
                "type": "image",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "url": service['img_url']
              },
              "body": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "text",
                    "text": service['title'],
                    "wrap": True,
                    "weight": "bold",
                    "size": "xl"
                  },
                  {
                    "type": "text",
                    "text": service['duration'],
                    "size": "md",
                    "weight": "bold"
                  },
                  {
                    "type": "text",
                    "text": service['description'],
                    "margin": "lg",
                    "wrap": True
                  },
                  {
                    "type": "box",
                    "layout": "baseline",
                    "contents": [
                      {
                        "type": "text",
                        "text": f"NT$ {service['price']}",
                        "wrap": True,
                        "weight": "bold",
                        "size": "xl",
                        "flex": 0
                      }
                    ],
                    "margin": "xl"
                  }
                ]
              },
              "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                  {
                    "type": "button",
                    "style": "primary",
                    "action": {
                      "type": "postback",
                      "label": "預約",
                      "data": f"action=select_date&service_id={service_id}",
                      "displayText": f"我想預約【{service['title']} {service['duration']}】"
                    },
                    "color": "#b28530"
                  },
                  {
                    "type": "button",
                    "action": {
                      "type": "uri",
                      "label": "了解詳情",
                      "uri": service['post_url']
                    }
                  }
                ]
              }
            }

            bubbles.append(bubble)
    flex_message = FlexSendMessage(
        alt_text='請選擇預約項目',
        contents={
          "type": "carousel",
          "contents": bubbles
        }
    )

    line_bot_api.reply_message(
        event.reply_token,
        [flex_message])

def service_select_date_event(event):
    data = dict(parse_qsl(event.postback.data))

    weekdat_string={
          0:'一',
          1:'二',
          2:'三',
          3:'四',
          4:'五',
          5:'六',
          6:'日',
     }#休息日就拿掉

    business_day = [1,2,3,4,5,6]#休息日就拿掉

    quick_reply_buttons = []

    today = datetime.datetime.today().date()#取得當天日期
    #weekday()取得星期幾?0是星期一
    for x in range(1,11):
        day = today + datetime.timedelta(days=x)#透過datetime.timedelta()可以取得隔天的日期
        

        if day != 0 and (day.weekday() in business_day):
            quick_reply_button = QuickReplyButton(
                action = PostbackAction(label=f'{day}({weekdat_string[day.weekday()]})',
                                        text=f'我要預約{day}({weekdat_string[day.weekday()]})這天',
                                        data= f'action=select_time&service_id={data["service_id"]}&date={day}'))
            quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text="請問要預約哪一天？",
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
         event.reply_token,
         [text_message]
    )




#選擇時間功能
def service_select_time_event(event):
    data = dict(parse_qsl(event.postback.data))

    available_time=['11:00', '14:00' ,'17:00', '20:00'] #可以自己更改時間段

    quick_reply_buttons = []

    for time in available_time:
         quick_reply_button = QuickReplyButton(action= PostbackAction(label=time,
                                                                       text=f'{time}這個時段',
                                                                       data=f'action=confirm&service_id={data["service_id"]}&date={data["date"]}&time={time}'))
         quick_reply_buttons.append(quick_reply_button)

    text_message = TextSendMessage(text='請問要預約哪個時段？',
                                   quick_reply=QuickReply(items=quick_reply_buttons))
    
    line_bot_api.reply_message(
         event.reply_token,
         [text_message]
    )

#
def service_confirm_event(event):
     
    data = dict(parse_qsl(event.postback.data))
    booking_service = services[int(data['service_id'])] #取得要預約的服務項目資料，會出現1234對應到上面的service

    confirm_template_message = TemplateSendMessage(
        alt_text='請確認預約項目',
        template = ConfirmTemplate(
            text=f'您即將預約\n\n{booking_service["title"]} {booking_service["duration"]}\n預約時段: {data["date"]} {data["time"]}\n\n確認沒問題請按【確定】',
            actions=[
                 PostbackAction(
                        label='確定',
                        display_text='確定沒問題！',
                        data=f'action=confirmed&service_id={data["service_id"]}&date={data["date"]}&time={data["time"]}'
                 ),
                 MessageAction(
                        label='重新預約',
                        text='@預約服務'
                 )
            ]
        )
    )
    line_bot_api.reply_message(
         event.reply_token,
         [confirm_template_message]
    )


def is_booked(event, user):
    reservation = Reservation.query.filter(Reservation.user_id == user.id,
                                           Reservation.is_canceled.is_(False),#代表沒有被取消
                                           Reservation.booking_datetime > datetime.datetime.now()).first()
                                           #需要大於當下的時間.first()是會回傳第一筆資料
    if reservation:#text顯示預約項目名稱和服務時段
        buttons_template_message = TemplateSendMessage(
            alt_text='您已經有預約了，是否需要取消?',
            template=ButtonsTemplate(
                title='您已經有預約了',
                text=f'{reservation.booking_service}\n預約時段: {reservation.booking_datetime}',
                actions=[
                    PostbackAction(
                        label='我想取消預約',
                        display_text='我想取消預約',
                        data='action=cancel'
                    )
                ]
            )
        )

        line_bot_api.reply_message(
            event.reply_token,
            [buttons_template_message])

        return True
    else:
        return False
