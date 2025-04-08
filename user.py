class User:
    def __init__(self, id, user_name, password, role, phone_number):
        self.id = id
        self.user_name = user_name
        self.password = password
        self.role = role
        self.phone_number = phone_number

    def get_id(self):
        return self.id

    def get_user_name(self):
        return self.user_name

    def get_password(self):
        return self.password

    def get_role(self):
        return self.role

    def get_phone_number(self):
        return self.phone_number

    def __str__(self):
        return f"|رقم المستخدم : {self.id} | اسم المستخدم: {self.user_name} | الدور: {self.role} | رقم الهاتف: {self.phone_number}"