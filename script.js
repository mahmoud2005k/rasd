const T = {
  ar: {
    brand:"رصد", badge:"تحليل فوري للروابط", title:"افحص الرابط قبل أن تفتحه",
    sub:"رصد يحلّل الروابط والمواقع المشبوهة ويكشف محاولات الاحتيال، لتبقى بياناتك وأموالك في أمان.",
    check:"افحص", hint:"لا يتم فتح الرابط أبداً، التحليل يتم على شكله وبنيته.",
    why:"أسباب الحكم", details:"تفاصيل الرابط",
    note:"هذه نتيجة تقديرية مبنية على تحليل شكل الرابط وليست ضماناً كاملاً. إذا شككت فلا تدخل أي بيانات.",
    repT:"أبلغ عن رابط مشبوه", send:"إرسال البلاغ", rn:"ملاحظات (اختياري)", rok:"تم حفظ بلاغك، شكراً لمساهمتك.", rerr:"تعذر إرسال البلاغ، حاول لاحقاً.",
    types:["تصيد (يطلب بيانات)","احتيال مالي","برمجيات خبيثة","انتحال جهة معروفة","أخرى"],
    tipT:"نصائح للحماية",
    tips:["لا تدخل كلمة السر إلا بعد التأكد من الدومين.","البنوك لا تطلب بياناتك عبر روابط الرسائل.","احذر الروابط المختصرة والعروض المبالغ فيها.","فعّل التحقق بخطوتين في حساباتك."],
    bad:"خطير", mid:"مشبوه", safe:"يبدو آمناً",
    vb:"احذر بشدة ولا تفتح الرابط.", vm:"فيه علامات مريبة، تأكد قبل المتابعة.", vs:"لم نجد علامات خطر واضحة.",
    empty:"اكتب رابطاً صحيحاً أولاً.",
    f:{proto:"البروتوكول",host:"الدومين",tld:"الامتداد",path:"المسار",len:"طول الرابط",sub:"الدومينات الفرعية",age:"عمر الدومين",vis:"الرابط مع كشف الرموز المخفية",ml:"احتمال الاحتيال (نموذج الذكاء الاصطناعي)",dns:"استجابة DNS"},
    r:{nohttps:"لا يستخدم تشفير HTTPS.",https:"يستخدم HTTPS (لكن هذا وحده لا يعني الأمان).",ip:"يستخدم عنوان IP بدل اسم دومين.",puny:"دومين بحروف مموهة (Punycode) قد تقلد موقعاً آخر.",at:"فيه رمز @ يخفي الوجهة الحقيقية.",tld:"امتداد دومين شائع في الاحتيال: ",short:"رابط مختصر يخفي الوجهة الحقيقية.",sub:"دومينات فرعية كثيرة قد تخفي الدومين الحقيقي.",len:"رابط طويل بشكل غير عادي.",hy:"شرطات كثيرة في الدومين.",dg:"أرقام كثيرة أو استبدال حروف بأرقام في الدومين.",brand:"يقلد اسم جهة معروفة وهو ليس موقعها الرسمي: ",kw:"كلمات تستدرج الضحية: ",port:"منفذ غير معتاد في الرابط.",enc:"ترميز كثيف في الرابط.",clean:"بنية الرابط تبدو عادية.",known:"الرابط موجود في قاعدة الروابط المشبوهة المعروفة. المصدر: ",rep:"بلّغ عنه مستخدمون من قبل. عدد البلاغات: ",charrep:"حروف مكررة بشكل غير طبيعي في الدومين (مثل gooogle).",random:"اسم الدومين يبدو عشوائياً (حروف وأرقام بلا معنى)، وهذا شائع في دومينات الاحتيال.",cons:"سلسلة طويلة من الحروف الساكنة لا تشبه كلمة حقيقية.",longhost:"اسم الدومين طويل بشكل مبالغ فيه.",file:"الرابط يشير إلى ملف تنفيذي أو ملف تثبيت: ",archive:"الرابط يشير إلى ملف مضغوط: ",redir:"الرابط يحمل رابطاً آخر بداخله (إعادة توجيه مخفية).",typo:"اسم الدومين قريب جداً من اسم جهة معروفة (خطأ إملائي يبدو مقصوداً): ",brandpath:"اسم جهة معروفة داخل مسار الرابط وليس في دومينها الرسمي: ",newdom:"الدومين حديث الإنشاء (عمره بالأيام): ",olddom:"الدومين قديم ومستقر (عمره بالأيام): ",invisible:"الرابط يحتوي أحرفاً أو مسافات مخفية غير مرئية (تُستخدم لتمويه الرابط): ",homograph:"حروف من أبجديات مختلفة تشبه اللاتينية (كيريلي أو يوناني) داخل نفس الاسم، وهذا هجوم تطابق بصري.",symbols:"رموز خاصة كثيرة في الرابط."},
    deepL:"فحص عميق: جلب الصفحة وتحليل وجهة نماذج الإدخال (اختياري)", dnsY:"يستجيب", dnsN:"لا يستجيب",
    quizT:"اختبر نفسك: احتيال أم آمن؟", quizSub:"عشرة أمثلة (روابط ورسائل). اختر الحكم ثم اقرأ التفسير.", qSafe:"آمن", qScam:"احتيال",
    qNext:"التالي", qOk:"إجابة صحيحة", qNo:"إجابة خاطئة", qQ:"السؤال", qDone:"انتهى الاختبار. نتيجتك:", qAgain:"أعد الاختبار", qFake:"أمثلة مكتوبة للتدريب وليست روابط للضغط.",
    msgT:"فحص الرسالة", msgSub:"الصق رسالة SMS أو واتساب كاملة. يستخرج رصد الروابط منها ويكشف أساليب النصب في النص مثل الجوائز والاستعجال وطلب رمز التحقق.",
    msgPh:"الصق الرسالة هنا...", msgBtn:"افحص الرسالة", msgEmpty:"الصق نص الرسالة أولاً.", msgFlags:"علامات في نص الرسالة", msgLinks:"الروابط في الرسالة", msgNone:"لم نجد علامات احتيال واضحة في هذه الرسالة.", msgNoLink:"لا توجد روابط في الرسالة.",
    cat:{prize:"وعد بجائزة أو ربح: ",urg:"استعجال أو تهديد بإيقاف الحساب: ",data:"طلب بيانات حساسة (رمز تحقق أو كلمة سر): ",money:"كلام عن رصيد أو مال أو استثمار: ",brand:"ذكر جهة معروفة، تأكد أنها المرسل الحقيقي: "},
    leakT:"فحص تسريب الحسابات", leakSub:"اكتشف إن كان بريد أو كلمة سر ظهرا في تسريبات بيانات معروفة، وهذا أول مؤشر على اختراق حساب موظف أو حساب شخصي.",
    emL:"البريد الإلكتروني", pwL:"كلمة السر", pwHint:"كلمة السر لا تغادر جهازك، يُرسل فقط جزء صغير من بصمتها المشفرة.",
    leakNote:"افحص بريدك أنت أو بريد موظف بموافقته فقط. البريد لا يُحفظ عندنا. النتيجة لا تعني بالضرورة أن الحساب مخترق الآن، لكنها تعني أن بياناته ظهرت في تسريب، فغيّر كلمة السر وفعّل التحقق بخطوتين.",
    checking:"جارٍ الفحص...", emBad:"اكتب بريداً إلكترونياً صحيحاً.", emNoApi:"الخادم غير متصل، شغّله أولاً.",
    emSafe:"لم نجد هذا البريد في التسريبات المعروفة.", emFound:"البريد ظهر في {n} تسريب:", emAdvice:"غيّر كلمة السر في هذه المواقع وأي موقع تكررها فيه، وفعّل التحقق بخطوتين.",
    emLimit:"محاولات كثيرة، حاول بعد قليل.", emErr:"تعذر الفحص الآن، حاول لاحقاً.",
    pwEmpty:"اكتب كلمة السر أولاً.", pwSafe:"لم نجد كلمة السر هذه في التسريبات المعروفة.", pwFound:"كلمة السر هذه ظهرت {n} مرة في تسريبات. لا تستخدمها أبداً.", pwErr:"تعذر الفحص الآن (قد يتطلب اتصالاً آمناً أو إنترنت)."
  },
  en: {
    brand:"Rasd", badge:"Instant link analysis", title:"Inspect a link before you open it",
    sub:"Rasd analyzes suspicious links and websites and exposes scam attempts, so your data and money stay safe.",
    check:"Scan", hint:"The link is never opened; analysis is based on its structure.",
    why:"Why this verdict", details:"Link details",
    note:"This is an estimate based on link structure, not a full guarantee. If in doubt, do not enter any data.",
    repT:"Report a suspicious link", send:"Submit report", rn:"Notes (optional)", rok:"Your report was saved. Thank you for helping.", rerr:"Could not send the report, try again later.",
    types:["Phishing (asks for data)","Financial scam","Malware","Brand impersonation","Other"],
    tipT:"Safety tips",
    tips:["Only enter passwords after verifying the domain.","Banks never ask for your data through message links.","Beware of shortened links and too-good offers.","Turn on two-step verification on your accounts."],
    bad:"Dangerous", mid:"Suspicious", safe:"Looks safe",
    vb:"High risk. Do not open this link.", vm:"Some red flags. Verify before continuing.", vs:"No clear warning signs found.",
    empty:"Please enter a valid link first.",
    f:{proto:"Protocol",host:"Domain",tld:"Extension",path:"Path",len:"Link length",sub:"Subdomains",age:"Domain age",vis:"Link with hidden characters revealed",ml:"Scam probability (AI model)",dns:"DNS response"},
    r:{nohttps:"Does not use HTTPS encryption.",https:"Uses HTTPS (but that alone does not mean it is safe).",ip:"Uses an IP address instead of a domain name.",puny:"Disguised characters (Punycode) that may mimic another site.",at:"Contains @ which hides the real destination.",tld:"Extension common in scams: ",short:"URL shortener hides the real destination.",sub:"Many subdomains may hide the real domain.",len:"Unusually long link.",hy:"Many hyphens in the domain.",dg:"Many digits or letter-to-digit swaps in the domain.",brand:"Imitates a known brand but is not its official site: ",kw:"Lure words found: ",port:"Unusual port in the link.",enc:"Heavy encoding in the link.",clean:"Link structure looks normal.",known:"This link is in the known suspicious links database. Source: ",rep:"Users reported it before. Reports: ",charrep:"Unnaturally repeated characters in the domain (like gooogle).",random:"The domain name looks random (meaningless letters and digits), common in scam domains.",cons:"Long run of consonants that does not look like a real word.",longhost:"Excessively long domain name.",file:"The link points to an executable or installer file: ",archive:"The link points to a compressed file: ",redir:"The link carries another link inside it (hidden redirect).",typo:"The domain name is very close to a known brand (a deliberate-looking typo): ",brandpath:"A known brand name appears in the path, not in its official domain: ",newdom:"The domain is newly registered (age in days): ",olddom:"The domain is old and established (age in days): ",invisible:"The link contains invisible characters or spaces (used to disguise the link): ",homograph:"Letters from different alphabets that look Latin (Cyrillic or Greek) inside one name, a visual look-alike (homograph) attack.",symbols:"Many special symbols in the link."},
    deepL:"Deep scan: fetch the page and analyze where its input forms send data (optional)", dnsY:"Resolves", dnsN:"Does not resolve",
    quizT:"Test yourself: scam or safe?", quizSub:"Ten examples (links and messages). Pick a verdict, then read the explanation.", qSafe:"Safe", qScam:"Scam",
    qNext:"Next", qOk:"Correct", qNo:"Wrong", qQ:"Question", qDone:"Quiz finished. Your score:", qAgain:"Try again", qFake:"Practice examples written as text, not links to click.",
    msgT:"Message check", msgSub:"Paste a full SMS or WhatsApp message. Rasd extracts its links and detects scam tactics in the text, like prizes, urgency and requests for verification codes.",
    msgPh:"Paste the message here...", msgBtn:"Check message", msgEmpty:"Paste the message text first.", msgFlags:"Signs in the message text", msgLinks:"Links in the message", msgNone:"No clear scam signs found in this message.", msgNoLink:"No links in the message.",
    cat:{prize:"Promise of a prize or winnings: ",urg:"Urgency or threat of account suspension: ",data:"Asks for sensitive data (verification code or password): ",money:"Talks about credit, money or investment: ",brand:"Mentions a known organization, verify it is the real sender: "},
    leakT:"Account leak check", leakSub:"Find out whether an email or password appeared in known data leaks, a first sign that an employee or personal account may be compromised.",
    emL:"Email address", pwL:"Password", pwHint:"Your password never leaves your device; only a small part of its hash is sent.",
    leakNote:"Check your own email, or an employee’s with their consent. We do not store the email. A result does not necessarily mean the account is hacked right now, but its data appeared in a leak, so change the password and turn on two-step verification.",
    checking:"Checking...", emBad:"Enter a valid email address.", emNoApi:"The server is not connected, start it first.",
    emSafe:"This email was not found in known leaks.", emFound:"This email appeared in {n} leaks:", emAdvice:"Change the password on these sites and anywhere you reused it, and turn on two-step verification.",
    emLimit:"Too many attempts, try again shortly.", emErr:"Could not check right now, try later.",
    pwEmpty:"Enter a password first.", pwSafe:"This password was not found in known leaks.", pwFound:"This password appeared {n} times in leaks. Never use it.", pwErr:"Could not check right now (needs a secure connection and internet)."
  }
};

