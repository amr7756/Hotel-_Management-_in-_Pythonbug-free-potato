import json
from customer import Customer


class CustomerManager:
    def __init__(self):
        self.customers = self.load_customers()
        if self.customers is None:
            self.customers = []

    def load_customers(self):
        try:
            with open('data/customers.json', 'r', encoding='utf-8') as file:
                customers_data = json.load(file)
                return [Customer(**customer_data) for customer_data in customers_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_customers(self):
        with open('data/customers.json', 'w', encoding='utf-8') as file:
            customers_data = [{
                'id': customer.id,
                'name': customer.name,
                'id_number': customer.id_number,
                'phone_number': customer.phone_number
            } for customer in self.customers]
            json.dump(customers_data, file, ensure_ascii=False, indent=4)

    def get_customers(self):
        return self.customers

    def generate_id(self):
        return 1 if not self.customers else max(customer.id for customer in self.customers) + 1

    def manage_customers(self, scanner):
        while True:
            try:
                print("\n*** إدارة العملاء ***")
                print("1. عرض العملاء")
                print("2. إضافة عميل")
                print("3. تعديل عميل")
                print("4. حذف عميل")
                print("5. البحث عن عميل")
                print("6. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_customers()
                elif choice == '2':
                    self.add_customer(scanner)
                elif choice == '3':
                    self.update_customer(scanner)
                elif choice == '4':
                    self.delete_customer(scanner)
                elif choice == '5':
                    self.search_customer(scanner)
                elif choice == '6':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 6.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def list_customers(self):
        if not self.customers:
            print("لا يوجد عملاء.")
        else:
            for customer in self.customers:
                print(customer)

    def add_customer(self, scanner):
        try:
            name = input("اسم العميل: ")
            while any(c.name == name for c in self.customers):
                print("العميل موجود بالفعل! يرجى إدخال اسم آخر.")
                name = input("اسم العميل: ")

            phone_number = input("رقم الهاتف: ")

            id_number = input("رقم الهوية: ")
            while any(c.id_number == id_number for c in self.customers):
                print("رقم الهوية مسجل مسبقًا! يرجى إدخال رقم هوية آخر.")
                id_number = input("رقم الهوية: ")

            new_customer = Customer(
                id=self.generate_id(),
                name=name,
                id_number=id_number,
                phone_number=phone_number
            )
            self.customers.append(new_customer)
            self.save_customers()
            print("تم إضافة العميل بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def update_customer(self, scanner):
        try:
            customer_id = int(input("أدخل رقم العميل: "))
            customer = next((c for c in self.customers if c.id == customer_id), None)

            if not customer:
                print("العميل غير موجود!")
                return

            new_name = customer.name
            new_id_number = customer.id_number
            new_phone = customer.phone_number

            choice = input("هل تريد تعديل اسم العميل؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل اسم العميل؟ (y/n): ").lower()

            if choice == 'y':
                new_name = input("الاسم الجديد: ")
                while any(c.name == new_name and c.id != customer_id for c in self.customers):
                    print("العميل موجود بالفعل! يرجى إدخال اسم آخر.")
                    new_name = input("الاسم الجديد: ")

            choice = input("هل تريد تعديل رقم الهاتف؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل رقم الهاتف؟ (y/n): ").lower()

            if choice == 'y':
                new_phone = input("رقم الهاتف الجديد: ")

            choice = input("هل تريد تعديل رقم الهوية؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل رقم الهوية؟ (y/n): ").lower()

            if choice == 'y':
                new_id_number = input("رقم الهوية الجديد: ")
                while any(c.id_number == new_id_number and c.id != customer_id for c in self.customers):
                    print("رقم الهوية مسجل مسبقًا! يرجى إدخال رقم هوية آخر.")
                    new_id_number = input("رقم الهوية الجديد: ")

            # تحديث بيانات العميل مباشرة
            customer.name = new_name
            customer.id_number = new_id_number
            customer.phone_number = new_phone

            self.save_customers()
            print("تم التعديل بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def delete_customer(self, scanner):
        try:
            customer_id = int(input("أدخل رقم العميل: "))
            customer_to_delete = next((c for c in self.customers if c.id == customer_id), None)

            if customer_to_delete:
                self.customers.remove(customer_to_delete)
                self.save_customers()
                print("تم الحذف بنجاح!")
            else:
                print("العميل غير موجود!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def search_customer(self, scanner):
        try:
            choice = input("ابحث بـ (1-رقم العميل / 2-رقم الهوية): ")
            if choice == '1':
                customer_id = int(input("رقم العميل: "))
                customer = next((c for c in self.customers if c.id == customer_id), None)
                print(customer if customer else "لا يوجد عميل بهذا الرقم")
            else:
                id_num = input("رقم الهوية: ")
                customer = next((c for c in self.customers if c.id_number == id_num), None)
                print(customer if customer else "لا يوجد عميل بهذا الرقم")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")