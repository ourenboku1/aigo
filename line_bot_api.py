from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent, StickerSendMessage, ImageSendMessage, LocationSendMessage,ImageCarouselTemplate,ImageCarouselColumn, PostbackAction, TemplateSendMessage, FlexSendMessage ,ButtonsTemplate ,PostbackEvent ,QuickReplyButton,QuickReply , ConfirmTemplate ,MessageAction
)

line_bot_api = LineBotApi('Sz1hgt3TkPaey3FgvI5zAxVhJTcy5aBztZSKGJwrx1hN1/3j8UtlfkRzoEGybPNwFlaChLfdBpHLyp0LI3GUt/P5SHMEHQ+TpnsrVpYeRLgqfM2LN8PhtML/1Z2LaP+gmcB6MAAOu6tjLXhcFzn0twdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('2a9195c6fc1f86b7b997dc6f01775f20')
