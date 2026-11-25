const DEFAULT_API = "http://127.0.0.1:5000";
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const WORD = { dangerous: ["خطير", "bad"], suspicious: ["مشبوه", "mid"], safe: ["يبدو آمناً", "safe"] };

async function apiBase() {
  const o = await chrome.storage.local.get("api");
  return (o.api || DEFAULT_API).replace(/\/$/, "");
}

async function run() {
  $("api").value = await apiBase();
  $("api").onchange = () => chrome.storage.local.set({ api: $("api").value.trim() });
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  const url = (tab && tab.url) || "";
  $("url").textContent = url;
  if (!/^https?:/i.test(url)) { $("res").textContent = "هذه الصفحة لا يمكن فحصها."; return; }
  $("res").textContent = "جارٍ الفحص...";
  try {
    const r = await fetch((await apiBase()) + "/api/analyze", {
      method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ url, source: "extension" })
    });
    if (!r.ok) throw new Error(r.status);
    const d = await r.json();
    const [word, cls] = WORD[d.verdict] || WORD.safe;
    const why = (d.reasons || []).filter(x => !["https", "clean"].includes(x.k)).slice(0, 4);
    $("res").innerHTML = `<div class="v ${cls}">${word} (${d.risk_score}/100)</div>` +
      (why.length ? "<ul>" + why.map(x => `<li class="${x.sev}">${esc(x.ar)}</li>`).join("") + "</ul>" : '<p class="mut">لا علامات خطر واضحة.</p>') +
      '<p class="mut">نتيجة تقديرية وليست ضماناً. إذا شككت فلا تدخل أي بيانات.</p>';
  } catch (e) {
    $("res").textContent = "تعذر الاتصال بالخادم. شغّله أولاً (python app.py).";
  }
}
run();
