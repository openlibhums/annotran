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

import annotran
import annotran.views
import deform

from h import i18n
from pyramid.view import view_config
from h.accounts import schemas

_ = i18n.TranslationString


def register_controller_init_patch(self, request):
    tos_link = ('<a href="/terms-of-service">' +
                _('Terms of Service') +
                '</a>')
    cg_link = ('<a href="/community-guidelines">' +
               _('Community Guidelines') +
               '</a>')
    privacy_link = ('<a href="/privacy-policy">' +
               _('Privacy Policy') +
               '</a>')
    form_footer = _(
        'You are agreeing to be bound by our {tos_link}, '
        '{cg_link} and {privacy_link}.').format(tos_link=tos_link, cg_link=cg_link, privacy_link=privacy_link)

    self.request = request
    self.schema = schemas.RegisterSchema().bind(request=self.request)
    self.form = deform.Form(self.schema,
                            buttons=(_('Sign up'),),
                            footer=form_footer)


class ProfileController(object):
    def __init__(self):
        pass

    @staticmethod
    @view_config(request_method='GET')
    def profile_get(controller_instance):
        """
        Shows the user's profile
        :param controller_instance: an instance of the ProfileController
        :return: a context dictionary for the profile template
        """
        return {'email': controller_instance.request.authenticated_user.email,
                'email_form': controller_instance.forms['email'].render(),
                'password_form': controller_instance.forms['password'].render(),
                'support_address': annotran.views.Shared.support_address}


def auth_controller_init_patch(self, request):
    """
    Replace the constructor of the h's h.account.views AuthController class - in order to skip the stream loading that
    is not used in the annotran
    :param request: the current request
    :return: None
    """
    form_footer = '<a href="{href}">{text}</a>'.format(
        href=request.route_path('forgot_password'),
        text=_('Forgot your password?'))
    self.request = request
    self.schema = schemas.LoginSchema().bind(request=self.request)
    self.form = deform.Form(self.schema,
                            buttons=(_('Sign in'),),
                            footer=form_footer)
    self.login_redirect = self.request.route_url('index')
    self.logout_redirect = self.request.route_url('index')
