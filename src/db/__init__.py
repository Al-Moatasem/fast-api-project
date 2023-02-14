from src.api.users.orm import User
from src.db.pg_connect import Base, engine

Base.metadata.create_all(bind=engine)
