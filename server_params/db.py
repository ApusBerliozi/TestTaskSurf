from sqlalchemy import create_engine

from app.models import Base
from config.config_reader import config

db_engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}/{config.db_name}")
Base.metadata.create_all(db_engine)
