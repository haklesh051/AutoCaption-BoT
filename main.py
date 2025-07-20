import pyrogram, os, asyncio
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, MessageNotModified

# ENV variables
try:
    api_id = int(os.environ.get("app_id", ""))
except Exception as e:
    print(f"⚠️ Api ID Invalid: {e}")

try:
    api_hash = os.environ.get("api_hash", "")
except Exception as e:
    print(f"⚠️ API Hash Invalid: {e}")

try:
    bot_token = os.environ.get("bot_token", "")
except Exception as e:
    print(f"⚠️ Bot Token Invalid: {e}")

try:
    custom_caption = os.environ.get("custom_caption", "`{file_name}`")
except Exception as e:
    print(f"⚠️ Custom Caption Invalid: {e}")

# Pyrogram Bot
AutoCaptionBot = pyrogram.Client(
    "AutoCaptionBot",
    api_id=app_id,
    api_hash=api_hash,
    bot_token=bot_token
)

# Start message
start_message = """
<b>👋 Hello {}</b>
<b>I am an AutoCaption bot</b>
<b>Just add me to your channel and I will auto caption your media files</b>
<b>@Mo_Tech_YT</b>
"""

# About message
about_message = """
<b>• Name : [AutoCaption V1](t.me/{username})</b>
<b>• Developer : <a href="https://github.com/PR0FESS0R-99">Muhammed</a></b>
<b>• Language : Python3</b>
<b>• Library : Pyrogram v{version}</b>
<b>• Updates : <a href="https://t.me/Mo_Tech_YT">Click Here</a></b>
<b>• Source Code : <a href="https://github.com/PR0FESS0R-99/AutoCaption-Bot">Click Here</a></b>
"""

# /start command
@AutoCaptionBot.on_message(pyrogram.filters.private & pyrogram.filters.command(["start"]))
def start_command(bot, update):
    update.reply(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# "start" button callback
@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("start"))
def strat_callback(bot, update):
    update.message.edit(
        start_message.format(update.from_user.mention),
        reply_markup=start_buttons(bot),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# "about" button callback
@AutoCaptionBot.on_callback_query(pyrogram.filters.regex("about"))
def about_callback(bot, update):
    bot_user = bot.get_me()
    update.message.edit(
        about_message.format(version=pyrogram.__version__, username=bot_user.username),
        reply_markup=about_buttons(),
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=True
    )

# Main caption editor
@AutoCaptionBot.on_message(pyrogram.filters.channel)
def edit_caption(bot, update: Message):
    if os.environ.get("custom_caption"):
        motech, mote = get_file_details(update)
        try:
            try:
                update.edit(custom_caption.format(file_name=motech.file_name, mote=mote))
            except FloodWait as e:
                asyncio.sleep(e.value)
                update.edit(custom_caption.format(file_name=motech.file_name, mote=mote))
        except MessageNotModified:
            pass

# File extractor
def get_file_details(update: Message):
    if update.media:
        for message_type in (
            "photo", "animation", "audio", "document",
            "video", "video_note", "voice", "sticker"
        ):
            obj = getattr(update, message_type)
            if obj:
                return obj, obj.file_id
    return None, None

# Start Buttons
def start_buttons(bot):
    bot_user = bot.get_me()
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📢 Updates", url="https://t.me/Mo_Tech_YT"),
        InlineKeyboardButton("ℹ️ About", callback_data="about")
    ], [
        InlineKeyboardButton("➕ Add To Your Channel", url=f"http://t.me/{bot_user.username}?startchannel=true")
    ]])

# About Buttons
def about_buttons():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("🏠 Back To Home", callback_data="start")
    ]])

print("✅ Telegram AutoCaption V1 Bot Started!")
print("👨‍💻 Bot Created By https://github.com/PR0FESS0R-99")

AutoCaptionBot.run()
