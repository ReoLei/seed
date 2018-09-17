from datetime import datetime

from flask_sqlalchemy import SQLAlchemy, BaseQuery, orm
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

__all__ = ['db', 'ma', 'migrate', 'session', 'BaseModel']



class SeedQuery(BaseQuery):
    def __init__(self, *args, **kwargs):
        super(SeedQuery, self).__init__(*args, **kwargs)


class SessionMixin(object):
    column_filter = []
    
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

    def save(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def row2dict(self):
        d = {}
        for column in self.__table__.columns:
            if column.name not in self.column_filter:
                d[column.name] = getattr(self, column.name)
        return d

db = SQLAlchemy(query_class=SeedQuery)
migrate = Migrate()
session = orm.scoped_session(orm.sessionmaker())
ma = Marshmallow()


class BaseModel(db.Model, SessionMixin):
    __abstract__ = True
    column_filter = ['created', 'updated']

    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow()
    )
    updated = db.Column(
        db.DateTime, default=datetime.utcnow(),
        onupdate=datetime.utcnow()
    )

    def __init__(self, *args, **kwargs):
        super(BaseModel, self).__init__(*args, **kwargs)