const BRANDS = {paypal:"paypal.com",google:"google.com",facebook:"facebook.com",instagram:"instagram.com",whatsapp:"whatsapp.com",telegram:"telegram.org",apple:"apple.com",microsoft:"microsoft.com",amazon:"amazon.com",netflix:"netflix.com",binance:"binance.com",libyana:"libyana.ly",almadar:"almadar.ly",tiktok:"tiktok.com",twitter:"twitter.com",youtube:"youtube.com",gmail:"gmail.com",outlook:"outlook.com",linkedin:"linkedin.com",snapchat:"snapchat.com",aliexpress:"aliexpress.com",spotify:"spotify.com",mastercard:"mastercard.com"};
const OFFICIAL = ["microsoft.com","microsoftonline.com","live.com","office.com","google.com","googleusercontent.com","googleapis.com","facebook.com","fb.com","instagram.com","whatsapp.com","whatsapp.net","amazon.com","amazonaws.com","apple.com","icloud.com","paypal.com","paypal.me","netflix.com","telegram.org","t.me","tiktok.com","binance.com","twitter.com","x.com","libyana.ly","almadar.ly","youtube.com","gmail.com","outlook.com","linkedin.com","snapchat.com","aliexpress.com","spotify.com","mastercard.com"];
const lev = (a, b) => {   // edit distance (insert / delete / replace / swap)
  const m = a.length, n = b.length, d = Array.from({ length: m + 1 }, (_, i) => [i, ...Array(n).fill(0)]);
  for (let j = 1; j <= n; j++) d[0][j] = j;
  for (let i = 1; i <= m; i++) for (let j = 1; j <= n; j++) {
    d[i][j] = Math.min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + (a[i - 1] === b[j - 1] ? 0 : 1));
    if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) d[i][j] = Math.min(d[i][j], d[i - 2][j - 2] + 1);
  }
  return d[m][n];
};
const INVIS = /[\u200B-\u200F\u202A-\u202E\u2060-\u2064\u2066-\u2069\uFEFF\u00AD\u180E\u00A0\u2000-\u200A\u3000]/g;
const BADTLD = ["xyz","top","click","icu","gq","tk","ml","cf","ga","work","loan","zip","mov","rest","cam","monster","buzz"];
const SHORT = ["bit.ly","tinyurl.com","t.co","cutt.ly","is.gd","rb.gy","shorturl.at","goo.gl","ow.ly","tiny.cc"];
const KW = ["login","signin","verify","secure","update","account","password","bank","wallet","gift","prize","free","bonus","confirm","suspend","urgent","claim","otp"];

