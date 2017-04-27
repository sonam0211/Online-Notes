import os
from peewee import Model, CharField, PostgresqlDatabase, ForeignKeyField
from werkzeug.security import generate_password_hash, check_password_hash
from playhouse.db_url import connect
import settings


psql_db = PostgresqlDatabase(
    settings.DB_NAME,
    user = settings.DB_USER,
    password=settings.DB_PASS,
    host=settings.DB_HOST,
    )


if os.environ.get('DATABASE_URL'):
    database = connect(os.environ.get('DATABASE_URL'))
else:
    database = psql_db

class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    name = CharField()
    email = CharField(null=False, unique=True)
    password_hash = CharField()

    @property
    def password(self):
        raise AttributeError('Password is not readable')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Notepad(BaseModel):
    area = CharField()
    user_id = ForeignKeyField(Users, null=False, db_column='user_id')
