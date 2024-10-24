from app.database.models import async_session
from app.database.models import User, Category, Items, Korzina
from sqlalchemy import select, delete
from sqlalchemy import BigInteger

async def add_us(id_tg_u:BigInteger, name_u:str, famil_u:str,age_u:int,nimber_u:str):
    async with async_session.begin() as session:
        use=User(tg_id=id_tg_u, name=name_u,famil=famil_u,age=age_u,nimber=nimber_u)
        session.add(use)
    await session.commit()

async def add_korzina( id_items_k:int, tg_id_k:BigInteger, name_k=str,description_k=str, price_k=int):
    async with async_session.begin() as session:
        v_korziny=Korzina(id_items=id_items_k, tg_id=tg_id_k, name=name_k,description=description_k, price=price_k)
        session.add(v_korziny)
    await session.commit()

async def del_korzina(id:int):
    async with async_session.begin() as session:
        del_kor=delete(Korzina).where(Korzina.id==id)
        await session.execute(del_kor)
    await session.commit()

async def get_korzina(tg_id):
    async with async_session() as session:
        return await session.scalars(select(Korzina).where(Korzina.tg_id==tg_id))

async def get_cat():
    async with async_session() as session:
        return await session.scalars(select(Category))

async def get_items(category_id):
    async with async_session() as session:
        return await session.scalars(select(Items).where(Items.category==category_id))

async def get_opis(item_id):
    async with async_session() as session:
        return await session.scalar(select(Items).where(Items.id==item_id))

async def get_kor(id):
    async with async_session() as session:
        return await session.scalar(select(Korzina).where(Korzina.id==id))


async def get_us(tg_id):
    async with async_session() as session:
        return await session.scalar(select(User).where(User.tg_id==tg_id))
