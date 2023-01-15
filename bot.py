from pyrogram import Client, filters 
from pyrogram.enums.messages_filter import MessagesFilter
from dotenv import load_dotenv
import time
import os

if os.getenv('DEBUG'):
    load_dotenv()

api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')
bot_token = os.getenv('BOT_TOKEN')
session_str = os.getenv('SESSION_STR')

app = Client('bot', api_id, api_hash, session_string=session_str)
print('Bot started')

@app.on_message(filters.channel)
async def main(_, message):

    chat_id = message.chat.id
    res = await message.reply('Processing')

    total_messages = await app.search_messages_count(chat_id)
    total_videos = await app.search_messages_count(chat_id, filter=MessagesFilter.VIDEO)
    total_documents = await app.search_messages_count(chat_id, filter=MessagesFilter.DOCUMENT)
    total_media = total_videos + total_documents

    res = await res.edit_text(
        f'Total messages - {total_messages}\n'
        f'Total videos - {total_videos}\n'
        f'Total documents - {total_messages}\n'
        f'Total media - {total_messages}'
    )

    file_ids = []

    fetched = 0

    duplicate = 0

    try:

        async for msg in app.search_messages(message.chat.id):

            if msg.document:
                media = msg.document

            elif msg.video:
                media = msg.video

            else:
                media = None

            if media:

                file_id = media.file_unique_id

                if file_id not in file_ids:

                    file_ids.append(file_id)

                else:

                    await msg.delete()
                    
                    duplicate += 1

            fetched += 1

            # if fetched % 20 == 0:

                # await res.edit_text(
                #     f'{res.text}\n'
                #     f'Messages fetched - {fetched}\n'
                #     f'Duplicate found - {duplicate}'
                # )

            print(fetched, duplicate, total_messages)

            time.sleep(0.2)

    except Exception as e:

        print('Waiting time', e.value if e.value else 10, 'secs. Required due to flood wait')

        if e.value:

            time.sleep(e.value)

        else:

            time.sleep(10)


app.run()


