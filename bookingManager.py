import json
from datetime import datetime, timedelta
from booking import Booking
from roomManager import RoomManager
from customerManager import CustomerManager
from discountManager import DiscountManager
from dateutil import parser


class BookingManager:
    def __init__(self):
        self.bookings = self.load_bookings()
        if self.bookings is None:
            self.bookings = []

    def load_bookings(self):
        try:
            with open('data/bookings.json', 'r', encoding='utf-8') as file:
                bookings_data = json.load(file)
                return [Booking(**b) for b in bookings_data]
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_bookings(self):
        with open('data/bookings.json', 'w', encoding='utf-8') as file:
            bookings_data = [{
                'booking_id': b.booking_id,
                'room_id': b.room_id,
                'customer_id': b.customer_id,
                'start_date': b.start_date.isoformat(),
                'end_date': b.end_date.isoformat(),
                'is_paid': b.is_paid,
                'total_price': b.total_price
            } for b in self.bookings]
            json.dump(bookings_data, file, ensure_ascii=False, indent=4)

    def manage_bookings(self, scanner):
        while True:
            try:
                print("\n*** إدارة الحجوزات ***")
                print("1. عرض الحجوزات")
                print("2. إضافة حجز")
                print("3. تعديل حجز")
                print("4. حذف حجز")
                print("5. البحث عن حجز")
                print("6. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_bookings()
                elif choice == '2':
                    self.add_booking(scanner)
                elif choice == '3':
                    self.update_booking(scanner)
                elif choice == '4':
                    self.delete_booking(scanner)
                elif choice == '5':
                    self.search_booking(scanner)
                elif choice == '6':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 6.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def list_bookings(self):
        if not self.bookings:
            print("لا توجد حجوزات.")
        else:
            for booking in self.bookings:
                print(booking)

    def add_booking(self, scanner):
        try:
            room_manager = RoomManager()
            customer_manager = CustomerManager()
            discount_manager = DiscountManager()

            available_rooms = room_manager.get_available_rooms()
            if not available_rooms:
                print("لا توجد غرف متاحة!")
                return

            customer_id = int(input("أدخل رقم العميل: "))
            while not any(c.id == customer_id for c in customer_manager.get_customers()):
                print("العميل غير مسجل! يرجى إدخال رقم عميل صحيح.")
                customer_id = int(input("أدخل رقم العميل: "))

            print("الغرف المتاحة:")
            for room in available_rooms:
                print(room)

            room_id = int(input("أدخل رقم الغرفة: "))
            while not any(r.id == room_id and r in available_rooms for r in room_manager.rooms):
                print("الغرفة غير صالحة! يرجى إدخال رقم غرفة من القائمة المعروضة.")
                room_id = int(input("أدخل رقم الغرفة: "))

            days = int(input("مدة الحجز بالأيام: "))
            room_price = room_manager.get_room_price(room_id)
            total_price = room_price * days

            discount = discount_manager.get_active_discount_for_room(room_id)
            if discount:
                total_price *= (1 - discount.percentage / 100)
                print(f"تم تطبيق خصم بنسبة {discount.percentage}%")

            print(f"السعر الإجمالي: {total_price}")

            is_paid_input = input("هل تم الدفع؟ (true/false): ").lower()
            while is_paid_input not in ['true', 'false']:
                print("إدخال غير صحيح! يرجى إدخال true أو false.")
                is_paid_input = input("هل تم الدفع؟ (true/false): ").lower()
            is_paid = is_paid_input == 'true'

            start_date = datetime.now()
            end_date = start_date + timedelta(days=days)

            new_booking = Booking(
                booking_id=self.generate_booking_id(),
                room_id=room_id,
                customer_id=customer_id,
                start_date=start_date,
                end_date=end_date,
                is_paid=is_paid,
                total_price=total_price
            )
            self.bookings.append(new_booking)
            room_manager.update_room_availability(room_id, False)
            self.save_bookings()
            print("تم الحجز بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def generate_booking_id(self):
        return 1 if not self.bookings else max(b.booking_id for b in self.bookings) + 1

    def check_expired_bookings(self):
        now = datetime.now()
        room_manager = RoomManager()

        for booking in self.bookings:
            if now > booking.end_date:
                room_manager.update_room_availability(booking.room_id, True)
                print(f"\nتم تحرير الغرفة رقم {booking.room_id}")

    def update_booking(self, scanner):
        try:
            booking_id = int(input("أدخل رقم الحجز: "))
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)

            if not booking:
                print("الحجز غير موجود!")
                return

            room_manager = RoomManager()
            discount_manager = DiscountManager()
            customer_manager = CustomerManager()

            # حفظ رقم الغرفة الأصلية قبل أي تعديلات
            original_room_id = booking.room_id

            new_customer_id = booking.customer_id
            new_room_id = booking.room_id
            new_days = (booking.end_date - booking.start_date).days
            new_is_paid = booking.is_paid

            choice = input("هل تريد تعديل رقم العميل؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل رقم العميل؟ (y/n): ").lower()

            if choice == 'y':
                new_customer_id = int(input("أدخل رقم العميل الجديد: "))
                while not any(c.id == new_customer_id for c in customer_manager.get_customers()):
                    print("العميل غير مسجل! يرجى إدخال رقم عميل صحيح.")
                    new_customer_id = int(input("أدخل رقم العميل الجديد: "))

            choice = input("هل تريد تعديل رقم الغرفة؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل رقم الغرفة؟ (y/n): ").lower()

            if choice == 'y':
                available_rooms = room_manager.get_available_rooms()
                # إضافة الغرفة الأصلية إلى القائمة المعروضة إذا كانت غير متاحة
                original_room = next(r for r in room_manager.rooms if r.id == original_room_id)
                if original_room not in available_rooms:
                    available_rooms.append(original_room)

                print("\nالغرف المتاحة للتعديل:")
                for room in available_rooms:
                    status = "(متاحة)" if room.is_available and room.id != original_room_id else "(محجوزة)"
                    if room.id == original_room_id:
                        status = "(الحالية - محجوزة)"
                    print(f"غرفة رقم: {room.id} | نوع: {room.room_type} | السعر: {room.price:.2f} {status}")

                new_room_id = int(input("\nأدخل رقم الغرفة الجديد: "))
                while not any(r.id == new_room_id for r in available_rooms):
                    print("الغرفة غير صالحة! يرجى إدخال رقم غرفة من القائمة المعروضة.")
                    new_room_id = int(input("أدخل رقم الغرفة الجديد: "))

            choice = input("هل تريد تعديل مدة الحجز؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل مدة الحجز؟ (y/n): ").lower()

            if choice == 'y':
                new_days = int(input("مدة الحجز الجديدة بالأيام: "))

            new_room_price = room_manager.get_room_price(new_room_id)
            new_total_price = new_room_price * new_days

            discount = discount_manager.get_active_discount_for_room(new_room_id)
            if discount:
                new_total_price *= (1 - discount.percentage / 100)
                print(f"تم تطبيق خصم بنسبة {discount.percentage}%")

            print(f"السعر الإجمالي الجديد: {new_total_price:.2f}")

            choice = input("هل تريد تعديل حالة الدفع؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل حالة الدفع؟ (y/n): ").lower()

            if choice == 'y':
                is_paid_input = input("هل تم الدفع؟ (true/false): ").lower()
                while is_paid_input not in ['true', 'false']:
                    print("إدخال غير صحيح! يرجى إدخال true أو false.")
                    is_paid_input = input("هل تم الدفع؟ (true/false): ").lower()
                new_is_paid = is_paid_input == 'true'

            new_end_date = booking.start_date + timedelta(days=new_days)

            # تحديث حالة الغرف إذا تغير رقم الغرفة
            if new_room_id != original_room_id:
                room_manager.update_room_availability(original_room_id, True)  # تحرير الغرفة القديمة
                room_manager.update_room_availability(new_room_id, False)  # حجز الغرفة الجديدة
                print(f"تم تحرير الغرفة {original_room_id} (أصبحت متاحة)")
                print(f"تم حجز الغرفة {new_room_id} (أصبحت غير متاحة)")
            else:
                # إذا لم تتغير الغرفة نتأكد من أنها محجوزة
                room_manager.update_room_availability(new_room_id, False)

            # تحديث بيانات الحجز
            booking.room_id = new_room_id
            booking.customer_id = new_customer_id
            booking.end_date = new_end_date
            booking.is_paid = new_is_paid
            booking.total_price = new_total_price

            self.save_bookings()
            print("تم التعديل بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def delete_booking(self, scanner):
        try:
            booking_id = int(input("أدخل رقم الحجز: "))
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)

            if booking:
                room_manager = RoomManager()
                room_manager.update_room_availability(booking.room_id, True)
                self.bookings.remove(booking)
                self.save_bookings()
                print("تم الحذف بنجاح!")
            else:
                print("الحجز غير موجود!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def search_booking(self, scanner):
        try:
            booking_id = int(input("أدخل رقم الحجز: "))
            booking = next((b for b in self.bookings if b.booking_id == booking_id), None)
            print(booking if booking else "الحجز غير موجود")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")