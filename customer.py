class Customer:
    def __init__(self, id, name, id_number, phone_number):
        self.id = id
        self.name = name
        self.id_number = id_number
        self.phone_number = phone_number

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_id_number(self):
        return self.id_number

    def get_phone_number(self):
        return self.phone_number

    def __str__(self):
        return f"عميل رقم: {self.id} | الاسم: {self.name} | رقم الهوية: {self.id_number} | رقم الهاتف: {self.phone_number}"