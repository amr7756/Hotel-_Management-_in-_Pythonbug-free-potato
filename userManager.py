import json
from datetime import datetime
from user import User


class UserManager:
    def __init__(self):
        self.users = self.load_users()
        if self.users is None:
            self.users = []

    def load_users(self):
        try:
            with open('data/users.json', 'r', encoding='utf-8') as file:
                users_data = json.load(file)
                return [User(**user_data) for user_data in users_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_users(self):
        with open('data/users.json', 'w', encoding='utf-8') as file:
            users_data = [{
                'id': user.id,
                'user_name': user.user_name,
                'password': user.password,
                'role': user.role,
                'phone_number': user.phone_number
            } for user in self.users]
            json.dump(users_data, file, ensure_ascii=False, indent=4)

    def authenticate_user(self, user_name, password):
        for user in self.users:
            if user.user_name == user_name and user.password == password:
                return user
        return None

    def generate_id(self):
        return 1 if not self.users else max(user.id for user in self.users) + 1

    def manage_users(self, scanner):
        while True:
            try:
                print("\n*** إدارة المستخدمين ***")
                print("1. عرض المستخدمين")
                print("2. إضافة مستخدم")
                print("3. تعديل مستخدم")
                print("4. حذف مستخدم")
                print("5. البحث عن مستخدم")
                print("6. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_users()
                elif choice == '2':
                    self.add_user(scanner)
                elif choice == '3':
                    self.update_user(scanner)
                elif choice == '4':
                    self.delete_user(scanner)
                elif choice == '5':
                    self.search_user(scanner)
                elif choice == '6':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 6.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def list_users(self):
        if not self.users:
            print("لا يوجد مستخدمين.")
        else:
            for user in self.users:
                print(user)

    def add_user(self, scanner):
        try:
            user_name = input("اسم المستخدم: ")
            while any(u.user_name == user_name for u in self.users):
                print("المستخدم موجود بالفعل! يرجى إدخال اسم مستخدم آخر.")
                user_name = input("اسم المستخدم: ")

            phone_number = input("رقم الهاتف: ")
            password = input("كلمة المرور: ")

            role = input("الدور (admin/user): ").lower()
            while role not in ['admin', 'user']:
                print("الدور غير صالح! يرجى إدخال دور صحيح (admin/user).")
                role = input("الدور (admin/user): ").lower()

            new_user = User(
                id=self.generate_id(),
                user_name=user_name,
                password=password,
                role=role,
                phone_number=phone_number
            )
            self.users.append(new_user)
            self.save_users()
            print("تم الإضافة بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def update_user(self, scanner):
        try:
            user_id = int(input("أدخل رقم المستخدم: "))
            user = next((u for u in self.users if u.id == user_id), None)

            if not user:
                print("المستخدم غير موجود!")
                return

            new_name = user.user_name
            new_password = user.password
            new_role = user.role
            new_phone = user.phone_number

            choice = input("هل تريد تعديل اسم المستخدم؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل اسم المستخدم؟ (y/n): ").lower()

            if choice == 'y':
                new_name = input("اسم المستخدم الجديد: ")
                while any(u.user_name == new_name and u.id != user_id for u in self.users):
                    print("المستخدم موجود بالفعل! يرجى إدخال اسم مستخدم آخر.")
                    new_name = input("اسم المستخدم الجديد: ")

            choice = input("هل تريد تعديل رقم الهاتف؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل رقم الهاتف؟ (y/n): ").lower()

            if choice == 'y':
                new_phone = input("رقم الهاتف الجديد: ")

            choice = input("هل تريد تعديل كلمة المرور؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل كلمة المرور؟ (y/n): ").lower()

            if choice == 'y':
                new_password = input("كلمة المرور الجديدة: ")

            choice = input("هل تريد تعديل الدور؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل الدور؟ (y/n): ").lower()

            if choice == 'y':
                new_role = input("الدور الجديد (admin/user): ").lower()
                while new_role not in ['admin', 'user']:
                    print("الدور غير صالح! يرجى إدخال دور صحيح (admin/user).")
                    new_role = input("الدور الجديد (admin/user): ").lower()

            # تحديث بيانات المستخدم
            user.user_name = new_name
            user.password = new_password
            user.role = new_role
            user.phone_number = new_phone

            self.save_users()
            print("تم التعديل بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def delete_user(self, scanner):
        try:
            user_id = int(input("أدخل رقم المستخدم: "))
            user_to_delete = next((u for u in self.users if u.id == user_id), None)

            if user_to_delete:
                self.users.remove(user_to_delete)
                self.save_users()
                print("تم الحذف بنجاح!")
            else:
                print("المستخدم غير موجود!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def search_user(self, scanner):
        try:
            choice = input("ابحث بـ (1-رقم المستخدم / 2-اسم المستخدم): ")
            if choice == '1':
                user_id = int(input("أدخل رقم المستخدم: "))
                user = next((u for u in self.users if u.id == user_id), None)
                print(user if user else "لا يوجد مستخدم بهذا الرقم")
            else:
                user_name = input("اسم المستخدم: ")
                user = next((u for u in self.users if u.user_name == user_name), None)
                print(user if user else "لا يوجد مستخدم بهذا الاسم")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")