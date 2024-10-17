from app.database.models import async_session
from app.database.models import User, Category, Items
from sqlalchemy import select
from sqlalchemy import BigInteger

async def add_us( id_tg_u:BigInteger, name_u:str, famil_u:str,age_u:int,nimber_u:str):
    async with async_session.begin() as session:
        use=User(tg_id=id_tg_u, name=name_u,famil=famil_u,age=age_u,nimber=nimber_u)
        session.add(use)
    await session.commit()

async def get_cat():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_items(category_id):
    async with async_session() as session:
        return await session.scalars(select(Items).where(Items.category==category_id))

async def get_opis(item_id):
    async with async_session() as session:
        return await session.scalar(select(Items).where(Items.id==item_id))

