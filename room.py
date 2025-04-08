class Room:
    def __init__(self, id, room_type, price, is_available):
        self.id = id
        self.room_type = room_type
        self.price = price
        self.is_available = is_available

    def get_id(self):
        return self.id

    def get_room_type(self):
        return self.room_type

    def get_price(self):
        return self.price

    def is_available(self):
        return self.is_available

    def __str__(self):
        return f"غرفة رقم: {self.id} | نوع: {self.room_type} | السعر: {self.price} | متاحة: {'نعم' if self.is_available else 'لا'}"