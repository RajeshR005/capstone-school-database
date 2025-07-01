from app.db.base_class import Base,engine
from app.models import *

Base.metadata.create_all(engine)