'''

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
'''
# monkey patching of hypothesis methods
from annotran.languages import models
from h import presenters
from h.api import search
from h.api import uri
from pyramid import renderers
from pyramid import httpexceptions as exc
from jinja2 import Environment, PackageLoader
from annotran.util import util

import collections
import h
import annotran
import os.path
import decimal


jinja_env = Environment(loader=PackageLoader(__package__, 'templates'))


# annotran's version of h.groups.views._read_group
def _read_group(request, group, language=None):
    """Return the rendered "Share this group" page.

    This is the page that's shown when a user who is already a member of a
    group visits the group's URL.

    """

    if group is None:
        pubid = "__world__"
        slug = "Public"
    else:
        pubid = group.pubid
        slug = group.slug

    url = request.route_url('group_read', pubid=pubid, slug=slug)

    # language = models.Language.get_by_groupubid(group.pubid)

    result = search.search(request,
                           private=False,
                           params={"group": pubid, "limit": 1000})
    annotations = [presenters.AnnotationHTMLPresenter(h.models.Annotation(a))
                   for a in result['rows']]

    # Group the annotations by URI.
    # Create a dict mapping the (normalized) URIs of the annotated documents
    # to the most recent annotation of each document.
    annotations_by_uri = collections.OrderedDict()
    for annotation in annotations:
        normalized_uri = uri.normalize(annotation.uri)
        if normalized_uri not in annotations_by_uri:
            annotations_by_uri[normalized_uri] = annotation
            if len(annotations_by_uri) >= 25:
                break

    document_links = [annotation.document_link
                      for annotation in annotations_by_uri.values()]

    template_data = {
        'group': group, 'group_url': url, 'document_links': document_links}

    return renderers.render_to_response(
        renderer_name='h:templates/groups/share.html.jinja2',
        value=template_data, request=request)


# annotran's version of h.session.model
def model(request):
    session = {}
    session['csrf'] = request.session.get_csrf_token()
    session['userid'] = request.authenticated_userid
    session['groups'] = h.session._current_groups(request)
    session['features'] = h.session.features.all(request)
    session['languages'] = _current_languages(request)
    session['votes'] = _current_votes(request)
    session['preferences'] = {}
    user = request.authenticated_user
    if user and not user.sidebar_tutorial_dismissed:
        session['preferences']['show_sidebar_tutorial'] = True
    return session

# annotran's version of h.client._angular_template_context
def _angular_template_context_ext(name):
    """Return the context for rendering a 'text/ng-template' <script>
       tag for an Angular directive.
    """
    jinja_env_ext = Environment(loader=PackageLoader(__package__, 'templates'))
    jinja_env = h.client.jinja_env

    # first look if there is a local copy in annotran that we should use
    angular_template_path = 'client/{}.html'.format(name)
    BASE_DIR = os.path.dirname(os.path.realpath(__file__))

    if os.path.isfile('{0}/templates/{1}'.format(BASE_DIR, angular_template_path)):
        content, _, _ = jinja_env_ext.loader.get_source(jinja_env_ext,
                                                        angular_template_path)
    else:
        content, _, _ = jinja_env.loader.get_source(jinja_env,
                                                    angular_template_path)
    return {'name': '{}.html'.format(name), 'content': content}


# annotran's version of h.api.groups.set_group_if_reply
def set_group_if_reply(annotation):
    """If the annotation is a reply set its group to that of its parent.

    If the annotation is a reply to another annotation (or a reply to a reply
    and so on) then it always belongs to the same group as the original
    annotation. If the client sent any 'group' field in the annotation we will
    just overwrite it!

    """

    def is_reply(annotation):
        """Return True if this annotation is a reply."""
        if annotation.get('references'):
            return True
        else:
            return False

    if not is_reply(annotation):
        return

    # Get the top-level annotation that this annotation is a reply
    # (or a reply-to-a-reply etc) to.
    top_level_annotation_id = annotation['references'][0]
    top_level_annotation = models.Annotation.fetch(top_level_annotation_id)

    # If we can't find the top-level annotation, there's nothing we can do, and
    # we should bail.
    if top_level_annotation is None:
        return

    if 'group' in top_level_annotation:
        annotation['group'] = top_level_annotation['group']
        annotation['language'] = top_level_annotation['language']
    else:
        if 'group' in annotation:
            del annotation['group']


