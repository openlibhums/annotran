# -*- coding: utf-8 -*-

from h import db
from h.test import factories
from h.groups import models as groups_models
from annotran.pages import models as pages_models
from annotran.languages import models as lang_models
from annotran.reports import models as reports_models
from annotran.translations import models as tran_models

def test_init():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    report = reports_models.Report(translation, author, reporter)
    db.Session.add(report)
    db.Session.flush()

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

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    report = reports_models.Report(translation, author, reporter)
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

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    assert reports_models.Report.get_by_id(23) is None

def test_get_report():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    report = reports_models.Report(translation, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_report(translation, author, reporter) == report

def test_get_report_translation_is_none():
    author = factories.User()
    reporter = factories.User()
    db.Session.add(author)
    db.Session.add(reporter)

    report = reports_models.Report(None, author, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_report(None, author, reporter) == None

def test_get_report_author_is_none():
    reporter = factories.User()
    db.Session.add(reporter)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    report = reports_models.Report(translation, None, reporter)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_report(translation, None, reporter) == None

def test_get_report_reporter_is_none():
    author = factories.User()
    db.Session.add(author)

    g = groups_models.Group(name="abc_group", creator=factories.User())
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    report = reports_models.Report(translation, author, None)
    db.Session.add(report)
    db.Session.flush()

    assert reports_models.Report.get_report(translation, author, None) == None

def test_get_all():
    author1 = factories.User()
    author2 = factories.User()
    author3 = factories.User()
    reporter = factories.User()
    db.Session.add(author1)
    db.Session.add(author2)
    db.Session.add(author3)
    db.Session.add(reporter)

    g = groups_models.Group(name="Public", creator=factories.User())
    g.id = -1
    g.pubid = "__world__"
    db.Session.add(g)

    l = lang_models.Language(name="abc_language")
    db.Session.add(l)

    p = pages_models.Page(uri="http://www.annotran_test.com/")
    db.Session.add(p)
    db.Session.flush()

    translation = tran_models.Translation(page=p, language=l, group=g)
    db.Session.add(translation)
    db.Session.flush()

    report1 = reports_models.Report(translation, author1, reporter)
    db.Session.add(report1)

    report2 = reports_models.Report(translation, author2, reporter)
    db.Session.add(report2)

    report3 = reports_models.Report(translation, author3, reporter)
    db.Session.add(report3)
    db.Session.flush()

    assert len(reports_models.Report.get_all()) == 3