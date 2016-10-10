# -*- coding: utf-8 -*-

from h import db
from annotran.pages import models as pages_models

def test_init():
    uri="http://www.annotran_test.com/"

    p = pages_models.Page(uri=uri)
    db.Session.add(p)
    db.Session.flush()

    assert p.id
    assert p.uri == uri

def test_get_by_uri():
    uri="http://www.annotran_test.com/"

    p = pages_models.Page(uri=uri)
    db.Session.add(p)
    db.Session.flush()

    assert pages_models.Page.get_by_uri(uri) == p


def test_get_by_id():
    uri="http://www.annotran_test.com/"

    p = pages_models.Page(uri=uri)
    db.Session.add(p)
    db.Session.flush()

    assert pages_models.Page.get_by_id(p.id) == p