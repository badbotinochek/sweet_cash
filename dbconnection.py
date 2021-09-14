from sqlalchemy import create_engine
from config import DATABASE_URI
from api.models.users import Base


engine = create_engine(DATABASE_URI)
Base.metadata.create_all(engine)