import os
from fastapi import FastAPI, Request, Header, HTTPException
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.models import (
    TextSendMessage,
    ImageSendMessage,
    FlexSendMessage,
    TextMessage
)
from linebot.models import QuickReply, QuickReplyButton, MessageAction

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
app.mount("/static", StaticFiles(directory="static"), name="static")

line_bot_api = LineBotApi(ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

# =====================
# BASE URL (Render)
# =====================
def BASE_URL():
    return "https://ulandresortline.onrender.com"

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

        # =====================
        # POSTBACK (Rich Menu / Card Button)
        # =====================
        if event.type == "postback":
            handle_postback(event)

        # =====================
        # TEXT MESSAGE (พิมพ์เอง)
        # =====================
        elif event.type == "message" and isinstance(event.message, TextMessage):
            handle_text(event)

    return {"ok": True}

# =====================
# POSTBACK HANDLER
# =====================
def handle_postback(event):
    action = event.postback.data

    if action == "coffee":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text="☕ ULand Coffee\nพร้อมเสิร์ฟความอร่อยทุกวัน 💛\nเปิดให้บริการเวลา 07.00 - 17.00 น.\nโทร 📞 094-7802363"
                ),
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/menu.JPG",
                    preview_image_url=f"{BASE_URL()}/static/images/menu.JPG",
                ),
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/special1.png",
                    preview_image_url=f"{BASE_URL()}/static/images/special1.png",
                ),
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/special2.png",
                    preview_image_url=f"{BASE_URL()}/static/images/special2.png",
                ),
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/special.JPG",
                    preview_image_url=f"{BASE_URL()}/static/images/special.JPG",
                ),
            ]
        )

    elif action in ["room_price", "rooms"]:
        send_room_card(event)

    elif action == "location":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="📍 แผนที่ Uland Resort\nhttps://maps.app.goo.gl/UQ4tG2kCCdW2E9em8"
            )
        )

    # elif action == "contact":
    #     profile = line_bot_api.get_profile(event.source.user_id)
    #     nickname = profile.display_name

    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(
    #            f"คุณ {nickname} ต้องการสอบถามเรื่องอะไรดีคะ 😊\n"
    #             "สามารถพิมพ์ 👉🏻หมายเลข👈🏻 เรื่องที่ต้องการสอบถามได้เลยค่ะ\n\n"
    #             "1. ประเภทและราคาห้องพัก\n"
    #             "2. รูปภาพรีสอร์ทและห้องพัก\n"
    #             "3. แผนที่รีสอร์ท\n"
    #             "4. รหัส Wi-Fi\n"
    #             "5. เมนูร้าน ULand Coffee"
    #         )
    #     )

    # ===== ROOM DETAIL =====
    #สุขใจ 550
    elif action == "room_detail_sj":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=(
                        "💖💖 ห้องพักโซนสุขใจ 550 บาท/คืน 💖💖\n"
                        "สิ่งอำนวยความสะดวกภายในห้องพัก\n"
                        "- ผ้าม่านโปร่งแสง\n"
                        "- เครื่องทำน้ำอุ่น\n"
                        "- ผ้าเช็ดตัว\n"
                        "- แอร์\n"
                        "- โต๊ะทำงาน\n"
                        "- ตู้เย็น\n"
                        "- ตู้เสื้อผ้า\n"
                        "- บริการลานจอดรถ\n"
                        "\n"
                        "สิ่งอำนวยความสะดวกภายในรีสอร์ท\n"
                        "- ร้านอาหาร\n"
                        "- ร้านคาเฟ่\n"
                        "- ร้านซักอบรีด\n"
                        "- ร้านยา\n"
                    )
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/SJ_1.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/SJ_1.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/SJ_2.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/SJ_2.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/SJ_3.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/SJ_3.jpg",
                ),
            ]
        )
    
    #เติทสุข 590
    elif action == "room_detail_ts":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=(
                        "💖💖 ห้องพักโซนเติมสุข 590 บาท/คืน 💖💖\n"
                        "สิ่งอำนวยความสะดวกภายในห้องพัก\n"
                        "- ผ้าม่านโปร่งแสง\n"
                        "- เครื่องทำน้ำอุ่น\n"
                        "- ผ้าเช็ดตัว\n"
                        "- แอร์\n"
                        "- โต๊ะทำงาน\n"
                        "- ตู้เย็น\n"
                        "- ตู้เสื้อผ้า\n"
                        "- ที่จอดรถหน้าบ้าน\n"
                        "\n"
                        "สิ่งอำนวยความสะดวกภายในรีสอร์ท\n"
                        "- ร้านอาหาร\n"
                        "- ร้านคาเฟ่\n"
                        "- ร้านซักอบรีด\n"
                        "- ร้านยา\n"
                    )
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/TS_1.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/TS_1.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/TS_2.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/TS_2.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/TS_3.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/TS_3.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/TS_4.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/TS_4.jpg",
                ),
            ]
        )
        user_id = event.source.user_id

        line_bot_api.push_message(
            user_id,
            ImageSendMessage(
                original_content_url=f"{BASE_URL()}/static/images/TS_5.jpg",
                preview_image_url=f"{BASE_URL()}/static/images/TS_5.jpg",
            )
        )
    #ก่อสุข 690
    elif action == "room_detail_ks":
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text=(
                        "💖💖 ห้องพักโซนก่อสุข 690 บาท/คืน 💖💖\n"
                        "สิ่งอำนวยความสะดวกภายในห้องพัก\n"
                        "- ระเบียงหลังบ้าน\n"
                        "- ผ้าม่านโปร่งแสง\n"
                        "- เครื่องทำน้ำอุ่น\n"
                        "- ผ้าเช็ดตัว\n"
                        "- แอร์\n"
                        "- โต๊ะทำงาน\n"
                        "- ตู้เย็น\n"
                        "- ตู้เสื้อผ้า\n"
                        "- ที่จอดรถหน้าบ้าน\n"
                        "\n"
                        "สิ่งอำนวยความสะดวกภายในรีสอร์ท\n"
                        "- ร้านอาหาร\n"
                        "- ร้านคาเฟ่\n"
                        "- ร้านซักอบรีด\n"
                        "- ร้านยา\n"
                    )
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/KS_1.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/KS_1.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/KS_2.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/KS_2.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/KS_3.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/KS_3.jpg",
                ),
                ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/KS_4.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/KS_4.jpg",
                ),
            ]
        )
        user_id = event.source.user_id

        line_bot_api.push_message(
            user_id,
            ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/KS_5.jpg",
                        preview_image_url=f"{BASE_URL()}/static/images/KS_5.jpg",
            ),
        )


    # elif action == "room_detail":
    #     line_bot_api.reply_message(
    #         event.reply_token,
    #         TextSendMessage(
    #             text="🛎 ห้องพักมี แอร์ / น้ำอุ่น / Wi-Fi / ทีวี / ตู้เย็น"
    #         )
    #     )

    elif action == "book_room":
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="กรุุณารอสักครู่ระบบกำลังติดต่อแอดมิน"
            )
        )

