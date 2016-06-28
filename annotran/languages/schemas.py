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

#this is a code reused from hypothesis, adapted and extended to be used for languages

# -*- coding: utf-8 -*-

import colander
import deform

from h import i18n
from h.accounts.schemas import CSRFSchema
from annotran.languages.models import LANGUAGE_NAME_MIN_LENGTH
from annotran.languages.models import LANGUAGE_NAME_MAX_LENGTH


_ = i18n.TranslationString



class LanguageSchema(CSRFSchema):

    """The schema for the create-a-new-language form."""

    name = colander.SchemaNode(
        colander.String(),
        title=_("What do you want to call the language?"),
        validator=colander.Length(
            min=LANGUAGE_NAME_MIN_LENGTH,
            max=LANGUAGE_NAME_MAX_LENGTH),
        widget=deform.widget.TextInputWidget(
            autofocus=True,
            css_class="language-form__name-input js-language-name-input",
            disable_autocomplete=True,
            label_css_class="language-form__name-label",
            max_length=LANGUAGE_NAME_MAX_LENGTH,
            placeholder=_("Language Name")))
