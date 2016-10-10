"""

Copyright (c) 2013-2014 Hypothes.is Project and contributors

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import decimal

import annotran
import annotran.pages.models
import annotran.votes.models
import h
import h.groups.models
import h.accounts.models
import h.models
import h.session
from annotran.util import util
from annotran.translations.models import Translation as tran_models


def _current_languages(request):
    """
    Get a list of current languages for a group and page. This list is meant to be returned to the client in the
    "session" model.
    :param request: the current request
    :return: a list of languages
    """
    url = util.get_url_from_request(request)

    languages = []
    user_id = request.authenticated_userid

    page = annotran.pages.models.Page.get_by_uri(util.strip_logout(url))

    if page is not None:

        public_translations = tran_models.get_public_translations(page)
        # public_languages = models.Language.get_public(page)

        for language in public_translations:
            languages.append({
                'groupubid': '__world__',
                'name': language.name,
                'id': language.pubid,
                'url': request.route_url('translation_read', public_language_id=language.pubid,
                                         public_group_id='__world__')
            })

        if user_id is None:
            return languages

        user = request.authenticated_user
        if user is None:
            return languages

        # return languages for all groups for that particular user
        translations_for_page = tran_models.get_page_translations(page)
        for group in user.groups:
            # list of languages for a group
            # this needs to also filter by the public group ID
            for language in translations_for_page:
                if group.id == language.group_id:
                    languages.append({
                        'groupubid': group.pubid,
                        'name': language.name,
                        'id': language.pubid,
                        'url': request.route_url('translation_read',
                                                 public_language_id=language.pubid,
                                                 public_group_id=group.pubid)
                    })
    return languages


def _current_votes(request):
    """
    Get votes for all users (authors) who wrote translations on a given page in a specified language. This list is meant
    to be returned to the client in the "session" model
    :param request: the current request
    :return: a list of votes
    """
    votes = []

    url = util.get_url_from_request(request)

    page = annotran.pages.models.Page.get_by_uri(util.strip_logout(url))

    user = request.authenticated_user

    if page is not None:
        public_translations = tran_models.get_public_translations(page)
        # public_languages = models.Language.get_public(page)

        for language in public_translations:
            l_votes = annotran.votes.models.Vote.get_author_scores(page, language)
            if l_votes:
                for auth_score in l_votes:
                    votes.append({
                        'author_id': auth_score.username,
                        'avg_score': str(round(decimal.Decimal(auth_score.average), 2)),
                        'language_id': language.pubid,
                        'group_id': "__world__",
                    })

        if user is None:
            return votes

        translations_for_page = tran_models.get_page_translations(page)
        # languages_for_page = models.Language.get_by_page(page)

        for group in user.groups:
            for language in translations_for_page:
                for auth_score in annotran.votes.models.Vote.get_author_scores(page, language, group):
                    votes.append({
                        'author_id': auth_score.username,
                        'avg_score': str(round(decimal.Decimal(auth_score.average), 2)),
                        'language_id': language.pubid,
                        'group_id': group.pubid,
                    })
    return votes


def model(request):
    """
    Setup the session
    :param request: the current request
    :return: a session object
    """

    # test whether our world group exists in the database
    # normally, in hypothesis, we don't have a world group in the DB
    # we need one so that we can create public languages that also feature in private groups
    # see: https://github.com/birkbeckOLH/annotran/issues/48
    world_group = h.groups.models.Group.get_by_pubid("__world__")

    if not world_group:

        dummy_user = h.accounts.models.User.get_by_username("ADummyUserForGroupCreation")

        # add a dummy user if one doesn't exist
        # NOTE: nobody can login as this user since there is no activation set
        if not dummy_user:
            dummy_user = h.accounts.models.User(username="ADummyUserForGroupCreation", email="dummy@martineve.com",
                                                password="ABCDEFGHIJKLMN0123456789")
            request.db.add(dummy_user)

            # Create a new activation for the user
            activation = h.accounts.models.Activation()
            request.db.add(activation)
            dummy_user.activation = activation

            # Flush the session to ensure that the user can be created and the
            # activation is successfully wired up
            request.db.flush()

        group = h.models.Group(name="Public", creator=dummy_user)
        group.id = -1
        group.pubid = "__world__"
        request.db.add(group)

    session = {'csrf': request.session.get_csrf_token(), 'userid': request.authenticated_userid,
               'groups': h.session._current_groups(request), 'features': h.session.features.all(request),
               'languages': _current_languages(request), 'votes': _current_votes(request), 'preferences': {}}

    user = request.authenticated_user

    if user and not user.sidebar_tutorial_dismissed:
        session['preferences']['show_sidebar_tutorial'] = True

    return session
