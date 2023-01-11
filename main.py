import pyrogram
from pyrogram import Client
from pyrogram import filters
import bypasser
import os
from bypasser import ddllist
import requests
import threading
from config import API_HASH, API_ID, BOT_TOKEN, AUTH

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# loop thread
def loopthread(message):
  urls = []
  for ele in message.text.split():
    if "http://" in ele or "https://" in ele:
      urls.append(ele)
  if len(urls) == 0:
    return

  if bypasser.ispresent(ddllist, urls[0]):
    msg = app.send_message(message.chat.id,
                           "⚡ <b>Generating..</b>",
                           reply_to_message_id=message.id)
  else:
    if urls[0] in "https://olamovies" or urls[0] in "https://psa.pm/":
      msg = app.send_message(message.chat.id,
                             "🔎 <b>This might take some time..</b>",
                             reply_to_message_id=message.id)
    else:
      msg = app.send_message(message.chat.id,
                             "😍 <b>Bypassing..</b>",
                             reply_to_message_id=message.id)

  link = ""
  for ele in urls:
    if bypasser.ispresent(ddllist, ele):
      try:
        temp = ddl.direct_link_generator(ele)
      except Exception as e:
        temp = "**Error**: " + str(e)
    else:
      try:
        temp = bypasser.shortners(ele)
      except Exception as e:
        temp = "**Error**: " + str(e)
    print("bypassed:", temp)
    link = link + temp + "\n\n"

  try:
    app.edit_message_text(message.chat.id,
                          msg.id,
                          f'__{link}__',
                          disable_web_page_preview=True)
  except:
    app.edit_message_text(message.chat.id, msg.id, "__Failed to Bypass__")


# start command
@app.on_message(filters.chat(AUTH) & filters.command(["start"]))
def send_start(client: pyrogram.client.Client,
               message: pyrogram.types.messages_and_media.message.Message):
  app.send_message(
    message.chat.id,
    f"__👋 **Hi {message.from_user.mention}, I am Link bypasser bot, just send me any Shortner links and i will give You results.**",
    reply_to_message_id=message.id)
                
# links
@app.on_message(filters.chat(AUTH) & filters.text)
def receive(client: pyrogram.client.Client,
            message: pyrogram.types.messages_and_media.message.Message):
  bypass = threading.Thread(target=lambda: loopthread(message), daemon=True)
  bypass.start()


# doc thread
def docthread(message):
  if message.document.file_name.endswith("dlc"):
    msg = app.send_message(message.chat.id,
                           "😍 <b>Bypassing..</b>",
                           reply_to_message_id=message.id)
    print("sent DLC file")
    sess = requests.session()
    file = app.download_media(message)
    dlccont = open(file, "r").read()
    link = bypasser.getlinks(dlccont, sess)
    app.edit_message_text(message.chat.id, msg.id, f'__{link}__')
    os.remove(file)


# doc
@app.on_message(filters.document)
def docfile(client: pyrogram.client.Client,
            message: pyrogram.types.messages_and_media.message.Message):
  bypass = threading.Thread(target=lambda: docthread(message), daemon=True)
  bypass.start()


#Bot Started
print("👍😍😍 Bot Started")
print("Now I Also Become a Piro Hecker 😎")
app.run()
