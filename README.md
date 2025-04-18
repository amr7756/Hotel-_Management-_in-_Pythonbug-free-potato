نظام إدارة الفندق - دليل شامل

جدول المحتويات

مقدمة عامة

الهيكل العام للنظام

المكونات البرمجية

هيكل تخزين البيانات

الوظائف التفصيلية

نظام إدارة المستخدمين

نظام إدارة الغرف

نظام إدارة العملاء

نظام إدارة الحجوزات

نظام إدارة الخصومات

الخصائص الفنية

دليل التثبيت

خطة التطوير

سياسات الاستخدام

استكشاف الأخطاء

مقدمة عامة:

نظام إدارة الفندق هو حل برمجي متكامل تم تطويره بلغة Python خصيصًا لإدارة العمليات اليومية في الفنادق. يعمل النظام عبر واجهة سطر الأوامر (CLI) ويقدم مجموعة متكاملة من الميزات المصممة لتبسيط عمليات الإدارة الفندقية بكفاءة عالية.

رابط المشروع على GitHub:

https://github.com/amr7756/Hotel-_Management-_in-_Pythonbug-free-potato.git

الهيكل العام للنظام:

المكونات البرمجية

نواة النظام الأساسية:

main.py: نقطة الدخول الرئيسية للتطبيق

hotelManager.py: الواجهة الإدارية الرئيسية

وحدات الإدارة المتخصصة:

userManager.py: إدارة المستخدمين والصلاحيات

roomManager.py: إدارة الغرف والفصول

customerManager.py: إدارة بيانات العملاء

bookingManager.py: إدارة الحجوزات والإقامات

discountManager.py: إدارة العروض والخصومات

نماذج البيانات:

user.py: نموذج بيانات المستخدم

room.py: نموذج بيانات الغرفة

customer.py: نموذج بيانات العميل

booking.py: نموذج بيانات الحجز

discount.py: نموذج بيانات الخصم

هيكل تخزين البيانات:

يستخدم النظام ملفات JSON منظمة في مجلد data/ لتخزين كافة المعلومات:

users.json: قاعدة بيانات المستخدمين

rooms.json: سجل الغرف

customers.json: سجل العملاء

bookings.json: سجل الحجوزات

discounts.json: سجل الخصومات

الوظائف التفصيلية

نظام إدارة المستخدمين

المصادقة والأمان:

نظام تسجيل دخول ثنائي الطبقات (مدير/موظف)

حد أقصى 4 محاولات تسجيل دخول

إدارة المستخدمين:

إضافة مستخدمين جدد مع تحديد الصلاحيات

تعديل بيانات المستخدمين (الاسم، كلمة المرور، الصلاحيات)

حذف المستخدمين من النظام

البحث عن المستخدمين (بالرقم أو الاسم)

عرض قائمة كاملة بالمستخدمين

نظام إدارة الغرف

إدارة الغرف الأساسية:

تسجيل غرف جديدة (النوع، السعر)

تعديل بيانات الغرف (السعر، الحالة، النوع)

حذف الغرف من النظام

البحث عن الغرف (بالرقم)

تتبع حالة الغرف:

عرض الغرف المتاحة

عرض الغرف المحجوزة

تحديث حالة الغرف تلقائيًا عند الحجز أو الإلغاء

نظام إدارة العملاء

سجل العملاء:

تسجيل عملاء جدد (الاسم، رقم الهوية، معلومات الاتصال)

تعديل بيانات العملاء

حذف سجلات العملاء

البحث عن العملاء (بالرقم أو رقم الهوية)

إدارة العلاقات:

تتبع تاريخ حجوزات العميل

نظام إدارة الحجوزات

عملية الحجز الكاملة:

إنشاء حجوزات جديدة (اختيار غرفة، عميل، فترة الإقامة)

تعديل الحجوزات (تغيير الغرفة، تمديد الإقامة)

إلغاء الحجوزات

البحث عن الحجوزات (برقم الحجز)

المعالجة التلقائية:

تطبيق الخصومات تلقائيًا

تحرير الغرف تلقائيًا عند انتهاء مدة الحجز

نظام إدارة الخصومات

أنواع الخصومات:

خصومات عامة (تنطبق على جميع الغرف)

خصومات خاصة (لغرف محددة)

إدارة الخصومات:

إضافة خصومات جديدة (النسبة، الفترة الزمنية، الغرف المستهدفة)

تعديل الخصومات الحالية

حذف الخصومات المنتهية

البحث عن الخصومات

المعالجة الذكية:

تنبيهات لانتهاء صلاحية الخصومات

الخصائص الفنية

معمارية النظام

تصميم نمطية (Modular Design) يسهل الصيانة والتطوير

فصل واضح بين واجهة المستخدم والمنطق وقاعدة البيانات

معالجة شاملة للاستثناءات والأخطاء

إدارة البيانات

نظام تخزين بيانات يعتمد على JSON

آلية نسخ احتياطي تلقائي

تحقق من تكامل البيانات

واجهة المستخدم

واجهة باللغة العربية

قوائم تفاعلية سهلة الاستخدام

توجيهات واضحة لكل عملية

تنسيق موحد لعرض البيانات

دليل التثبيت

المتطلبات النظامية

نظام تشغيل: Windows/Linux/macOS

إصدار Python: 3.8 أو أحدث

المكتبات المطلوبة: python-dateutil

خطوات التنصيب

استنساخ المستودع:

git clone https://github.com/amr7756/Hotel-_Management-_in-_Pythonbug-free-potato.git
cd Hotel-_Management-_in-_Pythonbug-free-potato

تثبيت المتطلبات:
pip install python-dateutil

تشغيل النظام:
python main.py

بيانات الدخول الافتراضية

الدور	اسم المستخدم	كلمة المرور

المدير	admin	1234

الموظف	user	1234


خطة التطوير

التحسينات المخطط لها

تطوير واجهة رسومية باستخدام Tkinter/PyQt

دعم قواعد البيانات (SQLite/MySQL)

نظام تقارير وإحصائيات متقدم

دعم تعدد اللغات

ميزات مقترحة

إمكانية إضافة ملاحظات خاصة لكل عميل

نظام الفواتير الإلكترونية

تكامل مع أنظمة الدفع الإلكتروني

تطبيق جوال للموظفين

نظام إشعارات (بريد إلكتروني/رسائل نصية)

سياسات الاستخدام

شروط الاستخدام

يخضع النظام لرخصة MIT

يسمح بالتعديل والتوزيع مع الحفاظ على حقوق الملكية

لا يتحمل المطور مسؤولية أي أضرار ناتجة عن الاستخدام

إرشادات المساهمة

الإبلاغ عن المشكلات عبر نظام Issues

اقتراح تحسينات عبر Pull Requests

اتباع دليل نمط البرمجة المحدد

كتابة توثيق كافي لأي إضافة جديدة

استكشاف الأخطاء

مشكلة في ملفات JSON: يمكن حذفها وسيتم إنشاؤها تلقائيًا

تثبيت المتطلبات:

pip install -r requirements.txt

أخطاء في التواريخ: تحقق من تثبيت مكتبة python-dateutil
