# -*- coding: utf-8 -*-
import pytest

from h import db
from annotran.languages import models as lang_models


def test_init():
    name = "abc_language"
    l = lang_models.Language(name=name)
    db.Session.add(l)
    db.Session.flush()
    assert l.id
    assert l.name == name


def test_with_short_name():
    """Should raise ValueError if name shorter than 4 characters."""
    with pytest.raises(ValueError):
        lang_models.Language(name="abc")


def test_with_long_name():
    """Should raise ValueError if name longer than 25 characters."""
    with pytest.raises(ValueError):
        lang_models.Language(name="abcdefghijklmnopqrstuvwxyz")


def test_repr():
    name = "abc_language"

    l = lang_models.Language(name=name)
    db.Session.add(l)
    db.Session.flush()

    assert repr(l) == name

def test_get_by_id_when_id_does_exist():
    l = lang_models.Language(name="abc_language")

    db.Session.add(l)
    db.Session.flush()

    assert lang_models.Language.get_by_id(l.id) == l


def test_get_by_id_when_id_does_not_exist():
    l = lang_models.Language(name="abc_language")

    db.Session.add(l)
    db.Session.flush()

    assert lang_models.Language.get_by_id(23) is None

def test_get_by_name():
    name="abc_language"

    l = lang_models.Language(name=name)
    db.Session.add(l)
    db.Session.flush()

    assert lang_models.Language.get_by_name(name) == l

def test_get_by_public_language_id():
    l = lang_models.Language(name="abc_language")

    db.Session.add(l)
    db.Session.flush()

    assert lang_models.Language.get_by_public_language_id(l.pubid) == l