// ضع هنا رابط الخادم بعد رفعه، مثال: "https://rasd-api.onrender.com". اتركه فارغاً للعمل بدون خادم.
const API = (window.RASD_API || "http://127.0.0.1:5000").replace(/\/$/, "");   // set in config.js

let L = "ar", last = null;
const $ = id => document.getElementById(id);

function setLang(l) {
  L = l;
  const t = T[l];
  document.documentElement.lang = l;
  document.documentElement.dir = l === "ar" ? "rtl" : "ltr";
  document.querySelectorAll("[data-i]").forEach(e => {
    const v = t[e.dataset.i];
    if (typeof v === "string") e.textContent = v;
  });
  $("lang").textContent = l === "ar" ? "English" : "العربية";
  $("rn").placeholder = t.rn;
  $("msgIn").placeholder = t.msgPh;
  $("rt").innerHTML = t.types.map((x, i) => `<option value="${i}">${x}</option>`).join("");
  $("tips").innerHTML = t.tips.map(x => `<div>${x}</div>`).join("");
  document.title = l === "ar" ? "رصد | Rasd" : "Rasd | رصد";
  if (last) render(last);
  if (typeof renderQuiz === "function") renderQuiz();
}

function analyze(raw) {
  let s = raw.trim();
  if (!s) return null;
  const hadScheme = /^[a-z][a-z0-9+.-]*:\/\//i.test(s);
  if (!hadScheme) s = "http://" + s;
  let u;
  try { u = new URL(s); } catch (e) { return null; }
  if (!u.hostname.includes(".") && !u.hostname.startsWith("[")) return null;

  const h = u.hostname.toLowerCase(), parts = h.split("."), tld = parts[parts.length - 1];
  const base = parts.slice(-2).join("."), subs = Math.max(0, parts.length - 2);
  const rs = []; let sc = 0;
  const add = (k, pts, sev, x = "") => { sc += pts; rs.push({ k, sev, x }); };

  // ---- أحرف مخفية وهجمات التطابق البصري: تُفحص على النص الأصلي قبل أن يعدّله المتصفح ----
  const t0 = raw.trim();
  let vis;
  const inv = t0.match(INVIS) || [];
  if (inv.length) {
    const hex = c => "U+" + c.charCodeAt(0).toString(16).toUpperCase().padStart(4, "0");
    add("invisible", 35, "h", [...new Set(inv.map(hex))].join(", "));
    vis = t0.replace(INVIS, c => "⟦" + hex(c) + "⟧");
  }
  const hostRaw = t0.replace(/^[a-z][a-z0-9+.-]*:\/\//i, "").split(/[\/?#]/)[0].replace(/^.*@/, "").replace(/:\d+$/, "").replace(INVIS, "");
  if (hostRaw.split(".").some(l => /[a-z]/i.test(l) && /[\u0370-\u03FF\u0400-\u04FF]/.test(l))) add("homograph", 40, "h");
  if ((t0.match(/[!$'()*+,;~|\\^`{}\[\]<>]/g) || []).length >= 3) add("symbols", 8, "m");

  if (hadScheme && u.protocol === "http:") add("nohttps", 15, "m");   // only when http:// was typed on purpose
  else if (hadScheme) add("https", 0, "g");
  if (/^\d{1,3}(\.\d{1,3}){3}$/.test(h) || h.startsWith("[")) add("ip", 30, "h");
  if (h.includes("xn--")) add("puny", 25, "h");
  if (s.includes("@") && u.username) add("at", 25, "h");
  if (BADTLD.includes(tld)) add("tld", 15, "m", "." + tld);
  if (SHORT.includes(base)) add("short", 20, "m");
  if (subs >= 3) add("sub", 15, "m");
  if (raw.length > 100) add("len", 10, "m");

  const name = parts.slice(0, -1).join(".");
  if ((name.replace(/xn--/g, "").match(/-/g) || []).length >= 3) add("hy", 10, "m");
  if ((name.match(/\d/g) || []).length >= 4 || /[a-z]\d[a-z]/.test(name)) add("dg", 12, "m");

  const flat = name.replace(/0/g, "o").replace(/1/g, "l").replace(/3/g, "e").replace(/\$/g, "s").replace(/rn/g, "m").replace(/vv/g, "w");
  for (const b in BRANDS) {
    if (flat.includes(b) && base !== BRANDS[b] && !h.endsWith("." + BRANDS[b]) && !OFFICIAL.includes(base)) { add("brand", 35, "h", b); break; }
  }
  const found = KW.filter(k => (h + u.pathname + u.search).toLowerCase().includes(k));
  if (found.length) add("kw", Math.min(24, found.length * 8), found.length > 1 ? "h" : "m", found.slice(0, 4).join(", "));
  if (u.port && !["80", "443"].includes(u.port)) add("port", 10, "m");
  if ((s.match(/%[0-9a-f]{2}/gi) || []).length > 5) add("enc", 8, "m");

  // ---- قواعد ذكية: أنماط النص داخل الرابط ----
  const label = parts.slice(0, -1).sort((a, b) => b.length - a.length)[0] || "";
  const rep = name.replace(/^www\./, "");
  if (/([a-z])\1\1|([0-9])\2{3,}/.test(rep)) add("charrep", 10, "m");

  const entropy = t => {
    const m = {};
    for (const c of t) m[c] = (m[c] || 0) + 1;
    return -Object.values(m).reduce((a, n) => a + (n / t.length) * Math.log2(n / t.length), 0);
  };
  const letters = label.replace(/[^a-z]/g, "");
  const consRatio = letters.replace(/[aeiouy]/g, "").length / Math.max(1, letters.length);
  if (!label.startsWith("xn--") && label.length >= 10 && entropy(label) >= 3.4 && (/\d/.test(label) || consRatio > 0.8)) add("random", 15, "m");
  if (/[bcdfghjklmnpqrstvwxz]{6,}/.test(label)) add("cons", 10, "m");
  if (h.length > 30) add("longhost", 8, "m");

  const ex = u.pathname.match(/\.(exe|apk|scr|bat|msi|vbs|jar|cmd|ps1|iso|dmg)$/i);
  const ar = u.pathname.match(/\.(zip|rar|7z)$/i);
  if (ex) add("file", 25, "h", "." + ex[1].toLowerCase());
  else if (ar) add("archive", 10, "m", "." + ar[1].toLowerCase());
  if (/https?(:|%3a)(\/\/|%2f%2f)/i.test(u.search)) add("redir", 15, "m");

  const lowPath = (u.pathname + u.search).toLowerCase();
  if (!rs.some(r => r.k === "brand")) {
    for (const b in BRANDS) {
      if (lowPath.includes(b) && base !== BRANDS[b] && !h.endsWith("." + BRANDS[b]) && !OFFICIAL.includes(base)) { add("brandpath", 15, "m", b); break; }
    }
  }


  // ---- انتحال بخطأ إملائي مقصود: اسم قريب جداً من علامة معروفة (instagrarm بدل instagram) ----
  if (!rs.some(r => r.k === "brand") && !OFFICIAL.includes(base)) {
    const toks = name.replace(/^www\./, "").split(/[.\-_]/).filter(x => x.length >= 6);
    for (const b in BRANDS) {
      if (b.length < 5) continue;
      const lim = b.length <= 8 ? 1 : 2;
      const hit = toks.find(x => x !== b && Math.abs(x.length - b.length) <= lim && lev(x, b) <= lim);
      if (hit) { add("typo", 30, "m", hit + " → " + b); break; }
    }
  }

  if (rs.every(r => r.sev === "g")) rs.push({ k: "clean", sev: "g", x: "" });

  sc = Math.min(100, sc);
  return { sc, rs, d: { proto: u.protocol.replace(":", ""), host: h, tld: "." + tld, path: (u.pathname + u.search) || "/", len: raw.length, sub: subs, ...(vis ? { vis } : {}) } };
}

// ===== فحص الرسائل: دوال نقية =====
const normAr = x => String(x).toLowerCase()
  .replace(/[\u064B-\u0652\u0640]/g, "")
  .replace(/[أإآ]/g, "ا").replace(/ى/g, "ي").replace(/ة/g, "ه").replace(/[ئ]/g, "ي").replace(/[ؤ]/g, "و")
  .replace(/[٠-٩]/g, c => String("٠١٢٣٤٥٦٧٨٩".indexOf(c)));
const CATS = {
  prize: { pts: 20, sev: "m", w: ["فزت","مبروك","ربحت","جائزة","اربح","هدية مجانية","سحب","you won","winner","prize","congratulations","lottery","ربحت معنا","ربحت معانا","تم اختيارك","جائزة نقدية","سحب يومي","you have been selected","gift card"] },
  urg:   { pts: 20, sev: "m", w: ["عاجل","فوراً","خلال 24 ساعة","سيتم إيقاف","تم إيقاف","تم تعليق","تم حظر","سيتم حظر","سيتم إغلاق","آخر فرصة","urgent","suspended","within 24 hours","last chance","immediately","تنبيه أمني","سيتم تجميد","تجميد حسابك","ينتهي اليوم","قبل انتهاء","security alert","act now","verify now"] },
  data:  { pts: 35, sev: "h", w: ["رمز التحقق","كلمة السر","كلمة المرور","الرقم السري","رقم البطاقة","أرسل الرمز","ادخل بياناتك","حدث بياناتك","تحديث بياناتك","تأكيد بياناتك","رقم الحساب","otp","cvv","pin","verify your","confirm your","password","كود التفعيل","رمز التفعيل","أرسل الكود","ادخل الرمز","صورة الهوية","تأكيد الهوية","your code","login to"] },
  money: { pts: 10, sev: "m", w: ["رصيد","شحن مجاني","حوالة","تحويل","بطاقة","تم خصم","أرباح","استثمار","تداول","عملة رقمية","free credit","bonus","investment","crypto","transfer","أرباح يومية","ربح مضمون","ضاعف أموالك","مضاعفة أموالك","حوالة مالية","double your"] },
  brand: { pts: 5,  sev: "g", w: ["ليبيانا","المدار","ليبيا للاتصالات","سداد","المصرف","مصرف","البريد","فيسبوك","واتساب","انستقرام","تيك توك","باي بال","paypal","facebook","whatsapp","instagram","netflix","binance","مصرف الجمهورية","المصرف التجاري الوطني","مصرف الوحدة","مصرف الصحاري","مصرف شمال أفريقيا","ليبيا للاتصالات والتقنية","جوجل","قوقل","جيميل","يوتيوب","سناب شات","تيليجرام","gmail","youtube","snapchat","telegram","linkedin","amazon","apple","microsoft"] }
};
const TLDS = "com|net|org|ly|info|xyz|top|click|icu|app|io|me|co|tk|ml|cf|ga|gq|biz|online|site|link|live|shop|cc|ru|cn|work|loan|zip|mov|rest|cam|monster|buzz";
const LINK_RE = new RegExp("(?:https?:\\/\\/|www\\.)[^\\s<>\"'،]+|\\b(?:[a-z0-9-]+\\.)+(?:" + TLDS + ")\\b(?:\\/[^\\s<>\"'،]*)?", "gi");

function extractLinks(text) {
  const out = [];
  for (let m of text.match(LINK_RE) || []) {
    m = m.replace(/[.,;:!?)\]}،؟]+$/, "");
    if (m && !out.includes(m)) out.push(m);
  }
  return out;
}

function hasPhrase(txt, ph) {
  const p = normAr(ph);
  return /^[a-z0-9 ]+$/.test(p) ? new RegExp("\\b" + p + "\\b").test(txt) : txt.includes(p);
}

function scanMessage(text) {
  const txt = normAr(text), cats = []; let score = 0;
  for (const k in CATS) {
    const found = CATS[k].w.filter(w => hasPhrase(txt, w));
    if (found.length) { cats.push({ k, words: found.slice(0, 4) }); if (k !== "brand") score += CATS[k].pts; }
  }
  const links = extractLinks(text);
  if (cats.some(c => c.k === "brand") && (links.length || score > 0)) score += CATS.brand.pts;
  return { cats, score, links };
}

let timer;
function render(a) {
  const t = T[L], lvl = a.sc >= 50 ? "bad" : a.sc >= 20 ? "mid" : "safe";
  const col = { bad: "var(--bad)", mid: "var(--warn)", safe: "var(--ok)" }[lvl];
  $("res").classList.remove("hidden");
  $("vd").textContent = t[lvl];
  $("vd").className = "verdict " + lvl;
  $("vs").textContent = lvl === "bad" ? t.vb : lvl === "mid" ? t.vm : t.vs;
  $("arc").style.stroke = col;
  requestAnimationFrame(() => $("arc").style.strokeDashoffset = 327 - 327 * a.sc / 100);

  clearInterval(timer);
  let n = 0; const step = Math.max(1, Math.ceil(a.sc / 30));
  timer = setInterval(() => { n = Math.min(a.sc, n + step); $("sc").textContent = n; if (n >= a.sc) clearInterval(timer); }, 25);

  $("rs").innerHTML = a.rs.map((r, i) =>
    `<li class="${r.sev}" style="animation-delay:${i * 70}ms"><span>${r.text ? esc(r.text[L]) : t.r[r.k]}${r.x ? ` <b dir="ltr">${r.x}</b>` : ""}</span></li>`).join("");
  const fmtAge = d => L === "ar"
    ? (d < 60 ? d + " يوم" : d < 730 ? Math.round(d / 30) + " شهر" : (d / 365).toFixed(1) + " سنة")
    : (d < 60 ? d + " days" : d < 730 ? Math.round(d / 30) + " months" : (d / 365).toFixed(1) + " years");
  $("det").innerHTML = Object.keys(t.f).filter(k => a.d[k] !== undefined).map(k =>
    `<div><span>${t.f[k]}</span><code>${String(k === "age" ? fmtAge(a.d[k]) : k === "ml" ? a.d[k] + "%" : k === "dns" ? (a.d[k] ? t.dnsY : t.dnsN) : a.d[k]).replace(/</g, "&lt;")}</code></div>`).join("");
}

async function enrich(a, raw, deep = false) {
  if (!API) return a;
  try {
    const r = await fetch(API + "/api/analyze", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: raw, deep })
    });
    if (!r.ok) return a;
    const d = await r.json();
    const mapped = (d.reasons || []).map(x => ({ k: "srv", key: x.k, sev: x.sev, text: { ar: x.ar, en: x.en } }));
    if (d.page && d.page.fetched === false) {
      mapped.push({ k: "srv", key: "page", sev: "g", text: {
        ar: "تعذر جلب الصفحة للفحص العميق (" + d.page.error + ").", en: "Could not fetch the page for the deep scan (" + d.page.error + ")." } });
    }
    const first = x => x.key === "known" || x.key === "rep";
    if (d.rules_included) {
      // the server already ran the rules, the database, the AI model and the domain checks
      a.sc = d.risk_score;
      a.rs = mapped;
    } else {
      if (mapped.some(x => x.sev !== "g")) a.rs = a.rs.filter(x => x.k !== "clean");
      a.rs = [...mapped.filter(first), ...a.rs, ...mapped.filter(x => !first(x))];
      if (d.known) a.sc = 100;
      else {
        a.sc = Math.min(100, a.sc + (d.ml_points || 0) + (d.flag_points || 0));
        if (d.reports > 0) a.sc = Math.max(a.sc, 55);
      }
    }
    if (d.domain && typeof d.domain.age_days === "number") a.d.age = d.domain.age_days;
    if (d.ml && d.ml.available) a.d.ml = Math.round(d.ml.probability * 100);
    if (d.domain && d.domain.dns) a.d.dns = d.domain.dns.resolves;
  } catch (e) { /* الخادم غير متاح: نكمل بالتحليل المحلي */ }
  return a;
}

