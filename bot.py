import asyncio

from aiogram import Bot, Dispatcher, Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup

from storage import create_db, add_task, get_task, done_task, delete_task, delete_all_done_task
from keyboards import main_keyboard, tasks_keyboard

router = Router()
token = "8673567036:AAEIcGYpHmUD-H8ZdJbx2ZvyPJmgyUSHFuk"


class TodoStates(StatesGroup):
    task_add_state = State()

@router.message(Command("start"))
async def start_cmd(message: Message, state: FSMContext):
    await message.answer("Бот для списка дел V 1.0. Добро пожаловать!", reply_markup=main_keyboard())

@router.message(Command("add"))
@router.message(F.text.in_({"➕ Добавить"}))
async def add_cmd(message: Message, state: FSMContext):
    await message.answer("Напиши текст задачи!")
    await state.set_state(TodoStates.task_add_state)

@router.message(TodoStates.task_add_state)
async def adding_new_task(message: Message, state: FSMContext):
    text = message.text
    user_id = message.from_user.id
    await add_task(user_id, text)
    await message.answer("Задача успешно добавлена!")
    await state.clear()

@router.message(Command("list"))
@router.message(F.text.in_({"📝 Мои задачи"}))
async def list_cmd(message: Message, state: FSMContext):
    result = ""
    rows = await get_task(message.from_user.id)
    for done_row in rows:
        icon = "✅" if done_row[2] == 1 else "❌"
        result += str(done_row[0]) + ". " + done_row[1] + " " + icon + "\n"
    await message.answer(result, reply_markup=tasks_keyboard(rows))

@router.callback_query(F.data.startswith("done_"))
async def task_done_callback(callback: CallbackQuery):
    task_id = int(callback.data.split("_")[1])
    await done_task(callback.from_user.id, task_id)
    await callback.message.answer("Задача №" + str(task_id) + " успешно выполнена!")

@router.message(Command("done"))
async def done_cmd(message: Message, state: FSMContext):
    try:
        task_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("Пожалуйста, укажите корректный номер задачи: /done 1")
        return
    check = await done_task(message.from_user.id, task_id)
    if check == 0:
        await message.answer("Задачи под данным номером не существует!")
    else:
        await message.answer("Задача №" + str(task_id) + " успешно выполнена!")

@router.message(Command("delete"))
@router.message(F.text.in_({"Удалить одну задачу"}))
async def delete_cmd(message: Message, state: FSMContext):
    try:
        task_id = int(message.text.split()[1])
    except (IndexError, ValueError):
        await message.answer("Пожалуйста, укажите корректный номер задачи: /delete 1")
        return
    check = await delete_task(message.from_user.id, task_id)
    if check == 0:
        await message.answer("Задачи под данным номером не существует!")
    else:
        await message.answer("Задача №" + str(task_id) + " успешно удалена!")

@router.message(Command("deldone"))
@router.message(F.text.in_({"🗑 Удалить выполненные"}))
async def deldone_cmd(message: Message, state: FSMContext):
    await delete_all_done_task(message.from_user.id)
    await message.answer("Все завершённые задачи успешно удалены!")


async def main():
    bot = Bot(token=token)
    dp = Dispatcher()
    dp.include_router(router)
    await create_db()
    await dp.start_polling(bot)

asyncio.run(main())