import asyncio

from db import async_session, Category


async def add_categories():
    products = Category(
        name="продукты", aliases="еда, products, продукты"
    )
    coffee = Category(
        name="кофе", aliases="coffee, кофе"
    )
    dinner = Category(
        name="обед", aliases="dinner, обед, ресторан, столовая, кафе"
    )
    fast_food = Category(
        name="фастфуд", aliases="fast food, мак, бк, бургер"
    )
    public_transport = Category(
        name="общ.транспорт", aliases="маршрутка, автобус, метро"
    )
    taxi = Category(
        name="такси", aliases="taxi, такси"
    )
    phone = Category(
        name="телефон", aliases="мтс, связь, телефон, phone"
    )
    internet = Category(
        name="инет", aliases="интернет, инет, internet"
    )
    subscriptions = Category(
        name="подписка", aliases="подписки, subscriptions, подписка"
    )
    other = Category(
        name="другое", aliases="other, другое"
    )

    async with async_session() as session:
        async with session.begin():
            session.add_all(
                [
                    products,
                    coffee,
                    other,
                    subscriptions,
                    dinner,
                    phone,
                    taxi,
                    public_transport,
                    fast_food,
                    internet
                ]
            )
        await session.commit()


if __name__ == "__main__":
    asyncio.run(add_categories())
