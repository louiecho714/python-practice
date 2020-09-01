from sqlalchemy import create_engine
from mytable import Base
from myclass import myclass

# conenction string
# postgresql+psycopg2://user:password@host:port/dbname[?key=value&key=value...]

engine = create_engine("postgresql+psycopg2://postgres:postgres@127.0.1:5432/my_test_data",
                        pool_size=5,max_overflow=4,
                        pool_recycle=7200,pool_timeout=30)


#Base.metadata.create_all(engine)
#myclass.create(bind=engine)

myclass.drop(bind=engine)
Base.metadata.drop_all(engine)
