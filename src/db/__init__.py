from src.api.images.orm import UploadedImage
from src.api.users.orm import User
from src.db.pg_connect import Base, engine

# As we are going to use Alembic in the migration process,
#   we will let it create the tables, and any other changes
# Base.metadata.create_all(bind=engine)