async function run() {
  const raw = $("url").value.trim();
  const a = analyze(raw);
  if (!a) { alert(T[L].empty + "\n\n«" + raw.slice(0, 80) + "» (" + raw.length + ")"); return; }
  await enrich(a, raw, !!($("deep") && $("deep").checked));
  last = a; render(a);
  $("res").scrollIntoView({ behavior: "smooth", block: "nearest" });
}

$("go").onclick = run;
$("url").addEventListener("keydown", e => { if (e.key === "Enter") run(); });
$("lang").onclick = () => setLang(L === "ar" ? "en" : "ar");

$("rb").onclick = async () => {
  const l = $("rl").value.trim();
  if (!l) { $("rl").focus(); return; }
  const msg = $("rok");
  msg.classList.remove("hidden");
  try {
    if (!API) throw new Error("no api");
    const r = await fetch(API + "/api/report", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ url: l, type: $("rt").value, notes: $("rn").value })
    });
    if (!r.ok) throw new Error("bad");
    msg.textContent = T[L].rok;
    msg.style.color = "var(--ok)";
    $("rl").value = ""; $("rn").value = "";
  } catch (e) {
    msg.textContent = T[L].rerr;
    msg.style.color = "var(--bad)";
  }
};


// ===== فحص تسريب الحسابات =====
const esc = x => String(x).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

