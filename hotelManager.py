from userManager import UserManager
from roomManager import RoomManager
from customerManager import CustomerManager
from bookingManager import BookingManager
from discountManager import DiscountManager

class HotelManager:
    def login(self):
        attempts = 4
        while attempts > 0:
            try:
                print("\n*** تسجيل الدخول ***")
                user_name = input("اسم المستخدم: ")
                password = input("كلمة المرور: ")

                user = UserManager().authenticate_user(user_name, password)

                if user:
                    if user.get_role() == "admin":
                        self.show_admin_menu()
                    else:
                        self.show_user_menu()
                    return
                else:
                    attempts -= 1
                    if attempts > 0:
                        print(f"\nبيانات الدخول غير صحيحة! تبقى لك من المحاولات: {attempts}\n")
                    else:
                        print("\nتم استنفاد جميع المحاولات! يرجى المحاولة لاحقًا.\n")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def show_admin_menu(self):
        while True:
            try:
                BookingManager().check_expired_bookings()
                DiscountManager().check_expired_discounts()
                print("\n*** القائمة الرئيسية ***")
                print("1. إدارة المستخدمين")
                print("2. إدارة الغرف")
                print("3. إدارة العملاء")
                print("4. إدارة الحجوزات")
                print("5. إدارة الخصومات")
                print("6. خروج")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    UserManager().manage_users(input)
                elif choice == '2':
                    RoomManager().manage_rooms_admin(input)
                elif choice == '3':
                    CustomerManager().manage_customers(input)
                elif choice == '4':
                    BookingManager().manage_bookings(input)
                elif choice == '5':
                    DiscountManager().manage_discounts_admin(input)
                elif choice == '6':
                    exit()
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 6.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def show_user_menu(self):
        while True:
            try:
                BookingManager().check_expired_bookings()
                DiscountManager().check_expired_discounts()
                print("\n*** القائمة الرئيسية ***")
                print("1. إدارة الغرف")
                print("2. إدارة العملاء")
                print("3. إدارة الحجوزات")
                print("4. إدارة الخصومات")
                print("5. خروج")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    RoomManager().manage_rooms_user(input)
                elif choice == '2':
                    CustomerManager().manage_customers(input)
                elif choice == '3':
                    BookingManager().manage_bookings(input)
                elif choice == '4':
                    DiscountManager().manage_discounts_user(input)
                elif choice == '5':
                    exit()
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 5.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")