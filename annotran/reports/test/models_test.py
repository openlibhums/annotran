# -*- coding: utf-8 -*-

from h import db
from h.test import factories
from h.groups import models as groups_models
from annotran.pages import models as pages_models
from annotran.languages import models as lang_models
from annotran.reports import models as reports_models

def test_init_when_group_not_none():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    report = reports_models.Report(p, l, g, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert report.id
    assert report.page_id == p.id
    assert report.language_id == l.id
    assert report.group_id == g.id
    assert report.author_id == author.id
    assert report.reporter_id == reporter.id

def test_init_when_group_none():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    report = reports_models.Report(p, l, g, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert report.id
    assert report.page_id == p.id
    assert report.language_id == l.id
    assert report.group_id == g.id
    assert report.author_id == author.id
    assert report.reporter_id == reporter.id


def test_get_by_id_when_id_does_exist():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    report = reports_models.Report(p, l, g, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_by_id(report.id) == report

def test_get_by_id_when_id_does_not_exist():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    assert reports_models.Report.get_by_id(23) is None

def test_get_report_when_group_not_none():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    report = reports_models.Report(p, l, g, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_report(p, l, g, author, reporter) == report


def test_get_report_when_group_none():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    report = reports_models.Report(p, l, g, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_report(p, l, None, author, reporter) == report


def test_get_all():
    author1 = factories.User()
    author2 = factories.User()
    reporter = factories.User()
    db.Session.add(author1)
    db.Session.add(author2)
    db.Session.add(reporter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language", group=g)
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/", language=l)
    db.Session.add(p)
    db.Session.flush()

    report = reports_models.Report(p, l, g, author1, reporter)
    db.Session.add(report)

    report = reports_models.Report(p, l, g, author2, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert len(reports_models.Report.get_all()) == 2