import logging
from aiogram import Bot, Dispatcher, types, executor
import yt_dlp
import os
import time
from requests import get
from dotenv import load_dotenv, find_dotenv

#Токен боту
load_dotenv(find_dotenv())
bot=Bot(os.getenv('token'))
dp=Dispatcher(bot)

#Бот дізнається інформацію о користувачи
class FilenameCollectorPP(yt_dlp.postprocessor.common.PostProcessor):
    def __init__(self):
        super(FilenameCollectorPP, self).__init__(None)
        self.filenames=[]

    def run(self, information):
        self.filenames.append(information["filepath"])
        return [], information

help(FilenameCollectorPP)

#Команда 'start' використовує їй відому інформацію і вітається з користувачем
@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    user_id=message.from_user.id
    user_name=message.from_user.first_name
    user_full_name=message.from_user.full_name
    logging.info(f'{user_id} {user_full_name} {time.asctime()}')
    await message.reply(f"Hello! {user_name}")

#За допомогою цього декоратору команда 'sea' може завантажити музику з ютуб, вказавши назву та виконавця
@dp.message_handler(commands=['sea'])
async def search_cmd(message: types.Message):
    #Ця функція відповідає - у якому форматі буде завантажуватись музика
    arg=message.get_args()
    YDL_OPTIONS={'format': 'bestaudio/best',
                 'noplaylist': 'True',
                 'postprocessors': [{
                     'key': 'FFmpegExtractAudio' ,
                     'preferredcodec': 'mp3',
                     'preferredquality': '192'
                     }]
    }
    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            get(arg)
        except:
            filename_collector=FilenameCollectorPP()
            ydl.add_post_processor(filename_collector)
            video=ydl.extract_info(f"ytsearch:{arg}", download=True)['entries'][0]
            await message.reply_document(open(filename_collector.filenames[0], 'rb'))
            time.sleep(5)
            os.remove(filename_collector.filenames[0])
        else:
            video=ydl.extract_info(arg, download=True)
        return filename_collector.filenames[0]
help(search_cmd)

#Цей умовний оператор перевіряє, чи файл виконується бузпосередньо як головний скрипт
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

#Аби бот працював увесь час
bot.polling(none_stop=True, interval=0)
