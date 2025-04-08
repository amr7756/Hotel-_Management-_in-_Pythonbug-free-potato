import json
from room import Room

class RoomManager:
    def __init__(self):
        self.rooms = self.load_rooms()
        if self.rooms is None:
            self.rooms = []

    def load_rooms(self):
        try:
            with open('data/rooms.json', 'r', encoding='utf-8') as file:
                return [Room(**r) for r in json.load(file)]
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def save_rooms(self):
        with open('data/rooms.json', 'w', encoding='utf-8') as file:
            json.dump([room.__dict__ for room in self.rooms], file, ensure_ascii=False, indent=4)

    def generate_id(self):
        return 1 if not self.rooms else self.rooms[-1].id + 1

    def get_available_rooms(self):
        return [room for room in self.rooms if room.is_available]

    def update_room_availability(self, room_id, available):
        for room in self.rooms:
            if room.id == room_id:
                room.is_available = available
        self.save_rooms()

    def manage_rooms_admin(self, scanner):
        while True:
            try:
                print("\n*** إدارة الغرف ***")
                print("1. عرض الغرف")
                print("2. إضافة غرفة")
                print("3. تعديل غرفة")
                print("4. حذف غرفة")
                print("5. البحث عن غرفة")
                print("6. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_rooms()
                elif choice == '2':
                    self.add_room(scanner)
                elif choice == '3':
                    self.update_room(scanner)
                elif choice == '4':
                    self.delete_room(scanner)
                elif choice == '5':
                    self.search_room(scanner)
                elif choice == '6':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 6.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def manage_rooms_user(self, scanner):
        while True:
            try:
                print("\n*** إدارة الغرف ***")
                print("1. عرض الغرف")
                print("2. البحث عن غرفة")
                print("3. رجوع")
                choice = input("اختر الخيار: ")

                if choice == '1':
                    self.list_rooms()
                elif choice == '2':
                    self.search_room(scanner)
                elif choice == '3':
                    return
                else:
                    print("خيار غير صحيح! يرجى اختيار رقم من 1 إلى 3.")
            except Exception as e:
                print(f"حدث خطأ غير متوقع: {str(e)}")

    def list_rooms(self):
        if not self.rooms:
            print("لاتوجد غرف.")
        else:
            for room in self.rooms:
                print(room)

    def add_room(self, scanner):
        try:
            room_type = input("نوع الغرفة: ")
            price = float(input("السعر: "))
            new_room = Room(
                id=self.generate_id(),
                room_type=room_type,
                price=price,
                is_available=True
            )
            self.rooms.append(new_room)
            self.save_rooms()
            print("تم إضافة الغرفة بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def update_room(self, scanner):
        try:
            room_id = int(input("أدخل رقم الغرفة: "))
            room = next((r for r in self.rooms if r.id == room_id), None)

            if not room:
                print("الغرفة غير موجودة!")
                return

            new_type = room.room_type
            new_price = room.price
            new_availability = room.is_available

            choice = input("هل تريد تعديل نوع الغرفة؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل نوع الغرفة؟ (y/n): ").lower()

            if choice == 'y':
                new_type = input("النوع الجديد: ")

            choice = input("هل تريد تعديل سعر الغرفة؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل سعر الغرفة؟ (y/n): ").lower()

            if choice == 'y':
                new_price = float(input("السعر الجديد: "))

            choice = input("هل تريد تعديل حالة الغرفة (متاحة/غير متاحة)؟ (y/n): ").lower()
            while choice not in ['y', 'n']:
                print("إدخال غير صحيح! يرجى إدخال (y/n).")
                choice = input("هل تريد تعديل حالة الغرفة (متاحة/غير متاحة)؟ (y/n): ").lower()

            if choice == 'y':
                availability_input = input("هل الغرفة متاحة؟ (true/false): ").lower()
                while availability_input not in ['true', 'false']:
                    print("إدخال غير صحيح! يرجى إدخال true أو false فقط.")
                    availability_input = input("هل الغرفة متاحة؟ (true/false): ").lower()
                new_availability = availability_input == 'true'

            updated_room = Room(
                id=room_id,
                room_type=new_type,
                price=new_price,
                is_available=new_availability
            )
            self.rooms[self.rooms.index(room)] = updated_room
            self.save_rooms()
            print("تم التعديل بنجاح!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def delete_room(self, scanner):
        try:
            room_id = int(input("أدخل رقم الغرفة: "))
            if any(r.id == room_id for r in self.rooms):
                self.rooms = [r for r in self.rooms if r.id != room_id]
                self.save_rooms()
                print("تم الحذف بنجاح!")
            else:
                print("الغرفة غير موجودة!")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def search_room(self, scanner):
        try:
            room_id = int(input("أدخل رقم الغرفة: "))
            room = next((r for r in self.rooms if r.id == room_id), None)
            print(room if room else "لا توجد غرفة بهذا الرقم")
        except Exception as e:
            print(f"حدث خطأ غير متوقع: {str(e)}")

    def search_room_booking(self, room_id):
        return room_id if any(r.id == room_id for r in self.rooms) else 0

    def get_room_price(self, room_id):
        room = next((r for r in self.rooms if r.id == room_id), None)
        return room.price if room else 0.0