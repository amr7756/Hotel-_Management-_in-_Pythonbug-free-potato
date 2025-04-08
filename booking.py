from datetime import datetime, timedelta
from dateutil import parser

class Booking:
    def __init__(self, booking_id, room_id, customer_id, start_date, end_date, is_paid, total_price):
        self.booking_id = booking_id
        self.room_id = room_id
        self.customer_id = customer_id
        self.start_date = parser.parse(start_date) if isinstance(start_date, str) else start_date
        self.end_date = parser.parse(end_date) if isinstance(end_date, str) else end_date
        self.is_paid = is_paid
        self.total_price = total_price

    def get_booking_id(self):
        return self.booking_id

    def get_room_id(self):
        return self.room_id

    def get_customer_id(self):
        return self.customer_id

    def get_start_date(self):
        return self.start_date

    def get_end_date(self):
        return self.end_date

    def is_paid(self):
        return self.is_paid

    def get_total_price(self):
        return self.total_price

    def __str__(self):
        return (f"حجز رقم {self.booking_id} | غرفة: {self.room_id} | عميل: {self.customer_id} | "
                f"من: {self.format_date_time(self.start_date)} | إلى: {self.format_date_time(self.end_date)} | "
                f"مدفوع: {'نعم' if self.is_paid else 'لا'} | السعر الإجمالي: {self.total_price}")

    @staticmethod
    def format_date_time(date):
        return date.strftime("%Y-%m-%d %H:%M:%S") if date else "غير محدد"