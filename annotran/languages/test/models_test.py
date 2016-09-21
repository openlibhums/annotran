# -*- coding: utf-8 -*-
import pytest

from h import db
from annotran.languages import models as lang_models
from h.test import factories
from h.groups import models as groups_models
from annotran.pages import models as pages_models


def test_init():
    name = "abc_language"

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name=name, group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    db.Session.flush()

    assert l.id
    assert l.name == name
    #assert language.members == [g] # TODO this would fail beacause of lazy='dynamic' in models.languages

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
    name = "abc_language"

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name=name, group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    db.Session.flush()

    assert repr(l) == name

def test_get_by_id_when_id_does_exist():
    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    db.Session.flush()

    assert lang_models.Language.get_by_id(l.id) == l

def test_get_by_id_when_id_does_not_exist():
    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    db.Session.flush()

    assert lang_models.Language.get_by_id(23) is None

def test_get_public():
    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l1 = lang_models.Language(name="abc_language_1", group=g)
    db.Session.add(l1)

    l2 = lang_models.Language(name="abc_language_2", group=g)
    db.Session.add(l2)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l1)
    p.members.append(l2)
    db.Session.add(p)

    db.Session.flush()

    assert lang_models.Language.get_public(p) == [l1, l2]

def test_get_by_page():
    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l1 = lang_models.Language(name="abc_language_1", group=g)
    db.Session.add(l1)

    l2 = lang_models.Language(name="abc_language_2", group=g)
    db.Session.add(l2)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l1)
    p.members.append(l2)
    db.Session.add(p)

    db.Session.flush()

    assert lang_models.Language.get_by_page(p) == [l1, l2]

def test_get_by_name():
    name="abc_language"

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name=name, group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    db.Session.flush()

    assert lang_models.Language.get_by_name(name) == l


def test_get_by_public_language_id():
    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)

    db.Session.flush()

    assert lang_models.Language.get_by_public_language_id(l.pubid, p) == l


