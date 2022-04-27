from typing import Union

from db import Expense, async_session


class ExpenseRepo:
    @classmethod
    async def create(
        cls, amount: int, category: str
    ) -> Union[Expense, None]:
        """Add expense to database"""

        async with async_session() as session:
            async with session.begin():
                db_expense = Expense(amount=amount, category=category)
                session.add(db_expense)
            db_expense = await session.refresh(db_expense)
            await session.commit()
        return db_expense