def _language_sort_key(language):
    """Sort private languages for the session model list"""

    # languages are sorted first by name but also by ID
    # so that multiple languages with the same name are displayed
    # in a consistent order in clients
    return (language.name.lower(), language.pubid)


def _current_languages(request):
    """Return a list of languages for a given group and page.

    This list is meant to be returned to the client in the "session" model.

    """
    url=util.get_url_from_request(request)

    languages = []
    userid = request.authenticated_userid

    page = annotran.pages.models.Page.get_by_uri(util.strip_logout(url))

    if page is not None:
        public_languages = models.Language.get_public(page)

        for language in public_languages:
            languages.append({
                'groupubid': '__world__',
                'name': language.name,
                'id': language.pubid,
                'url': request.route_url('language_read',
                                         pubid=language.pubid, groupubid='__world__'),
            })

        if userid is None:
            return languages

        user = request.authenticated_user
        if user is None:
            return languages
        # if user is None or get_group(request) is None:
        #   return languages
        # return languages for all groups for that particular user

        languages_for_page = models.Language.get_by_page(page)

        for group in user.groups:
            # list of languages for a group
            # this needs to also filter by grouppubid
            for language in languages_for_page:
                if group in language.members:
                    languages.append({
                        'groupubid': group.pubid,
                        'name': language.name,
                        'id': language.pubid,
                        'url': request.route_url('language_read',
                                                 pubid=language.pubid, groupubid=group.pubid),
                    })
    return languages

def _current_votes(request):
    """Return votes for all users (authors) who made translations on a given page and for a given language

    This list is meant to be returned to the client in the "session" model
    """
    votes = []

    url=util.get_url_from_request(request)

    page = annotran.pages.models.Page.get_by_uri(url)

    user = request.authenticated_user

    if page is not None:
        public_languages = models.Language.get_public(page)


        for language in public_languages:
            l_votes = annotran.votes.models.Vote.get_author_scores_plg(page, language)
            if l_votes:
                for auth_score in l_votes:
                    votes.append({
                        'author_id': auth_score.username,
                        'avg_score': str(round(decimal.Decimal(auth_score.average), 2)),
                    })

        if user is None:
            return votes


        languages_for_page = models.Language.get_by_page(page)

        for group in user.groups:
            for language in languages_for_page:
                if group in language.members:
                    for auth_score in annotran.votes.models.Vote.get_author_scores_plg(page, language, group):
                        votes.append({
                            'author_id': auth_score.username,
                            'avg_score': str(round(decimal.Decimal(auth_score.average), 2)),
                        })
    return votes


def get_group(request):

    if request.matchdict.get('pubid') is None:
        return None
    pubid = request.matchdict["pubid"]
    group = h.groups.models.Group.get_by_pubid(pubid)
    if group is None:
        raise exc.HTTPNotFound()
    return group

# h.client.render_app_html
def render_app_html(webassets_env,
                    service_url,
                    api_url,
                    sentry_public_dsn,
                    ga_tracking_id=None,
                    websocket_url=None,
                    extra={}):
    template = jinja_env.get_template('app.html.jinja2')
    assets_dict = h.client._app_html_context(api_url=api_url,
                                             service_url=service_url,
                                             ga_tracking_id=ga_tracking_id,
                                             sentry_public_dsn=sentry_public_dsn,
                                             webassets_env=webassets_env,
                                             websocket_url=websocket_url)
    return template.render(h.client._merge(assets_dict, extra))


# annotran's version of h.api.groups.set_group_if_reply
def set_group_if_reply(annotation):
    """If the annotation is a reply set its group to that of its parent.

    If the annotation is a reply to another annotation (or a reply to a reply
    and so on) then it always belongs to the same group as the original
    annotation. If the client sent any 'group' field in the annotation we will
    just overwrite it!

    """

    def is_reply(annotation):
        """Return True if this annotation is a reply."""
        if annotation.get('references'):
            return True
        else:
            return False

    if not is_reply(annotation):
        return

    # Get the top-level annotation that this annotation is a reply
    # (or a reply-to-a-reply etc) to.
    top_level_annotation_id = annotation['references'][0]
    top_level_annotation = models.Annotation.fetch(top_level_annotation_id)

    # If we can't find the top-level annotation, there's nothing we can do, and
    # we should bail.
    if top_level_annotation is None:
        return

    if 'group' in top_level_annotation:
        annotation['group'] = top_level_annotation['group']
        annotation['language'] = top_level_annotation['language']
    else:
        if 'group' in annotation:
            del annotation['group']
