from sqlalchemy import create_engine,text

db_url="mysql+pymysql://root:2741@localhost:3307"

db_name="capstone_school_db"

engine=create_engine(db_url)

def create_db():
    with engine.connect() as conn:
        conn.execute(text(f'CREATE DATABASE IF NOT EXISTS {db_name}'))
        print(f"Database Created Successfully {db_name}")

# create_db()