from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

def main_keyboard():
   return ReplyKeyboardMarkup(
        keyboard =[
            [KeyboardButton(text="📝 Мои задачи"), KeyboardButton(text="➕ Добавить"), KeyboardButton(text="✅ Завершить задачу")],
            [KeyboardButton(text="🗑 Удалить выполненные"), KeyboardButton(text="Удалить одну задачу")],
            [KeyboardButton(text="О боте")]
        ],
        resize_keyboard=True
   )
def tasks_keyboard(rows):
    buttons = []
    for row in rows:
        icon = "✅" if row[2] == 1 else "❌"
        button = InlineKeyboardButton(
            text=icon + " " + row[1],
            callback_data="done_" + str(row[0])
        )
        buttons.append([button])
    return InlineKeyboardMarkup(inline_keyboard=buttons)
