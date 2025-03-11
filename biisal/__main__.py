import os
import sys
import glob
import asyncio
import logging
import importlib
from pathlib import Path
from pyrogram import idle
from aiohttp import web
from biisal.bot import StreamBot
from biisal.vars import Var
from biisal.server import web_server
from biisal.utils.keepalive import ping_server
from biisal.bot.clients import initialize_clients

LOGO = """
 ____ ___ ___ ____    _    _     
| __ )_ _|_ _/ ___|  / \  | |    
|  _ \| | | |\___ \ / _ \ | |    
| |_) | | | | ___) / ___ \| |___ 
|____/___|___|____/_/   \_\_____|"""

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("aiohttp").setLevel(logging.ERROR)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("aiohttp.web").setLevel(logging.ERROR)

ppath = "biisal/bot/plugins/*.py"
files = glob.glob(ppath)
StreamBot.start()
loop = asyncio.get_event_loop()

async def start_services():
    print('\n')
    print('------------------- Initializing Telegram Bot -------------------')
    bot_info = await StreamBot.get_me()
    StreamBot.username = bot_info.username
    print("------------------------------ DONE ------------------------------")
    print()
    print("---------------------- Initializing Clients ----------------------")
    await initialize_clients()
    print("------------------------------ DONE ------------------------------")
    print('\n')
    print('--------------------------- Importing ---------------------------')
    for name in files:
        with open(name) as a:
            patt = Path(a.name)
            plugin_name = patt.stem.replace(".py", "")
            plugins_dir = Path(f"biisal/bot/plugins/{plugin_name}.py")
            import_path = ".plugins.{}".format(plugin_name)
            spec = importlib.util.spec_from_file_location(import_path, plugins_dir)
            load = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(load)
            sys.modules["biisal.bot.plugins." + plugin_name] = load
            print("Imported => " + plugin_name)
    if Var.ON_HEROKU:
        print("------------------ Starting Keep Alive Service ------------------")
        print()
        asyncio.create_task(ping_server())
    print('-------------------- Initializing Web Server -------------------------')
    app = web.AppRunner(await web_server())
    await app.setup()
    bind_address = "0.0.0.0" if Var.ON_HEROKU else Var.BIND_ADRESS
    await web.TCPSite(app, bind_address, Var.PORT).start()
    print('----------------------------- DONE ---------------------------------------------------------------------')
    print('\n')
    print('---------------------------------------------------------------------------------------------------------')
    print('---------------------------------------------------------------------------------------------------------')
    print(' follow me for more such exciting bots! https://github.com/biisal')
    print('---------------------------------------------------------------------------------------------------------')
    print('\n')
    print('----------------------- Service Started -----------------------------------------------------------------')
    print('                        bot =>> {}'.format((await StreamBot.get_me()).first_name))
    print('                        server ip =>> {}:{}'.format(bind_address, Var.PORT))
    print('                        Owner =>> {}'.format((Var.OWNER_USERNAME)))
    if Var.ON_HEROKU:
        print('                        app running on =>> {}'.format(Var.FQDN))
    print('---------------------------------------------------------------------------------------------------------')
    print(LOGO)
    try:
        await StreamBot.send_message(chat_id=Var.OWNER_ID[0], text='<b>ᴊᴀɪ sʜʀᴇᴇ ᴋʀɪsʜɴᴀ 😎\nʙᴏᴛ ʀᴇsᴛᴀʀᴛᴇᴅ !!</b>')
    except Exception as e:
        print(f'Got this error while sending restart msg to owner: {e}')
    await idle()

async def stop_services():
    await StreamBot.stop()
    print("Bot Stopped!")

if __name__ == '__main__':
    try:
        loop.run_until_complete(start_services())
    except KeyboardInterrupt:
        loop.run_until_complete(stop_services())
        logging.info('----------------------- Service Stopped -----------------------')


##### बदलाव
- *वेब सर्वर*: web_server से प्राप्त app को सही ढंग से शुरू किया। यह मानता है कि biisal/server.py में एक मान्य web.Application रिटर्न हो रहा है। अगर ऐसा नहीं है, तो हमें server.py भी देखना होगा।
- *शटडाउन हैंडलिंग*: stop_services जोड़ा ताकि बॉट सही ढंग से बंद हो।

---

#### 3. biisal/vars.py की जाँच
- सुनिश्चित करें कि Var.URL सही ढंग से सेट है। उदाहरण:
  python
  URL = "http://yourdomain.com/"  # या "http://45.67.89.100:8081/"
  
- अगर .env में सेट है, तो:
  
  URL=http://yourdomain.com/
  

---

#### 4. biisal/server.py (अनुमानित फिक्स)
चूंकि आपके पास web_server से संबंधित त्रुटि है, यहाँ एक बेसिक server.py का उदाहरण है जो काम करेगा। अगर आपके पास पहले से अलग कोड है, तो उसे शेयर करें।

python
from aiohttp import web

async def handle_root(request):
    return web.Response(text="Welcome to StreamBot Server!")

async def handle_watch(request):
    return web.Response(text="Streaming endpoint not implemented yet.")

async def handle_download(request):
    return web.Response(text="Download endpoint not implemented yet.")

async def web_server():
    app = web.Application()
    app.router.add_get('/', handle_root)
    app.router.add_get('/watch/{id}/{name}', handle_watch)
    app.router.add_get('/{id}/{name}', handle_download)
    return app
