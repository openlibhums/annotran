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


class Logic:

    # annotran's version of h.api.groups.set_group_if_reply
    @staticmethod
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
