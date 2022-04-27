from typing import NamedTuple

from sqlalchemy import select

from db import Category, async_session


class CategoryScheme(NamedTuple):
    code: int
    name: str
    aliases: list[str]


class Categories:
    async def get_categories(self) -> list[CategoryScheme]:
        categories = []
        async with async_session() as session:
            stmt = select(Category)
            db_categories: list[Category] = (
                (await session.execute(stmt)).scalars().all()
            )
        for category in db_categories:
            categories.append(
                CategoryScheme(
                    code=category.id,
                    name=category.name,
                    aliases=category.aliases.split(", ")
                )
            )
        return categories

    async def get_by_name(self, name: str) -> tuple[int, str]:
        categories = await self.get_categories()
        for category in categories:
            if name.lower() in category.aliases:
                return category.code, category.name
        else:
            category = await self.get_by_name("other")
            return category.code, category.name
