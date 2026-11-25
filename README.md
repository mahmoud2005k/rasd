# رصد (Rasd): كاشف الروابط والرسائل المشبوهة

نظام يفحص الرابط أو الرسالة ويعطي درجة خطورة من 100 مع الأسباب، بدون فتح الرابط.

## مكونات النظام
| الجزء | الملفات | الوظيفة |
| --- | --- | --- |
| الواجهة | index.html, style.css, script.js | فحص الرابط والرسائل، تسريب الحسابات، اختبار التوعية، عربي/إنجليزي |
| الخادم (Flask) | server/app.py | نقاط API: analyze, message, report, email-check, admin/stats |
| المحرك | server/engine.py | يجمع كل الفحوصات في تقرير واحد |
| القواعد | server/rules.py | قواعد الشكل: حروف مخفية، تطابق بصري، خطأ إملائي مقصود، ... |
| الذكاء الاصطناعي | server/features.py, train_model.py, ml.py | Stacking: Random Forest + XGBoost ثم Logistic Regression مع تفسير القرار |
| الدومين والصفحة | server/netinfo.py, page_analysis.py | عمر الدومين (RDAP/WHOIS)، DNS، وجهة نماذج الإدخال |
| الرسائل | server/messages.py, msg_data.py | عبارات النصب بالعربية والإنجليزية |
| بوت تيليجرام | server/bot.py | فحص الروابط والرسائل من تيليجرام |
| لوحة الإحصائيات | admin.html | أعداد الفحوص والبلاغات (تحتاج ADMIN_KEY) |
| إضافة المتصفح | extension/ | فحص الصفحة الحالية بضغطة زر |
| التقييم | server/evaluate_system.py, report_figures.py | أرقام ورسوم للتقرير |
| الاختبارات | server/tests/ | اختبارات تلقائية |

## التشغيل
```
cd server
python -m pip install -r requirements.txt
python app.py                 # الخادم  (http://127.0.0.1:5000)
python bot.py                 # بوت تيليجرام (نافذة ثانية)
python -m unittest discover -s tests -v    # الاختبارات
```
ثم افتح index.html بـ Live Server.

## تدريب النموذج وتقييمه
```
python train_model.py --csv malicious_phish.csv --url-col url --label-col type --phish-labels phishing --legit-labels benign --extra-phish suspicious_links.txt
python evaluate_system.py --csv malicious_phish.csv --n 2000
python report_figures.py --csv malicious_phish.csv --n 2000
```

## الخصوصية والأمان
- كلمة السر في فحص التسريب لا تغادر الجهاز (k-anonymity)، والبريد لا يُخزَّن.
- إحصائيات الفحص تخزّن الدومين والحكم والدرجة فقط، بدون الرابط الكامل وبدون عنوان IP.
- الفحص العميق يحجب الشبكات الداخلية ومحدود بعدد المرات.
- ملف .env (التوكن) لا يُرفع إلى GitHub.

## حدود النظام
الحكم تقديري. نموذج الروابط وحده بدقة نحو 80%، فلا يُستخدم وحده. التفاصيل في مستند الملخص.
