from datetime import datetime
from dateutil import parser

class Discount:
    def __init__(self, discount_id, description, percentage, start_date, end_date, room_id):
        self.discount_id = discount_id
        self.description = description
        self.percentage = percentage
        self.start_date = parser.parse(start_date) if isinstance(start_date, str) else start_date
        self.end_date = parser.parse(end_date) if isinstance(end_date, str) else end_date
        self.room_id = room_id

    def get_discount_id(self):
        return self.discount_id

    def get_description(self):
        return self.description

    def get_percentage(self):
        return self.percentage

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def get_room_id(self):
        return self.room_id

    def is_active(self):
        now = datetime.now()
        return now >= self.start_date and now <= self.end_date

    def __str__(self):
        room_info = "عام" if self.room_id is None else f"خاص بالغرفة {self.room_id}"
        return (f"خصم رقم {self.discount_id} | {self.description} | نسبة: {self.percentage}% | "
                f"من {self.format_date(self.start_date)} إلى {self.format_date(self.end_date)} | "
                f"الحالة: {'نشط' if self.is_active() else 'منتهي'} | نوع الخصم: {room_info}")

    @staticmethod
    def format_date(date):
        return date.strftime("%Y-%m-%d") if date else "غير محدد"