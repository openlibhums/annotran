# -*- coding: utf-8 -*-
import pytest

from h import db
from annotran.languages import models as lang_models
from h.test import factories
from h.groups import models as groups_models


def test_init():
    name = "My_Annotran_Language"
    user = factories.User()
    g = groups_models.Group(name="abcgroup", creator=user)

    language = lang_models.Language(name=name, group=g)
    db.Session.add(language)
    db.Session.flush()

    assert language.id
    assert language.name == name
    assert language.members == [g]

def test_with_short_name():
    """Should raise ValueError if name shorter than 4 characters."""
    with pytest.raises(ValueError):
        lang_models.Language(name="abc",
                             group=None)

def test_with_long_name():
    """Should raise ValueError if name longer than 25 characters."""
    with pytest.raises(ValueError):
        lang_models.Language(name="abcdefghijklmnopqrstuvwxyz",
                     group=None)
def test_repr():
    name = "My_Annotran_Language"
    g = groups_models.Group(name="abcgroup", creator=factories.User())

    language = lang_models.Language(name=name, group=g)
    db.Session.add(language)
    db.Session.flush()
    print repr(language)

    assert repr(language) == name

def test_get_by_id_when_id_does_exist():
    name = "My_Annotran_Language"
    g = groups_models.Group(name="abcgroup", creator=factories.User())

    language = lang_models.Language(name=name, group=g)
    db.Session.add(language)
    db.Session.flush()

    assert lang_models.Language.get_by_id(language.id) == language

def test_get_by_id_when_id_does_not_exist():
    name = "My_Annotran_Language"
    g = groups_models.Group(name="abcgroup", creator=factories.User())

    language = lang_models.Language(name=name, group=g)
    db.Session.add(language)
    db.Session.flush()

    assert lang_models.Language.get_by_id(23) is None





