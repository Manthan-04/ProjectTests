from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from typing import Annotated, Literal
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = 'sqlite:///./chatbot.db'
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
base = declarative_base()

class DBTransaction:
    def __init__(self):
        pass

    async def __build_cnx(self):
        db = sessionLocal()
        try:
            yield db
        finally:
            db.close()

    async def __build_ret_cnx(self):
        db = sessionLocal()
        try:
            return db
        finally:
            return None

    def get_cnx(self, returnCnx=False):
        if not returnCnx:
            return Annotated[Session, Depends(self.__build_cnx)]
        else:
            return Annotated[Session, Depends(self.__build_ret_cnx)]
        
    async def view(self, cnx, params, type='ORM'):
        if type == 'SQL':
            return cnx.query(params['table']).filter(params['columns'] == params['values']).first()
        else:
            return cnx.query(params['table']).filter(params['columns'] == params['values']).first()
        
    async def insert(self, cnx, params, type='ORM'):
        if type == 'SQL':
            pass
        else:
            createUser = params['table'](*[])
        cnx.add(createUser)
        cnx.commit()