async function sha1Hex(str) {
  const buf = await crypto.subtle.digest("SHA-1", new TextEncoder().encode(str));
  return [...new Uint8Array(buf)].map(b => b.toString(16).padStart(2, "0")).join("").toUpperCase();
}

$("pwGo").onclick = async () => {
  const t = T[L], out = $("pwRes"), p = $("pw").value;
  if (!p) { out.textContent = t.pwEmpty; out.className = "res2 mid"; return; }
  out.textContent = t.checking; out.className = "res2";
  try {
    const h = await sha1Hex(p), pre = h.slice(0, 5), suf = h.slice(5);
    const r = await fetch("https://api.pwnedpasswords.com/range/" + pre);
    if (!r.ok) throw new Error("bad");
    const row = (await r.text()).split("\n").map(l => l.trim().split(":")).find(a => a[0] === suf);
    const n = row ? parseInt(row[1], 10) : 0;
    if (n > 0) { out.textContent = t.pwFound.replace("{n}", n.toLocaleString("en")); out.className = "res2 bad"; }
    else { out.textContent = t.pwSafe; out.className = "res2 safe"; }
  } catch (e) { out.textContent = t.pwErr; out.className = "res2 mid"; }
  $("pw").value = "";
};

$("emGo").onclick = async () => {
  const t = T[L], out = $("emRes"), e = $("em").value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e)) { out.textContent = t.emBad; out.className = "res2 mid"; return; }
  if (!API) { out.textContent = t.emNoApi; out.className = "res2 mid"; return; }
  out.textContent = t.checking; out.className = "res2";
  try {
    const r = await fetch(API + "/api/email-check", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ email: e })
    });
    if (r.status === 429) { out.textContent = t.emLimit; out.className = "res2 mid"; return; }
    if (!r.ok) throw new Error("bad");
    const d = await r.json();
    if (d.found) {
      out.innerHTML = `<b>${t.emFound.replace("{n}", d.count)}</b><div class="chips">${d.breaches.map(b => `<span>${esc(b)}</span>`).join("")}</div><div>${t.emAdvice}</div>`;
      out.className = "res2 bad";
    } else { out.textContent = t.emSafe; out.className = "res2 safe"; }
  } catch (err) { out.textContent = t.emErr; out.className = "res2 mid"; }
};

