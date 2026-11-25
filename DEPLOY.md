# نشر رصد على الإنترنت: الدليل الكامل (10 خطوات)

## على جهازك
**1) القائمة الموثوقة** (من مجلد server، واسم ملف Tranco عندك قد يختلف، تعرفه بـ dir *.csv):
```
python make_allowlist.py top-1m.csv --n 10000
Select-String -Path allowlist.txt -Pattern "^bbc.com$"
```
(الأمر الثاني يتأكد أن bbc.com موجود، واكتبه كاملاً بكلمة Select-String.) ثم أعد تشغيل الخادم وجرّب instagram.com وbbc.com وgithub.com/login: كلها آمنة.

**2) تصغير النموذج** (يمنع مشكلة حد 100 ميغا في GitHub):
```
python compress_model.py
```
**3) تثبيت نسخ المكتبات** (يمنع مشاكل تحميل النموذج على الاستضافة):
```
python make_pins.py
```
سجّل سطر PYTHON_VERSION الذي يطبعه. وينشئ ملف requirements-deploy.txt.

**4) اختبار نهائي محلي:**
```
python -m unittest discover -s tests
```
لازم تنتهي بكلمة OK.

## GitHub
**5) رفع المشروع** (من مجلد rasd نفسه وليس server):
- أنشئ حساباً في github.com ثم مستودعاً جديداً اسمه rasd (بدون README).
- تأكد من Git: `git --version` (وإن لم يكن موجوداً ثبته من git-scm.com).
```
cd C:\Users\OFOQ\Desktop\rasd
git init
git add .
git status
git commit -m "Rasd"
git branch -M main
git remote add origin https://github.com/اسم_المستخدم/rasd.git
git push -u origin main
```
- في git status تأكد أن .env وملفات csv وrasd.db **ليست** في القائمة.
- لو طلب هوية: `git config --global user.name "اسمك"` و`git config --global user.email "ايميلك"` ثم أعد commit.

## Render (الخادم)
**6)** في render.com سجّل بحساب GitHub، ثم New + ← Web Service ← اختر مستودع rasd:
- Root Directory: `server`
- Build Command: `pip install -r requirements-deploy.txt`
- Start Command: `gunicorn app:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120`
- Instance Type: Free
- Environment (المتغيرات):
  - PYTHON_VERSION = (من الخطوة 3)
  - TELEGRAM_BOT_TOKEN = التوكن
  - TELEGRAM_CHAT_ID = الآيدي
  - FRONTEND_ORIGIN = *   (مؤقتاً)
  - ADMIN_KEY = مفتاح اللوحة (اختياري)
- اضغط Create Web Service وانتظر 5 إلى 10 دقائق حتى تظهر Your service is live.
- افتح `https://اسم-خدمتك.onrender.com/api/health` ← لازم `{"ok":true}`.
- لو انهار بسبب الذاكرة: أضف متغير DISABLE_ML = 1 (يعمل بدون النموذج، وتبقى القواعد والقاعدة).

## Netlify (الموقع)
**7)** افتح config.js وضع عنوان الخادم: `window.RASD_API = "https://اسم-خدمتك.onrender.com";` (بدون / في الآخر).
أنشئ مجلداً جديداً rasd-site وانسخ فيه 4 ملفات فقط: index.html وstyle.css وscript.js وconfig.js.
في netlify.com ← Add new site ← Deploy manually ← اسحب مجلد rasd-site ← يعطيك رابطاً https://xxxx.netlify.app

**8) أغلق الوصول** (CORS): في Render ← Environment ← غيّر FRONTEND_ORIGIN إلى رابط Netlify (بدون / في الآخر). تضيف `,http://127.0.0.1:5500` لو تريد الاختبار المحلي أيضاً. يعاد التشغيل تلقائياً.

## الاختبار والعرض
**9) اختبر من التلفون:** افتح رابط Netlify وافحص instagram.com ورابط احتيال ورسالة، وأرسل بلاغاً (يجب أن يصل تيليجرام).
ومن اللابتوب: `python check_online.py https://اسم-خدمتك.onrender.com` ← كل الأسطر OK.

**10) تجهيز العرض:**
- الخطة المجانية تنام بعد نحو 15 دقيقة، وأول طلب بعدها يأخذ نحو دقيقة. قبل المناقشة بعشر دقائق افتح /api/health وافحص رابطاً لتوقظها.
- جهّز نسخة احتياطية محلية (python app.py وLive Server) ولقطات شاشة.
- البوت يعمل فقط وأنت مشغل python bot.py على لابتوبك.
- إحصائيات اللوحة وقاعدة البيانات تُمسح عند إعادة تشغيل الخادم المجاني، والبلاغات تبقى في تيليجرام.

## مشاكل شائعة
| المشكلة | الحل |
| --- | --- |
| الموقع يظهر «تعذر الاتصال» | تأكد من config.js ومن عنوان الخادم، وأن FRONTEND_ORIGIN يطابق رابط Netlify حرفياً |
| أول فحص بطيء جداً | الخادم كان نائماً، انتظر دقيقة |
| فشل البناء على Render | انسخ آخر 20 سطراً من Logs |
| الخادم ينهار عند التشغيل | أضف DISABLE_ML=1 |
| رفض git push بسبب الحجم | شغّل compress_model.py ثم git add . وcommit من جديد |
