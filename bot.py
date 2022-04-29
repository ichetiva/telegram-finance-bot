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


@dp.message_handler(commands=["categories"])
async def categories_handler(message: types.Message):
    categories = await Categories().get_categories()
    categories_message = ""
    for category in categories:
        categories_message += "* {} ({})\n".format(
            category.name,
            ", ".join(alias for alias in category.aliases)
        )
    await message.answer(
        f"Доступные категории трат:\n\n{categories_message}"
    )


@dp.message_handler(commands=["today"])
async def today_statistics(message: types.Message):
    today_expenses = await ExpenseRepo.today()
    if len(today_expenses) == 0:
        return await message.answer(
            "Не удалось найти траты за сегодня."
        )
    statistics_message = ""
    for expense in today_expenses:
        category_name = await Categories().get_by_code(expense.category)
        statistics_message += "* {} руб. на {}\n".format(
            expense.amount, category_name
        )
    await message.answer(
        f"Траты за сегодня:\n\n{statistics_message}"
    )


@dp.message_handler(commands=["month"])
async def month_statistics(message: types.Message):
    sum_month_expenses = await ExpenseRepo.month()
    await message.answer(
        "Всего потрачено за месяц: {} руб.".format(sum_month_expenses)
    )


@dp.message_handler(commands=["expenses"])
async def last_expenses(message: types.Message):
    last_10_expenses = await ExpenseRepo.last_10_expenses()
    expenses_message = ""
    for expense in last_10_expenses:
        category_name = await Categories().get_by_code(expense.id)
        expenses_message += "* {} руб. на {} (удалить /delete_{})\n".format(
            expense.amount, category_name, expense.id
        )
    await message.answer(f"Последние траты:\n\n{expenses_message}")


@dp.message_handler(
    lambda message: message.text.lower().split("_")[0] == "/delete"
)
async def delete_expense(message: types.Message):
    await ExpenseRepo.delete(int(message.text.split("_")[1]))
    await message.answer("Удалено")


@dp.message_handler()
async def add_expense_handler(message: types.Message):
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