// ===== فحص الرسالة: الواجهة =====
$("msgGo").onclick = async () => {
  const t = T[L], out = $("msgRes"), text = $("msgIn").value.trim();
  if (!text) { out.innerHTML = `<p class="mut">${t.msgEmpty}</p>`; return; }
  out.innerHTML = `<p class="mut">${t.checking}</p>`;
  const m = scanMessage(text);
  const items = (await Promise.all(m.links.slice(0, 5).map(async l => {
    const a = analyze(l);
    if (!a) return null;
    await enrich(a, l);
    return { l, a };
  }))).filter(Boolean);
  const maxLink = items.reduce((x, i) => Math.max(x, i.a.sc), 0);
  const total = Math.min(100, m.score + maxLink);
  const lvl = total >= 50 ? "bad" : total >= 20 ? "mid" : "safe";
  const sevOf = c => CATS[c.k].sev;
  let html = `<div class="verdict ${lvl}">${t[lvl]} · ${total}/100</div><div class="mut">${lvl === "bad" ? t.vb : lvl === "mid" ? t.vm : t.vs}</div>`;
  if (m.cats.length) {
    html += `<h3>${t.msgFlags}</h3><ul class="rs">` + m.cats.map(c =>
      `<li class="${sevOf(c)}"><span>${t.cat[c.k]}<b>${m.cats.length ? c.words.map(esc).join("، ") : ""}</b></span></li>`).join("") + `</ul>`;
  }
  html += `<h3>${t.msgLinks}</h3>`;
  if (items.length) {
    html += `<ul class="rs">` + items.map(({ l, a }) => {
      const why = a.rs.filter(r => !["https", "clean"].includes(r.k)).slice(0, 2).map(r => (r.text ? esc(r.text[L]) : t.r[r.k]) + (r.x ? " " + esc(r.x) : "")).join(" ");
      return `<li class="${a.sc >= 50 ? "h" : a.sc >= 20 ? "m" : "g"}"><span dir="ltr">${esc(l.length > 60 ? l.slice(0, 57) + "..." : l)}</span><span class="pts">${a.sc}/100</span><span class="mut" style="flex-basis:100%">${why}</span></li>`;
    }).join("") + `</ul>`;
  } else html += `<p class="mut">${t.msgNoLink}</p>`;
  if (!m.cats.length && !items.length) html += `<p class="mut">${t.msgNone}</p>`;
  out.innerHTML = html;
};

