import json
from datetime import datetime, timedelta
from discount import Discount
from roomManager import RoomManager
from dateutil import parser

class DiscountManager:
    def __init__(self):
        self.discounts = self.load_discounts()
        if self.discounts is None:
            self.discounts = []

    def load_discounts(self):
        try:
            with open('data/discounts.json', 'r', encoding='utf-8') as file:
                discounts_data = json.load(file)
                return [Discount(**d) for d in discounts_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_discounts(self):
        with open('data/discounts.json', 'w', encoding='utf-8') as file:
            discounts_data = [{
                'discount_id': d.discount_id,
                'description': d.description,
                'percentage': d.percentage,
                'start_date': d.start_date.isoformat(),
                'end_date': d.end_date.isoformat(),
                'room_id': d.room_id
            } for d in self.discounts]
            json.dump(discounts_data, file, ensure_ascii=False, indent=4)

    def generate_id(self):
        return 1 if not self.discounts else self.discounts[-1].discount_id + 1

    def get_active_discount_for_room(self, room_id):
        for discount in self.discounts:
            if discount.is_active() and (discount.room_id is None or discount.room_id == room_id):
                return discount
        return None

    def manage_discounts_admin(self, scanner):
        while True:
            try:
                print("\n*** إدارة الخصومات ***")
                print("1. عرض الخصومات")
                print("2. إضافة خصم")
                print("3. تعديل خصم")
                print("4. حذف خصم")
                print("5. البحث عن خصم")
                print("6. فحص الخصومات المنتهية")
                print("7. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_discounts()
                elif choice == '2':
                    self.add_discount(scanner)
                elif choice == '3':
                    self.update_discount(scanner)
                elif choice == '4':
                    self.delete_discount(scanner)
                elif choice == '5':
                    self.search_discount(scanner)
                elif choice == '6':
                    self.check_expired_discounts()
                elif choice == '7':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 7.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def manage_discounts_user(self, scanner):
        while True:
            try:
                print("\n*** إدارة الخصومات ***")
                print("1. عرض الخصومات")
                print("2. البحث عن خصم")
                print("3. فحص الخصومات المنتهية")
                print("4. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_discounts()
                elif choice == '2':
                    self.search_discount(scanner)
                elif choice == '3':
                    self.check_expired_discounts()
                elif choice == '4':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 4.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def list_discounts(self):
        if not self.discounts:
            print("لا توجد خصومات.")
        else:
            for discount in self.discounts:
                print(discount)

    def add_discount(self, scanner):
        try:
            description = input("وصف الخصم: ")
            percentage = float(input("نسبة الخصم (%): "))

            discount_type = input("نوع الخصم (1-عام / 2-خاص بغرفة): ")
            while discount_type not in ['1', '2']:
                print("إدخال غير صحيح! يرجى إدخال 1 أو 2.")
                discount_type = input("نوع الخصم (1-عام / 2-خاص بغرفة): ")

            room_id = None
            if discount_type == '2':
                room_id = int(input("أدخل رقم الغرفة: "))
                while not any(r.id == room_id for r in RoomManager().rooms):
                    print("لا توجد غرفة بهذا الرقم! يرجى إدخال رقم غرفة صحيح.")
                    room_id = int(input("أدخل رقم الغرفة: "))

            days = int(input("مدة الخصم بالأيام: "))
            start_date = datetime.now()
            end_date = start_date + timedelta(days=days)

            new_discount = Discount(
                discount_id=self.generate_id(),
                description=description,
                percentage=percentage,
                start_date=start_date,
                end_date=end_date,
                room_id=room_id
            )
            self.discounts.append(new_discount)
            self.save_discounts()
            print("تم الإضافة بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def update_discount(self, scanner):
        try:
            discount_id = int(input("أدخل رقم الخصم: "))
            discount = next((d for d in self.discounts if d.discount_id == discount_id), None)

            if not discount:
                print("الخصم غير موجود!")
                return

            new_desc = discount.description
            new_percent = discount.percentage
            new_days = (discount.end_date - discount.start_date).days
            new_room_id = discount.room_id

            choice = input("هل تريد تعديل وصف الخصم؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل وصف الخصم؟ (y/n): ").lower()

            if choice == 'y':
                new_desc = input("الوصف الجديد: ")

            choice = input("هل تريد تعديل نسبة الخصم؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل نسبة الخصم؟ (y/n): ").lower()

            if choice == 'y':
                new_percent = float(input("النسبة الجديدة (%): "))

            choice = input("هل تريد تعديل نوع الخصم؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل نوع الخصم؟ (y/n): ").lower()

            if choice == 'y':
                discount_type = input("نوع الخصم (1-عام / 2-خاص بغرفة): ")
                while discount_type not in ['1', '2']:
                    print("إدخال غير صحيح! يرجى إدخال 1 أو 2.")
                    discount_type = input("نوع الخصم (1-عام / 2-خاص بغرفة): ")

                if discount_type == '2':
                    new_room_id = int(input("أدخل رقم الغرفة: "))
                    while not any(r.id == new_room_id for r in RoomManager().rooms):
                        print("لا توجد غرفة بهذا الرقم! يرجى إدخال رقم غرفة صحيح.")
                        new_room_id = int(input("أدخل رقم الغرفة: "))
                else:
                    new_room_id = None

            choice = input("هل تريد تعديل مدة الخصم؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل مدة الخصم؟ (y/n): ").lower()

            if choice == 'y':
                new_days = int(input("المدة الجديدة بالأيام: "))

            new_start = datetime.now()
            new_end = new_start + timedelta(days=new_days)

            updated_discount = Discount(
                discount_id=discount_id,
                description=new_desc,
                percentage=new_percent,
                start_date=new_start,
                end_date=new_end,
                room_id=new_room_id
            )
            self.discounts[self.discounts.index(discount)] = updated_discount
            self.save_discounts()
            print("تم التعديل بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def delete_discount(self, scanner):
        try:
            discount_id = int(input("أدخل رقم الخصم: "))
            if any(d.discount_id == discount_id for d in self.discounts):
                self.discounts = [d for d in self.discounts if d.discount_id != discount_id]
                self.save_discounts()
                print("تم الحذف بنجاح!")
            else:
                print("الخصم غير موجود!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def search_discount(self, scanner):
        try:
            discount_id = int(input("أدخل رقم الخصم: "))
            discount = next((d for d in self.discounts if d.discount_id == discount_id), None)
            print(discount if discount else "الخصم غير موجود")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def check_expired_discounts(self):
        try:
            now = datetime.now()
            expired_count = 0

            for discount in self.discounts:
                if discount.end_date < now:
                    print(f"الخصم رقم {discount.discount_id} منتهي")
                    expired_count += 1

            if expired_count == 0:
                print("\nلا توجد خصومات منتهية")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")