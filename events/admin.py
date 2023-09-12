from line_bot_api import *
from models.reservation import Reservation
import datetime
from extensions import db
from models.user import User

def list_reservation_event(event):
    reservation = Reservation.query.filter(Reservation.is_canceled.is_(False),
                                            Reservation.booking_datetime >datetime.datetime.now(),
                                            ).order_by(Reservation.booking_datetime.asc()).all()
    
    reservation_data_text = '## 預約名單: ##  \n\n'
    for reservation in reservation:
        reservation_data_text += f'''預約日期:{reservation.booking_datetime}
預約服務: {reservation.booking_service}
姓名: {reservation.user.display_name}\n'''

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reservation_data_text))