// ===== اختبار التوعية =====
const QUIZ = [
  { t: "https://www.facebook.com/login", ph: false,
    ar: "الدومين facebook.com هو الموقع الرسمي، وصفحة الدخول هنا طبيعية.", en: "facebook.com is the official domain, and a login page is normal there." },
  { t: "http://facebook-login-verify.xyz/secure", ph: true,
    ar: "الدومين ليس facebook.com. هو اسم مقلَّد بامتداد xyz الشائع في الاحتيال وبدون تشفير.", en: "The domain is not facebook.com. It is an imitation name with the scam-prone xyz extension and no encryption." },
  { t: "https://paypa1.com/signin", ph: true,
    ar: "الرقم 1 مكان الحرف l: paypa1 بدل paypal. تمويه بصري شائع.", en: "The digit 1 replaces the letter l: paypa1 instead of paypal. A common visual trick." },
  { t: "مبروك! فزت بجائزة 5000 دينار من ليبيانا. أرسل رمز التحقق الذي وصلك لتستلمها: bit.ly/x7Kq2", ph: true,
    ar: "جائزة لم تشارك فيها، وطلب رمز التحقق، ورابط مختصر يخفي الوجهة. الشركات الحقيقية لا تطلب رمز التحقق أبداً.", en: "A prize you never entered, a request for your verification code and a short link hiding the destination. Real companies never ask for your code." },
  { t: "https://accounts.google.com/signin", ph: false,
    ar: "accounts.google.com دومين فرعي رسمي. الجزء المهم هو ما قبل الامتداد مباشرة: google.com.", en: "accounts.google.com is an official subdomain. What matters is the part right before the extension: google.com." },
  { t: "https://www.instagrarm.com/accounts/login", ph: true,
    ar: "instagrarm بدل instagram: حرف r زائد. خطأ إملائي مقصود لتضليلك.", en: "instagrarm instead of instagram: an extra r. A deliberate typo to fool you." },
  { t: "تنبيه من المصرف: تم إيقاف حسابك. حدّث بياناتك خلال 24 ساعة: http://bank-update.top", ph: true,
    ar: "استعجال وتهديد بإيقاف الحساب، ورابط بامتداد top. المصرف الحقيقي لا يطلب تحديث البيانات برابط في رسالة.", en: "Urgency and a threat to suspend the account, with a top link. A real bank never asks you to update data through a link in a message." },
  { t: "https://login.microsoftonline.com", ph: false,
    ar: "يبدو غريباً لكنه دومين Microsoft الرسمي لتسجيل الدخول. الغرابة وحدها ليست دليلاً.", en: "It looks odd but it is Microsoft's official sign-in domain. Looking odd alone is not proof." },
  { t: "https://facebook.com.security-check.net/login", ph: true,
    ar: "الدومين الحقيقي هو security-check.net (آخر جزء قبل الامتداد). كلمة facebook.com مجرد اسم فرعي لتضليلك.", en: "The real domain is security-check.net (the last part before the extension). facebook.com is only a subdomain to mislead you." },
  { t: "https://ar.wikipedia.org/wiki/تصيد_احتيالي", ph: false,
    ar: "ويكيبيديا دومين رسمي، ووجود مسار عربي لا يدل على خطر.", en: "Wikipedia is an official domain, and an Arabic path is no sign of danger." }
];
let qi = 0, qScore = 0, qDone = false, qPicked = null;

