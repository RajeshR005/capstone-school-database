from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker,declarative_base

from app.core.config import settings



engine = create_engine(
                    settings.DATA_BASE,
                    connect_args={
                        "encoding": "UTF-8",
                        "nencoding": "UTF-8",}
                    )


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

