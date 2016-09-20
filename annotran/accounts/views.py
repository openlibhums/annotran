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
import deform
from h import i18n
from pyramid import httpexceptions
from pyramid.view import view_config
import annotran.views

_ = i18n.TranslationString


class ProfileController:
    def __init__(self):
        pass

    @staticmethod
    @view_config(request_method='GET')
    def profile_get(self):
        """
        Shows the user's profile
        :param self: an instance of the ProfileController
        :return: a context dictionary for the profile template
        """
        return {'email': self.request.authenticated_user.email,
                'email_form': self.forms['email'].render(),
                'password_form': self.forms['password'].render(),
                'support_address': annotran.views.Shared.support_address}

    @staticmethod
    @view_config(request_method='POST')
    def profile_post(self):
        """
        Handle POST payload from profile update form.
        :param self: an instance of the ProfileController
        :return: an HTTP redirect to the user's profile page
        """
        form_id = self.request.POST.get('__formid__')
        if form_id is None or form_id not in self.forms:
            raise httpexceptions.HTTPBadRequest()

        try:
            if form_id == 'email':
                self._handle_email_form()
            elif form_id == 'password':
                self._handle_password_form()
        except deform.ValidationFailure:
            return self.profile_get(self)

        self.request.session.flash(_("Success. We've saved your changes."), 'success')
        return httpexceptions.HTTPFound(
            location=self.request.route_url('profile'))