# =====================
# TEXT HANDLER (พิมพ์เลข)
# =====================
def handle_text(event):
    text = event.message.text.strip().lower()

    # 1 = ห้องพัก
    if text in ["1", "1.", "ราคา", "ประเภทและราคาห้องพัก"]:
        send_room_card(event)

    # 2 = รูปที่พัก
    elif text in ["2", "2.", "รูปภาพที่พัก"]:
        line_bot_api.reply_message(
            event.reply_token,
            [
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/V1.jpg",
                    preview_image_url=f"{BASE_URL()}/static/images/V1.jpg",
                ),
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/V2.jpg",
                    preview_image_url=f"{BASE_URL()}/static/images/V2.jpg",
                ),
                ImageSendMessage(
                    original_content_url=f"{BASE_URL()}/static/images/V3.jpg",
                    preview_image_url=f"{BASE_URL()}/static/images/V3.jpg",
                ),
            ]
        )

    # 3 = แผนที่
    elif text in ["3", "3.", "แผนที่รีสอร์ท"]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="📍ยูแลนด์รีสอร์ท ULand Resort \n https://maps.app.goo.gl/UQ4tG2kCCdW2E9em8"
            )
        )

    # 4 = wifi
    elif text in ["4", "4.", "wifi", "รหัส wifi"]:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                text="Wi-Fi: U Land Resort\nPassword: 92330000"
            )
        )

    # 5 = coffee
    elif text in ["5", "5.", "coffee", "uland coffee"]:
        line_bot_api.reply_message(
            event.reply_token,
            [
                TextSendMessage(
                    text="☕ ULand Coffee\nพร้อมเสิร์ฟความอร่อยทุกวัน 💛\nเปิดให้บริการเวลา 07.00 - 17.00 น.\nโทร 📞 094-7802363"
                    ),
                    ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/menu.JPG",
                        preview_image_url=f"{BASE_URL()}/static/images/menu.JPG",
                    ),
                    ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/special1.png",
                        preview_image_url=f"{BASE_URL()}/static/images/special1.png",
                    ),
                    ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/special2.png",
                        preview_image_url=f"{BASE_URL()}/static/images/special2.png",
                    ),
            ]
        )
        user_id = event.source.user_id

        line_bot_api.push_message(
            user_id,
            ImageSendMessage(
                        original_content_url=f"{BASE_URL()}/static/images/special.JPG",
                        preview_image_url=f"{BASE_URL()}/static/images/special.JPG",
            ),
        )
    #ติดต่อสอบถาม
    elif text in ["contact", "ติดต่อสอบถาม", "contact/faq"]:
        profile = line_bot_api.get_profile(event.source.user_id)
        nickname = profile.display_name

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(
                f"คุณ {nickname} ต้องการสอบถามเรื่องอะไรดีคะ สามารถพิมพ์หมายเลขหรือกดที่เมนูด้านล่างได้เลยค่ะ 😊\n"
                "1. ประเภทและราคาห้องพัก\n"
                "2. รูปภาพรีสอร์ทและห้องพัก\n"
                "3. แผนที่รีสอร์ท\n"
                "4. รหัส Wi-Fi\n"
                "5. เมนูร้าน ULand Coffee"
            ),
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(
                        action=MessageAction(label="💰 ประเภทและราคาห้องพัก", text="1")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="🖼 รูปภาพที่พัก", text="2")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="📍 แผนที่รีสอร์ท", text="3")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="📶 รหัส Wi-Fi", text="4")
                    ),
                    QuickReplyButton(
                        action=MessageAction(label="☕ ULand Coffee", text="5")
                    ),
                ]
            )
        )
        user_id = event.source.user_id

        line_bot_api.push_message(
            user_id,
            TextSendMessage(
                "หากต้องการติดต่อสอบถามเรื่องอื่นๆ สามารถทิ้งข้อความไว้ได้เลยค่ะแอดมินจะติดต่อกลับโดยเร็วที่สุด\n\nติดต่อด่วน โทร 062-8899824 , 065-7546414 , (หลัง 22.00 น. 094-7802363)"
            ),
        )
        return

