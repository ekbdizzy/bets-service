import contextlib
from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from settings import settings


Base = declarative_base()


engine = create_async_engine(
    settings.get_postgres_uri(),
    future=True,
    echo=False,
)
Session = async_sessionmaker(
    bind=engine,
    autocommit=False,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@contextlib.asynccontextmanager
async def db_session() -> AsyncSession:
    async with Session() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e
        finally:
            await session.close()
