from sqlalchemy import Column, MetaData,ForeignKey,Table
from sqlalchemy.dialects.postgresql import (INTEGER,CHAR)
import mytable as mt

meta = MetaData()
myclass = Table("myclass",meta,
            Column("id", INTEGER,primary_key=True),
            Column("name", CHAR(50),ForeignKey(mt.mytable.name)),
            Column("class_name", CHAR(50))
            )
