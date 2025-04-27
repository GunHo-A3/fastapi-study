from sqlmodel import SQLModel, create_engine, Session

sqlite_file_name = "relational.db"
engine = create_engine(f'sqlite:///{sqlite_file_name}', echo=False)

def get_session():
    with Session(engine) as session:
        yield session

def create_db():
    SQLModel.metadata.create_all(engine)