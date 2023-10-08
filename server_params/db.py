from sqlalchemy import create_engine

db_engine = create_engine(f"postgresql://{config.db_username}:{config.db_password}@{config.db_host}/{config.db_name}")
