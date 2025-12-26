import os
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    FlexSendMessage
)

# =====================
# LOAD ENV
# =====================
load_dotenv()

CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")

if not CHANNEL_SECRET or not ACCESS_TOKEN:
    raise RuntimeError("Missing LINE env vars")

# =====================
# APP INIT
# =====================
app = FastAPI()

# 👇 สำคัญมาก: mount static
app.mount("/static", StaticFiles(directory="static"), name="static")

line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

# =====================
# HEALTH CHECK
# =====================
@app.get("/")
def root():
    return {"status": "ok"}

# =====================
# WEBHOOK
# =====================
@app.post("/webhook")
async def webhook(request: Request, x_line_signature: str = Header(None)):
    body = (await request.body()).decode("utf-8")

    try:
        events = parser.parse(body, x_line_signature)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid signature")

    for event in events:
        if event.type == "postback":
            action = event.postback.data

            # -----------------
            # Uland Coffee (รูป + ข้อความ)
            # -----------------
            if action == "coffee":
                line_bot_api.reply_message(
                    event.reply_token,
                    [
                         TextSendMessage(
                            text="☕ ULand Coffee \nพร้อมเสิร์ฟความอร่อยทุกวัน 💛 \nเปิดให้บริการเวลา 07.00 - 17.00 น. \n\nสั่ง กาแฟ น้ำ ขนม ได้ที่นี่เลยค่ะหรือโทร 📞 094-7802363"
                        ),
                        ImageSendMessage(
                            original_content_url=f"{BASE_URL()}/static/images/coffee.jpg",
                            preview_image_url=f"{BASE_URL()}/static/images/coffee.jpg"
                        )
                    ]
                )

            # -----------------
            # Location
            # -----------------
            elif action == "location":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="📍 แผนที่ Uland Resort\nhttps://maps.google.com/?q=YOUR_LOCATION"
                    )
                )

            # -----------------
            # Contact / FAQ
            # -----------------
            elif action == "contact":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text=(
                            "📞 ติดต่อสอบถาม\n"
                            "โทร: 08x-xxx-xxxx\n\n"
                            "⏰ เช็กอิน: 14:00\n"
                            "⏰ เช็กเอาต์: 12:00\n\n"
                            "พิมพ์คำถามได้เลยครับ 😊"
                        )
                    )
                )

            # -----------------
            # ประเภทห้องพัก (Card โรงแรม)
            # -----------------
            elif action in ["room_price", "rooms"]:
                line_bot_api.reply_message(
                    event.reply_token,
                    FlexSendMessage(
                        alt_text="ประเภทห้องพัก",
                        contents=hotel_cards()
                    )
                )

            # -----------------
            # ปุ่มจาก Card
            # -----------------
            elif action == "room_detail":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text=(
                            "🛎 รายละเอียดห้องพักโซน \"เติมสุข\"\n"
                            "• แอร์\n• เครื่องทำน้ำอุ่น\n• Wi-Fi\n"
                            "• ทีวี\n• ตู้เย็น\n• ที่จอดรถ"
                        )
                    )
                )

            elif action == "book_room":
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(
                        text="📅 ต้องการจองห้องพัก\nพิมพ์:\nจอง + วันที่เข้าพัก + จำนวนคืน"
                    )
                )

            # -----------------
            # DEFAULT
            # -----------------
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text=f"ไม่รู้จักเมนู: {action}")
                )

    return {"ok": True}

# =====================
# BASE URL (Render)
# =====================
def BASE_URL():
    # 👉 ใส่โดเมน Render ของคุณตรงนี้
    return "https://uland-linebot.onrender.com"

# =====================
# FLEX CARD HOTEL
# =====================
def hotel_cards():
    return {
        "type": "carousel",
        "contents": [
            room_card(
                title='ห้องพักโซน "เติมสุข"',
                price="590 บาท / คืน",
                image_url=f"{BASE_URL()}/static/images/room1.jpg"
            ),
            room_card(
                title="ห้อง Deluxe",
                price="890 บาท / คืน",
                image_url=f"{BASE_URL()}/static/images/room2.jpg"
            )
        ]
    }

def room_card(title, price, image_url):
    return {
        "type": "bubble",
        "hero": {
            "type": "image",
            "url": image_url,
            "size": "full",
            "aspectRatio": "20:13",
            "aspectMode": "cover"
        },
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title,
                    "weight": "bold",
                    "size": "lg"
                },
                {
                    "type": "text",
                    "text": price,
                    "color": "#666666"
                }
            ]
        },
        "footer": {
            "type": "box",
            "layout": "horizontal",
            "contents": [
                {
                    "type": "button",
                    "action": {
                        "type": "postback",
                        "label": "ข้อมูลเพิ่มเติม",
                        "data": "room_detail"
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "จองห้องพัก",
                        "data": "book_room"
                    }
                }
            ]
        }
    }
