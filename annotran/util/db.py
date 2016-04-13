from sqlalchemy import *
from datetime import datetime
from sqlalchemy.orm import *

metadata = MetaData('sqlite:///annotran.sqlite')

user_table = Table(
    't_user', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_name', Unicode(16), unique=True, nullable=False),
    Column('password', Unicode(40), nullable=False),
    Column('display_name', Unicode(255), default=''),
    Column('created', DateTime, default=datetime.now))


group_table = Table(
    't_group', metadata,
    Column('id', Integer, primary_key=True),
    Column('group_name', Unicode(16), unique=True, nullable=False))

permission_table = Table(
    't_permission', metadata,
    Column('id', Integer, primary_key=True),
    Column('permission_name', Unicode(16), unique=True, nullable=False))

user_group_table = Table(
    't_user_group', metadata,
    Column('user_id', None, ForeignKey('t_user.id'), primary_key=True),
    Column('group_id', None, ForeignKey('t_group.id'), primary_key=True))

metadata.create_all()

stmt = user_table.insert()
stmt.execute(user_name='t1', password='t1', display_name='test test')

stmt = user_table.select()
result = stmt.execute().fetchall()
print(result)


class User(object): pass
class Group(object): pass
class Permission(object): pass

mapper(User, user_table)
mapper(Group, group_table)
mapper(Permission, permission_table)

Session = sessionmaker()
session = Session()

# create new user using session object
newuser = User()
newuser.user_name = 'usr'
newuser.password = 'password'
session.add(newuser)
session.commit()


query = session.query(User)
for user in query:
    print user.user_name

for user in query.filter_by(display_name='test test'):
    print user.id, user.user_name, user.password