function renderQuiz() {
  const box = $("quizBox");
  if (!box) return;
  const t = T[L];
  if (qi >= QUIZ.length) {
    box.innerHTML = `<div class="verdict ${qScore >= 8 ? "safe" : qScore >= 5 ? "mid" : "bad"}">${t.qDone} ${qScore}/${QUIZ.length}</div><button class="btn" id="qAgain">${t.qAgain}</button>`;
    $("qAgain").onclick = () => { qi = 0; qScore = 0; qPicked = null; renderQuiz(); };
    return;
  }
  const q = QUIZ[qi];
  let html = `<div class="mut">${t.qQ} ${qi + 1}/${QUIZ.length}</div><div class="qitem" dir="auto">${esc(q.t)}</div>`;
  if (qPicked === null) {
    html += `<div class="qbtns"><button class="btn" id="qSafe">${t.qSafe}</button><button class="btn" id="qScam">${t.qScam}</button></div><p class="mut small">${t.qFake}</p>`;
  } else {
    const ok = (qPicked === q.ph);
    html += `<div class="qfb ${ok ? "safe" : "bad"}"><b>${ok ? t.qOk : t.qNo}</b><div>${esc(q[L])}</div></div><div class="qbtns"><button class="btn" id="qNext">${t.qNext}</button></div>`;
  }
  box.innerHTML = html;
  if (qPicked === null) {
    const pick = v => { qPicked = v; if (v === q.ph) qScore++; renderQuiz(); };
    $("qSafe").onclick = () => pick(false);
    $("qScam").onclick = () => pick(true);
  } else {
    $("qNext").onclick = () => { qi++; qPicked = null; renderQuiz(); };
  }
}

const io = new IntersectionObserver(es => es.forEach(e => { if (e.isIntersecting) e.target.classList.add("in"); }), { threshold: .15 });
document.querySelectorAll(".reveal").forEach(el => io.observe(el));

setLang("ar");
renderQuiz();
