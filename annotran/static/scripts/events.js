/*

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
**/


/**
 * This module extends the set of global events that are dispatched
 * on $rootScope and defined in the same module in h
 */
module.exports = {
    /** Broadcast when a language is added */
    LANGUAGE_ADDED: 'languageAdded',
    /** Broadcast when the session is reloaded */
    SESSION_RELOADED: 'SessionReloaded',
    /** Broadcast when the currently selected language changes */
    LANGUAGE_FOCUSED: 'languageFocused',
    /** Broadcast when the list of groups changes */
    LANGUAGES_CHANGED: 'languagesChanged',
    /** Broadcast when the list of users is loaded*/
    USERS_LOADED: 'usersLoaded',
    /** Broadcast when the currently selected user changes*/
    USERS_FOCUSED: 'userFocused',
    /** Broadcast when the user deleted an annotation*/
    USER_DELETED_ANNOTATION: 'user_deleted_annotation',
    /** Broadcast when moving to another sentence in sentence-by-sentence mode*/
    MOVING_TO_SENTENCE: 'moving_to_sentence',
    /** Broadcast when the rootscope lists are updated*/
    ROOTSCOPE_LISTS_UPDATED: 'rootscope_lists_updated',
};