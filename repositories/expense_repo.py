from datetime import date
from typing import Union, List

from sqlalchemy import select, delete
from sqlalchemy.sql import text

from db import Category, Expense, async_session


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

    @classmethod
    async def today(
        cls
    ) -> List[Expense]:
        """Get today expenses from database"""

        async with async_session() as session:
            stmt = select(Expense, Category.name).filter(
                Expense.created_at == date.today()
            ).join(Category, Category.id == Expense.category)
            db_expenses: List[Expense] = (
                await session.execute(stmt)
            ).scalars().all()
        return db_expenses

    @classmethod
    async def month(
        cls
    ) -> int:
        """Get sum expenses for current month from database"""

        async with async_session() as session:
            stmt = text(
                """
                SELECT sum(e.amount)
                FROM expenses e
                WHERE
                    extract(month FROM e.created_at::date) = extract(month FROM current_date::date) 
                    AND extract(year FROM e.created_at::date) = extract(year FROM current_date::date)
                """
            )
            sum_month_expenses = (
                await session.execute(stmt)
            ).scalars().first()
            return sum_month_expenses

    @classmethod
    async def last_10_expenses(cls) -> List[Expense]:
        """Get last ten expenses from database"""

        async with async_session() as session:
            stmt = select(Expense).group_by(Expense.id).limit(10)
            last_expenses = (
                await session.execute(stmt)
            ).scalars().all()
            return last_expenses
    
    @classmethod
    async def delete(cls, code: int) -> None:
        """Delete some exepense by code from database"""

        async with async_session() as session:
            stmt = delete(Expense).where(Expense.id == code)
            await session.execute(stmt)
            await session.commit()
