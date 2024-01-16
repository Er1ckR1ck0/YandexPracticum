from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, URLInputFile
from main import bot
from templates import *
import json
router = Router()

@router.message(Command(commands=['start']))
async def start(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text = 'Начать тестирование', callback_data = 'questionnaire_start'))
    keyboard.add(types.InlineKeyboardButton(text = 'Погоди, а что это за бот?', callback_data = 'questionnaire_help'))
    keyboard.adjust(1) # количество кнопок в строке
    try:
        with open('./info/info.json', 'r') as file:
            data = json.load(file)
    except:
        data = {}
    if str(message.from_user.id) not in data:
        data[str(message.from_user.id)] =  {
                        "states": 0,
                        "correct_answer": 0,
                        "wront_answer": 0
            }
    with open('./info/info.json', 'w') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    await bot.send_video(chat_id = message.from_user.id, video = FSInputFile('./content/Start 1.mp4'), caption = start_text.format(name = message.from_user.first_name), reply_markup = keyboard.as_markup())

@router.message(Command(commands=['help']))
async def start(message: Message):
    keyboard = InlineKeyboardBuilder()
    keyboard.add(types.InlineKeyboardButton(text = 'Начать тестирование', callback_data = 'questionnaire_start'))
    keyboard.adjust(1)
    await bot.send_video(chat_id = message.from_user.id, video = FSInputFile('./content/help.mp4'), caption = help_text, reply_markup=keyboard.as_markup())
    

@router.message(F.text)
async def message(message: Message):
    await message.answer(text = "Хэй! Полегче, я не смогу ответить тебе на текстовые запросы, но в дальнейшем буду принимать любые ответы, просто нужно дальше меня дописывать)")

@router.message(F.sticker)
async def message(message: Message):
    await message.answer(text = "Стикеры люблю, но прислать что-то не смогу")

@router.message(F.photo)
async def message(message: Message):
    await message.answer(text = "Я не понимаю, что на фото. Надеюсь, всё отлично, хотя (опять-же) я ничего не смогу увидеть")   

@router.message(F.document)
async def message(message: Message):
    await message.answer(text = "Ну... отправить файл кому-то не смогу, но использовать меня как хранилище тоже можешь.")    

# @router.message(Command(commands=['music']))
# async def start(message: Message):
#     random_music = URLInputFile(music[randint(0, len(music) - 1)])
#     await message.answer_audio(random_music)