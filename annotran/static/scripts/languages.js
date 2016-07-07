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
 * this is a drop-down list for language, and it is created by adapting the original file
 from hypothes.is project: languages.js-!>
**/

/**
 * @ngdoc service
 * @name  languages
 *
 * @description Provides access to the list of languages for available translations.
 *
 *              The list of languages is initialized from the session state
 *              and can then later be updated using the add() method.
 */
'use strict';

var STORAGE_KEY = 'annotran.languages.focus';

// this assumes that h is stored in the same root directory as annotran
var events = require('../../../../../h/h/static/scripts/events.js');

// @ngInject
function languages(localStorage, session, settings, $rootScope, $http) {
  // The currently focused language. Translations displayed are filtered to this language only
  // and any new translations that the user creates
  // will be created for this language.
  var focusedLanguage;
  var focusedGroup;
  var groupPubid;
  
  var map;


  function containsValue(groupubid, language) {
    var i=0, langs = map[groupubid];
    for (i = 0; i < langs.length; i++) {
      if (langs[i] == language) {
        return true;
      }
    }
    return false;
  };

  function all() {
    var languages = [], i;
    for (i = 0; i < session.state.languages.length; i++) {
      var grpubid = session.state.languages[i].groupubid;
      if (!map[grpubid]) {
        map[grpubid] = [];
      }
      map[grpubid].push(session.state.languages[i]);
    }
    return map || [];
  };
  
  function getLanguageList() {
    var result;
    if (groupPubid) {
      if (!map) {
        map = new Object();
        map = all();
      } 
      result = map[groupPubid];
      return result;
    }
  };

  // Return the full object for the language with the given id.
  function get(id) {
    if (gs) {
      var gs = getLanguageList();
      for (var i = 0, max = gs.length; i < max; i++) {
        if (gs[i].id === id) {
          return gs[i];
        }
      }
    }
  };

  function addLanguage(language) {
    var response = $http({
      method: 'POST',
      url: settings.serviceUrl + 'languages/' + language + '/' + groupPubid + '/addLanguage',
    });

    // the language list will be updated in response to a session state
    // change notification from the server. We could improve the UX here
    // by optimistically updating the session state

    return response;
  };

  /** Return the currently focused language. If no language is explicitly focused we
   * will check localStorage to see if we have persisted a focused language from
   * a previous session. Lastly, we fall back to the first language available.
   */
  function focused() {
    if (focusedLanguage && focusedLanguage.groupubid == groupPubid) {
      if (containsValue(groupPubid, focusedLanguage)) {
        return focusedLanguage;
      }
    }
    var fromStorage = get(localStorage.getItem(STORAGE_KEY));
    if (fromStorage && fromStorage.groupubid == groupPubid) {
      focusedLanguage = fromStorage;
      return focusedLanguage;
    }
    if (getLanguageList()) {
      return getLanguageList()[0];
    }    
  }

  /** Set the language with the passed id as the currently focused language. */
  function focus(id) {
    if (id) {
      var g = get(id);
      if (g) {
        focusedLanguage = g;
        localStorage.setItem(STORAGE_KEY, g.id);
        $rootScope.$broadcast(events.LANGUAGES_FOCUSED, g.id);
      }
    }
  };

  // reset the focused language if the user leaves it
  $rootScope.$on(events.LANGUAGES_CHANGED, function () {
    if (focusedLanguage) {
      focusedLanguage = get(focusedLanguage.id);
      if (!focusedLanguage) {
        $rootScope.$broadcast(events.LANGUAGES_FOCUSED, focused());
      }
    }
  });


  $rootScope.$on(events.GROUP_FOCUSED, function (event, groupubid) {
    //load languages for selected group
    groupPubid = groupubid;
    focused();
     /*
    var lid;
    if (focusedLanguage)
        lid = focusedLanguage.id;
    else
        lid = 'None';

    var response = $http({
      method: 'GET',
      url: settings.serviceUrl + 'languages/' + lid + '/' + groupubid,
    });
    */
    return getLanguageList();
  });


  
  return {
    getLanguageList: getLanguageList,
    get: get,
    addLanguage: addLanguage,

    focused: focused,
    focus: focus,
  };
};

module.exports = languages;