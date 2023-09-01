from line_bot_api import *
from urllib.parse import parse_qsl


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