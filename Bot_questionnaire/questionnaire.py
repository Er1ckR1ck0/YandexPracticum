from aiogram import Router, F, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, FSInputFile, URLInputFile
from templates import *
import json
import asyncio

router = Router()

def create_answer_keyboards(user_id):
    with open('./info/states.json', 'r', encoding='utf-8') as file:
        data_states = json.load(file)
    with open('./info/info.json', 'r', encoding='utf-8') as file:
        data_info = json.load(file)
    user_state = data_info[str(user_id)]['states']
    print(user_state)
    keyboard = InlineKeyboardBuilder()
    for i in data_states['states'][0]['variables'][str(user_state)]:
        if i == data_states['states'][0]['correct_answers'][str(user_state)]:
            keyboard.add(types.InlineKeyboardButton(text = i, callback_data = 'questionnaire_correct'))
        else:
            keyboard.add(types.InlineKeyboardButton(text = i, callback_data = 'questionnaire_uncorrect'))
    keyboard.adjust(1)
    return keyboard

@router.callback_query(F.data.startswith("questionnaire"))
async def questionnaire(callback: CallbackQuery):
    action = callback.data.split('_')[1]
    print(action)
    if action == "correct":
        await callback.message.delete()
        with open('./info/states.json', 'r', encoding='utf-8') as file:
            data_states = json.load(file)
        with open('./info/info.json', 'r', encoding='utf-8') as file:
            data_info = json.load(file)
        user_state = data_info[str(callback.from_user.id)]['states'] 
        text = data_states['states'][0]['answers'][str(user_state)]
        await callback.message.answer_video(video = FSInputFile(f'./content/answer{user_state}.mp4'), caption = text)
        data_info[str(callback.from_user.id)]['states'] += 1
        data_info[str(callback.from_user.id)]['correct_answer'] += 1
        with open('./info/info.json', 'w', encoding='utf-8') as file:
            json.dump(data_info, file, ensure_ascii=False, indent=4)
        asyncio.sleep(15)
        if data_info[str(callback.from_user.id)]['states'] == 5:
            data_info[str(callback.from_user.id)]['states'] = 0
            if data_info[str(callback.from_user.id)]['correct_answer'] == 4:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Покоритель Волны»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 3:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Дающий искру»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 2:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Jumior+»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 1:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Junior»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 0:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Начинающий»"
            data_info[str(callback.from_user.id)]['correct_answer'] = 0
            data_info[str(callback.from_user.id)]['wront_answer'] = 0
            keyboard = InlineKeyboardBuilder()
            keyboard.add(types.InlineKeyboardButton(text = 'Начать снова', callback_data = 'questionnaire_start'))
            keyboard.adjust(1)
            await callback.message.answer(text = text, reply_markup = keyboard.as_markup())
        else:
            text = data_states['states'][0]['questions'][str(data_info[str(callback.from_user.id)]['states'])]
            keyboard = create_answer_keyboards(callback.from_user.id)
            await callback.message.answer_video(video = FSInputFile(f'./content/quest{data_info[str(callback.from_user.id)]["states"]}.mp4'), caption = text, reply_markup = keyboard.as_markup())

    elif action == "uncorrect":
        await callback.message.delete()
        with open('./info/info.json', 'r', encoding='utf-8') as file:
            data_info = json.load(file)
        with open('./info/states.json', 'r', encoding='utf-8') as file:
            data_states = json.load(file)
        with open('./info/info.json', 'r', encoding='utf-8') as file:
            data_info = json.load(file)
        user_state = data_info[str(callback.from_user.id)]['states'] 
        text = data_states['states'][0]['wrong_answers'][str(user_state)]
        await callback.message.answer_video(video = FSInputFile(f'./content/answer{user_state}.mp4'), caption = text)
        data_info[str(callback.from_user.id)]['states'] += 1
        data_info[str(callback.from_user.id)]['wront_answer'] += 1
        with open('./info/info.json', 'w', encoding='utf-8') as file:
            json.dump(data_info, file, ensure_ascii=False, indent=4)
        asyncio.sleep(15)
        if data_info[str(callback.from_user.id)]['states'] == 5:
            data_info[str(callback.from_user.id)]['states'] = 0
            if data_info[str(callback.from_user.id)]['correct_answer'] == 4:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Покоритель Волны»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 3:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Дающий искру»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 2:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Jumior+»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 1:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Junior»"
            elif data_info[str(callback.from_user.id)]['correct_answer'] == 0:
                text = f"Поздравляем! Вы набрали {data_info[str(callback.from_user.id)]['correct_answer']}/4 правильных ответов.\n\nНаша оценка вам: «Начинающий»"
            data_info[str(callback.from_user.id)]['correct_answer'] = 0
            data_info[str(callback.from_user.id)]['wront_answer'] = 0
            keyboard = InlineKeyboardBuilder()
            keyboard.add(types.InlineKeyboardButton(text = 'Начать снова', callback_data = 'questionnaire_start'))
            keyboard.adjust(1)
            await callback.message.answer(text = text, reply_markup = keyboard.as_markup())
        else:
            text = data_states['states'][0]['questions'][str(data_info[str(callback.from_user.id)]["states"])]
            keyboard = create_answer_keyboards(callback.from_user.id)
            await callback.message.answer_video(video = FSInputFile(f'./content/quest{data_info[str(callback.from_user.id)]["states"]}.mp4'), caption = text, reply_markup = keyboard.as_markup())

    elif action == "help":
        keyboard = InlineKeyboardBuilder()
        keyboard.add(types.InlineKeyboardButton(text = 'Начать тестирование', callback_data = 'questionnaire_start'))
        keyboard.adjust(1)
        print(callback.from_user.id)
        await callback.message.answer_video(video = FSInputFile('./content/help.mp4'), caption = help_text, reply_markup=keyboard.as_markup())

    elif action == "start":
        with open('./info/info.json', 'r', encoding='utf-8') as file:
            data_info = json.load(file)
        data_info[str(callback.from_user.id)]['states'] = 1
        data_info[str(callback.from_user.id)]['correct_answer'] = 0
        data_info[str(callback.from_user.id)]['wront_answer'] = 0
        with open('./info/info.json', 'w', encoding='utf-8') as file:
            json.dump(data_info, file, ensure_ascii=False, indent=4)
        with open('./info/states.json', 'r', encoding='utf-8') as file:
            data_states = json.load(file)
        keyboard = create_answer_keyboards(callback.from_user.id)
        text = data_states['states'][0]['questions'][str(data_info[str(callback.from_user.id)]['states'])]
        await callback.message.answer_video(video = FSInputFile(f'./content/quest1.mp4'), caption = text, reply_markup=keyboard.as_markup())