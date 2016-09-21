# -*- coding: utf-8 -*-

from h import db
from h.test import factories
from h.groups import models as groups_models
from annotran.languages import models as lang_models
from annotran.pages import models as pages_models


def test_init():
    uri="http://www.annotran_test.com/"

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri=uri, language=l)
    db.Session.add(p)

    db.Session.flush()

    assert p.id
    assert p.uri == uri
    assert p.members == [l]

def test_get_by_uri():
    uri="http://www.annotran_test.com/"

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri=uri, language=l)
    db.Session.add(p)

    db.Session.flush()

    assert pages_models.Page.get_by_uri(uri) == p


def test_get_by_id():
    uri="http://www.annotran_test.com/"

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri=uri, language=l)
    db.Session.add(p)

    db.Session.flush()

    assert pages_models.Page.get_by_id(p.id) == p