import os
import json
import requests
from datetime import datetime, timedelta

# Telegram
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Load data
with open("dams.json", "r", encoding="utf-8") as f:
    dams = json.load(f)

def risk_score(fill, rain, faults):
    score = 0

    if fill >= 95:
        score += 45
    elif fill >= 85:
        score += 30
    elif fill >= 75:
        score += 15

    if rain >= 50:
        score += 30
    elif rain >= 20:
        score += 15

    if faults:
        score += 25

    return min(score, 100)

def level(score):
    if score >= 80:
        return "🔴 حرج"
    elif score >= 60:
        return "🟠 مرتفع"
    elif score >= 30:
        return "🟡 متابعة"
    else:
        return "🟢 طبيعي"

now = datetime.utcnow() + timedelta(hours=3)

report = f"""📄 تقرير رصد السدود
🕒 {now.strftime('%Y-%m-%d %H:%M')} بتوقيت السعودية
════════════════════

"""

for d in dams:
    score = risk_score(d["fill"], d["rain"], d["fault"])
    state = level(score)

    report += f"""🏞️ {d["name"]}
• الامتلاء: {d["fill"]}%
• أمطار الحوض: {d["rain"]} ملم
• أعطال: {"نعم" if d["fault"] else "لا"}
• الحالة: {state}
• المؤشر: {score}/100

"""

def send(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": msg
    })

send(report)
print(report)
