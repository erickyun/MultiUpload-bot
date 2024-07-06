import json
from pyrogram import Client, filters
from pyrogram.types import Message
from modules.gdrive import gdriveDownload
from modules.tg import tgDownload
from modules.ddl import ddlDownload, URLRx
from modules.cache import CacheSize, clearCache
import os
from dotenv import load_dotenv
import re
load_dotenv()

service_id_rx = re.compile("#(\d{1,2})")
authorized_list = json.loads(os.getenv('authorized_list'))

app = Client("my_account", api_id=os.getenv('api_id'),
             api_hash=os.getenv('api_hash'), bot_token=os.getenv('bot_token'))

help_message = """**Supported upload hosts:**`
+----+-------------+--------+
| #  |     Host    |  Limit |
+====+=============+========+
| 1  | anonfiles   | 20 GB  |
+----+-------------+--------+
| 2  | Catbox      | 200 MB |
+----+-------------+--------+
| 3  | file.io     | 2 GB   |
+----+-------------+--------+
| 4  | Filemail    | 5 GB   |
+----+-------------+--------+
| 5  | Gofile      | unlim  |
+----+-------------+--------+
| 6  | KrakenFiles | 1 GB   |
+----+-------------+--------+
| 7  | LetsUpload  | 10 GB  |
+----+-------------+--------+
| 8  | MegaUp      | 5 GB   |
+----+-------------+--------+
| 9  | MixDrop     | unlim  |
+----+-------------+--------+
| 10 | pixeldrain  | 10 GB  |
+----+-------------+--------+
| 11 | Racaty      | 10 GB  |
+----+-------------+--------+
| 12 | transfer.sh | unlim  |
+----+-------------+--------+
| 13 | Uguu        | 128 MB |
+----+-------------+--------+
| 14 | WeTransfer  | 2 GB   |
+----+-------------+--------+
| 15 | workupload  | 2 GB   |
+----+-------------+--------+
| 16 | zippyshare  | 500 MB |
+----+-------------+--------+`

**Supported links: G-Drive url, TG file, DDL**

ex: Gdrive to anonfiles:
`/up gdrive-url #1`

ex: TG file to WeTransfer:
reply to a file with `/up #14`

**Made by [bunny](https://t.me/pseudoboi) 🧪**
"""
if not os.path.exists('Downloads'):
    os.makedirs('Downloads')

print("Bot started", flush=True)
@app.on_message(filters.text & ~filters.channel)
def echo(client, message: Message):
    if not message.chat.id in authorized_list:
        message.reply_text('**Unauthorized!**')
        return

    if '/help' in message.text:
        message.reply(help_message, disable_web_page_preview=True, quote=True)
        return
    try:
        if '/up' in message.text:
            serviceID = service_id_rx.search(message.text)
            if serviceID:
                serviceID = int(serviceID.group(1))-1
                if serviceID > 15:
                    message.reply_text("Invalid Host ID")
                    return
            else:
                serviceID = int(os.getenv('default_host_id')) - 1
            if 'drive.google' in message.text:
                progressMessage =  message.reply("Please wait while I download your G-Drive file...")
                gdriveDownload(message, serviceID, progressMessage)
            elif message.reply_to_message or 't.me' in message.text:
                print("Telegram...")
                progressMessage =  message.reply("Please wait while I download your Telegram file...")
                tgDownload(app, message, serviceID, progressMessage)
            elif URLRx.search(message.text):
                print("URl....")
                progressMessage =  message.reply("Please wait while I download your link...")
                ddlDownload(message, serviceID, progressMessage)
        elif '/stats' in message.text:
            CacheSize(message)
        elif '/clear' in message.text:
            clearCache(message)
    except Exception as e:
        print(e, flush=True)
        message.reply(e)
        return
app.run()