# =====================
# ROOM CARD
# =====================
def send_room_card(event):
    line_bot_api.reply_message(
        event.reply_token,
        FlexSendMessage(
            alt_text="ประเภทและราคาห้องพัก",
            contents=hotel_cards()
        )
    )

def hotel_cards():
    return {
        "type": "carousel",
        "contents": [
            room_card(
                title='ห้องพักโซน "สุขใจ"',
                price="550 บาท / คืน",
                image_url=f"{BASE_URL()}/static/images/SJ_2.jpg",
                detail_data="room_detail_sj",
                book_data="book_room"
            ),
            room_card(
                title='ห้องพักโซน "เติมสุข"',
                price="590 บาท / คืน",
                image_url=f"{BASE_URL()}/static/images/TS_3.jpg",
                detail_data="room_detail_ts",
                book_data="book_room"
            ),
            room_card(
                title='ห้องพักโซน "ก่อสุข"',
                price="690 บาท / คืน",
                image_url=f"{BASE_URL()}/static/images/KS_4.jpg",
                detail_data="room_detail_ks",
                book_data="book_room"
            )
        ]
    }


def room_card(title, price, image_url, detail_data, book_data):
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
                {"type": "text", "text": title, "weight": "bold", "size": "lg"},
                {"type": "text", "text": price, "color": "#666666"}
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
                        "data": detail_data
                    }
                },
                {
                    "type": "button",
                    "style": "primary",
                    "action": {
                        "type": "postback",
                        "label": "จองห้องพัก",
                        "data": book_data
                    }
                }
            ]
        }
    }
