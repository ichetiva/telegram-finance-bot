from aiogram import Bot, Dispatcher, types, executor

from credentials import BOT_TOKEN
from repositories import ExpenseRepo
from use_cases.categories import Categories

bot = Bot(BOT_TOKEN)
# if need then set storage
dp = Dispatcher(bot)


@dp.message_handler(commands=["help", "start"])
async def welcome_handler(message: types.Message):
    await message.answer("Welcome!")


@dp.message_handler()
async def expense_handler(message: types.Message):
    amount = message.text.split()[0]
    if not amount.isdigit():
        return
    amount = int(amount)
    category = " ".join(word for word in message.text.split()[1:])
    category_id, category_name = await Categories().get_by_name(category.lower())
    await ExpenseRepo.create(amount, category_id)
    await message.answer("Добавлены траты {} руб. на {}".format(
        amount, category_name
    ))


executor.start_polling(dp)
