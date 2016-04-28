from sqlalchemy import *
from sqlalchemy.orm import *

class LanguageSchema():

    # The schema for the add-a-new-language form.

    # TODO: place metadata somewhere else

    metadata = MetaData('sqlite:///annotran.sqlite')

    language_table = Table('language', metadata,
                           Column('id', Integer, primary_key=True),
                           Column('name', String(20)))